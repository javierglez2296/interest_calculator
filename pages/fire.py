import math
import dash
from dash import html, dcc, Input, Output, State, callback, clientside_callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from helpers import (
    parse_number,
    calcular_fire,
    años_para_fire,
    generar_curva_fire,
    capital_en_n_años,
    formatear_euros_es,
)

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/fire",
    title="Calculadora FIRE | Cuándo podrás alcanzar la libertad financiera",
    name="FIRE",
    description=(
        "Calcula cuánto dinero necesitas para alcanzar FIRE, "
        "cuántos años tardarías y cómo acelerar tu libertad financiera."
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
                    className="mb-2",
                ),
                html.Div(
                    value,
                    className=f"fw-bold {'text-success' if highlight else ''}",
                    style={"fontSize": "1.75rem", "lineHeight": "1.1"},
                ),
                html.Div(subtitle or "", className="small text-muted mt-1"),
            ]
        ),
        className="shadow-sm border-0 rounded-4 h-100",
    )


def input_block(label, input_id, value, help_text=None):
    return html.Div(
        [
            dbc.Label(label, className="fw-semibold mb-2"),
            dbc.Input(
                id=input_id,
                value=value,
                type="text",
                className="mb-1 rounded-3",
                inputMode="numeric",
            ),
            html.Div(help_text or "", className="small text-muted mb-3"),
        ]
    )


def info_card(title, body, icon=None, emphasis_class="text-dark"):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H5(
                    [
                        html.Span(icon or "", className="me-2"),
                        title,
                    ],
                    className=f"fw-bold mb-2 {emphasis_class}",
                ),
                body,
            ]
        ),
        className="shadow-sm border-0 rounded-4 h-100",
    )


def badge(text, color="primary"):
    return html.Div(
        text,
        className=f"small fw-bold text-{color} mb-2",
        style={"letterSpacing": "0.04em"},
    )


# =========================================================
# LAYOUT
# =========================================================

