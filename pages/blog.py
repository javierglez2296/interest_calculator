from dash import html, register_page, page_registry
import dash_bootstrap_components as dbc

register_page(
    __name__,
    path="/blog",
    name="Blog",
    title="Blog de finanzas | interescompuesto.app",
    description="Artículos sobre interés compuesto, FIRE, inversión indexada e hipotecas."
)

# =========================================================
# HELPERS
# =========================================================

EXCLUDE_PATHS = [
    "/",
    "/calculadora",
    "/fire",
    "/hipoteca",
    "/rentabilidad-alquiler",
    "/comparador",
    "/blog",  # importante excluir la propia página blog
]


def get_articulos():
    articulos = []

    for page in page_registry.values():
        path = page.get("path")

        # Filtrar páginas que no son artículos
        if not path or path in EXCLUDE_PATHS:
            continue

        # Solo queremos artículos (puedes ajustar esto si quieres)
        # Aquí asumimos que todo lo que no es herramienta es artículo
        if path.startswith("/blog"):
            continue  # por si tienes otros

        titulo = page.get("title", "Artículo")
        descripcion = page.get("description", "")

        # Categoría automática simple
        if "hipoteca" in path:
            categoria = "Hipoteca"
        elif "fire" in path:
            categoria = "FIRE"
        elif "broker" in path or "trade" in path:
            categoria = "Broker"
        elif "cuenta" in path:
            categoria = "Banca"
        else:
            categoria = "Inversión"

        articulos.append(
            {
                "titulo": titulo,
                "descripcion": descripcion,
                "url": path,
                "categoria": categoria,
                "lectura": "6 min",
            }
        )

    # Orden opcional (más nuevos arriba si quieres luego)
    return articulos[::-1]


def article_card(article):
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        [
                            dbc.Badge(article["categoria"], color="light", text_color="dark", className="me-2"),
                            html.Span(article["lectura"], className="text-muted small"),
                        ],
                        className="mb-3"
                    ),
                    html.H2(
                        html.A(
                            article["titulo"],
                            href=article["url"],
                            className="text-decoration-none text-dark stretched-link"
                        ),
                        className="h4 mb-3"
                    ),
                    html.P(article["descripcion"], className="text-muted mb-0"),
                ]
            ),
            className="shadow-sm border-0 rounded-4 h-100 position-relative"
        ),
        md=6,
        lg=4,
        className="mb-4"
    )


# =========================================================
# LAYOUT
# =========================================================

def layout():
    articulos = get_articulos()

    return dbc.Container(
        [
            dbc.Row(
                dbc.Col(
                    [
                        html.H1("Blog", className="fw-bold mb-3"),
                        html.P(
                            "Guías prácticas sobre inversión, libertad financiera e hipotecas.",
                            className="lead text-muted mb-4"
                        ),
                    ],
                    lg=9
                ),
                className="pt-4 pt-md-5"
            ),

            dbc.Row([article_card(a) for a in articulos], className="pb-5")
        ],
        fluid=True,
        className="py-2 px-3 px-md-4 px-lg-5"
    )
