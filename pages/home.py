import dash
from dash import html, Output, Input, clientside_callback
import dash_bootstrap_components as dbc
from components.disclaimer_afiliados import build_disclaimer

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/",
    title="Calculadora de interés compuesto, FIRE y hipoteca | interescompuesto.app",
    name="Inicio",
    description=(
        "Descubre cuánto dinero puedes tener en el futuro. Calcula interés compuesto, "
        "FIRE e hipoteca de forma rápida, clara y gratuita."
    ),
)

# =========================================================
# HELPERS
# =========================================================

def section_badge(texto, color_class="text-primary"):
    return html.Div(
        texto,
        className=f"small fw-bold {color_class} mb-2",
        style={"letterSpacing": "0.04em"},
    )


def teaser_card(titulo, texto, href, boton_texto="Abrir", badge=None, icono=None, featured=False):
    header_items = [html.Span(icono or "✨", className="card-icon me-2")]
    if badge:
        header_items.append(html.Span(badge, className="mini-badge"))

    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(header_items, className="d-flex align-items-center mb-3"),
                html.H3(titulo, className="h5 fw-bold mb-2 text-dark"),
                html.P(texto, className="text-muted small mb-4"),
                dbc.Button(
                    boton_texto,
                    href=href,
                    color="primary" if featured else "light",
                    className=(
                        "w-100 rounded-pill fw-semibold border-0"
                        if featured else
                        "w-100 rounded-pill fw-semibold border"
                    ),
                ),
            ]
        ),
        className=(
            "h-100 shadow-sm border-0 rounded-4 teaser-card "
            + ("teaser-card-featured" if featured else "")
        ),
    )


def benefit_card(icono, titulo, texto):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(icono, className="benefit-icon mb-3"),
                html.H3(titulo, className="h5 fw-bold mb-2"),
                html.P(texto, className="text-muted small mb-0"),
            ]
        ),
        className="h-100 border-0 shadow-sm rounded-4 benefit-card",
    )


def compare_card(icono, titulo, descripcion, bullets, href, boton, featured=False):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(icono, className="compare-icon mb-3"),
                html.H3(titulo, className="h5 fw-bold mb-3"),
                html.P(descripcion, className="text-muted small mb-3"),
                html.Ul([html.Li(item) for item in bullets], className="compare-list mb-4"),
                dbc.Button(
                    boton,
                    href=href,
                    color="primary" if featured else "light",
                    outline=not featured,
                    className="w-100 rounded-pill fw-semibold",
                ),
            ]
        ),
        className="h-100 border-0 shadow-sm rounded-4 compare-card",
    )


def article_card(top_label, title, text, href, featured=False):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(top_label, className="article-top-label mb-2"),
                html.H3(title, className="h5 fw-bold mb-2"),
                html.P(text, className="text-muted small mb-4"),
                dbc.Button(
                    "Leer artículo",
                    href=href,
                    color="primary" if featured else "light",
                    className=(
                        "w-100 rounded-pill fw-semibold border-0"
                        if featured else
                        "w-100 rounded-pill fw-semibold border"
                    ),
                ),
            ]
        ),
        className="h-100 border-0 shadow-sm rounded-4 article-card",
    )


# =========================================================
# HERO
# =========================================================

