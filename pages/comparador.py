import dash
from dash import html, dcc, Input, Output, callback, dash_table
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
# DATOS DEMO
# =========================================================
FONDOS = [
    {
        "nombre": "Indexado S&P 500",
        "rentabilidad": 0.080,
        "comision": 0.0010,
        "riesgo": "alto",
        "categoria": "Indexado USA",
        "ideal_para": "quien prioriza crecimiento a largo plazo y tolera volatilidad elevada",
    },
    {
        "nombre": "Indexado MSCI World",
        "rentabilidad": 0.070,
        "comision": 0.0015,
        "riesgo": "medio",
        "categoria": "Global",
        "ideal_para": "quien busca una solución global sencilla y diversificada",
    },
    {
        "nombre": "Fondo Global Value",
        "rentabilidad": 0.066,
        "comision": 0.0120,
        "riesgo": "medio",
        "categoria": "Gestión activa",
        "ideal_para": "quien quiere gestión activa y acepta más coste a cambio de criterio gestor",
    },
    {
        "nombre": "Indexado Europa",
        "rentabilidad": 0.061,
        "comision": 0.0018,
        "riesgo": "medio",
        "categoria": "Regional",
        "ideal_para": "quien quiere exposición específica a Europa",
    },
    {
        "nombre": "Indexado Emergentes",
        "rentabilidad": 0.074,
        "comision": 0.0025,
        "riesgo": "alto",
        "categoria": "Emergentes",
        "ideal_para": "quien acepta más riesgo buscando más crecimiento potencial",
    },
    {
        "nombre": "Cartera RoboAdvisor",
        "rentabilidad": 0.058,
        "comision": 0.0045,
        "riesgo": "bajo",
        "categoria": "Gestionado",
        "ideal_para": "quien prefiere comodidad y delegar la gestión",
    },
    {
        "nombre": "Fondo Mixto Moderado",
        "rentabilidad": 0.045,
        "comision": 0.0090,
        "riesgo": "bajo",
        "categoria": "Mixto",
        "ideal_para": "quien prioriza estabilidad sobre crecimiento agresivo",
    },
]

CATEGORIAS = sorted({f["categoria"] for f in FONDOS})

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


def category_badge(text):
    return dbc.Badge(
        text,
        color="light",
        class_name="me-2 px-3 py-2 rounded-pill text-dark border"
    )


def recommendation_card(mejor, aportado_total):
    ganancia = max(mejor["valor"] - aportado_total, 0)

    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Recomendación principal", className="cmp-section-kicker"),
                html.H2(mejor["nombre"], className="h3 fw-bold mb-2"),
                html.P(
                    "Es la opción con mayor valor final estimado dentro de los filtros seleccionados.",
                    className="text-muted mb-3",
                ),
                html.Div(
                    [
                        category_badge(mejor["categoria"]),
                        risk_badge(mejor["riesgo"]),
                    ],
                    className="mb-3"
                ),
                html.Div(
                    formatear_euros_es(mejor["valor"]),
                    className="cmp-recommendation-value mb-1",
                ),
                html.Div(
                    f"Ganancia potencial estimada: {formatear_euros_es(ganancia)}",
                    className="text-muted mb-3",
                ),
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div("Mejor para ti si…", className="cmp-mini-label"),
                            html.P(mejor["ideal_para"], className="mb-0 text-muted"),
                        ]
                    ),
                    className="border-0 rounded-4 cmp-inner-soft-card"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 mb-4 cmp-recommendation-card",
    )


def difference_banner(diferencia, no_invertir, mejor):
    ventaja_vs_no_invertir = mejor["valor"] - no_invertir

    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Lectura rápida", className="cmp-section-kicker"),
                html.H3(
                    f"Elegir bien puede suponer {formatear_euros_es(diferencia)} más entre productos.",
                    className="fw-bold mb-2",
                ),
                html.P(
                    f"Frente a no obtener rentabilidad, el mejor escenario proyecta {formatear_euros_es(ventaja_vs_no_invertir)} adicionales sobre el dinero aportado.",
                    className="text-muted mb-0",
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 mb-4 cmp-banner-card",
    )


