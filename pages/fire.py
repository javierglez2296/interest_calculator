import dash
from dash import html, dcc, Input, Output, callback, clientside_callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from helpers import parse_number, calcular_fire, años_para_fire, formatear_euros_es

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/fire",
    title="Calculadora FIRE | Cuándo podrás alcanzar la libertad financiera",
    name="FIRE",
    description=(
        "Calcula cuánto dinero necesitas para alcanzar FIRE, "
        "cuántos años tardarías en lograrlo y cómo cambian tus resultados "
        "si aumentas tus aportaciones."
    ),
)

# =========================================================
# COMPONENTES
# =========================================================

def metric_card(title, value, subtitle=None, highlight=False, icon=None):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    [
                        html.Span(icon or "", className="me-2"),
                        html.Span(title, className="small text-muted fw-semibold"),
                    ],
                    className="mb-2"
                ),
                html.Div(
                    value,
                    className=f"fw-bold {'text-success' if highlight else ''}",
                    style={"fontSize": "1.65rem", "lineHeight": "1.1"},
                ),
                html.Div(
                    subtitle or "",
                    className="small text-muted mt-1"
                ),
            ]
        ),
        className="shadow-sm border-0 rounded-4 h-100",
    )


def info_card(title, body, icon=None, color_class="text-dark"):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    [
                        html.Span(icon or "", className="me-2"),
                        title
                    ],
                    className=f"fw-bold mb-2 {color_class}",
                ),
                html.Div(body, className="text-muted"),
            ]
        ),
        className="shadow-sm border-0 rounded-4 h-100",
    )


def input_block(label, input_id, value, placeholder=""):
    return html.Div(
        [
            dbc.Label(label, className="fw-semibold mb-2"),
            dbc.Input(
                id=input_id,
                value=value,
                type="text",
                placeholder=placeholder,
                className="mb-3 rounded-3",
                inputMode="numeric",
            ),
        ]
    )


