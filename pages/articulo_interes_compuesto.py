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


def article_styles():
    return html.Style("""
    :root {
        --article-primary: #2563eb;
        --article-primary-dark: #1d4ed8;
        --article-success: #16a34a;
        --article-text: #101828;
        --article-text-soft: #667085;
        --article-border: rgba(16,24,40,0.06);
        --article-bg-soft: #f8fbff;
    }

    html {
        scroll-behavior: smooth;
    }

    .article-shell {
        max-width: 100%;
    }

    .article-hero-card {
        background:
            radial-gradient(circle at top left, rgba(37,99,235,0.14), transparent 32%),
            linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
        border: 1px solid rgba(37,99,235,0.08);
    }

    .article-breadcrumb {
        font-size: 0.9rem;
    }

    .article-breadcrumb a {
        color: var(--article-primary-dark);
        text-decoration: none;
    }

    .article-breadcrumb a:hover {
        text-decoration: underline;
    }

    .article-title {
        color: var(--article-text);
        letter-spacing: -0.03em;
        line-height: 1.05;
    }

    .article-lead {
        color: var(--article-text-soft);
        font-size: 1.08rem;
        max-width: 880px;
    }

    .article-meta-badge .badge {
        border-radius: 999px !important;
    }

    .article-soft-card,
    .article-side-card,
    .article-highlight-card,
    .article-table-card,
    .article-cta-card {
        background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
    }

    .article-section {
        scroll-margin-top: 110px;
    }

    .article-section-title {
        color: var(--article-text);
        letter-spacing: -0.02em;
    }

    .article-section-subtitle {
        color: var(--article-text-soft);
    }

    .article-content p,
    .article-content li {
        color: #344054;
        line-height: 1.85;
        font-size: 1.04rem;
    }

    .article-content ul {
        padding-left: 1.2rem;
    }

    .article-content li {
        margin-bottom: 0.65rem;
    }

    .article-label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--article-primary-dark);
        font-weight: 800;
        margin-bottom: 0.55rem;
    }

    .article-side-sticky {
        position: sticky;
        top: 100px;
    }

    .article-toc a {
        color: #475467;
        text-decoration: none;
    }

    .article-toc a:hover {
        color: var(--article-primary-dark);
    }

    .article-toc li {
        margin-bottom: 0.55rem;
    }

    .article-quote {
        font-size: 1.15rem;
        line-height: 1.7;
        color: var(--article-text);
    }

    .article-code-box {
        background: #f8fafc;
        border: 1px solid rgba(16,24,40,0.06);
        border-radius: 1rem;
    }

    .article-inline-cta {
        background:
            linear-gradient(135deg, rgba(37,99,235,0.08) 0%, rgba(22,163,74,0.06) 100%),
            #ffffff;
        border: 1px solid rgba(37,99,235,0.08);
    }

    .article-affiliate-cta {
        background:
            linear-gradient(135deg, rgba(22,163,74,0.12) 0%, rgba(37,99,235,0.08) 100%),
            #ffffff;
        border: 1px solid rgba(16,24,40,0.06);
    }

    .article-divider {
        margin: 3rem 0;
        opacity: 0.08;
    }

    .article-related-card,
    .article-insight-card,
    .article-faq-card {
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .article-related-card:hover,
    .article-insight-card:hover,
    .article-faq-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 34px rgba(16,24,40,0.10) !important;
    }

    [data-bs-theme="dark"] .article-title,
    [data-bs-theme="dark"] .article-section-title,
    [data-bs-theme="dark"] .article-quote {
        color: #f8fafc;
    }

    [data-bs-theme="dark"] .article-lead,
    [data-bs-theme="dark"] .article-section-subtitle,
    [data-bs-theme="dark"] .article-content p,
    [data-bs-theme="dark"] .article-content li,
    [data-bs-theme="dark"] .article-toc a {
        color: #cbd5e1;
    }

    [data-bs-theme="dark"] .article-hero-card,
    [data-bs-theme="dark"] .article-soft-card,
    [data-bs-theme="dark"] .article-side-card,
    [data-bs-theme="dark"] .article-highlight-card,
    [data-bs-theme="dark"] .article-table-card,
    [data-bs-theme="dark"] .article-cta-card,
    [data-bs-theme="dark"] .article-inline-cta,
    [data-bs-theme="dark"] .article-affiliate-cta {
        background: #111827;
        border-color: rgba(255,255,255,0.08);
    }

    [data-bs-theme="dark"] .article-code-box {
        background: #0f172a;
        border-color: rgba(255,255,255,0.08);
    }

    @media (max-width: 991.98px) {
        .article-side-sticky {
            position: static;
        }
    }

    @media (max-width: 768px) {
        .article-title {
            font-size: 2.2rem !important;
            line-height: 1.08;
        }

        .article-lead {
            font-size: 1rem;
        }

        .article-content p,
        .article-content li {
            font-size: 1rem;
            line-height: 1.8;
        }
    }
    """)


