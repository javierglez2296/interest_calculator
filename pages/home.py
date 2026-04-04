import dash
from dash import html
import dash_bootstrap_components as dbc
from components.disclaimer_afiliados import build_disclaimer

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/",
    title="Inicio | Interés Compuesto",
    name="Inicio",
    description="Calculadoras financieras en español para interés compuesto, FIRE e hipoteca. Simula inversión, libertad financiera y cuota hipotecaria."
)

def teaser_card(titulo, texto, href, boton_texto="Abrir"):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H3(titulo, className="h4 fw-bold"),
                html.P(texto, className="text-muted"),
                dbc.Button(boton_texto, href=href, color="primary"),
            ]
        ),
        className="h-100 shadow-sm border-0 rounded-4",
    )

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1(
                            "Calculadoras financieras en español",
                            className="display-5 fw-bold mb-3"
                        ),
                        html.P(
                            "Calcula el crecimiento de tu inversión con interés compuesto, estima tu número FIRE "
                            "y simula la cuota de tu hipoteca con herramientas claras, rápidas y gratuitas.",
                            className="lead text-muted"
                        ),
                        html.Div(
                            [
                                dbc.Button(
                                    "Calcular interés compuesto",
                                    href="/calculadora",
                                    color="primary",
                                    className="me-2 mb-2",
                                ),
                                dbc.Button(
                                    "Ver opción MyInvestor",
                                    href=MYINVESTOR_AFFILIATE_URL,
                                    target="_blank",
                                    color="success",
                                    className="mb-2",
                                ),
                            ]
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
                                    html.H4("Empieza por aquí", className="fw-bold"),
                                    html.Ul(
                                        [
                                            html.Li("Interés compuesto"),
                                            html.Li("FIRE"),
                                            html.Li("Hipoteca"),
                                            html.Li("Artículos prácticos"),
                                        ]
                                    )
                                ]
                            ),
                            className="shadow-sm border-0 rounded-4 mt-4 mt-lg-5",
                        )
                    ],
                    lg=5,
                ),
            ],
            className="align-items-center py-4 py-md-5",
        ),

        build_disclaimer(),

        html.H2("Calculadoras", className="fw-bold mt-5 mb-4"),
        dbc.Row(
            [
                dbc.Col(
                    teaser_card(
                        "Calculadora de interés compuesto",
                        "Simula capital inicial, aportaciones mensuales, rentabilidad, inflación y comisiones.",
                        "/calculadora",
                    ),
                    md=4,
                    className="mb-4",
                ),
                dbc.Col(
                    teaser_card(
                        "Calculadora FIRE",
                        "Calcula cuánto necesitas para alcanzar la independencia financiera.",
                        "/fire",
                    ),
                    md=4,
                    className="mb-4",
                ),
                dbc.Col(
                    teaser_card(
                        "Calculadora de hipoteca",
                        "Estima la cuota mensual y consulta un cuadro de amortización simple.",
                        "/hipoteca",
                    ),
                    md=4,
                    className="mb-4",
                ),
            ]
        ),

        html.H2("Artículos destacados", className="fw-bold mt-5 mb-4"),
        dbc.Row(
            [
                dbc.Col(
                    teaser_card(
                        "Qué es el interés compuesto y cómo aprovecharlo",
                        "Una guía clara para entender por qué el largo plazo importa tanto.",
                        "/blog/interes-compuesto",
                        "Leer",
                    ),
                    md=4,
                    className="mb-4",
                ),
                dbc.Col(
                    teaser_card(
                        "Cuánto necesitas para FIRE",
                        "La lógica detrás de la regla del 4% y cómo hacer tus propios números.",
                        "/blog/fire",
                        "Leer",
                    ),
                    md=4,
                    className="mb-4",
                ),
                dbc.Col(
                    teaser_card(
                        "Hipoteca fija o variable",
                        "Claves para entender la cuota, el coste total y el riesgo.",
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
