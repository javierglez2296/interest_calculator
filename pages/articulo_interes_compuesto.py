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
    return html.Fragment(
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
                        html.Span("Interés compuesto", className="text-muted"),
                    ],
                    className="small mb-3"
                ),
                html.Div(
                    "Finanzas personales · Inversión a largo plazo · 8 min de lectura",
                    className="text-muted small text-uppercase fw-semibold mb-3"
                ),
                html.H1(
                    "Qué es el interés compuesto y cómo funciona de verdad",
                    className="fw-bold display-6 mb-3"
                ),
                html.P(
                    "El interés compuesto es una de las ideas más potentes de las finanzas personales. "
                    "No consiste solo en ganar dinero sobre tu inversión inicial, sino también en generar "
                    "rendimientos sobre los beneficios acumulados con el paso del tiempo.",
                    className="lead mb-3"
                ),
                html.P(
                    "Dicho de forma simple: cuando reinviertes en lugar de retirar, tu dinero empieza a "
                    "trabajar sobre una base cada vez mayor. Al principio el efecto parece pequeño, pero "
                    "a largo plazo puede marcar una diferencia enorme.",
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
                        html.Li("El interés compuesto acelera el crecimiento del dinero con el tiempo."),
                        html.Li("Cuanto antes empieces, mayor será su efecto."),
                        html.Li("Las aportaciones periódicas suelen importar más de lo que parece."),
                        html.Li("Las comisiones y la falta de constancia pueden frenarlo mucho."),
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
                html.H2("Ejemplo sencillo", className="h4 fw-bold mb-3"),
                html.P(
                    "Imagina que inviertes 10.000 € al 7% anual y no tocas el dinero. "
                    "El primer año ganarías unos 700 €. Pero el siguiente año ya no generarías "
                    "rendimientos solo sobre 10.000 €, sino sobre 10.700 €. Y después sobre una cifra todavía mayor."
                ),
                html.P(
                    "Ese proceso de reinversión continua es lo que hace que el crecimiento no sea lineal, "
                    "sino acumulativo. Por eso el interés compuesto suele notarse de verdad a partir de varios años, "
                    "no de varios meses.",
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
                html.H2("Haz tu propia simulación", className="h4 fw-bold mb-2"),
                html.P(
                    "La mejor forma de entender el interés compuesto es probar distintos escenarios: "
                    "capital inicial, aportaciones mensuales, rentabilidad, inflación y años.",
                    className="mb-3"
                ),
                dbc.Button(
                    "Ir a la calculadora de interés compuesto",
                    href=CALCULADORA_URL,
                    color="primary",
                    className="rounded-pill px-4"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4"
    )


def affiliate_cta():
    return dbc.Card(
        dbc.CardBody(
            [
                html.H2("Empieza a invertir con costes bajos", className="h4 fw-bold mb-2"),
                html.P(
                    "Si estás buscando una plataforma sencilla para empezar a ahorrar o invertir a largo plazo, "
                    "puedes echar un vistazo a MyInvestor. Antes de abrir cuenta, compara condiciones, productos "
                    "y comisiones para ver si encaja contigo.",
                    className="mb-3"
                ),
                dbc.Button(
                    "Ver opciones en MyInvestor",
                    href=MYINVESTOR_AFFILIATE_URL,
                    target="_blank",
                    rel="sponsored noopener noreferrer",
                    color="success",
                    className="rounded-pill px-4"
                ),
                html.P(
                    "Enlace de afiliado. Puede ayudarnos a mantener la web sin coste adicional para ti.",
                    className="small text-muted mt-3 mb-0"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4"
    )


def faq_section():
    return html.Section(
        [
            html.H2("Preguntas frecuentes sobre el interés compuesto", className="h3 fw-bold mt-5 mb-4"),
            html.H3("¿Qué es exactamente el interés compuesto?", className="h5 fw-bold"),
            html.P(
                "Es el efecto por el cual tu dinero genera rendimientos y esos rendimientos, a su vez, "
                "vuelven a generar nuevos rendimientos cuando se reinvierten."
            ),
            html.H3("¿Hace falta mucho dinero para beneficiarse?", className="h5 fw-bold mt-4"),
            html.P(
                "No. Empezar con una cantidad pequeña pero de forma constante suele ser más importante que "
                "esperar años a reunir una gran suma."
            ),
            html.H3("¿Se puede aplicar solo a la bolsa?", className="h5 fw-bold mt-4"),
            html.P(
                "No necesariamente. El concepto se puede aplicar a cualquier producto donde los rendimientos "
                "permanezcan invertidos o acumulándose con el tiempo."
            ),
            html.H3("¿Qué errores lo perjudican más?", className="h5 fw-bold mt-4"),
            html.P(
                "Las comisiones altas, vender con frecuencia, retirar el dinero demasiado pronto y no mantener "
                "una estrategia constante."
            ),
        ]
    )


def article_body():
    return dbc.Row(
        [
            dbc.Col(
                [
                    key_takeaways(),

                    html.H2("Cómo funciona el interés compuesto", className="h3 fw-bold mt-4 mb-3"),
                    html.P(
                        "El mecanismo es simple: inviertes un capital, ese capital genera una rentabilidad, "
                        "y en vez de retirar las ganancias las dejas dentro. A partir de ahí, el siguiente periodo "
                        "ya parte de una base más alta."
                    ),
                    html.P(
                        "Ese crecimiento acumulativo es la razón por la que dos personas con diferencias pequeñas "
                        "en tiempo o constancia pueden terminar con patrimonios muy distintos al cabo de 15 o 20 años."
                    ),

                    example_box(),

                    html.H2("Las variables que más influyen", className="h3 fw-bold mt-4 mb-3"),
                    html.P(
                        "Aunque mucha gente se obsesiona con encontrar la rentabilidad perfecta, en la práctica el "
                        "resultado final depende sobre todo de unas pocas variables."
                    ),
                    html.Ul(
                        [
                            html.Li([html.Strong("Capital inicial: "), "cuanto mayor sea, más base habrá desde el inicio."]),
                            html.Li([html.Strong("Aportaciones periódicas: "), "son clave para acelerar el crecimiento."]),
                            html.Li([html.Strong("Tiempo: "), "es probablemente la variable más poderosa."]),
                            html.Li([html.Strong("Rentabilidad media: "), "importa, pero suele ser menos decisiva que la constancia."]),
                            html.Li([html.Strong("Costes y fiscalidad: "), "pueden reducir bastante el resultado final."]),
                        ]
                    ),

                    calculator_cta(),

                    html.H2("Por qué empezar pronto marca tanta diferencia", className="h3 fw-bold mt-4 mb-3"),
                    html.P(
                        "Una de las grandes lecciones del interés compuesto es que el tiempo importa mucho más de lo que parece. "
                        "Dos inversores pueden aportar cantidades parecidas, pero quien empieza antes suele tener ventaja incluso "
                        "aunque aporte menos dinero durante los primeros años."
                    ),
                    html.P(
                        "Esto ocurre porque los primeros años construyen la base sobre la que crecerá todo lo demás. "
                        "No se trata solo de ahorrar más, sino de dar tiempo a la bola de nieve para que ruede."
                    ),

                    html.H2("Qué puede frenar el interés compuesto", className="h3 fw-bold mt-4 mb-3"),
                    html.Ul(
                        [
                            html.Li([html.Strong("Comisiones altas: "), "reducen la rentabilidad cada año."]),
                            html.Li([html.Strong("Entrar y salir constantemente: "), "rompe el proceso de acumulación."]),
                            html.Li([html.Strong("Retirar demasiado pronto: "), "impide que el capital siga creciendo."]),
                            html.Li([html.Strong("Falta de constancia: "), "interrumpe uno de los motores principales del resultado final."]),
                            html.Li([html.Strong("Expectativas irreales: "), "pueden llevar a asumir riesgos innecesarios."]),
                        ]
                    ),

                    html.H2("La fórmula del interés compuesto", className="h3 fw-bold mt-4 mb-3"),
                    html.P(
                        "La fórmula básica es:"
                    ),
                    html.Div(
                        html.Code("Capital final = Capital inicial × (1 + rentabilidad)^n"),
                        className="bg-light border rounded-3 p-3 mb-3 d-block"
                    ),
                    html.P(
                        "Si además haces aportaciones periódicas, el cálculo se vuelve algo más completo. "
                        "Por eso suele ser más útil utilizar una calculadora y comparar escenarios reales."
                    ),

                    affiliate_cta(),

                    faq_section(),

                    html.H2("Conclusión", className="h3 fw-bold mt-5 mb-3"),
                    html.P(
                        "El interés compuesto no es magia ni te hará rico en pocos meses. Pero sí puede convertir "
                        "un ahorro disciplinado en un patrimonio relevante si le das suficiente tiempo."
                    ),
                    html.P(
                        "La combinación más poderosa suele ser bastante simple: empezar cuanto antes, aportar con regularidad, "
                        "mantener costes bajos y evitar tocar la inversión innecesariamente."
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
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("En este artículo", className="h5 fw-bold mb-3"),
                                html.Ul(
                                    [
                                        html.Li("Qué es el interés compuesto"),
                                        html.Li("Cómo funciona"),
                                        html.Li("Variables clave"),
                                        html.Li("Errores frecuentes"),
                                        html.Li("Fórmula y ejemplo"),
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
                                    "Simula cuánto podría crecer tu dinero con aportaciones mensuales.",
                                    className="mb-3"
                                ),
                                dbc.Button(
                                    "Abrir calculadora",
                                    href=CALCULADORA_URL,
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
                                html.H3("Consejo", className="h5 fw-bold mb-2"),
                                html.P(
                                    "No subestimes el poder de aportar una cantidad fija cada mes durante muchos años.",
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