hero = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Div("Calculadoras financieras en español", className="hero-pill"),
                    html.H1(
                        "Entiende mejor tu dinero y decide con más criterio",
                        className="display-4 fw-bold mb-3 hero-title",
                    ),
                    html.P(
                        "Simula tu inversión, tu objetivo FIRE y tu hipoteca con herramientas claras, rápidas "
                        "y pensadas para ayudarte a pasar de la teoría a la acción.",
                        className="hero-subtitle mb-4",
                    ),
                    html.Div(
                        [
                            dbc.Button(
                                "💰 Calcular mi dinero futuro",
                                href="/calculadora",
                                color="primary",
                                size="lg",
                                className="me-2 mb-2 px-4 rounded-pill fw-semibold",
                            ),
                            dbc.Button(
                                "Ver calculadoras",
                                href="#calculadoras-home",
                                color="light",
                                size="lg",
                                className="mb-2 px-4 rounded-pill fw-semibold border",
                            ),
                        ],
                        className="mb-3",
                    ),
                    html.Div(
                        [
                            html.Span("Sin registro", className="me-3"),
                            html.Span("Gratis", className="me-3"),
                            html.Span("Resultados inmediatos"),
                        ],
                        className="text-muted small mb-4",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Div(
                                    [
                                        html.Div("3", className="hero-stat-number"),
                                        html.P("calculadoras", className="hero-stat-label"),
                                    ],
                                    className="hero-stat",
                                ),
                                xs=4,
                            ),
                            dbc.Col(
                                html.Div(
                                    [
                                        html.Div("Gratis", className="hero-stat-number"),
                                        html.P("uso libre", className="hero-stat-label"),
                                    ],
                                    className="hero-stat",
                                ),
                                xs=4,
                            ),
                            dbc.Col(
                                html.Div(
                                    [
                                        html.Div("1 min", className="hero-stat-number"),
                                        html.P("para simular", className="hero-stat-label"),
                                    ],
                                    className="hero-stat",
                                ),
                                xs=4,
                            ),
                        ],
                        className="g-2",
                    ),
                ],
                lg=6,
                className="py-5",
            ),
            dbc.Col(
                [
                    dbc.Card(
                        [
                            html.Div(
                                [
                                    html.Span(className="mockup-dot"),
                                    html.Span(className="mockup-dot"),
                                    html.Span(className="mockup-dot"),
                                ],
                                className="mockup-topbar",
                            ),
                            dbc.CardBody(
                                [
                                    html.Div("Simulación orientativa", className="mockup-badge mb-3"),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                html.Div(
                                                    [
                                                        html.Div("Capital futuro", className="mockup-label"),
                                                        html.P("154.320€", className="mockup-value"),
                                                    ],
                                                    className="mockup-box",
                                                ),
                                                md=6,
                                                className="mb-3",
                                            ),
                                            dbc.Col(
                                                html.Div(
                                                    [
                                                        html.Div("Aportación mensual", className="mockup-label"),
                                                        html.P("300€/mes", className="mockup-value"),
                                                    ],
                                                    className="mockup-box",
                                                ),
                                                md=6,
                                                className="mb-3",
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        [
                                            html.Div(className="mockup-chart-line-1"),
                                            html.Div(className="mockup-chart-line-2"),
                                        ],
                                        className="mockup-chart mb-3",
                                    ),
                                    html.Div(
                                        [
                                            html.Div("Visualiza escenarios", className="fw-semibold text-dark mb-1"),
                                            html.Div(
                                                "Comprende mejor qué ocurre cuando cambias tiempo, rentabilidad o aportaciones.",
                                                className="text-muted small",
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ],
                        className="hero-mockup rounded-4 border-0",
                    )
                ],
                lg=6,
                className="d-flex align-items-center",
            ),
        ],
        className="align-items-center",
    ),
    fluid=True,
    className="px-4 px-md-5 py-5 gradient-hero home-section",
)

# =========================================================
# FRANJA DE CONFIANZA
# =========================================================

trust_strip = dbc.Container(
    dbc.Row(
        [
            dbc.Col(html.Div([html.Strong("Claro"), html.Span("explicaciones simples")], className="trust-item"), md=3, xs=6),
            dbc.Col(html.Div([html.Strong("Rápido"), html.Span("simulación inmediata")], className="trust-item"), md=3, xs=6),
            dbc.Col(html.Div([html.Strong("Útil"), html.Span("para invertir y vivienda")], className="trust-item"), md=3, xs=6),
            dbc.Col(html.Div([html.Strong("Gratis"), html.Span("sin registro")], className="trust-item"), md=3, xs=6),
        ],
        className="py-3",
    ),
    fluid=True,
    className="px-4 px-md-5 trust-strip home-section",
)

# =========================================================
# BENEFICIOS
# =========================================================

benefits = dbc.Container(
    [
        html.Div(className="separator-space"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        section_badge("POR QUÉ USARLA"),
                        html.H2(
                            "Todo lo que necesitas para tomar mejores decisiones financieras",
                            className="fw-bold mb-2 section-title",
                        ),
                        html.P(
                            "Herramientas claras, resultados rápidos y contenido útil para pasar de la teoría a la acción.",
                            className="section-subtitle mb-4",
                        ),
                    ],
                    width=12,
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    benefit_card(
                        "📈",
                        "Visualiza tu futuro",
                        "Entiende cuánto puede crecer tu patrimonio con aportaciones periódicas y tiempo.",
                    ),
                    md=4,
                    className="mb-4",
                ),
                dbc.Col(
                    benefit_card(
                        "🔥",
                        "Planifica tu FIRE",
                        "Calcula cuánto necesitas para acercarte a la libertad financiera y qué ritmo necesitas.",
                    ),
                    md=4,
                    className="mb-4",
                ),
                dbc.Col(
                    benefit_card(
                        "🏠",
                        "Decide mejor tu hipoteca",
                        "Evita errores y comprende mejor el coste real de comprar vivienda.",
                    ),
                    md=4,
                    className="mb-4",
                ),
            ]
        ),
    ],
    fluid=True,
    className="px-4 px-md-5 py-4 home-section",
)

