import dash
from dash import html
import dash_bootstrap_components as dbc
from components.disclaimer_afiliados import build_disclaimer

dash.register_page(
    __name__,
    path="/",
    title="Calculadora de interés compuesto, FIRE, hipoteca y rentabilidad | interescompuesto.app",
    name="Inicio",
    description=(
        "Calculadoras financieras en español para inversión, FIRE, hipoteca, "
        "rentabilidad de alquiler y comparación de alternativas."
    ),
)

# =========================================================
# HELPERS
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
                                        "Ver calculadora hipoteca",
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
                                        "Explora las tres áreas clave de la web: inversión, independencia "
                                        "financiera y compra de vivienda.",
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
                                "Desde inversión a vivienda, pasando por independencia financiera, "
                                "rentabilidad inmobiliaria y comparativas. Esta home debe funcionar "
                                "como un hub real de herramientas.",
                                className="section-subtitle mb-0",
                            ),
                        ],
                        lg=8,
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.Div(
                                    "Más clics internos, más tiempo en página y más oportunidades de monetización.",
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
        ]
    ),
    className="calculadoras-section",
)

quick_actions_section = html.Div(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div("Empieza según tu objetivo", className="section-eyebrow"),
                            html.H2(
                                "No todas las personas buscan lo mismo",
                                className="section-title fw-bold mb-3",
                            ),
                            html.P(
                                "Te dejo accesos rápidos según el tipo de decisión que quieras tomar ahora.",
                                className="section-subtitle mb-4",
                            ),
                        ],
                        lg=8,
                    ),
                ]
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

# =========================================================
# LAYOUT
# =========================================================
layout = html.Div(
    [
        html.Style(
            """
            .home-hero {
                background:
                    radial-gradient(circle at top left, rgba(13,110,253,0.10), transparent 35%),
                    radial-gradient(circle at top right, rgba(25,135,84,0.08), transparent 28%),
                    linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
                padding-top: 4rem;
                padding-bottom: 4rem;
            }

            .hero-badge {
                display: inline-block;
                background: #eef4ff;
                color: #0d6efd;
                border: 1px solid #d7e6ff;
                padding: 0.45rem 0.85rem;
                border-radius: 999px;
                font-size: 0.82rem;
                font-weight: 700;
                letter-spacing: 0.02em;
            }

            .hero-title {
                font-size: clamp(2.2rem, 5vw, 4.2rem);
                line-height: 1.05;
                letter-spacing: -0.04em;
                color: #101828;
                max-width: 12ch;
            }

            .hero-subtitle {
                font-size: 1.05rem;
                color: #475467;
                max-width: 60ch;
            }

            .hero-metrics {
                display: flex;
                gap: 0.85rem;
                flex-wrap: wrap;
                margin-top: 1.5rem;
            }

            .hero-metric-card {
                background: rgba(255,255,255,0.85);
                border: 1px solid #eaecf0;
                border-radius: 18px;
                padding: 0.8rem 1rem;
                min-width: 140px;
                box-shadow: 0 8px 20px rgba(16,24,40,0.04);
            }

            .hero-metric-label {
                color: #667085;
                font-size: 0.78rem;
                font-weight: 600;
                margin-bottom: 0.15rem;
            }

            .hero-metric-value {
                color: #101828;
                font-size: 1rem;
                font-weight: 800;
            }

            .hero-side-card {
                background: rgba(255,255,255,0.9);
                backdrop-filter: blur(8px);
            }

            .teaser-card {
                transition: transform 0.18s ease, box-shadow 0.18s ease;
            }

            .teaser-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 16px 35px rgba(16,24,40,0.08);
            }

            .teaser-icon {
                font-size: 1.25rem;
            }

            .calculadoras-section {
                padding-top: 5rem;
                padding-bottom: 4rem;
                background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
            }

            .quick-actions-section {
                padding-top: 1rem;
                padding-bottom: 3rem;
                background: #ffffff;
            }

            .cta-section {
                padding-bottom: 3rem;
                background: #ffffff;
            }

            .section-eyebrow {
                display: inline-block;
                font-size: 0.78rem;
                font-weight: 800;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: #0d6efd;
                background: #eef4ff;
                border: 1px solid #d7e6ff;
                padding: 0.42rem 0.75rem;
                border-radius: 999px;
                margin-bottom: 1rem;
            }

            .section-title {
                font-size: clamp(1.8rem, 3vw, 2.7rem);
                line-height: 1.08;
                letter-spacing: -0.03em;
                color: #101828;
            }

            .section-subtitle {
                color: #667085;
                font-size: 1.02rem;
                max-width: 720px;
            }

            .calc-card {
                background: rgba(255,255,255,0.94);
                box-shadow: 0 10px 30px rgba(16,24,40,0.06);
                transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
                border: 1px solid rgba(16,24,40,0.06);
                backdrop-filter: blur(8px);
            }

            .calc-card:hover {
                transform: translateY(-4px);
                box-shadow: 0 18px 40px rgba(16,24,40,0.10);
                border-color: rgba(13,110,253,0.18);
            }

            .calc-card-featured {
                background:
                    linear-gradient(180deg, rgba(255,255,255,0.98) 0%, rgba(244,248,255,0.96) 100%);
                border: 1px solid rgba(13,110,253,0.18);
                box-shadow: 0 14px 40px rgba(13,110,253,0.10);
            }

            .calc-card-icon {
                width: 52px;
                height: 52px;
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
                background: linear-gradient(180deg, #f8fbff 0%, #eef4ff 100%);
                border: 1px solid #d7e6ff;
            }

            .calc-card-badge {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                padding: 0.35rem 0.7rem;
                border-radius: 999px;
                font-size: 0.74rem;
                font-weight: 700;
                color: #0d6efd;
                background: #eef4ff;
                border: 1px solid #d7e6ff;
                text-align: center;
            }

            .calc-card-btn.btn-light {
                background: #f8fafc;
                border: 1px solid #e4e7ec;
            }

            .calc-card-btn.btn-light:hover {
                background: #eef2f6;
                border-color: #d0d5dd;
            }

            .calc-highlight-box {
                background:
                    radial-gradient(circle at top right, rgba(13,110,253,0.08), transparent 30%),
                    linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
                border: 1px solid #eaecf0;
                border-radius: 24px;
                padding: 1.25rem;
                box-shadow: 0 8px 24px rgba(16,24,40,0.04);
            }

            .quick-card {
                transition: transform 0.18s ease, box-shadow 0.18s ease;
            }

            .quick-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 16px 35px rgba(16,24,40,0.08);
            }

            .cta-panel {
                background:
                    radial-gradient(circle at top right, rgba(13,110,253,0.08), transparent 28%),
                    linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
            }

            @media (max-width: 991px) {
                .home-hero {
                    padding-top: 3rem;
                    padding-bottom: 3rem;
                }

                .calculadoras-section {
                    padding-top: 3.5rem;
                    padding-bottom: 2.5rem;
                }

                .hero-title {
                    max-width: none;
                }
            }
            """
        ),
        hero_section,
        html.Div(id="todas-las-calculadoras"),
        calculadoras_section,
        quick_actions_section,
        cta_section,
        books_section_v3(),
        build_disclaimer(title="Empieza a dar el siguiente paso"),
    ]
)
