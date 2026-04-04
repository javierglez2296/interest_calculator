import json
from dash import html, dcc, register_page
import dash_bootstrap_components as dbc

register_page(
    __name__,
    path="/blog/interes-compuesto",
    name="Interés compuesto",
    title="Qué es el interés compuesto y cómo funciona [Guía 2026] | interescompuesto.app",
    description=(
        "Descubre qué es el interés compuesto, cómo funciona, ejemplos reales, "
        "fórmula, errores frecuentes y cómo aprovecharlo para invertir a largo plazo."
    ),
)

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"
CALCULADORA_URL = "/calculadora"
BLOG_URL = "/blog"
HOME_URL = "/"

ARTICLE_URL = "https://interescompuesto.app/blog/interes-compuesto"
SITE_NAME = "interescompuesto.app"

# =========================================================
# SEO STRUCTURED DATA
# =========================================================
article_schema = {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Qué es el interés compuesto y cómo funciona",
    "description": (
        "Guía práctica para entender qué es el interés compuesto, cómo funciona, "
        "qué factores lo impulsan y cómo aprovecharlo para invertir a largo plazo."
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
        "interés compuesto",
        "qué es el interés compuesto",
        "cómo funciona el interés compuesto",
        "invertir a largo plazo",
        "calculadora interés compuesto"
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
            "name": "Qué es el interés compuesto",
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
            "name": "¿Qué es el interés compuesto?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": (
                    "El interés compuesto es el crecimiento del dinero cuando los rendimientos "
                    "generados se reinvierten y empiezan a producir nuevos rendimientos con el tiempo."
                )
            }
        },
        {
            "@type": "Question",
            "name": "¿Por qué es tan importante el tiempo en el interés compuesto?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": (
                    "Porque cuantos más años permanezca invertido el capital, más veces actúa "
                    "el efecto de reinversión. El crecimiento suele ser lento al principio y "
                    "mucho más visible a largo plazo."
                )
            }
        },
        {
            "@type": "Question",
            "name": "¿Qué frena el interés compuesto?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": (
                    "Las comisiones altas, vender con frecuencia, retirar el dinero demasiado pronto, "
                    "interrumpir las aportaciones y asumir rentabilidades irreales."
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


def premium_badge(text, color="light"):
    return dbc.Badge(
        text,
        color=color,
        pill=True,
        class_name="px-3 py-2 rounded-pill fw-semibold me-2 mb-2"
    )


def section_header(title, subtitle=None):
    return html.Div(
        [
            html.H2(title, className="h3 fw-bold mb-2"),
            html.P(subtitle, className="text-muted mb-0") if subtitle else None,
        ],
        className="mb-4"
    )


def hero_section():
    return dbc.Row(
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Nav(
                            [
                                dcc.Link("Inicio", href=HOME_URL, className="text-decoration-none"),
                                html.Span(" / ", className="text-muted"),
                                dcc.Link("Blog", href=BLOG_URL, className="text-decoration-none"),
                                html.Span(" / ", className="text-muted"),
                                html.Span("Interés compuesto", className="text-muted"),
                            ],
                            className="small mb-4"
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                premium_badge("Guía 2026", "dark"),
                                                premium_badge("Finanzas personales", "light"),
                                                premium_badge("Largo plazo", "light"),
                                                premium_badge("8 min lectura", "light"),
                                            ],
                                            className="mb-3"
                                        ),
                                        html.H1(
                                            "Qué es el interés compuesto y cómo funciona de verdad",
                                            className="fw-bold display-5 mb-3"
                                        ),
                                        html.P(
                                            "El interés compuesto hace que tu dinero no solo crezca por lo que inviertes, "
                                            "sino también por lo que van generando tus propias ganancias con el paso del tiempo.",
                                            className="lead mb-3"
                                        ),
                                        html.P(
                                            "Es una de las ideas más importantes para construir patrimonio a largo plazo: "
                                            "menos ruido, más tiempo, más constancia y costes bajos.",
                                            className="text-muted mb-4"
                                        ),
                                        html.Div(
                                            [
                                                dbc.Button(
                                                    "Probar calculadora",
                                                    href=CALCULADORA_URL,
                                                    color="primary",
                                                    className="rounded-pill px-4 py-2 fw-semibold me-2 mb-2"
                                                ),
                                                dbc.Button(
                                                    "Ver MyInvestor",
                                                    href=MYINVESTOR_AFFILIATE_URL,
                                                    target="_blank",
                                                    rel="sponsored noopener noreferrer",
                                                    color="light",
                                                    className="rounded-pill px-4 py-2 fw-semibold border mb-2"
                                                ),
                                            ]
                                        ),
                                    ],
                                    lg=8
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.Div("Visual rápido", className="text-uppercase small fw-bold text-muted mb-3"),
                                                html.Div("1 €", className="display-6 fw-bold mb-1"),
                                                html.P("invertido hoy no trabaja solo una vez", className="text-muted mb-3"),
                                                html.Div("→", className="display-6 fw-bold mb-1"),
                                                html.Div("más base", className="h4 fw-bold mb-1"),
                                                html.P(
                                                    "cada año tus ganancias pueden empezar a generar nuevas ganancias",
                                                    className="text-muted mb-0"
                                                ),
                                            ]
                                        ),
                                        className="border-0 shadow-sm rounded-4 h-100 bg-light"
                                    ),
                                    lg=4,
                                    className="mt-4 mt-lg-0"
                                )
                            ],
                            className="align-items-center"
                        )
                    ]
                ),
                className="border-0 shadow-sm rounded-4"
            ),
            lg=12
        ),
        className="pt-4 pt-md-5"
    )


