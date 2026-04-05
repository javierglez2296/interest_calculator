import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from helpers import parse_number, calcular_interes_compuesto, formatear_euros_es
from components.disclaimer_afiliados import build_disclaimer

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/comparador",
    title="Comparador de fondos | interescompuesto.app",
    name="Comparador",
)

# =========================================================
# DATOS
# =========================================================
FONDOS = [
    {"nombre": "S&P 500 ETF", "rentabilidad": 0.08, "comision": 0.001, "riesgo": "alto", "categoria": "Indexado USA"},
    {"nombre": "MSCI World", "rentabilidad": 0.07, "comision": 0.0015, "riesgo": "medio", "categoria": "Global"},
    {"nombre": "Vanguard Global", "rentabilidad": 0.072, "comision": 0.002, "riesgo": "medio", "categoria": "Global"},
    {"nombre": "Amundi World", "rentabilidad": 0.069, "comision": 0.0018, "riesgo": "medio", "categoria": "Global"},
    {"nombre": "iShares Core", "rentabilidad": 0.071, "comision": 0.0012, "riesgo": "medio", "categoria": "Indexado"},
    {"nombre": "RoboAdvisor", "rentabilidad": 0.06, "comision": 0.004, "riesgo": "bajo", "categoria": "Gestionado"},
]


# =========================================================
# HELPERS UI
# =========================================================
def metric_card(title, value, subtitle=None, highlight=False):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, className="cmp-metric-label"),
                html.Div(
                    value,
                    className=f"cmp-metric-value {'cmp-metric-value-highlight' if highlight else ''}",
                ),
                html.Div(subtitle, className="cmp-metric-subtitle") if subtitle else None,
            ]
        ),
        className="border-0 shadow-sm rounded-4 h-100 cmp-metric-card",
    )


def input_block(label, component, hint=None):
    return html.Div(
        [
            dbc.Label(label, className="fw-semibold mb-2"),
            component,
            html.Div(hint, className="cmp-input-hint mt-2") if hint else None,
        ],
        className="mb-3",
    )


def risk_badge(riesgo):
    color_map = {
        "bajo": "success",
        "medio": "warning",
        "alto": "danger",
    }
    return dbc.Badge(
        riesgo.capitalize(),
        color=color_map.get(riesgo, "secondary"),
        pill=True,
        class_name="px-3 py-2 fw-semibold"
    )


def recommendation_card(mejor):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Recomendación principal", className="cmp-section-kicker"),
                html.H2(mejor["nombre"], className="h3 fw-bold mb-2"),
                html.P(
                    f"Según los parámetros introducidos, es la opción con mayor valor final estimado dentro del filtro seleccionado.",
                    className="text-muted mb-3",
                ),
                html.Div(
                    [
                        dbc.Badge(mejor["categoria"], color="light", class_name="me-2 px-3 py-2 rounded-pill text-dark"),
                        risk_badge(mejor["riesgo"]),
                    ],
                    className="mb-3",
                ),
                html.Div(
                    formatear_euros_es(mejor["valor"]),
                    className="cmp-recommendation-value mb-1",
                ),
                html.Div(
                    f"Rentabilidad estimada: {mejor['rentabilidad'] * 100:.1f}% · Comisión: {mejor['comision'] * 100:.2f}%",
                    className="text-muted",
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 mb-4 cmp-recommendation-card",
    )


def difference_banner(diferencia):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Impacto de elegir bien", className="cmp-section-kicker"),
                html.H3(
                    f"La diferencia entre la mejor y la peor opción es de {formatear_euros_es(diferencia)}",
                    className="fw-bold mb-2",
                ),
                html.P(
                    "Pequeñas diferencias en rentabilidad y comisiones pueden generar una brecha muy grande con el paso de los años.",
                    className="text-muted mb-0",
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 mb-4 cmp-banner-card",
    )


