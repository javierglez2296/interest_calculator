import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from components.disclaimer_afiliados import build_disclaimer
from utils.premium import STRIPE_PAYMENT_LINK

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/",
    title="Calculadoras financieras: interés compuesto, FIRE, hipoteca e inversión",
    name="Inicio",
    description=(
        "Calculadoras financieras gratis en español para interés compuesto, FIRE, "
        "hipoteca, rentabilidad de alquiler, inversión y libertad financiera."
    ),
)


# =========================================================
# DATA
# =========================================================

CALCULADORAS = [
    {
        "titulo": "Interés compuesto",
        "descripcion": "Simula cuánto puede crecer tu dinero con aportaciones periódicas, rentabilidad e inflación.",
        "href": "/calculadora",
        "icono": "📈",
        "badge": "Más usada",
        "destacada": True,
    },
    {
        "titulo": "FIRE",
        "descripcion": "Calcula cuánto necesitas para vivir de tus inversiones y alcanzar libertad financiera.",
        "href": "/fire",
        "icono": "🔥",
        "badge": "Libertad financiera",
        "destacada": False,
    },
    {
        "titulo": "Hipoteca",
        "descripcion": "Estima cuota mensual, intereses totales, entrada necesaria y esfuerzo financiero.",
        "href": "/hipoteca",
        "icono": "🏠",
        "badge": "Vivienda",
        "destacada": False,
    },
    {
        "titulo": "Rentabilidad alquiler",
        "descripcion": "Analiza cashflow, rentabilidad neta, gastos, hipoteca y retorno inmobiliario.",
        "href": "/rentabilidad-alquiler",
        "icono": "💸",
        "badge": "Inmobiliario",
        "destacada": False,
    },
    {
        "titulo": "Comparador de inversión",
        "descripcion": "Compara vivienda, bolsa, fondos, monetarios y otras alternativas con números.",
        "href": "/comparador",
        "icono": "⚖️",
        "badge": "Comparativa",
        "destacada": False,
    },
]

GUIAS_POPULARES = [
    {
        "titulo": "Invertir 500 € al mes",
        "texto": "Simula cuánto podrías acumular invirtiendo 500 € mensuales a largo plazo.",
        "href": "/invertir-500-euros-mes",
        "tag": "Inversión mensual",
    },
    {
        "titulo": "Cómo conseguir 100.000 €",
        "texto": "Guía realista para llegar a 100.000 € mediante ahorro e interés compuesto.",
        "href": "/como-conseguir-100000-euros",
        "tag": "Objetivo patrimonio",
    },
    {
        "titulo": "Vivir con 2.000 € al mes",
        "texto": "Calcula cuánto capital necesitas para generar 2.000 € mensuales.",
        "href": "/cuanto-dinero-necesitas-para-vivir-con-2000-euros-mes",
        "tag": "FIRE",
    },
    {
        "titulo": "Dónde invertir 10.000 €",
        "texto": "Ideas y simulación para invertir 10.000 € a medio y largo plazo.",
        "href": "/donde-invertir-10000-euros",
        "tag": "Capital inicial",
    },
]

CLUSTERS_SEO = [
    {
        "titulo": "Invertir cada mes",
        "descripcion": "Escenarios de aportación mensual para ver el efecto del interés compuesto.",
        "links": [
            ("Invertir 100 € al mes", "/invertir-100-euros-mes"),
            ("Invertir 300 € al mes", "/invertir-300-euros-mes"),
            ("Invertir 500 € al mes", "/invertir-500-euros-mes"),
            ("Invertir 1.000 € al mes", "/invertir-1000-euros-mes"),
        ],
    },
    {
        "titulo": "Objetivos de patrimonio",
        "descripcion": "Guías para calcular cuánto puedes tardar en alcanzar ciertos objetivos.",
        "links": [
            ("Conseguir 100.000 €", "/como-conseguir-100000-euros"),
            ("Conseguir 200.000 €", "/como-conseguir-200000-euros"),
            ("Conseguir 500.000 €", "/como-conseguir-500000-euros"),
            ("Conseguir un millón", "/como-conseguir-un-millon-de-euros"),
        ],
    },
    {
        "titulo": "Vivir de inversiones",
        "descripcion": "Calcula cuánto capital necesitas para generar ingresos mensuales.",
        "links": [
            ("Vivir con 1.000 € al mes", "/cuanto-dinero-necesitas-para-vivir-con-1000-euros-mes"),
            ("Vivir con 1.500 € al mes", "/cuanto-dinero-necesitas-para-vivir-con-1500-euros-mes"),
            ("Vivir con 2.000 € al mes", "/cuanto-dinero-necesitas-para-vivir-con-2000-euros-mes"),
            ("Vivir de rentas en España", "/cuanto-dinero-necesitas-para-vivir-de-rentas-en-espana"),
        ],
    },
    {
        "titulo": "Comparativas de inversión",
        "descripcion": "Compara alternativas habituales antes de tomar una decisión.",
        "links": [
            ("S&P 500 o Nasdaq 100", "/invertir-en-sp500-o-nasdaq"),
            ("S&P 500 o MSCI World", "/sp500-o-msci-world"),
            ("Fondos indexados o ETFs", "/fondos-indexados-o-etfs"),
            ("Bolsa o amortizar hipoteca", "/invertir-en-bolsa-o-amortizar-hipoteca"),
        ],
    },
]

