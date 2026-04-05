from dash import html
import dash_bootstrap_components as dbc


def footer_link(label, href):
    return html.A(
        label,
        href=href,
        className="footer-link d-block mb-2",
    )


def build_footer():
    return html.Footer(
        [
            html.Style(
                """
                .site-footer {
                    background:
                        linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
                    border-top: 1px solid rgba(16, 24, 40, 0.06);
                    margin-top: 3rem;
                }

                [data-bs-theme="dark"] .site-footer {
                    background:
                        linear-gradient(180deg, #101828 0%, #0b1220 100%);
                    border-top: 1px solid rgba(255, 255, 255, 0.08);
                }

                .footer-brand {
                    display: flex;
                    align-items: center;
                    gap: 0.65rem;
                    margin-bottom: 1rem;
                }

                .footer-brand-dot {
                    width: 14px;
                    height: 14px;
                    border-radius: 999px;
                    background: linear-gradient(135deg, #2563eb 0%, #16a34a 100%);
                    box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.10);
                    flex-shrink: 0;
                }

                .footer-brand-text {
                    font-size: 1.05rem;
                    font-weight: 800;
                    letter-spacing: -0.02em;
                    color: #101828;
                    margin: 0;
                }

                [data-bs-theme="dark"] .footer-brand-text {
                    color: #f8fafc;
                }

                .footer-description {
                    color: #667085;
                    font-size: 0.95rem;
                    line-height: 1.7;
                    max-width: 420px;
                    margin-bottom: 0;
                }

                [data-bs-theme="dark"] .footer-description {
                    color: #98a2b3;
                }

                .footer-title {
                    font-size: 0.82rem;
                    font-weight: 800;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    color: #1d4ed8;
                    margin-bottom: 1rem;
                }

                [data-bs-theme="dark"] .footer-title {
                    color: #93c5fd;
                }

                .footer-link {
                    color: #475467;
                    text-decoration: none;
                    font-weight: 500;
                    transition: color 0.2s ease, transform 0.2s ease;
                }

                .footer-link:hover {
                    color: #1d4ed8;
                    transform: translateX(2px);
                }

                [data-bs-theme="dark"] .footer-link {
                    color: #cbd5e1;
                }

                [data-bs-theme="dark"] .footer-link:hover {
                    color: #dbeafe;
                }

                .footer-bottom {
                    border-top: 1px solid rgba(16, 24, 40, 0.06);
                    margin-top: 2rem;
                    padding-top: 1.25rem;
                }

                [data-bs-theme="dark"] .footer-bottom {
                    border-top: 1px solid rgba(255, 255, 255, 0.08);
                }

                .footer-bottom-text {
                    color: #667085;
                    font-size: 0.9rem;
                    margin-bottom: 0.35rem;
                }

                .footer-disclaimer {
                    color: #667085;
                    font-size: 0.84rem;
                    margin-bottom: 0;
                    line-height: 1.6;
                }

                [data-bs-theme="dark"] .footer-bottom-text,
                [data-bs-theme="dark"] .footer-disclaimer {
                    color: #98a2b3;
                }

                @media (max-width: 767.98px) {
                    .footer-brand {
                        margin-bottom: 0.85rem;
                    }

                    .footer-title {
                        margin-top: 1.5rem;
                        margin-bottom: 0.75rem;
                    }

                    .footer-bottom {
                        margin-top: 1.5rem;
                    }
                }
                """
            ),
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Div(
                                        [
                                            html.Div(className="footer-brand-dot"),
                                            html.P("Interés Compuesto", className="footer-brand-text"),
                                        ],
                                        className="footer-brand",
                                    ),
                                    html.P(
                                        "Simuladores financieros en español para ayudarte a entender mejor tu inversión, tu libertad financiera y tu hipoteca.",
                                        className="footer-description",
                                    ),
                                ],
                                md=5,
                                className="mb-4 mb-md-0",
                            ),
                            dbc.Col(
                                [
                                    html.Div("Herramientas", className="footer-title"),
                                    footer_link("Interés compuesto", "/calculadora"),
                                    footer_link("FIRE", "/fire"),
                                    footer_link("Hipoteca", "/hipoteca"),
                                ],
                                md=3,
                            ),
                            dbc.Col(
                                [
                                    html.Div("Contenido", className="footer-title"),
                                    footer_link("Inicio", "/"),
                                    footer_link("Blog", "/blog"),
                                    footer_link("Qué es el interés compuesto", "/blog/interes-compuesto"),
                                ],
                                md=4,
                            ),
                        ],
                        className="py-5",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Div(
                                        "© 2026 interescompuesto.app · Simuladores financieros en español",
                                        className="footer-bottom-text text-center text-md-start",
                                    ),
                                    html.P(
                                        "La información ofrecida en esta web es orientativa y no constituye asesoramiento financiero personalizado.",
                                        className="footer-disclaimer text-center text-md-start",
                                    ),
                                ],
                                width=12,
                                className="footer-bottom",
                            )
                        ]
                    ),
                ],
                fluid=True,
                className="px-4 px-md-5",
            ),
        ],
        className="site-footer",
    )
