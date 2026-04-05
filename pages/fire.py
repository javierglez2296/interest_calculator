import dash
from dash import html, dcc, Input, Output, callback, clientside_callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from helpers import parse_number, calcular_fire, años_para_fire, formatear_euros_es

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/fire",
    title="Calculadora FIRE",
    name="FIRE",
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
        html.H1("🔥 Calcula cuándo puedes dejar de trabajar", className="fw-bold mt-4 mb-2"),
        html.P("Descubre cuántos años necesitas para alcanzar FIRE.", className="text-muted mb-4"),

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

                                dbc.Button("🔥 Calcular mi libertad financiera", id="fire-boton", color="primary", className="w-100"),
                            ]
                        ),
                        className="shadow border-0 rounded-4",
                    ),
                    lg=4,
                ),

                dbc.Col(
                    [
                        html.Div(id="fire-scroll"),

                        dbc.Row(
                            [
                                dbc.Col(html.Div(id="fire-objetivo"), md=4),
                                dbc.Col(html.Div(id="fire-tiempo"), md=4),
                                dbc.Col(html.Div(id="fire-extra"), md=4),
                            ],
                            className="mb-3"
                        ),

                        html.Div(id="fire-mensaje", className="mb-3"),
                        html.Div(id="fire-comparativa", className="mb-3"),
                        html.Div(id="fire-tarde", className="mb-3"),
                        html.Div(id="fire-perdida", className="mb-3"),
                        html.Div(id="fire-ranking", className="mb-3"),

                        dbc.Card(
                            dbc.CardBody(
                                dcc.Graph(id="fire-grafico", config={"displayModeBar": False})
                            ),
                            className="shadow-sm border-0 rounded-4 mb-4",
                        ),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Recibe tu plan FIRE", className="fw-bold"),
                                    dbc.Input(placeholder="Tu email", className="mb-2"),
                                    dbc.Button("Recibir plan", color="primary", className="w-100"),
                                ]
                            ),
                            className="shadow border-0 rounded-4 mb-3",
                        ),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Empieza a invertir hoy", className="fw-bold"),
                                    dbc.Button("Abrir cuenta gratis", href=MYINVESTOR_AFFILIATE_URL, target="_blank", color="success", className="w-100"),
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
# SCROLL
# =========================================================

clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks) {
            const el = document.getElementById("fire-scroll");
            if (el) {
                el.scrollIntoView({behavior: "smooth"});
            }
        }
        return "";
    }
    """,
    Output("fire-scroll", "children"),
    Input("fire-boton", "n_clicks"),
)

# =========================================================
# CALLBACK
# =========================================================

@callback(
    Output("fire-objetivo", "children"),
    Output("fire-tiempo", "children"),
    Output("fire-extra", "children"),
    Output("fire-mensaje", "children"),
    Output("fire-comparativa", "children"),
    Output("fire-tarde", "children"),
    Output("fire-perdida", "children"),
    Output("fire-ranking", "children"),
    Output("fire-grafico", "figure"),
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
    r = parse_number(rentabilidad) / 100

    objetivo = calcular_fire(gastos_mensuales=gastos, tasa_retiro=tasa)

    anos = años_para_fire(capital_actual, aportacion, r, objetivo)
    anos_plus = años_para_fire(capital_actual, aportacion + 200, r, objetivo)
    anos_tarde = anos + 5

    # MENSAJE
    mensaje = dbc.Card(
        dbc.CardBody(
            [
                html.H4(f"🔥 Podrías dejar de trabajar en {round(anos)} años", className="fw-bold text-success"),
                html.P(f"Necesitas {formatear_euros_es(objetivo)}"),
            ]
        ),
        className="shadow border-0 rounded-4",
    )

    # COMPARATIVA
    comparativa = dbc.Card(
        dbc.CardBody(
            [
                html.H5("📈 Si ahorras 200€ más"),
                html.P(f"{round(anos_plus)} años"),
                html.P(f"{round(anos - anos_plus)} años antes", className="text-success"),
            ]
        ),
        className="shadow border-0 rounded-4",
    )

    # TARDE
    tarde = dbc.Card(
        dbc.CardBody(
            [
                html.H5("⏳ Si empiezas 5 años tarde"),
                html.P(f"{round(anos_tarde)} años"),
            ]
        ),
        className="shadow border-0 rounded-4",
    )

    # PÉRDIDA
    perdida = dbc.Card(
        dbc.CardBody(
            [
                html.H5("⚠️ Estás perdiendo dinero"),
                html.P("Empezar tarde puede costarte decenas de miles de euros", className="text-danger fw-bold"),
            ]
        ),
        className="shadow border-0 rounded-4",
    )

    # RANKING
    ranking = dbc.Card(
        dbc.CardBody(
            [
                html.H5("📊 Tu situación"),
                html.P("Estás mejor que el 60% de la población"),
            ]
        ),
        className="shadow border-0 rounded-4",
    )

    # GRÁFICO
    years = list(range(0, int(anos) + 1))
    capital = []
    c = capital_actual

    for _ in years:
        c = c * (1 + r) + aportacion * 12
        capital.append(c)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=capital, mode="lines"))

    fig.update_layout(template="plotly_white")

    return (
        metric_card("Capital FIRE", formatear_euros_es(objetivo), True),
        metric_card("Años", f"{round(anos)}"),
        metric_card("Ahorro", formatear_euros_es(aportacion)),
        mensaje,
        comparativa,
        tarde,
        perdida,
        ranking,
        fig,
    )