ARTICULOS_DESTACADOS = [
    {
        "titulo": "Qué es el interés compuesto",
        "texto": "Entiende cómo funciona y por qué puede marcar tanta diferencia a largo plazo.",
        "href": "/blog/interes-compuesto",
    },
    {
        "titulo": "Qué es FIRE",
        "texto": "Descubre cuánto dinero necesitas para vivir de tus inversiones.",
        "href": "/blog/fire",
    },
    {
        "titulo": "Cómo calcular una hipoteca",
        "texto": "Aprende a interpretar cuota, intereses y coste total antes de comprar vivienda.",
        "href": "/blog/hipoteca",
    },
]

LIBROS = [
    {
        "titulo": "Padre Rico, Padre Pobre",
        "texto": "Un clásico para cambiar tu forma de pensar sobre dinero, activos y libertad financiera.",
        "href": "https://amzn.to/4tzZ9aB",
        "badge": "Mentalidad",
    },
    {
        "titulo": "The Psychology of Money",
        "texto": "Muy bueno para entender que invertir bien no va solo de números, sino de comportamiento.",
        "href": "https://amzn.to/4vc02Yt",
        "badge": "Comportamiento",
    },
    {
        "titulo": "El inversor inteligente",
        "texto": "Una referencia para invertir con más criterio y visión a largo plazo.",
        "href": "https://amzn.to/4sQ3Lt1",
        "badge": "Clásico",
    },
]


# =========================================================
# HELPERS UI
# =========================================================

def hero_metric(label, value):
    return html.Div(
        [
            html.Div(label, className="hero-metric-label"),
            html.Div(value, className="hero-metric-value"),
        ],
        className="hero-metric-card",
    )


def section_header(eyebrow, title, subtitle=None):
    return html.Div(
        [
            html.Div(eyebrow, className="section-eyebrow"),
            html.H2(title, className="section-title fw-bold mb-3"),
            html.P(subtitle, className="section-subtitle mb-4") if subtitle else None,
        ]
    )


def teaser_card(titulo, texto, href, boton_texto, icono="✨"):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(icono, className="teaser-icon mb-2"),
                html.Div(titulo, className="fw-bold mb-1"),
                html.Div(texto, className="text-muted small mb-3"),
                dbc.Button(
                    boton_texto,
                    href=href,
                    color="light",
                    className="rounded-pill px-3 fw-semibold border",
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 h-100 teaser-card",
    )


def calculadora_card(titulo, descripcion, href, icono="📊", badge=None, destacada=False):
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        [
                            html.Div(icono, className="calc-card-icon"),
                            html.Div(badge, className="calc-card-badge") if badge else None,
                        ],
                        className="d-flex justify-content-between align-items-start mb-3",
                    ),
                    html.H3(titulo, className="h5 fw-bold mb-2"),
                    html.P(
                        descripcion,
                        className="text-muted small mb-4",
                        style={"minHeight": "72px"},
                    ),
                    dbc.Button(
                        "Usar calculadora",
                        href=href,
                        color="primary" if destacada else "light",
                        className="w-100 rounded-pill fw-semibold calc-card-btn",
                    ),
                ]
            ),
            class_name=f"calc-card border-0 rounded-4 h-100 {'calc-card-featured' if destacada else ''}",
        ),
        xl=4,
        md=6,
        className="mb-4",
    )


