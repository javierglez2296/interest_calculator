import io
from urllib.parse import urlencode, parse_qs

import dash
from dash import (
    html,
    dcc,
    Input,
    Output,
    State,
    callback,
    clientside_callback,
    ctx,
)
import dash_bootstrap_components as dbc
import pandas as pd
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
        },
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


def build_empty_figure(message, height=440):
    fig = go.Figure()
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=20, b=10),
        height=height,
        xaxis=dict(visible=False, showgrid=False, zeroline=False),
        yaxis=dict(visible=False, showgrid=False, zeroline=False),
        annotations=[
            dict(
                text=message,
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


def build_donut_figure(aportado, ganancia):
    fig = go.Figure(
        go.Pie(
            labels=["Aportado por ti", "Crecimiento estimado"],
            values=[max(aportado, 0), max(ganancia, 0)],
            hole=0.68,
            sort=False,
            textinfo="none",
            hovertemplate="%{label}<br>%{value:,.2f} €<extra></extra>",
        )
    )
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=10, b=10),
        height=320,
        showlegend=True,
        legend=dict(orientation="h", y=-0.08, x=0.5, xanchor="center"),
        paper_bgcolor="white",
        plot_bgcolor="white",
        annotations=[
            dict(
                text="Composición<br>final",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=16, color="#344054"),
            )
        ],
    )
    return fig