def premium_badge(text, color="light"):
    return dbc.Badge(
        text,
        color=color,
        pill=True,
        class_name="px-3 py-2 rounded-pill fw-semibold me-2 mb-2"
    )


def section_header(title, subtitle=None, section_id=None):
    return html.Div(
        [
            html.H2(title, className="h3 fw-bold mb-2 article-section-title", id=section_id),
            html.P(subtitle, className="article-section-subtitle mb-0") if subtitle else None,
        ],
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
                                html.Span("Interés compuesto", className="text-muted"),
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
                                                premium_badge("Finanzas personales", "light"),
                                                premium_badge("Largo plazo", "light"),
                                                premium_badge("8 min lectura", "light"),
                                            ],
                                            className="mb-3 article-meta-badge"
                                        ),
                                        html.H1(
                                            "Qué es el interés compuesto y cómo funciona de verdad",
                                            className="fw-bold display-5 mb-3 article-title"
                                        ),
                                        html.P(
                                            "El interés compuesto hace que tu dinero no solo crezca por lo que inviertes, sino también por lo que van generando tus propias ganancias con el paso del tiempo.",
                                            className="lead mb-3 article-lead"
                                        ),
                                        html.P(
                                            "Es una de las ideas más importantes para construir patrimonio a largo plazo: menos ruido, más tiempo, más constancia y costes bajos.",
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


def key_takeaways():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Resumen rápido", className="article-label"),
                html.H2("Ideas clave", className="h4 fw-bold mb-3", id="ideas-clave"),
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
        className="border-0 shadow-sm rounded-4 article-highlight-card"
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
                            html.Div(period, className="article-label"),
                            html.H3(title, className="h5 fw-bold mb-2"),
                            html.P(text, className="mb-0 text-muted"),
                        ]
                    ),
                    className="border-0 shadow-sm rounded-4 h-100 article-soft-card"
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
                "El interés compuesto no suele impresionar al principio. Su fuerza aparece más tarde.",
                "crecimiento-tiempo"
            ),
            dbc.Row(cols)
        ],
        className="my-5"
    )


def comparison_table():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Comparativa", className="article-label"),
                html.H2("Interés simple vs interés compuesto", className="h4 fw-bold mb-3", id="comparativa"),
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
        className="border-0 shadow-sm rounded-4 my-4 article-table-card"
    )


def example_box():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Ejemplo sencillo", className="article-label"),
                html.H2("Qué ocurre con 10.000 € al 7%", className="h4 fw-bold mb-3", id="ejemplo"),
                html.P(
                    "Imagina que inviertes 10.000 € al 7% anual y no retiras nada. El primer año ganarías unos 700 €. Al siguiente, ya no se calcula sobre 10.000 €, sino sobre 10.700 €."
                ),
                html.P(
                    "Y después sobre una cifra todavía mayor. Ese es el núcleo del interés compuesto: la base va creciendo y cada periodo puede producir más que el anterior.",
                    className="mb-0"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4 article-soft-card"
    )


def formula_box():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Fórmula básica", className="article-label"),
                html.H2("Cómo se calcula", className="h4 fw-bold mb-3", id="formula"),
                html.P("La versión simplificada sería:", className="mb-3"),
                html.Div(
                    html.Code(
                        "Capital final = Capital inicial × (1 + rentabilidad)^n",
                        className="fs-6"
                    ),
                    className="article-code-box p-3 p-md-4 mb-3"
                ),
                html.P(
                    "Cuando añades aportaciones mensuales, inflación, comisiones o impuestos, el cálculo se vuelve más completo. Por eso tiene más sentido usar una calculadora real.",
                    className="mb-0 text-muted"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4 article-soft-card"
    )


def quote_box():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Idea central", className="article-label"),
                html.Blockquote(
                    "La mayoría de personas abandona antes de llegar a la fase donde el interés compuesto empieza a notarse de verdad.",
                    className="blockquote mb-2 article-quote"
                ),
                html.P(
                    "No porque el concepto falle, sino porque sus mejores resultados suelen llegar bastante tarde.",
                    className="mb-0 text-muted"
                )
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4 article-highlight-card"
    )


def calculator_cta():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Herramienta", className="article-label"),
                html.H2("Haz tu propia simulación", className="h4 fw-bold mb-2"),
                html.P(
                    "Cambia capital inicial, aportaciones, años, rentabilidad, inflación y costes para ver cómo afectan al resultado final.",
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
        className="border-0 shadow-sm rounded-4 my-4 article-inline-cta"
    )


