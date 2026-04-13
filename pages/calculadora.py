from urllib.parse import urlencode, parse_qs

import numpy as np
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
    no_update,
    ALL,
)
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

from utils.premium import (
    is_premium_unlocked,
    premium_cta_card,
    premium_active_alert,
)
from helpers import (
    parse_number,
    calcular_interes_compuesto,
    formatear_euros_es,
)
from utils.simulations import add_simulation, delete_simulation, normalize_store
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
        ganancia = item.get("ganado", total - aportado)
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
        ganancia = item.get("ganado", total - aportado)
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
# HELPERS CÁLCULO
# =========================================================
def get_aportacion_mensual(aportacion, aportacion_tipo):
    aportacion = max(parse_number(aportacion), 0)
    return aportacion if aportacion_tipo == "mensual" else (aportacion / 12)


def build_main_figure(evolucion):
    if not evolucion:
        return build_empty_figure(
            "La simulación se actualiza automáticamente con tus datos"
        )

    x = [x["año"] for x in evolucion]
    aportado = [x["aportado"] for x in evolucion]
    total = [x["total"] for x in evolucion]
    real = [x["real"] for x in evolucion]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=x,
            y=aportado,
            mode="lines",
            name="Aportado",
            hovertemplate="Año %{x}<br>Aportado: %{y:,.2f} €<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x,
            y=total,
            mode="lines",
            name="Valor total",
            hovertemplate="Año %{x}<br>Total: %{y:,.2f} €<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x,
            y=real,
            mode="lines",
            name="Valor real",
            line=dict(dash="dash"),
            hovertemplate="Año %{x}<br>Valor real: %{y:,.2f} €<extra></extra>",
        )
    )

    fig.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=20, b=10),
        height=440,
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend=dict(orientation="h", y=1.06, x=0),
        xaxis_title="Años",
        yaxis_title="Euros",
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(15, 23, 42, 0.08)", zeroline=False)
    return fig


def build_interpretation(valor_final, valor_real_final, aportado, ganancia, anios):
    ratio_ganancia = (ganancia / aportado) if aportado > 0 else 0

    bloques = [
        html.P(
            f"En esta simulación acabarías con aproximadamente {formatear_euros_es(valor_final)} tras {anios} años.",
            style={"color": "#475467", "lineHeight": "1.8"},
        ),
        html.P(
            f"Habrías aportado {formatear_euros_es(aportado)} y el crecimiento estimado sería de {formatear_euros_es(ganancia)}.",
            style={"color": "#475467", "lineHeight": "1.8"},
        ),
        html.P(
            f"Ajustando por inflación, el valor real estimado sería de {formatear_euros_es(valor_real_final)}.",
            style={"color": "#475467", "lineHeight": "1.8"},
        ),
    ]

    if ratio_ganancia >= 0.5:
        bloques.append(
            html.P(
                "Aquí el interés compuesto ya tiene bastante peso: el crecimiento acumulado aporta una parte relevante del resultado final.",
                style={"color": "#475467", "lineHeight": "1.8"},
            )
        )
    else:
        bloques.append(
            html.P(
                "Todavía domina más lo que tú aportas que lo que genera la rentabilidad, algo totalmente normal en horizontes más cortos.",
                style={"color": "#475467", "lineHeight": "1.8"},
            )
        )

    return html.Div(bloques)


def build_emotional_message(valor_final, anios):
    if valor_final < 50000:
        return dbc.Alert(
            f"En {anios} años estarías construyendo una base interesante, pero la clave aquí sigue siendo la constancia.",
            color="light",
            className="rounded-4 border-0",
        )
    if valor_final < 200000:
        return dbc.Alert(
            f"En {anios} años ya tendrías una cifra seria. Aquí el tiempo empieza a jugar muy a tu favor.",
            color="success",
            className="rounded-4 border-0",
        )
    return dbc.Alert(
        "Esta simulación ya entra en una zona potente: el interés compuesto y el tiempo empiezan a hacer mucho trabajo por ti.",
        color="success",
        className="rounded-4 border-0 fw-semibold",
    )