def build_breakdown_bars(aportado, ganancia, cash_value):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=["Tu simulación", "Dinero parado"],
            y=[aportado, cash_value],
            name="Capital aportado",
            hovertemplate="%{x}<br>%{y:,.2f} €<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=["Tu simulación", "Dinero parado"],
            y=[max(ganancia, 0), 0],
            name="Crecimiento",
            hovertemplate="%{x}<br>%{y:,.2f} €<extra></extra>",
        )
    )
    fig.update_layout(
        template="plotly_white",
        barmode="stack",
        margin=dict(l=10, r=10, t=20, b=10),
        height=360,
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend_title="",
        xaxis_title="",
        yaxis_title="Euros",
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(15, 23, 42, 0.08)", zeroline=False)
    return fig


def scenario_defaults(scenario):
    presets = {
        "conservador": {"rentabilidad": "4", "inflacion": "2", "comision": "0.30"},
        "base": {"rentabilidad": "7", "inflacion": "2", "comision": "0.20"},
        "optimista": {"rentabilidad": "9", "inflacion": "2", "comision": "0.15"},
    }
    return presets.get(scenario, presets["base"])


def cash_evolution(capital_inicial, aportacion_mensual, anios, inflacion):
    evolucion = []
    total = capital_inicial
    aportado = capital_inicial
    for year in range(1, anios + 1):
        aportado += aportacion_mensual * 12
        total += aportacion_mensual * 12
        real = total / ((1 + inflacion) ** year) if inflacion > -1 else total
        evolucion.append(
            {
                "año": year,
                "aportado": aportado,
                "total": total,
                "real": real,
            }
        )
    return evolucion


def build_advice_block(valor_final, total_aportado, anios, aportacion_mensual, ganancia):
    ratio = (ganancia / total_aportado) if total_aportado > 0 else 0

    if valor_final < 50000:
        title = "Aún estás en fase de construcción"
        bullets = [
            "Tu prioridad probablemente debería ser crear el hábito de aportación periódica.",
            "Subir poco a poco la aportación puede tener más impacto que buscar rentabilidades extremas.",
            "Revisar comisiones y mantener constancia es más importante que complicar la estrategia.",
        ]
    elif valor_final < 200000:
        title = "Ya hay una base financiera visible"
        bullets = [
            "La consistencia empieza a notarse y el interés compuesto gana peso.",
            "Un pequeño aumento de aportación mensual puede acelerar bastante el resultado final.",
            "Tiene sentido vigilar costes, diversificación y horizonte temporal.",
        ]
    else:
        title = "Tu simulación ya entra en una fase potente"
        bullets = [
            "Aquí el tiempo y la disciplina empiezan a trabajar claramente a tu favor.",
            "Conviene cuidar especialmente las comisiones, porque restan mucho en cifras grandes.",
            "Tiene sentido revisar objetivos concretos: patrimonio, independencia parcial o renta futura.",
        ]

    extra_line = (
        "En esta simulación el crecimiento pesa bastante frente a lo aportado."
        if ratio >= 0.5
        else "En esta simulación aún pesa más la aportación que el crecimiento, algo normal en etapas iniciales."
    )

    return dbc.Card(
        dbc.CardBody(
            [
                section_eyebrow("Qué haría yo con este resultado"),
                html.H4(
                    title,
                    className="fw-bold mb-3",
                    style={"color": "#0f172a"},
                ),
                html.P(
                    extra_line,
                    className="mb-3",
                    style={"color": "#475467", "lineHeight": "1.7"},
                ),
                html.Ul(
                    [html.Li(item) for item in bullets],
                    style={
                        "paddingLeft": "1.2rem",
                        "marginBottom": "0",
                        "color": "#475467",
                        "lineHeight": "1.8",
                        "fontSize": "1rem",
                    },
                ),
            ]
        ),
        className="border-0 rounded-4",
        style={
            "background": "#ffffff",
            "boxShadow": "0 14px 36px rgba(16, 24, 40, 0.06)",
        },
    )


def evolution_to_dataframe(evolucion):
    rows = []
    for item in evolucion:
        total = item["total"]
        aportado = item["aportado"]
        ganancia = total - aportado
        rows.append(
            {
                "Año": item["año"],
                "Aportado": round(aportado, 2),
                "Valor total": round(total, 2),
                "Ganancia": round(ganancia, 2),
                "Valor real": round(item["real"], 2),
            }
        )
    return pd.DataFrame(rows)


# =========================================================
# LAYOUT
# =========================================================
layout = dbc.Container(
    [
        dcc.Location(id="ic-url", refresh=False),
        dcc.Store(id="ic-evolucion-store"),
        dcc.Download(id="ic-download-csv"),

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
                                    "Simula tu inversión con capital inicial, aportaciones periódicas, rentabilidad, inflación y comisiones. "
                                    "Obtén una estimación mucho más clara, visual y realista de cómo podría evolucionar tu patrimonio.",
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
                                        premium_badge("Escenarios"),
                                        premium_badge("CSV exportable"),
                                        premium_badge("Enlace compartible"),
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
                                    "Elige un escenario orientativo y ajusta tus variables clave. "
                                    "La idea es que puedas visualizar mejor el impacto de tiempo, aportaciones y costes.",
                                    className="mb-4",
                                    style={"color": "#667085", "lineHeight": "1.6"},
                                ),

                                dbc.Label("Escenario", className="fw-semibold mb-2"),
                                dcc.RadioItems(
                                    id="ic-scenario",
                                    options=[
                                        {"label": " Conservador", "value": "conservador"},
                                        {"label": " Base", "value": "base"},
                                        {"label": " Optimista", "value": "optimista"},
                                    ],
                                    value="base",
                                    inline=True,
                                    inputStyle={"marginRight": "6px", "marginLeft": "10px"},
                                    labelStyle={
                                        "display": "inline-flex",
                                        "alignItems": "center",
                                        "fontWeight": "600",
                                        "color": "#344054",
                                    },
                                    className="mb-3",
                                ),

                                dbc.Label("Tipo de aportación", className="fw-semibold mb-2"),
                                dcc.RadioItems(
                                    id="ic-aportacion-tipo",
                                    options=[
                                        {"label": " Mensual", "value": "mensual"},
                                        {"label": " Anual", "value": "anual"},
                                    ],
                                    value="mensual",
                                    inline=True,
                                    inputStyle={"marginRight": "6px", "marginLeft": "10px"},
                                    labelStyle={
                                        "display": "inline-flex",
                                        "alignItems": "center",
                                        "fontWeight": "600",
                                        "color": "#344054",
                                    },
                                    className="mb-3",
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
                                    "Aportación",
                                    "ic-aportacion",
                                    "300",
                                    "text",
                                    "Puedes introducir una aportación mensual o anual según el selector superior",
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
                                    },
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
                                info_chip("CSV exportable"),
                                info_chip("Enlace compartible"),
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

                        dbc.Row(
                            [
                                dbc.Col(
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
                                        className="border-0 rounded-4 h-100",
                                        style={
                                            "background": "#ffffff",
                                            "boxShadow": "0 14px 36px rgba(16, 24, 40, 0.06)",
                                        },
                                    ),
                                    lg=7,
                                    className="mb-4",
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                section_eyebrow("Composición final"),
                                                html.H4(
                                                    "Aportado vs crecimiento",
                                                    className="fw-bold mb-3",
                                                    style={"color": "#0f172a"},
                                                ),
                                                dcc.Graph(
                                                    id="ic-donut",
                                                    figure=build_empty_figure(
                                                        "Calcula tu simulación para ver la composición final",
                                                        height=320,
                                                    ),
                                                    config={"displayModeBar": False},
                                                ),
                                            ]
                                        ),
                                        className="border-0 rounded-4 h-100",
                                        style={
                                            "background": "#ffffff",
                                            "boxShadow": "0 14px 36px rgba(16, 24, 40, 0.06)",
                                        },
                                    ),
                                    lg=5,
                                    className="mb-4",
                                ),
                            ]
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
                                        figure=build_empty_figure(
                                            "Introduce tus datos y pulsa en calcular para ver la evolución de tu inversión"
                                        ),
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
                        html.Div(id="ic-insights", className="mb-4"),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    section_eyebrow("Comparativa extra"),
                                    html.H4(
                                        "Invertir vs dejar el dinero parado",
                                        className="fw-bold mb-2",
                                        style={"color": "#0f172a"},
                                    ),
                                    html.P(
                                        "Una comparación simple entre tu simulación y el mismo dinero sin rentabilidad.",
                                        className="mb-3",
                                        style={"color": "#667085"},
                                    ),
                                    dcc.Graph(
                                        id="ic-breakdown-bars",
                                        figure=build_empty_figure(
                                            "Calcula tu simulación para comparar alternativas",
                                            height=360,
                                        ),
                                        config={"displayModeBar": False},
                                    ),
                                    html.Div(id="ic-cash-comparison-copy"),
                                ]
                            ),
                            className="border-0 rounded-4 mb-4",
                            style={
                                "background": "#ffffff",
                                "boxShadow": "0 14px 36px rgba(16, 24, 40, 0.06)",
                            },
                        ),

                        html.Div(id="ic-advice-block", className="mb-4"),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                [
                                                    section_eyebrow("Detalle anual"),
                                                    html.H4(
                                                        "Resumen de la evolución por años",
                                                        className="fw-bold mb-3",
                                                        style={"color": "#0f172a"},
                                                    ),
                                                ],
                                                md=8,
                                            ),
                                            dbc.Col(
                                                dbc.Button(
                                                    "Descargar CSV",
                                                    id="ic-download-btn",
                                                    color="secondary",
                                                    className="w-100 rounded-pill fw-semibold",
                                                ),
                                                md=4,
                                                className="d-flex align-items-start",
                                            ),
                                        ],
                                        className="g-3 mb-2",
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
                                    section_eyebrow("Compartir simulación"),
                                    html.H4(
                                        "Genera un enlace con tus parámetros",
                                        className="fw-bold mb-3",
                                        style={"color": "#0f172a"},
                                    ),
                                    html.P(
                                        "Puedes copiar este enlace para abrir la misma simulación más tarde o compartirla.",
                                        className="mb-3",
                                        style={"color": "#475467", "lineHeight": "1.7"},
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                dbc.Input(
                                                    id="ic-share-link",
                                                    type="text",
                                                    value="",
                                                    readOnly=True,
                                                    className="rounded-4 py-3",
                                                    style={"background": "#f8fafc"},
                                                ),
                                                md=9,
                                                className="mb-2 mb-md-0",
                                            ),
                                            dbc.Col(
                                                dbc.Button(
                                                    "Copiar enlace",
                                                    id="ic-copy-link-btn",
                                                    color="secondary",
                                                    className="w-100 rounded-pill fw-semibold py-3",
                                                ),
                                                md=3,
                                            ),
                                        ],
                                        className="g-2",
                                    ),
                                    html.Div(
                                        id="ic-copy-feedback",
                                        className="mt-3",
                                        style={"fontSize": "0.92rem", "color": "#146c43", "fontWeight": "700"},
                                    ),
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
                                        className="w-100 rounded-pill fw-bold py-3",
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
# COPIAR ENLACE
# =========================================================
clientside_callback(
    """
    function(n_clicks, value) {
        if (!n_clicks || !value) {
            return "";
        }
        try {
            navigator.clipboard.writeText(value);
            return "Enlace copiado al portapapeles";
        } catch(e) {
            return "No se pudo copiar automáticamente. Copia el enlace manualmente.";
        }
    }
    """,
    Output("ic-copy-feedback", "children"),
    Input("ic-copy-link-btn", "n_clicks"),
    State("ic-share-link", "value"),
)

