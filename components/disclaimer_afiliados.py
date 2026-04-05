from dash import html
import dash_bootstrap_components as dbc

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"
DEGIRO_AFFILIATE_URL = "#"


def affiliate_card(title, description, button_text, href, color="success", disabled=False, badge=None):
    button = dbc.Button(
        button_text,
        color=color,
        className="w-100 rounded-pill fw-semibold",
        disabled=disabled,
    )

    if disabled:
        button_block = html.Div(button)
    else:
        button_block = html.A(
            button,
            href=href,
            target="_blank",
            rel="noopener noreferrer nofollow sponsored",
            style={"textDecoration": "none"},
        )

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
                button_block,
            ]
        ),
        className="affiliate-card h-100 border-0 shadow-sm rounded-4",
    )


def build_disclaimer(title="Da el siguiente paso cuando estés listo"):
    return html.Div(
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
        className="affiliate-wrapper rounded-4 mt-5"
    )