def quick_action_card(title, text, href, button_text):
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(title, className="fw-bold mb-2"),
                    html.P(text, className="text-muted small mb-3"),
                    dbc.Button(
                        button_text,
                        href=href,
                        color="light",
                        className="rounded-pill border fw-semibold px-3",
                    ),
                ]
            ),
            className="border-0 shadow-sm rounded-4 h-100 quick-card",
        ),
        md=4,
        className="mb-3",
    )


def guide_card(titulo, texto, href, tag):
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(tag, className="book-badge mb-2"),
                    html.H3(titulo, className="h5 fw-bold mb-2"),
                    html.P(texto, className="text-muted small mb-3"),
                    dbc.Button(
                        "Leer guía",
                        href=href,
                        color="light",
                        className="rounded-pill border fw-semibold px-3",
                    ),
                ]
            ),
            className="border-0 shadow-sm rounded-4 h-100",
        ),
        lg=3,
        md=6,
        className="mb-4",
    )


def cluster_card(cluster):
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3(cluster["titulo"], className="h5 fw-bold mb-2"),
                    html.P(cluster["descripcion"], className="text-muted small mb-3"),
                    html.Ul(
                        [
                            html.Li(
                                dcc.Link(text, href=href, className="text-decoration-none fw-semibold")
                            )
                            for text, href in cluster["links"]
                        ],
                        className="mb-0 ps-3",
                    ),
                ]
            ),
            className="border-0 shadow-sm rounded-4 h-100",
        ),
        lg=3,
        md=6,
        className="mb-4",
    )


def articulo_card(titulo, texto, href):
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3(titulo, className="h5 fw-bold mb-2"),
                    html.P(texto, className="text-muted small mb-3"),
                    dbc.Button(
                        "Leer artículo",
                        href=href,
                        color="light",
                        className="rounded-pill border fw-semibold px-3",
                    ),
                ]
            ),
            className="border-0 shadow-sm rounded-4 h-100",
        ),
        md=4,
        className="mb-3",
    )


def book_card(titulo, texto, href, badge=None):
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(badge, className="book-badge mb-2") if badge else None,
                    html.H3(titulo, className="h5 fw-bold mb-2"),
                    html.P(texto, className="text-muted small mb-3"),
                    dbc.Button(
                        "Ver recomendación",
                        href=href,
                        target="_blank",
                        rel="sponsored noopener noreferrer",
                        color="light",
                        className="rounded-pill border fw-semibold px-3",
                    ),
                ]
            ),
            className="border-0 shadow-sm rounded-4 h-100",
        ),
        lg=4,
        md=6,
        className="mb-4",
    )


# =========================================================
# SECTIONS
# =========================================================