# =========================================================
# CARGA DESDE URL
# =========================================================
@callback(
    Output("ic-capital-inicial", "value"),
    Output("ic-aportacion", "value"),
    Output("ic-aportacion-tipo", "value"),
    Output("ic-anios", "value"),
    Output("ic-rentabilidad", "value"),
    Output("ic-inflacion", "value"),
    Output("ic-comision", "value"),
    Output("ic-scenario", "value"),
    Input("ic-url", "search"),
    prevent_initial_call=False,
)
def cargar_desde_url(search):
    defaults = {
        "capital": "10000",
        "aportacion": "300",
        "tipo": "mensual",
        "anios": "20",
        "rent": "7",
        "infl": "2",
        "fee": "0.2",
        "escenario": "base",
    }

    if not search:
        return (
            defaults["capital"],
            defaults["aportacion"],
            defaults["tipo"],
            defaults["anios"],
            defaults["rent"],
            defaults["infl"],
            defaults["fee"],
            defaults["escenario"],
        )

    qs = parse_qs(search.lstrip("?"))

    capital = qs.get("capital", [defaults["capital"]])[0]
    aportacion = qs.get("aportacion", [defaults["aportacion"]])[0]
    tipo = qs.get("tipo", [defaults["tipo"]])[0]
    anios = qs.get("anios", [defaults["anios"]])[0]
    rent = qs.get("rent", [defaults["rent"]])[0]
    infl = qs.get("infl", [defaults["infl"]])[0]
    fee = qs.get("fee", [defaults["fee"]])[0]
    escenario = qs.get("escenario", [defaults["escenario"]])[0]

    if tipo not in {"mensual", "anual"}:
        tipo = defaults["tipo"]
    if escenario not in {"conservador", "base", "optimista"}:
        escenario = defaults["escenario"]

    return capital, aportacion, tipo, anios, rent, infl, fee, escenario


