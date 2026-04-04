from dash import html, register_page
import dash_bootstrap_components as dbc

register_page(
    __name__,
    path="/blog",
    name="Blog",
    title="Blog de finanzas | interescompuesto.app",
    description="Artículos sobre interés compuesto, FIRE, inversión indexada e hipotecas."
)

ARTICULOS = [
    {
        "titulo": "Qué es el interés compuesto y cómo aprovecharlo a largo plazo",
        "descripcion": "Descubre cómo funciona el interés compuesto y por qué puede marcar una gran diferencia en tu patrimonio.",
        "url": "/blog/interes-compuesto",
        "categoria": "Interés compuesto",
        "lectura": "6 min"
    },
    {
        "titulo": "Qué es el movimiento FIRE y cuánto dinero necesitas",
        "descripcion": "Aprende qué significa FIRE, cómo calcular tu número objetivo y qué variables importan de verdad.",
        "url": "/blog/fire",
        "categoria": "FIRE",
        "lectura": "7 min"
    },
    {
        "titulo": "Cómo calcular una hipoteca y no cometer errores al comprar vivienda",
        "descripcion": "Te explico cómo estimar la cuota, los intereses y el coste real total de una hipoteca.",
        "url": "/blog/hipoteca",
        "categoria": "Hipoteca",
        "lectura": "8 min"
    },
]

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

layout = dbc.Container(
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

        dbc.Row([article_card(a) for a in ARTICULOS], className="pb-5")
    ],
    fluid=True,
    className="py-2 px-3 px-md-4 px-lg-5"
)
