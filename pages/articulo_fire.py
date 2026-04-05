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


def premium_badge(text, color="light"):
    return dbc.Badge(
        text,
        color=color,
        pill=True,
        class_name="px-3 py-2 rounded-pill fw-semibold me-2 mb-2"
    )


def section_header(title, subtitle=None, section_id=None):
    children = [
        html.H2(title, className="h3 fw-bold mb-2 article-section-title", id=section_id)
    ]
    if subtitle:
        children.append(html.P(subtitle, className="article-section-subtitle mb-0"))

    return html.Div(
        children,
        className="mb-4 article-section"
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
                                html.Span("FIRE", className="text-muted"),
                            ],
                            className="article-breadcrumb mb-4"
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                premium_badge("Guía 2026", "dark"),
                                                premium_badge("Independencia financiera", "light"),
                                                premium_badge("Regla del 4%", "light"),
                                                premium_badge("9 min lectura", "light"),
                                            ],
                                            className="mb-3 article-meta-badge"
                                        ),
                                        html.H1(
                                            "Qué es el movimiento FIRE, cómo funciona y cuánto dinero necesitas",
                                            className="fw-bold display-5 mb-3 article-title"
                                        ),
                                        html.P(
                                            "FIRE significa Financial Independence, Retire Early. La idea central es construir un patrimonio capaz de cubrir tus gastos y reducir tu dependencia del sueldo.",
                                            className="lead mb-3 article-lead"
                                        ),
                                        html.P(
                                            "Aunque mucha gente lo asocia a jubilarse muy joven, en la práctica también puede servir para ganar libertad, flexibilidad y tranquilidad financiera.",
                                            className="text-muted mb-4"
                                        ),
                                        html.Div(
                                            [
                                                dbc.Button(
                                                    "Probar calculadora FIRE",
                                                    href=FIRE_CALCULATOR_URL,
                                                    color="primary",
                                                    className="rounded-pill px-4 py-2 fw-semibold me-2 mb-2"
                                                ),
                                                dbc.Button(
                                                    "Ir al resumen rápido",
                                                    href="#ideas-clave",
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
                                                html.Div("Visual rápido", className="article-label"),
                                                html.Div("Gastos anuales × 25", className="h3 fw-bold mb-2"),
                                                html.P(
                                                    "es una forma orientativa de estimar tu número FIRE usando la regla del 4%",
                                                    className="text-muted mb-3"
                                                ),
                                                html.Div("FIRE ≠ dejar de trabajar ya", className="h5 fw-bold mb-1"),
                                                html.P(
                                                    "para mucha gente significa ganar opciones, no retirarse de inmediato",
                                                    className="text-muted mb-0"
                                                ),
                                            ]
                                        ),
                                        className="border-0 shadow-sm rounded-4 h-100 article-soft-card"
                                    ),
                                    lg=4,
                                    className="mt-4 mt-lg-0"
                                )
                            ],
                            className="align-items-center"
                        )
                    ]
                ),
                className="border-0 shadow-sm rounded-4 article-hero-card"
            ),
            lg=12
        ),
        className="pt-4 pt-md-5"
    )


def key_takeaways():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Resumen rápido", className="article-label"),
                html.H2("Ideas clave", className="h4 fw-bold mb-3", id="ideas-clave"),
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
        className="border-0 shadow-sm rounded-4 article-highlight-card"
    )


def insight_cards():
    items = [
        ("Libertad", "Más opciones vitales", "FIRE puede darte margen para cambiar de trabajo, reducir jornada o decidir con menos presión."),
        ("Ahorro", "Una variable central", "La tasa de ahorro suele influir más de lo que parece en la velocidad del plan."),
        ("Tiempo", "El multiplicador silencioso", "Cuantos más años inviertas, más ayuda recibes del interés compuesto."),
    ]

    cols = []
    for title, subtitle, text in items:
        cols.append(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(title, className="article-label"),
                            html.H3(subtitle, className="h5 fw-bold mb-2"),
                            html.P(text, className="mb-0 text-muted"),
                        ]
                    ),
                    className="border-0 shadow-sm rounded-4 h-100 article-soft-card article-insight-card"
                ),
                md=4,
                className="mb-3 mb-md-0"
            )
        )

    return dbc.Row(cols, className="my-4")