def insight_cards():
    items = [
        ("Tiempo", "La variable más poderosa", "Cuantos más años dejes trabajar al capital, mayor suele ser la diferencia final."),
        ("Constancia", "Más importante de lo que parece", "Aportar cada mes puede pesar más que intentar encontrar el momento perfecto."),
        ("Costes", "Pueden restarte mucho", "Pequeñas comisiones anuales tienen un impacto enorme cuando se acumulan durante décadas."),
    ]

    cols = []
    for title, subtitle, text in items:
        cols.append(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(title, className="text-uppercase small fw-bold text-muted mb-2"),
                            html.H3(subtitle, className="h5 fw-bold mb-2"),
                            html.P(text, className="mb-0 text-muted"),
                        ]
                    ),
                    className="border-0 shadow-sm rounded-4 h-100"
                ),
                md=4,
                className="mb-3 mb-md-0"
            )
        )

    return dbc.Row(cols, className="my-4")


def key_takeaways():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Resumen rápido", className="text-uppercase small fw-bold text-muted mb-2"),
                html.H2("Ideas clave", className="h4 fw-bold mb-3"),
                html.Ul(
                    [
                        html.Li("El interés compuesto reinvierte ganancias y acelera el crecimiento con el tiempo."),
                        html.Li("Empezar antes suele importar más que empezar con mucho dinero."),
                        html.Li("Las aportaciones periódicas pueden marcar una diferencia enorme."),
                        html.Li("Las comisiones altas y la impaciencia son grandes enemigos."),
                    ],
                    className="mb-0"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 bg-light"
    )


def timeline_growth():
    steps = [
        ("5 años", "Aún parece modesto", "Aquí mucha gente infravalora el proceso porque el crecimiento todavía no impresiona demasiado."),
        ("10 años", "Empieza a notarse", "La base acumulada ya es más grande y el efecto se vuelve más visible."),
        ("20 años", "La diferencia suele ser enorme", "Es donde constancia, reinversión y tiempo suelen empezar a separarlo todo."),
        ("30 años", "El tiempo hace el trabajo pesado", "La fase más potente del interés compuesto suele llegar muy tarde."),
    ]

    cols = []
    for period, title, text in steps:
        cols.append(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(period, className="text-uppercase small fw-bold text-primary mb-2"),
                            html.H3(title, className="h5 fw-bold mb-2"),
                            html.P(text, className="mb-0 text-muted"),
                        ]
                    ),
                    className="border-0 shadow-sm rounded-4 h-100"
                ),
                md=6,
                xl=3,
                className="mb-3"
            )
        )

    return html.Div(
        [
            section_header(
                "Cómo suele verse en el tiempo",
                "El interés compuesto no suele impresionar al principio. Su fuerza aparece más tarde."
            ),
            dbc.Row(cols)
        ],
        className="my-5"
    )


