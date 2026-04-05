import json
from dash import Dash, html, dcc, page_container
import dash_bootstrap_components as dbc

from components.navbar import build_navbar
from components.footer import build_footer

# =========================================================
# CONFIG
# =========================================================
SITE_NAME = "interescompuesto.app"
SITE_URL = "https://interescompuesto.app"
SITE_DESCRIPTION = (
    "Calculadoras financieras en español: interés compuesto, FIRE e hipoteca. "
    "Simula tu inversión, libertad financiera y cuota hipotecaria."
)

# PON AQUÍ TU ID REAL DE GOOGLE ANALYTICS 4
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
# STRUCTURED DATA
# =========================================================
website_json_ld = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": SITE_NAME,
    "url": SITE_URL,
    "description": SITE_DESCRIPTION,
    "inLanguage": "es",
}

organization_json_ld = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": SITE_NAME,
    "url": SITE_URL,
}

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

        <meta property="og:type" content="website">
        <meta property="og:title" content="{SITE_NAME}">
        <meta property="og:description" content="{SITE_DESCRIPTION}">
        <meta property="og:url" content="{SITE_URL}">
        <meta property="og:site_name" content="{SITE_NAME}">
        <meta property="og:locale" content="es_ES">

        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:title" content="{SITE_NAME}">
        <meta name="twitter:description" content="{SITE_DESCRIPTION}">

        <script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            window.gtag = gtag;
            gtag('js', new Date());
            gtag('config', '{GA_MEASUREMENT_ID}');
        </script>

        <script type="application/ld+json">
            {json.dumps(website_json_ld, ensure_ascii=False)}
        </script>
        <script type="application/ld+json">
            {json.dumps(organization_json_ld, ensure_ascii=False)}
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
        dcc.Store(id="theme-store", storage_type="local"),

        build_navbar(),

        html.Main(
            html.Div(
                page_container,
                className="page-inner"
            ),
            className="site-main page-wrapper"
        ),

        build_footer(),
    ],
    className="site-shell"
)

# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    app.run(debug=True)
