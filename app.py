import json
from datetime import date

import dash
from dash import Dash, html, dcc, page_container
import dash_bootstrap_components as dbc
from flask import Response

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
# STRUCTURED DATA
# =========================================================
website_json_ld = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": SITE_NAME,
    "url": SITE_URL,
    "description": SITE_DESCRIPTION,
    "inLanguage": "es",
    "potentialAction": {
        "@type": "SearchAction",
        "target": f"{SITE_URL}/blog?q={{search_term_string}}",
        "query-input": "required name=search_term_string",
    },
}

organization_json_ld = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": SITE_NAME,
    "url": SITE_URL,
    "logo": SITE_IMAGE,
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

        <link id="dynamic-canonical" rel="canonical" href="{SITE_URL}">

        <meta property="og:type" content="website">
        <meta property="og:title" content="{SITE_NAME}">
        <meta property="og:description" content="{SITE_DESCRIPTION}">
        <meta id="dynamic-og-url" property="og:url" content="{SITE_URL}">
        <meta property="og:site_name" content="{SITE_NAME}">
        <meta property="og:locale" content="es_ES">
        <meta property="og:image" content="{SITE_IMAGE}">
        <meta property="og:image:alt" content="interescompuesto.app">

        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:title" content="{SITE_NAME}">
        <meta name="twitter:description" content="{SITE_DESCRIPTION}">
        <meta name="twitter:image" content="{SITE_IMAGE}">

        <link rel="preconnect" href="https://www.googletagmanager.com">
        <link rel="preconnect" href="https://www.google-analytics.com">

        <script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            window.gtag = gtag;
            gtag('js', new Date());
            gtag('config', '{GA_MEASUREMENT_ID}');
        </script>

        <script>
            (function() {{
                function updateDynamicMeta() {{
                    var canonical = document.getElementById('dynamic-canonical');
                    var ogUrl = document.getElementById('dynamic-og-url');
                    var cleanUrl = window.location.origin + window.location.pathname;

                    if (canonical) {{
                        canonical.setAttribute('href', cleanUrl);
                    }}
                    if (ogUrl) {{
                        ogUrl.setAttribute('content', cleanUrl);
                    }}
                }}

                document.addEventListener('DOMContentLoaded', updateDynamicMeta);

                var pushState = history.pushState;
                history.pushState = function() {{
                    pushState.apply(history, arguments);
                    setTimeout(updateDynamicMeta, 50);
                }};

                var replaceState = history.replaceState;
                history.replaceState = function() {{
                    replaceState.apply(history, arguments);
                    setTimeout(updateDynamicMeta, 50);
                }};

                window.addEventListener('popstate', function() {{
                    setTimeout(updateDynamicMeta, 50);
                }});
            }})();
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
        dcc.Location(id="global-url", refresh=False),
        dcc.Location(id="url", refresh=False),

        dcc.Store(
            id="premium-access",
            storage_type="local",
            data={"unlocked": False, "source": None},
        ),
        dcc.Store(id="theme-store", storage_type="local"),
        dcc.Store(id="saved-simulations-store", storage_type="local"),

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