def comparison_table():
    return dbc.Card(
        dbc.CardBody(
            [
                html.H2("Interés simple vs interés compuesto", className="h4 fw-bold mb-3"),
                dbc.Table(
                    [
                        html.Thead(
                            html.Tr(
                                [
                                    html.Th("Concepto"),
                                    html.Th("Interés simple"),
                                    html.Th("Interés compuesto"),
                                ]
                            )
                        ),
                        html.Tbody(
                            [
                                html.Tr(
                                    [
                                        html.Td("Sobre qué se calcula"),
                                        html.Td("Solo sobre el capital inicial"),
                                        html.Td("Sobre capital inicial + ganancias acumuladas"),
                                    ]
                                ),
                                html.Tr(
                                    [
                                        html.Td("Crecimiento"),
                                        html.Td("Más lineal"),
                                        html.Td("Más acumulativo"),
                                    ]
                                ),
                                html.Tr(
                                    [
                                        html.Td("Potencia a largo plazo"),
                                        html.Td("Limitada"),
                                        html.Td("Muy superior"),
                                    ]
                                ),
                                html.Tr(
                                    [
                                        html.Td("Qué lo impulsa"),
                                        html.Td("Tipo y plazo"),
                                        html.Td("Tiempo, reinversión, constancia y costes bajos"),
                                    ]
                                ),
                            ]
                        ),
                    ],
                    hover=True,
                    responsive=True,
                    bordered=False,
                    class_name="align-middle mb-0"
                )
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4"
    )


def example_box():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Ejemplo sencillo", className="text-uppercase small fw-bold text-muted mb-2"),
                html.H2("Qué ocurre con 10.000 € al 7%", className="h4 fw-bold mb-3"),
                html.P(
                    "Imagina que inviertes 10.000 € al 7% anual y no retiras nada. "
                    "El primer año ganarías unos 700 €. Al siguiente, ya no se calcula sobre 10.000 €, "
                    "sino sobre 10.700 €."
                ),
                html.P(
                    "Y después sobre una cifra todavía mayor. Ese es el núcleo del interés compuesto: "
                    "la base va creciendo y cada periodo puede producir más que el anterior.",
                    className="mb-0"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4"
    )


def formula_box():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Fórmula básica", className="text-uppercase small fw-bold text-muted mb-2"),
                html.H2("Cómo se calcula", className="h4 fw-bold mb-3"),
                html.P("La versión simplificada sería:", className="mb-3"),
                html.Div(
                    html.Code(
                        "Capital final = Capital inicial × (1 + rentabilidad)^n",
                        className="fs-6"
                    ),
                    className="bg-light border rounded-4 p-3 p-md-4 mb-3"
                ),
                html.P(
                    "Cuando añades aportaciones mensuales, inflación, comisiones o impuestos, el cálculo se vuelve más completo. "
                    "Por eso tiene más sentido usar una calculadora real.",
                    className="mb-0 text-muted"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4"
    )


def quote_box():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Idea central", className="text-uppercase small fw-bold text-muted mb-2"),
                html.Blockquote(
                    "La mayoría de personas abandona antes de llegar a la fase donde el interés compuesto empieza a notarse de verdad.",
                    className="blockquote mb-2"
                ),
                html.P(
                    "No porque el concepto falle, sino porque sus mejores resultados suelen llegar bastante tarde.",
                    className="mb-0 text-muted"
                )
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4 bg-light"
    )


def calculator_cta():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Herramienta", className="text-uppercase small fw-bold text-muted mb-2"),
                html.H2("Haz tu propia simulación", className="h4 fw-bold mb-2"),
                html.P(
                    "Cambia capital inicial, aportaciones, años, rentabilidad, inflación y costes "
                    "para ver cómo afectan al resultado final.",
                    className="mb-3"
                ),
                dbc.Button(
                    "Ir a la calculadora de interés compuesto",
                    href=CALCULADORA_URL,
                    color="primary",
                    className="rounded-pill px-4 py-2 fw-semibold"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4"
    )


def affiliate_cta():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Plataforma sugerida", className="text-uppercase small fw-bold text-muted mb-2"),
                html.H2("Empieza con costes bajos", className="h4 fw-bold mb-2"),
                html.P(
                    "Si estás buscando una plataforma sencilla para ahorrar o invertir a largo plazo, "
                    "puedes revisar MyInvestor. Compara siempre comisiones, productos y condiciones.",
                    className="mb-3"
                ),
                dbc.Button(
                    "Ver opciones en MyInvestor",
                    href=MYINVESTOR_AFFILIATE_URL,
                    target="_blank",
                    rel="sponsored noopener noreferrer",
                    color="success",
                    className="rounded-pill px-4 py-2 fw-semibold"
                ),
                html.P(
                    "Enlace de afiliado. Puede ayudarnos a mantener la web sin coste adicional para ti.",
                    className="small text-muted mt-3 mb-0"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4"
    )


def faq_item(question, answer):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H3(question, className="h5 fw-bold mb-2"),
                html.P(answer, className="mb-0 text-muted"),
            ]
        ),
        className="border-0 shadow-sm rounded-4 mb-3"
    )