def build_scenarios_comparison(capital_inicial, aportacion_mensual, anios):
    escenarios = [
        ("Conservador", 0.04, 0.02, 0.0030),
        ("Base", 0.07, 0.02, 0.0020),
        ("Optimista", 0.09, 0.02, 0.0015),
    ]

    cards = []
    for nombre, rent, infl, fee in escenarios:
        evolucion = calcular_interes_compuesto(
            capital_inicial=capital_inicial,
            aportacion_mensual=aportacion_mensual,
            años=anios,
            rentabilidad_anual=rent,
            inflacion=infl,
            comision=fee,
        )
        if evolucion:
            valor_final = evolucion[-1]["total"]
            valor_real = evolucion[-1]["real"]
        else:
            valor_final = capital_inicial
            valor_real = capital_inicial

        cards.append(
            dbc.Col(
                scenario_card(
                    nombre,
                    formatear_euros_es(valor_final),
                    f"Valor real aprox.: {formatear_euros_es(valor_real)}",
                    highlight=(nombre == "Base"),
                ),
                md=4,
                className="mb-3",
            )
        )

    return dbc.Card(
        dbc.CardBody(
            [
                section_eyebrow("Escenarios"),
                html.H4(
                    "Cómo cambia el resultado según el escenario",
                    className="fw-bold mb-3",
                    style={"color": "#0f172a"},
                ),
                dbc.Row(cards),
            ]
        ),
        className="border-0 rounded-4",
        style={
            "background": "#ffffff",
            "boxShadow": "0 14px 36px rgba(16, 24, 40, 0.06)",
        },
    )


def build_start_delay_comparison(capital_inicial, aportacion_mensual, anios, rentabilidad, inflacion, comision):
    anios_tarde = max(anios - 5, 1)

    actual = calcular_interes_compuesto(
        capital_inicial=capital_inicial,
        aportacion_mensual=aportacion_mensual,
        años=anios,
        rentabilidad_anual=rentabilidad,
        inflacion=inflacion,
        comision=comision,
    )

    tarde = calcular_interes_compuesto(
        capital_inicial=capital_inicial,
        aportacion_mensual=aportacion_mensual,
        años=anios_tarde,
        rentabilidad_anual=rentabilidad,
        inflacion=inflacion,
        comision=comision,
    )

    actual_final = actual[-1]["total"] if actual else capital_inicial
    tarde_final = tarde[-1]["total"] if tarde else capital_inicial
    diferencia = actual_final - tarde_final

    return dbc.Card(
        dbc.CardBody(
            [
                section_eyebrow("Empezar antes"),
                html.H4(
                    "Qué te cuesta retrasar 5 años la decisión",
                    className="fw-bold mb-3",
                    style={"color": "#0f172a"},
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            summary_stat_card(
                                "Si empiezas ahora",
                                formatear_euros_es(actual_final),
                                f"{anios} años de inversión",
                            ),
                            md=4,
                            className="mb-3",
                        ),
                        dbc.Col(
                            summary_stat_card(
                                "Si empiezas 5 años más tarde",
                                formatear_euros_es(tarde_final),
                                f"{anios_tarde} años de inversión",
                            ),
                            md=4,
                            className="mb-3",
                        ),
                        dbc.Col(
                            summary_stat_card(
                                "Diferencia",
                                formatear_euros_es(diferencia),
                                "Impacto aproximado del retraso",
                            ),
                            md=4,
                            className="mb-3",
                        ),
                    ]
                ),
            ]
        ),
        className="border-0 rounded-4",
        style={
            "background": "#ffffff",
            "boxShadow": "0 14px 36px rgba(16, 24, 40, 0.06)",
        },
    )


def build_insights_block(valor_final, total_aportado, ganancia):
    ratio = (ganancia / total_aportado) if total_aportado > 0 else 0
    fee_impact_msg = (
        "Las comisiones merecen mucha atención aquí: a largo plazo restan una cantidad importante."
        if valor_final > 150000
        else "Aunque el patrimonio aún no es enorme, vigilar comisiones sigue siendo buena idea."
    )

    yearly_income_4pct = valor_final * 0.04
    monthly_income_4pct = yearly_income_4pct / 12

    cards = [
        dbc.Col(
            summary_stat_card(
                "Renta anual al 4%",
                formatear_euros_es(yearly_income_4pct),
                "Referencia orientativa",
            ),
            md=4,
            className="mb-3",
        ),
        dbc.Col(
            summary_stat_card(
                "Renta mensual al 4%",
                formatear_euros_es(monthly_income_4pct),
                "Referencia orientativa",
            ),
            md=4,
            className="mb-3",
        ),
        dbc.Col(
            summary_stat_card(
                "Peso del crecimiento",
                f"{ratio * 100:.1f}%",
                "Sobre lo aportado",
            ),
            md=4,
            className="mb-3",
        ),
    ]

    return dbc.Card(
        dbc.CardBody(
            [
                section_eyebrow("Insights"),
                html.H4(
                    "Lecturas útiles de tu resultado",
                    className="fw-bold mb-3",
                    style={"color": "#0f172a"},
                ),
                dbc.Row(cards),
                html.P(
                    fee_impact_msg,
                    style={"color": "#475467", "lineHeight": "1.8"},
                    className="mb-2",
                ),
                html.P(
                    "La regla del 4% es solo una referencia orientativa, no una recomendación cerrada.",
                    style={"color": "#667085", "lineHeight": "1.7"},
                    className="mb-0",
                ),
            ]
        ),
        className="border-0 rounded-4",
        style={
            "background": "#ffffff",
            "boxShadow": "0 14px 36px rgba(16, 24, 40, 0.06)",
        },
    )


