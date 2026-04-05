from dash import html
import dash_bootstrap_components as dbc

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"
DEGIRO_AFFILIATE_URL = "#"


def affiliate_card(title, description, button_text, href, color="success", disabled=False, badge=None):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.H5(title, className="fw-bold mb-1"),
                        html.Span(badge, className="affiliate-badge") if badge else None,
                    ],
                    className="d-flex justify-content-between align-items-center mb-2"
                ),
                html.P(description, className="text-muted small mb-4"),
                html.A(
                    dbc.Button(
                        button_text,
                        color=color,
                        className="w-100 rounded-pill fw-semibold",
                        disabled=disabled,
                    ),
                    href=href,
                    target="_blank",
                    rel="noopener noreferrer nofollow sponsored",
                    style={"textDecoration": "none"},
                ),
            ]
        ),
        className="affiliate-card h-100 border-0 shadow-sm rounded-4",
    )


def build_disclaimer(title="Da el siguiente paso cuando estés listo"):
    return html.Div(
        [
            html.Style(
                """
                .affiliate-wrapper {
                    background:
                        linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
                    border: 1px solid rgba(16,24,40,0.06);
                }

                .affiliate-title {
                    color: #101828;
                    letter-spacing: -0.02em;
                }

                .affiliate-subtitle {
                    color: #667085;
                    max-width: 680px;
                }

                .affiliate-card {
                    background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
                    transition: transform 0.2s ease, box-shadow 0.2s ease;
                }

                .affiliate-card:hover {
                    transform: translateY(-4px);
                    box-shadow: 0 16px 34px rgba(16,24,40,0.10) !important;
                }

                .affiliate-badge {
                    font-size: 0.7rem;
                    font-weight: 700;
                    color: #1d4ed8;
                    background: rgba(37,99,235,0.10);
                    padding: 0.25rem 0.55rem;
                    border-radius: 999px;
                }

                .affiliate-alert {
                    background: rgba(16,24,40,0.03);
                    border: 1px solid rgba(16,24,40,0.06);
                    border-radius: 0.75rem;
                }

                [data-bs-theme="dark"] .affiliate-wrapper {
                    background: #0f172a;
                    border: 1px solid rgba(255,255,255,0.08);
                }

                [data-bs-theme="dark"] .affiliate-title {
                    color: #f8fafc;
                }

                [data-bs-theme="dark"] .affiliate-subtitle {
                    color: #94a3b8;
                }

                [data-bs-theme="dark"] .affiliate-card {
                    background: #111827;
                }

                [data-bs-theme="dark"] .affiliate-alert {
                    background: rgba(255,255,255,0.04);
                    border: 1px solid rgba(255,255,255,0.08);
                    color: #94a3b8;
                }
                """
            ),

            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H2(title, className="fw-bold mb-2 affiliate-title"),
                                    html.P(
                                        "Si después de simular quieres empezar, estas opciones pueden encajar según tu perfil y objetivo.",
                                        className="affiliate-subtitle mb-4",
                                    ),
                                ],
                                width=12
                            )
                        ]
                    ),

                    dbc.Row(
                        [
                            dbc.Col(
                                affiliate_card(
                                    "MyInvestor",
                                    "Ideal para inversión a largo plazo con fondos indexados y estrategia pasiva.",
                                    "Abrir cuenta gratis",
                                    MYINVESTOR_AFFILIATE_URL,
                                    color="success",
                                    badge="Recomendado"
                                ),
                                md=6,
                                className="mb-3"
                            ),

                            dbc.Col(
                                affiliate_card(
                                    "DEGIRO",
                                    "Pensado para acciones y ETFs. Añádelo cuando tengas el partner activo.",
                                    "Próximamente",
                                    DEGIRO_AFFILIATE_URL,
                                    color="secondary",
                                    disabled=True
                                ),
                                md=6,
                                className="mb-3"
                            ),
                        ],
                        className="g-3"
                    ),

                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Alert(
                                    "Algunos enlaces pueden ser promocionales. Si contratas a través de ellos, la web puede recibir una comisión sin coste adicional para ti.",
                                    className="affiliate-alert mt-3 mb-0 small",
                                ),
                                width=12
                            )
                        ]
                    ),
                ],
                fluid=True,
                className="px-4 px-md-5 py-5"
            ),
        ],
        className="affiliate-wrapper rounded-4 mt-5"
    )
