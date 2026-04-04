import json
from dash import html, dcc, register_page
import dash_bootstrap_components as dbc

register_page(
    __name__,
    path="/blog/hipoteca",
    name="Hipoteca artículo",
    title="Cómo calcular una hipoteca y cuánto pagarás de verdad [Guía 2026] | interescompuesto.app",
    description=(
        "Aprende cómo calcular una hipoteca, cuánto pagarás al mes, qué entrada necesitas, "
        "qué gastos iniciales debes tener en cuenta y cómo evitar errores al comprar vivienda."
    ),
)

HIPOTECA_CALCULATOR_URL = "/hipoteca"
BLOG_URL = "/blog"
HOME_URL = "/"

ARTICLE_URL = "https://interescompuesto.app/blog/hipoteca"
SITE_NAME = "interescompuesto.app"

# =========================================================
# SEO STRUCTURED DATA
# =========================================================
article_schema = {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Cómo calcular una hipoteca y cuánto pagarás de verdad",
    "description": (
        "Guía práctica para entender cómo calcular una hipoteca, qué factores influyen "
        "en la cuota mensual, cuánto dinero necesitas ahorrar y qué errores evitar al comprar vivienda."
    ),
    "author": {
        "@type": "Organization",
        "name": SITE_NAME
    },
    "publisher": {
        "@type": "Organization",
        "name": SITE_NAME
    },
    "mainEntityOfPage": ARTICLE_URL,
    "url": ARTICLE_URL,
    "inLanguage": "es",
    "keywords": [
        "cómo calcular una hipoteca",
        "calculadora hipoteca",
        "cuánto pago de hipoteca",
        "cuota hipotecaria",
        "entrada hipoteca",
        "gastos compra vivienda",
        "hipoteca fija o variable",
        "comprar casa"
    ]
}

breadcrumb_schema = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "Inicio",
            "item": "https://interescompuesto.app/"
        },
        {
            "@type": "ListItem",
            "position": 2,
            "name": "Blog",
            "item": "https://interescompuesto.app/blog"
        },
        {
            "@type": "ListItem",
            "position": 3,
            "name": "Cómo calcular una hipoteca",
            "item": ARTICLE_URL
        }
    ]
}

faq_schema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {
            "@type": "Question",
            "name": "¿Cómo se calcula una hipoteca?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": (
                    "Una hipoteca se calcula principalmente con el capital prestado, el tipo de interés "
                    "y el plazo del préstamo. Cuanto mayor sea el interés o menor el plazo, más alta "
                    "suele ser la cuota mensual."
                )
            }
        },
        {
            "@type": "Question",
            "name": "¿Qué entrada necesito para comprar una vivienda?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": (
                    "Como referencia general, muchas operaciones exigen disponer de ahorro para la entrada "
                    "y para gastos adicionales. En la práctica, conviene contar con un colchón suficiente "
                    "antes de firmar."
                )
            }
        },
        {
            "@type": "Question",
            "name": "¿Qué porcentaje del sueldo debería destinar a la hipoteca?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": (
                    "Como regla orientativa, suele considerarse prudente que la cuota hipotecaria no supere "
                    "aproximadamente el 30% al 35% de los ingresos netos del hogar."
                )
            }
        },
        {
            "@type": "Question",
            "name": "¿Es mejor una hipoteca fija o variable?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": (
                    "La hipoteca fija da estabilidad y previsibilidad en la cuota. La variable puede resultar "
                    "más barata o más cara según la evolución de los tipos de interés. Conviene comparar escenarios."
                )
            }
        }
    ]
}


def seo_json_ld_block():
    return html.Div(
        [
            html.Script(
                type="application/ld+json",
                children=json.dumps(article_schema, ensure_ascii=False)
            ),
            html.Script(
                type="application/ld+json",
                children=json.dumps(breadcrumb_schema, ensure_ascii=False)
            ),
            html.Script(
                type="application/ld+json",
                children=json.dumps(faq_schema, ensure_ascii=False)
            ),
        ]
    )