def result_card(item, rank, aportado_total):
    rank_labels = {
        1: "Mejor opción",
        2: "Muy competitiva",
        3: "Buena alternativa",
    }

    rank_text = rank_labels.get(rank, "Alternativa")
    ganancia = max(item["valor"] - aportado_total, 0)

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
                            className="mb-3 mb-md-0"
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    [
                                        html.H4(item["nombre"], className="fw-bold mb-2"),
                                        category_badge(item["categoria"]),
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
                                                html.Div("Ganancia potencial", className="cmp-result-label"),
                                                html.Div(formatear_euros_es(ganancia), className="cmp-result-value-small text-success"),
                                            ],
                                            md=3,
                                            className="mb-3 mb-md-0"
                                        ),
                                        dbc.Col(
                                            [
                                                html.Div("Rentabilidad anual", className="cmp-result-label"),
                                                html.Div(f"{item['rentabilidad'] * 100:.2f}%", className="cmp-result-value-small"),
                                            ],
                                            md=3,
                                            className="mb-3 mb-md-0"
                                        ),
                                        dbc.Col(
                                            [
                                                html.Div("Comisión anual", className="cmp-result-label"),
                                                html.Div(f"{item['comision'] * 100:.2f}%", className="cmp-result-value-small text-danger"),
                                            ],
                                            md=2,
                                        ),
                                    ],
                                    className="g-3"
                                ),
                                html.Hr(className="my-4"),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Card(
                                                dbc.CardBody(
                                                    [
                                                        html.Div("Mejor para ti si…", className="cmp-mini-label"),
                                                        html.P(item["ideal_para"], className="mb-0 text-muted"),
                                                    ]
                                                ),
                                                className="border-0 rounded-4 cmp-inner-soft-card"
                                            ),
                                            md=8,
                                            className="mb-3 mb-md-0"
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                "Empieza a invertir",
                                                href=MYINVESTOR_AFFILIATE_URL,
                                                target="_blank",
                                                color="success",
                                                className="rounded-pill px-4 fw-semibold w-100",
                                            ),
                                            md=4,
                                            className="d-flex align-items-stretch"
                                        ),
                                    ],
                                    className="g-3"
                                )
                            ],
                            xs=9,
                            md=10
                        )
                    ],
                    className="align-items-center"
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 mb-3 cmp-result-card",
    )


