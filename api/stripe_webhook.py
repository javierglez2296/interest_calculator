from flask import request, jsonify
import stripe

from server import server
from utils.config import (
    STRIPE_SECRET_KEY,
    STRIPE_WEBHOOK_SECRET,
    PREMIUM_PRODUCT_CODE,
)
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
            secret=STRIPE_WEBHOOK_SECRET,
        )
    except ValueError as e:
        print("❌ Payload inválido:", str(e))
        return jsonify({"error": "invalid payload"}), 400
    except stripe.error.SignatureVerificationError as e:
        print("❌ Firma inválida:", str(e))
        return jsonify({"error": "invalid signature"}), 400
    except Exception as e:
        print("❌ Error verificando webhook:", str(e))
        return jsonify({"error": "verification failed"}), 400

    event_type = event.get("type")
    event_id = event.get("id")
    obj = event.get("data", {}).get("object", {})

    if event_type == "checkout.session.completed":
        session = obj

        payment_status = session.get("payment_status")
        session_id = session.get("id")
        livemode = session.get("livemode", False)

        customer_details = session.get("customer_details") or {}
        email = (customer_details.get("email") or "").strip().lower()

        payment_link_id = session.get("payment_link")
        metadata = session.get("metadata") or {}
        product_code = metadata.get("product_code") or PREMIUM_PRODUCT_CODE

        if payment_status != "paid":
            print(f"⚠️ Session completada pero no pagada: {session_id} / {payment_status}")
            return jsonify({"status": "ignored_unpaid"}), 200

        if not email:
            print(f"⚠️ Session sin email: {session_id}")
            return jsonify({"status": "ignored_no_email"}), 200

        try:
            supabase = get_supabase_admin()

            existing = (
                supabase.table("purchases")
                .select("id")
                .eq("stripe_event_id", event_id)
                .limit(1)
                .execute()
            )

            if existing.data:
                print(f"ℹ️ Evento ya procesado: {event_id}")
                return jsonify({"status": "already_processed"}), 200

            supabase.table("purchases").upsert(
                {
                    "email": email,
                    "product_code": product_code,
                    "premium_active": True,
                    "stripe_event_id": event_id,
                    "stripe_session_id": session_id,
                    "stripe_payment_link_id": payment_link_id,
                    "stripe_livemode": livemode,
                    "customer_email": email,
                },
                on_conflict="email,product_code",
            ).execute()

            print(f"✅ Premium global activado para {email}")

        except Exception as e:
            print("❌ Error guardando compra en Supabase:", str(e))
            return jsonify({"error": "database_error"}), 500

    return jsonify({"status": "ok"}), 200
