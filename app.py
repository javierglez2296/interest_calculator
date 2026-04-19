import json
from datetime import date

import dash
from dash import Dash, html, dcc, page_container
import dash_bootstrap_components as dbc
from flask import Response, request, jsonify

from components.navbar import build_navbar
from components.footer import build_footer

from utils.supabase_client import get_supabase_admin
from utils.config import HIPOTECA_PRODUCT_CODE

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
# ENDPOINT CHECK PREMIUM (🔥 CLAVE)
# =========================================================
@server.route("/api/check-premium", methods=["POST"])
def check_premium():
    try:
        data = request.get_json(silent=True) or {}
        email = (data.get("email") or "").strip().lower()

        if not email:
            return jsonify({"unlocked": False, "reason": "missing_email"}), 400

        supabase = get_supabase_admin()

        result = (
            supabase.table("purchases")
            .select("email")
            .eq("email", email)
            .eq("premium_active", True)
            .limit(1)
            .execute()
        )

        unlocked = bool(result.data)

        return jsonify({"unlocked": unlocked, "email": email}), 200

    except Exception as e:
        print("❌ Error check-premium:", str(e))
        return jsonify({"unlocked": False}), 500


# =========================================================
# SITEMAP
# =========================================================
@server.route("/sitemap.xml")
def sitemap():
    today = date.today().isoformat()

    urls = []
    for page in dash.page_registry.values():
        path = page.get("path")
        if not path or path == "/404":
            continue

        urls.append(f"""
  <url>
    <loc>{SITE_URL}{path}</loc>
    <lastmod>{today}</lastmod>
  </url>""")

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
        <meta name="theme-color" content="#ffffff">

        <link rel="canonical" href="{SITE_URL}">

        <meta property="og:title" content="{SITE_NAME}">
        <meta property="og:description" content="{SITE_DESCRIPTION}">
        <meta property="og:image" content="{SITE_IMAGE}">

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
            html.Div(page_container, className="page-inner"),
            className="site-main page-wrapper",
        ),

        build_footer(),
    ],
)

# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    app.run_server(debug=True)
