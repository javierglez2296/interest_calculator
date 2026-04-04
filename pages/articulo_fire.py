import json
from dash import html, dcc, register_page
import dash_bootstrap_components as dbc

register_page(
    __name__,
    path="/blog/fire",
    name="FIRE",
    title="Qué es FIRE, cómo funciona y cuánto dinero necesitas [Guía 2026] | interescompuesto.app",
    description=(
        "Descubre qué es el movimiento FIRE, cómo calcular tu número FIRE, "
        "la regla del 4%, ejemplos, tipos de FIRE y errores frecuentes."
    ),
)

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"
FIRE_CALCULATOR_URL = "/fire"
BLOG_URL = "/blog"
HOME_URL = "/"

ARTICLE_URL = "https://interescompuesto.app/blog/fire"
SITE_NAME = "interescompuesto.app"

# =========================================================
# SEO STRUCTURED DATA
# =========================================================
article_schema = {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Qué es el movimiento FIRE, cómo funciona y cuánto dinero necesitas",
    "description": (
        "Guía práctica para entender el movimiento FIRE, calcular tu objetivo "
        "de independencia financiera y evitar errores habituales."
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
        "FIRE",
        "movimiento FIRE",
        "qué es FIRE",
        "independencia financiera",
        "regla del 4%",
        "cuánto dinero necesito para FIRE",
        "calculadora FIRE"
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
            "name": "Qué es FIRE",
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
            "name": "¿Qué significa FIRE?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": (
                    "FIRE significa Financial Independence, Retire Early. "
                    "Es una filosofía basada en ahorrar e invertir para alcanzar "
                    "la independencia financiera lo antes posible."
                )
            }
        },
        {
            "@type": "Question",
            "name": "¿Qué es la regla del 4%?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": (
                    "La regla del 4% es una referencia que sugiere que una persona "
                    "podría retirar alrededor del 4% anual de su cartera en jubilación. "
                    "De forma orientativa, equivale a multiplicar los gastos anuales por 25."
                )
            }
        },
        {
            "@type": "Question",
            "name": "¿Hace falta jubilarse pronto para aplicar FIRE?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": (
                    "No. Muchas personas usan FIRE no para dejar de trabajar pronto, "
                    "sino para ganar seguridad, flexibilidad y menos dependencia del sueldo."
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
                        html.Span("FIRE", className="text-muted"),
                    ],
                    className="small mb-3"
                ),
                html.Div(
                    "Finanzas personales · Independencia financiera · 9 min de lectura",
                    className="text-muted small text-uppercase fw-semibold mb-3"
                ),
                html.H1(
                    "Qué es el movimiento FIRE, cómo funciona y cuánto dinero necesitas",
                    className="fw-bold display-6 mb-3"
                ),
                html.P(
                    "FIRE significa Financial Independence, Retire Early. En español, se suele traducir como "
                    "independencia financiera y retiro temprano. La idea central es acumular un patrimonio "
                    "capaz de cubrir tus gastos, de forma que dependas menos de tu sueldo.",
                    className="lead mb-3"
                ),
                html.P(
                    "Aunque mucha gente asocia FIRE con dejar de trabajar a los 35 o 40 años, en realidad la "
                    "filosofía puede aplicarse de forma mucho más flexible. Para muchas personas, FIRE no es "
                    "jubilarse cuanto antes, sino ganar libertad, margen de decisión y tranquilidad financiera.",
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
                        html.Li("FIRE busca que tus inversiones cubran tus gastos."),
                        html.Li("La regla del 4% es una referencia útil, no una garantía."),
                        html.Li("La tasa de ahorro y el tiempo invertido son determinantes."),
                        html.Li("No hace falta retirarte pronto para beneficiarte de esta filosofía."),
                    ],
                    className="mb-0"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4 bg-light"
    )


