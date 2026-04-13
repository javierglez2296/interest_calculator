import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path="/premium-ok",
    title="Pago confirmado | interescompuesto.app",
    name="Premium OK",
)

layout = dbc.Container(
    [
        dcc.Location(id="premium-ok-url", refresh=False),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div(
                                    "Pago completado",
                                    className="text-uppercase fw-bold mb-3",
                                    style={
                                        "letterSpacing": "0.08em",
                                        "color": "#667085",
                                        "fontSize": "0.85rem",
                                    },
                                ),
                                html.Div(
                                    "✅",
                                    className="mb-3",
                                    style={
                                        "fontSize": "3rem",
                                        "lineHeight": "1",
                                    },
                                ),
                                html.H1(
                                    "Ya tienes desbloqueadas todas las calculadoras premium",
                                    className="fw-bold mb-3",
                                    style={
                                        "color": "#0f172a",
                                        "fontSize": "clamp(2rem, 4vw, 3rem)",
                                        "lineHeight": "1.1",
                                        "letterSpacing": "-0.03em",
                                    },
                                ),
                                html.P(
                                    "Se ha activado el acceso premium en este dispositivo. Ya puedes usar Monte Carlo, guardar simulaciones, exportaciones y futuras funciones premium.",
                                    className="mb-4",
                                    style={
                                        "color": "#475467",
                                        "lineHeight": "1.75",
                                        "fontSize": "1.05rem",
                                        "maxWidth": "700px",
                                        "margin": "0 auto",
                                    },
                                ),
                                dbc.Alert(
                                    "Acceso premium activado correctamente.",
                                    color="success",
                                    className="rounded-4 border-0 mb-4",
                                ),
                                html.Div(
                                    [
                                        dbc.Button(
                                            "Ir a la calculadora de interés compuesto",
                                            href="/calculadora",
                                            color="success",
                                            className="rounded-pill fw-bold px-4 py-3 me-2 mb-2",
                                        ),
                                        dbc.Button(
                                            "Ver calculadora FIRE",
                                            href="/fire",
                                            color="secondary",
                                            className="rounded-pill fw-semibold px-4 py-3 mb-2",
                                        ),
                                    ],
                                    className="d-flex flex-wrap justify-content-center",
                                ),
                            ],
                            className="text-center p-4 p-md-5",
                        ),
                        className="border-0 rounded-4",
                        style={
                            "background": "linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)",
                            "boxShadow": "0 18px 45px rgba(16, 24, 40, 0.08)",
                        },
                    ),
                    lg=8,
                    className="mx-auto",
                )
            ]
        )
    ],
    fluid=True,
    className="py-5 px-4",
    style={"maxWidth": "1200px"},
)


@callback(
    Output("premium-access", "data", allow_duplicate=True),
    Input("premium-ok-url", "pathname"),
    prevent_initial_call="initial_duplicate",
)
def unlock_premium(pathname):
    if pathname == "/premium-ok":
        return {"unlocked": True, "source": "stripe_redirect"}
    return dash.no_update