hero_section = html.Div(
    dbc.Container(
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            "CALCULADORAS FINANCIERAS · INVERSIÓN · FIRE · VIVIENDA",
                            className="hero-badge mb-3",
                        ),
                        html.H1(
                            "Calculadoras financieras para invertir mejor, comprar vivienda y alcanzar libertad financiera",
                            className="hero-title fw-bold mb-3",
                        ),
                        html.P(
                            "Simula interés compuesto, calcula tu número FIRE, estima tu hipoteca y analiza la rentabilidad de un alquiler con herramientas claras, prácticas y gratuitas.",
                            className="hero-subtitle mb-4",
                        ),
                        html.Div(
                            [
                                dbc.Button(
                                    "Empezar con interés compuesto",
                                    href="/calculadora",
                                    color="primary",
                                    className="rounded-pill px-4 py-2 fw-semibold me-2 mb-2",
                                ),
                                dbc.Button(
                                    "Calcular libertad financiera",
                                    href="/fire",
                                    color="light",
                                    className="rounded-pill px-4 py-2 fw-semibold border mb-2",
                                ),
                            ],
                            className="mb-2",
                        ),
                        html.Div(
                            [
                                hero_metric("Herramientas", "5 calculadoras"),
                                hero_metric("Guías", "40+ escenarios"),
                                hero_metric("Precio", "Gratis"),
                            ],
                            className="hero-metrics",
                        ),
                    ],
                    lg=7,
                    className="mb-4 mb-lg-0",
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div("Empieza por aquí", className="text-primary fw-bold small mb-2"),
                                html.H2("Tu hoja de ruta financiera", className="h4 fw-bold mb-3"),
                                html.P(
                                    "Elige según tu objetivo: invertir, vivir de rentas, comprar vivienda o comparar alternativas.",
                                    className="text-muted small mb-4",
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            teaser_card(
                                                "Quiero invertir",
                                                "Simula cuánto puede crecer tu dinero con aportaciones mensuales.",
                                                "/calculadora",
                                                "Abrir calculadora",
                                                "📈",
                                            ),
                                            md=12,
                                            className="mb-3",
                                        ),
                                        dbc.Col(
                                            teaser_card(
                                                "Quiero vivir de rentas",
                                                "Calcula cuánto patrimonio necesitas para generar ingresos.",
                                                "/cuanto-dinero-necesitas-para-vivir-con-2000-euros-mes",
                                                "Ver guía",
                                                "🔥",
                                            ),
                                            md=12,
                                            className="mb-3",
                                        ),
                                        dbc.Col(
                                            teaser_card(
                                                "Quiero comprar vivienda",
                                                "Estima cuota, intereses y esfuerzo financiero.",
                                                "/hipoteca",
                                                "Calcular hipoteca",
                                                "🏠",
                                            ),
                                            md=12,
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        className="border-0 shadow-sm rounded-4 h-100 hero-side-card",
                    ),
                    lg=5,
                ),
            ],
            className="align-items-center",
        )
    ),
    className="home-hero",
)

calculadoras_section = html.Div(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        section_header(
                            "Calculadoras principales",
                            "Herramientas para tomar mejores decisiones con tu dinero",
                            "Empieza por una calculadora y después profundiza con las guías relacionadas.",
                        ),
                        lg=8,
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.Div(
                                    "Más simulación, más claridad y mejores decisiones.",
                                    className="small text-muted mb-2",
                                ),
                                html.Div("Acceso directo a 5 herramientas", className="fw-bold"),
                            ],
                            className="calc-highlight-box mt-4 mt-lg-0",
                        ),
                        lg=4,
                    ),
                ],
                className="align-items-end mb-4",
            ),
            dbc.Row(
                [
                    calculadora_card(
                        c["titulo"],
                        c["descripcion"],
                        c["href"],
                        c["icono"],
                        c["badge"],
                        c["destacada"],
                    )
                    for c in CALCULADORAS
                ]
            ),
        ],
        id="todas-las-calculadoras",
    ),
    className="calculadoras-section",
)

guias_populares_section = html.Div(
    dbc.Container(
        [
            section_header(
                "Guías populares",
                "Escenarios que la gente busca antes de invertir",
                "Estas páginas ayudan a Google a entender mejor la estructura de la web y llevan tráfico hacia las calculadoras.",
            ),
            dbc.Row(
                [
                    guide_card(g["titulo"], g["texto"], g["href"], g["tag"])
                    for g in GUIAS_POPULARES
                ]
            ),
        ]
    ),
    className="articulos-section py-5",
)

clusters_section = html.Div(
    dbc.Container(
        [
            section_header(
                "Explora por objetivo",
                "Guías organizadas para invertir, ahorrar, vivir de rentas y comparar opciones",
                "Un hub de contenidos para navegar por las principales decisiones financieras personales.",
            ),
            dbc.Row([cluster_card(cluster) for cluster in CLUSTERS_SEO]),
        ]
    ),
    className="quick-actions-section py-5",
)

quick_actions_section = html.Div(
    dbc.Container(
        [
            section_header(
                "Empieza según tu objetivo",
                "No todo el mundo busca lo mismo",
                "Elige la ruta que más encaja con la decisión que quieres tomar ahora.",
            ),
            dbc.Row(
                [
                    quick_action_card(
                        "Quiero invertir mejor",
                        "Empieza por interés compuesto y después revisa guías de aportaciones mensuales.",
                        "/invertir-500-euros-mes",
                        "Ver inversión",
                    ),
                    quick_action_card(
                        "Quiero comprar vivienda",
                        "Usa la calculadora de hipoteca para estimar cuota, intereses y coste total.",
                        "/hipoteca",
                        "Ver hipoteca",
                    ),
                    quick_action_card(
                        "Quiero vivir de rentas",
                        "Comprueba cuánto patrimonio necesitas para generar ingresos mensuales.",
                        "/fire",
                        "Calcular FIRE",
                    ),
                ]
            ),
        ]
    ),
    className="quick-actions-section",
)

