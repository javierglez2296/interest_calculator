import dash
from dash import html
import dash_bootstrap_components as dbc

from components.disclaimer_afiliados import build_disclaimer

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/",
    title="Calculadoras financieras de interés compuesto, FIRE, hipoteca y rentabilidad | interescompuesto.app",
    name="Inicio",
    description=(
        "Calculadoras financieras en español para interés compuesto, FIRE, hipoteca, "
        "rentabilidad de alquiler y comparativas. Gratis, claras y prácticas."
    ),
)

# =========================================================
# DATA
# =========================================================
CALCULADORAS = [
    {
        "titulo": "Interés compuesto",
        "descripcion": "Descubre cuánto puede crecer tu dinero con aportaciones periódicas y visión a largo plazo.",
        "href": "/calculadora",
        "icono": "📈",
        "badge": "Más usada",
        "destacada": True,
    },
    {
        "titulo": "FIRE",
        "descripcion": "Calcula cuánto necesitas para vivir de tus inversiones y cuánto podrías tardar en conseguirlo.",
        "href": "/fire",
        "icono": "🔥",
        "badge": "Libertad financiera",
        "destacada": False,
    },
    {
        "titulo": "Hipoteca",
        "descripcion": "Simula cuota, intereses, coste total y esfuerzo financiero antes de comprar vivienda.",
        "href": "/hipoteca",
        "icono": "🏠",
        "badge": "Vivienda",
        "destacada": False,
    },
    {
        "titulo": "Rentabilidad alquiler",
        "descripcion": "Analiza cashflow, rentabilidad neta y el impacto de financiar una inversión inmobiliaria.",
        "href": "/rentabilidad-alquiler",
        "icono": "💸",
        "badge": "Inmobiliario",
        "destacada": False,
    },
    {
        "titulo": "Comparador de inversión",
        "descripcion": "Compara vivienda, bolsa y otras alternativas para ver qué opción encaja mejor contigo.",
        "href": "/comparador",
        "icono": "⚖️",
        "badge": "Comparativa",
        "destacada": False,
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
        "texto": "Más exigente, pero una referencia atemporal para invertir con criterio.",
        "href": "https://amzn.to/4sQ3Lt1",
        "badge": "Clásico",
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
        "texto": "Descubre cuánto dinero necesitas para vivir de tus inversiones y cómo se calcula.",
        "href": "/blog/fire",
    },
    {
        "titulo": "Cómo calcular una hipoteca",
        "texto": "Aprende a interpretar cuota, intereses y coste total antes de comprar vivienda.",
        "href": "/blog/hipoteca",
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
                        style={"minHeight": "68px"},
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


def calculadoras_grid():
    return dbc.Row(
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


def books_section_v3():
    return html.Div(
        dbc.Container(
            [
                html.Div("Libros recomendados", className="section-eyebrow"),
                html.H2(
                    "Aprende a invertir mejor",
                    className="section-title fw-bold mb-3",
                ),
                html.P(
                    "Una selección sencilla para mejorar mentalidad financiera, criterio de inversión y visión a largo plazo.",
                    className="section-subtitle mb-4",
                ),
                dbc.Row(
                    [
                        book_card(
                            libro["titulo"],
                            libro["texto"],
                            libro["href"],
                            libro["badge"],
                        )
                        for libro in LIBROS
                    ]
                ),
            ]
        ),
        className="books-section",
    )


# =========================================================
# SECTIONS
# =========================================================
hero_section = html.Div(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                "FINANZAS PERSONALES · INVERSIÓN · FIRE · HIPOTECA",
                                className="hero-badge mb-3",
                            ),
                            html.H1(
                                "Calculadoras financieras para interés compuesto, FIRE, hipoteca y rentabilidad",
                                className="hero-title fw-bold mb-3",
                            ),
                            html.P(
                                "Simula tu inversión, calcula tu libertad financiera, estima tu hipoteca y analiza la rentabilidad de alquiler con herramientas claras, prácticas y gratis.",
                                className="hero-subtitle mb-4",
                            ),
                            html.Div(
                                [
                                    dbc.Button(
                                        "Probar interés compuesto",
                                        href="/calculadora",
                                        color="primary",
                                        className="rounded-pill px-4 py-2 fw-semibold me-2 mb-2",
                                    ),
                                    dbc.Button(
                                        "Ver hipoteca",
                                        href="/hipoteca",
                                        color="light",
                                        className="rounded-pill px-4 py-2 fw-semibold border mb-2",
                                    ),
                                ],
                                className="mb-2",
                            ),
                            html.Div(
                                [
                                    hero_metric("Herramientas", "5 calculadoras"),
                                    hero_metric("Uso", "Gratis"),
                                    hero_metric("Enfoque", "100% práctico"),
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
                                    html.Div(
                                        "Empieza por aquí",
                                        className="text-primary fw-bold small mb-2",
                                    ),
                                    html.H2(
                                        "Tu hoja de ruta financiera",
                                        className="h4 fw-bold mb-3",
                                    ),
                                    html.P(
                                        "Explora las áreas clave de la web: inversión, independencia financiera, compra de vivienda y análisis inmobiliario.",
                                        className="text-muted small mb-4",
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                teaser_card(
                                                    "Interés compuesto",
                                                    "Descubre cuánto puede crecer tu dinero con aportaciones periódicas.",
                                                    "/calculadora",
                                                    "Abrir calculadora",
                                                    "📈",
                                                ),
                                                md=12,
                                                className="mb-3",
                                            ),
                                            dbc.Col(
                                                teaser_card(
                                                    "FIRE",
                                                    "Calcula cuánto necesitas para vivir de tus inversiones.",
                                                    "/fire",
                                                    "Ver FIRE",
                                                    "🔥",
                                                ),
                                                md=12,
                                                className="mb-3",
                                            ),
                                            dbc.Col(
                                                teaser_card(
                                                    "Hipoteca",
                                                    "Estima cuota, coste total y esfuerzo financiero antes de comprar.",
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
        ]
    ),
    className="home-hero",
)

calculadoras_section = html.Div(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div("Todas tus herramientas", className="section-eyebrow"),
                            html.H2(
                                "Todo lo que necesitas para simular tus decisiones financieras",
                                className="section-title fw-bold mb-3",
                            ),
                            html.P(
                                "Desde inversión a vivienda, pasando por FIRE, rentabilidad inmobiliaria y comparativas. La home debe funcionar como un hub real de herramientas.",
                                className="section-subtitle mb-0",
                            ),
                        ],
                        lg=8,
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.Div(
                                    "Más clics internos, más tiempo en página y más opciones de monetización.",
                                    className="small text-muted mb-2",
                                ),
                                html.Div(
                                    "Acceso directo a 5 calculadoras",
                                    className="fw-bold",
                                    style={"color": "#101828"},
                                ),
                            ],
                            className="calc-highlight-box mt-4 mt-lg-0",
                        ),
                        lg=4,
                    ),
                ],
                className="align-items-end mb-4",
            ),
            calculadoras_grid(),
        ],
        id="todas-las-calculadoras",
    ),
    className="calculadoras-section",
)