def article_intro():
    return dbc.Row(
        dbc.Col(
            [
                html.Nav(
                    [
                        dcc.Link("Inicio", href=HOME_URL, className="text-decoration-none"),
                        html.Span(" / ", className="text-muted"),
                        dcc.Link("Blog", href=BLOG_URL, className="text-decoration-none"),
                        html.Span(" / ", className="text-muted"),
                        html.Span("Hipoteca", className="text-muted"),
                    ],
                    className="small mb-3"
                ),
                html.Div(
                    "Hipoteca · Vivienda · 11 min de lectura",
                    className="text-muted small text-uppercase fw-semibold mb-3"
                ),
                html.H1(
                    "Cómo calcular una hipoteca y cuánto pagarás de verdad",
                    className="fw-bold display-6 mb-3"
                ),
                html.P(
                    "Cuando miras una vivienda, es fácil centrarse solo en el precio de compra. "
                    "Pero la decisión real pasa por otra pregunta: cuánto capital vas a financiar, "
                    "qué cuota mensual asumirás y cuánto terminarás pagando entre intereses y gastos.",
                    className="lead mb-3"
                ),
                html.P(
                    "Una hipoteca puede ser razonable y sostenible, o convertirse en una carga que limite tu ahorro "
                    "durante años. La diferencia suele estar en hacer bien los números antes de firmar.",
                    className="mb-0"
                ),
            ],
            lg=9,
            xl=8
        ),
        className="pt-4 pt-md-5"
    )


