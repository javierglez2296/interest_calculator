import dash
from dash import html
import dash_bootstrap_components as dbc
from components.disclaimer_afiliados import build_disclaimer

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/",
    title="Calculadora de interés compuesto, FIRE y hipoteca | interescompuesto.app",
    name="Inicio",
    description="Descubre cuánto dinero puedes tener en el futuro. Calcula interés compuesto, FIRE e hipoteca de forma rápida y gratuita."
)

# =========================================================
# HELPERS
# =========================================================
def teaser_card(titulo, texto, href, boton_texto="Abrir", badge=None, icono=None):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.Span(icono or "✨", className="card-icon me-2"),
                        html.Span(badge, className="mini-badge") if badge else None,
                    ],
                    className="d-flex align-items-center mb-3"
                ),
                html.H3(titulo, className="h5 fw-bold mb-2 text-dark"),
                html.P(texto, className="text-muted small mb-4"),
                dbc.Button(
                    boton_texto,
                    href=href,
                    color="primary",
                    className="w-100 rounded-pill fw-semibold"
                ),
            ]
        ),
        className="h-100 shadow-sm border-0 rounded-4 teaser-card"
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
        className="h-100 border-0 shadow-sm rounded-4 benefit-card"
    )


def compare_card(icono, titulo, descripcion, bullets, href, boton):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(icono, className="compare-icon mb-3"),
                html.H3(titulo, className="h5 fw-bold mb-3"),
                html.P(descripcion, className="text-muted small mb-3"),
                html.Ul(
                    [html.Li(item) for item in bullets],
                    className="compare-list mb-4"
                ),
                dbc.Button(
                    boton,
                    href=href,
                    color="primary",
                    outline=True,
                    className="w-100 rounded-pill fw-semibold"
                ),
            ]
        ),
        className="h-100 border-0 shadow-sm rounded-4 compare-card"
    )


