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
        className="site-footer",
    )