# =========================================================
# MONTE CARLO
# =========================================================
def first_year_reaching_target(series, target):
    if target is None or target <= 0:
        return None
    for i, value in enumerate(series):
        if value >= target:
            return i
    return None


def montecarlo_interes_compuesto(
    capital_inicial,
    aportacion_mensual,
    anios,
    rentabilidad_media_anual,
    volatilidad_anual,
    inflacion_anual,
    comision_anual,
    n_simulaciones=2000,
    seed=42,
):
    meses = int(anios * 12)
    if meses <= 0:
        return None

    rng = np.random.default_rng(seed)

    rentabilidad_media_mensual = (1 + rentabilidad_media_anual) ** (1 / 12) - 1
    volatilidad_mensual = volatilidad_anual / np.sqrt(12)
    inflacion_mensual = (1 + inflacion_anual) ** (1 / 12) - 1 if inflacion_anual > -1 else 0.0
    comision_mensual = comision_anual / 12

    retornos_mensuales = rng.normal(
        loc=rentabilidad_media_mensual,
        scale=volatilidad_mensual,
        size=(n_simulaciones, meses),
    )

    capitales = np.zeros((n_simulaciones, meses + 1))
    capitales[:, 0] = capital_inicial

    for mes in range(1, meses + 1):
        capitales[:, mes] = capitales[:, mes - 1] * (1 + retornos_mensuales[:, mes - 1])
        capitales[:, mes] += aportacion_mensual
        capitales[:, mes] *= (1 - comision_mensual)
        capitales[:, mes] = np.clip(capitales[:, mes], 0, None)

    year_points = [0] + [12 * i for i in range(1, anios + 1)]
    paths_yearly = capitales[:, year_points]

    real_paths = np.zeros_like(paths_yearly)
    for i, year in enumerate(range(0, anios + 1)):
        factor_inflacion = (1 + inflacion_mensual) ** (year * 12) if inflacion_mensual > -1 else 1
        real_paths[:, i] = paths_yearly[:, i] / factor_inflacion if factor_inflacion != 0 else paths_yearly[:, i]

    p10 = np.percentile(paths_yearly, 10, axis=0)
    p50 = np.percentile(paths_yearly, 50, axis=0)
    p90 = np.percentile(paths_yearly, 90, axis=0)

    real_p10 = np.percentile(real_paths, 10, axis=0)
    real_p50 = np.percentile(real_paths, 50, axis=0)
    real_p90 = np.percentile(real_paths, 90, axis=0)

    return {
        "years": list(range(0, anios + 1)),
        "paths": paths_yearly,
        "real_paths": real_paths,
        "final_values": paths_yearly[:, -1],
        "real_final_values": real_paths[:, -1],
        "p10": p10,
        "p50": p50,
        "p90": p90,
        "real_p10": real_p10,
        "real_p50": real_p50,
        "real_p90": real_p90,
    }


def build_montecarlo_fan_chart(mc_result):
    if not mc_result:
        return build_empty_figure("Activa el modo premium para ver la simulación Monte Carlo", height=420)

    years = mc_result["years"]
    p10 = mc_result["p10"]
    p50 = mc_result["p50"]
    p90 = mc_result["p90"]
    real_p50 = mc_result["real_p50"]

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=years,
            y=p90,
            mode="lines",
            line=dict(width=0),
            name="Percentil 90",
            hovertemplate="Año %{x}<br>P90: %{y:,.0f} €<extra></extra>",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years,
            y=p10,
            mode="lines",
            fill="tonexty",
            name="Rango 10-90",
            hovertemplate="Año %{x}<br>P10: %{y:,.0f} €<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years,
            y=p50,
            mode="lines",
            name="Percentil 50",
            hovertemplate="Año %{x}<br>Mediana: %{y:,.0f} €<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years,
            y=real_p50,
            mode="lines",
            name="Mediana real",
            line=dict(dash="dash"),
            hovertemplate="Año %{x}<br>Mediana real: %{y:,.0f} €<extra></extra>",
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=420,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        legend=dict(orientation="h", y=1.06, x=0),
        yaxis_title="Euros",
        xaxis_title="Años",
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(15, 23, 42, 0.08)", zeroline=False)
    return fig


