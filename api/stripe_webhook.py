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

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        print("❌ Error verificando webhook:", str(e))
        return jsonify({"error": "invalid webhook"}), 400

    # 🎯 Evento clave
    if event["type"] == "checkout.session.completed":

        session = event["data"]["object"]

        email = session.get("customer_details", {}).get("email")

        if email:
            print(f"💰 Pago recibido de: {email}")

            supabase = get_supabase_admin()

            supabase.table("purchases").upsert({
                "email": email,
                "premium_active": True
            }).execute()

    return jsonify({"status": "ok"}), 200
