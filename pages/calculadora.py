import dash
from dash import html, dcc, Input, Output, callback, clientside_callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from helpers import parse_number, calcular_interes_compuesto, formatear_euros_es
from components.disclaimer_afiliados import build_disclaimer

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/calculadora",
    title="Calculadora de interés compuesto | interescompuesto.app",
    name="Calculadora",
)

# =========================================================
# HELPERS UI
# =========================================================
def section_eyebrow(text):
    return html.Div(
        text,
        className="text-uppercase fw-bold small mb-2",
        style={
            "letterSpacing": "0.08em",
            "color": "#667085",
        },
    )


def premium_badge(text):
    return html.Span(
        text,
        className="d-inline-flex align-items-center rounded-pill px-3 py-2 me-2 mb-2",
        style={
            "background": "#ffffff",
            "border": "1px solid rgba(15, 23, 42, 0.08)",
            "fontSize": "0.92rem",
            "fontWeight": "600",
            "color": "#344054",
            "boxShadow": "0 4px 12px rgba(16, 24, 40, 0.04)",
        },
    )


def info_chip(text):
    return html.Div(
        text,
        className="d-inline-flex align-items-center rounded-pill px-3 py-2 me-2 mb-2",
        style={
            "background": "rgba(25, 135, 84, 0.08)",
            "color": "#146c43",
            "fontWeight": "700",
            "fontSize": "0.88rem",
        }
    )


def metric_card(title, value, subtitle=None, highlight=False):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    title,
                    className="mb-2",
                    style={
                        "fontSize": "0.92rem",
                        "fontWeight": "700",
                        "color": "#667085",
                        "letterSpacing": "0.01em",
                    },
                ),
                html.Div(
                    value,
                    className="fw-bold mb-2",
                    style={
                        "fontSize": "clamp(1.55rem, 2.6vw, 2.15rem)",
                        "lineHeight": "1.1",
                        "color": "#198754" if highlight else "#101828",
                    },
                ),
                html.Div(
                    subtitle,
                    style={
                        "fontSize": "0.93rem",
                        "color": "#667085",
                        "lineHeight": "1.45",
                    },
                ) if subtitle else None,
            ]
        ),
        className="border-0 rounded-4 h-100",
        style={
            "background": "linear-gradient(180deg, #ffffff 0%, #fbfbfc 100%)",
            "boxShadow": "0 12px 30px rgba(16, 24, 40, 0.06)",
        },
    )


def summary_stat_card(title, value, subtitle=None):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    title,
                    style={
                        "fontSize": "0.86rem",
                        "fontWeight": "700",
                        "color": "#667085",
                        "textTransform": "uppercase",
                        "letterSpacing": "0.06em",
                    },
                    className="mb-2",
                ),
                html.Div(
                    value,
                    style={
                        "fontSize": "1.35rem",
                        "fontWeight": "800",
                        "color": "#101828",
                        "lineHeight": "1.15",
                    },
                    className="mb-1",
                ),
                html.Div(
                    subtitle,
                    style={
                        "fontSize": "0.88rem",
                        "color": "#667085",
                    },
                ) if subtitle else None,
            ]
        ),
        className="border-0 rounded-4 h-100",
        style={
            "background": "#ffffff",
            "boxShadow": "0 10px 24px rgba(16, 24, 40, 0.05)",
        },
    )


def input_group(label, input_id, value, input_type="text", hint=None, prefix=None, suffix=None):
    left = dbc.InputGroupText(prefix) if prefix else None
    right = dbc.InputGroupText(suffix) if suffix else None

    children = []
    if left:
        children.append(left)

    children.append(
        dbc.Input(
            id=input_id,
            value=value,
            type=input_type,
            className="py-3 border-0",
            style={
                "fontSize": "1.02rem",
                "fontWeight": "600",
                "background": "#f8fafc",
                "boxShadow": "none",
            },
        )
    )

    if right:
        children.append(right)

    return html.Div(
        [
            dbc.Label(
                label,
                className="fw-semibold mb-2",
                style={"fontSize": "0.97rem", "color": "#1f2937"},
            ),
            dbc.InputGroup(
                children,
                className="rounded-4 overflow-hidden",
                style={
                    "border": "1px solid rgba(15, 23, 42, 0.08)",
                    "boxShadow": "0 2px 10px rgba(15, 23, 42, 0.03)",
                },
            ),
            html.Div(
                hint,
                className="mt-2",
                style={"fontSize": "0.88rem", "color": "#667085"},
            ) if hint else None,
        ],
        className="mb-3",
    )


