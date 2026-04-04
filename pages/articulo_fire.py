import json
from dash import html, register_page
import dash_bootstrap_components as dbc

register_page(
    __name__,
    path="/blog/fire",
    name="FIRE",
    title="Qué es FIRE y cuánto dinero necesitas | interescompuesto.app",
    description="Descubre qué es el movimiento FIRE, cómo calcular tu objetivo y qué errores evitar."
)

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

json_ld = {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Qué es el movimiento FIRE y cuánto dinero necesitas",
    "description": "Guía básica para entender FIRE y calcular una cifra objetivo razonable.",
    "author": {
        "@type": "Person",
        "name": "interescompuesto.app"
    },
    "publisher": {
        "@type": "Organization",
        "name": "interescompuesto.app"
    },
    "mainEntityOfPage": "https://interescompuesto.app/blog/fire"
}

layout = dbc.Container(
    [
        html.Script(type="application/ld+json", children=json.dumps(json_ld, ensure_ascii=False)),

        dbc.Row(
            dbc.Col(
                [
                    html.Div("FIRE · 7 min de lectura", className="text-muted mb-3"),
                    html.H1("Qué es el movimiento FIRE y cuánto dinero necesitas", className="fw-bold mb-4"),
                    html.P(
                        "FIRE significa Financial Independence, Retire Early. La idea central es acumular suficiente patrimonio "
                        "como para que tus inversiones cubran tus gastos, dándote más libertad sobre tu tiempo.",
                        className="lead"
                    ),
                ],
                lg=8
            ),
            className="pt-4 pt-md-5"
        ),

        dbc.Row(
            dbc.Col(
                [
                    html.P(
                        "No hace falta dejar de trabajar a los 35 para que FIRE tenga sentido. Mucha gente usa esta filosofía "
                        "simplemente para ganar seguridad financiera y reducir dependencia del sueldo."
                    ),
                    html.H2("La regla del 4%", className="h3 mt-4 mb-3"),
                    html.P(
                        "Una referencia conocida es multiplicar tus gastos anuales por 25. "
                        "Por ejemplo, si gastas 20.000 € al año, tu objetivo FIRE teórico sería 500.000 €."
                    ),
                    html.P(
                        "Es una aproximación útil, no una verdad absoluta. Depende de tu país, impuestos, rentabilidad futura, "
                        "edad, flexibilidad de gasto y tolerancia al riesgo."
                    ),
                    html.H2("Qué variables importan más", className="h3 mt-4 mb-3"),
                    html.Ul(
                        [
                            html.Li("Tu nivel de gasto anual."),
                            html.Li("Tu tasa de ahorro."),
                            html.Li("Los años que inviertes."),
                            html.Li("La rentabilidad real de tu cartera."),
                        ]
                    ),
                    html.P(
                        "Normalmente, la tasa de ahorro tiene un impacto enorme. Cuanto más ahorras e inviertes, antes te acercas a la independencia financiera."
                    ),
                    html.H2("Errores frecuentes", className="h3 mt-4 mb-3"),
                    html.Ul(
                        [
                            html.Li("Usar rentabilidades demasiado optimistas."),
                            html.Li("No tener en cuenta inflación e impuestos."),
                            html.Li("Olvidar que los gastos cambian con la vida."),
                            html.Li("Plantearlo como un todo o nada."),
                        ]
                    ),
                    html.P(
                        "Lo más útil suele ser verlo como un proceso gradual: primero un colchón, luego una cartera que cubra una parte de tus gastos, "
                        "y más adelante una independencia más completa."
                    ),

                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("Una opción para empezar a invertir", className="h5 mb-3"),
                                html.P(
                                    "Si quieres empezar a construir patrimonio a largo plazo, puedes revisar opciones como MyInvestor.",
                                    className="mb-3"
                                ),
                                dbc.Button(
                                    "Descubrir MyInvestor",
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
                        "FIRE no va solo de jubilarte pronto. Va de tener margen, opciones y menos dependencia financiera. "
                        "Aunque nunca busques retirarte antes, aplicar parte de esta filosofía puede mejorar mucho tu situación."
                    ),
                ],
                lg=8
            ),
            className="pb-5"
        )
    ],
    fluid=True,
    className="py-2 px-3 px-md-4 px-lg-5"
)