def result_card(item, rank):
    rank_labels = {
        1: "Mejor opción",
        2: "Muy competitiva",
        3: "Buena alternativa",
    }

    rank_text = rank_labels.get(rank, "Alternativa")

    return dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(f"#{rank}", className="cmp-rank-number"),
                                html.Div(rank_text, className="cmp-rank-label"),
                            ],
                            xs=3,
                            md=2,
                            lg=2,
                            className="mb-3 mb-md-0"
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        html.H4(item["nombre"], className="fw-bold mb-2"),
                                        dbc.Badge(item["categoria"], color="light", class_name="me-2 px-3 py-2 rounded-pill text-dark"),
                                        risk_badge(item["riesgo"]),
                                    ],
                                    className="mb-3"
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.Div("Valor final estimado", className="cmp-result-label"),
                                                html.Div(formatear_euros_es(item["valor"]), className="cmp-result-value"),
                                            ],
                                            md=4,
                                            className="mb-3 mb-md-0"
                                        ),
                                        dbc.Col(
                                            [
                                                html.Div("Rentabilidad anual", className="cmp-result-label"),
                                                html.Div(f"{item['rentabilidad'] * 100:.1f}%", className="cmp-result-value-small"),
                                            ],
                                            md=3,
                                            className="mb-3 mb-md-0"
                                        ),
                                        dbc.Col(
                                            [
                                                html.Div("Comisión anual", className="cmp-result-label"),
                                                html.Div(f"{item['comision'] * 100:.2f}%", className="cmp-result-value-small text-danger"),
                                            ],
                                            md=3,
                                            className="mb-3 mb-md-0"
                                        ),
                                        dbc.Col(
                                            [
                                                html.Div("Coste estimado", className="cmp-result-label"),
                                                html.Div(formatear_euros_es(item["comisiones"]), className="cmp-result-value-small"),
                                            ],
                                            md=2,
                                        ),
                                    ],
                                    className="g-3"
                                ),
                            ],
                            xs=9,
                            md=10,
                            lg=10
                        )
                    ],
                    className="align-items-center"
                ),
                html.Hr(className="my-4"),
                dbc.Button(
                    "Empieza a invertir",
                    href=MYINVESTOR_AFFILIATE_URL,
                    target="_blank",
                    color="success",
                    className="rounded-pill px-4 fw-semibold"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 mb-3 cmp-result-card",
    )


