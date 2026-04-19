import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import requests

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
                                html.Div("✅", className="mb-3", style={"fontSize": "3rem", "lineHeight": "1"}),
                                html.H1(
                                    "Valida tu acceso premium",
                                    className="fw-bold mb-3",
                                    style={
                                        "color": "#0f172a",
                                        "fontSize": "clamp(2rem, 4vw, 3rem)",
                                        "lineHeight": "1.1",
                                        "letterSpacing": "-0.03em",
                                    },
                                ),
                                html.P(
                                    "Introduce el mismo email que usaste en Stripe. Si el pago está registrado, activaremos el premium en este navegador.",
                                    className="mb-4",
                                    style={
                                        "color": "#475467",
                                        "lineHeight": "1.75",
                                        "fontSize": "1.05rem",
                                        "maxWidth": "700px",
                                        "margin": "0 auto",
                                    },
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

                                html.Div(
                                    [
                                        dbc.Button(
                                            "Ir a hipoteca",
                                            href="/hipoteca",
                                            color="primary",
                                            className="rounded-pill fw-bold px-4 py-3 me-2 mb-2",
                                        ),
                                        dbc.Button(
                                            "Volver al inicio",
                                            href="/",
                                            color="light",
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
        ),
    ],
    fluid=True,
    className="py-5 px-4",
    style={"maxWidth": "1200px"},
)


@callback(
    Output("premium-access", "data", allow_duplicate=True),
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
            dbc.Alert("Introduce tu email para validar el premium.", color="warning", class_name="rounded-4"),
        )

    try:
        response = requests.post(
            "https://interescompuesto.app/api/check-premium",
            json={"email": email, "product_code": "hipoteca_pro"},
            timeout=8,
        )

        data = response.json()

        if response.ok and data.get("unlocked"):
            return (
                {"unlocked": True, "source": "server_validation", "email": email},
                dbc.Alert("✅ Premium activado correctamente en este navegador.", color="success", class_name="rounded-4"),
            )

        return (
            {"unlocked": False, "source": "server_validation", "email": email},
            dbc.Alert("No hemos encontrado una compra premium activa con ese email.", color="danger", class_name="rounded-4"),
        )

    except Exception:
        return (
            dash.no_update,
            dbc.Alert("Error validando el premium. Inténtalo de nuevo en unos segundos.", color="warning", class_name="rounded-4"),
        )
