import dash
from dash import html, dcc, Input, Output, callback, clientside_callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from helpers import parse_number, calcular_interes_compuesto, formatear_euros_es

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/calculadora",
    title="Calculadora de interés compuesto",
    name="Calculadora",
)

# =========================================================
# COMPONENTES
# =========================================================

def metric_card(title, value, highlight=False):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, className="text-muted small"),
                html.Div(
                    value,
                    className=f"fw-bold {'text-success' if highlight else ''}",
                    style={"fontSize": "1.6rem"},
                ),
            ]
        ),
        className="shadow-sm border-0 rounded-4 h-100",
    )

# =========================================================
# LAYOUT
# =========================================================

layout = dbc.Container(
    [
        html.H1(
            "💰 Calcula cuánto dinero puedes tener en el futuro",
            className="fw-bold mt-4 mb-2",
        ),
        html.P(
            "Introduce tus datos y descubre cómo el interés compuesto puede multiplicar tu dinero.",
            className="text-muted mb-4"
        ),

        dbc.Row(
            [
                # INPUTS
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Datos de inversión", className="fw-bold mb-3"),

                                dbc.Label("Capital inicial (€)"),
                                dbc.Input(id="ic-capital-inicial", value="10000", type="text", className="mb-3"),

                                dbc.Label("Aportación mensual (€)"),
                                dbc.Input(id="ic-aportacion", value="300", type="text", className="mb-3"),

                                dbc.Label("Años"),
                                dbc.Input(id="ic-anios", value="20", type="number", className="mb-3"),

                                dbc.Label("Rentabilidad (%)"),
                                dbc.Input(id="ic-rentabilidad", value="7", type="text", className="mb-3"),

                                dbc.Label("Inflación (%)"),
                                dbc.Input(id="ic-inflacion", value="2", type="text", className="mb-3"),

                                dbc.Label("Comisión (%)"),
                                dbc.Input(id="ic-comision", value="0.2", type="text", className="mb-3"),

                                dbc.Button(
                                    "💰 Calcular mi dinero futuro",
                                    id="ic-boton",
                                    color="primary",
                                    className="w-100 mt-2",
                                ),
                            ]
                        ),
                        className="shadow border-0 rounded-4",
                    ),
                    lg=4,
                ),

                # RESULTADOS
                dbc.Col(
                    [
                        html.Div(id="scroll-target"),

                        dbc.Row(
                            [
                                dbc.Col(html.Div(id="ic-resultado-final"), md=4, className="mb-3"),
                                dbc.Col(html.Div(id="ic-total-aportado"), md=4, className="mb-3"),
                                dbc.Col(html.Div(id="ic-ganancia"), md=4, className="mb-3"),
                            ]
                        ),

                        html.Div(id="ic-mensaje-emocional", className="mb-3"),

                        html.Div(id="ic-comparativa", className="mb-4"),

                        dbc.Card(
                            dbc.CardBody(
                                dcc.Graph(id="ic-grafico", config={"displayModeBar": False})
                            ),
                            className="shadow-sm border-0 rounded-4 mb-4",
                        ),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Empieza a invertir hoy", className="fw-bold"),
                                    html.P(
                                        "Para conseguir este resultado necesitas invertir. Puedes empezar con poco dinero.",
                                        className="text-muted"
                                    ),
                                    dbc.Button(
                                        "Abrir cuenta gratis",
                                        href=MYINVESTOR_AFFILIATE_URL,
                                        target="_blank",
                                        color="success",
                                        className="w-100"
                                    )
                                ]
                            ),
                            className="shadow border-0 rounded-4",
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

# =========================================================
# SCROLL AUTOMÁTICO
# =========================================================

clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks) {
            const el = document.getElementById("scroll-target");
            if (el) {
                el.scrollIntoView({behavior: "smooth"});
            }
        }
        return "";
    }
    """,
    Output("scroll-target", "children"),
    Input("ic-boton", "n_clicks"),
)

# =========================================================
# CALLBACK PRINCIPAL
# =========================================================

@callback(
    Output("ic-resultado-final", "children"),
    Output("ic-total-aportado", "children"),
    Output("ic-ganancia", "children"),
    Output("ic-grafico", "figure"),
    Output("ic-mensaje-emocional", "children"),
    Output("ic-comparativa", "children"),
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
            metric_card("Valor final", "0 €"),
            metric_card("Aportado", "0 €"),
            metric_card("Ganancia", "0 €"),
            fig,
            "",
            "",
        )

    anos = [x["año"] for x in evolucion]
    total = [x["total"] for x in evolucion]
    aportado = [x["aportado"] for x in evolucion]
    real = [x["real"] for x in evolucion]

    valor_final = total[-1]
    total_aportado = aportado[-1]
    ganancia = valor_final - total_aportado

    # COMPARATIVA +100€
    evolucion_plus = calcular_interes_compuesto(
        capital_inicial=capital_inicial,
        aportacion_mensual=aportacion + 100,
        años=anios,
        rentabilidad_anual=rentabilidad,
        inflacion=inflacion,
        comision=comision,
    )

    valor_plus = evolucion_plus[-1]["total"] if evolucion_plus else 0
    diferencia = valor_plus - valor_final

    # GRÁFICO
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=anos, y=aportado, mode="lines", name="Invertido"))
    fig.add_trace(go.Scatter(x=anos, y=total, mode="lines", name="Total"))
    fig.add_trace(go.Scatter(x=anos, y=real, mode="lines", name="Valor real"))

    fig.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis_title="Años",
        yaxis_title="€",
        legend_title="",
    )

    mensaje = html.Div(
        [
            html.H4(
                f"💰 Podrías tener {formatear_euros_es(valor_final)}",
                className="fw-bold text-success"
            ),
            html.P(
                f"Has invertido {formatear_euros_es(total_aportado)} y generado {formatear_euros_es(ganancia)} de beneficio.",
                className="text-muted"
            ),
        ],
        className="p-3 bg-light rounded-4",
    )

    comparativa = dbc.Card(
        dbc.CardBody(
            [
                html.H5("📈 Si inviertes 100€ más al mes", className="fw-bold"),
                html.P(f"Tendrías {formatear_euros_es(valor_plus)}"),
                html.P(
                    f"+{formatear_euros_es(diferencia)} extra",
                    className="text-success fw-bold"
                ),
            ]
        ),
        className="shadow border-0 rounded-4",
    )

    return (
        metric_card("Valor final", formatear_euros_es(valor_final), True),
        metric_card("Aportado", formatear_euros_es(total_aportado)),
        metric_card("Ganancia", formatear_euros_es(ganancia), True),
        fig,
        mensaje,
        comparativa,
    )
