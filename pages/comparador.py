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
    title="Comparador de inversiones: fondos, bolsa y carteras | interescompuesto.app",
    name="Comparador",
    description="Compara fondos indexados, carteras, bolsa y alternativas de inversión según rentabilidad, riesgo, comisiones, inflación y horizonte temporal.",
)

# =========================================================
# PRODUCTOS
# =========================================================
FONDOS = [
    {
        "nombre": "Indexado S&P 500",
        "rentabilidad_base": 0.080,
        "volatilidad": 0.18,
        "comision": 0.0010,
        "riesgo": "alto",
        "categoria": "Indexado USA",
        "ideal_para": "quien prioriza crecimiento a largo plazo y tolera caídas temporales fuertes",
    },
    {
        "nombre": "Indexado MSCI World",
        "rentabilidad_base": 0.070,
        "volatilidad": 0.15,
        "comision": 0.0015,
        "riesgo": "medio",
        "categoria": "Global",
        "ideal_para": "quien busca una solución global sencilla, diversificada y de bajo coste",
    },
    {
        "nombre": "Fondo Global Value",
        "rentabilidad_base": 0.066,
        "volatilidad": 0.16,
        "comision": 0.0120,
        "riesgo": "medio",
        "categoria": "Gestión activa",
        "ideal_para": "quien acepta más coste a cambio de criterio gestor y posible descorrelación",
    },
    {
        "nombre": "Indexado Europa",
        "rentabilidad_base": 0.061,
        "volatilidad": 0.14,
        "comision": 0.0018,
        "riesgo": "medio",
        "categoria": "Regional",
        "ideal_para": "quien quiere exposición específica a Europa sin pagar altas comisiones",
    },
    {
        "nombre": "Indexado Emergentes",
        "rentabilidad_base": 0.074,
        "volatilidad": 0.22,
        "comision": 0.0025,
        "riesgo": "alto",
        "categoria": "Emergentes",
        "ideal_para": "quien acepta mucha volatilidad buscando crecimiento potencial a muy largo plazo",
    },
    {
        "nombre": "Cartera RoboAdvisor",
        "rentabilidad_base": 0.058,
        "volatilidad": 0.10,
        "comision": 0.0045,
        "riesgo": "bajo",
        "categoria": "Gestionado",
        "ideal_para": "quien prefiere comodidad, gestión delegada y una cartera más equilibrada",
    },
    {
        "nombre": "Fondo Mixto Moderado",
        "rentabilidad_base": 0.045,
        "volatilidad": 0.08,
        "comision": 0.0090,
        "riesgo": "bajo",
        "categoria": "Mixto",
        "ideal_para": "quien prioriza estabilidad y menor volatilidad frente a crecimiento agresivo",
    },
]

CATEGORIAS = sorted({f["categoria"] for f in FONDOS})

ESCENARIOS = {
    "conservador": {
        "label": "Conservador",
        "ajuste": -0.020,
        "inflacion": 0.025,
        "descripcion": "Reduce rentabilidades esperadas y mantiene inflación algo más exigente.",
    },
    "base": {
        "label": "Base",
        "ajuste": 0.000,
        "inflacion": 0.020,
        "descripcion": "Escenario equilibrado para una simulación razonable a largo plazo.",
    },
    "optimista": {
        "label": "Optimista",
        "ajuste": 0.015,
        "inflacion": 0.018,
        "descripcion": "Rentabilidades algo más favorables y menor presión inflacionaria.",
    },
}

PERFILES = {
    "conservador": {
        "label": "Conservador",
        "riesgos_preferidos": ["bajo"],
        "mensaje": "prioriza estabilidad, menor volatilidad y dormir tranquilo.",
    },
    "moderado": {
        "label": "Moderado",
        "riesgos_preferidos": ["bajo", "medio"],
        "mensaje": "busca equilibrio entre crecimiento y control del riesgo.",
    },
    "agresivo": {
        "label": "Agresivo",
        "riesgos_preferidos": ["medio", "alto"],
        "mensaje": "acepta volatilidad para maximizar crecimiento a largo plazo.",
    },
}


