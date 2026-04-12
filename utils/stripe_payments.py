import os
import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def create_premium_checkout_session(success_url, cancel_url, customer_email=None, user_id=None):
    metadata = {}
    if user_id:
        metadata["user_id"] = str(user_id)

    session = stripe.checkout.Session.create(
        mode="payment",  # usa "subscription" si quieres mensual
        line_items=[
            {
                "price": os.getenv("STRIPE_PREMIUM_PRICE_ID"),
                "quantity": 1,
            }
        ],
        success_url=success_url,
        cancel_url=cancel_url,
        customer_email=customer_email,
        metadata=metadata,
    )
    return session