def affiliate_cta():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Plataforma sugerida", className="article-label"),
                html.H2("Empieza con costes bajos", className="h4 fw-bold mb-2"),
                html.P(
                    "Si estás buscando una plataforma sencilla para ahorrar o invertir a largo plazo, puedes revisar MyInvestor. Compara siempre comisiones, productos y condiciones.",
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
        className="border-0 shadow-sm rounded-4 my-4 article-affiliate-cta"
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
                "Preguntas frecuentes sobre el interés compuesto",
                "Las dudas más habituales, respondidas de forma clara.",
                "faq"
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
        ("Qué es y cómo funciona", "#que-es"),
        ("Interés simple vs compuesto", "#comparativa"),
        ("Ejemplo sencillo", "#ejemplo"),
        ("Variables clave", "#variables"),
        ("Errores frecuentes", "#errores"),
        ("Fórmula", "#formula"),
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
                className="border-0 shadow-sm rounded-4 mb-4 article-side-card"
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div("Consejo", className="article-label"),
                        html.H3("La paciencia también rentabiliza", className="h5 fw-bold mb-2"),
                        html.P(
                            "Muchas veces la diferencia entre un resultado mediocre y uno muy bueno no está en la brillantez, sino en mantenerse durante años.",
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
                            "Cómo funciona el interés compuesto",
                            "La lógica es simple. El impacto acumulado, no tanto.",
                            "que-es"
                        ),
                        html.Div(
                            [
                                html.P(
                                    "El mecanismo es sencillo: inviertes un capital, ese capital genera rentabilidad, y en lugar de retirar las ganancias, las mantienes invertidas. A partir de ahí, el siguiente periodo arranca desde una base superior."
                                ),
                                html.P(
                                    "Eso hace que el crecimiento deje de ser lineal. Y ahí es donde aparece su fuerza: cada año no solo sumas dinero, también aumentas la base que puede seguir creciendo."
                                ),
                            ],
                            className="article-content"
                        ),

                        comparison_table(),
                        example_box(),
                        timeline_growth(),

                        html.Hr(className="article-divider"),

                        section_header(
                            "Las variables que más influyen",
                            "No todo pesa igual en el resultado final.",
                            "variables"
                        ),
                        html.Div(
                            [
                                html.P(
                                    "Aunque mucha gente se obsesiona con la rentabilidad, en la práctica el resultado suele depender de unas pocas variables que importan muchísimo."
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
                            ],
                            className="article-content"
                        ),

                        calculator_cta(),
                        quote_box(),

                        html.Hr(className="article-divider"),

                        section_header(
                            "Por qué empezar pronto marca tanta diferencia",
                            "La ventaja no siempre está en aportar más, sino en dejar más tiempo."
                        ),
                        html.Div(
                            [
                                html.P(
                                    "Dos personas pueden invertir cantidades parecidas, pero quien empieza antes suele acabar con bastante más. No porque sea mejor inversor, sino porque da más tiempo a que las ganancias se acumulen sobre sí mismas."
                                ),
                                html.P(
                                    "Los primeros años construyen la base. Y esa base es la que luego hace posible que el crecimiento se vuelva cada vez más visible."
                                ),
                            ],
                            className="article-content"
                        ),

                        html.Hr(className="article-divider"),

                        section_header(
                            "Qué puede frenar el interés compuesto",
                            "Pequeños errores repetidos durante años tienen mucho peso.",
                            "errores"
                        ),
                        html.Div(
                            [
                                html.Ul(
                                    [
                                        html.Li([html.Strong("Comisiones altas: "), "restan rentabilidad todos los años."]),
                                        html.Li([html.Strong("Entrar y salir sin parar: "), "rompe el efecto acumulativo."]),
                                        html.Li([html.Strong("Retirar el dinero demasiado pronto: "), "frena el crecimiento futuro."]),
                                        html.Li([html.Strong("No ser constante: "), "reduce uno de los motores principales del resultado final."]),
                                        html.Li([html.Strong("Buscar rentabilidades irreales: "), "puede llevarte a asumir riesgos innecesarios."]),
                                    ]
                                ),
                            ],
                            className="article-content"
                        ),

                        formula_box(),
                        affiliate_cta(),
                        faq_section(),
                        related_articles(),

                        html.Hr(className="article-divider"),

                        section_header("Conclusión"),
                        html.Div(
                            [
                                html.P(
                                    "El interés compuesto no es magia ni una promesa de riqueza rápida. Pero sí es uno de los mecanismos más potentes para construir patrimonio a largo plazo."
                                ),
                                html.P(
                                    "La combinación que mejor suele funcionar es bastante sobria: empezar cuanto antes, aportar de forma regular, mantener costes bajos y dejar trabajar al tiempo."
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
        article_styles(),
        seo_json_ld_block(),
        hero_section(),
        article_body(),
    ],
    fluid=True,
    className="py-2 px-3 px-md-4 px-lg-5 article-shell"
)
