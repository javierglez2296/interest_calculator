import dash
from dash import html
import dash_bootstrap_components as dbc
from components.disclaimer_afiliados import build_disclaimer

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

# =========================================================
# AMAZON AFILIADOS
# =========================================================
# Sustituye estos links por tus enlaces reales de Amazon Afiliados
BOOKS = [
    {
        "title": "Padre Rico, Padre Pobre",
        "subtitle": "El clásico para cambiar tu mentalidad sobre dinero, activos e ingresos.",
        "tag": "Para empezar",
        "rating": "4,7/5",
        "cta": "Ver en Amazon",
        "href": "https://www.amazon.es/",
        "image": "https://m.media-amazon.com/images/I/81bsw6fnUiL.jpg",
    },
    {
        "title": "El inversor inteligente",
        "subtitle": "Una referencia atemporal para entender inversión con criterio y disciplina.",
        "tag": "Inversión clásica",
        "rating": "4,8/5",
        "cta": "Ver en Amazon",
        "href": "https://www.amazon.es/",
        "image": "https://m.media-amazon.com/images/I/91+NBrXG-PL.jpg",
    },
    {
        "title": "The Psychology of Money",
        "subtitle": "Uno de los mejores libros para entender por qué invertimos como invertimos.",
        "tag": "Mentalidad",
        "rating": "4,8/5",
        "cta": "Ver en Amazon",
        "href": "https://www.amazon.es/",
        "image": "https://m.media-amazon.com/images/I/71g2ednj0JL.jpg",
    },
]


dash.register_page(
    __name__,
    path="/",
    title="Calculadora de interés compuesto, FIRE y hipoteca | interescompuesto.app",
    name="Inicio",
    description=(
        "Descubre cuánto dinero puedes tener en el futuro. Calcula interés compuesto, "
        "FIRE e hipoteca de forma rápida y gratuita."
    ),
)

# =========================================================
# COMPONENTES
# =========================================================
def teaser_card(titulo, texto, href, boton_texto="Abrir", icono="→"):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(icono, className="feature-icon mb-3"),
                html.H3(titulo, className="h5 fw-bold mb-2"),
                html.P(texto, className="text-muted small mb-3"),
                dbc.Button(
                    boton_texto,
                    href=href,
                    color="primary",
                    className="w-100 rounded-pill fw-semibold",
                ),
            ]
        ),
        className="feature-card h-100 border-0 shadow-sm rounded-4",
    )


def book_card(book):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.Span(book["tag"], className="book-chip"),
                        html.Span(f"⭐ {book['rating']}", className="book-rating"),
                    ],
                    className="d-flex justify-content-between align-items-center mb-3",
                ),
                html.Div(
                    html.Img(
                        src=book["image"],
                        alt=book["title"],
                        className="img-fluid",
                        style={
                            "maxHeight": "180px",
                            "objectFit": "contain",
                            "borderRadius": "14px",
                        },
                    ),
                    className="text-center mb-3",
                ),
                html.H3(book["title"], className="h5 fw-bold mb-2"),
                html.P(book["subtitle"], className="text-muted small mb-4"),
                dbc.Button(
                    [
                        html.Span(book["cta"]),
                        html.Span(" →", className="ms-1"),
                    ],
                    href=book["href"],
                    target="_blank",
                    rel="sponsored noopener noreferrer",
                    color="dark",
                    className="w-100 rounded-pill fw-semibold book-btn",
                ),
            ]
        ),
        className="book-card h-100 border-0 shadow-sm rounded-4",
    )