# =========================================================
# HELPERS UI
# =========================================================
def section_kicker(text):
    return html.Div(
        text,
        className="text-uppercase fw-bold small mb-2",
        style={"letterSpacing": "0.08em", "color": "#667085"},
    )


def metric_card(title, value, subtitle=None, highlight=False):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, style={"fontSize": "0.85rem", "fontWeight": "800", "color": "#667085"}),
                html.Div(
                    value,
                    className="fw-bold my-2",
                    style={
                        "fontSize": "clamp(1.35rem, 2.3vw, 1.95rem)",
                        "lineHeight": "1.1",
                        "color": "#198754" if highlight else "#101828",
                    },
                ),
                html.Div(subtitle, style={"fontSize": "0.9rem", "color": "#667085"}) if subtitle else None,
            ]
        ),
        className="border-0 rounded-4 h-100",
        style={"boxShadow": "0 12px 30px rgba(16,24,40,.06)", "background": "#fff"},
    )


def input_block(label, component, hint=None):
    return html.Div(
        [
            dbc.Label(label, className="fw-semibold mb-2", style={"color": "#1f2937"}),
            component,
            html.Div(hint, className="mt-2", style={"fontSize": "0.88rem", "color": "#667085"}) if hint else None,
        ],
        className="mb-3",
    )


def risk_badge(riesgo):
    color_map = {"bajo": "success", "medio": "warning", "alto": "danger"}
    return dbc.Badge(riesgo.capitalize(), color=color_map.get(riesgo, "secondary"), pill=True, class_name="px-3 py-2 fw-semibold")


def category_badge(text):
    return dbc.Badge(text, color="light", class_name="me-2 px-3 py-2 rounded-pill text-dark border")


def make_input(input_id, value, input_type="text"):
    return dbc.Input(
        id=input_id,
        value=value,
        type=input_type,
        className="py-3 rounded-4",
        style={"background": "#f8fafc", "border": "1px solid rgba(15,23,42,.08)", "fontWeight": "600"},
    )


def recomendacion_inteligente(mejor, perfil, diferencia, horizonte, ventaja_real):
    perfil_txt = PERFILES.get(perfil, PERFILES["moderado"])["mensaje"]

    if mejor["riesgo"] in PERFILES.get(perfil, PERFILES["moderado"])["riesgos_preferidos"]:
        encaje = "encaja bien con el perfil seleccionado"
    else:
        encaje = "ofrece buen resultado, aunque su nivel de riesgo puede no encajar del todo con el perfil elegido"

    if horizonte >= 20:
        plazo = "El horizonte es suficientemente largo para que el interés compuesto tenga mucho peso."
    elif horizonte >= 10:
        plazo = "El plazo es razonable, aunque conviene no depender de resultados perfectos."
    else:
        plazo = "El plazo es corto: aquí el riesgo y las comisiones pesan más."

    return (
        f"Para un perfil que {perfil_txt}, {mejor['nombre']} {encaje}. "
        f"{plazo} En esta simulación, la diferencia frente a la peor alternativa es de "
        f"{formatear_euros_es(diferencia)} y la ventaja real estimada frente a no invertir es de "
        f"{formatear_euros_es(ventaja_real)}."
    )