def faq_section():
    return html.Section(
        [
            section_header(
                "Preguntas frecuentes sobre el interés compuesto",
                "Las dudas más habituales, respondidas de forma clara."
            ),
            faq_item(
                "¿Qué es exactamente el interés compuesto?",
                "Es el efecto por el que tu dinero genera rendimientos y esos rendimientos vuelven a producir nuevos rendimientos cuando se reinvierten."
            ),
            faq_item(
                "¿Hace falta mucho dinero para beneficiarse?",
                "No. Empezar con una cantidad pequeña pero de forma constante suele ser más importante que esperar a tener una gran suma."
            ),
            faq_item(
                "¿Solo se aplica a la bolsa?",
                "No. Puede aplicarse a cualquier producto en el que los rendimientos permanezcan acumulándose con el tiempo."
            ),
            faq_item(
                "¿Qué errores lo perjudican más?",
                "Las comisiones altas, retirar dinero demasiado pronto, entrar y salir continuamente y no mantener constancia."
            ),
        ],
        className="mt-5"
    )


def related_articles():
    cards = [
        (
            "Calculadora de interés compuesto",
            "Haz simulaciones con aportaciones mensuales, inflación, comisiones e impuestos.",
            CALCULADORA_URL,
            "Abrir calculadora"
        ),
        (
            "Calculadora FIRE",
            "Descubre cuánto patrimonio podrías necesitar para acercarte a la independencia financiera.",
            "/fire",
            "Ver calculadora FIRE"
        ),
        (
            "Calculadora de hipoteca",
            "Calcula cuota mensual, coste total e impacto del tipo de interés en tu préstamo.",
            "/hipoteca",
            "Ver calculadora hipotecaria"
        ),
    ]

    cols = []
    for title, text, href, cta in cards:
        cols.append(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H3(title, className="h5 fw-bold mb-2"),
                            html.P(text, className="text-muted mb-3"),
                            dbc.Button(
                                cta,
                                href=href,
                                color="light",
                                className="rounded-pill px-4 fw-semibold border"
                            ),
                        ]
                    ),
                    className="border-0 shadow-sm rounded-4 h-100"
                ),
                md=4,
                className="mb-3 mb-md-0"
            )
        )

    return html.Section(
        [
            section_header(
                "Sigue explorando",
                "Otras herramientas útiles de interescompuesto.app"
            ),
            dbc.Row(cols)
        ],
        className="mt-5"
    )