def scenario_card(title, amount, extra=None, highlight=False):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    title,
                    className="mb-2",
                    style={
                        "fontSize": "0.92rem",
                        "fontWeight": "700",
                        "color": "#667085",
                    },
                ),
                html.Div(
                    amount,
                    className="fw-bold mb-2",
                    style={
                        "fontSize": "1.7rem",
                        "lineHeight": "1.15",
                        "color": "#198754" if highlight else "#101828",
                    },
                ),
                html.Div(
                    extra,
                    style={
                        "fontSize": "0.93rem",
                        "color": "#667085",
                        "lineHeight": "1.5",
                    },
                ) if extra else None,
            ]
        ),
        className="border-0 rounded-4 h-100",
        style={
            "background": "#ffffff",
            "boxShadow": "0 10px 28px rgba(16, 24, 40, 0.06)",
            "border": "1px solid rgba(0,0,0,0.04)",
        },
    )


def build_yearly_table(evolucion):
    if not evolucion:
        return html.Div()

    rows = []
    total_rows = len(evolucion)

    if total_rows <= 12:
        sampled = evolucion
    else:
        sampled = [evolucion[0]]
        step = max(1, total_rows // 8)
        sampled.extend(evolucion[i] for i in range(step, total_rows - 1, step))
        sampled.append(evolucion[-1])

        unique_years = set()
        filtered = []
        for item in sampled:
            year = item["año"]
            if year not in unique_years:
                unique_years.add(year)
                filtered.append(item)
        sampled = filtered

    for item in sampled:
        total = item["total"]
        aportado = item["aportado"]
        ganancia = total - aportado
        real = item["real"]

        rows.append(
            html.Tr(
                [
                    html.Td(item["año"], className="fw-semibold"),
                    html.Td(formatear_euros_es(aportado)),
                    html.Td(formatear_euros_es(total)),
                    html.Td(formatear_euros_es(ganancia)),
                    html.Td(formatear_euros_es(real)),
                ]
            )
        )

    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Año"),
                        html.Th("Aportado"),
                        html.Th("Valor total"),
                        html.Th("Ganancia"),
                        html.Th("Valor real"),
                    ]
                )
            ),
            html.Tbody(rows),
        ],
        bordered=False,
        hover=True,
        responsive=True,
        class_name="align-middle mb-0",
        style={"fontSize": "0.95rem"},
    )


def build_empty_figure():
    fig = go.Figure()
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=20, b=10),
        height=440,
        xaxis=dict(visible=False, showgrid=False, zeroline=False),
        yaxis=dict(visible=False, showgrid=False, zeroline=False),
        annotations=[
            dict(
                text="Introduce tus datos y pulsa en calcular para ver la evolución de tu inversión",
                x=0.5,
                y=0.5,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(size=16, color="#667085"),
                align="center",
            )
        ],
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    return fig