def recommendation_card(mejor, aportado_total, perfil, diferencia, horizonte, ventaja_real):
    ganancia = max(mejor["valor"] - aportado_total, 0)
    texto = recomendacion_inteligente(mejor, perfil, diferencia, horizonte, ventaja_real)

    return dbc.Card(
        dbc.CardBody(
            [
                section_kicker("Recomendación automática"),
                html.H2(mejor["nombre"], className="h3 fw-bold mb-2", style={"color": "#0f172a"}),
                html.P(texto, className="mb-3", style={"color": "#475467", "lineHeight": "1.7"}),
                html.Div([category_badge(mejor["categoria"]), risk_badge(mejor["riesgo"])], className="mb-3"),
                html.Div(formatear_euros_es(mejor["valor"]), className="fw-bold mb-1", style={"fontSize": "2.2rem", "color": "#198754"}),
                html.Div(f"Ganancia estimada: {formatear_euros_es(ganancia)}", className="text-muted mb-4"),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button(
                                "Simular inversión con más detalle",
                                href="/calculadora",
                                color="primary",
                                className="w-100 rounded-pill fw-bold py-3",
                            ),
                            md=6,
                            className="mb-2",
                        ),
                        dbc.Col(
                            dbc.Button(
                                "Abrir cuenta para empezar",
                                href=MYINVESTOR_AFFILIATE_URL,
                                target="_blank",
                                color="success",
                                className="w-100 rounded-pill fw-bold py-3",
                            ),
                            md=6,
                            className="mb-2",
                        ),
                    ]
                ),
            ]
        ),
        className="border-0 rounded-4 mb-4",
        style={"boxShadow": "0 18px 45px rgba(16,24,40,.08)", "background": "linear-gradient(135deg,#fff 0%,#f8fbff 100%)"},
    )


def decision_banner(diferencia, no_invertir, mejor, peor, valor_real_mejor):
    ventaja_vs_no_invertir = mejor["valor"] - no_invertir

    return dbc.Card(
        dbc.CardBody(
            [
                section_kicker("Decisión financiera"),
                html.H3(
                    f"Elegir {mejor['nombre']} en vez de {peor['nombre']} supone {formatear_euros_es(diferencia)} de diferencia.",
                    className="fw-bold mb-3",
                    style={"color": "#0f172a"},
                ),
                html.P(
                    f"Frente a dejar el dinero parado, el mejor escenario proyecta {formatear_euros_es(ventaja_vs_no_invertir)} adicionales. "
                    f"Ajustando por inflación, el valor final equivalente sería de {formatear_euros_es(valor_real_mejor)}.",
                    className="mb-0",
                    style={"color": "#475467", "lineHeight": "1.7"},
                ),
            ]
        ),
        className="border-0 rounded-4 mb-4",
        style={"boxShadow": "0 14px 36px rgba(16,24,40,.06)", "background": "#ffffff"},
    )


def result_card(item, rank, aportado_total):
    ganancia = max(item["valor"] - aportado_total, 0)
    rent_neta = item["rentabilidad"] - item["comision"]

    return dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(f"#{rank}", className="fw-bold", style={"fontSize": "1.8rem", "color": "#198754" if rank == 1 else "#344054"}),
                                html.Div("Ranking", style={"fontSize": ".85rem", "color": "#667085", "fontWeight": "700"}),
                            ],
                            xs=3,
                            md=2,
                        ),
                        dbc.Col(
                            [
                                html.H4(item["nombre"], className="fw-bold mb-2", style={"color": "#0f172a"}),
                                html.Div([category_badge(item["categoria"]), risk_badge(item["riesgo"])], className="mb-3"),
                                dbc.Row(
                                    [
                                        dbc.Col([html.Div("Valor final", className="text-muted small fw-bold"), html.Div(formatear_euros_es(item["valor"]), className="fw-bold")], md=3, className="mb-2"),
                                        dbc.Col([html.Div("Valor real", className="text-muted small fw-bold"), html.Div(formatear_euros_es(item["valor_real"]), className="fw-bold")], md=3, className="mb-2"),
                                        dbc.Col([html.Div("Ganancia", className="text-muted small fw-bold"), html.Div(formatear_euros_es(ganancia), className="fw-bold text-success")], md=2, className="mb-2"),
                                        dbc.Col([html.Div("Rent. neta", className="text-muted small fw-bold"), html.Div(f"{rent_neta * 100:.2f}%", className="fw-bold")], md=2, className="mb-2"),
                                        dbc.Col([html.Div("Comisión", className="text-muted small fw-bold"), html.Div(f"{item['comision'] * 100:.2f}%", className="fw-bold text-danger")], md=2, className="mb-2"),
                                    ],
                                    className="g-3",
                                ),
                                html.Hr(className="my-3"),
                                html.P(
                                    item["ideal_para"],
                                    className="mb-0",
                                    style={"color": "#667085", "lineHeight": "1.6"},
                                ),
                            ],
                            xs=9,
                            md=10,
                        ),
                    ],
                    className="align-items-start",
                )
            ]
        ),
        className="border-0 rounded-4 mb-3",
        style={"boxShadow": "0 12px 30px rgba(16,24,40,.06)", "background": "#fff"},
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
                "Rentabilidad bruta": f"{item['rentabilidad'] * 100:.2f}%",
                "Comisión": f"{item['comision'] * 100:.2f}%",
                "Rentabilidad neta": f"{(item['rentabilidad'] - item['comision']) * 100:.2f}%",
                "Valor final": formatear_euros_es(item["valor"]),
                "Valor real": formatear_euros_es(item["valor_real"]),
            }
        )

    return dbc.Card(
        dbc.CardBody(
            [
                section_kicker("Ranking resumido"),
                dash_table.DataTable(
                    data=data,
                    columns=[{"name": k, "id": k} for k in data[0].keys()],
                    sort_action="native",
                    style_table={"overflowX": "auto"},
                    style_header={"fontWeight": "800", "border": "none", "backgroundColor": "#f8fbff"},
                    style_cell={"textAlign": "left", "padding": "12px", "border": "none", "fontFamily": "inherit", "fontSize": "14px"},
                    style_data_conditional=[{"if": {"row_index": 0}, "fontWeight": "800", "backgroundColor": "#f7fcf9"}],
                ),
            ]
        ),
        className="border-0 rounded-4 mb-4",
        style={"boxShadow": "0 12px 30px rgba(16,24,40,.06)", "background": "#fff"},
    )