def build_montecarlo_histogram(mc_result):
    if not mc_result:
        return build_empty_figure("Activa el modo premium para ver la distribución final", height=360)

    final_values = mc_result["final_values"]

    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=final_values,
            nbinsx=35,
            hovertemplate="%{x:,.0f} €<br>Frecuencia: %{y}<extra></extra>",
            name="Distribución final",
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=360,
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="white",
        plot_bgcolor="white",
        xaxis_title="Valor final",
        yaxis_title="Frecuencia",
        showlegend=False,
    )
    fig.update_xaxes(gridcolor="rgba(15, 23, 42, 0.08)")
    fig.update_yaxes(gridcolor="rgba(15, 23, 42, 0.08)", zeroline=False)
    return fig


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
                                        premium_badge("Monte Carlo premium"),
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
                                html.Hr(className="my-4"),
                                section_eyebrow("Premium"),
                                dbc.Switch(
                                    id="ic-premium-mode",
                                    label="Activar análisis Monte Carlo",
                                    value=False,
                                    className="mb-3",
                                ),
                                html.Div(id="ic-premium-lock-note", className="mb-3"),
                                html.Div(
                                    [
                                        input_group(
                                            "Volatilidad anual",
                                            "ic-volatilidad",
                                            "15",
                                            "text",
                                            "Ejemplo orientativo para renta variable global",
                                            suffix="%",
                                        ),
                                        input_group(
                                            "Número de simulaciones",
                                            "ic-n-simulaciones",
                                            "2000",
                                            "number",
                                            "Más simulaciones = resultado más estable, pero algo más lento",
                                        ),
                                        input_group(
                                            "Objetivo de patrimonio",
                                            "ic-objetivo",
                                            "500000",
                                            "text",
                                            "Para calcular la probabilidad de alcanzar una meta",
                                            suffix="€",
                                        ),
                                    ],
                                    id="ic-premium-controls",
                                ),
                                dbc.Button(
                                    "Ver resultados",
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
                                                        "La simulación se actualiza automáticamente",
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
                                            "La simulación se actualiza automáticamente con tus datos"
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
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    section_eyebrow("Premium · Monte Carlo"),
                                    html.H4(
                                        "Rango probable de resultados",
                                        className="fw-bold mb-2",
                                        style={"color": "#0f172a"},
                                    ),
                                    html.P(
                                        "En lugar de asumir una rentabilidad fija todos los años, Monte Carlo simula muchos caminos posibles con volatilidad.",
                                        className="mb-3",
                                        style={"color": "#667085"},
                                    ),
                                    html.Div(id="ic-premium-summary", className="mb-4"),
                                    dcc.Graph(
                                        id="ic-montecarlo-chart",
                                        figure=build_empty_figure("Activa premium para ver el rango de resultados", height=420),
                                        config={"displayModeBar": False},
                                    ),
                                    dcc.Graph(
                                        id="ic-montecarlo-hist",
                                        figure=build_empty_figure("Activa premium para ver la distribución final", height=360),
                                        config={"displayModeBar": False},
                                    ),
                                    html.Div(id="ic-premium-goal"),
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
                                            "La simulación se actualiza automáticamente",
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
                                                    readonly=True,
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
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Div("Guardar simulación", className="fw-bold mb-2"),
                                    dbc.Input(
                                        id="save-simulation-name",
                                        placeholder="Ej: Escenario 7% a 25 años",
                                        className="mb-3",
                                    ),
                                    dbc.Button(
                                        "Guardar",
                                        id="save-simulation-btn",
                                        color="primary",
                                        className="rounded-pill fw-semibold",
                                        n_clicks=0,
                                    ),
                                    html.Div(id="save-simulation-message", className="mt-3"),
                                ]
                            ),
                            className="border-0 shadow-sm rounded-4 mb-4",
                        ),
                        html.Div(id="saved-simulations-list"),
                    ],
                    lg=12,
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
# CLIENTSIDE
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
# PRECARGA URL
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
)
def load_from_url(search):
    if not search:
        return "10000", "300", "mensual", "20", "7", "2", "0.2", "base"

    params = parse_qs(search.lstrip("?"))

    capital = params.get("capital", ["10000"])[0]
    aportacion = params.get("aportacion", ["300"])[0]
    tipo = params.get("tipo", ["mensual"])[0]
    anios = params.get("anios", ["20"])[0]
    rent = params.get("rent", ["7"])[0]
    infl = params.get("infl", ["2"])[0]
    fee = params.get("fee", ["0.2"])[0]
    escenario = params.get("escenario", ["base"])[0]

    return capital, aportacion, tipo, anios, rent, infl, fee, escenario


# =========================================================
# ESCENARIO
# =========================================================
@callback(
    Output("ic-rentabilidad", "value", allow_duplicate=True),
    Output("ic-inflacion", "value", allow_duplicate=True),
    Output("ic-comision", "value", allow_duplicate=True),
    Input("ic-scenario", "value"),
    prevent_initial_call=True,
)
def update_scenario_defaults(scenario):
    defaults = scenario_defaults(scenario)
    return defaults["rentabilidad"], defaults["inflacion"], defaults["comision"]


# =========================================================
# PREMIUM LOCK NOTE
# =========================================================
@callback(
    Output("ic-premium-lock-note", "children"),
    Input("premium-access", "data"),
)
def render_premium_lock_note(access_data):
    unlocked = is_premium_unlocked(access_data)

    if unlocked:
        return premium_active_alert()

    return premium_cta_card()