premium_section = html.Div(
    dbc.Container(
        dbc.Card(
            dbc.CardBody(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div("Premium", className="section-eyebrow mb-3"),
                                html.Div("Pago único · 9€", className="premium-price-badge mb-3"),
                                html.H2(
                                    "Desbloquea todas las calculadoras premium",
                                    className="premium-title mb-3",
                                ),
                                html.P(
                                    "Accede a funciones avanzadas como Monte Carlo, comparativas, exportación y futuras mejoras premium.",
                                    className="section-subtitle mb-4",
                                ),
                                html.Div(
                                    [
                                        html.Div("✔ Monte Carlo", className="premium-feature-chip"),
                                        html.Div("✔ Guardar simulaciones", className="premium-feature-chip"),
                                        html.Div("✔ Exportar resultados", className="premium-feature-chip"),
                                        html.Div("✔ Comparativas avanzadas", className="premium-feature-chip"),
                                    ],
                                    className="premium-feature-grid mb-4",
                                ),
                                html.Div("Sin suscripción. Pago único.", className="premium-mini-note mb-4"),
                            ],
                            lg=8,
                            className="mb-4 mb-lg-0",
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    dbc.Button(
                                        "Desbloquear todo por 9€",
                                        href=STRIPE_PAYMENT_LINK,
                                        target="_blank",
                                        color="dark",
                                        className="premium-cta-btn w-100 mb-3",
                                    ),
                                    dbc.Button(
                                        "Probar calculadora",
                                        href="/calculadora",
                                        color="light",
                                        className="rounded-pill fw-semibold border w-100",
                                    ),
                                ],
                                className="d-flex flex-column justify-content-center h-100",
                            ),
                            lg=4,
                        ),
                    ],
                    className="align-items-center",
                )
            ),
            className="border-0 premium-panel",
        )
    ),
    className="premium-section",
)

seo_text_section = html.Div(
    dbc.Container(
        [
            section_header(
                "Centro de simulación financiera",
                "Calculadoras para inversión, vivienda, FIRE y rentabilidad",
            ),
            html.P(
                [
                    "interescompuesto.app reúne herramientas financieras en español para ayudarte a tomar decisiones con más contexto. "
                    "Puedes usar la ",
                    dcc.Link("calculadora de interés compuesto", href="/calculadora"),
                    " para estimar cuánto podría crecer tu dinero, la ",
                    dcc.Link("calculadora FIRE", href="/fire"),
                    " para proyectar independencia financiera, la ",
                    dcc.Link("calculadora de hipoteca", href="/hipoteca"),
                    " para analizar una compra de vivienda y la ",
                    dcc.Link("calculadora de rentabilidad de alquiler", href="/rentabilidad-alquiler"),
                    " para estudiar operaciones inmobiliarias.",
                ],
                className="section-subtitle mb-3",
            ),
            html.P(
                "La idea no es complicarlo, sino ayudarte a simular escenarios reales, comparar alternativas y evitar decisiones impulsivas.",
                className="section-subtitle mb-0",
            ),
        ]
    ),
    className="seo-text-section py-5",
)

articulos_section = html.Div(
    dbc.Container(
        [
            section_header(
                "Aprende antes de decidir",
                "Guías y artículos para entender mejor tus números",
                "Contenido base para complementar las calculadoras y reforzar el enlazado interno.",
            ),
            dbc.Row([articulo_card(a["titulo"], a["texto"], a["href"]) for a in ARTICULOS_DESTACADOS]),
        ]
    ),
    className="articulos-section",
)

