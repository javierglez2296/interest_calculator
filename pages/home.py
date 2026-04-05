import dash
from dash import html
import dash_bootstrap_components as dbc
from components.disclaimer_afiliados import build_disclaimer

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/",
    title="Calculadora de interés compuesto, FIRE y hipoteca | interescompuesto.app",
    name="Inicio",
    description="Descubre cuánto dinero puedes tener en el futuro. Calcula interés compuesto, FIRE e hipoteca de forma rápida y gratuita."
)

# =========================================================
# COMPONENTES
# =========================================================

def teaser_card(titulo, texto, href, boton_texto="Abrir"):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H3(titulo, className="h5 fw-bold mb-2"),
                html.P(texto, className="text-muted small mb-3"),
                dbc.Button(boton_texto, href=href, color="primary", className="w-100"),
            ]
        ),
        className="h-100 shadow-sm border-0 rounded-4 hover-card",
    )

# =========================================================
# HERO SECTION (MUY IMPORTANTE)
# =========================================================

hero = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H1(
                        "Descubre cuánto dinero puedes tener en el futuro",
                        className="display-4 fw-bold mb-3",
                    ),
                    html.P(
                        "Simula tu inversión en 10 segundos y empieza a construir ingresos pasivos hoy.",
                        className="lead text-muted mb-4",
                    ),

                    html.Div(
                        [
                            dbc.Button(
                                "💰 Calcular mi dinero futuro",
                                href="/calculadora",
                                color="primary",
                                size="lg",
                                className="me-2 mb-2 px-4",
                            ),
                            dbc.Button(
                                "Empieza a invertir (gratis)",
                                href=MYINVESTOR_AFFILIATE_URL,
                                target="_blank",
                                color="success",
                                size="lg",
                                className="mb-2 px-4",
                            ),
                        ]
                    ),

                    html.P(
                        "Más de 1.000 personas ya usan estas calculadoras cada mes",
                        className="text-muted small mt-3",
                    ),
                ],
                lg=7,
                className="py-5",
            ),

            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("🚀 Empieza aquí", className="fw-bold mb-3"),
                                html.Ul(
                                    [
                                        html.Li("Calcula tu dinero futuro"),
                                        html.Li("Descubre cuándo puedes jubilarte"),
                                        html.Li("Optimiza tu hipoteca"),
                                        html.Li("Aprende a invertir mejor"),
                                    ],
                                    className="mb-0",
                                ),
                            ]
                        ),
                        className="shadow border-0 rounded-4 p-3",
                    )
                ],
                lg=5,
                className="d-flex align-items-center",
            ),
        ],
        className="align-items-center",
    ),
    fluid=True,
    className="px-4 px-md-5 py-5",
)

# =========================================================
# BLOQUE EMOCIONAL (MUY IMPORTANTE)
# =========================================================

emotional_block = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2(
                            "El tiempo es lo que más dinero genera",
                            className="fw-bold mb-3",
                        ),
                        html.P(
                            "Invertir 300€/mes durante 20 años puede convertirse en más de 150.000€.",
                            className="lead text-muted",
                        ),
                        html.P(
                            "La mayoría empieza demasiado tarde. Tú aún estás a tiempo.",
                            className="text-muted",
                        ),
                    ],
                    md=8,
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            "Ver simulación ahora",
                            href="/calculadora",
                            color="primary",
                            size="lg",
                            className="w-100",
                        )
                    ],
                    md=4,
                    className="d-flex align-items-center",
                ),
            ],
            className="align-items-center bg-light rounded-4 p-4 shadow-sm",
        )
    ],
    fluid=True,
    className="px-4 px-md-5 my-5",
)

# =========================================================
# CALCULADORAS
# =========================================================

calculadoras = dbc.Container(
    [
        html.H2("Calculadoras", className="fw-bold mb-4"),
        dbc.Row(
            [
                dbc.Col(
                    teaser_card(
                        "💰 Interés compuesto",
                        "Descubre cuánto crecerá tu dinero con el tiempo.",
                        "/calculadora",
                        "Calcular",
                    ),
                    md=4,
                    className="mb-4",
                ),
                dbc.Col(
                    teaser_card(
                        "🔥 FIRE",
                        "Calcula cuándo podrás dejar de trabajar.",
                        "/fire",
                        "Descubrir",
                    ),
                    md=4,
                    className="mb-4",
                ),
                dbc.Col(
                    teaser_card(
                        "🏠 Hipoteca",
                        "Calcula tu cuota y el coste real de tu vivienda.",
                        "/hipoteca",
                        "Simular",
                    ),
                    md=4,
                    className="mb-4",
                ),
            ]
        ),
    ],
    fluid=True,
    className="px-4 px-md-5",
)

# =========================================================
# CTA AFILIADOS (DINERO)
# =========================================================

cta_inversion = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H3("Empieza a invertir hoy", className="fw-bold mb-3"),
                    html.P(
                        "No necesitas miles de euros. Puedes empezar con muy poco y aprovechar el interés compuesto.",
                        className="text-muted",
                    ),
                ],
                md=8,
            ),
            dbc.Col(
                [
                    dbc.Button(
                        "Abrir cuenta gratis",
                        href=MYINVESTOR_AFFILIATE_URL,
                        target="_blank",
                        color="success",
                        size="lg",
                        className="w-100",
                    )
                ],
                md=4,
                className="d-flex align-items-center",
            ),
        ],
        className="align-items-center bg-success bg-opacity-10 rounded-4 p-4 shadow-sm",
    ),
    fluid=True,
    className="px-4 px-md-5 my-5",
)

# =========================================================
# ARTÍCULOS
# =========================================================

articulos = dbc.Container(
    [
        html.H2("Aprende a invertir mejor", className="fw-bold mb-4"),
        dbc.Row(
            [
                dbc.Col(
                    teaser_card(
                        "Qué es el interés compuesto",
                        "La clave para multiplicar tu dinero a largo plazo.",
                        "/blog/interes-compuesto",
                        "Leer",
                    ),
                    md=4,
                    className="mb-4",
                ),
                dbc.Col(
                    teaser_card(
                        "Cuánto necesitas para FIRE",
                        "Descubre tu número de libertad financiera.",
                        "/blog/fire",
                        "Leer",
                    ),
                    md=4,
                    className="mb-4",
                ),
                dbc.Col(
                    teaser_card(
                        "Hipoteca: guía completa",
                        "Evita errores que pueden costarte miles de euros.",
                        "/blog/hipoteca",
                        "Leer",
                    ),
                    md=4,
                    className="mb-4",
                ),
            ]
        ),
    ],
    fluid=True,
    className="px-4 px-md-5",
)

# =========================================================
# LAYOUT FINAL
# =========================================================

layout = html.Div(
    [
        hero,
        emotional_block,
        calculadoras,
        cta_inversion,
        build_disclaimer(),
        articulos,
    ]
)