quick_actions_section = html.Div(
    dbc.Container(
        [
            html.Div("Empieza según tu objetivo", className="section-eyebrow"),
            html.H2(
                "No todo el mundo busca lo mismo",
                className="section-title fw-bold mb-3",
            ),
            html.P(
                "Te dejo accesos rápidos según el tipo de decisión que quieras tomar ahora.",
                className="section-subtitle mb-4",
            ),
            dbc.Row(
                [
                    quick_action_card(
                        "Quiero invertir mejor",
                        "Empieza por interés compuesto si quieres ver cuánto puede crecer tu dinero.",
                        "/calculadora",
                        "Ver inversión",
                    ),
                    quick_action_card(
                        "Quiero comprar vivienda",
                        "Usa la calculadora de hipoteca para ver cuota, intereses y coste total.",
                        "/hipoteca",
                        "Ver hipoteca",
                    ),
                    quick_action_card(
                        "Quiero comparar opciones",
                        "Comprueba si te encaja más invertir en bolsa, vivienda u otra alternativa.",
                        "/comparador",
                        "Comparar opciones",
                    ),
                ]
            ),
        ]
    ),
    className="quick-actions-section",
)

seo_text_section = html.Div(
    dbc.Container(
        [
            html.Div("Tu centro de simulación financiera", className="section-eyebrow"),
            html.H2(
                "Una web para calcular decisiones de inversión, vivienda y libertad financiera",
                className="section-title fw-bold mb-3",
            ),
            html.P(
                "interescompuesto.app reúne calculadoras financieras en español para ayudarte a tomar decisiones con más contexto. Puedes usar la calculadora de interés compuesto para estimar cuánto podría crecer tu dinero con aportaciones periódicas, la calculadora FIRE para proyectar cuándo podrías alcanzar la independencia financiera, la calculadora de hipoteca para entender cuota, intereses y coste total, y la calculadora de rentabilidad de alquiler para analizar cashflow y retorno inmobiliario.",
                className="section-subtitle mb-3",
            ),
            html.P(
                "La idea no es complicarlo, sino darte herramientas prácticas para simular escenarios reales y comparar alternativas. Tanto si quieres empezar a invertir como si estás valorando comprar vivienda o construir ingresos pasivos, aquí puedes hacerlo de forma clara, visual y gratuita.",
                className="section-subtitle mb-0",
            ),
        ]
    ),
    className="seo-text-section py-5",
)