# =========================================================
# PRESETS DE ESCENARIO
# =========================================================
@callback(
    Output("ic-rentabilidad", "value", allow_duplicate=True),
    Output("ic-inflacion", "value", allow_duplicate=True),
    Output("ic-comision", "value", allow_duplicate=True),
    Input("ic-scenario", "value"),
    prevent_initial_call=True,
)
def aplicar_escenario(scenario):
    preset = scenario_defaults(scenario)
    return preset["rentabilidad"], preset["inflacion"], preset["comision"]


# =========================================================
# ENLACE COMPARTIBLE
# =========================================================
@callback(
    Output("ic-share-link", "value"),
    Input("ic-capital-inicial", "value"),
    Input("ic-aportacion", "value"),
    Input("ic-aportacion-tipo", "value"),
    Input("ic-anios", "value"),
    Input("ic-rentabilidad", "value"),
    Input("ic-inflacion", "value"),
    Input("ic-comision", "value"),
    Input("ic-scenario", "value"),
)
def generar_share_link(capital, aportacion, aportacion_tipo, anios, rentabilidad, inflacion, comision, scenario):
    params = {
        "capital": capital or "",
        "aportacion": aportacion or "",
        "tipo": aportacion_tipo or "mensual",
        "anios": anios or "",
        "rent": rentabilidad or "",
        "infl": inflacion or "",
        "fee": comision or "",
        "escenario": scenario or "base",
    }
    return f"https://interescompuesto.app/calculadora?{urlencode(params)}"


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
    Output("ic-donut", "figure"),
    Output("ic-insights", "children"),
    Output("ic-breakdown-bars", "figure"),
    Output("ic-cash-comparison-copy", "children"),
    Output("ic-advice-block", "children"),
    Output("ic-evolucion-store", "data"),
    Input("ic-boton", "n_clicks"),
    Input("ic-capital-inicial", "value"),
    Input("ic-aportacion", "value"),
    Input("ic-aportacion-tipo", "value"),
    Input("ic-anios", "value"),
    Input("ic-rentabilidad", "value"),
    Input("ic-inflacion", "value"),
    Input("ic-comision", "value"),
    Input("ic-scenario", "value"),
)
def actualizar_calculadora(
    _,
    capital_inicial,
    aportacion_input,
    aportacion_tipo,
    anios,
    rentabilidad,
    inflacion,
    comision,
    scenario,
):
    capital_inicial = parse_number(capital_inicial)
    aportacion_raw = parse_number(aportacion_input)
    anios = int(anios or 0)
    rentabilidad_pct = parse_number(rentabilidad)
    inflacion_pct = parse_number(inflacion)
    comision_pct = parse_number(comision)

    rentabilidad = rentabilidad_pct / 100
    inflacion = inflacion_pct / 100
    comision = comision_pct / 100

    aportacion_mensual = aportacion_raw / 12 if aportacion_tipo == "anual" else aportacion_raw
    aportacion_anual_equiv = aportacion_mensual * 12

    evolucion = calcular_interes_compuesto(
        capital_inicial=capital_inicial,
        aportacion_mensual=aportacion_mensual,
        años=anios,
        rentabilidad_anual=rentabilidad,
        inflacion=inflacion,
        comision=comision,
    )

    if not evolucion:
        empty = html.Div()
        empty_fig = build_empty_figure("Introduce datos válidos para ver la evolución")
        return (
            summary_stat_card("Capital inicial", "0 €"),
            summary_stat_card("Aportación", "0 €"),
            summary_stat_card("Rentabilidad", "0 %"),
            summary_stat_card("Horizonte", "0 años"),
            metric_card("Valor final", "0 €", "Estimación nominal final"),
            metric_card("Total aportado", "0 €", "Lo que habrías invertido"),
            metric_card("Ganancia potencial", "0 €", "Crecimiento estimado"),
            empty_fig,
            "",
            "",
            "",
            "",
            empty,
            build_empty_figure("Calcula tu simulación para ver la composición final", height=320),
            "",
            build_empty_figure("Calcula tu simulación para comparar alternativas", height=360),
            "",
            "",
            [],
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
        aportacion_mensual=aportacion_mensual + 100,
        años=anios,
        rentabilidad_anual=rentabilidad,
        inflacion=inflacion,
        comision=comision,
    )

    evolucion_200 = calcular_interes_compuesto(
        capital_inicial=capital_inicial,
        aportacion_mensual=aportacion_mensual + 200,
        años=anios,
        rentabilidad_anual=rentabilidad,
        inflacion=inflacion,
        comision=comision,
    )

    valor_100 = evolucion_100[-1]["total"] if evolucion_100 else 0
    valor_200 = evolucion_200[-1]["total"] if evolucion_200 else 0

    diferencia_100 = valor_100 - valor_final
    diferencia_200 = valor_200 - valor_final

    anios_espera = 5
    anios_retrasados = max(anios - anios_espera, 0)

    evolucion_tarde = (
        calcular_interes_compuesto(
            capital_inicial=capital_inicial,
            aportacion_mensual=aportacion_mensual,
            años=anios_retrasados,
            rentabilidad_anual=rentabilidad,
            inflacion=inflacion,
            comision=comision,
        )
        if anios_retrasados > 0
        else []
    )

    valor_tarde = evolucion_tarde[-1]["total"] if evolucion_tarde else 0
    diferencia_por_esperar = valor_final - valor_tarde

    evolucion_cash = cash_evolution(
        capital_inicial=capital_inicial,
        aportacion_mensual=aportacion_mensual,
        anios=anios,
        inflacion=inflacion,
    )
    valor_cash = evolucion_cash[-1]["total"] if evolucion_cash else capital_inicial
    diferencia_vs_cash = valor_final - valor_cash

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
    fig.update_xaxes(showgrid=False, zeroline=False, tickfont=dict(size=12), title_font=dict(size=13))
    fig.update_yaxes(gridcolor="rgba(15, 23, 42, 0.08)", zeroline=False, tickfont=dict(size=12), title_font=dict(size=13))

    donut = build_donut_figure(total_aportado, ganancia)
    bar_fig = build_breakdown_bars(total_aportado, ganancia, valor_cash)

    quick_1 = summary_stat_card(
        "Capital inicial",
        formatear_euros_es(capital_inicial),
        "Punto de partida",
    )
    quick_2 = summary_stat_card(
        "Aportación",
        formatear_euros_es(aportacion_raw),
        "Mensual" if aportacion_tipo == "mensual" else "Anual",
    )
    quick_3 = summary_stat_card(
        "Rentabilidad anual",
        f"{rentabilidad_pct:.2f} %",
        f"Escenario: {scenario.capitalize()}",
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
                    },
                ),
                html.P(
                    f"Habrías aportado {formatear_euros_es(total_aportado)} y el crecimiento potencial sería de {formatear_euros_es(ganancia)}.",
                    className="mb-0",
                    style={
                        "fontSize": "1rem",
                        "color": "#475467",
                        "lineHeight": "1.7",
                    },
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
                            f"{formatear_euros_es(aportacion_mensual)} al mes ({formatear_euros_es(aportacion_anual_equiv)} al año)",
                            False,
                        ),
                        md=4,
                        className="mb-3",
                    ),
                    dbc.Col(
                        scenario_card(
                            "+100 €/mes",
                            formatear_euros_es(valor_100),
                            f"{formatear_euros_es(diferencia_100)} más frente al escenario actual",
                            True,
                        ),
                        md=4,
                        className="mb-3",
                    ),
                    dbc.Col(
                        scenario_card(
                            "+200 €/mes",
                            formatear_euros_es(valor_200),
                            f"{formatear_euros_es(diferencia_200)} más frente al escenario actual",
                            True,
                        ),
                        md=4,
                        className="mb-3",
                    ),
                ]
            ),
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
                                if anios_retrasados > 0
                                else "No hay horizonte suficiente para comparar"
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

    porcentaje_ganancia = (ganancia / total_aportado * 100) if total_aportado > 0 else 0
    multiple_capital = (valor_final / capital_inicial) if capital_inicial > 0 else 0

    insights = dbc.Card(
        dbc.CardBody(
            [
                section_eyebrow("Insights clave"),
                html.H4(
                    "Lecturas rápidas de tu simulación",
                    className="fw-bold mb-3",
                    style={"color": "#0f172a"},
                ),
                html.Ul(
                    [
                        html.Li(
                            f"Tu aportación equivalente sería de {formatear_euros_es(aportacion_anual_equiv)} al año."
                        ),
                        html.Li(
                            f"El crecimiento estimado representa aproximadamente un {porcentaje_ganancia:.1f} % sobre lo aportado."
                        ),
                        html.Li(
                            f"El capital final sería unas {multiple_capital:.2f} veces tu capital inicial."
                            if capital_inicial > 0
                            else "No se puede calcular el múltiplo sobre capital inicial porque es 0."
                        ),
                        html.Li(
                            "A horizontes largos, el tiempo y la constancia suelen pesar más que intentar acertar el momento perfecto."
                        ),
                    ],
                    style={
                        "paddingLeft": "1.2rem",
                        "marginBottom": "0",
                        "color": "#475467",
                        "lineHeight": "1.8",
                        "fontSize": "1rem",
                    },
                ),
            ]
        ),
        className="border-0 rounded-4",
        style={
            "background": "#ffffff",
            "boxShadow": "0 14px 36px rgba(16, 24, 40, 0.06)",
        },
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
                "Subir ligeramente la aportación periódica puede producir una diferencia muy significativa cuando se mantiene durante años."
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
        },
    )

    cash_copy = html.P(
        (
            f"Con esta simulación, invertir te llevaría a {formatear_euros_es(valor_final)}, "
            f"frente a {formatear_euros_es(valor_cash)} si simplemente fueras acumulando el dinero sin rentabilidad. "
            f"La diferencia sería de {formatear_euros_es(diferencia_vs_cash)}."
        ),
        className="mb-0 mt-3",
        style={"color": "#475467", "lineHeight": "1.7"},
    )

    tabla_anual = build_yearly_table(evolucion)
    advice_block = build_advice_block(valor_final, total_aportado, anios, aportacion_mensual, ganancia)

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
        donut,
        insights,
        bar_fig,
        cash_copy,
        advice_block,
        evolucion,
    )