# =========================================================
# CÁLCULO PRINCIPAL
# =========================================================
@callback(
    Output("ic-quick-stat-1", "children"),
    Output("ic-quick-stat-2", "children"),
    Output("ic-quick-stat-3", "children"),
    Output("ic-quick-stat-4", "children"),
    Output("ic-resultado-final", "children"),
    Output("ic-total-aportado", "children"),
    Output("ic-ganancia", "children"),
    Output("ic-mensaje-emocional", "children"),
    Output("ic-interpretacion", "children"),
    Output("ic-donut", "figure"),
    Output("ic-grafico", "figure"),
    Output("ic-comparativa", "children"),
    Output("ic-start-delay-comparison", "children"),
    Output("ic-insights", "children"),
    Output("ic-breakdown-bars", "figure"),
    Output("ic-cash-comparison-copy", "children"),
    Output("ic-advice-block", "children"),
    Output("ic-tabla-anual", "children"),
    Output("ic-share-link", "value"),
    Output("ic-evolucion-store", "data"),
    Input("ic-capital-inicial", "value"),
    Input("ic-aportacion", "value"),
    Input("ic-aportacion-tipo", "value"),
    Input("ic-anios", "value"),
    Input("ic-rentabilidad", "value"),
    Input("ic-inflacion", "value"),
    Input("ic-comision", "value"),
    Input("ic-scenario", "value"),
)
def calcular_simulacion(
    capital_inicial,
    aportacion,
    aportacion_tipo,
    anios,
    rentabilidad,
    inflacion,
    comision,
    scenario,
):
    try:
        capital_inicial_num = max(parse_number(capital_inicial), 0)
        aportacion_mensual = get_aportacion_mensual(aportacion, aportacion_tipo)
        anios_num = int(parse_number(anios))
        rentabilidad_num = parse_number(rentabilidad) / 100
        inflacion_num = parse_number(inflacion) / 100
        comision_num = parse_number(comision) / 100

        if anios_num <= 0:
            raise ValueError("El horizonte temporal debe ser mayor que 0.")

        evolucion = calcular_interes_compuesto(
            capital_inicial=capital_inicial_num,
            aportacion_mensual=aportacion_mensual,
            años=anios_num,
            rentabilidad_anual=rentabilidad_num,
            inflacion=inflacion_num,
            comision=comision_num,
        )

        valor_final = evolucion[-1]["total"] if evolucion else capital_inicial_num
        valor_real_final = evolucion[-1]["real"] if evolucion else capital_inicial_num
        total_aportado = evolucion[-1]["aportado"] if evolucion else capital_inicial_num
        ganancia = evolucion[-1].get("ganado", valor_final - total_aportado) if evolucion else 0

        cash_evo = cash_evolution(
            capital_inicial=capital_inicial_num,
            aportacion_mensual=aportacion_mensual,
            anios=anios_num,
            inflacion=inflacion_num,
        )
        cash_value = cash_evo[-1]["total"] if cash_evo else capital_inicial_num
        diff_vs_cash = valor_final - cash_value

        rentabilidad_neta = (rentabilidad_num - comision_num) * 100
        multiplicador = (valor_final / total_aportado) if total_aportado > 0 else 0
        poder_adquisitivo = (valor_real_final / valor_final) if valor_final > 0 else 0
        ganancia_pct = (ganancia / total_aportado) * 100 if total_aportado > 0 else 0

        quick1 = summary_stat_card(
            "Rentabilidad neta",
            f"{rentabilidad_neta:.2f}%",
            "Rentabilidad - comisión",
        )
        quick2 = summary_stat_card(
            "Valor real final",
            formatear_euros_es(valor_real_final),
            "Ajustado por inflación",
        )
        quick3 = summary_stat_card(
            "Multiplicador",
            f"{multiplicador:.2f}x",
            "Sobre lo aportado",
        )
        quick4 = summary_stat_card(
            "Poder adquisitivo",
            f"{poder_adquisitivo * 100:.1f}%",
            "Del valor nominal final",
        )

        resultado_final_card = metric_card(
            "Valor final estimado",
            formatear_euros_es(valor_final),
            "Capital acumulado al final del periodo",
            highlight=True,
        )
        total_aportado_card = metric_card(
            "Total aportado",
            formatear_euros_es(total_aportado),
            "Capital puesto por ti",
        )
        ganancia_card = metric_card(
            "Ganancia estimada",
            formatear_euros_es(ganancia),
            f"{ganancia_pct:.1f}% sobre lo aportado",
            highlight=ganancia > 0,
        )

        emotional = build_emotional_message(valor_final, anios_num)
        interpretation = build_interpretation(
            valor_final=valor_final,
            valor_real_final=valor_real_final,
            aportado=total_aportado,
            ganancia=ganancia,
            anios=anios_num,
        )
        donut = build_donut_figure(total_aportado, ganancia)
        grafico = build_main_figure(evolucion)
        comparativa = build_scenarios_comparison(
            capital_inicial=capital_inicial_num,
            aportacion_mensual=aportacion_mensual,
            anios=anios_num,
        )
        delay_comparison = build_start_delay_comparison(
            capital_inicial=capital_inicial_num,
            aportacion_mensual=aportacion_mensual,
            anios=anios_num,
            rentabilidad=rentabilidad_num,
            inflacion=inflacion_num,
            comision=comision_num,
        )
        insights = build_insights_block(
            valor_final=valor_final,
            total_aportado=total_aportado,
            ganancia=ganancia,
        )
        breakdown = build_breakdown_bars(total_aportado, ganancia, cash_value)

        cash_copy = dbc.Alert(
            f"Frente a dejar el dinero parado, la diferencia estimada sería de {formatear_euros_es(diff_vs_cash)}.",
            color="success" if diff_vs_cash > 0 else "light",
            className="rounded-4 border-0 mt-3",
        )

        advice_block = build_advice_block(
            valor_final=valor_final,
            total_aportado=total_aportado,
            anios=anios_num,
            aportacion_mensual=aportacion_mensual,
            ganancia=ganancia,
        )

        tabla = build_yearly_table(evolucion)

        share_params = urlencode(
            {
                "capital": capital_inicial,
                "aportacion": aportacion,
                "tipo": aportacion_tipo,
                "anios": anios,
                "rent": rentabilidad,
                "infl": inflacion,
                "fee": comision,
                "escenario": scenario,
            }
        )
        share_link = f"/calculadora?{share_params}"

        return (
            quick1,
            quick2,
            quick3,
            quick4,
            resultado_final_card,
            total_aportado_card,
            ganancia_card,
            emotional,
            interpretation,
            donut,
            grafico,
            comparativa,
            delay_comparison,
            insights,
            breakdown,
            cash_copy,
            advice_block,
            tabla,
            share_link,
            evolucion,
        )

    except Exception as e:
        error_alert = dbc.Alert(
            f"No se pudo calcular la simulación: {e}",
            color="danger",
            className="rounded-4 border-0",
        )
        empty_metric = metric_card("Error", "—", "Revisa los datos")
        empty_fig = build_empty_figure("No se pudo generar la simulación")

        return (
            empty_metric,
            empty_metric,
            empty_metric,
            empty_metric,
            empty_metric,
            empty_metric,
            empty_metric,
            error_alert,
            html.Div(),
            build_empty_figure("Error en la composición final", height=320),
            empty_fig,
            html.Div(),
            html.Div(),
            html.Div(),
            build_empty_figure("Error en la comparativa", height=360),
            html.Div(),
            html.Div(),
            html.Div(),
            "",
            None,
        )


