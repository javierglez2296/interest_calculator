import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from helpers import parse_number, calcular_interes_compuesto, formatear_euros_es

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/comparador",
    title="Comparador de fondos",
    name="Comparador",
)

# =========================================================
# DATOS (ESCALABLES)
# =========================================================

fondos = [
    {"nombre": "S&P 500 ETF", "rentabilidad": 0.08, "comision": 0.001, "riesgo": "alto"},
    {"nombre": "MSCI World", "rentabilidad": 0.07, "comision": 0.0015, "riesgo": "medio"},
    {"nombre": "Vanguard Global", "rentabilidad": 0.072, "comision": 0.002, "riesgo": "medio"},
    {"nombre": "Amundi World", "rentabilidad": 0.069, "comision": 0.0018, "riesgo": "medio"},
    {"nombre": "iShares Core", "rentabilidad": 0.071, "comision": 0.0012, "riesgo": "medio"},
    {"nombre": "RoboAdvisor", "rentabilidad": 0.06, "comision": 0.004, "riesgo": "bajo"},
]

# =========================================================
# LAYOUT
# =========================================================

layout = dbc.Container(
    [
        html.H1("📊 Comparador de inversiones", className="fw-bold mt-4"),
        html.P("Descubre qué inversión te hace ganar más dinero.", className="text-muted mb-4"),

        dbc.Row(
            [
                dbc.Col(dbc.Input(id="aportacion", value="300", type="text"), md=3),
                dbc.Col(dbc.Input(id="anios", value="20", type="number"), md=3),
                dbc.Col(
                    dbc.Select(
                        id="riesgo",
                        options=[
                            {"label": "Todos", "value": "all"},
                            {"label": "Bajo", "value": "bajo"},
                            {"label": "Medio", "value": "medio"},
                            {"label": "Alto", "value": "alto"},
                        ],
                        value="all",
                    ),
                    md=3,
                ),
                dbc.Col(dbc.Button("Comparar", id="btn", color="primary", className="w-100"), md=3),
            ],
            className="mb-4",
        ),

        html.Div(id="recomendador"),
        html.Div(id="resumen"),
        dcc.Graph(id="grafico"),
        html.Div(id="tabla"),
    ],
    fluid=True,
)

# =========================================================
# CALLBACK
# =========================================================

@callback(
    Output("recomendador", "children"),
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

    fondos_filtrados = [f for f in fondos if riesgo == "all" or f["riesgo"] == riesgo]

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
        comisiones_pagadas = valor * f["comision"] * anios

        resultados.append({**f, "valor": valor, "comisiones": comisiones_pagadas})

        anos = [x["año"] for x in evolucion]
        total = [x["total"] for x in evolucion]

        fig.add_trace(go.Scatter(x=anos, y=total, mode="lines", name=f["nombre"]))

    resultados.sort(key=lambda x: x["valor"], reverse=True)

    mejor = resultados[0]
    peor = resultados[-1]
    diferencia = mejor["valor"] - peor["valor"]

    # =========================================================
    # RECOMENDADOR
    # =========================================================

    recomendador = dbc.Card(
        dbc.CardBody(
            [
                html.H4("🤖 Recomendación para ti", className="fw-bold"),
                html.P(f"Según tus datos, la mejor opción es: {mejor['nombre']}"),
                html.P(f"Podrías obtener {formatear_euros_es(mejor['valor'])}", className="text-success fw-bold"),
            ]
        ),
        className="shadow border-0 rounded-4 mb-4",
    )

    # =========================================================
    # RESUMEN
    # =========================================================

    resumen = dbc.Card(
        dbc.CardBody(
            [
                html.H4("🔥 Diferencia clave", className="fw-bold"),
                html.P(
                    f"Elegir bien puede darte {formatear_euros_es(diferencia)} más",
                    className="text-success fw-bold"
                ),
            ]
        ),
        className="shadow border-0 rounded-4 mb-4",
    )

    # =========================================================
    # TABLA
    # =========================================================

    filas = []
    for r in resultados:

        filas.append(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H5(r["nombre"], className="fw-bold"),
                        html.P(f"Resultado: {formatear_euros_es(r['valor'])}"),
                        html.P(f"Comisiones estimadas: {formatear_euros_es(r['comisiones'])}", className="text-danger"),
                        html.P(f"Riesgo: {r['riesgo']}"),
                        dbc.Button(
                            "Empieza a invertir",
                            href=MYINVESTOR_AFFILIATE_URL,
                            target="_blank",
                            color="success",
                            className="w-100",
                        ),
                    ]
                ),
                className="shadow border-0 rounded-4 mb-3",
            )
        )

    fig.update_layout(template="plotly_white")

    return recomendador, resumen, fig, filas
