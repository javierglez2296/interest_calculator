import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import requests

from utils.config import SITE_URL

dash.register_page(
    __name__,
    path="/premium-ok",
    title="Pago confirmado | interescompuesto.app",
    name="Premium OK",
)

layout = dbc.Container(
    [
        dcc.Location(id="premium-ok-url", refresh=False),
        dcc.Store(id="premium-access", storage_type="local"),

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
                                html.Div("✅", className="mb-3", style={"fontSize": "3rem"}),

                                html.H1(
                                    "Activa tu acceso premium",
                                    className="fw-bold mb-3",
                                ),

                                html.P(
                                    "Introduce el email que usaste en Stripe. Si el pago está registrado, activaremos el premium en este navegador.",
                                    className="mb-4 text-muted",
                                ),

                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Input(
                                                id="premium-email-input",
                                                type="email",
                                                placeholder="tuemail@dominio.com",
                                                class_name="rounded-pill",
                                            ),
                                            md=8,
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                "Activar premium",
                                                id="premium-validate-btn",
                                                color="success",
                                                className="rounded-pill fw-bold w-100",
                                            ),
                                            md=4,
                                        ),
                                    ],
                                    class_name="g-2 justify-content-center mb-4",
                                ),

                                html.Div(id="premium-validation-feedback", className="mb-4"),

                                dbc.Button(
                                    "Ir a la app",
                                    href="/",
                                    color="primary",
                                    className="rounded-pill px-4",
                                ),
                            ],
                            className="text-center p-4 p-md-5",
                        ),
                        className="border-0 rounded-4 shadow-sm",
                    ),
                    lg=8,
                    className="mx-auto",
                )
            ]
        ),
    ],
    fluid=True,
    className="py-5 px-4",
)


@callback(
    Output("premium-access", "data"),
    Output("premium-validation-feedback", "children"),
    Input("premium-validate-btn", "n_clicks"),
    State("premium-email-input", "value"),
    prevent_initial_call=True,
)
def validate_premium_access(n_clicks, email):
    email = (email or "").strip().lower()

    if not email:
        return (
            dash.no_update,
            dbc.Alert(
                "Introduce tu email para validar el premium.",
                color="warning",
                class_name="rounded-4",
            ),
        )

    try:
        response = requests.post(
            f"{SITE_URL}/api/check-premium",
            json={"email": email},
            timeout=8,
        )

        data = response.json()

        if response.ok and data.get("unlocked"):
            return (
                {
                    "unlocked": True,
                    "email": email,
                },
                dbc.Alert(
                    "✅ Premium activado correctamente.",
                    color="success",
                    class_name="rounded-4",
                ),
            )

        return (
            {"unlocked": False, "email": email},
            dbc.Alert(
                "❌ No hemos encontrado una compra premium con ese email.",
                color="danger",
                class_name="rounded-4",
            ),
        )

    except Exception as e:
        print("❌ Error validando premium:", e)
        return (
            dash.no_update,
            dbc.Alert(
                "Error validando el premium. Inténtalo de nuevo.",
                color="warning",
                class_name="rounded-4",
            ),
        )
