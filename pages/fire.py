import math
import dash
from dash import html, dcc, Input, Output, callback, clientside_callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from helpers import (
    parse_number,
    calcular_fire,
    años_para_fire,
    generar_curva_fire,
    capital_en_n_años,
    formatear_euros_es
)

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/fire",
    title="Calculadora FIRE | Libertad financiera",
    name="FIRE",
    description=(
        "Calcula cuánto dinero necesitas para alcanzar FIRE, "
        "cuántos años tardarías y cómo mejorar tu estrategia."
    ),
)

# =========================================================
# COMPONENTES
# =========================================================

def metric_card(title, value, subtitle=None, highlight=False, icon=None):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(f"{icon or ''} {title}", className="small text-muted fw-semibold mb-1"),
                html.Div(
                    value,
                    className=f"fw-bold {'text-success' if highlight else ''}",
                    style={"fontSize": "1.7rem", "lineHeight": "1.1"},
                ),
                html.Div(subtitle or "", className="small text-muted mt-1"),
            ]
        ),
        className="shadow-sm border-0 rounded-4 h-100",
    )


def input_block(label, input_id, value):
    return html.Div(
        [
            dbc.Label(label, className="fw-semibold"),
            dbc.Input(
                id=input_id,
                value=value,
                type="text",
                className="mb-3 rounded-3",
                inputMode="numeric",
            ),
        ]
    )


def simple_info_card(title, children, icon=None):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H5(f"{icon or ''} {title}", className="fw-bold mb-2"),
                children,
            ]
        ),
        className="shadow-sm border-0 rounded-4 h-100",
    )


# =========================================================
# LAYOUT
# =========================================================

layout = dbc.Container(
    [
        html.H1("🔥 Calcula cuándo puedes alcanzar FIRE", className="fw-bold mt-4"),
        html.P(
            "Simula cuánto necesitas para vivir de tus inversiones y cuánto tiempo tardarías en conseguirlo.",
            className="text-muted mb-4",
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Tus datos", className="fw-bold mb-3"),
                                input_block("Gastos mensuales (€)", "fire-gastos", "1500"),
                                input_block("Tasa de retiro (%)", "fire-tasa", "4"),
                                input_block("Capital actual (€)", "fire-capital-actual", "25000"),
                                input_block("Aportación mensual (€)", "fire-aportacion", "600"),
                                input_block("Rentabilidad anual (%)", "fire-rentabilidad", "7"),

                                dbc.Button(
                                    "🔥 Calcular FIRE",
                                    id="fire-boton",
                                    color="primary",
                                    className="w-100 mt-2 rounded-3 fw-semibold",
                                ),

                                html.Hr(className="my-4"),

                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.Div("Empieza a invertir hoy", className="fw-bold mb-2"),
                                            html.P(
                                                "Una cartera simple y constante puede marcar una diferencia enorme a 10, 20 o 30 años.",
                                                className="small text-muted mb-3",
                                            ),
                                            dbc.Button(
                                                "Abrir cuenta gratis",
                                                id="fire-cta-top",
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
                                dbc.Col(html.Div(id="fire-aportacion"), md=4, className="mb-3"),
                            ],
                            className="mb-1"
                        ),

                        html.Div(id="fire-mensaje", className="mb-3"),

                        dbc.Row(
                            [
                                dbc.Col(html.Div(id="fire-comparativa"), md=6, className="mb-3"),
                                dbc.Col(html.Div(id="fire-tarde"), md=6, className="mb-3"),
                            ],
                            className="mb-3"
                        ),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4("Evolución estimada de tu patrimonio", className="fw-bold mb-1"),
                                    html.P(
                                        "Simulación anual hasta alcanzar tu objetivo FIRE.",
                                        className="text-muted mb-3",
                                    ),
                                    dcc.Graph(id="fire-grafico", config={"displayModeBar": False}),
                                ]
                            ),
                            className="shadow-sm border-0 rounded-4 mb-4",
                        ),

                        html.Div(id="fire-estrategia", className="mb-4"),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4("Recibe tu plan FIRE", className="fw-bold mb-2"),
                                    html.P(
                                        "Próximamente podrás recibir una guía práctica para acelerar tu libertad financiera.",
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

        html.Div(id="fire-cta-top-tracker", style={"display": "none"}),
        html.Div(id="fire-cta-bottom-tracker", style={"display": "none"}),
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
# TRACKING ANALYTICS
# =========================================================

clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks) {
            if (window.gtag) {
                window.gtag('event', 'click_fire_cta_top', {
                    event_category: 'affiliate',
                    event_label: 'myinvestor_fire_top',
                    value: 1
                });
            }
        }
        return "";
    }
    """,
    Output("fire-cta-top-tracker", "children"),
    Input("fire-cta-top", "n_clicks"),
)

clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks) {
            if (window.gtag) {
                window.gtag('event', 'click_fire_cta_bottom', {
                    event_category: 'affiliate',
                    event_label: 'myinvestor_fire_bottom',
                    value: 1
                });
            }
        }
        return "";
    }
    """,
    Output("fire-cta-bottom-tracker", "children"),
    Input("fire-cta-bottom", "n_clicks"),
)