# =========================================================
# LAYOUT
# =========================================================
layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                section_eyebrow("Simulador premium"),
                                html.H1(
                                    "Calcula cuánto podría crecer tu dinero con el paso del tiempo",
                                    className="fw-bold mb-3",
                                    style={
                                        "fontSize": "clamp(2rem, 4.2vw, 3.55rem)",
                                        "lineHeight": "1.06",
                                        "letterSpacing": "-0.03em",
                                        "color": "#0f172a",
                                        "maxWidth": "920px",
                                    },
                                ),
                                html.P(
                                    "Simula tu inversión con capital inicial, aportaciones mensuales, rentabilidad, inflación y comisiones. "
                                    "Obtén una estimación clara, visual y realista de cómo podría evolucionar tu patrimonio a largo plazo.",
                                    className="mb-4",
                                    style={
                                        "fontSize": "1.08rem",
                                        "color": "#475467",
                                        "maxWidth": "860px",
                                        "lineHeight": "1.7",
                                    },
                                ),
                                html.Div(
                                    [
                                        premium_badge("Interés compuesto"),
                                        premium_badge("Aportaciones periódicas"),
                                        premium_badge("Inflación incluida"),
                                        premium_badge("Comisiones incluidas"),
                                    ],
                                    className="mb-2",
                                ),
                            ]
                        ),
                        className="border-0 rounded-4 mt-4 mb-4",
                        style={
                            "background": "linear-gradient(135deg, #ffffff 0%, #f8fbff 50%, #f6f8fb 100%)",
                            "boxShadow": "0 18px 50px rgba(16, 24, 40, 0.08)",
                        },
                    ),
                    width=12,
                )
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                section_eyebrow("Tu simulación"),
                                html.H4(
                                    "Configura los datos de tu inversión",
                                    className="fw-bold mb-3",
                                    style={"color": "#0f172a"},
                                ),
                                html.P(
                                    "Ajusta las variables clave y descubre cómo pequeñas decisiones pueden provocar una gran diferencia con el tiempo.",
                                    className="mb-4",
                                    style={"color": "#667085", "lineHeight": "1.6"},
                                ),

                                input_group(
                                    "Capital inicial",
                                    "ic-capital-inicial",
                                    "10000",
                                    "text",
                                    "Ejemplo: 10.000 €",
                                    suffix="€",
                                ),
                                input_group(
                                    "Aportación mensual",
                                    "ic-aportacion",
                                    "300",
                                    "text",
                                    "Cantidad que añadirías cada mes",
                                    suffix="€",
                                ),
                                input_group(
                                    "Horizonte temporal",
                                    "ic-anios",
                                    "20",
                                    "number",
                                    "Número de años que mantendrías la inversión",
                                    suffix="años",
                                ),
                                input_group(
                                    "Rentabilidad anual media",
                                    "ic-rentabilidad",
                                    "7",
                                    "text",
                                    "Rentabilidad anual esperada antes de inflación",
                                    suffix="%",
                                ),
                                input_group(
                                    "Inflación anual",
                                    "ic-inflacion",
                                    "2",
                                    "text",
                                    "Para estimar el valor real futuro de tu dinero",
                                    suffix="%",
                                ),
                                input_group(
                                    "Comisión anual",
                                    "ic-comision",
                                    "0.2",
                                    "text",
                                    "Coste aproximado del producto o cartera",
                                    suffix="%",
                                ),

                                dbc.Button(
                                    "Calcular mi dinero futuro",
                                    id="ic-boton",
                                    color="success",
                                    size="lg",
                                    className="w-100 rounded-pill fw-bold mt-2 py-3",
                                    style={
                                        "boxShadow": "0 12px 25px rgba(25, 135, 84, 0.25)",
                                        "fontSize": "1rem",
                                    }
                                ),

                                html.Div(
                                    "Simulación orientativa. No constituye asesoramiento financiero ni garantiza rentabilidades futuras.",
                                    className="mt-3",
                                    style={
                                        "fontSize": "0.88rem",
                                        "color": "#667085",
                                        "lineHeight": "1.5",
                                    },
                                ),
                            ]
                        ),
                        className="border-0 rounded-4",
                        style={
                            "background": "#ffffff",
                            "boxShadow": "0 18px 45px rgba(16, 24, 40, 0.08)",
                            "position": "sticky",
                            "top": "90px",
                        },
                    ),
                    lg=4,
                    className="mb-4",
                ),

                dbc.Col(
                    [
                        html.Div(id="scroll-target", className="anchor-spacer"),

                        html.Div(
                            [
                                info_chip("Resultado estimado"),
                                info_chip("Comparativa incluida"),
                                info_chip("Tabla anual"),
                            ],
                            className="mb-3",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(html.Div(id="ic-quick-stat-1"), md=3, className="mb-3"),
                                dbc.Col(html.Div(id="ic-quick-stat-2"), md=3, className="mb-3"),
                                dbc.Col(html.Div(id="ic-quick-stat-3"), md=3, className="mb-3"),
                                dbc.Col(html.Div(id="ic-quick-stat-4"), md=3, className="mb-3"),
                            ],
                            className="mb-1",
                        ),

                        dbc.Row(
                            [
                                dbc.Col(html.Div(id="ic-resultado-final"), md=4, className="mb-3"),
                                dbc.Col(html.Div(id="ic-total-aportado"), md=4, className="mb-3"),
                                dbc.Col(html.Div(id="ic-ganancia"), md=4, className="mb-3"),
                            ],
                            className="mb-1",
                        ),

                        html.Div(id="ic-mensaje-emocional", className="mb-4"),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    section_eyebrow("Lectura rápida"),
                                    html.H4(
                                        "Qué significa realmente tu simulación",
                                        className="fw-bold mb-3",
                                        style={"color": "#0f172a"},
                                    ),
                                    html.Div(id="ic-interpretacion"),
                                ]
                            ),
                            className="border-0 rounded-4 mb-4",
                            style={
                                "background": "#ffffff",
                                "boxShadow": "0 14px 36px rgba(16, 24, 40, 0.06)",
                            },
                        ),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    section_eyebrow("Visualización"),
                                    html.H4(
                                        "Evolución estimada de tu inversión",
                                        className="fw-bold mb-2",
                                        style={"color": "#0f172a"},
                                    ),
                                    html.P(
                                        "Compara lo aportado, el valor total y el valor real ajustado por inflación.",
                                        className="mb-3",
                                        style={"color": "#667085"},
                                    ),
                                    dcc.Graph(
                                        id="ic-grafico",
                                        figure=build_empty_figure(),
                                        config={"displayModeBar": False},
                                    ),
                                ]
                            ),
                            className="border-0 rounded-4 mb-4",
                            style={
                                "background": "#ffffff",
                                "boxShadow": "0 14px 36px rgba(16, 24, 40, 0.06)",
                            },
                        ),

                        html.Div(id="ic-comparativa", className="mb-4"),
                        html.Div(id="ic-start-delay-comparison", className="mb-4"),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    section_eyebrow("Detalle anual"),
                                    html.H4(
                                        "Resumen de la evolución por años",
                                        className="fw-bold mb-3",
                                        style={"color": "#0f172a"},
                                    ),
                                    html.Div(id="ic-tabla-anual"),
                                ]
                            ),
                            className="border-0 rounded-4 mb-4",
                            style={
                                "background": "#ffffff",
                                "boxShadow": "0 14px 36px rgba(16, 24, 40, 0.06)",
                            },
                        ),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    section_eyebrow("Siguiente paso"),
                                    html.H4(
                                        "Convierte la simulación en una decisión real",
                                        className="fw-bold mb-3",
                                        style={"color": "#0f172a"},
                                    ),
                                    html.P(
                                        "La diferencia entre planear e invertir suele estar en empezar. "
                                        "No necesitas hacerlo perfecto, pero sí con criterio, costes razonables y constancia.",
                                        className="mb-3",
                                        style={"color": "#475467", "lineHeight": "1.7"},
                                    ),
                                    html.Div(
                                        [
                                            html.Div("✔ Empezar antes importa", className="mb-2"),
                                            html.Div("✔ Los costes importan mucho", className="mb-2"),
                                            html.Div("✔ La constancia suele marcar la diferencia", className="mb-3"),
                                        ],
                                        style={"color": "#344054", "fontWeight": "600"},
                                    ),
                                    dbc.Button(
                                        "Abrir cuenta y empezar a invertir",
                                        href=MYINVESTOR_AFFILIATE_URL,
                                        target="_blank",
                                        color="success",
                                        size="lg",
                                        className="w-100 rounded-pill fw-bold py-3"
                                    ),
                                ]
                            ),
                            className="border-0 rounded-4 mb-4",
                            style={
                                "background": "linear-gradient(135deg, #ffffff 0%, #f7fcf9 100%)",
                                "boxShadow": "0 18px 45px rgba(16, 24, 40, 0.08)",
                            },
                        ),

                        build_disclaimer(title="Más opciones para dar el siguiente paso"),
                    ],
                    lg=8,
                ),
            ],
            className="gy-4",
        ),
    ],
    fluid=True,
    className="px-4 px-md-5 pb-5",
    style={"maxWidth": "1500px"},
)

