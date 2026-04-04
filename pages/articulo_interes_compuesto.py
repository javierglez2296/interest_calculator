import json
from dash import html, register_page
import dash_bootstrap_components as dbc

register_page(
    __name__,
    path="/blog/interes-compuesto",
    name="Interés compuesto",
    title="Qué es el interés compuesto | interescompuesto.app",
    description="Qué es el interés compuesto, cómo funciona y por qué es una de las bases de la inversión a largo plazo."
)

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

json_ld = {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Qué es el interés compuesto y cómo aprovecharlo a largo plazo",
    "description": "Guía práctica para entender el interés compuesto y su impacto en la inversión a largo plazo.",
    "author": {
        "@type": "Person",
        "name": "interescompuesto.app"
    },
    "publisher": {
        "@type": "Organization",
        "name": "interescompuesto.app"
    },
    "mainEntityOfPage": "https://interescompuesto.app/blog/interes-compuesto"
}

layout = dbc.Container(
    [
        html.Script(type="application/ld+json", children=json.dumps(json_ld, ensure_ascii=False)),

        dbc.Row(
            dbc.Col(
                [
                    html.Div("Interés compuesto · 6 min de lectura", className="text-muted mb-3"),
                    html.H1("Qué es el interés compuesto y cómo aprovecharlo a largo plazo", className="fw-bold mb-4"),
                    html.P(
                        "El interés compuesto es uno de los conceptos más potentes de las finanzas personales. "
                        "Consiste en generar rendimientos no solo sobre el capital inicial, sino también sobre los intereses acumulados con el tiempo.",
                        className="lead"
                    ),
                ],
                lg=8
            ),
            className="pt-4 pt-md-5"
        ),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P(
                            "Cuando inviertes y reinviertes los beneficios, tu dinero empieza a crecer sobre una base cada vez mayor. "
                            "Al principio parece lento, pero con los años el efecto se vuelve mucho más visible."
                        ),
                        html.H2("Un ejemplo sencillo", className="h3 mt-4 mb-3"),
                        html.P(
                            "Si inviertes 10.000 € al 7% anual y dejas que los rendimientos se reinviertan, no solo ganas sobre esos 10.000 €. "
                            "Cada año también ganas sobre los beneficios de los años anteriores."
                        ),
                        html.P(
                            "Por eso el tiempo es una variable tan importante. Cuanto antes empieces, más años tendrá tu dinero para trabajar por ti."
                        ),
                        html.H2("Las tres variables clave", className="h3 mt-4 mb-3"),
                        html.Ul(
                            [
                                html.Li("Capital inicial."),
                                html.Li("Aportaciones periódicas."),
                                html.Li("Tiempo y rentabilidad anual media."),
                            ]
                        ),
                        html.P(
                            "Mucha gente se obsesiona con encontrar la inversión perfecta, pero en la práctica suele pesar más ahorrar con constancia, "
                            "invertir durante muchos años y mantener costes bajos."
                        ),
                        html.H2("Qué puede frenar el interés compuesto", className="h3 mt-4 mb-3"),
                        html.Ul(
                            [
                                html.Li("Comisiones altas."),
                                html.Li("Impuestos sobre beneficios realizados."),
                                html.Li("Sacar el dinero demasiado pronto."),
                                html.Li("No ser constante con las aportaciones."),
                            ]
                        ),
                        html.P(
                            "Si quieres hacer tus propios números, puedes usar nuestra calculadora y probar distintos escenarios de aportación, rentabilidad e inflación."
                        ),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H3("Empieza a invertir con costes bajos", className="h5 mb-3"),
                                    html.P(
                                        "Si estás buscando una opción sencilla para empezar a invertir o ahorrar, puedes echar un vistazo a MyInvestor.",
                                        className="mb-3"
                                    ),
                                    dbc.Button(
                                        "Ver MyInvestor",
                                        href=MYINVESTOR_AFFILIATE_URL,
                                        target="_blank",
                                        rel="sponsored noopener noreferrer",
                                        color="primary"
                                    ),
                                ]
                            ),
                            className="shadow-sm border-0 rounded-4 my-4"
                        ),

                        html.H2("Conclusión", className="h3 mt-4 mb-3"),
                        html.P(
                            "El interés compuesto no hace milagros de un día para otro, pero sí puede transformar un ahorro disciplinado en un patrimonio importante "
                            "a largo plazo. La clave suele ser empezar, mantenerte y dejar pasar el tiempo."
                        ),
                    ],
                    lg=8
                )
            ],
            className="pb-5"
        )
    ],
    fluid=True,
    className="py-2 px-3 px-md-4 px-lg-5"
)
