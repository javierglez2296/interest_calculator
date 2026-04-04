import dash
from dash import html, Input, Output, callback
import dash_bootstrap_components as dbc

from helpers import parse_number, calcular_fire, años_para_fire, formatear_euros_es

dash.register_page(
    __name__,
    path="/fire",
    title="Calculadora FIRE",
    name="FIRE",
)

layout = dbc.Container(
    [
        html.H1("Calculadora FIRE", className="fw-bold mt-4 mb-3"),
        html.P(
            "Calcula cuánto capital necesitarías para cubrir tus gastos anuales.",
            className="text-muted mb-4"
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Label("Gastos mensuales (€)"),
                                dbc.Input(id="fire-gastos", value="1500", type="text", className="mb-3"),

                                dbc.Label("Tasa de retiro (%)"),
                                dbc.Input(id="fire-tasa", value="4", type="text", className="mb-3"),

                                dbc.Label("Capital actual (€)"),
                                dbc.Input(id="fire-capital-actual", value="25000", type="text", className="mb-3"),

                                dbc.Label("Aportación mensual (€)"),
                                dbc.Input(id="fire-aportacion", value="600", type="text", className="mb-3"),

                                dbc.Label("Rentabilidad anual (%)"),
                                dbc.Input(id="fire-rentabilidad", value="7", type="text", className="mb-3"),

                                dbc.Button("Calcular", id="fire-boton", color="primary", className="w-100"),
                            ]
                        ),
                        className="shadow-sm border-0 rounded-4",
                    ),
                    lg=4,
                ),
                dbc.Col(
                    [
                        html.Div(id="fire-objetivo", className="mb-3"),
                        html.Div(id="fire-tiempo", className="mb-3"),
                    ],
                    lg=8,
                ),
            ],
            className="gy-4",
        ),
    ],
    fluid=True,
    className="px-4 px-md-5 pb-5",
)

def metric_card(title, value):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, className="text-muted small"),
                html.Div(value, className="fw-bold fs-4"),
            ]
        ),
        className="shadow-sm border-0 rounded-4",
    )

@callback(
    Output("fire-objetivo", "children"),
    Output("fire-tiempo", "children"),
    Input("fire-boton", "n_clicks"),
    Input("fire-gastos", "value"),
    Input("fire-tasa", "value"),
    Input("fire-capital-actual", "value"),
    Input("fire-aportacion", "value"),
    Input("fire-rentabilidad", "value"),
)
def actualizar_fire(_, gastos, tasa, capital_actual, aportacion, rentabilidad):
    gastos = parse_number(gastos)
    tasa = parse_number(tasa) / 100
    capital_actual = parse_number(capital_actual)
    aportacion = parse_number(aportacion)
    rentabilidad = parse_number(rentabilidad) / 100

    if tasa <= 0:
        return metric_card("Capital objetivo", "Error"), metric_card("Tiempo estimado", "Error")

    objetivo = calcular_fire(gastos_mensuales=gastos, tasa_retiro=tasa)
    anos = años_para_fire(
        capital_actual=capital_actual,
        aportacion_mensual=aportacion,
        rentabilidad=rentabilidad,
        objetivo=objetivo,
    )

    if anos >= 1000:
        tiempo = "No alcanzable con estos datos"
    else:
        tiempo = f"{anos:.1f} años".replace(".", ",")

    return (
        metric_card("Capital objetivo FIRE", formatear_euros_es(objetivo)),
        metric_card("Tiempo estimado hasta FIRE", tiempo),
    )