def empty_state():
    return (
        dbc.Alert(
            "No hay productos para ese nivel de riesgo. Prueba otro filtro.",
            color="warning",
            class_name="rounded-4 border-0"
        ),
        "",
        go.Figure(),
        "",
        "",
        "",
    )


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
                                html.Div("Comparador premium", className="cmp-hero-badge"),
                                html.H1(
                                    "Compara fondos y descubre qué opción puede darte un mejor resultado",
                                    className="fw-bold cmp-hero-title mb-3",
                                ),
                                html.P(
                                    "Simula una aportación mensual, el plazo y tu nivel de riesgo para ver cómo cambian los resultados según rentabilidad y comisiones.",
                                    className="cmp-hero-subtitle mb-0",
                                ),
                            ]
                        ),
                        className="border-0 shadow-sm rounded-4 cmp-hero-card mt-4 mb-4",
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
                                html.Div("Configura tu comparación", className="cmp-section-kicker"),
                                html.H3("Tus parámetros", className="fw-bold mb-3"),

                                input_block(
                                    "Aportación mensual (€)",
                                    dbc.Input(
                                        id="aportacion",
                                        value="300",
                                        type="text",
                                        className="cmp-input",
                                    ),
                                    "Ejemplo: 300 € al mes"
                                ),

                                input_block(
                                    "Años",
                                    dbc.Input(
                                        id="anios",
                                        value="20",
                                        type="number",
                                        className="cmp-input",
                                    ),
                                    "Horizonte temporal de la inversión"
                                ),

                                input_block(
                                    "Nivel de riesgo",
                                    dbc.Select(
                                        id="riesgo",
                                        options=[
                                            {"label": "Todos", "value": "all"},
                                            {"label": "Bajo", "value": "bajo"},
                                            {"label": "Medio", "value": "medio"},
                                            {"label": "Alto", "value": "alto"},
                                        ],
                                        value="all",
                                        className="cmp-input",
                                    ),
                                    "Filtra las opciones según el perfil de riesgo"
                                ),

                                dbc.Button(
                                    "Comparar opciones",
                                    id="btn",
                                    color="primary",
                                    className="w-100 rounded-pill fw-semibold mt-2",
                                    size="lg",
                                ),
                            ]
                        ),
                        className="border-0 shadow-sm rounded-4 cmp-form-card",
                    ),
                    lg=4,
                    className="mb-4",
                ),

                dbc.Col(
                    [
                        html.Div(id="recomendador"),
                        dbc.Row(
                            [
                                dbc.Col(html.Div(id="metric-mejor"), md=4, className="mb-3"),
                                dbc.Col(html.Div(id="metric-peor"), md=4, className="mb-3"),
                                dbc.Col(html.Div(id="metric-diferencia"), md=4, className="mb-3"),
                            ]
                        ),
                        html.Div(id="resumen"),
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Div("Evolución comparada", className="cmp-section-kicker"),
                                    dcc.Graph(id="grafico", config={"displayModeBar": False}),
                                ]
                            ),
                            className="border-0 shadow-sm rounded-4 mb-4",
                        ),
                        html.Div(id="tabla"),
                        build_disclaimer(title="Opciones para pasar de comparar a invertir"),
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
# CALLBACK
# =========================================================
@callback(
    Output("recomendador", "children"),
    Output("metric-mejor", "children"),
    Output("metric-peor", "children"),
    Output("metric-diferencia", "children"),
    Output("resumen", "children"),
    Output("grafico", "figure"),
    Output("tabla", "children"),
    Input("btn", "n_clicks"),
    Input("aportacion", "value"),
    Input("anios", "value"),
    Input("riesgo", "value"),
)
def calcular(_, aportacion, anios, riesgo):
    aportacion = parse_number(aportacion)
    anios = int(anios or 0)

    fondos_filtrados = [f for f in FONDOS if riesgo == "all" or f["riesgo"] == riesgo]

    if not fondos_filtrados or aportacion < 0 or anios <= 0:
        fig = go.Figure()
        fig.update_layout(template="plotly_white", margin=dict(l=10, r=10, t=20, b=10))
        return (
            dbc.Alert("Introduce unos valores válidos para ver la comparación.", color="warning", class_name="rounded-4 border-0"),
            metric_card("Mejor opción", "—"),
            metric_card("Peor opción", "—"),
            metric_card("Diferencia", "—"),
            "",
            fig,
            "",
        )

    resultados = []
    fig = go.Figure()

    for f in fondos_filtrados:
        evolucion = calcular_interes_compuesto(
            capital_inicial=0,
            aportacion_mensual=aportacion,
            años=anios,
            rentabilidad_anual=f["rentabilidad"],
            inflacion=0,
            comision=f["comision"],
        )

        valor = evolucion[-1]["total"] if evolucion else 0
        total_aportado = aportacion * 12 * anios
        comisiones_pagadas = max(valor - total_aportado, 0) * f["comision"] * anios

        resultados.append(
            {
                **f,
                "valor": valor,
                "comisiones": comisiones_pagadas,
            }
        )

        anos = [x["año"] for x in evolucion]
        total = [x["total"] for x in evolucion]

        fig.add_trace(
            go.Scatter(
                x=anos,
                y=total,
                mode="lines",
                name=f["nombre"],
                line=dict(width=3),
            )
        )

    resultados.sort(key=lambda x: x["valor"], reverse=True)

    mejor = resultados[0]
    peor = resultados[-1]
    diferencia = mejor["valor"] - peor["valor"]

    recomendador = recommendation_card(mejor)

    resumen = difference_banner(diferencia)

    filas = [
        result_card(item, idx + 1)
        for idx, item in enumerate(resultados)
    ]

    fig.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Años",
        yaxis_title="€",
        hovermode="x unified",
        legend_title="",
    )

    return (
        recomendador,
        metric_card("Mejor opción", formatear_euros_es(mejor["valor"]), mejor["nombre"], True),
        metric_card("Peor opción", formatear_euros_es(peor["valor"]), peor["nombre"]),
        metric_card("Diferencia", formatear_euros_es(diferencia), "Brecha entre ambas", True),
        resumen,
        fig,
        filas,
    )