layout = dbc.Container(
    [
        # HERO
        dbc.Row(
            [
                dbc.Col(
                    [
                        badge("LIBERTAD FINANCIERA", "primary"),
                        html.H1(
                            "🔥 Calcula cuándo podrías alcanzar FIRE",
                            className="fw-bold display-6 mb-3",
                        ),
                        html.P(
                            "Descubre cuánto capital necesitas para vivir de tus inversiones, "
                            "cuántos años tardarías en lograrlo y qué palancas tienen más impacto.",
                            className="lead text-muted mb-0",
                            style={"maxWidth": "900px"},
                        ),
                    ],
                    width=12,
                )
            ],
            className="mt-4 mb-4",
        ),

        dbc.Row(
            [
                # =========================================================
                # COLUMNA IZQUIERDA
                # =========================================================
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Tus datos", className="fw-bold mb-3"),
                                html.P(
                                    "Usa cifras aproximadas. En segundos verás tu número FIRE y el tiempo estimado.",
                                    className="text-muted small mb-4",
                                ),

                                input_block(
                                    "Gastos mensuales (€)",
                                    "fire-gastos",
                                    "1500",
                                    "Tu nivel de gasto mensual objetivo.",
                                ),
                                input_block(
                                    "Tasa de retiro (%)",
                                    "fire-tasa",
                                    "4",
                                    "La regla clásica suele usar 4%, aunque depende del caso.",
                                ),
                                input_block(
                                    "Capital actual (€)",
                                    "fire-capital-actual",
                                    "25000",
                                    "Todo lo que ya tienes invertido o reservado para este objetivo.",
                                ),
                                input_block(
                                    "Aportación mensual (€)",
                                    "fire-aportacion",
                                    "600",
                                    "Lo que puedes invertir cada mes.",
                                ),
                                input_block(
                                    "Rentabilidad anual (%)",
                                    "fire-rentabilidad",
                                    "7",
                                    "Estimación media anual de tu cartera a largo plazo.",
                                ),

                                dbc.Button(
                                    "🔥 Calcular mi plan FIRE",
                                    id="fire-boton",
                                    color="primary",
                                    className="w-100 rounded-3 fw-semibold py-2 mt-2",
                                ),

                                html.Hr(className="my-4"),

                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.Div("Empieza a invertir hoy", className="fw-bold mb-2"),
                                            html.P(
                                                "Una estrategia sencilla y constante puede marcar una diferencia enorme a 10, 20 o 30 años.",
                                                className="small text-muted mb-3",
                                            ),
                                            html.Ul(
                                                [
                                                    html.Li("Sin complicarte con productos raros."),
                                                    html.Li("Ideal para empezar con pequeñas cantidades."),
                                                    html.Li("Cuanto antes empieces, antes trabaja el interés compuesto."),
                                                ],
                                                className="small text-muted mb-3 ps-3",
                                            ),
                                            dbc.Button(
                                                "Empezar a invertir",
                                                id="fire-cta-top",
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

                # =========================================================
                # COLUMNA DERECHA
                # =========================================================
                dbc.Col(
                    [
                        html.Div(id="fire-scroll"),

                        dbc.Row(
                            [
                                dbc.Col(html.Div(id="fire-objetivo"), md=4, className="mb-3"),
                                dbc.Col(html.Div(id="fire-tiempo"), md=4, className="mb-3"),
                                dbc.Col(html.Div(id="fire-aportacion-card"), md=4, className="mb-3"),
                            ],
                            className="mb-1",
                        ),

                        html.Div(id="fire-mensaje", className="mb-3"),

                        dbc.Row(
                            [
                                dbc.Col(html.Div(id="fire-comparativa"), md=6, className="mb-3"),
                                dbc.Col(html.Div(id="fire-tarde"), md=6, className="mb-3"),
                            ],
                            className="mb-1",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(html.Div(id="fire-potencia"), md=6, className="mb-3"),
                                dbc.Col(html.Div(id="fire-diagnostico"), md=6, className="mb-3"),
                            ],
                            className="mb-3",
                        ),

                        # CTA INTERMEDIO
                        html.Div(id="fire-cta-intermedio", className="mb-4"),

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
                                    html.H4("Recibe mejoras y nuevas calculadoras", className="fw-bold mb-2"),
                                    html.P(
                                        "Más adelante podrás recibir una guía práctica para acelerar tu libertad financiera.",
                                        className="text-muted mb-3",
                                    ),
                                    dbc.Input(
                                        placeholder="Tu email",
                                        className="mb-2 rounded-3",
                                        type="email",
                                    ),
                                    dbc.Button(
                                        "Quiero recibir novedades",
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

        # trackers
        html.Div(id="fire-cta-top-tracker", style={"display": "none"}),
        html.Div(id="fire-cta-bottom-tracker", style={"display": "none"}),
        html.Div(id="fire-cta-middle-tracker", style={"display": "none"}),

        # sticky mobile CTA
        html.Div(
            dbc.Button(
                "Empezar a invertir",
                id="fire-cta-mobile",
                color="success",
                className="w-100 fw-bold rounded-3",
            ),
            className="d-md-none",
            style={
                "position": "fixed",
                "left": "12px",
                "right": "12px",
                "bottom": "12px",
                "zIndex": "1050",
                "paddingBottom": "max(0px, env(safe-area-inset-bottom))",
            },
        ),
        html.Div(id="fire-cta-mobile-tracker", style={"display": "none"}),
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
# TRACKING + APERTURA ENLACES
# =========================================================

clientside_callback(
    f"""
    function(n_clicks) {{
        if (n_clicks) {{
            if (window.gtag) {{
                window.gtag('event', 'click_fire_cta_top', {{
                    event_category: 'affiliate',
                    event_label: 'myinvestor_fire_top',
                    value: 1
                }});
            }}
            window.open("{MYINVESTOR_AFFILIATE_URL}", "_blank");
        }}
        return "";
    }}
    """,
    Output("fire-cta-top-tracker", "children"),
    Input("fire-cta-top", "n_clicks"),
)

clientside_callback(
    f"""
    function(n_clicks) {{
        if (n_clicks) {{
            if (window.gtag) {{
                window.gtag('event', 'click_fire_cta_bottom', {{
                    event_category: 'affiliate',
                    event_label: 'myinvestor_fire_bottom',
                    value: 1
                }});
            }}
            window.open("{MYINVESTOR_AFFILIATE_URL}", "_blank");
        }}
        return "";
    }}
    """,
    Output("fire-cta-bottom-tracker", "children"),
    Input("fire-cta-bottom", "n_clicks"),
)

clientside_callback(
    f"""
    function(n_clicks) {{
        if (n_clicks) {{
            if (window.gtag) {{
                window.gtag('event', 'click_fire_cta_middle', {{
                    event_category: 'affiliate',
                    event_label: 'myinvestor_fire_middle',
                    value: 1
                }});
            }}
            window.open("{MYINVESTOR_AFFILIATE_URL}", "_blank");
        }}
        return "";
    }}
    """,
    Output("fire-cta-middle-tracker", "children"),
    Input("fire-cta-middle", "n_clicks"),
)

clientside_callback(
    f"""
    function(n_clicks) {{
        if (n_clicks) {{
            if (window.gtag) {{
                window.gtag('event', 'click_fire_cta_mobile', {{
                    event_category: 'affiliate',
                    event_label: 'myinvestor_fire_mobile',
                    value: 1
                }});
            }}
            window.open("{MYINVESTOR_AFFILIATE_URL}", "_blank");
        }}
        return "";
    }}
    """,
    Output("fire-cta-mobile-tracker", "children"),
    Input("fire-cta-mobile", "n_clicks"),
)

# =========================================================
# CALLBACK PRINCIPAL
# =========================================================

@callback(
    Output("fire-objetivo", "children"),
    Output("fire-tiempo", "children"),
    Output("fire-aportacion-card", "children"),
    Output("fire-mensaje", "children"),
    Output("fire-comparativa", "children"),
    Output("fire-tarde", "children"),
    Output("fire-potencia", "children"),
    Output("fire-diagnostico", "children"),
    Output("fire-cta-intermedio", "children"),
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
    # -----------------------------------------------------
    # sanitización
    # -----------------------------------------------------
    gastos = max(parse_number(gastos), 0)
    tasa_pct = max(parse_number(tasa), 0.1)
    capital_actual = max(parse_number(capital_actual), 0)
    aportacion = max(parse_number(aportacion), 0)
    rentabilidad_pct = parse_number(rentabilidad)

    # límites razonables visuales
    if rentabilidad_pct < -99:
        rentabilidad_pct = -99
    if rentabilidad_pct > 50:
        rentabilidad_pct = 50

    tasa = tasa_pct / 100
    r = rentabilidad_pct / 100

    objetivo = calcular_fire(gastos, tasa)
    anos = años_para_fire(capital_actual, aportacion, r, objetivo)
    anos_plus = años_para_fire(capital_actual, aportacion + 200, r, objetivo)

    # -----------------------------------------------------
    # métricas principales
    # -----------------------------------------------------
    if math.isinf(anos):
        anos_texto = "No alcanzable"
        anos_num = None
    else:
        anos_texto = f"{round(anos)} años"
        anos_num = round(anos)

    # -----------------------------------------------------
    # mensaje principal
    # -----------------------------------------------------
    if math.isinf(anos):
        mensaje_titulo = "⚠️ Con esta combinación, FIRE no parece alcanzable"
        mensaje_texto = (
            "Con tu capital, aportación y rentabilidad estimada actuales, tardarías demasiado en alcanzar el objetivo. "
            "La palanca más potente suele ser aumentar la aportación mensual o ajustar el gasto objetivo."
        )
        mensaje_color = "text-warning"
    elif anos <= 10:
        mensaje_titulo = f"🔥 Podrías alcanzar FIRE en aproximadamente {anos_num} años"
        mensaje_texto = (
            f"Tu plan tiene muy buena base. Para cubrir unos gastos mensuales de {formatear_euros_es(gastos)}, "
            f"necesitarías alrededor de {formatear_euros_es(objetivo)}."
        )
        mensaje_color = "text-success"
    elif anos <= 20:
        mensaje_titulo = f"🔥 Podrías alcanzar FIRE en aproximadamente {anos_num} años"
        mensaje_texto = (
            f"Tu objetivo es realista. Con una estrategia simple y constancia, alcanzar "
            f"{formatear_euros_es(objetivo)} es totalmente plausible."
        )
        mensaje_color = "text-primary"
    else:
        mensaje_titulo = f"🔥 Podrías alcanzar FIRE en aproximadamente {anos_num} años"
        mensaje_texto = (
            f"Tu objetivo sigue siendo viable, pero tu ritmo actual hace que quede lejano. "
            "La buena noticia es que un pequeño aumento de aportación puede recortar varios años."
        )
        mensaje_color = "text-warning"

    mensaje = dbc.Card(
        dbc.CardBody(
            [
                html.H4(mensaje_titulo, className=f"fw-bold {mensaje_color}"),
                html.P(mensaje_texto, className="mb-0 text-muted"),
            ]
        ),
        className="shadow border-0 rounded-4",
    )

    # -----------------------------------------------------
    # comparativa +200€/mes
    # -----------------------------------------------------
    if not math.isinf(anos) and not math.isinf(anos_plus):
        mejora_anos = max(round(anos - anos_plus), 0)
        comparativa = info_card(
            "Si ahorras 200€ más al mes",
            [
                html.P(
                    f"Si subes tu aportación a {formatear_euros_es(aportacion + 200)} al mes, "
                    f"podrías llegar en unos {round(anos_plus)} años.",
                    className="mb-2",
                ),
                html.P(
                    f"Eso supone aproximadamente {mejora_anos} años antes.",
                    className="text-success fw-bold mb-0",
                ),
            ],
            "📈",
        )
    else:
        comparativa = info_card(
            "Si ahorras 200€ más al mes",
            html.P(
                "Aumentar la aportación mensual sigue siendo la palanca más fuerte para acercarte a FIRE.",
                className="mb-0",
            ),
            "📈",
        )

    # -----------------------------------------------------
    # coste de esperar
    # -----------------------------------------------------
    capital_5 = capital_en_n_años(capital_actual, aportacion, r, 5)
    coste_retraso = max(capital_5 - capital_actual, 0)

    tarde = info_card(
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
        "⏳",
        "text-danger",
    )

    # -----------------------------------------------------
    # lectura de potencia del plan
    # -----------------------------------------------------
    if aportacion == 0:
        potencia_texto = "Sin aportaciones mensuales, dependerás casi por completo del capital actual y del tiempo."
    elif aportacion < 300:
        potencia_texto = "Tu aportación actual es modesta. Aumentarla un poco tendría mucho impacto."
    elif aportacion < 800:
        potencia_texto = "Tu aportación mensual ya tiene buena base para construir un plan sólido."
    else:
        potencia_texto = "Tu aportación mensual es potente. La clave es mantenerla constante a largo plazo."

    potencia = info_card(
        "Tu palanca principal",
        [
            html.P(potencia_texto, className="mb-2"),
            html.P(
                f"Ahora mismo estás aportando {formatear_euros_es(aportacion)} al mes.",
                className="small text-muted mb-0",
            ),
        ],
        "💪",
    )

    # -----------------------------------------------------
    # diagnóstico rápido
    # -----------------------------------------------------
    if rentabilidad_pct < 4:
        diagnostico_texto = "Tu hipótesis de rentabilidad es conservadora. Está bien para no sobreestimar resultados."
    elif rentabilidad_pct <= 8:
        diagnostico_texto = "Tu rentabilidad estimada está en una zona razonable para simulaciones a largo plazo."
    else:
        diagnostico_texto = "Tu rentabilidad estimada es exigente. Vigila no construir expectativas demasiado optimistas."

    diagnostico = info_card(
        "Lectura rápida del escenario",
        [
            html.P(diagnostico_texto, className="mb-2"),
            html.P(
                f"Estás simulando una rentabilidad del {rentabilidad_pct:.1f}% anual.",
                className="small text-muted mb-0",
            ),
        ],
        "🧭",
    )

    # -----------------------------------------------------
    # CTA intermedio dinámico
    # -----------------------------------------------------
    if math.isinf(anos):
        cta_mid_title = "Empieza por crear el hábito"
        cta_mid_text = (
            "No necesitas hacerlo perfecto. Lo más importante ahora es empezar a invertir con regularidad."
        )
        cta_mid_button = "Empezar poco a poco"
    elif anos <= 10:
        cta_mid_title = "Estás cerca: protege tu avance"
        cta_mid_text = (
            "La disciplina y la constancia pueden marcar la diferencia entre llegar o quedarte a medio camino."
        )
        cta_mid_button = "Mantener mi estrategia"
    elif anos <= 20:
        cta_mid_title = "Tu objetivo es realista"
        cta_mid_text = (
            "Con una estrategia sencilla y aportaciones constantes, puedes recortar varios años."
        )
        cta_mid_button = "Dar el siguiente paso"
    else:
        cta_mid_title = "Recortar tiempo importa mucho"
        cta_mid_text = (
            "Empezar ya y elevar poco a poco tu aportación puede cambiar tu horizonte FIRE más de lo que parece."
        )
        cta_mid_button = "Empezar hoy a invertir"

    cta_intermedio = dbc.Card(
        dbc.CardBody(
            [
                badge("SIGUIENTE PASO", "success"),
                html.H4(cta_mid_title, className="fw-bold mb-2"),
                html.P(cta_mid_text, className="text-muted mb-3"),
                dbc.Button(
                    cta_mid_button,
                    id="fire-cta-middle",
                    color="success",
                    className="rounded-3 fw-semibold px-4 py-2",
                ),
            ]
        ),
        className="shadow border-0 rounded-4",
    )

    # -----------------------------------------------------
    # gráfico
    # -----------------------------------------------------
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
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(0,0,0,0.06)")

    # -----------------------------------------------------
    # CTA dinámico final
    # -----------------------------------------------------
    if math.isinf(anos):
        cta_badge = "PLAN DE ACCIÓN"
        cta_title = "Ahora mismo no necesitas perfección: necesitas empezar"
        cta_text = (
            "Con tus datos actuales, alcanzar FIRE parece demasiado lejano. La prioridad no es buscar "
            "la inversión perfecta, sino construir el hábito de aportar cada mes y aumentar tu capacidad de ahorro."
        )
        cta_points = [
            "Empieza aunque sea con una cantidad modesta.",
            "Automatiza aportaciones para crear constancia.",
            "Una estrategia simple es mejor que no hacer nada.",
        ]
        cta_button_text = "Empezar a invertir poco a poco"

    elif anos <= 10:
        cta_badge = "MUY CERCA DE FIRE"
        cta_title = "Estás cerca: ahora toca no cometer errores"
        cta_text = (
            "Tu plan ya tiene una base muy sólida. Lo más importante ahora es mantener la disciplina, "
            "evitar pausas largas y seguir invirtiendo con una estrategia sencilla."
        )
        cta_points = [
            "Mantén la constancia incluso cuando el mercado caiga.",
            "Evita complicarte con productos innecesarios.",
            "Cada año de disciplina puede acercarte mucho a la meta.",
        ]
        cta_button_text = "Mantener mi estrategia de inversión"

    elif anos <= 20:
        cta_badge = "ACELERA TU PLAN"
        cta_title = "Tu objetivo es realista, pero puedes recortar varios años"
        cta_text = (
            "Estás en una zona muy buena: con constancia puedes llegar. La combinación que más impacto suele tener "
            "es aumentar poco a poco la aportación y mantener una cartera simple a largo plazo."
        )
        cta_points = [
            "Subir tu aportación mensual puede marcar una diferencia enorme.",
            "La automatización evita perder meses importantes.",
            "No necesitas hacerlo perfecto, solo hacerlo constante.",
        ]
        cta_button_text = "Dar el siguiente paso para invertir"

    else:
        cta_badge = "RECORTA TIEMPO"
        cta_title = "Estás lejos de FIRE, pero puedes acelerar mucho el proceso"
        cta_text = (
            "Con tus datos actuales, el objetivo todavía queda lejos. La buena noticia es que empezar ya "
            "y aumentar tu ritmo de inversión puede recortar muchos años frente a esperar."
        )
        cta_points = [
            "Empezar hoy importa más que esperar al momento perfecto.",
            "Aumentar el ahorro mensual tiene más impacto del que parece.",
            "Una cartera sencilla puede ayudarte a avanzar sin bloquearte.",
        ]
        cta_button_text = "Empezar hoy a construir mi libertad financiera"

    # texto estratégico superior
    if math.isinf(anos):
        diagnostico_estrategia = "Ahora mismo tu prioridad no debería ser optimizar unas décimas de rentabilidad, sino construir hábito y capacidad de ahorro."
        accion_1 = "Revisar tus gastos fijos y elevar el margen mensual."
        accion_2 = "Empezar cuanto antes con una rutina de inversión constante."
        accion_3 = "Usar una cartera sencilla para no quedarte paralizado."
    elif anos <= 10:
        diagnostico_estrategia = "Tu plan ya tiene muy buena base. El foco ahora es mantener la constancia y evitar errores."
        accion_1 = "No interrumpir aportaciones cuando caiga el mercado."
        accion_2 = "Mantener comisiones bajas y estrategia simple."
        accion_3 = "Aumentar aportación cuando suban tus ingresos."
    elif anos <= 20:
        diagnostico_estrategia = "Estás en una zona muy razonable. Un pequeño aumento en aportación puede recortar varios años."
        accion_1 = "Intentar subir tu aportación mensual de forma progresiva."
        accion_2 = "No sobrecomplicar la cartera."
        accion_3 = "Automatizar inversión para mantener disciplina."
    else:
        diagnostico_estrategia = "Tu objetivo es viable, pero todavía dependes mucho de aumentar el ahorro mensual."
        accion_1 = "Priorizar una tasa de ahorro más alta."
        accion_2 = "Evitar estar demasiado tiempo en liquidez sin invertir."
        accion_3 = "Revisar si tus gastos objetivo en FIRE son realistas."

    estrategia = dbc.Card(
        dbc.CardBody(
            [
                badge("PLAN RECOMENDADO", "primary"),
                html.H4("La estrategia que más puede acercarte a FIRE", className="fw-bold mb-3"),
                html.P(diagnostico_estrategia, className="text-muted mb-4"),

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
                    className="mb-2",
                ),

                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div(cta_badge, className="small fw-bold text-success mb-2"),
                            html.H5(cta_title, className="fw-bold mb-2"),
                            html.P(cta_text, className="text-muted mb-3"),
                            html.Ul(
                                [html.Li(point) for point in cta_points],
                                className="text-muted mb-3 ps-3",
                            ),
                            dbc.Button(
                                cta_button_text,
                                id="fire-cta-bottom",
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
        potencia,
        diagnostico,
        cta_intermedio,
        fig,
        estrategia,
    )