# =========================================================
# BLOQUE PRINCIPAL DE DECISIÓN
# =========================================================

decision_block = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        section_badge("EMPIEZA POR AQUÍ", "text-success"),
                        html.H2(
                            "Si estás empezando, la calculadora de interés compuesto es el mejor primer paso",
                            className="fw-bold mb-3 section-title",
                        ),
                        html.P(
                            "Es la forma más rápida de ver qué pasa si inviertes con constancia durante años.",
                            className="lead text-muted mb-2",
                        ),
                        html.P(
                            "Después podrás profundizar en FIRE o en la parte de hipoteca según tu situación.",
                            className="text-muted mb-4",
                        ),
                        html.Ul(
                            [
                                html.Li("Ideal para entender el efecto del tiempo."),
                                html.Li("Útil para comparar escenarios en menos de un minuto."),
                                html.Li("La mejor puerta de entrada si aún no inviertes o quieres invertir mejor."),
                            ],
                            className="text-muted ps-3 mb-4",
                        ),
                    ],
                    md=8,
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            "Ir a interés compuesto",
                            href="/calculadora",
                            color="primary",
                            size="lg",
                            className="w-100 rounded-pill fw-semibold mb-2",
                        ),
                        dbc.Button(
                            "Ver FIRE",
                            href="/fire",
                            color="light",
                            size="lg",
                            className="w-100 rounded-pill fw-semibold border mb-2",
                        ),
                        dbc.Button(
                            "Ver hipoteca",
                            href="/hipoteca",
                            color="light",
                            size="lg",
                            className="w-100 rounded-pill fw-semibold border",
                        ),
                    ],
                    md=4,
                    className="d-flex flex-column justify-content-center",
                ),
            ],
            className="align-items-center emotional-box rounded-4 p-4 p-md-5 shadow-sm",
        )
    ],
    fluid=True,
    className="px-4 px-md-5 my-5 home-section",
)

# =========================================================
# COMPARATIVA
# =========================================================

comparativa = dbc.Container(
    [
        section_badge("ELIGE TU HERRAMIENTA"),
        html.H2("¿Qué calculadora necesitas ahora?", className="fw-bold mb-2 section-title"),
        html.P(
            "Cada herramienta responde a una pregunta distinta. Elige según tu objetivo actual.",
            className="section-subtitle mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    compare_card(
                        "💰",
                        "Interés compuesto",
                        "Para estimar cuánto puede crecer tu dinero con el tiempo.",
                        [
                            "Ideal si estás empezando a invertir",
                            "Útil para comparar escenarios",
                            "Muy visual y rápida de usar",
                        ],
                        "/calculadora",
                        "Ir a la calculadora",
                        featured=True,
                    ),
                    md=4,
                    className="mb-4",
                ),
                dbc.Col(
                    compare_card(
                        "🔥",
                        "FIRE",
                        "Para calcular cuánto patrimonio necesitas para vivir de tus inversiones.",
                        [
                            "Útil si buscas libertad financiera",
                            "Te ayuda a definir una meta",
                            "Buena para planificar a largo plazo",
                        ],
                        "/fire",
                        "Ir a FIRE",
                    ),
                    md=4,
                    className="mb-4",
                ),
                dbc.Col(
                    compare_card(
                        "🏠",
                        "Hipoteca",
                        "Para entender cuota mensual, intereses y coste real de comprar vivienda.",
                        [
                            "Perfecta antes de comprar casa",
                            "Aclara el impacto del plazo",
                            "Te ayuda a comparar opciones",
                        ],
                        "/hipoteca",
                        "Ir a hipoteca",
                    ),
                    md=4,
                    className="mb-4",
                ),
            ]
        ),
    ],
    fluid=True,
    className="px-4 px-md-5 py-4 soft-section home-section",
    id="calculadoras-home",
)

