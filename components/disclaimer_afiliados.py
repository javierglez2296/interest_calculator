from dash import html
import dash_bootstrap_components as dbc

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"
DEGIRO_AFFILIATE_URL = "#"

def build_disclaimer(title="Opciones para empezar a invertir"):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4(title, className="fw-bold mb-3"),
                html.P(
                    "Si después de hacer tu simulación quieres pasar a la acción, aquí puedes añadir opciones patrocinadas coherentes con el resultado.",
                    className="muted",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5("MyInvestor", className="fw-bold"),
                                        html.P(
                                            "Enfoque útil para fondos indexados e inversión a largo plazo en España.",
                                            className="muted",
                                        ),
                                        html.A(
                                            dbc.Button(
                                                "Abrir cuenta con MyInvestor",
                                                color="success",
                                                className="w-100",
                                            ),
                                            href=MYINVESTOR_AFFILIATE_URL,
                                            target="_blank",
                                            rel="noopener noreferrer nofollow sponsored",
                                            style={"textDecoration": "none"},
                                        ),
                                    ]
                                ),
                                className="soft-card h-100",
                            ),
                            md=6,
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5("DEGIRO", className="fw-bold"),
                                        html.P(
                                            "Reserva este bloque para acciones/ETFs cuando tengas el partner activo.",
                                            className="muted",
                                        ),
                                        html.A(
                                            dbc.Button(
                                                "Próximamente DEGIRO",
                                                color="secondary",
                                                className="w-100",
                                                disabled=True,
                                            ),
                                            href=DEGIRO_AFFILIATE_URL,
                                            style={"textDecoration": "none"},
                                        ),
                                    ]
                                ),
                                className="soft-card h-100",
                            ),
                            md=6,
                        ),
                    ],
                    className="g-3",
                ),
                dbc.Alert(
                    "Aviso de afiliación: algunos enlaces pueden ser promocionales. Si contratas a través de ellos, la web puede recibir una comisión sin coste adicional para ti.",
                    color="light",
                    className="mt-3 mb-0 small",
                ),
            ]
        ),
        className="soft-card mt-4",
    )