def number_fire_box():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Ejemplo rápido", className="article-label"),
                html.H2("Calcular tu número FIRE", className="h4 fw-bold mb-3", id="numero-fire"),
                html.P(
                    "Una forma sencilla de estimar tu objetivo FIRE es multiplicar tus gastos anuales por 25. Es la referencia asociada a la regla del 4%."
                ),
                html.P(
                    "Por ejemplo, si gastas 24.000 € al año, tu número FIRE teórico sería:"
                ),
                html.Div(
                    html.Code("24.000 € × 25 = 600.000 €"),
                    className="article-code-box p-3 mb-3 d-block"
                ),
                html.P(
                    "Eso no significa que 600.000 € garanticen nada por sí solos. Es solo un punto de partida que conviene adaptar a impuestos, inflación, comisiones, edad, flexibilidad de gasto y tipo de cartera.",
                    className="mb-0"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4 article-soft-card"
    )


def fire_calculator_cta():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Herramienta", className="article-label"),
                html.H2("Calcula tu objetivo FIRE", className="h4 fw-bold mb-2"),
                html.P(
                    "La mejor forma de aterrizar esta idea es usar una calculadora y ajustar tus propios datos: gastos, patrimonio, aportaciones, rentabilidad e inflación.",
                    className="mb-3"
                ),
                dbc.Button(
                    "Ir a la calculadora FIRE",
                    href=FIRE_CALCULATOR_URL,
                    color="primary",
                    className="rounded-pill px-4 py-2 fw-semibold"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4 article-inline-cta"
    )


def affiliate_cta():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Plataforma sugerida", className="article-label"),
                html.H2("Una opción para empezar a construir patrimonio", className="h4 fw-bold mb-2"),
                html.P(
                    "Si estás empezando a invertir a largo plazo, puedes revisar plataformas como MyInvestor. Antes de decidirte, compara bien productos, costes y fiscalidad para ver si encaja contigo.",
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
                    "Enlace de afiliado. Puede ayudarnos a mantener la web sin coste extra para ti.",
                    className="small text-muted mt-3 mb-0"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4 article-affiliate-cta"
    )


def quote_box():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Idea importante", className="article-label"),
                html.Blockquote(
                    "FIRE no tiene por qué ser un objetivo extremo. También puede ser una forma de ganar libertad poco a poco.",
                    className="blockquote mb-2 article-quote"
                ),
                html.P(
                    "La independencia financiera parcial también tiene mucho valor, aunque nunca busques retirarte pronto.",
                    className="mb-0 text-muted"
                )
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4 article-highlight-card"
    )


def faq_item(question, answer):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H3(question, className="h5 fw-bold mb-2"),
                html.P(answer, className="mb-0 text-muted"),
            ]
        ),
        className="border-0 shadow-sm rounded-4 mb-3 article-faq-card article-soft-card"
    )


def faq_section():
    return html.Section(
        [
            section_header(
                "Preguntas frecuentes sobre FIRE",
                "Las dudas más habituales, respondidas de forma clara.",
                "faq"
            ),
            faq_item(
                "¿Qué significa exactamente FIRE?",
                "Es una estrategia de ahorro e inversión orientada a alcanzar la independencia financiera lo antes posible, con la opción de reducir o dejar el trabajo remunerado."
            ),
            faq_item(
                "¿La regla del 4% siempre funciona?",
                "No. Es una referencia útil, pero no una garantía. Debe adaptarse a cada caso y al contexto de mercado, fiscalidad, edad y nivel de gasto."
            ),
            faq_item(
                "¿FIRE es solo para sueldos altos?",
                "No necesariamente. Tener más ingresos ayuda, pero también importan mucho el nivel de gasto, la tasa de ahorro y la constancia inversora."
            ),
            faq_item(
                "¿Hace falta querer jubilarse pronto?",
                "No. Mucha gente usa FIRE como herramienta para ganar seguridad financiera, poder negociar mejor su carrera o reducir jornada en el futuro."
            ),
        ],
        className="mt-5"
    )