affiliate_cta_section = html.Div(
    dbc.Container(
        dbc.Card(
            dbc.CardBody(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div("Dar el siguiente paso", className="section-eyebrow mb-3"),
                                html.H2("Cuando quieras pasar de simular a actuar", className="fw-bold mb-2"),
                                html.P(
                                    "Después de hacer tus números, el siguiente paso suele ser elegir una plataforma sencilla para empezar a invertir con aportaciones periódicas.",
                                    className="text-muted mb-0",
                                ),
                            ],
                            lg=8,
                            className="mb-3 mb-lg-0",
                        ),
                        dbc.Col(
                            html.Div(
                                dbc.Button(
                                    "Ver opción para empezar",
                                    href=MYINVESTOR_AFFILIATE_URL,
                                    target="_blank",
                                    rel="sponsored noopener noreferrer",
                                    color="success",
                                    className="rounded-pill px-4 py-2 fw-semibold w-100",
                                ),
                                className="d-flex align-items-center h-100",
                            ),
                            lg=4,
                        ),
                    ]
                )
            ),
            className="border-0 shadow-sm rounded-4",
        )
    ),
    className="affiliate-cta-section py-4",
)

faq_section = html.Div(
    dbc.Container(
        [
            section_header(
                "Preguntas frecuentes",
                "Dudas habituales antes de usar las calculadoras",
            ),
            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        html.P(
                            "Sí. Puedes usar gratis las calculadoras de interés compuesto, FIRE, hipoteca, rentabilidad de alquiler y comparador de inversión.",
                            className="mb-0",
                        ),
                        title="¿Las calculadoras son gratis?",
                    ),
                    dbc.AccordionItem(
                        html.P(
                            "Son simulaciones orientativas. Te ayudan a tomar mejores decisiones, pero no sustituyen asesoramiento financiero personalizado.",
                            className="mb-0",
                        ),
                        title="¿Los resultados son exactos?",
                    ),
                    dbc.AccordionItem(
                        html.P(
                            "Depende de tu objetivo. Para inversión a largo plazo, empieza por interés compuesto. Para libertad financiera, usa FIRE. Para vivienda, empieza por hipoteca.",
                            className="mb-0",
                        ),
                        title="¿Por qué calculadora debería empezar?",
                    ),
                    dbc.AccordionItem(
                        html.P(
                            "Sí. Muchas guías incluyen enlaces a calculadoras para que puedas adaptar los números a tu caso concreto.",
                            className="mb-0",
                        ),
                        title="¿Puedo simular mi propio caso?",
                    ),
                ],
                start_collapsed=True,
                always_open=False,
            ),
        ]
    ),
    className="faq-section py-5",
)

books_section = html.Div(
    dbc.Container(
        [
            section_header(
                "Libros recomendados",
                "Aprende a invertir mejor",
                "Una selección sencilla para mejorar mentalidad financiera, criterio de inversión y visión a largo plazo.",
            ),
            dbc.Row(
                [
                    book_card(libro["titulo"], libro["texto"], libro["href"], libro["badge"])
                    for libro in LIBROS
                ]
            ),
        ]
    ),
    className="books-section",
)

cta_section = html.Div(
    dbc.Container(
        dbc.Card(
            dbc.CardBody(
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div("Acceso rápido", className="section-eyebrow mb-3"),
                                html.H2("Haz tu primera simulación en menos de un minuto", className="fw-bold mb-2"),
                                html.P(
                                    "Empieza por la calculadora que más impacto tenga en tu decisión actual.",
                                    className="text-muted mb-0",
                                ),
                            ],
                            lg=8,
                            className="mb-3 mb-lg-0",
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    dbc.Button(
                                        "Ir a interés compuesto",
                                        href="/calculadora",
                                        color="primary",
                                        className="rounded-pill px-4 py-2 fw-semibold me-2 mb-2",
                                    ),
                                    dbc.Button(
                                        "Ver guías populares",
                                        href="#guias-populares",
                                        color="light",
                                        className="rounded-pill px-4 py-2 fw-semibold border mb-2",
                                    ),
                                ],
                                className="text-lg-end",
                            ),
                            lg=4,
                            className="d-flex align-items-center justify-content-lg-end",
                        ),
                    ]
                )
            ),
            className="border-0 shadow-sm rounded-4 cta-panel",
        )
    ),
    className="cta-section",
)


# =========================================================
# LAYOUT
# =========================================================

layout = html.Div(
    [
        hero_section,
        calculadoras_section,
        html.Div(guias_populares_section, id="guias-populares"),
        clusters_section,
        quick_actions_section,
        premium_section,
        seo_text_section,
        articulos_section,
        affiliate_cta_section,
        faq_section,
        cta_section,
        books_section,
        build_disclaimer(title="Empieza a dar el siguiente paso"),
    ]
)
