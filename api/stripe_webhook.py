from flask import request, jsonify
import stripe

from server import server
from utils.config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
from utils.supabase_client import get_supabase_admin

stripe.api_key = STRIPE_SECRET_KEY


@server.route("/api/stripe-webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    if not sig_header:
        return jsonify({"error": "missing signature"}), 400

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        print("❌ Payload inválido:", str(e))
        return jsonify({"error": "invalid payload"}), 400
    except stripe.error.SignatureVerificationError as e:
        print("❌ Firma inválida:", str(e))
        return jsonify({"error": "invalid signature"}), 400
    except Exception as e:
        print("❌ Error general verificando webhook:", str(e))
        return jsonify({"error": "webhook verification failed"}), 400

    event_type = event.get("type")
    event_id = event.get("id")
    data_object = event.get("data", {}).get("object", {})

    # Solo procesamos el evento correcto
    if event_type == "checkout.session.completed":
        session = data_object

        payment_status = session.get("payment_status")
        session_id = session.get("id")
        livemode = session.get("livemode", False)

        customer_details = session.get("customer_details") or {}
        email = (customer_details.get("email") or "").strip().lower()

        client_reference_id = session.get("client_reference_id")
        metadata = session.get("metadata") or {}

        # Seguridad extra: solo activar si realmente está pagado
        if payment_status != "paid":
            print(f"⚠️ Session completada pero no pagada. session_id={session_id}, payment_status={payment_status}")
            return jsonify({"status": "ignored_unpaid"}), 200

        if not email:
            print(f"⚠️ Pago sin email. session_id={session_id}")
            return jsonify({"status": "ignored_no_email"}), 200

        try:
            supabase = get_supabase_admin()

            # OPCIONAL PERO MUY RECOMENDABLE:
            # 1) comprobar si ya procesaste event_id en una tabla stripe_events
            # 2) si no, insertarlo antes o junto con la compra

            result = supabase.table("purchases").upsert(
                {
                    "email": email,
                    "premium_active": True,
                    "stripe_event_id": event_id,
                    "stripe_session_id": session_id,
                    "stripe_livemode": livemode,
                    "client_reference_id": client_reference_id,
                    "product_code": metadata.get("product_code", "premium"),
                },
                on_conflict="email"
            ).execute()

            print(f"✅ Pago registrado: email={email}, session_id={session_id}, livemode={livemode}")

        except Exception as e:
            print("❌ Error guardando en Supabase:", str(e))
            return jsonify({"error": "database error"}), 500

    return jsonify({"status": "ok"}), 200