# =========================================================
# MONTE CARLO PREMIUM
# =========================================================
@callback(
    Output("ic-premium-summary", "children"),
    Output("ic-montecarlo-chart", "figure"),
    Output("ic-montecarlo-hist", "figure"),
    Output("ic-premium-goal", "children"),
    Input("premium-access", "data"),
    Input("ic-premium-mode", "value"),
    Input("ic-capital-inicial", "value"),
    Input("ic-aportacion", "value"),
    Input("ic-aportacion-tipo", "value"),
    Input("ic-anios", "value"),
    Input("ic-rentabilidad", "value"),
    Input("ic-inflacion", "value"),
    Input("ic-comision", "value"),
    Input("ic-volatilidad", "value"),
    Input("ic-n-simulaciones", "value"),
    Input("ic-objetivo", "value"),
)
def calcular_montecarlo_premium(
    access_data,
    premium_mode,
    capital_inicial,
    aportacion,
    aportacion_tipo,
    anios,
    rentabilidad,
    inflacion,
    comision,
    volatilidad,
    n_simulaciones,
    objetivo,
):
    unlocked = is_premium_unlocked(access_data)

    if not premium_mode:
        return (
            dbc.Alert(
                "Activa el interruptor de Monte Carlo para ver el análisis premium.",
                color="light",
                className="rounded-4 border-0",
            ),
            build_empty_figure("Activa el análisis Monte Carlo", height=420),
            build_empty_figure("Activa el análisis Monte Carlo", height=360),
            html.Div(),
        )

    if not unlocked:
        return (
            premium_cta_card(),
            build_empty_figure("Monte Carlo disponible en premium", height=420),
            build_empty_figure("Distribución final disponible en premium", height=360),
            html.Div(),
        )

    try:
        capital_inicial_num = max(parse_number(capital_inicial), 0)
        aportacion_mensual = get_aportacion_mensual(aportacion, aportacion_tipo)
        anios_num = int(parse_number(anios))
        rentabilidad_num = parse_number(rentabilidad) / 100
        inflacion_num = parse_number(inflacion) / 100
        comision_num = parse_number(comision) / 100
        volatilidad_num = max(parse_number(volatilidad), 0) / 100
        n_sim_num = int(parse_number(n_simulaciones or 2000))
        objetivo_num = parse_number(objetivo) if objetivo not in [None, ""] else None

        if anios_num <= 0:
            raise ValueError("Horizonte temporal inválido")

        mc_result = montecarlo_interes_compuesto(
            capital_inicial=capital_inicial_num,
            aportacion_mensual=aportacion_mensual,
            anios=anios_num,
            rentabilidad_media_anual=rentabilidad_num,
            volatilidad_anual=volatilidad_num,
            inflacion_anual=inflacion_num,
            comision_anual=comision_num,
            n_simulaciones=n_sim_num,
        )

        final_values = mc_result["final_values"]
        real_final_values = mc_result["real_final_values"]

        p10 = np.percentile(final_values, 10)
        p50 = np.percentile(final_values, 50)
        p90 = np.percentile(final_values, 90)
        real_p50 = np.percentile(real_final_values, 50)

        prob_objetivo = None
        if objetivo_num and objetivo_num > 0:
            prob_objetivo = float(np.mean(final_values >= objetivo_num))

        year_100k = first_year_reaching_target(mc_result["p50"], 100000)
        year_obj = first_year_reaching_target(mc_result["p50"], objetivo_num) if objetivo_num else None

        summary = dbc.Row(
            [
                dbc.Col(
                    summary_stat_card(
                        "Percentil 10",
                        formatear_euros_es(p10),
                        "Escenario prudente",
                    ),
                    md=3,
                    className="mb-3",
                ),
                dbc.Col(
                    summary_stat_card(
                        "Percentil 50",
                        formatear_euros_es(p50),
                        "Escenario central",
                    ),
                    md=3,
                    className="mb-3",
                ),
                dbc.Col(
                    summary_stat_card(
                        "Percentil 90",
                        formatear_euros_es(p90),
                        "Escenario favorable",
                    ),
                    md=3,
                    className="mb-3",
                ),
                dbc.Col(
                    summary_stat_card(
                        "Mediana real",
                        formatear_euros_es(real_p50),
                        "Ajustada por inflación",
                    ),
                    md=3,
                    className="mb-3",
                ),
            ]
        )

        goal_children = []

        if prob_objetivo is not None:
            goal_children.append(
                dbc.Alert(
                    f"Probabilidad estimada de alcanzar {formatear_euros_es(objetivo_num)}: {prob_objetivo * 100:.1f}%",
                    color="success" if prob_objetivo >= 0.6 else "warning",
                    className="rounded-4 border-0 mb-3 fw-semibold",
                )
            )

        insights = []
        if year_100k is not None:
            insights.append(f"En la trayectoria mediana superarías 100.000€ alrededor del año {year_100k}.")
        if year_obj is not None:
            insights.append(f"En la trayectoria mediana alcanzarías tu objetivo alrededor del año {year_obj}.")
        elif objetivo_num:
            insights.append("En la trayectoria mediana no llegarías al objetivo dentro del horizonte elegido.")

        if insights:
            goal_children.append(
                dbc.Card(
                    dbc.CardBody(
                        html.Ul(
                            [html.Li(x) for x in insights],
                            className="mb-0",
                            style={"lineHeight": "1.8", "color": "#475467"},
                        )
                    ),
                    className="border-0 rounded-4",
                    style={
                        "background": "#ffffff",
                        "boxShadow": "0 10px 24px rgba(16, 24, 40, 0.05)",
                    },
                )
            )

        return (
            summary,
            build_montecarlo_fan_chart(mc_result),
            build_montecarlo_histogram(mc_result),
            html.Div(goal_children),
        )

    except Exception as e:
        return (
            dbc.Alert(
                f"No se pudo calcular Monte Carlo: {e}",
                color="danger",
                className="rounded-4 border-0",
            ),
            build_empty_figure("Error en la simulación Monte Carlo", height=420),
            build_empty_figure("Error en la distribución final", height=360),
            html.Div(),
        )