def related_articles():
    cards = [
        (
            "Calculadora FIRE",
            "Descubre cuántos años podrías tardar en alcanzar la independencia financiera.",
            FIRE_CALCULATOR_URL,
            "Abrir calculadora FIRE"
        ),
        (
            "Calculadora de interés compuesto",
            "Simula cómo puede crecer tu patrimonio con aportaciones periódicas.",
            "/calculadora",
            "Ver interés compuesto"
        ),
        (
            "Calculadora de hipoteca",
            "Calcula cuota mensual, coste total e impacto del tipo de interés.",
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
                    className="border-0 shadow-sm rounded-4 h-100 article-related-card article-soft-card"
                ),
                md=4,
                className="mb-3 mb-md-0"
            )
        )

    return html.Section(
        [
            section_header(
                "Sigue explorando",
                "Otras herramientas útiles de interescompuesto.app",
                "relacionados"
            ),
            dbc.Row(cols)
        ],
        className="mt-5"
    )


def table_of_contents():
    items = [
        ("Qué es FIRE", "#que-es"),
        ("Regla del 4%", "#regla-4"),
        ("Número FIRE", "#numero-fire"),
        ("Variables clave", "#variables"),
        ("Tipos de FIRE", "#tipos-fire"),
        ("Errores frecuentes", "#errores"),
        ("FAQ", "#faq"),
    ]

    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Navegación", className="article-label"),
                html.H3("En este artículo", className="h5 fw-bold mb-3"),
                html.Ul(
                    [
                        html.Li(html.A(label, href=href, className="text-decoration-none"))
                        for label, href in items
                    ],
                    className="mb-0 article-toc"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 mb-4 article-side-card"
    )


def sidebar_blocks():
    return html.Div(
        [
            table_of_contents(),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div("Herramienta recomendada", className="article-label"),
                        html.H3("Calcula tu objetivo FIRE", className="h5 fw-bold mb-2"),
                        html.P(
                            "Simula cuántos años podrías tardar en alcanzar la independencia financiera.",
                            className="mb-3 text-muted"
                        ),
                        dbc.Button(
                            "Abrir calculadora FIRE",
                            href=FIRE_CALCULATOR_URL,
                            color="outline-primary",
                            className="rounded-pill px-4 fw-semibold"
                        ),
                    ]
                ),
                className="border-0 shadow-sm rounded-4 mb-4 article-side-card"
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div("Consejo", className="article-label"),
                        html.H3("FIRE también puede ser gradual", className="h5 fw-bold mb-2"),
                        html.P(
                            "No necesitas verlo como un todo o nada. Reducir dependencia del sueldo ya es una mejora importante.",
                            className="mb-0 text-muted"
                        ),
                    ]
                ),
                className="border-0 shadow-sm rounded-4 mb-4 article-highlight-card"
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div("Afiliado", className="article-label"),
                        html.H3("Ver MyInvestor", className="h5 fw-bold mb-2"),
                        html.P(
                            "Revisa opciones para invertir a largo plazo y construir patrimonio.",
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
                className="border-0 shadow-sm rounded-4 article-affiliate-cta"
            ),
        ],
        className="article-side-sticky"
    )