def seo_links_block():
    return dbc.Card(
        dbc.CardBody(
            [
                section_kicker("Guías relacionadas"),
                html.H3("Sigue comparando antes de decidir", className="fw-bold mb-3", style={"color": "#0f172a"}),
                dbc.Row(
                    [
                        dbc.Col(html.A("Invertir en S&P 500 durante 30 años", href="/invertir-en-s-p-500-durante-30-anos", className="text-decoration-none fw-semibold"), md=6, className="mb-3"),
                        dbc.Col(html.A("Invertir en fondos indexados durante 30 años", href="/invertir-en-fondos-indexados-durante-30-anos", className="text-decoration-none fw-semibold"), md=6, className="mb-3"),
                        dbc.Col(html.A("Vivienda vs bolsa", href="/vivienda-vs-bolsa", className="text-decoration-none fw-semibold"), md=6, className="mb-3"),
                        dbc.Col(html.A("Calculadora de interés compuesto", href="/calculadora", className="text-decoration-none fw-semibold"), md=6, className="mb-3"),
                        dbc.Col(html.A("Calculadora FIRE", href="/fire", className="text-decoration-none fw-semibold"), md=6, className="mb-3"),
                        dbc.Col(html.A("Rentabilidad de alquiler", href="/rentabilidad-alquiler", className="text-decoration-none fw-semibold"), md=6, className="mb-3"),
                    ]
                ),
            ]
        ),
        className="border-0 rounded-4 mb-4",
        style={"boxShadow": "0 12px 30px rgba(16,24,40,.06)", "background": "#fff"},
    )