# =========================================================
# ESTILOS
# =========================================================
custom_styles = html.Style("""
:root {
    --brand-primary: #2563eb;
    --brand-primary-dark: #1d4ed8;
    --brand-success: #16a34a;
    --brand-warning: #f59e0b;
    --brand-danger-soft: #fff4e8;
    --brand-soft: #eef4ff;
    --brand-soft-2: #f8fbff;
    --brand-soft-3: #f5faff;
    --text-main: #101828;
    --text-soft: #667085;
    --border-soft: rgba(16, 24, 40, 0.08);
    --shadow-soft: 0 10px 30px rgba(16,24,40,0.06);
}

body {
    background-color: #ffffff;
}

.home-section {
    position: relative;
    z-index: 1;
}

.gradient-hero {
    background:
        radial-gradient(circle at top left, rgba(37,99,235,0.18), transparent 35%),
        radial-gradient(circle at 85% 20%, rgba(22,163,74,0.10), transparent 28%),
        linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
}

.hero-title {
    color: var(--text-main);
    line-height: 1.03;
    letter-spacing: -0.03em;
}

.hero-subtitle {
    color: var(--text-soft);
    font-size: 1.1rem;
    max-width: 650px;
}

.hero-pill {
    display: inline-block;
    background: rgba(37,99,235,0.10);
    color: var(--brand-primary-dark);
    border: 1px solid rgba(37,99,235,0.12);
    padding: 0.45rem 0.85rem;
    border-radius: 999px;
    font-size: 0.88rem;
    font-weight: 700;
    margin-bottom: 1rem;
}

.hero-mockup {
    background: linear-gradient(180deg, #ffffff 0%, #f9fbff 100%);
    border: 1px solid rgba(37,99,235,0.08);
    box-shadow: 0 20px 50px rgba(16,24,40,0.10);
    overflow: hidden;
}

.mockup-topbar {
    background: linear-gradient(90deg, #eef4ff 0%, #f8fbff 100%);
    border-bottom: 1px solid rgba(16,24,40,0.06);
    padding: 0.9rem 1rem;
}

.mockup-dot {
    width: 10px;
    height: 10px;
    border-radius: 999px;
    display: inline-block;
    margin-right: 0.4rem;
    background: #cbd5e1;
}

.mockup-badge {
    display: inline-block;
    padding: 0.28rem 0.65rem;
    border-radius: 999px;
    background: rgba(22,163,74,0.10);
    color: #15803d;
    font-size: 0.78rem;
    font-weight: 700;
}

.mockup-box {
    background: #ffffff;
    border: 1px solid rgba(16,24,40,0.06);
    border-radius: 1rem;
    padding: 1rem;
}

.mockup-label {
    font-size: 0.8rem;
    color: var(--text-soft);
    margin-bottom: 0.35rem;
}

.mockup-value {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-main);
    margin-bottom: 0;
}

.mockup-chart {
    height: 180px;
    border-radius: 1rem;
    background:
        linear-gradient(180deg, rgba(37,99,235,0.06) 0%, rgba(37,99,235,0.00) 100%),
        #ffffff;
    border: 1px solid rgba(37,99,235,0.08);
    position: relative;
    overflow: hidden;
}

.mockup-chart-line-1,
.mockup-chart-line-2 {
    position: absolute;
    left: 8%;
    right: 8%;
    height: 3px;
    border-radius: 999px;
    transform-origin: left center;
}

.mockup-chart-line-1 {
    bottom: 28%;
    background: linear-gradient(90deg, #93c5fd 0%, #2563eb 100%);
    transform: rotate(-9deg);
}

.mockup-chart-line-2 {
    bottom: 18%;
    background: linear-gradient(90deg, #86efac 0%, #16a34a 100%);
    transform: rotate(-15deg);
}

.hero-stat {
    background: #ffffff;
    border: 1px solid rgba(16,24,40,0.06);
    border-radius: 1rem;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 8px 24px rgba(16,24,40,0.05);
}

.hero-stat-number {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text-main);
    margin-bottom: 0.2rem;
}

.hero-stat-label {
    font-size: 0.84rem;
    color: var(--text-soft);
    margin-bottom: 0;
}

.section-title {
    color: var(--text-main);
    letter-spacing: -0.02em;
}

.section-subtitle {
    color: var(--text-soft);
    max-width: 760px;
}

.trust-strip {
    background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
    border-top: 1px solid rgba(16,24,40,0.05);
    border-bottom: 1px solid rgba(16,24,40,0.05);
}

.trust-item {
    text-align: center;
    padding: 0.5rem 0.75rem;
}

.trust-item strong {
    display: block;
    color: var(--text-main);
    font-size: 1rem;
}

.trust-item span {
    color: var(--text-soft);
    font-size: 0.88rem;
}

.teaser-card,
.compare-card,
.article-card,
.benefit-card {
    transition: transform 0.22s ease, box-shadow 0.22s ease;
    background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
}

.teaser-card:hover,
.compare-card:hover,
.article-card:hover,
.benefit-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 34px rgba(16,24,40,0.10) !important;
}

.card-icon {
    font-size: 1.25rem;
}

.mini-badge {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--brand-primary-dark);
    background: rgba(37,99,235,0.10);
    padding: 0.28rem 0.6rem;
    border-radius: 999px;
}

.benefit-icon,
.compare-icon {
    width: 52px;
    height: 52px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--brand-soft);
    font-size: 1.4rem;
}

.soft-section {
    background: linear-gradient(180deg, #ffffff 0%, #f9fbff 100%);
}

.emotional-box {
    background:
        linear-gradient(135deg, rgba(37,99,235,0.08) 0%, rgba(22,163,74,0.06) 100%),
        #ffffff;
    border: 1px solid rgba(37,99,235,0.08);
}

.cta-invest {
    background:
        linear-gradient(135deg, rgba(22,163,74,0.12) 0%, rgba(37,99,235,0.08) 100%),
        #ffffff;
    border: 1px solid rgba(16,24,40,0.06);
}

.article-top-label {
    color: var(--brand-primary-dark);
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}

.compare-list {
    padding-left: 1.1rem;
    color: #475467;
    font-size: 0.92rem;
}

.compare-list li {
    margin-bottom: 0.45rem;
}

.final-cta-box {
    background:
        radial-gradient(circle at top right, rgba(37,99,235,0.10), transparent 28%),
        linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
    border: 1px solid rgba(37,99,235,0.08);
}

.separator-space {
    height: 24px;
}

@media (max-width: 768px) {
    .hero-title {
        font-size: 2.2rem !important;
        line-height: 1.08;
    }

    .hero-subtitle {
        font-size: 1rem;
    }

    .hero-stat {
        margin-bottom: 0.75rem;
    }

    .mockup-chart {
        height: 150px;
    }
}
""")

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
                        "Descubre cuánto dinero puedes tener en el futuro",
                        className="display-4 fw-bold mb-3 hero-title",
                    ),
                    html.P(
                        "Simula tu inversión, tu objetivo FIRE y tu hipoteca con herramientas claras, rápidas y pensadas para ayudarte a decidir mejor.",
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
                                "Ver todas las calculadoras",
                                href="#calculadoras-home",
                                color="light",
                                size="lg",
                                className="mb-2 px-4 rounded-pill fw-semibold border",
                            ),
                        ],
                        className="mb-3"
                    ),
                    html.P(
                        "Sin registro. Gratis. Resultados inmediatos.",
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
                                    className="hero-stat"
                                ),
                                xs=4
                            ),
                            dbc.Col(
                                html.Div(
                                    [
                                        html.Div("Gratis", className="hero-stat-number"),
                                        html.P("uso libre", className="hero-stat-label"),
                                    ],
                                    className="hero-stat"
                                ),
                                xs=4
                            ),
                            dbc.Col(
                                html.Div(
                                    [
                                        html.Div("1 min", className="hero-stat-number"),
                                        html.P("para simular", className="hero-stat-label"),
                                    ],
                                    className="hero-stat"
                                ),
                                xs=4
                            ),
                        ],
                        className="g-2"
                    ),
                ],
                lg=6,
                className="py-5"
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
                                className="mockup-topbar"
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
                                                    className="mockup-box"
                                                ),
                                                md=6,
                                                className="mb-3"
                                            ),
                                            dbc.Col(
                                                html.Div(
                                                    [
                                                        html.Div("Aportación mensual", className="mockup-label"),
                                                        html.P("300€/mes", className="mockup-value"),
                                                    ],
                                                    className="mockup-box"
                                                ),
                                                md=6,
                                                className="mb-3"
                                            ),
                                        ]
                                    ),
                                    html.Div(
                                        [
                                            html.Div(className="mockup-chart-line-1"),
                                            html.Div(className="mockup-chart-line-2"),
                                        ],
                                        className="mockup-chart mb-3"
                                    ),
                                    html.Div(
                                        [
                                            html.Div("Visualiza escenarios", className="fw-semibold text-dark mb-1"),
                                            html.Div(
                                                "Comprende mejor qué ocurre cuando cambias tiempo, rentabilidad o aportaciones.",
                                                className="text-muted small"
                                            ),
                                        ]
                                    )
                                ]
                            )
                        ],
                        className="hero-mockup rounded-4 border-0"
                    )
                ],
                lg=6,
                className="d-flex align-items-center"
            ),
        ],
        className="align-items-center"
    ),
    fluid=True,
    className="px-4 px-md-5 py-5 gradient-hero home-section"
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
        className="py-3"
    ),
    fluid=True,
    className="px-4 px-md-5 trust-strip home-section"
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
                        html.H2("Todo lo que necesitas para tomar mejores decisiones financieras", className="fw-bold mb-2 section-title"),
                        html.P(
                            "Herramientas claras, resultados rápidos y contenido útil para pasar de la teoría a la acción.",
                            className="section-subtitle mb-4"
                        ),
                    ],
                    width=12
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    benefit_card("📈", "Visualiza tu futuro", "Entiende cuánto puede crecer tu patrimonio con aportaciones periódicas y tiempo."),
                    md=4,
                    className="mb-4"
                ),
                dbc.Col(
                    benefit_card("🔥", "Planifica tu FIRE", "Calcula cuánto necesitas para acercarte a la libertad financiera."),
                    md=4,
                    className="mb-4"
                ),
                dbc.Col(
                    benefit_card("🏠", "Decide mejor tu hipoteca", "Evita errores y comprende mejor el coste real de comprar vivienda."),
                    md=4,
                    className="mb-4"
                ),
            ]
        )
    ],
    fluid=True,
    className="px-4 px-md-5 py-4 home-section"
)