# =========================================================
# GUARDAR SIMULACIONES
# =========================================================
@callback(
    Output("saved-simulations-store", "data"),
    Output("save-simulation-message", "children"),
    Output("save-simulation-name", "value"),
    Input("save-simulation-btn", "n_clicks"),
    State("saved-simulations-store", "data"),
    State("save-simulation-name", "value"),
    State("ic-capital-inicial", "value"),
    State("ic-aportacion", "value"),
    State("ic-aportacion-tipo", "value"),
    State("ic-anios", "value"),
    State("ic-rentabilidad", "value"),
    State("ic-inflacion", "value"),
    State("ic-comision", "value"),
    State("ic-scenario", "value"),
    State("premium-access", "data"),
    prevent_initial_call=True,
)
def save_interes_compuesto_simulation(
    n_clicks,
    store,
    nombre,
    capital_inicial,
    aportacion,
    aportacion_tipo,
    anios,
    rentabilidad,
    inflacion,
    comision,
    scenario,
    access_data,
):
    if not n_clicks:
        return no_update, no_update, no_update

    if not is_premium_unlocked(access_data):
        return (
            no_update,
            dbc.Alert(
                "Guardar simulaciones es una función premium. Desbloquéala con el pago único.",
                color="warning",
                className="rounded-4 border-0",
            ),
            no_update,
        )

    data = {
        "capital_inicial": capital_inicial,
        "aportacion": aportacion,
        "aportacion_tipo": aportacion_tipo,
        "anios": anios,
        "rentabilidad": rentabilidad,
        "inflacion": inflacion,
        "comision": comision,
        "scenario": scenario,
    }

    updated_store = add_simulation(
        store=store,
        calculator_key="interes_compuesto",
        nombre=nombre,
        data=data,
    )

    return (
        updated_store,
        dbc.Alert(
            "Simulación guardada correctamente.",
            color="success",
            className="rounded-4",
        ),
        "",
    )


