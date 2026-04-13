import dash_bootstrap_components as dbc
from dash import html

# =========================================================
# CONFIG
# =========================================================
PREMIUM_PRICE = "9€"
STRIPE_PAYMENT_LINK = "https://buy.stripe.com/cNi00kaRr1Ri8sU0tr1VK00"


# =========================================================
# HELPERS
# =========================================================
def is_premium_unlocked(access_data):
    """
    Comprueba si el usuario tiene premium activo
    """
    return bool((access_data or {}).get("unlocked"))


def get_premium_badges():
    return [
        "Monte Carlo",
        "Guardar simulaciones",
        "Exportar CSV",
        "Comparativas avanzadas",
        "Todas las calculadoras premium",
    ]


# =========================================================
# CTA PRINCIPAL
# =========================================================
def premium_cta_card(
    price=PREMIUM_PRICE,
    payment_link=STRIPE_PAYMENT_LINK,
    title=None,
    subtitle=None,
):
    title = title or f"Desbloquea todas las calculadoras por {price}"
    subtitle = subtitle or (
        "Pago único. Sin suscripción. Acceso inmediato a todas las funciones premium."
    )

    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    "Premium",
                    className="text-uppercase fw-bold mb-2",
                    style={
                        "letterSpacing": "0.08em",
                        "color": "#667085",
                        "fontSize": "0.85rem",
                    },
                ),
                html.H4(
                    title,
                    className="fw-bold mb-2",
                    style={"color": "#0f172a"},
                ),
                html.P(
                    subtitle,
                    className="mb-3",
                    style={"color": "#475467", "lineHeight": "1.7"},
                ),
                html.Div(
                    [
                        html.Div(f"✔ {badge}", className="mb-2")
                        for badge in get_premium_badges()
                    ],
                    style={
                        "color": "#344054",
                        "fontWeight": "600",
                    },
                    className="mb-3",
                ),
                dbc.Button(
                    f"Desbloquear todo por {price}",
                    href=payment_link,
                    target="_blank",
                    color="dark",
                    className="w-100 rounded-pill fw-bold py-3",
                ),
                html.Div(
                    "Pago único · Sin suscripción · Acceso inmediato",
                    className="mt-3 text-center",
                    style={
                        "fontSize": "0.9rem",
                        "color": "#667085",
                        "fontWeight": "600",
                    },
                ),
            ]
        ),
        className="border-0 rounded-4",
        style={
            "background": "linear-gradient(135deg, #ffffff 0%, #f8fafc 100%)",
            "boxShadow": "0 14px 36px rgba(16, 24, 40, 0.06)",
        },
    )


# =========================================================
# ESTADO BLOQUEADO
# =========================================================
def premium_locked_note(feature_name="esta función"):
    return dbc.Alert(
        f"{feature_name.capitalize()} está disponible en la versión premium.",
        color="warning",
        className="rounded-4 border-0",
    )


# =========================================================
# ESTADO ACTIVO
# =========================================================
def premium_active_alert():
    return dbc.Alert(
        "Premium activo. Ya puedes usar todas las funciones desbloqueadas.",
        color="success",
        className="rounded-4 border-0",
    )


def premium_success_card():
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    "Acceso activado",
                    className="text-uppercase fw-bold mb-2",
                    style={
                        "letterSpacing": "0.08em",
                        "color": "#198754",
                        "fontSize": "0.85rem",
                    },
                ),
                html.H4(
                    "Ya tienes desbloqueadas todas las calculadoras premium",
                    className="fw-bold mb-2",
                    style={"color": "#0f172a"},
                ),
                html.P(
                    "Ya puedes usar Monte Carlo, guardar simulaciones, exportar resultados y acceder a futuras funciones premium.",
                    className="mb-0",
                    style={"color": "#475467", "lineHeight": "1.7"},
                ),
            ]
        ),
        className="border-0 rounded-4",
        style={
            "background": "linear-gradient(135deg, #f7fcf9 0%, #ffffff 100%)",
            "boxShadow": "0 14px 36px rgba(16, 24, 40, 0.06)",
        },
    )