# =========================================================
# BLOQUE EMOCIONAL
# =========================================================
emotional_block = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2(
                            "El tiempo puede hacer más por tu dinero que tus esfuerzos puntuales",
                            className="fw-bold mb-3 section-title",
                        ),
                        html.P(
                            "Invertir de forma constante durante años puede marcar una diferencia enorme en tu patrimonio futuro.",
                            className="lead text-muted mb-2",
                        ),
                        html.P(
                            "No necesitas empezar perfecto. Necesitas empezar con criterio y mantener constancia.",
                            className="text-muted mb-0",
                        ),
                    ],
                    md=8,
                ),
                dbc.Col(
                    [
                        dbc.Button(
                            "Ver simulación ahora",
                            href="/calculadora",
                            color="primary",
                            size="lg",
                            className="w-100 rounded-pill fw-semibold"
                        )
                    ],
                    md=4,
                    className="d-flex align-items-center"
                ),
            ],
            className="align-items-center emotional-box rounded-4 p-4 p-md-5 shadow-sm",
        )
    ],
    fluid=True,
    className="px-4 px-md-5 my-5 home-section"
)

# =========================================================
# COMPARATIVA
# =========================================================
comparativa = dbc.Container(
    [
        html.H2("¿Qué calculadora necesitas ahora?", className="fw-bold mb-2 section-title"),
        html.P(
            "Cada herramienta responde a una pregunta distinta. Elige según tu objetivo.",
            className="section-subtitle mb-4"
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
                        "Ir a la calculadora"
                    ),
                    md=4,
                    className="mb-4"
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
                        "Ir a FIRE"
                    ),
                    md=4,
                    className="mb-4"
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
                        "Ir a hipoteca"
                    ),
                    md=4,
                    className="mb-4"
                ),
            ]
        ),
    ],
    fluid=True,
    className="px-4 px-md-5 py-4 soft-section home-section",
    id="calculadoras-home"
)