# =========================================================
# SCROLL AUTOMÁTICO
# =========================================================
clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks) {
            setTimeout(() => {
                const el = document.getElementById("scroll-target");
                if (el) {
                    el.scrollIntoView({behavior: "smooth", block: "start"});
                }
            }, 120);
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
    Output("ic-quick-stat-1", "children"),
    Output("ic-quick-stat-2", "children"),
    Output("ic-quick-stat-3", "children"),
    Output("ic-quick-stat-4", "children"),
    Output("ic-resultado-final", "children"),
    Output("ic-total-aportado", "children"),
    Output("ic-ganancia", "children"),
    Output("ic-grafico", "figure"),
    Output("ic-mensaje-emocional", "children"),
    Output("ic-comparativa", "children"),
    Output("ic-start-delay-comparison", "children"),
    Output("ic-interpretacion", "children"),
    Output("ic-tabla-anual", "children"),
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
    rentabilidad_pct = parse_number(rentabilidad)
    inflacion_pct = parse_number(inflacion)
    comision_pct = parse_number(comision)

    rentabilidad = rentabilidad_pct / 100
    inflacion = inflacion_pct / 100
    comision = comision_pct / 100

    evolucion = calcular_interes_compuesto(
        capital_inicial=capital_inicial,
        aportacion_mensual=aportacion,
        años=anios,
        rentabilidad_anual=rentabilidad,
        inflacion=inflacion,
        comision=comision,
    )

    if not evolucion:
        empty = html.Div()
        return (
            summary_stat_card("Capital inicial", "0 €"),
            summary_stat_card("Aportación mensual", "0 €"),
            summary_stat_card("Rentabilidad", "0 %"),
            summary_stat_card("Horizonte", "0 años"),
            metric_card("Valor final", "0 €", "Estimación nominal final"),
            metric_card("Total aportado", "0 €", "Lo que habrías invertido"),
            metric_card("Ganancia potencial", "0 €", "Crecimiento estimado"),
            build_empty_figure(),
            "",
            "",
            "",
            "",
            empty,
        )

    anos = [x["año"] for x in evolucion]
    total = [x["total"] for x in evolucion]
    aportado_hist = [x["aportado"] for x in evolucion]
    real = [x["real"] for x in evolucion]

    valor_final = total[-1]
    total_aportado = aportado_hist[-1]
    ganancia = valor_final - total_aportado

    evolucion_100 = calcular_interes_compuesto(
        capital_inicial=capital_inicial,
        aportacion_mensual=aportacion + 100,
        años=anios,
        rentabilidad_anual=rentabilidad,
        inflacion=inflacion,
        comision=comision,
    )

    evolucion_200 = calcular_interes_compuesto(
        capital_inicial=capital_inicial,
        aportacion_mensual=aportacion + 200,
        años=anios,
        rentabilidad_anual=rentabilidad,
        inflacion=inflacion,
        comision=comision,
    )

    valor_100 = evolucion_100[-1]["total"] if evolucion_100 else 0
    valor_200 = evolucion_200[-1]["total"] if evolucion_200 else 0

    diferencia_100 = valor_100 - valor_final
    diferencia_200 = valor_200 - valor_final

    # Empezar hoy vs esperar 5 años
    anios_espera = 5
    anios_retrasados = max(anios - anios_espera, 0)

    evolucion_tarde = calcular_interes_compuesto(
        capital_inicial=capital_inicial,
        aportacion_mensual=aportacion,
        años=anios_retrasados,
        rentabilidad_anual=rentabilidad,
        inflacion=inflacion,
        comision=comision,
    ) if anios_retrasados > 0 else []

    valor_tarde = evolucion_tarde[-1]["total"] if evolucion_tarde else 0
    diferencia_por_esperar = valor_final - valor_tarde

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=anos,
            y=aportado_hist,
            mode="lines",
            name="Capital aportado",
            line=dict(width=3),
            hovertemplate="Año %{x}<br>Aportado: %{y:,.2f} €<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=anos,
            y=total,
            mode="lines",
            name="Valor total",
            line=dict(width=4),
            hovertemplate="Año %{x}<br>Valor total: %{y:,.2f} €<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=anos,
            y=real,
            mode="lines",
            name="Valor real",
            line=dict(width=3, dash="dot"),
            hovertemplate="Año %{x}<br>Valor real: %{y:,.2f} €<extra></extra>",
        )
    )

    fig.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=20, b=10),
        height=440,
        xaxis_title="Años",
        yaxis_title="Euros",
        legend_title="",
        hovermode="x unified",
        paper_bgcolor="white",
        plot_bgcolor="white",
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12),
        title_font=dict(size=13),
    )
    fig.update_yaxes(
        gridcolor="rgba(15, 23, 42, 0.08)",
        zeroline=False,
        tickfont=dict(size=12),
        title_font=dict(size=13),
    )

    quick_1 = summary_stat_card(
        "Capital inicial",
        formatear_euros_es(capital_inicial),
        "Punto de partida",
    )
    quick_2 = summary_stat_card(
        "Aportación mensual",
        formatear_euros_es(aportacion),
        "Ahorro periódico",
    )
    quick_3 = summary_stat_card(
        "Rentabilidad anual",
        f"{rentabilidad_pct:.2f} %",
        "Antes de inflación",
    )
    quick_4 = summary_stat_card(
        "Horizonte temporal",
        f"{anios} años",
        f"Inflación {inflacion_pct:.2f} % · Comisión {comision_pct:.2f} %",
    )

    mensaje = dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    "Estimación principal",
                    className="mb-2",
                    style={
                        "fontSize": "0.9rem",
                        "fontWeight": "700",
                        "color": "#667085",
                        "textTransform": "uppercase",
                        "letterSpacing": "0.07em",
                    },
                ),
                html.H3(
                    f"Podrías alcanzar {formatear_euros_es(valor_final)}",
                    className="fw-bold mb-2",
                    style={
                        "fontSize": "clamp(1.5rem, 2.2vw, 2.2rem)",
                        "color": "#0f172a",
                        "lineHeight": "1.2",
                    }
                ),
                html.P(
                    f"Habrías aportado {formatear_euros_es(total_aportado)} y el crecimiento potencial sería de {formatear_euros_es(ganancia)}.",
                    className="mb-0",
                    style={
                        "fontSize": "1rem",
                        "color": "#475467",
                        "lineHeight": "1.7",
                    }
                ),
            ]
        ),
        className="border-0 rounded-4",
        style={
            "background": "linear-gradient(135deg, #ffffff 0%, #f7fbff 100%)",
            "boxShadow": "0 14px 36px rgba(16, 24, 40, 0.07)",
        },
    )

    comparativa = html.Div(
        [
            section_eyebrow("Escenarios alternativos"),
            html.H4(
                "Cómo cambia el resultado si aumentas tu aportación",
                className="fw-bold mb-3",
                style={"color": "#0f172a"},
            ),
            dbc.Row(
                [
                    dbc.Col(
                        scenario_card(
                            "Escenario actual",
                            formatear_euros_es(valor_final),
                            f"{formatear_euros_es(aportacion)} al mes",
                            False,
                        ),
                        md=4,
                        className="mb-3"
                    ),
                    dbc.Col(
                        scenario_card(
                            "+100 €/mes",
                            formatear_euros_es(valor_100),
                            f"{formatear_euros_es(diferencia_100)} más frente al escenario actual",
                            True,
                        ),
                        md=4,
                        className="mb-3"
                    ),
                    dbc.Col(
                        scenario_card(
                            "+200 €/mes",
                            formatear_euros_es(valor_200),
                            f"{formatear_euros_es(diferencia_200)} más frente al escenario actual",
                            True,
                        ),
                        md=4,
                        className="mb-3"
                    ),
                ]
            )
        ]
    )

    comparativa_tiempo = html.Div(
        [
            section_eyebrow("Impacto del tiempo"),
            html.H4(
                "Empezar hoy vs esperar 5 años",
                className="fw-bold mb-3",
                style={"color": "#0f172a"},
            ),
            dbc.Row(
                [
                    dbc.Col(
                        scenario_card(
                            "Empezando hoy",
                            formatear_euros_es(valor_final),
                            f"Invirtiendo durante {anios} años",
                            True,
                        ),
                        md=6,
                        className="mb-3",
                    ),
                    dbc.Col(
                        scenario_card(
                            "Esperando 5 años",
                            formatear_euros_es(valor_tarde),
                            (
                                f"Podrías acabar con {formatear_euros_es(diferencia_por_esperar)} menos"
                                if anios_retrasados > 0 else
                                "No hay horizonte suficiente para comparar"
                            ),
                            False,
                        ),
                        md=6,
                        className="mb-3",
                    ),
                ]
            ),
        ]
    )

    interpretacion = html.Ul(
        [
            html.Li(
                f"Si alcanzaras {formatear_euros_es(valor_final)}, una parte importante no vendría de lo aportado, sino del crecimiento acumulado con el tiempo."
            ),
            html.Li(
                "El tiempo suele ser la variable más poderosa. Empezar antes puede tener más impacto que intentar optimizar cada detalle desde el principio."
            ),
            html.Li(
                "Subir ligeramente la aportación mensual puede producir una diferencia muy significativa cuando se mantiene durante años."
            ),
            html.Li(
                "La inflación y las comisiones reducen el resultado real, así que conviene vigilar costes y pensar siempre en términos de largo plazo."
            ),
        ],
        style={
            "paddingLeft": "1.2rem",
            "marginBottom": "0",
            "color": "#475467",
            "lineHeight": "1.8",
            "fontSize": "1rem",
        }
    )

    tabla_anual = build_yearly_table(evolucion)

    return (
        quick_1,
        quick_2,
        quick_3,
        quick_4,
        metric_card("Valor final", formatear_euros_es(valor_final), "Estimación nominal al final del periodo", True),
        metric_card("Total aportado", formatear_euros_es(total_aportado), "Dinero que habrías puesto tú directamente"),
        metric_card("Ganancia potencial", formatear_euros_es(ganancia), "Crecimiento estimado generado por la inversión", True),
        fig,
        mensaje,
        comparativa,
        comparativa_tiempo,
        interpretacion,
        tabla_anual,
    )
