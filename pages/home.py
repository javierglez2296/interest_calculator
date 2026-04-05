import dash
from dash import html, dcc, Output, Input
import dash_bootstrap_components as dbc
from components.disclaimer_afiliados import build_disclaimer

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

# =========================================================
# CONFIG LIBROS
# =========================================================
BOOKS = [
    {
        "title": "Padre Rico, Padre Pobre",
        "subtitle": "El clásico para cambiar tu mentalidad sobre dinero, activos e ingresos.",
        "note": "Ideal para empezar si todavía no piensas en términos de activos, ingresos y patrimonio.",
        "tag": "Principiantes",
        "rating": "4,7/5",
        "cta": "Ver precio",
        "href": "https://amzn.to/4tzZ9aB",
        "image": "https://m.media-amazon.com/images/I/81bsw6fnUiL.jpg",
        "featured": True,
        "category": "empezar",
    },
    {
        "title": "El hombre más rico de Babilonia",
        "subtitle": "Un libro sencillo y muy efectivo para entender ahorro, disciplina y construcción de riqueza.",
        "note": "Muy recomendable si quieres fundamentos simples y fáciles de recordar.",
        "tag": "Principiantes",
        "rating": "4,7/5",
        "cta": "Ver libro",
        "href": "https://amzn.to/4tzviz8",
        "image": "https://m.media-amazon.com/images/I/71xLmdLOIVL.jpg",
        "featured": False,
        "category": "empezar",
    },
    {
        "title": "El inversor inteligente",
        "subtitle": "Una referencia atemporal para invertir con criterio, paciencia y disciplina.",
        "note": "Perfecto si quieres dejar de pensar como especulador y actuar más como inversor.",
        "tag": "Inversión",
        "rating": "4,8/5",
        "cta": "Ver libro",
        "href": "https://amzn.to/4sQ3Lt1",
        "image": "https://m.media-amazon.com/images/I/91+NBrXG-PL.jpg",
        "featured": True,
        "category": "inversion",
    },
    {
        "title": "Un paso por delante de Wall Street",
        "subtitle": "Peter Lynch explica cómo detectar buenas oportunidades con sentido común.",
        "note": "Muy bueno para aprender a observar negocios reales sin complicarte de más.",
        "tag": "Inversión",
        "rating": "4,7/5",
        "cta": "Ver precio",
        "href": "https://amzn.to/3NONGEW",
        "image": "https://m.media-amazon.com/images/I/81yovluA7SL.jpg",
        "featured": False,
        "category": "inversion",
    },
    {
        "title": "The Psychology of Money",
        "subtitle": "Uno de los mejores libros para entender el comportamiento detrás de tus decisiones financieras.",
        "note": "Muy potente para mejorar mentalidad, evitar errores y pensar mejor a largo plazo.",
        "tag": "Mentalidad",
        "rating": "4,8/5",
        "cta": "Comprar en Amazon",
        "href": "https://amzn.to/4vc02Yt",
        "image": "https://m.media-amazon.com/images/I/71g2ednj0JL.jpg",
        "featured": True,
        "category": "mentalidad",
    },
    {
        "title": "Hábitos atómicos",
        "subtitle": "No es un libro de inversión, pero sí una gran base para crear disciplina y consistencia.",
        "note": "Muy útil si sabes lo que debes hacer, pero te cuesta mantenerlo en el tiempo.",
        "tag": "Mentalidad",
        "rating": "4,8/5",
        "cta": "Ver libro",
        "href": "https://amzn.to/4vcvHc5",
        "image": "https://m.media-amazon.com/images/I/91bYsX41DVL.jpg",
        "featured": False,
        "category": "mentalidad",
    },
]

BOOK_TABS = [
    ("empezar", "Empezar"),
    ("inversion", "Inversión"),
    ("mentalidad", "Mentalidad"),
]

# =========================================================
# PAGE CONFIG
# =========================================================
dash.register_page(
    __name__,
    path="/",
    title="Calculadora de interés compuesto, FIRE y hipoteca | interescompuesto.app",
    name="Inicio",
    description=(
        "Descubre cuánto dinero puedes tener en el futuro. Calcula interés compuesto, "
        "FIRE e hipoteca de forma rápida, clara y gratuita."
    ),
)

# =========================================================
# HELPERS UI
# =========================================================
def section_badge(texto, color_class="text-primary"):
    return html.Div(
        texto,
        className=f"small fw-bold {color_class} mb-2",
        style={"letterSpacing": "0.08em", "textTransform": "uppercase"},
    )


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


def hero_metric(label, value):
    return html.Div(
        [
            html.Div(label, className="hero-metric-label"),
            html.Div(value, className="hero-metric-value"),
        ],
        className="hero-metric",
    )