# =========================================================
# CALCULADORAS
# =========================================================
calculadoras = dbc.Container(
    [
        html.H2("Calculadoras", className="fw-bold mb-2 section-title"),
        html.P(
            "Accede directamente a la herramienta que quieras usar.",
            className="section-subtitle mb-4"
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
                        icono="💰"
                    ),
                    md=4,
                    className="mb-4"
                ),
                dbc.Col(
                    teaser_card(
                        "FIRE",
                        "Calcula cuánto necesitas para alcanzar la libertad financiera y vivir de tus inversiones.",
                        "/fire",
                        "Descubrir",
                        badge="Objetivo",
                        icono="🔥"
                    ),
                    md=4,
                    className="mb-4"
                ),
                dbc.Col(
                    teaser_card(
                        "Hipoteca",
                        "Simula tu cuota mensual y entiende el coste real de comprar una vivienda.",
                        "/hipoteca",
                        "Simular",
                        badge="Vivienda",
                        icono="🏠"
                    ),
                    md=4,
                    className="mb-4"
                ),
            ]
        ),
    ],
    fluid=True,
    className="px-4 px-md-5 py-4 home-section"
)

# =========================================================
# CTA AFILIADO
# =========================================================
cta_inversion = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                [
                    html.Div("Empieza con una cuenta real", className="article-top-label mb-2"),
                    html.H3("Cuando quieras pasar de simular a invertir, empieza por algo simple", className="fw-bold mb-3 section-title"),
                    html.P(
                        "Primero entiende tus números. Después, si te encaja, puedes abrir una cuenta e invertir poco a poco con constancia.",
                        className="text-muted mb-0",
                    ),
                ],
                md=8,
            ),
            dbc.Col(
                [
                    dbc.Button(
                        "Abrir cuenta gratis",
                        href=MYINVESTOR_AFFILIATE_URL,
                        target="_blank",
                        color="success",
                        size="lg",
                        className="w-100 rounded-pill fw-semibold"
                    )
                ],
                md=4,
                className="d-flex align-items-center"
            ),
        ],
        className="align-items-center cta-invest rounded-4 p-4 p-md-5 shadow-sm",
    ),
    fluid=True,
    className="px-4 px-md-5 my-5 home-section"
)