articulos_section = html.Div(
    dbc.Container(
        [
            html.Div("Aprende antes de decidir", className="section-eyebrow"),
            html.H2(
                "Guías y artículos para entender mejor tus números",
                className="section-title fw-bold mb-3",
            ),
            html.P(
                "Además de las calculadoras, tienes contenido para profundizar en inversión, FIRE e hipoteca.",
                className="section-subtitle mb-4",
            ),
            dbc.Row(
                [articulo_card(a["titulo"], a["texto"], a["href"]) for a in ARTICULOS_DESTACADOS]
            ),
        ]
    ),
    className="articulos-section",
)

simulaciones_section = html.Div(
    dbc.Container(
        [
            html.Div("Ideas para empezar", className="section-eyebrow"),
            html.H2(
                "Simulaciones que suelen interesar más",
                className="section-title fw-bold mb-3",
            ),
            html.P(
                "Empieza por uno de estos escenarios típicos y luego ajusta tus números.",
                className="section-subtitle mb-4",
            ),
            dbc.Row(
                [
                    quick_action_card(
                        "Invertir 300 € al mes",
                        "Hazte una idea de cuánto podrías acumular a largo plazo con aportaciones periódicas.",
                        "/calculadora",
                        "Simular ahora",
                    ),
                    quick_action_card(
                        "Calcular independencia financiera",
                        "Comprueba cuánto patrimonio necesitarías para vivir de tus inversiones.",
                        "/fire",
                        "Ver FIRE",
                    ),
                    quick_action_card(
                        "Estimar una hipoteca",
                        "Visualiza cuota, intereses y coste total antes de decidir si comprar vivienda.",
                        "/hipoteca",
                        "Ver hipoteca",
                    ),
                ]
            ),
        ]
    ),
    className="simulaciones-section",
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
                                html.H2(
                                    "Cuando quieras pasar de simular a actuar",
                                    className="fw-bold mb-2",
                                ),
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
            html.Div("Preguntas frecuentes", className="section-eyebrow"),
            html.H2(
                "Dudas habituales antes de usar las calculadoras",
                className="section-title fw-bold mb-4",
            ),
            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            html.P(
                                "Sí. Puedes usar gratis las calculadoras de interés compuesto, FIRE, hipoteca, rentabilidad de alquiler y comparador de inversión.",
                                className="mb-0",
                            )
                        ],
                        title="¿Las calculadoras son gratis?",
                    ),
                    dbc.AccordionItem(
                        [
                            html.P(
                                "Son simulaciones orientativas. Te ayudan a tomar mejores decisiones, pero no sustituyen asesoramiento financiero personalizado.",
                                className="mb-0",
                            )
                        ],
                        title="¿Los resultados son exactos?",
                    ),
                    dbc.AccordionItem(
                        [
                            html.P(
                                "Depende de lo que quieras analizar. Si buscas inversión a largo plazo, empieza por interés compuesto. Si quieres libertad financiera, usa FIRE. Si vas a comprar vivienda, empieza por hipoteca.",
                                className="mb-0",
                            )
                        ],
                        title="¿Por qué calculadora debería empezar?",
                    ),
                ],
                start_collapsed=True,
                always_open=False,
            ),
        ]
    ),
    className="faq-section py-5",
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
                                html.H2(
                                    "Haz tu primera simulación en menos de un minuto",
                                    className="fw-bold mb-2",
                                ),
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
                                        "Ver todas las calculadoras",
                                        href="#todas-las-calculadoras",
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

layout = html.Div(
    [
        hero_section,
        calculadoras_section,
        quick_actions_section,
        seo_text_section,
        articulos_section,
        simulaciones_section,
        affiliate_cta_section,
        faq_section,
        cta_section,
        books_section_v3(),
        build_disclaimer(title="Empieza a dar el siguiente paso"),
    ]
)