def book_card_v3(book):
    badges = []

    if book.get("featured"):
        badges.append(html.Span("Más recomendado", className="book-featured-badge"))

    badges.extend(
        [
            html.Span(book["tag"], className="book-chip"),
            html.Span(f"⭐ {book['rating']}", className="book-rating"),
        ]
    )

    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    badges,
                    className="d-flex flex-wrap align-items-center gap-2 mb-3",
                ),
                html.Div(
                    html.Img(
                        src=book["image"],
                        alt=book["title"],
                        className="img-fluid",
                        style={
                            "height": "210px",
                            "width": "100%",
                            "objectFit": "contain",
                            "display": "block",
                            "margin": "0 auto",
                        },
                    ),
                    className="book-image-wrap mb-3",
                ),
                html.H3(book["title"], className="h5 fw-bold mb-2"),
                html.P(book["subtitle"], className="text-muted small mb-2"),
                html.P(
                    book.get("note", ""),
                    className="small fw-semibold book-note mb-4",
                ),
                dbc.Button(
                    [
                        html.Span(book.get("cta", "Ver libro")),
                        html.Span(" →", className="ms-1"),
                    ],
                    href=book["href"],
                    target="_blank",
                    rel="sponsored noopener noreferrer",
                    color="dark",
                    className="w-100 rounded-pill fw-semibold book-btn-v3",
                ),
            ]
        ),
        className="book-card-v3 h-100 border-0 shadow-sm rounded-4",
    )


def build_books_grid(category):
    filtered = [book for book in BOOKS if book["category"] == category]
    return html.Div(
        [book_card_v3(book) for book in filtered],
        className="books-grid-v3",
    )


def books_section_v3():
    return html.Section(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                section_badge("Libros recomendados"),
                                html.H2(
                                    "Aprende finanzas con una selección curada",
                                    className="fw-bold mb-3",
                                    style={"fontSize": "clamp(1.9rem, 4vw, 3rem)"},
                                ),
                                html.P(
                                    "No hace falta leer decenas de libros. Estos son algunos de los "
                                    "más útiles para empezar, invertir mejor y desarrollar una mentalidad financiera sólida.",
                                    className="lead text-muted mb-0",
                                ),
                            ],
                            lg=8,
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    html.Div(
                                        "Selección premium",
                                        className="small fw-bold text-dark mb-1",
                                    ),
                                    html.Div(
                                        "Ordenada por intención para que el usuario encuentre antes lo que busca.",
                                        className="text-muted small",
                                    ),
                                ],
                                className="books-side-note",
                            ),
                            lg=4,
                            className="mt-4 mt-lg-0",
                        ),
                    ],
                    className="align-items-end mb-4 mb-lg-5",
                ),
                dcc.Tabs(
                    id="books-tabs",
                    value="empezar",
                    className="books-tabs-wrapper",
                    parent_className="books-tabs-parent",
                    children=[
                        dcc.Tab(
                            label=label,
                            value=value,
                            className="books-tab",
                            selected_className="books-tab books-tab-selected",
                        )
                        for value, label in BOOK_TABS
                    ],
                ),
                html.Div(
                    id="books-tab-content",
                    className="mt-4",
                    children=build_books_grid("empezar"),
                ),
                html.Div(
                    "Desliza para ver más →",
                    className="books-mobile-hint d-lg-none",
                ),
                dbc.Alert(
                    "Algunos enlaces pueden ser de afiliado. Si compras a través de ellos, la web puede recibir una pequeña comisión sin coste extra para ti.",
                    color="light",
                    className="mt-4 rounded-4 border-0 small text-muted mb-0",
                ),
            ],
            fluid=False,
        ),
        className="books-premium-section-v3 py-5 py-lg-6",
    )


# =========================================================
# LAYOUT
# =========================================================
layout = html.Div(
    [
        html.Section(
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Div(
                                        "FINANZAS PERSONALES · INVERSIÓN · HIPOTECA",
                                        className="hero-badge mb-3",
                                    ),
                                    html.H1(
                                        "Calculadoras financieras claras, útiles y pensadas para tomar mejores decisiones",
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
                                            hero_metric("Herramientas", "3 calculadoras"),
                                            hero_metric("Uso", "Gratis"),
                                            hero_metric("Enfoque", "100% práctico"),
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
                                            html.Div(
                                                "Empieza por aquí",
                                                className="text-primary fw-bold small mb-2",
                                            ),
                                            html.H2(
                                                "Tu hoja de ruta financiera",
                                                className="h4 fw-bold mb-3",
                                            ),
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
        books_section_v3(),
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

# =========================================================
# CALLBACKS
# =========================================================
@dash.callback(
    Output("books-tab-content", "children"),
    Input("books-tabs", "value"),
)
def render_books_tab(tab_value):
    return build_books_grid(tab_value)
