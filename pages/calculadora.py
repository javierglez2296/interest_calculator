import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from helpers import parse_number, calcular_interes_compuesto, formatear_euros_es

dash.register_page(
    __name__,
    path="/calculadora",
    title="Calculadora de interés compuesto",
    name="Calculadora",
)

layout = dbc.Container(
    [
        html.H1("Calculadora de interés compuesto", className="fw-bold mt-4 mb-3"),
        html.P(
            "Simula cómo puede evolucionar tu patrimonio con aportaciones periódicas.",
            className="text-muted mb-4"
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Label("Capital inicial (€)"),
                                dbc.Input(id="ic-capital-inicial", value="10000", type="text", className="mb-3"),

                                dbc.Label("Aportación mensual (€)"),
                                dbc.Input(id="ic-aportacion", value="300", type="text", className="mb-3"),

                                dbc.Label("Años"),
                                dbc.Input(id="ic-anios", value="20", type="number", className="mb-3"),

                                dbc.Label("Rentabilidad anual (%)"),
                                dbc.Input(id="ic-rentabilidad", value="7", type="text", className="mb-3"),

                                dbc.Label("Inflación anual (%)"),
                                dbc.Input(id="ic-inflacion", value="2", type="text", className="mb-3"),

                                dbc.Label("Comisión anual (%)"),
                                dbc.Input(id="ic-comision", value="0.2", type="text", className="mb-3"),

                                dbc.Button("Calcular", id="ic-boton", color="primary", className="w-100"),
                            ]
                        ),
                        className="shadow-sm border-0 rounded-4",
                    ),
                    lg=4,
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Div(id="ic-resultado-final"), md=4, className="mb-3"),
                                dbc.Col(html.Div(id="ic-total-aportado"), md=4, className="mb-3"),
                                dbc.Col(html.Div(id="ic-ganancia"), md=4, className="mb-3"),
                            ]
                        ),
                        dbc.Card(
                            dbc.CardBody(
                                dcc.Graph(id="ic-grafico", config={"displayModeBar": False})
                            ),
                            className="shadow-sm border-0 rounded-4",
                        ),
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
        className="shadow-sm border-0 rounded-4 h-100",
    )

@callback(
    Output("ic-resultado-final", "children"),
    Output("ic-total-aportado", "children"),
    Output("ic-ganancia", "children"),
    Output("ic-grafico", "figure"),
    Input("ic-boton", "n_clicks"),
    Input("ic-capital-inicial", "value"),
    Input("ic-aportacion", "value"),
    Input("ic-anios", "value"),
    Input("ic-rentabilidad", "value"),
    Input("ic-inflacion", "value"),
    Input("ic-comision", "value"),
)
def actualizar_calculadora(_, capital_inicial, aportacion, anios, rentabilidad, inflacion, comision):
    capital_inicial = parse_number(capital_inicial)
    aportacion = parse_number(aportacion)
    anios = int(anios or 0)
    rentabilidad = parse_number(rentabilidad) / 100
    inflacion = parse_number(inflacion) / 100
    comision = parse_number(comision) / 100

    evolucion = calcular_interes_compuesto(
        capital_inicial=capital_inicial,
        aportacion_mensual=aportacion,
        años=anios,
        rentabilidad_anual=rentabilidad,
        inflacion=inflacion,
        comision=comision,
    )

    if not evolucion:
        fig = go.Figure()
        fig.update_layout(template="plotly_white")
        return (
            metric_card("Valor final", "0,00 €"),
            metric_card("Total aportado", "0,00 €"),
            metric_card("Ganancia", "0,00 €"),
            fig,
        )

    anos = [x["año"] for x in evolucion]
    total = [x["total"] for x in evolucion]
    aportado = [x["aportado"] for x in evolucion]
    real = [x["real"] for x in evolucion]

    valor_final = total[-1]
    total_aportado = aportado[-1]
    ganancia = valor_final - total_aportado

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=anos, y=aportado, mode="lines", name="Capital aportado"))
    fig.add_trace(go.Scatter(x=anos, y=total, mode="lines", name="Valor total"))
    fig.add_trace(go.Scatter(x=anos, y=real, mode="lines", name="Valor real"))

    fig.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Años",
        yaxis_title="Euros",
        legend_title="",
    )

    return (
        metric_card("Valor final", formatear_euros_es(valor_final)),
        metric_card("Total aportado", formatear_euros_es(total_aportado)),
        metric_card("Ganancia", formatear_euros_es(ganancia)),
        fig,
    )
