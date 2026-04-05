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
# ESTILOS GLOBALES
# =========================================================
global_styles = html.Style("""
:root {
    --site-bg: #ffffff;
    --site-bg-soft: #f8fbff;
    --site-text: #101828;
    --site-text-soft: #667085;
    --site-border: rgba(16, 24, 40, 0.06);
}

html {
    scroll-behavior: smooth;
}

body {
    background: var(--site-bg);
    color: var(--site-text);
}

.site-shell {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background:
        radial-gradient(circle at top left, rgba(37,99,235,0.03), transparent 22%),
        linear-gradient(180deg, #ffffff 0%, #ffffff 100%);
}

.site-main {
    flex: 1 0 auto;
    width: 100%;
}

.page-wrapper {
    width: 100%;
}

.page-inner {
    width: 100%;
}

.section-divider {
    height: 1px;
    background: var(--site-border);
    margin: 0;
}

[data-bs-theme="dark"] body {
    background: #0b1220;
    color: #f8fafc;
}

[data-bs-theme="dark"] .site-shell {
    background:
        radial-gradient(circle at top left, rgba(59,130,246,0.05), transparent 22%),
        linear-gradient(180deg, #0b1220 0%, #0b1220 100%);
}

@media (max-width: 768px) {
    .site-main {
        overflow-x: hidden;
    }
}
""")

# =========================================================
# LAYOUT
# =========================================================
app.layout = html.Div(
    [
        global_styles,
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