# =========================================================
# LAYOUT
# =========================================================

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            "LIBERTAD FINANCIERA",
                            className="small fw-bold text-primary mb-2"
                        ),
                        html.H1(
                            "🔥 Calcula cuándo podrías alcanzar FIRE",
                            className="fw-bold display-6 mb-3",
                        ),
                        html.P(
                            "Descubre cuánto capital necesitas para vivir de tus inversiones, "
                            "cuántos años tardarías en conseguirlo y cómo acelerar el proceso.",
                            className="lead text-muted mb-4",
                            style={"maxWidth": "850px"},
                        ),
                    ],
                    width=12
                )
            ],
            className="mt-4"
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Introduce tus datos", className="fw-bold mb-3"),
                                html.P(
                                    "Usa cifras aproximadas. En segundos verás tu número FIRE y el tiempo estimado.",
                                    className="text-muted small mb-4",
                                ),

                                input_block("Gastos mensuales (€)", "fire-gastos", "1500", "Ej: 1500"),
                                input_block("Tasa de retiro (%)", "fire-tasa", "4", "Ej: 4"),
                                input_block("Capital actual (€)", "fire-capital-actual", "25000", "Ej: 25000"),
                                input_block("Aportación mensual (€)", "fire-aportacion", "600", "Ej: 600"),
                                input_block("Rentabilidad anual (%)", "fire-rentabilidad", "7", "Ej: 7"),

                                dbc.Button(
                                    "🔥 Calcular mi libertad financiera",
                                    id="fire-boton",
                                    color="primary",
                                    className="w-100 rounded-3 fw-semibold mt-2 py-2",
                                ),

                                html.Hr(className="my-4"),

                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.Div("¿Quieres empezar a invertir?", className="fw-bold mb-2"),
                                            html.P(
                                                "Si aún no has dado el paso, puedes abrir cuenta y empezar con una estrategia sencilla.",
                                                className="small text-muted mb-3",
                                            ),
                                            dbc.Button(
                                                "Abrir cuenta gratis",
                                                href=MYINVESTOR_AFFILIATE_URL,
                                                target="_blank",
                                                color="success",
                                                className="w-100 rounded-3 fw-semibold",
                                            ),
                                        ]
                                    ),
                                    className="border-0 bg-light rounded-4",
                                ),
                            ]
                        ),
                        className="shadow border-0 rounded-4 sticky-top",
                        style={"top": "90px"},
                    ),
                    lg=4,
                ),

                dbc.Col(
                    [
                        html.Div(id="fire-scroll"),

                        dbc.Row(
                            [
                                dbc.Col(html.Div(id="fire-objetivo"), md=4, className="mb-3"),
                                dbc.Col(html.Div(id="fire-tiempo"), md=4, className="mb-3"),
                                dbc.Col(html.Div(id="fire-extra"), md=4, className="mb-3"),
                            ],
                            className="mb-1"
                        ),

                        html.Div(id="fire-mensaje", className="mb-3"),

                        dbc.Row(
                            [
                                dbc.Col(html.Div(id="fire-comparativa"), md=6, className="mb-3"),
                                dbc.Col(html.Div(id="fire-tarde"), md=6, className="mb-3"),
                            ]
                        ),

                        dbc.Row(
                            [
                                dbc.Col(html.Div(id="fire-perdida"), md=6, className="mb-3"),
                                dbc.Col(html.Div(id="fire-ranking"), md=6, className="mb-3"),
                            ]
                        ),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Div(
                                        [
                                            html.H4("Evolución estimada de tu patrimonio", className="fw-bold mb-1"),
                                            html.P(
                                                "Simulación anual hasta alcanzar tu objetivo FIRE.",
                                                className="text-muted mb-0"
                                            ),
                                        ],
                                        className="mb-3"
                                    ),
                                    dcc.Graph(id="fire-grafico", config={"displayModeBar": False}),
                                ]
                            ),
                            className="shadow-sm border-0 rounded-4 mb-4",
                        ),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4("Recibe tu plan FIRE", className="fw-bold mb-2"),
                                    html.P(
                                        "Próximamente podrás recibir una guía práctica con pasos para acelerar tu libertad financiera.",
                                        className="text-muted mb-3",
                                    ),
                                    dbc.Input(
                                        placeholder="Tu email",
                                        className="mb-2 rounded-3",
                                        type="email",
                                    ),
                                    dbc.Button(
                                        "Recibir plan",
                                        color="primary",
                                        className="w-100 rounded-3 fw-semibold",
                                    ),
                                ]
                            ),
                            className="shadow border-0 rounded-4 mb-3",
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
                el.scrollIntoView({behavior: "smooth", block: "start"});
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
    gastos = max(parse_number(gastos), 0)
    tasa_pct = max(parse_number(tasa), 0.1)
    capital_actual = max(parse_number(capital_actual), 0)
    aportacion = max(parse_number(aportacion), 0)
    rentabilidad_pct = parse_number(rentabilidad)

    tasa = tasa_pct / 100
    r = rentabilidad_pct / 100

    objetivo = calcular_fire(gastos_mensuales=gastos, tasa_retiro=tasa)
    anos = max(años_para_fire(capital_actual, aportacion, r, objetivo), 0)

    aportacion_plus = aportacion + 200
    anos_plus = max(años_para_fire(capital_actual, aportacion_plus, r, objetivo), 0)

    # Escenario empezar 5 años tarde:
    # simulamos que mantienes todo igual pero pierdes 5 años de aportación e interés compuesto
    capital_despues_5 = capital_actual
    for _i in range(5):
        capital_despues_5 = capital_despues_5 * (1 + r) + aportacion * 12

    anos_desde_hoy_si_empezaras_tarde = 5 + max(
        años_para_fire(capital_actual, aportacion, r, objetivo),
        0
    )

    # coste aproximado de retrasar 5 años = diferencia entre capital que tendrías en 5 años
    # si empiezas hoy vs seguir en 0 progreso sobre el plan durante 5 años
    coste_retraso = max(capital_despues_5 - capital_actual, 0)

    # mensaje principal
    if anos <= 10:
        titular = f"🔥 Podrías alcanzar FIRE en unos {round(anos)} años"
        subtitular = "Vas por un camino muy sólido."
        color_class = "text-success"
    elif anos <= 20:
        titular = f"🔥 Podrías alcanzar FIRE en unos {round(anos)} años"
        subtitular = "Tu objetivo es realista si mantienes la constancia."
        color_class = "text-primary"
    else:
        titular = f"🔥 Podrías alcanzar FIRE en unos {round(anos)} años"
        subtitular = "Tu objetivo sigue siendo posible, pero acelerar el ahorro tendría mucho impacto."
        color_class = "text-warning"

    mensaje = dbc.Card(
        dbc.CardBody(
            [
                html.H3(titular, className=f"fw-bold mb-2 {color_class}"),
                html.P(
                    f"Con unos gastos mensuales de {formatear_euros_es(gastos)}, "
                    f"necesitarías aproximadamente {formatear_euros_es(objetivo)} "
                    f"para cubrir tu nivel de vida con una tasa de retiro del {tasa_pct:.1f}%.",
                    className="mb-0 text-muted",
                ),
                html.Div(subtitular, className="small mt-2 fw-semibold"),
            ]
        ),
        className="shadow border-0 rounded-4",
    )

    ahorro_extra_anos = max(anos - anos_plus, 0)

    comparativa = info_card(
        "Si ahorras 200€ más al mes",
        [
            html.Div(
                f"Podrías llegar en {round(anos_plus)} años en lugar de {round(anos)}.",
                className="mb-1",
            ),
            html.Div(
                f"Eso te adelantaría aproximadamente {round(ahorro_extra_anos)} años.",
                className="fw-semibold text-success",
            ),
        ],
        icon="📈",
    )

    tarde = info_card(
        "Si empiezas 5 años más tarde",
        [
            html.Div(
                f"Tu horizonte total podría irse a unos {round(anos_desde_hoy_si_empezaras_tarde)} años desde hoy.",
                className="mb-1",
            ),
            html.Div(
                "El interés compuesto premia mucho empezar pronto, incluso con cantidades modestas.",
                className="small",
            ),
        ],
        icon="⏳",
    )

    perdida = info_card(
        "Coste estimado de retrasar el plan",
        [
            html.Div(
                f"Esperar 5 años puede costarte alrededor de {formatear_euros_es(coste_retraso)} en patrimonio potencial acumulado.",
                className="mb-1 fw-semibold text-danger",
            ),
            html.Div(
                "No es una pérdida real en efectivo, sino una oportunidad perdida por no poner a trabajar antes tu capital.",
                className="small",
            ),
        ],
        icon="⚠️",
        color_class="text-danger",
    )

    if aportacion <= 300:
        consejo = "Tu mayor palanca probablemente es aumentar la aportación mensual."
    elif rentabilidad_pct < 5:
        consejo = "Tu simulación usa una rentabilidad conservadora; revisa si refleja bien tu estrategia real."
    else:
        consejo = "Tu combinación de ahorro y rentabilidad ya tiene buena base a largo plazo."

    ranking = info_card(
        "Lectura rápida de tu plan",
        [
            html.Div(consejo, className="mb-2"),
            html.Div(
                f"Hoy ahorras {formatear_euros_es(aportacion)} al mes con una hipótesis de rentabilidad del {rentabilidad_pct:.1f}% anual.",
                className="small",
            ),
        ],
        icon="🧭",
    )

    # gráfico
    years = list(range(0, int(round(anos)) + 1))
    capital = [capital_actual]
    c = capital_actual

    for _year in years[1:]:
        c = c * (1 + r) + aportacion * 12
        capital.append(c)

    objetivo_line = [objetivo] * len(years)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=years,
            y=capital,
            mode="lines",
            name="Patrimonio estimado",
            line=dict(width=4),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=years,
            y=objetivo_line,
            mode="lines",
            name="Objetivo FIRE",
            line=dict(dash="dash", width=2),
        )
    )

    fig.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=20, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        xaxis_title="Años",
        yaxis_title="Patrimonio (€)",
        hovermode="x unified",
    )

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(0,0,0,0.06)")

    return (
        metric_card(
            "Capital FIRE",
            formatear_euros_es(objetivo),
            "Patrimonio objetivo",
            True,
            "🎯",
        ),
        metric_card(
            "Tiempo estimado",
            f"{round(anos)} años",
            "Hasta alcanzar FIRE",
            False,
            "⏱️",
        ),
        metric_card(
            "Aportación mensual",
            formatear_euros_es(aportacion),
            "Tu ritmo actual",
            False,
            "💶",
        ),
        mensaje,
        comparativa,
        tarde,
        perdida,
        ranking,
        fig,
    )
