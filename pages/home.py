import dash
from dash import html
import dash_bootstrap_components as dbc

from components.disclaimer_afiliados import build_disclaimer


dash.register_page(
    __name__,
    path="/",
    title="Calculadoras financieras: interés compuesto, FIRE, hipoteca y rentabilidad | interescompuesto.app",
    name="Inicio",
    description=(
        "Calculadoras financieras en español para inversión, FIRE, hipoteca, "
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
                                "FINANZAS PERSONALES · INVERSIÓN · HIPOTECA",
                                className="hero-badge mb-3",
                            ),
                            html.H1(
                                "Calculadoras financieras claras, útiles y pensadas para tomar mejores decisiones",
                                className="hero-title fw-bold mb-3",
                            ),
                            html.P(
                                "Simula tu interés compuesto, calcula tu objetivo FIRE, estima tu hipoteca, "
                                "analiza alquileres y compara alternativas de inversión. Todo en español, "
                                "sin ruido y con enfoque práctico.",
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
                                        "Explora las áreas clave de la web: inversión, independencia financiera, "
                                        "compra de vivienda y análisis inmobiliario.",
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
                                "Desde inversión a vivienda, pasando por FIRE, rentabilidad inmobiliaria y comparativas. "
                                "La home debe funcionar como un hub real de herramientas.",
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

premium_section = html.Div(
    dbc.Container(
        [
            dbc.Card(
                dbc.CardBody(
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Div("Versión premium", className="section-eyebrow mb-3"),
                                    html.H2(
                                        "Una plataforma más avanzada está en camino",
                                        className="fw-bold mb-3 premium-title",
                                    ),
                                    html.P(
                                        "Estoy preparando una versión premium con funciones avanzadas para quienes "
                                        "quieran ir más allá de las simulaciones básicas.",
                                        className="text-muted mb-3",
                                    ),
                                    html.Ul(
                                        [
                                            html.Li("Guardar simulaciones y escenarios"),
                                            html.Li("Comparativas avanzadas"),
                                            html.Li("Herramientas pro de inversión y vivienda"),
                                            html.Li("Exportaciones y funcionalidades extra"),
                                        ],
                                        className="premium-list text-muted mb-0",
                                    ),
                                ],
                                lg=8,
                                className="mb-4 mb-lg-0",
                            ),
                            dbc.Col(
                                html.Div(
                                    [
                                        html.Div("Próximamente", className="calc-card-badge mb-3"),
                                        dbc.Button(
                                            "Ver versión premium",
                                            href="/premium",
                                            color="primary",
                                            className="rounded-pill px-4 py-2 fw-semibold w-100 mb-2",
                                        ),
                                        html.Div(
                                            "Muy pronto podrás acceder a herramientas avanzadas de pago.",
                                            className="small text-muted",
                                        ),
                                    ],
                                    className="calc-highlight-box h-100 d-flex flex-column justify-content-center",
                                ),
                                lg=4,
                            ),
                        ]
                    )
                ),
                className="border-0 shadow-sm rounded-4 premium-panel",
            )
        ]
    ),
    className="premium-section",
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
        premium_section,
        cta_section,
        books_section_v3(),
        build_disclaimer(title="Empieza a dar el siguiente paso"),
    ]
)