def key_takeaways():
    return dbc.Card(
        dbc.CardBody(
            [
                html.H2("Ideas clave", className="h5 fw-bold mb-3"),
                html.Ul(
                    [
                        html.Li("La cuota depende del capital, el interés y el plazo."),
                        html.Li("No basta con saber si puedes pagar la mensualidad."),
                        html.Li("La entrada y los gastos iniciales pesan mucho en la operación."),
                        html.Li("Cuota baja no siempre significa buena hipoteca."),
                        html.Li("Comprar casa debe encajar en tu vida y en tu liquidez, no solo en el banco."),
                    ],
                    className="mb-0"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4 bg-light"
    )


def example_box():
    return dbc.Card(
        dbc.CardBody(
            [
                html.H2("Ejemplo práctico", className="h4 fw-bold mb-3"),
                html.P(
                    "Imagina una vivienda de 280.000 €. Si puedes aportar 56.000 € de entrada, "
                    "el importe a financiar sería de 224.000 €."
                ),
                html.P(
                    "A partir de ahí, la cuota mensual cambia bastante según el interés y el plazo. "
                    "No es lo mismo devolver ese préstamo a 25 años que a 30 años."
                ),
                html.P(
                    "En general, cuanto más largo sea el plazo, menor será la cuota mensual. "
                    "Pero también mayor será el coste total de intereses al final de la hipoteca.",
                    className="mb-0"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4"
    )


def warning_box():
    return dbc.Card(
        dbc.CardBody(
            [
                html.H2("El error típico", className="h4 fw-bold mb-3 text-danger"),
                html.P(
                    "Muchísimas personas se preguntan solo: “¿Puedo pagar esta cuota?”. "
                    "La pregunta correcta es más amplia: “¿Puedo pagar esta cuota, mantener ahorro, "
                    "cubrir imprevistos y seguir teniendo margen de vida?”.",
                    className="mb-0"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4"
    )


def savings_box():
    return dbc.Card(
        dbc.CardBody(
            [
                html.H2("¿Cuánto dinero deberías ahorrar antes de comprar?", className="h4 fw-bold mb-3"),
                html.P(
                    "Uno de los mayores errores al comprar vivienda es llegar justo a la firma. "
                    "Aunque la cuota parezca asumible, muchas operaciones se complican porque el comprador "
                    "ha consumido casi todo su ahorro en entrada y gastos."
                ),
                html.P(
                    "Antes de hipotecarte, intenta valorar tres capas de ahorro:"
                ),
                html.Ul(
                    [
                        html.Li([html.Strong("Entrada: "), "la parte del precio que no cubre el banco."]),
                        html.Li([html.Strong("Gastos de compra: "), "impuestos, tasación y otros costes asociados."]),
                        html.Li([html.Strong("Colchón de seguridad: "), "reserva para no quedarte sin liquidez tras la compra."]),
                    ],
                    className="mb-3"
                ),
                html.P(
                    "Comprar con margen suele ser mucho más sano que comprar al límite, incluso si eso implica "
                    "esperar un poco más o elegir una vivienda algo más barata.",
                    className="mb-0"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4"
    )


def calculator_cta():
    return dbc.Card(
        dbc.CardBody(
            [
                html.H2("Haz tu simulación hipotecaria", className="h4 fw-bold mb-2"),
                html.P(
                    "Prueba distintos escenarios de precio, entrada, interés y plazo para ver qué cuota "
                    "tendrías y si de verdad encaja en tu situación financiera.",
                    className="mb-3"
                ),
                dbc.Button(
                    "Ir a la calculadora de hipoteca",
                    href=HIPOTECA_CALCULATOR_URL,
                    color="primary",
                    className="rounded-pill px-4"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4"
    )


def compare_box():
    return dbc.Card(
        dbc.CardBody(
            [
                html.H2("Hipoteca fija vs variable", className="h4 fw-bold mb-3"),
                html.Div(
                    [
                        html.P(
                            [
                                html.Strong("Hipoteca fija: "),
                                "sabes desde el principio cuánto pagarás cada mes. "
                                "Suele dar tranquilidad y facilita planificar."
                            ]
                        ),
                        html.P(
                            [
                                html.Strong("Hipoteca variable: "),
                                "la cuota puede subir o bajar con los tipos de interés. "
                                "Puede salir mejor o peor, pero introduce incertidumbre."
                            ]
                        ),
                        html.P(
                            "La mejor opción no es universal. Depende de tu tolerancia al riesgo, "
                            "tu estabilidad financiera y del valor que le des a una cuota estable.",
                            className="mb-0"
                        ),
                    ]
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4"
    )


def rent_vs_buy_box():
    return dbc.Card(
        dbc.CardBody(
            [
                html.H2("¿Alquilar o comprar?", className="h4 fw-bold mb-3"),
                html.P(
                    "Comprar no siempre es automáticamente mejor que alquilar. Depende del precio de la vivienda, "
                    "de tus planes a medio plazo, del coste de oportunidad de tus ahorros y del nivel de cuota que "
                    "asumirías respecto a tus ingresos."
                ),
                html.P(
                    "Comprar puede tener sentido si vas a permanecer años en la vivienda, tienes estabilidad y "
                    "la operación no te deja sin margen. Alquilar puede ser preferible si necesitas flexibilidad "
                    "o si comprar te obliga a tensionar demasiado tus finanzas.",
                    className="mb-0"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4"
    )


def faq_section():
    return html.Section(
        [
            html.H2("Preguntas frecuentes sobre hipotecas", className="h3 fw-bold mt-5 mb-4"),
            html.H3("¿Qué datos necesito para calcular una hipoteca?", className="h5 fw-bold"),
            html.P(
                "Los cuatro más importantes son el precio de compra, la entrada disponible, "
                "el tipo de interés y el plazo del préstamo."
            ),
            html.H3("¿Cuánto debería destinar a la cuota?", className="h5 fw-bold mt-4"),
            html.P(
                "Como referencia general, suele considerarse prudente no superar aproximadamente "
                "el 30% al 35% de los ingresos netos del hogar."
            ),
            html.H3("¿Qué gastos hay además de la cuota mensual?", className="h5 fw-bold mt-4"),
            html.P(
                "Además de la cuota, conviene contar con entrada, impuestos, tasación, posibles gastos "
                "administrativos, reformas, mobiliario, seguros y mantenimiento."
            ),
            html.H3("¿Qué es más importante: la cuota o el coste total?", className="h5 fw-bold mt-4"),
            html.P(
                "Las dos cosas. Una cuota baja puede parecer atractiva, pero si alargas demasiado el plazo "
                "terminarás pagando muchos más intereses."
            ),
            html.H3("¿Es mala idea comprar quedándote sin ahorros?", className="h5 fw-bold mt-4"),
            html.P(
                "Suele ser arriesgado. Lo más prudente es llegar a la compra con cierto margen de liquidez "
                "para no depender de que todo salga perfecto tras la firma."
            ),
        ]
    )


def article_body():
    return dbc.Row(
        [
            dbc.Col(
                [
                    key_takeaways(),

                    html.H2("Cómo se calcula una hipoteca", className="h3 fw-bold mt-4 mb-3"),
                    html.P(
                        "Calcular una hipoteca consiste en estimar la cuota mensual que pagarás a partir de tres elementos: "
                        "capital prestado, tipo de interés y plazo. A eso luego debes sumarle una visión más amplia del coste total."
                    ),
                    html.P(
                        "Dicho de forma simple: primero defines cuánto dinero te presta el banco, después aplicas el interés "
                        "y finalmente distribuyes la devolución a lo largo de los años del préstamo."
                    ),

                    example_box(),
                    warning_box(),

                    html.H2("Los 4 datos básicos que necesitas", className="h3 fw-bold mt-4 mb-3"),
                    html.Ul(
                        [
                            html.Li([html.Strong("Precio de compra: "), "el valor total de la vivienda."]),
                            html.Li([html.Strong("Entrada: "), "el ahorro que aportas de tu bolsillo."]),
                            html.Li([html.Strong("Tipo de interés: "), "el porcentaje que cobra el banco por prestarte el dinero."]),
                            html.Li([html.Strong("Plazo: "), "los años durante los que devolverás el préstamo."]),
                        ]
                    ),
                    html.P(
                        "Con estos datos puedes calcular una estimación bastante útil. Pero una buena decisión hipotecaria "
                        "no termina cuando conoces la cuota."
                    ),

                    savings_box(),

                    html.H2("Qué gastos debes mirar además de la cuota", className="h3 fw-bold mt-4 mb-3"),
                    html.P(
                        "Uno de los errores más caros es pensar que comprar vivienda solo exige pagar la entrada y luego la mensualidad. "
                        "En la práctica, hay varios costes que conviene incluir desde el principio."
                    ),
                    html.Ul(
                        [
                            html.Li("Entrada inicial."),
                            html.Li("Impuestos asociados a la compraventa."),
                            html.Li("Tasación."),
                            html.Li("Notaría o costes administrativos si proceden."),
                            html.Li("Reformas, muebles, mudanza o pequeños imprevistos."),
                            html.Li("Gastos recurrentes de vivienda: comunidad, IBI, seguro y mantenimiento."),
                        ]
                    ),

                    calculator_cta(),

                    html.H2("Qué cuota suele ser prudente", className="h3 fw-bold mt-4 mb-3"),
                    html.P(
                        "Como referencia general, suele recomendarse que la cuota hipotecaria no supere aproximadamente "
                        "el 30% al 35% de los ingresos netos del hogar."
                    ),
                    html.P(
                        "Pero esa referencia no basta por sí sola. También importa mucho tu estabilidad laboral, el colchón de emergencia, "
                        "si tienes hijos, otros préstamos, gastos fijos elevados o planes de ahorro relevantes."
                    ),
                    html.P(
                        "Una cuota asumible sobre el papel puede ser demasiado exigente en la práctica si te deja sin capacidad de maniobra."
                    ),

                    compare_box(),

                    html.H2("Errores frecuentes al comparar hipotecas", className="h3 fw-bold mt-4 mb-3"),
                    html.Ul(
                        [
                            html.Li([html.Strong("Mirar solo la cuota mensual: "), "sin valorar el coste total del préstamo."]),
                            html.Li([html.Strong("Agotar todos los ahorros: "), "y quedarse sin colchón después de la compra."]),
                            html.Li([html.Strong("Elegir plazo largo solo para bajar cuota: "), "sin medir cuánto encarece la operación."]),
                            html.Li([html.Strong("No comparar escenarios: "), "fija frente a variable, distintos intereses o entradas."]),
                            html.Li([html.Strong("Subestimar gastos futuros: "), "comunidad, reparaciones, IBI o mantenimiento."]),
                        ]
                    ),

                    rent_vs_buy_box(),

                    faq_section(),

                    html.H2("Conclusión", className="h3 fw-bold mt-5 mb-3"),
                    html.P(
                        "Comprar vivienda no es solo una decisión emocional. También es una de las mayores decisiones financieras "
                        "que tomarás en muchos años."
                    ),
                    html.P(
                        "Antes de firmar, conviene saber cuánto capital financias, qué cuota mensual tendrás, cuánto pagarás en total "
                        "y con cuánto margen de liquidez te quedarás después."
                    ),
                    html.P(
                        [
                            "Si quieres hacer números con tus propios datos, prueba nuestra ",
                            dcc.Link("calculadora de hipoteca", href=HIPOTECA_CALCULATOR_URL),
                            " y compara escenarios antes de decidir."
                        ],
                        className="mb-0"
                    ),
                ],
                lg=8,
                xl=8
            ),

            dbc.Col(
                [
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("En este artículo", className="h5 fw-bold mb-3"),
                                html.Ul(
                                    [
                                        html.Li("Cómo se calcula"),
                                        html.Li("Cuánto ahorrar antes"),
                                        html.Li("Gastos reales"),
                                        html.Li("Fija vs variable"),
                                        html.Li("Alquiler vs compra"),
                                    ],
                                    className="mb-0"
                                ),
                            ]
                        ),
                        className="border-0 shadow-sm rounded-4 mb-4"
                    ),

                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("Herramienta recomendada", className="h5 fw-bold mb-2"),
                                html.P(
                                    "Calcula tu cuota mensual y compara escenarios de plazo, interés y entrada.",
                                    className="mb-3"
                                ),
                                dbc.Button(
                                    "Abrir calculadora",
                                    href=HIPOTECA_CALCULATOR_URL,
                                    color="outline-primary",
                                    className="rounded-pill"
                                ),
                            ]
                        ),
                        className="border-0 shadow-sm rounded-4 mb-4"
                    ),

                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("Consejo práctico", className="h5 fw-bold mb-2"),
                                html.P(
                                    "Si una vivienda te encaja solo en el escenario más optimista, probablemente no te encaja de verdad.",
                                    className="mb-0"
                                ),
                            ]
                        ),
                        className="border-0 shadow-sm rounded-4 mb-4"
                    ),

                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("Siguiente paso", className="h5 fw-bold mb-2"),
                                html.P(
                                    "Haz una simulación con una cuota cómoda, no con la cuota máxima que te concedería el banco.",
                                    className="mb-0"
                                ),
                            ]
                        ),
                        className="border-0 shadow-sm rounded-4"
                    ),
                ],
                lg=4,
                xl=3,
                className="mt-4 mt-lg-0"
            ),
        ],
        className="pb-5"
    )


layout = dbc.Container(
    [
        seo_json_ld_block(),
        article_intro(),
        article_body(),
    ],
    fluid=True,
    className="py-2 px-3 px-md-4 px-lg-5"
)