def article_body():
    return dbc.Row(
        [
            dbc.Col(
                html.Div(
                    [
                        insight_cards(),
                        key_takeaways(),

                        html.Hr(className="article-divider"),

                        section_header(
                            "Qué es FIRE y por qué atrae a tanta gente",
                            "No va solo de jubilarse joven, sino de ganar opciones.",
                            "que-es"
                        ),
                        html.Div(
                            [
                                html.P(
                                    "El movimiento FIRE se ha hecho popular porque plantea una idea muy potente: vivir con menos dependencia del salario y tener más control sobre tu tiempo. No se trata solo de dinero, sino de opciones."
                                ),
                                html.P(
                                    "Poder cambiar de trabajo, reducir jornada, tomarte un descanso o elegir proyectos con menos presión también forma parte del atractivo de FIRE."
                                ),
                                html.P(
                                    "Por eso conviene entenderlo como un espectro. Algunas personas aspiran a una independencia total; otras solo buscan que su patrimonio cubra una parte creciente de sus gastos."
                                ),
                            ],
                            className="article-content"
                        ),

                        number_fire_box(),

                        html.Hr(className="article-divider"),

                        section_header(
                            "La regla del 4%: útil, pero no perfecta",
                            "Una referencia práctica, no una garantía matemática.",
                            "regla-4"
                        ),
                        html.Div(
                            [
                                html.P(
                                    "La regla del 4% es probablemente la referencia más conocida dentro del mundo FIRE. De forma simple, plantea que una persona podría retirar aproximadamente el 4% anual de su cartera para financiar sus gastos."
                                ),
                                html.P(
                                    "De ahí sale la idea de multiplicar los gastos anuales por 25. Sin embargo, esta cifra no debe tomarse como una verdad universal."
                                ),
                                html.P(
                                    "Puede variar según la composición de la cartera, los impuestos, la inflación, la secuencia de rendimientos y tu flexibilidad para ajustar gastos."
                                ),
                            ],
                            className="article-content"
                        ),

                        section_header(
                            "Qué variables importan más para alcanzar FIRE",
                            "No todo depende de la rentabilidad.",
                            "variables"
                        ),
                        html.Div(
                            [
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
                                    "En muchos casos, mejorar la tasa de ahorro unos puntos porcentuales tiene más impacto que intentar adivinar qué activo dará la mejor rentabilidad el próximo año."
                                ),
                            ],
                            className="article-content"
                        ),

                        fire_calculator_cta(),
                        quote_box(),

                        html.Hr(className="article-divider"),

                        section_header(
                            "Tipos de FIRE",
                            "La filosofía puede adaptarse a estilos de vida muy distintos.",
                            "tipos-fire"
                        ),
                        html.Div(
                            [
                                html.P(
                                    "No todo FIRE es igual. Con el tiempo han aparecido distintas variantes que ayudan a adaptar la filosofía a perfiles y estilos de vida diferentes."
                                ),
                                html.Ul(
                                    [
                                        html.Li([html.Strong("Lean FIRE: "), "buscar independencia financiera con un nivel de gasto bajo."]),
                                        html.Li([html.Strong("Fat FIRE: "), "aspirar a independencia con un nivel de vida más holgado."]),
                                        html.Li([html.Strong("Barista FIRE: "), "cubrir parte de los gastos con inversiones y parte con trabajo flexible."]),
                                        html.Li([html.Strong("Coast FIRE: "), "acumular pronto una base suficiente y después solo cubrir gastos corrientes."]),
                                    ]
                                ),
                            ],
                            className="article-content"
                        ),

                        html.Hr(className="article-divider"),

                        section_header(
                            "Errores frecuentes al planificar FIRE",
                            "Pequeños supuestos irreales pueden distorsionar todo el plan.",
                            "errores"
                        ),
                        html.Div(
                            [
                                html.Ul(
                                    [
                                        html.Li([html.Strong("Usar rentabilidades demasiado optimistas: "), "puede distorsionar todo el plan."]),
                                        html.Li([html.Strong("Olvidar inflación e impuestos: "), "el patrimonio necesario suele ser mayor del que parece."]),
                                        html.Li([html.Strong("No revisar los gastos reales: "), "muchas personas calculan FIRE con cifras poco realistas."]),
                                        html.Li([html.Strong("Verlo como un todo o nada: "), "la independencia parcial también tiene mucho valor."]),
                                        html.Li([html.Strong("Ignorar cambios vitales: "), "familia, vivienda o salud pueden modificar el objetivo."]),
                                    ]
                                ),
                            ],
                            className="article-content"
                        ),

                        affiliate_cta(),
                        faq_section(),
                        related_articles(),

                        html.Hr(className="article-divider"),

                        section_header("Conclusión"),
                        html.Div(
                            [
                                html.P(
                                    "FIRE no va solo de jubilarte joven. Va de construir una posición financiera que te dé más libertad, más margen y menos dependencia de un único sueldo."
                                ),
                                html.P(
                                    "Aunque nunca busques retirarte pronto, aplicar parte de esta filosofía puede ayudarte a vivir con más seguridad, tomar mejores decisiones y acercarte a una independencia financiera progresiva."
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
                            className="article-content"
                        ),
                    ]
                ),
                lg=8,
                xl=8
            ),
            dbc.Col(
                sidebar_blocks(),
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
    className="py-2 px-3 px-md-4 px-lg-5 article-shell"
)
