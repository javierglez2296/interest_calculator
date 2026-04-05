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


def article_styles():
    return html.Style("""
    :root {
        --article-primary: #2563eb;
        --article-primary-dark: #1d4ed8;
        --article-danger: #dc2626;
        --article-text: #101828;
        --article-text-soft: #667085;
        --article-border: rgba(16,24,40,0.06);
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
            linear-gradient(135deg, rgba(37,99,235,0.08) 0%, rgba(37,99,235,0.04) 100%),
            #ffffff;
        border: 1px solid rgba(37,99,235,0.08);
    }

    .article-warning-cta {
        background:
            linear-gradient(135deg, rgba(220,38,38,0.08) 0%, rgba(37,99,235,0.05) 100%),
            #ffffff;
        border: 1px solid rgba(220,38,38,0.10);
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
    [data-bs-theme="dark"] .article-warning-cta {
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
                                html.Span("Hipoteca", className="text-muted"),
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
                                                premium_badge("Hipoteca", "light"),
                                                premium_badge("Vivienda", "light"),
                                                premium_badge("11 min lectura", "light"),
                                            ],
                                            className="mb-3 article-meta-badge"
                                        ),
                                        html.H1(
                                            "Cómo calcular una hipoteca y cuánto pagarás de verdad",
                                            className="fw-bold display-5 mb-3 article-title"
                                        ),
                                        html.P(
                                            "Cuando miras una vivienda, es fácil centrarse solo en el precio de compra. Pero la decisión real pasa por otra pregunta: cuánto capital vas a financiar, qué cuota mensual asumirás y cuánto terminarás pagando entre intereses y gastos.",
                                            className="lead mb-3 article-lead"
                                        ),
                                        html.P(
                                            "Una hipoteca puede ser razonable y sostenible, o convertirse en una carga que limite tu ahorro durante años. La diferencia suele estar en hacer bien los números antes de firmar.",
                                            className="text-muted mb-4"
                                        ),
                                        html.Div(
                                            [
                                                dbc.Button(
                                                    "Probar calculadora hipotecaria",
                                                    href=HIPOTECA_CALCULATOR_URL,
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
                                                html.Div("Cuota baja ≠ buena hipoteca", className="h4 fw-bold mb-2"),
                                                html.P(
                                                    "alargar mucho el plazo reduce la mensualidad, pero puede disparar el coste total de intereses",
                                                    className="text-muted mb-3"
                                                ),
                                                html.Div("Comprar con margen importa", className="h5 fw-bold mb-1"),
                                                html.P(
                                                    "llegar sin liquidez a la firma puede tensar tus finanzas desde el primer día",
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
        className="border-0 shadow-sm rounded-4 article-highlight-card"
    )


def insight_cards():
    items = [
        ("Cuota", "No es toda la historia", "Una mensualidad asumible puede seguir escondiendo un coste total demasiado alto."),
        ("Liquidez", "Te protege más de lo que parece", "Llegar con colchón a la compra suele ser mucho más sano que firmar al límite."),
        ("Plazo", "Reduce cuota, sube coste", "Alargar años puede ayudar al flujo mensual, pero también encarecer bastante la operación."),
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


def example_box():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Ejemplo práctico", className="article-label"),
                html.H2("Qué ocurre con una vivienda de 280.000 €", className="h4 fw-bold mb-3", id="ejemplo"),
                html.P(
                    "Imagina una vivienda de 280.000 €. Si puedes aportar 56.000 € de entrada, el importe a financiar sería de 224.000 €."
                ),
                html.P(
                    "A partir de ahí, la cuota mensual cambia bastante según el interés y el plazo. No es lo mismo devolver ese préstamo a 25 años que a 30 años."
                ),
                html.P(
                    "En general, cuanto más largo sea el plazo, menor será la cuota mensual. Pero también mayor será el coste total de intereses al final de la hipoteca.",
                    className="mb-0"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4 article-soft-card"
    )


def warning_box():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Error frecuente", className="article-label"),
                html.H2("El error típico al comprar vivienda", className="h4 fw-bold mb-3 text-danger", id="error-tipico"),
                html.P(
                    "Muchísimas personas se preguntan solo: “¿Puedo pagar esta cuota?”. La pregunta correcta es más amplia: “¿Puedo pagar esta cuota, mantener ahorro, cubrir imprevistos y seguir teniendo margen de vida?”.",
                    className="mb-0"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4 article-warning-cta"
    )


def savings_box():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Ahorro previo", className="article-label"),
                html.H2("Cuánto deberías ahorrar antes de comprar", className="h4 fw-bold mb-3", id="ahorro-previo"),
                html.P(
                    "Uno de los mayores errores al comprar vivienda es llegar justo a la firma. Aunque la cuota parezca asumible, muchas operaciones se complican porque el comprador ha consumido casi todo su ahorro en entrada y gastos."
                ),
                html.P("Antes de hipotecarte, intenta valorar tres capas de ahorro:"),
                html.Ul(
                    [
                        html.Li([html.Strong("Entrada: "), "la parte del precio que no cubre el banco."]),
                        html.Li([html.Strong("Gastos de compra: "), "impuestos, tasación y otros costes asociados."]),
                        html.Li([html.Strong("Colchón de seguridad: "), "reserva para no quedarte sin liquidez tras la compra."]),
                    ],
                    className="mb-3"
                ),
                html.P(
                    "Comprar con margen suele ser mucho más sano que comprar al límite, incluso si eso implica esperar un poco más o elegir una vivienda algo más barata.",
                    className="mb-0"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4 article-soft-card"
    )


def calculator_cta():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Herramienta", className="article-label"),
                html.H2("Haz tu simulación hipotecaria", className="h4 fw-bold mb-2"),
                html.P(
                    "Prueba distintos escenarios de precio, entrada, interés y plazo para ver qué cuota tendrías y si de verdad encaja en tu situación financiera.",
                    className="mb-3"
                ),
                dbc.Button(
                    "Ir a la calculadora de hipoteca",
                    href=HIPOTECA_CALCULATOR_URL,
                    color="primary",
                    className="rounded-pill px-4 py-2 fw-semibold"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4 article-inline-cta"
    )


def compare_box():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Comparativa", className="article-label"),
                html.H2("Hipoteca fija vs variable", className="h4 fw-bold mb-3", id="fija-vs-variable"),
                html.P(
                    [
                        html.Strong("Hipoteca fija: "),
                        "sabes desde el principio cuánto pagarás cada mes. Suele dar tranquilidad y facilita planificar."
                    ]
                ),
                html.P(
                    [
                        html.Strong("Hipoteca variable: "),
                        "la cuota puede subir o bajar con los tipos de interés. Puede salir mejor o peor, pero introduce incertidumbre."
                    ]
                ),
                html.P(
                    "La mejor opción no es universal. Depende de tu tolerancia al riesgo, tu estabilidad financiera y del valor que le des a una cuota estable.",
                    className="mb-0"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4 article-soft-card"
    )


def rent_vs_buy_box():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Decisión de vivienda", className="article-label"),
                html.H2("¿Alquilar o comprar?", className="h4 fw-bold mb-3", id="alquilar-o-comprar"),
                html.P(
                    "Comprar no siempre es automáticamente mejor que alquilar. Depende del precio de la vivienda, de tus planes a medio plazo, del coste de oportunidad de tus ahorros y del nivel de cuota que asumirías respecto a tus ingresos."
                ),
                html.P(
                    "Comprar puede tener sentido si vas a permanecer años en la vivienda, tienes estabilidad y la operación no te deja sin margen. Alquilar puede ser preferible si necesitas flexibilidad o si comprar te obliga a tensionar demasiado tus finanzas.",
                    className="mb-0"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 my-4 article-soft-card"
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
                "Preguntas frecuentes sobre hipotecas",
                "Las dudas más habituales, respondidas de forma clara.",
                "faq"
            ),
            faq_item(
                "¿Qué datos necesito para calcular una hipoteca?",
                "Los cuatro más importantes son el precio de compra, la entrada disponible, el tipo de interés y el plazo del préstamo."
            ),
            faq_item(
                "¿Cuánto debería destinar a la cuota?",
                "Como referencia general, suele considerarse prudente no superar aproximadamente el 30% al 35% de los ingresos netos del hogar."
            ),
            faq_item(
                "¿Qué gastos hay además de la cuota mensual?",
                "Además de la cuota, conviene contar con entrada, impuestos, tasación, posibles gastos administrativos, reformas, mobiliario, seguros y mantenimiento."
            ),
            faq_item(
                "¿Qué es más importante: la cuota o el coste total?",
                "Las dos cosas. Una cuota baja puede parecer atractiva, pero si alargas demasiado el plazo terminarás pagando muchos más intereses."
            ),
            faq_item(
                "¿Es mala idea comprar quedándote sin ahorros?",
                "Suele ser arriesgado. Lo más prudente es llegar a la compra con cierto margen de liquidez para no depender de que todo salga perfecto tras la firma."
            ),
        ],
        className="mt-5"
    )


def related_articles():
    cards = [
        (
            "Calculadora de hipoteca",
            "Calcula tu cuota mensual y compara escenarios de interés, plazo y entrada.",
            HIPOTECA_CALCULATOR_URL,
            "Abrir calculadora hipotecaria"
        ),
        (
            "Calculadora FIRE",
            "Comprueba cómo encaja la compra de vivienda dentro de tu independencia financiera.",
            "/fire",
            "Ver calculadora FIRE"
        ),
        (
            "Calculadora de interés compuesto",
            "Analiza el coste de oportunidad de tus ahorros y tus inversiones a largo plazo.",
            "/calculadora",
            "Ver interés compuesto"
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
        ("Cómo se calcula", "#como-se-calcula"),
        ("Ahorro previo", "#ahorro-previo"),
        ("Gastos reales", "#gastos-reales"),
        ("Cuota prudente", "#cuota-prudente"),
        ("Fija vs variable", "#fija-vs-variable"),
        ("Alquilar o comprar", "#alquilar-o-comprar"),
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
                        html.H3("Calcula tu cuota mensual", className="h5 fw-bold mb-2"),
                        html.P(
                            "Compara distintos escenarios de interés, plazo y entrada antes de decidir.",
                            className="mb-3 text-muted"
                        ),
                        dbc.Button(
                            "Abrir calculadora",
                            href=HIPOTECA_CALCULATOR_URL,
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
                        html.Div("Consejo práctico", className="article-label"),
                        html.H3("Una vivienda no debe dejarte sin margen", className="h5 fw-bold mb-2"),
                        html.P(
                            "Si una operación solo te encaja en el escenario más optimista, probablemente no te encaja de verdad.",
                            className="mb-0 text-muted"
                        ),
                    ]
                ),
                className="border-0 shadow-sm rounded-4 mb-4 article-highlight-card"
            ),
            dbc.Card(
                dbc.CardBody(
                    [
                        html.Div("Siguiente paso", className="article-label"),
                        html.H3("Simula una cuota cómoda", className="h5 fw-bold mb-2"),
                        html.P(
                            "Haz números con una cuota que te deje ahorro, liquidez y margen para imprevistos.",
                            className="mb-0 text-muted"
                        ),
                    ]
                ),
                className="border-0 shadow-sm rounded-4 article-soft-card"
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
                            "Cómo se calcula una hipoteca",
                            "Capital, interés y plazo: la base del cálculo.",
                            "como-se-calcula"
                        ),
                        html.Div(
                            [
                                html.P(
                                    "Calcular una hipoteca consiste en estimar la cuota mensual que pagarás a partir de tres elementos: capital prestado, tipo de interés y plazo. A eso luego debes sumarle una visión más amplia del coste total."
                                ),
                                html.P(
                                    "Dicho de forma simple: primero defines cuánto dinero te presta el banco, después aplicas el interés y finalmente distribuyes la devolución a lo largo de los años del préstamo."
                                ),
                            ],
                            className="article-content"
                        ),

                        example_box(),
                        warning_box(),

                        section_header(
                            "Los 4 datos básicos que necesitas",
                            "Sin estos datos, cualquier cálculo queda cojo."
                        ),
                        html.Div(
                            [
                                html.Ul(
                                    [
                                        html.Li([html.Strong("Precio de compra: "), "el valor total de la vivienda."]),
                                        html.Li([html.Strong("Entrada: "), "el ahorro que aportas de tu bolsillo."]),
                                        html.Li([html.Strong("Tipo de interés: "), "el porcentaje que cobra el banco por prestarte el dinero."]),
                                        html.Li([html.Strong("Plazo: "), "los años durante los que devolverás el préstamo."]),
                                    ]
                                ),
                                html.P(
                                    "Con estos datos puedes calcular una estimación bastante útil. Pero una buena decisión hipotecaria no termina cuando conoces la cuota."
                                ),
                            ],
                            className="article-content"
                        ),

                        savings_box(),

                        html.Hr(className="article-divider"),

                        section_header(
                            "Qué gastos debes mirar además de la cuota",
                            "La mensualidad no es todo el coste de comprar vivienda.",
                            "gastos-reales"
                        ),
                        html.Div(
                            [
                                html.P(
                                    "Uno de los errores más caros es pensar que comprar vivienda solo exige pagar la entrada y luego la mensualidad. En la práctica, hay varios costes que conviene incluir desde el principio."
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
                            ],
                            className="article-content"
                        ),

                        calculator_cta(),

                        section_header(
                            "Qué cuota suele ser prudente",
                            "Una referencia útil, pero no suficiente por sí sola.",
                            "cuota-prudente"
                        ),
                        html.Div(
                            [
                                html.P(
                                    "Como referencia general, suele recomendarse que la cuota hipotecaria no supere aproximadamente el 30% al 35% de los ingresos netos del hogar."
                                ),
                                html.P(
                                    "Pero esa referencia no basta por sí sola. También importa mucho tu estabilidad laboral, el colchón de emergencia, si tienes hijos, otros préstamos, gastos fijos elevados o planes de ahorro relevantes."
                                ),
                                html.P(
                                    "Una cuota asumible sobre el papel puede ser demasiado exigente en la práctica si te deja sin capacidad de maniobra."
                                ),
                            ],
                            className="article-content"
                        ),

                        compare_box(),

                        html.Hr(className="article-divider"),

                        section_header(
                            "Errores frecuentes al comparar hipotecas",
                            "Pequeños atajos mentales pueden salir caros.",
                            "errores"
                        ),
                        html.Div(
                            [
                                html.Ul(
                                    [
                                        html.Li([html.Strong("Mirar solo la cuota mensual: "), "sin valorar el coste total del préstamo."]),
                                        html.Li([html.Strong("Agotar todos los ahorros: "), "y quedarse sin colchón después de la compra."]),
                                        html.Li([html.Strong("Elegir plazo largo solo para bajar cuota: "), "sin medir cuánto encarece la operación."]),
                                        html.Li([html.Strong("No comparar escenarios: "), "fija frente a variable, distintos intereses o entradas."]),
                                        html.Li([html.Strong("Subestimar gastos futuros: "), "comunidad, reparaciones, IBI o mantenimiento."]),
                                    ]
                                ),
                            ],
                            className="article-content"
                        ),

                        rent_vs_buy_box(),
                        faq_section(),
                        related_articles(),

                        html.Hr(className="article-divider"),

                        section_header("Conclusión"),
                        html.Div(
                            [
                                html.P(
                                    "Comprar vivienda no es solo una decisión emocional. También es una de las mayores decisiones financieras que tomarás en muchos años."
                                ),
                                html.P(
                                    "Antes de firmar, conviene saber cuánto capital financias, qué cuota mensual tendrás, cuánto pagarás en total y con cuánto margen de liquidez te quedarás después."
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
