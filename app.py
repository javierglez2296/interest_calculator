import json
from datetime import date

import dash
import stripe
from dash import Dash, html, dcc, page_container
import dash_bootstrap_components as dbc
from flask import Response, request, jsonify

from components.navbar import build_navbar
from components.footer import build_footer
from utils.supabase_client import get_supabase_admin
from utils.config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, PREMIUM_PRODUCT_CODE

# =========================================================
# CONFIG
# =========================================================
SITE_NAME = "interescompuesto.app"
SITE_URL = "https://interescompuesto.app"
SITE_DESCRIPTION = (
    "Calculadoras financieras en español: interés compuesto, FIRE e hipoteca. "
    "Simula tu inversión, libertad financiera y cuota hipotecaria."
)
SITE_IMAGE = f"{SITE_URL}/assets/og-default.jpg"
GA_MEASUREMENT_ID = "G-VJS7ZLKTBX"

stripe.api_key = STRIPE_SECRET_KEY

# =========================================================
# APP
# =========================================================
app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[dbc.themes.LUX],
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {"name": "description", "content": SITE_DESCRIPTION},
        {"name": "robots", "content": "index, follow"},
        {"name": "theme-color", "content": "#ffffff"},
        {"charset": "utf-8"},
    ],
    title=SITE_NAME,
    update_title=None,
)

server = app.server

# =========================================================
# STRIPE WEBHOOK
# =========================================================
@server.route("/api/stripe-webhook", methods=["POST"])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            STRIPE_WEBHOOK_SECRET,
        )
    except Exception as e:
        print("❌ Error verificando webhook Stripe:", str(e))
        return jsonify({"error": str(e)}), 400

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        email = (
            session.get("customer_details", {}).get("email")
            or session.get("customer_email")
            or ""
        ).strip().lower()

        if not email:
            print("❌ Webhook sin email")
            return jsonify({"received": True, "warning": "missing_email"}), 200

        try:
            supabase = get_supabase_admin()

            supabase.upsert_purchase(
                {
                    "email": email,
                    "premium_active": True,
                    "product_code": PREMIUM_PRODUCT_CODE,
                    "stripe_session_id": session.get("id"),
                }
            )

            print(f"✅ Premium guardado en Supabase para {email}")

        except Exception as e:
            print("❌ Error guardando compra en Supabase:", str(e))
            return jsonify({"error": "supabase_error"}), 500

    return jsonify({"received": True}), 200


# =========================================================
# API PREMIUM GLOBAL
# =========================================================
@server.route("/api/check-premium", methods=["POST"])
def check_premium():
    try:
        data = request.get_json(silent=True) or {}
        email = (data.get("email") or "").strip().lower()

        if not email:
            return jsonify({"unlocked": False, "reason": "missing_email"}), 400

        supabase = get_supabase_admin()
        result = supabase.check_premium(email)

        return jsonify({
            "unlocked": bool(result),
            "email": email,
        }), 200

    except Exception as e:
        print("❌ Error check-premium:", str(e))
        return jsonify({"unlocked": False, "reason": "server_error"}), 500


# =========================================================
# SITEMAP
# =========================================================
@server.route("/sitemap.xml")
def sitemap():
    today = date.today().isoformat()

    priorities = {
        "/": "1.0",
        "/calculadora": "0.9",
        "/fire": "0.9",
        "/hipoteca": "0.9",
        "/rentabilidad-alquiler": "0.9",
        "/comparador": "0.9",
        "/blog": "0.8",
        "/premium-ok": "0.2",
    }

    changefreqs = {
        "/": "weekly",
        "/calculadora": "weekly",
        "/fire": "weekly",
        "/hipoteca": "weekly",
        "/rentabilidad-alquiler": "weekly",
        "/comparador": "weekly",
        "/blog": "weekly",
        "/premium-ok": "yearly",
    }

    urls = []

    for page in dash.page_registry.values():
        path = page.get("path")

        if not path:
            continue

        if path == "/404" or "not_found" in str(page.get("module", "")).lower():
            continue

        loc = f"{SITE_URL}{path}"
        priority = priorities.get(path, "0.7")
        changefreq = changefreqs.get(path, "monthly")

        if path.startswith("/blog/") and path != "/blog":
            priority = "0.7"
            changefreq = "monthly"

        urls.append(
            f"""
  <url>
    <loc>{loc}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>"""
        )

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{''.join(sorted(urls))}
</urlset>"""

    return Response(xml, mimetype="application/xml")


# =========================================================
# HTML BASE
# =========================================================
app.index_string = f"""
<!DOCTYPE html>
<html lang="es">
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}

        <meta name="description" content="{SITE_DESCRIPTION}">
        <meta name="robots" content="index, follow">

        <link rel="canonical" href="{SITE_URL}">

        <script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            gtag('config', '{GA_MEASUREMENT_ID}');
        </script>
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
"""

# =========================================================
# LAYOUT
# =========================================================
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),

        dcc.Store(
            id="premium-access",
            storage_type="local",
            data={"unlocked": False, "email": None},
        ),

        build_navbar(),

        html.Main(
            html.Div(
                page_container,
                className="page-inner",
            ),
            className="site-main page-wrapper",
        ),

        build_footer(),
    ],
    className="site-shell",
)

# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    app.run_server(debug=True)