# =========================================================
# CALLBACK
# =========================================================

@callback(
    Output("fire-objetivo", "children"),
    Output("fire-tiempo", "children"),
    Output("fire-aportacion", "children"),
    Output("fire-mensaje", "children"),
    Output("fire-comparativa", "children"),
    Output("fire-tarde", "children"),
    Output("fire-grafico", "figure"),
    Output("fire-estrategia", "children"),
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

    objetivo = calcular_fire(gastos, tasa)
    anos = años_para_fire(capital_actual, aportacion, r, objetivo)
    anos_plus = años_para_fire(capital_actual, aportacion + 200, r, objetivo)

    if math.isinf(anos):
        anos_texto = "No alcanzable con estos datos"
    else:
        anos_texto = f"{round(anos)} años"

    if math.isinf(anos):
        mensaje_titulo = "⚠️ Con esta combinación, FIRE no parece alcanzable"
        mensaje_texto = (
            "Con tu capital, aportación y rentabilidad estimada actuales, tardarías demasiado en alcanzar el objetivo. "
            "La forma más potente de mejorar el resultado suele ser aumentar la aportación mensual o reducir gastos futuros."
        )
        mensaje_color = "text-warning"
    else:
        mensaje_titulo = f"🔥 Podrías alcanzar FIRE en aproximadamente {round(anos)} años"
        mensaje_texto = (
            f"Para cubrir unos gastos mensuales de {formatear_euros_es(gastos)}, "
            f"necesitarías alrededor de {formatear_euros_es(objetivo)}."
        )
        mensaje_color = "text-success"

    mensaje = dbc.Card(
        dbc.CardBody(
            [
                html.H4(mensaje_titulo, className=f"fw-bold {mensaje_color}"),
                html.P(mensaje_texto, className="mb-0 text-muted"),
            ]
        ),
        className="shadow border-0 rounded-4",
    )

    if not math.isinf(anos) and not math.isinf(anos_plus):
        mejora_anos = max(round(anos - anos_plus), 0)
        comparativa_texto = [
            html.P(
                f"Si aumentas tu aportación a {formatear_euros_es(aportacion + 200)} al mes, "
                f"podrías llegar en unos {round(anos_plus)} años.",
                className="mb-2",
            ),
            html.P(f"Eso supone aproximadamente {mejora_anos} años antes.", className="text-success fw-bold mb-0"),
        ]
    else:
        comparativa_texto = [
            html.P(
                "Subir la aportación mensual sigue siendo la palanca más fuerte para acercarte a FIRE.",
                className="mb-0",
            )
        ]

    comparativa = simple_info_card(
        "Si ahorras 200€ más al mes",
        comparativa_texto,
        "📈"
    )

    capital_5 = capital_en_n_años(capital_actual, aportacion, r, 5)
    coste_retraso = max(capital_5 - capital_actual, 0)

    tarde = simple_info_card(
        "El coste de esperar 5 años",
        [
            html.P(
                f"Retrasar tu plan puede suponer renunciar a unos {formatear_euros_es(coste_retraso)} de patrimonio potencial acumulado.",
                className="mb-2",
            ),
            html.P(
                "No es dinero perdido directamente, pero sí tiempo que el interés compuesto deja de trabajar a tu favor.",
                className="text-muted small mb-0",
            ),
        ],
        "⏳"
    )

    years, capital = generar_curva_fire(capital_actual, aportacion, r, objetivo, 60)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=years,
            y=capital,
            mode="lines",
            name="Capital estimado",
            line=dict(width=4),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years,
            y=[objetivo] * len(years),
            mode="lines",
            name="Objetivo FIRE",
            line=dict(dash="dash", width=2),
        )
    )

    fig.update_layout(
        template="plotly_white",
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_title="Años",
        yaxis_title="Patrimonio (€)",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(0,0,0,0.06)")

    if math.isinf(anos):
        diagnostico = "Ahora mismo tu prioridad no debería ser optimizar un 0,5% de rentabilidad extra, sino aumentar capacidad de ahorro."
        accion_1 = "Revisar tus gastos fijos y elevar el margen mensual."
        accion_2 = "Empezar cuanto antes con una rutina de inversión constante."
        accion_3 = "Usar una cartera sencilla para no quedarte paralizado."
    elif anos <= 10:
        diagnostico = "Tu plan ya tiene muy buena base. El foco ahora es mantener la constancia y evitar errores."
        accion_1 = "No interrumpir aportaciones cuando caiga el mercado."
        accion_2 = "Mantener comisiones bajas y estrategia simple."
        accion_3 = "Aumentar aportación cuando suban tus ingresos."
    elif anos <= 20:
        diagnostico = "Estás en una zona muy razonable. Un pequeño aumento en aportación puede recortar varios años."
        accion_1 = "Intentar subir tu aportación mensual de forma progresiva."
        accion_2 = "No sobrecomplicar la cartera."
        accion_3 = "Automatizar inversión para mantener disciplina."
    else:
        diagnostico = "Tu objetivo es viable, pero todavía dependes mucho de aumentar el ahorro mensual."
        accion_1 = "Priorizar una tasa de ahorro más alta."
        accion_2 = "Evitar estar demasiado tiempo en liquidez sin invertir."
        accion_3 = "Revisar si tus gastos objetivo en FIRE son realistas."

    estrategia = dbc.Card(
        dbc.CardBody(
            [
                html.Div("PLAN RECOMENDADO", className="small fw-bold text-primary mb-2"),
                html.H4("La estrategia que más puede acercarte a FIRE", className="fw-bold mb-3"),
                html.P(diagnostico, className="text-muted mb-4"),

                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div("1", className="fw-bold fs-4 mb-2 text-primary"),
                                        html.Div(accion_1, className="fw-semibold"),
                                    ]
                                ),
                                className="border-0 bg-light rounded-4 h-100",
                            ),
                            md=4,
                            className="mb-3",
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div("2", className="fw-bold fs-4 mb-2 text-primary"),
                                        html.Div(accion_2, className="fw-semibold"),
                                    ]
                                ),
                                className="border-0 bg-light rounded-4 h-100",
                            ),
                            md=4,
                            className="mb-3",
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div("3", className="fw-bold fs-4 mb-2 text-primary"),
                                        html.Div(accion_3, className="fw-semibold"),
                                    ]
                                ),
                                className="border-0 bg-light rounded-4 h-100",
                            ),
                            md=4,
                            className="mb-3",
                        ),
                    ],
                    className="mb-2"
                ),

                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5("Empieza antes de que pase otro año", className="fw-bold mb-2"),
                            html.P(
                                "La mayoría de personas no fracasan por elegir mal un fondo. "
                                "Fracasan por tardar demasiado en empezar o por no mantener constancia.",
                                className="text-muted mb-3",
                            ),
                            html.Ul(
                                [
                                    html.Li("Sin papeleo complejo ni estrategia rara."),
                                    html.Li("Ideal para empezar con una cartera sencilla."),
                                    html.Li("Cuanto antes empieces, antes trabaja el interés compuesto."),
                                ],
                                className="text-muted mb-3",
                            ),
                            dbc.Button(
                                "Abrir cuenta y empezar a invertir",
                                id="fire-cta-bottom",
                                href=MYINVESTOR_AFFILIATE_URL,
                                target="_blank",
                                color="success",
                                className="w-100 rounded-3 fw-semibold py-2",
                            ),
                            html.Div(
                                "Invertir conlleva riesgos. Este contenido es informativo y no constituye asesoramiento financiero personalizado.",
                                className="small text-muted mt-3",
                            ),
                        ]
                    ),
                    className="border-0 rounded-4 bg-light",
                ),
            ]
        ),
        className="shadow border-0 rounded-4",
    )

    return (
        metric_card("Capital FIRE", formatear_euros_es(objetivo), "Objetivo estimado", True, "🎯"),
        metric_card("Tiempo estimado", anos_texto, "Hasta alcanzar FIRE", False, "⏱️"),
        metric_card("Aportación mensual", formatear_euros_es(aportacion), "Tu ritmo actual", False, "💰"),
        mensaje,
        comparativa,
        tarde,
        fig,
        estrategia,
    )