# =========================================================
# ARTÍCULOS
# =========================================================
articulos = dbc.Container(
    [
        html.H2("Aprende a invertir mejor", className="fw-bold mb-2 section-title"),
        html.P(
            "Guías sencillas para entender conceptos clave y tomar decisiones con más criterio.",
            className="section-subtitle mb-4"
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div("Guía básica", className="article-top-label mb-2"),
                                html.H3("Qué es el interés compuesto", className="h5 fw-bold mb-2"),
                                html.P(
                                    "Entiende el mecanismo que puede multiplicar tu dinero a largo plazo.",
                                    className="text-muted small mb-4"
                                ),
                                dbc.Button(
                                    "Leer artículo",
                                    href="/blog/interes-compuesto",
                                    color="primary",
                                    className="w-100 rounded-pill fw-semibold"
                                ),
                            ]
                        ),
                        className="h-100 border-0 shadow-sm rounded-4 article-card"
                    ),
                    md=4,
                    className="mb-4"
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div("Libertad financiera", className="article-top-label mb-2"),
                                html.H3("Cuánto necesitas para FIRE", className="h5 fw-bold mb-2"),
                                html.P(
                                    "Descubre cómo estimar tu número FIRE y qué variables influyen realmente.",
                                    className="text-muted small mb-4"
                                ),
                                dbc.Button(
                                    "Leer artículo",
                                    href="/blog/fire",
                                    color="primary",
                                    className="w-100 rounded-pill fw-semibold"
                                ),
                            ]
                        ),
                        className="h-100 border-0 shadow-sm rounded-4 article-card"
                    ),
                    md=4,
                    className="mb-4"
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div("Vivienda", className="article-top-label mb-2"),
                                html.H3("Hipoteca: guía completa", className="h5 fw-bold mb-2"),
                                html.P(
                                    "Evita errores frecuentes y calcula mejor el coste real de comprar vivienda.",
                                    className="text-muted small mb-4"
                                ),
                                dbc.Button(
                                    "Leer artículo",
                                    href="/blog/hipoteca",
                                    color="primary",
                                    className="w-100 rounded-pill fw-semibold"
                                ),
                            ]
                        ),
                        className="h-100 border-0 shadow-sm rounded-4 article-card"
                    ),
                    md=4,
                    className="mb-4"
                ),
            ]
        ),
    ],
    fluid=True,
    className="px-4 px-md-5 py-4 home-section"
)

# =========================================================
# CTA FINAL
# =========================================================
final_cta = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H2("Empieza por entender tus números", className="fw-bold mb-3 section-title"),
                    html.P(
                        "No necesitas hacerlo todo hoy. Empieza por una simulación y toma mejores decisiones paso a paso.",
                        className="text-muted mb-4"
                    ),
                    html.Div(
                        [
                            dbc.Button(
                                "Ir a interés compuesto",
                                href="/calculadora",
                                color="primary",
                                className="me-2 mb-2 rounded-pill fw-semibold px-4"
                            ),
                            dbc.Button(
                                "Ver FIRE",
                                href="/fire",
                                color="light",
                                className="me-2 mb-2 rounded-pill fw-semibold px-4 border"
                            ),
                            dbc.Button(
                                "Ver hipoteca",
                                href="/hipoteca",
                                color="light",
                                className="mb-2 rounded-pill fw-semibold px-4 border"
                            ),
                        ]
                    )
                ],
                md=12
            )
        ],
        className="final-cta-box rounded-4 p-4 p-md-5 shadow-sm"
    ),
    fluid=True,
    className="px-4 px-md-5 my-5 home-section"
)

# =========================================================
# LAYOUT FINAL
# =========================================================
layout = html.Div(
    [
        custom_styles,
        hero,
        trust_strip,
        benefits,
        emotional_block,
        comparativa,
        calculadoras,
        cta_inversion,
        build_disclaimer(),
        articulos,
        final_cta,
    ]
)