def build_ranking_table(resultados):
    data = []
    for idx, item in enumerate(resultados, start=1):
        data.append(
            {
                "Puesto": idx,
                "Producto": item["nombre"],
                "Categoría": item["categoria"],
                "Riesgo": item["riesgo"].capitalize(),
                "Rentabilidad": f"{item['rentabilidad'] * 100:.2f}%",
                "Comisión": f"{item['comision'] * 100:.2f}%",
                "Valor final": formatear_euros_es(item["valor"]),
            }
        )

    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Ranking resumido", className="cmp-section-kicker"),
                dash_table.DataTable(
                    data=data,
                    columns=[
                        {"name": "Puesto", "id": "Puesto"},
                        {"name": "Producto", "id": "Producto"},
                        {"name": "Categoría", "id": "Categoría"},
                        {"name": "Riesgo", "id": "Riesgo"},
                        {"name": "Rentabilidad", "id": "Rentabilidad"},
                        {"name": "Comisión", "id": "Comisión"},
                        {"name": "Valor final", "id": "Valor final"},
                    ],
                    sort_action="native",
                    style_table={"overflowX": "auto"},
                    style_header={
                        "fontWeight": "700",
                        "border": "none",
                        "backgroundColor": "#f8fbff",
                    },
                    style_cell={
                        "textAlign": "left",
                        "padding": "12px",
                        "border": "none",
                        "fontFamily": "inherit",
                        "fontSize": "14px",
                        "backgroundColor": "white",
                    },
                    style_data_conditional=[
                        {"if": {"row_index": 0}, "fontWeight": "700"},
                    ],
                )
            ]
        ),
        className="border-0 shadow-sm rounded-4 mb-4"
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
                                    "Simula capital inicial, aportación mensual, plazo, riesgo y categoría para ver cómo cambian los resultados según rentabilidad y comisiones.",
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
                                    "Capital inicial (€)",
                                    dbc.Input(
                                        id="capital-inicial",
                                        value="10000",
                                        type="text",
                                        className="cmp-input",
                                    ),
                                    "Ejemplo: 10.000 €"
                                ),

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
                                ),

                                input_block(
                                    "Categoría",
                                    dbc.Select(
                                        id="categoria",
                                        options=[{"label": "Todas", "value": "all"}] + [
                                            {"label": cat, "value": cat} for cat in CATEGORIAS
                                        ],
                                        value="all",
                                        className="cmp-input",
                                    ),
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
                                dbc.Col(html.Div(id="metric-mejor"), md=3, className="mb-3"),
                                dbc.Col(html.Div(id="metric-peor"), md=3, className="mb-3"),
                                dbc.Col(html.Div(id="metric-diferencia"), md=3, className="mb-3"),
                                dbc.Col(html.Div(id="metric-aportado"), md=3, className="mb-3"),
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

                        html.Div(id="ranking-resumen"),
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
    Output("metric-aportado", "children"),
    Output("resumen", "children"),
    Output("grafico", "figure"),
    Output("ranking-resumen", "children"),
    Output("tabla", "children"),
    Input("btn", "n_clicks"),
    Input("capital-inicial", "value"),
    Input("aportacion", "value"),
    Input("anios", "value"),
    Input("riesgo", "value"),
    Input("categoria", "value"),
)
def calcular(_, capital_inicial, aportacion, anios, riesgo, categoria):
    capital_inicial = parse_number(capital_inicial)
    aportacion = parse_number(aportacion)
    anios = int(anios or 0)

    fig = go.Figure()
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Años",
        yaxis_title="€",
        hovermode="x unified",
        legend_title="",
    )

    if capital_inicial < 0 or aportacion < 0 or anios <= 0:
        return (
            dbc.Alert("Introduce valores válidos para ver la comparación.", color="warning", class_name="rounded-4 border-0"),
            metric_card("Mejor opción", "—"),
            metric_card("Peor opción", "—"),
            metric_card("Diferencia", "—"),
            metric_card("Total aportado", "—"),
            "",
            fig,
            "",
            "",
        )

    fondos_filtrados = [
        f for f in FONDOS
        if (riesgo == "all" or f["riesgo"] == riesgo)
        and (categoria == "all" or f["categoria"] == categoria)
    ]

    if not fondos_filtrados:
        return (
            dbc.Alert("No hay productos para ese filtro. Prueba otra combinación.", color="warning", class_name="rounded-4 border-0"),
            metric_card("Mejor opción", "—"),
            metric_card("Peor opción", "—"),
            metric_card("Diferencia", "—"),
            metric_card("Total aportado", "—"),
            "",
            fig,
            "",
            "",
        )

    resultados = []
    aportado_total = capital_inicial + (aportacion * 12 * anios)

    for f in fondos_filtrados:
        evolucion = calcular_interes_compuesto(
            capital_inicial=capital_inicial,
            aportacion_mensual=aportacion,
            años=anios,
            rentabilidad_anual=f["rentabilidad"],
            inflacion=0,
            comision=f["comision"],
        )

        valor = evolucion[-1]["total"] if evolucion else 0
        comisiones_estimadas = max(valor - aportado_total, 0) * f["comision"] * anios

        resultados.append(
            {
                **f,
                "valor": valor,
                "comisiones": comisiones_estimadas,
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

    fig.add_trace(
        go.Scatter(
            x=list(range(1, anios + 1)),
            y=[capital_inicial + (aportacion * 12 * year) for year in range(1, anios + 1)],
            mode="lines",
            name="Sin rentabilidad",
            line=dict(width=2, dash="dash"),
        )
    )

    resultados.sort(key=lambda x: x["valor"], reverse=True)

    mejor = resultados[0]
    peor = resultados[-1]
    diferencia = mejor["valor"] - peor["valor"]
    no_invertir = aportado_total

    recomendador = recommendation_card(mejor, aportado_total)
    resumen = difference_banner(diferencia, no_invertir, mejor)
    ranking = build_ranking_table(resultados)

    filas = [
        result_card(item, idx + 1, aportado_total)
        for idx, item in enumerate(resultados)
    ]

    return (
        recomendador,
        metric_card("Mejor opción", formatear_euros_es(mejor["valor"]), mejor["nombre"], True),
        metric_card("Peor opción", formatear_euros_es(peor["valor"]), peor["nombre"]),
        metric_card("Diferencia", formatear_euros_es(diferencia), "Brecha entre mejor y peor", True),
        metric_card("Total aportado", formatear_euros_es(aportado_total), "Capital inicial + aportaciones"),
        resumen,
        fig,
        ranking,
        filas,
    )