# =========================================================
# DESCARGA CSV
# =========================================================
@callback(
    Output("ic-download-csv", "data"),
    Input("ic-download-btn", "n_clicks"),
    State("ic-evolucion-store", "data"),
    prevent_initial_call=True,
)
def descargar_csv(n_clicks, evolucion_data):
    if not n_clicks or not evolucion_data:
        return dash.no_update

    df = evolution_to_dataframe(evolucion_data)
    return dcc.send_data_frame(df.to_csv, "simulacion_interes_compuesto.csv", index=False)


# =========================================================
# SCROLL SUAVE AL RESULTADO
# =========================================================
clientside_callback(
    """
    function(n_clicks) {
        if (!n_clicks) {
            return window.dash_clientside.no_update;
        }

        setTimeout(function() {
            const target = document.getElementById("resultado-anchor");
            if (target) {
                target.scrollIntoView({ behavior: "smooth", block: "start" });
            }
        }, 150);

        return "";
    }
    """,
    Output("scroll-trigger", "children"),
    Input("btn-calcular", "n_clicks"),
)


# =========================================================
# SCROLL A LA CALCULADORA DESDE HERO CTA
# =========================================================
clientside_callback(
    """
    function(n_clicks) {
        if (!n_clicks) {
            return window.dash_clientside.no_update;
        }

        setTimeout(function() {
            const target = document.getElementById("calculadora-anchor");
            if (target) {
                target.scrollIntoView({ behavior: "smooth", block: "start" });
            }
        }, 100);

        return "";
    }
    """,
    Output("scroll-calculadora-trigger", "children"),
    Input("btn-ir-calculadora", "n_clicks"),
)


# =========================================================
# AUTORRELLENO DE EJEMPLO
# =========================================================
@callback(
    Output("capital-inicial", "value"),
    Output("aportacion-mensual", "value"),
    Output("rentabilidad-anual", "value"),
    Output("anos", "value"),
    Output("inflacion-anual", "value"),
    Input("btn-ejemplo", "n_clicks"),
    prevent_initial_call=True,
)
def cargar_ejemplo(n_clicks):
    if not n_clicks:
        return dash.no_update

    return "10.000", "300", "7", "20", "2"


# =========================================================
# RESET FORM
# =========================================================
@callback(
    Output("capital-inicial", "value", allow_duplicate=True),
    Output("aportacion-mensual", "value", allow_duplicate=True),
    Output("rentabilidad-anual", "value", allow_duplicate=True),
    Output("anos", "value", allow_duplicate=True),
    Output("inflacion-anual", "value", allow_duplicate=True),
    Input("btn-reset", "n_clicks"),
    prevent_initial_call=True,
)
def reset_form(n_clicks):
    if not n_clicks:
        return dash.no_update

    return "10.000", "300", "7", "20", "2"