def number_fire_box():
    return dbc.Card(
        dbc.CardBody(
            [
                html.H2("Ejemplo rápido: calcular tu número FIRE", className="h4 fw-bold mb-3"),
                html.P(
                    "Una forma sencilla de estimar tu objetivo FIRE es multiplicar tus gastos anuales por 25. "
                    "Es la referencia asociada a la llamada regla del 4%."
                ),
                html.P(
                    "Por ejemplo, si gastas 24.000 € al año, tu número FIRE teórico sería:"
                ),
                html.Div(
                    html.Code("24.000 € × 25 = 600.000 €"),
                    className="bg-light border rounded-3 p-3 mb-3 d-block"
                ),
                html.P(
                    "Eso no significa que 600.000 € garanticen nada por sí solos. Es solo un punto de partida "
                    "que conviene adaptar a impuestos, inflación, comisiones, edad, flexibilidad de gasto y "
                    "tipo de cartera.",
                    className="mb-0"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4"
    )


def fire_calculator_cta():
    return dbc.Card(
        dbc.CardBody(
            [
                html.H2("Calcula tu objetivo FIRE", className="h4 fw-bold mb-2"),
                html.P(
                    "La mejor forma de aterrizar esta idea es usar una calculadora y ajustar tus propios datos: "
                    "gastos, patrimonio, aportaciones, rentabilidad e inflación.",
                    className="mb-3"
                ),
                dbc.Button(
                    "Ir a la calculadora FIRE",
                    href=FIRE_CALCULATOR_URL,
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
                html.H2("Una opción para empezar a construir patrimonio", className="h4 fw-bold mb-2"),
                html.P(
                    "Si estás empezando a invertir a largo plazo, puedes revisar plataformas como MyInvestor. "
                    "Antes de decidirte, compara bien productos, costes y fiscalidad para ver si encaja contigo.",
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
                    "Enlace de afiliado. Puede ayudarnos a mantener la web sin coste extra para ti.",
                    className="small text-muted mt-3 mb-0"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4"
    )


def faq_section():
    return html.Section(
        [
            html.H2("Preguntas frecuentes sobre FIRE", className="h3 fw-bold mt-5 mb-4"),
            html.H3("¿Qué significa exactamente FIRE?", className="h5 fw-bold"),
            html.P(
                "Es una estrategia de ahorro e inversión orientada a alcanzar la independencia financiera "
                "lo antes posible, con la opción de reducir o dejar el trabajo remunerado."
            ),
            html.H3("¿La regla del 4% siempre funciona?", className="h5 fw-bold mt-4"),
            html.P(
                "No. Es una referencia útil, pero no una garantía. Debe adaptarse a cada caso y al contexto "
                "de mercado, fiscalidad, edad y nivel de gasto."
            ),
            html.H3("¿FIRE es solo para sueldos altos?", className="h5 fw-bold mt-4"),
            html.P(
                "No necesariamente. Tener más ingresos ayuda, pero también importan mucho el nivel de gasto, "
                "la tasa de ahorro y la constancia inversora."
            ),
            html.H3("¿Hace falta querer jubilarse pronto?", className="h5 fw-bold mt-4"),
            html.P(
                "No. Mucha gente usa FIRE como herramienta para ganar seguridad financiera, poder negociar mejor "
                "su carrera o reducir jornada en el futuro."
            ),
        ]
    )


def article_body():
    return dbc.Row(
        [
            dbc.Col(
                [
                    key_takeaways(),

                    html.H2("Qué es FIRE y por qué atrae a tanta gente", className="h3 fw-bold mt-4 mb-3"),
                    html.P(
                        "El movimiento FIRE se ha hecho popular porque plantea una idea muy potente: vivir con menos "
                        "dependencia del salario y tener más control sobre tu tiempo. No se trata solo de dinero, sino "
                        "de opciones. Poder cambiar de trabajo, reducir jornada, tomarte un descanso o elegir proyectos "
                        "con menos presión también forma parte del atractivo de FIRE."
                    ),
                    html.P(
                        "Por eso conviene entenderlo como un espectro. Algunas personas aspiran a una independencia total; "
                        "otras solo buscan que su patrimonio cubra una parte creciente de sus gastos."
                    ),

                    number_fire_box(),

                    html.H2("La regla del 4%: útil, pero no perfecta", className="h3 fw-bold mt-4 mb-3"),
                    html.P(
                        "La regla del 4% es probablemente la referencia más conocida dentro del mundo FIRE. De forma simple, "
                        "plantea que una persona podría retirar aproximadamente el 4% anual de su cartera para financiar sus gastos."
                    ),
                    html.P(
                        "De ahí sale la idea de multiplicar los gastos anuales por 25. Sin embargo, esta cifra no debe tomarse "
                        "como una verdad universal. Puede variar según la composición de la cartera, los impuestos, la inflación, "
                        "la secuencia de rendimientos y tu flexibilidad para ajustar gastos."
                    ),

                    html.H2("Qué variables importan más para alcanzar FIRE", className="h3 fw-bold mt-4 mb-3"),
                    html.P(
                        "Aunque la atención suele centrarse en la rentabilidad, en la práctica hay varias variables que pesan mucho."
                    ),
                    html.Ul(
                        [
                            html.Li([html.Strong("Gasto anual: "), "es la base de tu número FIRE."]),
                            html.Li([html.Strong("Tasa de ahorro: "), "cuanto más ahorras, más rápido avanzas."]),
                            html.Li([html.Strong("Años invertidos: "), "el tiempo multiplica el efecto del interés compuesto."]),
                            html.Li([html.Strong("Rentabilidad real: "), "importa más la rentabilidad después de inflación."]),
                            html.Li([html.Strong("Flexibilidad personal: "), "si puedes ajustar gastos, tu plan gana solidez."]),
                        ]
                    ),
                    html.P(
                        "En muchos casos, mejorar la tasa de ahorro unos puntos porcentuales tiene más impacto que intentar "
                        "adivinar qué activo dará la mejor rentabilidad el próximo año."
                    ),

                    fire_calculator_cta(),

                    html.H2("Tipos de FIRE", className="h3 fw-bold mt-4 mb-3"),
                    html.P(
                        "No todo FIRE es igual. Con el tiempo han aparecido distintas variantes que ayudan a adaptar la filosofía "
                        "a perfiles y estilos de vida diferentes."
                    ),
                    html.Ul(
                        [
                            html.Li([html.Strong("Lean FIRE: "), "buscar independencia financiera con un nivel de gasto bajo."]),
                            html.Li([html.Strong("Fat FIRE: "), "aspirar a independencia con un nivel de vida más holgado."]),
                            html.Li([html.Strong("Barista FIRE: "), "cubrir parte de los gastos con inversiones y parte con trabajo flexible."]),
                            html.Li([html.Strong("Coast FIRE: "), "acumular pronto una base suficiente y después solo cubrir gastos corrientes."]),
                        ]
                    ),

                    html.H2("Errores frecuentes al planificar FIRE", className="h3 fw-bold mt-4 mb-3"),
                    html.Ul(
                        [
                            html.Li([html.Strong("Usar rentabilidades demasiado optimistas: "), "puede distorsionar todo el plan."]),
                            html.Li([html.Strong("Olvidar inflación e impuestos: "), "el patrimonio necesario suele ser mayor del que parece."]),
                            html.Li([html.Strong("No revisar los gastos reales: "), "muchas personas calculan FIRE con cifras poco realistas."]),
                            html.Li([html.Strong("Verlo como un todo o nada: "), "la independencia parcial también tiene mucho valor."]),
                            html.Li([html.Strong("Ignorar cambios vitales: "), "familia, vivienda o salud pueden modificar el objetivo."]),
                        ]
                    ),

                    affiliate_cta(),

                    faq_section(),

                    html.H2("Conclusión", className="h3 fw-bold mt-5 mb-3"),
                    html.P(
                        "FIRE no va solo de jubilarte joven. Va de construir una posición financiera que te dé más libertad, "
                        "más margen y menos dependencia de un único sueldo."
                    ),
                    html.P(
                        "Aunque nunca busques retirarte pronto, aplicar parte de esta filosofía puede ayudarte a vivir con más "
                        "seguridad, tomar mejores decisiones y acercarte a una independencia financiera progresiva."
                    ),
                    html.P(
                        [
                            "Si quieres aterrizarlo con números, prueba nuestra ",
                            dcc.Link("calculadora FIRE", href=FIRE_CALCULATOR_URL),
                            " y juega con distintos escenarios."
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
                                        html.Li("Qué es FIRE"),
                                        html.Li("Regla del 4%"),
                                        html.Li("Número FIRE"),
                                        html.Li("Tipos de FIRE"),
                                        html.Li("Errores frecuentes"),
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
                                    "Calcula cuántos años podrías tardar en alcanzar la independencia financiera.",
                                    className="mb-3"
                                ),
                                dbc.Button(
                                    "Abrir calculadora FIRE",
                                    href=FIRE_CALCULATOR_URL,
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
                                html.H3("Idea importante", className="h5 fw-bold mb-2"),
                                html.P(
                                    "FIRE no tiene por qué ser un objetivo extremo. También puede ser una forma de ganar libertad poco a poco.",
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