# =========================================================
# LAYOUT
# =========================================================
layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            section_kicker("Comparador de inversión"),
                            html.H1(
                                "Compara fondos, carteras y alternativas para decidir dónde invertir",
                                className="fw-bold mb-3",
                                style={"fontSize": "clamp(2rem,4vw,3.4rem)", "lineHeight": "1.05", "color": "#0f172a"},
                            ),
                            html.P(
                                "No mires solo la rentabilidad. Compara comisiones, inflación, riesgo, valor real y coste de oportunidad para tomar una decisión más completa.",
                                className="mb-4",
                                style={"fontSize": "1.08rem", "color": "#475467", "maxWidth": "900px", "lineHeight": "1.7"},
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(dbc.Button("Comparar ahora", href="#comparador-form", color="primary", className="rounded-pill fw-bold px-4 py-3 w-100"), md=4, className="mb-2"),
                                    dbc.Col(dbc.Button("Calcular interés compuesto", href="/calculadora", color="secondary", outline=True, className="rounded-pill fw-bold px-4 py-3 w-100"), md=4, className="mb-2"),
                                ]
                            ),
                        ]
                    ),
                    className="border-0 rounded-4 mt-4 mb-4",
                    style={"background": "linear-gradient(135deg,#ffffff 0%,#f8fbff 55%,#f7fcf9 100%)", "boxShadow": "0 18px 50px rgba(16,24,40,.08)"},
                )
            )
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div(id="comparador-form"),
                                section_kicker("Configura tu comparación"),
                                html.H3("Tus parámetros", className="fw-bold mb-3", style={"color": "#0f172a"}),

                                input_block("Capital inicial (€)", make_input("capital-inicial", "10000"), "Ejemplo: 10.000 €"),
                                input_block("Aportación mensual (€)", make_input("aportacion", "300"), "Ejemplo: 300 € al mes"),
                                input_block("Años", make_input("anios", "20", "number"), "Horizonte temporal"),

                                input_block(
                                    "Escenario",
                                    dbc.Select(
                                        id="escenario",
                                        options=[{"label": v["label"], "value": k} for k, v in ESCENARIOS.items()],
                                        value="base",
                                        className="py-3 rounded-4",
                                    ),
                                    "Cambia rentabilidad esperada e inflación.",
                                ),

                                input_block(
                                    "Perfil inversor",
                                    dbc.Select(
                                        id="perfil",
                                        options=[{"label": v["label"], "value": k} for k, v in PERFILES.items()],
                                        value="moderado",
                                        className="py-3 rounded-4",
                                    ),
                                    "Ayuda a interpretar si la opción encaja contigo.",
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
                                        className="py-3 rounded-4",
                                    ),
                                ),

                                input_block(
                                    "Categoría",
                                    dbc.Select(
                                        id="categoria",
                                        options=[{"label": "Todas", "value": "all"}] + [{"label": cat, "value": cat} for cat in CATEGORIAS],
                                        value="all",
                                        className="py-3 rounded-4",
                                    ),
                                ),

                                dbc.Button("Comparar opciones", id="btn", color="primary", className="w-100 rounded-pill fw-bold mt-2 py-3", size="lg"),
                                html.Div(
                                    "Simulación orientativa. No es asesoramiento financiero ni garantiza resultados futuros.",
                                    className="mt-3",
                                    style={"fontSize": "0.88rem", "color": "#667085", "lineHeight": "1.5"},
                                ),
                            ]
                        ),
                        className="border-0 rounded-4",
                        style={"boxShadow": "0 18px 45px rgba(16,24,40,.08)", "position": "sticky", "top": "90px"},
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
                                    section_kicker("Evolución comparada"),
                                    html.H3("Cómo evoluciona tu dinero en cada opción", className="fw-bold mb-3", style={"color": "#0f172a"}),
                                    dcc.Graph(id="grafico", config={"displayModeBar": False}),
                                ]
                            ),
                            className="border-0 rounded-4 mb-4",
                            style={"boxShadow": "0 12px 30px rgba(16,24,40,.06)", "background": "#fff"},
                        ),

                        html.Div(id="ranking-resumen"),
                        html.Div(id="tabla"),
                        seo_links_block(),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    section_kicker("Siguiente paso"),
                                    html.H3("De comparar a decidir", className="fw-bold mb-3", style={"color": "#0f172a"}),
                                    html.P(
                                        "Una buena decisión no depende solo de elegir el producto con más rentabilidad esperada. También importan el plazo, tu tolerancia al riesgo, las comisiones y la constancia.",
                                        style={"color": "#475467", "lineHeight": "1.7"},
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(dbc.Button("Simular mi caso exacto", href="/calculadora", color="primary", className="w-100 rounded-pill fw-bold py-3"), md=6, className="mb-2"),
                                            dbc.Col(dbc.Button("Empezar a invertir", href=MYINVESTOR_AFFILIATE_URL, target="_blank", color="success", className="w-100 rounded-pill fw-bold py-3"), md=6, className="mb-2"),
                                        ]
                                    ),
                                ]
                            ),
                            className="border-0 rounded-4 mb-4",
                            style={"boxShadow": "0 18px 45px rgba(16,24,40,.08)", "background": "linear-gradient(135deg,#fff 0%,#f7fcf9 100%)"},
                        ),

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
    style={"maxWidth": "1500px"},
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
    Input("escenario", "value"),
    Input("perfil", "value"),
    Input("riesgo", "value"),
    Input("categoria", "value"),
)
def calcular(_, capital_inicial, aportacion, anios, escenario, perfil, riesgo, categoria):
    capital_inicial = max(parse_number(capital_inicial), 0)
    aportacion = max(parse_number(aportacion), 0)

    try:
        anios = int(parse_number(anios))
    except Exception:
        anios = 0

    fig = go.Figure()
    fig.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=20, b=10),
        height=460,
        xaxis_title="Años",
        yaxis_title="€",
        hovermode="x unified",
        legend_title="",
        paper_bgcolor="white",
        plot_bgcolor="white",
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="rgba(15,23,42,.08)", zeroline=False)

    if capital_inicial < 0 or aportacion < 0 or anios <= 0:
        return (
            dbc.Alert("Introduce valores válidos para ver la comparación.", color="warning", className="rounded-4 border-0"),
            metric_card("Mejor opción", "—"),
            metric_card("Peor opción", "—"),
            metric_card("Diferencia", "—"),
            metric_card("Total aportado", "—"),
            "",
            fig,
            "",
            "",
        )

    escenario_data = ESCENARIOS.get(escenario, ESCENARIOS["base"])
    inflacion = escenario_data["inflacion"]
    ajuste = escenario_data["ajuste"]

    fondos_filtrados = [
        f for f in FONDOS
        if (riesgo == "all" or f["riesgo"] == riesgo)
        and (categoria == "all" or f["categoria"] == categoria)
    ]

    if not fondos_filtrados:
        return (
            dbc.Alert("No hay productos para ese filtro. Prueba otra combinación.", color="warning", className="rounded-4 border-0"),
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
        rentabilidad = max(f["rentabilidad_base"] + ajuste, -0.50)

        evolucion = calcular_interes_compuesto(
            capital_inicial=capital_inicial,
            aportacion_mensual=aportacion,
            años=anios,
            rentabilidad_anual=rentabilidad,
            inflacion=inflacion,
            comision=f["comision"],
        )

        valor = evolucion[-1]["total"] if evolucion else capital_inicial
        valor_real = evolucion[-1]["real"] if evolucion else capital_inicial

        resultados.append(
            {
                **f,
                "rentabilidad": rentabilidad,
                "valor": valor,
                "valor_real": valor_real,
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
                hovertemplate="%{fullData.name}<br>Año %{x}<br>%{y:,.0f} €<extra></extra>",
            )
        )

    fig.add_trace(
        go.Scatter(
            x=list(range(1, anios + 1)),
            y=[capital_inicial + (aportacion * 12 * year) for year in range(1, anios + 1)],
            mode="lines",
            name="Sin rentabilidad",
            line=dict(width=2, dash="dash"),
            hovertemplate="Sin rentabilidad<br>Año %{x}<br>%{y:,.0f} €<extra></extra>",
        )
    )

    resultados.sort(key=lambda x: x["valor"], reverse=True)

    mejor = resultados[0]
    peor = resultados[-1]
    diferencia = mejor["valor"] - peor["valor"]
    no_invertir = aportado_total
    ventaja_real = mejor["valor_real"] - no_invertir

    recomendador = recommendation_card(
        mejor=mejor,
        aportado_total=aportado_total,
        perfil=perfil,
        diferencia=diferencia,
        horizonte=anios,
        ventaja_real=ventaja_real,
    )

    resumen = decision_banner(
        diferencia=diferencia,
        no_invertir=no_invertir,
        mejor=mejor,
        peor=peor,
        valor_real_mejor=mejor["valor_real"],
    )

    ranking = build_ranking_table(resultados)
    filas = [result_card(item, idx + 1, aportado_total) for idx, item in enumerate(resultados)]

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