def render_saved_interes_compuesto(items):
    if not items:
        return dbc.Card(
            dbc.CardBody(
                html.Div(
                    "Todavía no has guardado simulaciones.",
                    className="text-muted",
                )
            ),
            className="border-0 shadow-sm rounded-4",
        )

    cards = []
    for item in items[:10]:
        data = item.get("data", {})
        item_id = item.get("id")

        capital = data.get("capital_inicial", "0")
        aportacion = data.get("aportacion", "0")
        aportacion_tipo = data.get("aportacion_tipo", "mensual")
        anios = data.get("anios", "0")
        rentabilidad = data.get("rentabilidad", "0")
        inflacion = data.get("inflacion", "0")
        comision = data.get("comision", "0")
        scenario = data.get("scenario", "base")

        subtitulo = (
            f"Capital inicial: {capital} € · "
            f"Aportación: {aportacion} €/{'mes' if aportacion_tipo == 'mensual' else 'año'} · "
            f"Años: {anios} · "
            f"Rentabilidad: {rentabilidad}% · "
            f"Inflación: {inflacion}% · "
            f"Comisión: {comision}% · "
            f"Escenario: {str(scenario).capitalize()}"
        )

        cards.append(
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div(
                                            item.get("nombre", "Simulación"),
                                            className="fw-bold mb-1",
                                        ),
                                        html.Div(
                                            subtitulo,
                                            className="text-muted small",
                                            style={"lineHeight": "1.6"},
                                        ),
                                    ],
                                    md=10,
                                    className="mb-2 mb-md-0",
                                ),
                                dbc.Col(
                                    dbc.Button(
                                        "Eliminar",
                                        id={"type": "delete-sim-btn", "index": item_id},
                                        color="danger",
                                        outline=True,
                                        className="rounded-pill w-100",
                                        size="sm",
                                    ),
                                    md=2,
                                    className="d-flex align-items-center",
                                ),
                            ],
                            className="g-2",
                        )
                    ]
                ),
                className="border-0 shadow-sm rounded-4 mb-3",
            )
        )

    return html.Div(cards)


@callback(
    Output("saved-simulations-store", "data", allow_duplicate=True),
    Input({"type": "delete-sim-btn", "index": ALL}, "n_clicks"),
    State("saved-simulations-store", "data"),
    prevent_initial_call=True,
)
def delete_saved_simulation(_, store):
    triggered = ctx.triggered_id
    if not triggered:
        return no_update

    item_id = triggered.get("index")
    updated_store = delete_simulation(
        store=store,
        calculator_key="interes_compuesto",
        simulation_id=item_id,
    )
    return updated_store


@callback(
    Output("saved-simulations-list", "children"),
    Input("saved-simulations-store", "data"),
)
def update_saved_interes_compuesto_list(store):
    store = normalize_store(store)
    items = store.get("interes_compuesto", [])
    return render_saved_interes_compuesto(items)


# =========================================================
# CSV
# =========================================================
@callback(
    Output("ic-download-csv", "data"),
    Input("ic-download-btn", "n_clicks"),
    State("ic-evolucion-store", "data"),
    State("premium-access", "data"),
    prevent_initial_call=True,
)
def descargar_csv(n_clicks, evolucion_data, access_data):
    if not n_clicks or not evolucion_data:
        return dash.no_update

    if not is_premium_unlocked(access_data):
        return dash.no_update

    df = evolution_to_dataframe(evolucion_data)
    return dcc.send_data_frame(df.to_csv, "simulacion_interes_compuesto.csv", index=False)