# =========================================================
# CALCULADORAS
# =========================================================

calculadoras = dbc.Container(
    [
        section_badge("ACCESO RÁPIDO"),
        html.H2("Calculadoras", className="fw-bold mb-2 section-title"),
        html.P(
            "Accede directamente a la herramienta que quieras usar.",
            className="section-subtitle mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    teaser_card(
                        "Interés compuesto",
                        "Descubre cuánto crecerá tu dinero con aportaciones mensuales, rentabilidad y tiempo.",
                        "/calculadora",
                        "Calcular",
                        badge="Más usada",
                        icono="💰",
                        featured=True,
                    ),
                    md=4,
                    className="mb-4",
                ),
                dbc.Col(
                    teaser_card(
                        "FIRE",
                        "Calcula cuánto necesitas para alcanzar la libertad financiera y vivir de tus inversiones.",
                        "/fire",
                        "Descubrir",
                        badge="Objetivo",
                        icono="🔥",
                    ),
                    md=4,
                    className="mb-4",
                ),
                dbc.Col(
                    teaser_card(
                        "Hipoteca",
                        "Simula tu cuota mensual y entiende el coste real de comprar una vivienda.",
                        "/hipoteca",
                        "Simular",
                        badge="Vivienda",
                        icono="🏠",
                    ),
                    md=4,
                    className="mb-4",
                ),
            ]
        ),
    ],
    fluid=True,
    className="px-4 px-md-5 py-4 home-section",
)

# =========================================================
# CTA AFILIADO PRINCIPAL
# =========================================================

cta_inversion = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                [
                    section_badge("CUANDO QUIERAS PASAR A LA ACCIÓN", "text-success"),
                    html.H3(
                        "Cuando quieras pasar de simular a invertir, empieza por algo simple",
                        className="fw-bold mb-3 section-title",
                    ),
                    html.P(
                        "Primero entiende tus números. Después, si te encaja, puedes abrir una cuenta "
                        "e invertir poco a poco con constancia.",
                        className="text-muted mb-3",
                    ),
                    html.Ul(
                        [
                            html.Li("Pensado para empezar sin complicarte demasiado."),
                            html.Li("Mejor una estrategia simple que esperar eternamente."),
                            html.Li("Cuanto antes empieces, antes trabaja el interés compuesto."),
                        ],
                        className="text-muted ps-3 mb-0",
                    ),
                ],
                md=8,
            ),
            dbc.Col(
                [
                    dbc.Button(
                        "Abrir cuenta gratis",
                        id="home-cta-invest",
                        color="success",
                        size="lg",
                        className="w-100 rounded-pill fw-semibold mb-2",
                    ),
                    html.Div(
                        "El enlace puede ser afiliado.",
                        className="small text-muted text-center",
                    ),
                ],
                md=4,
                className="d-flex flex-column justify-content-center",
            ),
        ],
        className="align-items-center cta-invest rounded-4 p-4 p-md-5 shadow-sm",
    ),
    fluid=True,
    className="px-4 px-md-5 my-5 home-section",
)

# =========================================================
# ARTÍCULOS
# =========================================================