def books_section():
    return html.Section(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div("RECOMENDADOS", className="section-kicker"),
                                html.H2(
                                    "Libros de finanzas e inversión que merecen la pena",
                                    className="fw-bold display-6 mb-3",
                                ),
                                html.P(
                                    "Si estás mejorando tus finanzas, aprendiendo a invertir o "
                                    "buscando construir patrimonio a largo plazo, esta selección "
                                    "te puede ahorrar años de errores.",
                                    className="lead text-muted mb-0",
                                ),
                            ],
                            lg=8,
                        ),
                        dbc.Col(
                            html.Div(
                                dbc.Button(
                                    "Ver más recomendaciones",
                                    href="/blog",
                                    color="light",
                                    className="rounded-pill px-4 py-2 fw-semibold border",
                                ),
                                className="d-flex justify-content-lg-end align-items-lg-center h-100 mt-3 mt-lg-0",
                            ),
                            lg=4,
                        ),
                    ],
                    className="align-items-center mb-4 mb-lg-5",
                ),
                dbc.Row(
                    [dbc.Col(book_card(book), md=6, lg=4, className="mb-4") for book in BOOKS],
                    className="g-4",
                ),
                dbc.Row(
                    dbc.Col(
                        dbc.Alert(
                            [
                                html.Span("Aviso: "),
                                "algunos enlaces pueden ser de afiliado. Si compras a través de ellos, "
                                "la web puede recibir una pequeña comisión sin coste extra para ti.",
                            ],
                            color="light",
                            className="mt-4 rounded-4 border-0 small text-muted mb-0",
                        ),
                        width=12,
                    )
                ),
            ],
            fluid=False,
        ),
        className="books-premium-section py-5 py-lg-6",
    )