def article_body():
    return dbc.Row(
        [
            dbc.Col(
                [
                    insight_cards(),
                    key_takeaways(),

                    html.Hr(className="my-5"),

                    section_header(
                        "Cómo funciona el interés compuesto",
                        "La lógica es simple. El impacto acumulado, no tanto."
                    ),
                    html.P(
                        "El mecanismo es sencillo: inviertes un capital, ese capital genera rentabilidad, "
                        "y en lugar de retirar las ganancias, las mantienes invertidas. A partir de ahí, "
                        "el siguiente periodo arranca desde una base superior."
                    ),
                    html.P(
                        "Eso hace que el crecimiento deje de ser lineal. Y ahí es donde aparece su fuerza: "
                        "cada año no solo sumas dinero, también aumentas la base que puede seguir creciendo."
                    ),

                    comparison_table(),
                    example_box(),
                    timeline_growth(),

                    html.Hr(className="my-5"),

                    section_header(
                        "Las variables que más influyen",
                        "No todo pesa igual en el resultado final."
                    ),
                    html.P(
                        "Aunque mucha gente se obsesiona con la rentabilidad, en la práctica el resultado suele depender "
                        "de unas pocas variables que importan muchísimo."
                    ),
                    html.Ul(
                        [
                            html.Li([html.Strong("Capital inicial: "), "te da una base desde la que empezar."]),
                            html.Li([html.Strong("Aportaciones periódicas: "), "alimentan el crecimiento de forma continua."]),
                            html.Li([html.Strong("Tiempo: "), "suele ser la variable más poderosa."]),
                            html.Li([html.Strong("Rentabilidad media: "), "importa, pero no compensa la falta de constancia."]),
                            html.Li([html.Strong("Comisiones y fiscalidad: "), "pueden reducir mucho el resultado final."]),
                        ]
                    ),

                    calculator_cta(),
                    quote_box(),

                    html.Hr(className="my-5"),

                    section_header(
                        "Por qué empezar pronto marca tanta diferencia",
                        "La ventaja no siempre está en aportar más, sino en dejar más tiempo."
                    ),
                    html.P(
                        "Dos personas pueden invertir cantidades parecidas, pero quien empieza antes suele acabar con bastante más. "
                        "No porque sea mejor inversor, sino porque da más tiempo a que las ganancias se acumulen sobre sí mismas."
                    ),
                    html.P(
                        "Los primeros años construyen la base. Y esa base es la que luego hace posible que el crecimiento se vuelva "
                        "cada vez más visible."
                    ),

                    html.Hr(className="my-5"),

                    section_header(
                        "Qué puede frenar el interés compuesto",
                        "Pequeños errores repetidos durante años tienen mucho peso."
                    ),
                    html.Ul(
                        [
                            html.Li([html.Strong("Comisiones altas: "), "restan rentabilidad todos los años."]),
                            html.Li([html.Strong("Entrar y salir sin parar: "), "rompe el efecto acumulativo."]),
                            html.Li([html.Strong("Retirar el dinero demasiado pronto: "), "frena el crecimiento futuro."]),
                            html.Li([html.Strong("No ser constante: "), "reduce uno de los motores principales del resultado final."]),
                            html.Li([html.Strong("Buscar rentabilidades irreales: "), "puede llevarte a asumir riesgos innecesarios."]),
                        ]
                    ),

                    formula_box(),
                    affiliate_cta(),
                    faq_section(),
                    related_articles(),

                    html.Hr(className="my-5"),

                    section_header("Conclusión"),
                    html.P(
                        "El interés compuesto no es magia ni una promesa de riqueza rápida. "
                        "Pero sí es uno de los mecanismos más potentes para construir patrimonio a largo plazo."
                    ),
                    html.P(
                        "La combinación que mejor suele funcionar es bastante sobria: empezar cuanto antes, "
                        "aportar de forma regular, mantener costes bajos y dejar trabajar al tiempo."
                    ),
                    html.P(
                        [
                            "Si quieres verlo con números, prueba nuestra ",
                            dcc.Link("calculadora de interés compuesto", href=CALCULADORA_URL),
                            " y compara distintos escenarios."
                        ],
                        className="mb-0"
                    ),
                ],
                lg=8,
                xl=8
            ),

            dbc.Col(
                [
                    html.Div(
                        [
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div("Navegación", className="text-uppercase small fw-bold text-muted mb-2"),
                                        html.H3("En este artículo", className="h5 fw-bold mb-3"),
                                        html.Ul(
                                            [
                                                html.Li("Qué es el interés compuesto"),
                                                html.Li("Cómo funciona"),
                                                html.Li("Interés simple vs compuesto"),
                                                html.Li("Variables clave"),
                                                html.Li("Errores frecuentes"),
                                                html.Li("Fórmula y ejemplo"),
                                                html.Li("Preguntas frecuentes"),
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
                                        html.Div("Herramienta recomendada", className="text-uppercase small fw-bold text-muted mb-2"),
                                        html.H3("Simula tu caso", className="h5 fw-bold mb-2"),
                                        html.P(
                                            "Calcula cuánto podría crecer tu dinero con aportaciones periódicas.",
                                            className="mb-3 text-muted"
                                        ),
                                        dbc.Button(
                                            "Abrir calculadora",
                                            href=CALCULADORA_URL,
                                            color="outline-primary",
                                            className="rounded-pill px-4 fw-semibold"
                                        ),
                                    ]
                                ),
                                className="border-0 shadow-sm rounded-4 mb-4"
                            ),

                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div("Consejo", className="text-uppercase small fw-bold text-muted mb-2"),
                                        html.H3("La paciencia también rentabiliza", className="h5 fw-bold mb-2"),
                                        html.P(
                                            "Muchas veces la diferencia entre un resultado mediocre y uno muy bueno "
                                            "no está en la brillantez, sino en mantenerse durante años.",
                                            className="mb-0 text-muted"
                                        ),
                                    ]
                                ),
                                className="border-0 shadow-sm rounded-4 mb-4 bg-light"
                            ),

                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div("Afiliado", className="text-uppercase small fw-bold text-muted mb-2"),
                                        html.H3("Ver MyInvestor", className="h5 fw-bold mb-2"),
                                        html.P(
                                            "Revisa opciones de ahorro e inversión a largo plazo.",
                                            className="mb-3 text-muted"
                                        ),
                                        dbc.Button(
                                            "Ir a MyInvestor",
                                            href=MYINVESTOR_AFFILIATE_URL,
                                            target="_blank",
                                            rel="sponsored noopener noreferrer",
                                            color="success",
                                            className="rounded-pill px-4 fw-semibold"
                                        ),
                                    ]
                                ),
                                className="border-0 shadow-sm rounded-4"
                            ),
                        ],
                        style={"position": "sticky", "top": "100px"}
                    )
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
        hero_section(),
        article_body(),
    ],
    fluid=True,
    className="py-2 px-3 px-md-4 px-lg-5"
)
