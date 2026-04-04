import json
from dash import Dash, html, dcc, page_container
import dash_bootstrap_components as dbc

from components.navbar import create_navbar
from components.footer import create_footer
from components.disclaimer_afiliados import disclaimer_afiliados

# =========================================================
# CONFIG
# =========================================================
SITE_NAME = "interescompuesto.app"
SITE_URL = "https://interescompuesto.app"
SITE_DESCRIPTION = (
    "Calculadoras financieras en español: interés compuesto, FIRE e hipoteca. "
    "Simula tu inversión, libertad financiera y cuota hipotecaria."
)

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
        create_navbar(),

        html.Main(
            page_container,
            className="flex-grow-1"
        ),

        dbc.Container(
            [
                html.Hr(className="my-4"),
                disclaimer_afiliados(),
            ],
            fluid=True,
            className="px-3 px-md-4 px-lg-5"
        ),

        create_footer(),
    ],
    className="min-vh-100 d-flex flex-column"
)

# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":
    app.run(debug=True)