# =========================================================
# LAYOUT
# =========================================================
layout = html.Div(
    [
        html.Style(
            """
            .home-hero {
                background:
                    radial-gradient(circle at top left, rgba(13,110,253,0.10), transparent 35%),
                    radial-gradient(circle at top right, rgba(25,135,84,0.10), transparent 30%),
                    linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
                padding-top: 4rem;
                padding-bottom: 4rem;
            }

            .hero-badge {
                display: inline-block;
                background: #eef4ff;
                color: #0d6efd;
                border: 1px solid #d7e6ff;
                padding: 0.45rem 0.85rem;
                border-radius: 999px;
                font-size: 0.82rem;
                font-weight: 700;
                letter-spacing: 0.02em;
            }

            .hero-title {
                font-size: clamp(2.1rem, 5vw, 4.2rem);
                line-height: 1.05;
                letter-spacing: -0.04em;
            }

            .hero-subtitle {
                font-size: 1.05rem;
                color: #5c667a;
                max-width: 760px;
            }

            .hero-metrics {
                display: flex;
                flex-wrap: wrap;
                gap: 0.8rem;
                margin-top: 1.5rem;
            }

            .hero-metric {
                background: rgba(255,255,255,0.78);
                border: 1px solid rgba(15,23,42,0.06);
                box-shadow: 0 10px 30px rgba(15,23,42,0.06);
                border-radius: 18px;
                padding: 0.9rem 1rem;
                min-width: 150px;
            }

            .hero-metric-label {
                font-size: 0.78rem;
                color: #667085;
                margin-bottom: 0.25rem;
            }

            .hero-metric-value {
                font-size: 1.1rem;
                font-weight: 800;
                color: #101828;
            }

            .feature-card {
                transition: all 0.22s ease;
                background: #ffffff;
            }

            .feature-card:hover,
            .book-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 18px 45px rgba(15,23,42,0.10) !important;
            }

            .feature-icon {
                width: 48px;
                height: 48px;
                border-radius: 14px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(135deg, #eef4ff 0%, #f5f8ff 100%);
                font-size: 1.2rem;
            }

            .books-premium-section {
                background:
                    linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
            }

            .section-kicker {
                display: inline-block;
                font-size: 0.78rem;
                font-weight: 800;
                letter-spacing: 0.08em;
                color: #0d6efd;
                margin-bottom: 0.85rem;
            }

            .book-card {
                background: linear-gradient(180deg, #ffffff 0%, #fcfdff 100%);
                transition: all 0.22s ease;
            }

            .book-chip {
                display: inline-flex;
                align-items: center;
                padding: 0.35rem 0.7rem;
                background: #eef4ff;
                color: #0d6efd;
                border-radius: 999px;
                font-size: 0.75rem;
                font-weight: 700;
            }

            .book-rating {
                font-size: 0.8rem;
                font-weight: 700;
                color: #344054;
            }

            .book-btn {
                box-shadow: 0 8px 20px rgba(17,24,39,0.10);
            }

            .soft-section {
                padding-top: 4rem;
                padding-bottom: 4rem;
            }

            @media (max-width: 768px) {
                .hero-title {
                    font-size: 2.3rem;
                }

                .hero-subtitle {
                    font-size: 1rem;
                }

                .hero-metrics {
                    gap: 0.6rem;
                }

                .hero-metric {
                    flex: 1 1 calc(50% - 0.6rem);
                    min-width: unset;
                }
            }
            """
        ),

        # HERO
        html.Section(
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Div("FINANZAS PERSONALES · INVERSIÓN · HIPOTECA", className="hero-badge mb-3"),
                                    html.H1(
                                        "Calculadoras financieras claras, útiles y hechas para tomar mejores decisiones",
                                        className="hero-title fw-bold mb-3",
                                    ),
                                    html.P(
                                        "Simula tu interés compuesto, calcula tu objetivo FIRE y estima tu hipoteca "
                                        "de forma sencilla. Todo en español, sin ruido y con enfoque práctico.",
                                        className="hero-subtitle mb-4",
                                    ),
                                    html.Div(
                                        [
                                            dbc.Button(
                                                "Probar calculadora",
                                                href="/calculadora",
                                                color="primary",
                                                className="rounded-pill px-4 py-2 fw-semibold me-2 mb-2",
                                            ),
                                            dbc.Button(
                                                "Ver calculadora hipoteca",
                                                href="/hipoteca",
                                                color="light",
                                                className="rounded-pill px-4 py-2 fw-semibold border mb-2",
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Div("Herramientas", className="hero-metric-label"),
                                                    html.Div("3 calculadoras", className="hero-metric-value"),
                                                ],
                                                className="hero-metric",
                                            ),
                                            html.Div(
                                                [
                                                    html.Div("Uso", className="hero-metric-label"),
                                                    html.Div("Gratis", className="hero-metric-value"),
                                                ],
                                                className="hero-metric",
                                            ),
                                            html.Div(
                                                [
                                                    html.Div("Enfoque", className="hero-metric-label"),
                                                    html.Div("100% práctico", className="hero-metric-value"),
                                                ],
                                                className="hero-metric",
                                            ),
                                        ],
                                        className="hero-metrics",
                                    ),
                                ],
                                lg=7,
                                className="mb-4 mb-lg-0",
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.Div("Empieza por aquí", className="text-primary fw-bold small mb-2"),
                                            html.H2("Tu hoja de ruta financiera", className="h4 fw-bold mb-3"),
                                            html.P(
                                                "Explora las tres áreas clave de la web: inversión, independencia "
                                                "financiera y compra de vivienda.",
                                                className="text-muted small mb-4",
                                            ),
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        teaser_card(
                                                            "Interés compuesto",
                                                            "Descubre cuánto puede crecer tu dinero con aportaciones periódicas.",
                                                            "/calculadora",
                                                            "Abrir calculadora",
                                                            "📈",
                                                        ),
                                                        md=12,
                                                        className="mb-3",
                                                    ),
                                                    dbc.Col(
                                                        teaser_card(
                                                            "FIRE",
                                                            "Calcula cuánto necesitas para vivir de tus inversiones.",
                                                            "/fire",
                                                            "Ver FIRE",
                                                            "🔥",
                                                        ),
                                                        md=12,
                                                        className="mb-3",
                                                    ),
                                                    dbc.Col(
                                                        teaser_card(
                                                            "Hipoteca",
                                                            "Estima cuota, coste total y esfuerzo financiero antes de comprar.",
                                                            "/hipoteca",
                                                            "Calcular hipoteca",
                                                            "🏠",
                                                        ),
                                                        md=12,
                                                    ),
                                                ]
                                            ),
                                        ]
                                    ),
                                    className="border-0 shadow-sm rounded-4 h-100",
                                ),
                                lg=5,
                            ),
                        ],
                        className="align-items-center",
                    )
                ]
            ),
            className="home-hero",
        ),

        # BLOQUE PREMIUM LIBROS
        books_section(),

        # DISCLAIMER AFILIADOS
        dbc.Container(
            build_disclaimer(
                text=(
                    "Algunos enlaces de esta web pueden ser de afiliado. Esto significa que "
                    "podemos recibir una pequeña comisión si decides contratar o comprar desde ellos, "
                    "sin coste adicional para ti."
                )
            ),
            className="pb-4",
        ),
    ]
)