articulos = dbc.Container(
    [
        section_badge("APRENDE ANTES DE DECIDIR"),
        html.H2("Aprende a invertir mejor", className="fw-bold mb-2 section-title"),
        html.P(
            "Guías sencillas para entender conceptos clave y tomar decisiones con más criterio.",
            className="section-subtitle mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    article_card(
                        "Guía básica",
                        "Qué es el interés compuesto",
                        "Entiende el mecanismo que puede multiplicar tu dinero a largo plazo.",
                        "/blog/interes-compuesto",
                        featured=True,
                    ),
                    md=4,
                    className="mb-4",
                ),
                dbc.Col(
                    article_card(
                        "Libertad financiera",
                        "Cuánto necesitas para FIRE",
                        "Descubre cómo estimar tu número FIRE y qué variables influyen realmente.",
                        "/blog/fire",
                    ),
                    md=4,
                    className="mb-4",
                ),
                dbc.Col(
                    article_card(
                        "Vivienda",
                        "Hipoteca: guía completa",
                        "Evita errores frecuentes y calcula mejor el coste real de comprar vivienda.",
                        "/blog/hipoteca",
                    ),
                    md=4,
                    className="mb-4",
                ),
            ]
        ),
    ],
    fluid=True,
    className="px-4 px-md-5 py-4 home-section",
)

# =========================================================
# CTA FINAL
# =========================================================

final_cta = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                [
                    section_badge("DA EL PRIMER PASO", "text-primary"),
                    html.H2("Empieza por entender tus números", className="fw-bold mb-3 section-title"),
                    html.P(
                        "No necesitas hacerlo todo hoy. Empieza por una simulación y toma mejores decisiones paso a paso.",
                        className="text-muted mb-4",
                    ),
                    html.Div(
                        [
                            dbc.Button(
                                "Ir a interés compuesto",
                                href="/calculadora",
                                color="primary",
                                className="me-2 mb-2 rounded-pill fw-semibold px-4",
                            ),
                            dbc.Button(
                                "Ver FIRE",
                                href="/fire",
                                color="light",
                                className="me-2 mb-2 rounded-pill fw-semibold px-4 border",
                            ),
                            dbc.Button(
                                "Ver hipoteca",
                                href="/hipoteca",
                                color="light",
                                className="mb-2 rounded-pill fw-semibold px-4 border",
                            ),
                        ]
                    ),
                ],
                md=12,
            )
        ],
        className="final-cta-box rounded-4 p-4 p-md-5 shadow-sm",
    ),
    fluid=True,
    className="px-4 px-md-5 my-5 home-section",
)

# =========================================================
# STICKY CTA MÓVIL
# =========================================================

mobile_sticky_cta = html.Div(
    dbc.Button(
        "Empezar a invertir",
        id="home-cta-mobile",
        color="success",
        className="w-100 fw-bold rounded-pill",
    ),
    className="d-md-none",
    style={
        "position": "fixed",
        "left": "12px",
        "right": "12px",
        "bottom": "12px",
        "zIndex": "1050",
        "paddingBottom": "max(0px, env(safe-area-inset-bottom))",
    },
)

# =========================================================
# TRACKERS
# =========================================================

trackers = html.Div(
    [
        html.Div(id="home-cta-invest-tracker", style={"display": "none"}),
        html.Div(id="home-cta-mobile-tracker", style={"display": "none"}),
    ]
)

# =========================================================
# TRACKING CALLBACKS
# =========================================================

clientside_callback(
    f"""
    function(n_clicks) {{
        if (n_clicks) {{
            if (window.gtag) {{
                window.gtag('event', 'click_home_cta_invest', {{
                    event_category: 'affiliate',
                    event_label: 'myinvestor_home_main',
                    value: 1
                }});
            }}
            window.open("{MYINVESTOR_AFFILIATE_URL}", "_blank");
        }}
        return "";
    }}
    """,
    Output("home-cta-invest-tracker", "children"),
    Input("home-cta-invest", "n_clicks"),
)

clientside_callback(
    f"""
    function(n_clicks) {{
        if (n_clicks) {{
            if (window.gtag) {{
                window.gtag('event', 'click_home_cta_mobile', {{
                    event_category: 'affiliate',
                    event_label: 'myinvestor_home_mobile',
                    value: 1
                }});
            }}
            window.open("{MYINVESTOR_AFFILIATE_URL}", "_blank");
        }}
        return "";
    }}
    """,
    Output("home-cta-mobile-tracker", "children"),
    Input("home-cta-mobile", "n_clicks"),
)

# =========================================================
# LAYOUT FINAL
# =========================================================

layout = html.Div(
    [
        hero,
        trust_strip,
        benefits,
        decision_block,
        comparativa,
        calculadoras,
        cta_inversion,
        build_disclaimer(),
        articulos,
        final_cta,
        mobile_sticky_cta,
        trackers,
    ]
)
