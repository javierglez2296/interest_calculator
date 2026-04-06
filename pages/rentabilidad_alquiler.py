import math

import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from components.disclaimer_afiliados import build_disclaimer

dash.register_page(
    __name__,
    path="/rentabilidad-alquiler",
    title="Calculadora de rentabilidad de alquiler | interescompuesto.app",
    name="Rentabilidad alquiler",
    description=(
        "Calcula la rentabilidad de una vivienda en alquiler, con o sin hipoteca. "
        "Simula rentabilidad bruta, neta, cashflow y compara contra una inversión indexada."
    ),
)

HIPOTECA_URL = "/hipoteca"
COMPARADOR_URL = "/comparador"
SP500_RETURN_DEFAULT = 7.0


# =========================================================
# HELPERS
# =========================================================
def safe_float(value, default=0.0):
    try:
        if value in (None, ""):
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def fmt_eur(value, dec=2):
    try:
        value = float(value)
        fmt = f"{{:,.{dec}f}f}}"
        txt = fmt.format(value)
        txt = txt.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{txt} €"
    except Exception:
        return "0,00 €"


def fmt_pct(value, dec=2):
    try:
        return f"{float(value):.{dec}f} %".replace(".", ",")
    except Exception:
        return "0,00 %"


def section_eyebrow(text):
    return html.Div(
        text,
        className="small fw-bold mb-2",
        style={
            "letterSpacing": "0.08em",
            "textTransform": "uppercase",
            "color": "#0d6efd",
        },
    )


def metric_card(title, value, subtitle=None, accent=False):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, className="text-muted small fw-semibold mb-2"),
                html.Div(
                    value,
                    className=f"fw-bold {'text-primary' if accent else ''}",
                    style={"fontSize": "2rem", "lineHeight": "1.0", "letterSpacing": "-0.03em"},
                ),
                html.Div(subtitle, className="text-muted small mt-2") if subtitle else None,
            ]
        ),
        className="border-0 shadow-sm rounded-4 h-100",
        style={"background": "linear-gradient(180deg, #ffffff 0%, #fbfdff 100%)"},
    )


def input_eur(label, input_id, value, step=1000, help_text=None):
    children = [
        html.Label(label, className="fw-semibold mb-2"),
        dbc.InputGroup(
            [
                dbc.Input(
                    id=input_id,
                    type="number",
                    value=value,
                    step=step,
                    min=0,
                    class_name="rounded-start-4",
                ),
                dbc.InputGroupText("€", className="rounded-end-4"),
            ],
            class_name="mb-2",
        ),
    ]
    if help_text:
        children.append(html.Div(help_text, className="text-muted small"))
    return html.Div(children, className="mb-3")


def input_pct(label, input_id, value, step=0.5, help_text=None, max_value=None):
    children = [
        html.Label(label, className="fw-semibold mb-2"),
        dbc.InputGroup(
            [
                dbc.Input(
                    id=input_id,
                    type="number",
                    value=value,
                    step=step,
                    min=0,
                    max=max_value,
                    class_name="rounded-start-4",
                ),
                dbc.InputGroupText("%", className="rounded-end-4"),
            ],
            class_name="mb-2",
        ),
    ]
    if help_text:
        children.append(html.Div(help_text, className="text-muted small"))
    return html.Div(children, className="mb-3")


def cuota_hipoteca_mensual(capital, interes_anual_pct, años):
    if capital <= 0 or años <= 0:
        return 0.0
    r = interes_anual_pct / 100 / 12
    n = años * 12
    if r == 0:
        return capital / n
    return capital * (r * (1 + r) ** n) / ((1 + r) ** n - 1)


def calc_operacion(
    precio_compra,
    gastos_compra,
    reforma,
    alquiler_mensual,
    ocupacion_pct,
    ibi,
    comunidad,
    seguro,
    mantenimiento,
    gestion_pct,
    irpf_pct,
):
    inversion_total = precio_compra + gastos_compra + reforma
    ingresos_anuales = alquiler_mensual * 12 * (ocupacion_pct / 100.0)
    gasto_gestion = ingresos_anuales * (gestion_pct / 100.0)
    gastos_anuales = ibi + comunidad + seguro + mantenimiento + gasto_gestion
    beneficio_antes_irpf = ingresos_anuales - gastos_anuales
    irpf = max(beneficio_antes_irpf, 0) * (irpf_pct / 100.0)
    beneficio_neto = beneficio_antes_irpf - irpf
    rent_bruta = (ingresos_anuales / inversion_total * 100.0) if inversion_total > 0 else 0.0
    rent_neta = (beneficio_neto / inversion_total * 100.0) if inversion_total > 0 else 0.0
    cashflow_mensual = beneficio_neto / 12.0

    return {
        "inversion_total": inversion_total,
        "ingresos_anuales": ingresos_anuales,
        "gasto_gestion": gasto_gestion,
        "gastos_anuales": gastos_anuales,
        "beneficio_antes_irpf": beneficio_antes_irpf,
        "irpf": irpf,
        "beneficio_neto": beneficio_neto,
        "rent_bruta": rent_bruta,
        "rent_neta": rent_neta,
        "cashflow_mensual": cashflow_mensual,
    }


def semaforo(rent_neta):
    if rent_neta >= 7:
        return "Muy atractiva", "success", "La operación parece muy interesante para una primera estimación."
    if rent_neta >= 5:
        return "Buena", "primary", "La rentabilidad parece sólida y merece análisis más profundo."
    if rent_neta >= 3:
        return "Aceptable", "warning", "Puede tener sentido, pero está más ajustada."
    return "Floja", "danger", "Con estos supuestos, revisaría precio, gastos o renta esperada."


def badge_estado(label, color):
    return dbc.Badge(
        label,
        color=color,
        pill=True,
        class_name="px-3 py-2",
        style={"fontSize": "0.95rem"},
    )


def grafico_breakdown(data, cuota_anual_hipoteca=0):
    categorias = ["Ingresos", "Gastos", "IRPF", "Beneficio neto"]
    beneficio_final = data["beneficio_neto"] - cuota_anual_hipoteca
    valores = [
        data["ingresos_anuales"],
        data["gastos_anuales"] + cuota_anual_hipoteca,
        data["irpf"],
        max(beneficio_final, 0),
    ]
    textos = [fmt_eur(v, 0) for v in valores]

    fig = go.Figure()
    fig.add_bar(x=categorias, y=valores, text=textos, textposition="outside")
    fig.update_layout(
        height=330,
        margin=dict(l=20, r=20, t=10, b=20),
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        yaxis_title="Euros / año",
    )
    return fig


def grafico_comparativa(inversion_total, rent_neta_sin_deuda, rent_sobre_capital, sp500_return, usar_hipoteca):
    valor_sin_deuda = inversion_total * (1 + rent_neta_sin_deuda / 100.0)
    valor_sp500 = inversion_total * (1 + sp500_return / 100.0)

    x = ["Alquiler sin deuda", "S&P 500"]
    y = [valor_sin_deuda, valor_sp500]
    texts = [fmt_eur(valor_sin_deuda, 0), fmt_eur(valor_sp500, 0)]

    if usar_hipoteca:
        valor_con_hipoteca = inversion_total * (1 + rent_sobre_capital / 100.0)
        x.insert(1, "Alquiler con deuda")
        y.insert(1, valor_con_hipoteca)
        texts.insert(1, fmt_eur(valor_con_hipoteca, 0))

    fig = go.Figure()
    fig.add_bar(x=x, y=y, text=texts, textposition="outside")
    fig.update_layout(
        height=330,
        margin=dict(l=20, r=20, t=10, b=20),
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        yaxis_title="Valor orientativo tras 1 año",
    )
    return fig


def pro_card():
    return dbc.Card(
        dbc.CardBody(
            [
                section_eyebrow("VERSIÓN PRO"),
                html.H3("Desbloquea el análisis completo", className="h4 fw-bold mb-3"),
                html.P(
                    "La parte gratuita te sirve para filtrar. La PRO te ayudaría a decidir si comprar o no.",
                    className="text-muted mb-3",
                ),
                html.Div(
                    [
                        dbc.Badge("10 años", color="light", text_color="dark", class_name="me-2 mb-2"),
                        dbc.Badge("Amortización", color="light", text_color="dark", class_name="me-2 mb-2"),
                        dbc.Badge("Revalorización", color="light", text_color="dark", class_name="me-2 mb-2"),
                        dbc.Badge("Escenarios avanzados", color="light", text_color="dark", class_name="me-2 mb-2"),
                        dbc.Badge("PDF", color="light", text_color="dark", class_name="me-2 mb-2"),
                    ],
                    className="mb-4",
                ),
                html.Div(
                    [
                        html.Div("🔒 Resultado premium bloqueado", className="fw-semibold mb-2"),
                        html.Div(
                            "Rentabilidad acumulada, evolución del préstamo, sensibilidad por vacancia y comparativa más realista.",
                            className="text-muted small",
                        ),
                    ],
                    style={
                        "border": "1px dashed #cbd5e1",
                        "borderRadius": "16px",
                        "padding": "1rem",
                        "background": "#f8fafc",
                    },
                    className="mb-4",
                ),
                dbc.Button("Desbloquear análisis completo", color="primary", className="rounded-pill px-4"),
            ]
        ),
        className="border-0 shadow-sm rounded-4 h-100",
        style={"background": "linear-gradient(180deg, #ffffff 0%, #f5f9ff 100%)"},
    )


def locked_preview():
    return dbc.Card(
        dbc.CardBody(
            [
                section_eyebrow("PREVIEW PRO"),
                html.H3("Lo que vería el usuario premium", className="h5 fw-bold mb-3"),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div("Rentabilidad acumulada a 10 años", className="fw-semibold mb-2"),
                                html.Div("12,84 %", className="display-6 fw-bold text-primary"),
                            ],
                            className="mb-3",
                            style={"filter": "blur(5px)", "opacity": 0.65},
                        ),
                        html.Div(
                            [
                                html.Div("Cashflow acumulado", className="fw-semibold mb-2"),
                                html.Div("28.420 €", className="h2 fw-bold"),
                            ],
                            className="mb-3",
                            style={"filter": "blur(5px)", "opacity": 0.65},
                        ),
                        html.Div(
                            "Gráfico a 10 años, payback, escenario conservador/base/optimista y comparativa real con indexados.",
                            className="text-muted",
                            style={"filter": "blur(3px)", "opacity": 0.75},
                        ),
                    ],
                    style={
                        "position": "relative",
                        "borderRadius": "18px",
                        "padding": "1rem",
                        "background": "#f8fafc",
                        "border": "1px solid #e9eef5",
                    },
                ),
                html.Div(
                    dbc.Button(
                        "Quiero la versión PRO",
                        color="dark",
                        className="rounded-pill px-4 mt-4 w-100",
                    )
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 h-100",
    )


def email_capture_box():
    return dbc.Card(
        dbc.CardBody(
            [
                section_eyebrow("CAPTACIÓN"),
                html.H3("Déjame tu email y te aviso cuando esté lista la PRO", className="h5 fw-bold mb-3"),
                html.P(
                    "Perfecto si quieres validar interés antes de montar pagos o acceso privado.",
                    className="text-muted mb-3",
                ),
                dbc.InputGroup(
                    [
                        dbc.Input(
                            type="email",
                            placeholder="Tu email",
                            class_name="rounded-start-pill",
                        ),
                        dbc.Button(
                            "Avisadme",
                            color="primary",
                            className="rounded-end-pill px-4",
                        ),
                    ],
                    class_name="mb-2",
                ),
                html.Div(
                    "Puedes usar este bloque primero como captación y luego cambiarlo por pago o login.",
                    className="text-muted small",
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 h-100",
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
                            "INVERSIÓN INMOBILIARIA",
                            className="d-inline-block fw-bold mb-3",
                            style={
                                "fontSize": "0.82rem",
                                "letterSpacing": "0.08em",
                                "textTransform": "uppercase",
                                "color": "#0d6efd",
                                "background": "#eef4ff",
                                "border": "1px solid #d7e6ff",
                                "padding": "0.45rem 0.85rem",
                                "borderRadius": "999px",
                            },
                        ),
                        html.H1(
                            "Calculadora de rentabilidad de alquiler",
                            className="fw-bold mb-3",
                            style={
                                "fontSize": "clamp(2.1rem, 5vw, 4rem)",
                                "lineHeight": "1.02",
                                "letterSpacing": "-0.05em",
                                "color": "#101828",
                            },
                        ),
                        html.P(
                            "Analiza una vivienda en alquiler con o sin hipoteca. "
                            "Obtén una primera lectura gratis y reserva el análisis profundo para una versión premium.",
                            className="lead text-muted mb-4",
                            style={"maxWidth": "760px"},
                        ),
                        html.Div(
                            [
                                dbc.Button(
                                    "Probar gratis",
                                    href="#calculadora-rentabilidad",
                                    color="primary",
                                    className="rounded-pill px-4 me-2 mb-2",
                                ),
                                dbc.Button(
                                    "Ver hipoteca",
                                    href=HIPOTECA_URL,
                                    color="light",
                                    className="rounded-pill px-4 border mb-2",
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                dbc.Badge("Gratis", color="light", text_color="dark", class_name="me-2 mt-2"),
                                dbc.Badge("Con hipoteca", color="light", text_color="dark", class_name="me-2 mt-2"),
                                dbc.Badge("Lista para freemium", color="light", text_color="dark", class_name="mt-2"),
                            ]
                        ),
                    ],
                    lg=7,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                section_eyebrow("ESTRUCTURA FREEMIUM"),
                                html.H2("Gratis para atraer, PRO para monetizar", className="h4 fw-bold mb-3"),
                                html.Div(
                                    [
                                        html.Div("Gratis", className="fw-bold mb-2"),
                                        html.Ul(
                                            [
                                                html.Li("Rentabilidad bruta"),
                                                html.Li("Rentabilidad neta"),
                                                html.Li("Cashflow"),
                                                html.Li("Comparativa simple"),
                                            ],
                                            className="text-muted mb-3",
                                        ),
                                        html.Div("PRO", className="fw-bold mb-2"),
                                        html.Ul(
                                            [
                                                html.Li("10 años"),
                                                html.Li("Amortización"),
                                                html.Li("Revalorización"),
                                                html.Li("Informe descargable"),
                                            ],
                                            className="text-muted mb-0",
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        className="border-0 shadow-sm rounded-4",
                    ),
                    lg=5,
                ),
            ],
            class_name="py-5 align-items-center",
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div(id="calculadora-rentabilidad"),
                                section_eyebrow("SUPUESTOS"),
                                html.H2("Introduce los datos", className="h4 fw-bold mb-4"),

                                html.H4("Compra", className="h6 fw-bold mb-3"),
                                input_eur("Precio de compra", "precio_compra", 180000, step=1000),
                                input_eur("Impuestos y gastos de compra", "gastos_compra", 18000, step=500),
                                input_eur("Reforma y puesta a punto", "reforma", 10000, step=500),

                                html.Hr(className="my-4"),

                                html.H4("Ingresos", className="h6 fw-bold mb-3"),
                                input_eur("Alquiler mensual esperado", "alquiler_mensual", 950, step=25),
                                input_pct("Ocupación estimada", "ocupacion", 95, step=1, max_value=100),

                                html.Hr(className="my-4"),

                                html.H4("Gastos anuales", className="h6 fw-bold mb-3"),
                                input_eur("IBI anual", "ibi", 450, step=25),
                                input_eur("Comunidad anual", "comunidad", 720, step=25),
                                input_eur("Seguro anual", "seguro", 220, step=10),
                                input_eur("Mantenimiento anual", "mantenimiento", 600, step=25),
                                input_pct("Gestión / administración", "gestion_pct", 0, step=0.5),
                                input_pct("IRPF efectivo estimado", "irpf_pct", 19, step=1),

                                html.Hr(className="my-4"),

                                html.H4("Hipoteca", className="h6 fw-bold mb-3"),
                                dbc.RadioItems(
                                    id="usar_hipoteca",
                                    options=[
                                        {"label": "Sin hipoteca", "value": "no"},
                                        {"label": "Con hipoteca", "value": "si"},
                                    ],
                                    value="no",
                                    inline=True,
                                    class_name="mb-3",
                                ),
                                input_pct("Porcentaje financiado", "ltv_pct", 70, step=1),
                                input_pct("Tipo de interés", "interes_hipoteca", 3.0, step=0.1),
                                input_eur("Plazo (años)", "años_hipoteca", 25, step=1),

                                html.Hr(className="my-4"),

                                html.H4("Comparativa", className="h6 fw-bold mb-3"),
                                input_pct("Rentabilidad anual esperada del S&P 500", "sp500_return", SP500_RETURN_DEFAULT, step=0.5),
                            ]
                        ),
                        className="border-0 shadow-sm rounded-4 h-100",
                    ),
                    lg=5,
                ),

                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Div(id="metric_bruta"), md=6),
                                dbc.Col(html.Div(id="metric_neta"), md=6),
                            ],
                            class_name="g-4 mb-4",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Div(id="metric_cashflow"), md=6),
                                dbc.Col(html.Div(id="metric_desembolso"), md=6),
                            ],
                            class_name="g-4 mb-4",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Div(id="metric_cuota"), md=6),
                                dbc.Col(html.Div(id="metric_capital"), md=6),
                            ],
                            class_name="g-4 mb-4",
                        ),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    section_eyebrow("LECTURA RÁPIDA"),
                                    html.Div(id="signal_badge", className="mb-3"),
                                    html.Div(id="signal_text", className="text-muted"),
                                ]
                            ),
                            className="border-0 shadow-sm rounded-4 mb-4",
                        ),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    section_eyebrow("BREAKDOWN GRATIS"),
                                    dcc.Graph(id="breakdown_chart", config={"displayModeBar": False}),
                                ]
                            ),
                            className="border-0 shadow-sm rounded-4 mb-4",
                        ),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    section_eyebrow("COMPARATIVA GRATIS"),
                                    dcc.Graph(id="compare_chart", config={"displayModeBar": False}),
                                ]
                            ),
                            className="border-0 shadow-sm rounded-4",
                        ),
                    ],
                    lg=7,
                ),
            ],
            class_name="g-4 pb-4",
        ),

        dbc.Row(
            [
                dbc.Col(pro_card(), lg=5),
                dbc.Col(locked_preview(), lg=7),
            ],
            class_name="g-4 pb-4",
        ),

        dbc.Row(
            [
                dbc.Col(email_capture_box(), lg=5),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                section_eyebrow("IDEAS CLAVE"),
                                html.Div(id="insights_wrap", className="text-muted"),
                            ]
                        ),
                        className="border-0 shadow-sm rounded-4 h-100",
                    ),
                    lg=7,
                ),
            ],
            class_name="g-4 pb-4",
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                section_eyebrow("SIGUIENTE PASO"),
                                html.H3("Conecta esta página con tu funnel", className="h4 fw-bold mb-3"),
                                html.P(
                                    "Ahora mismo ya puedes usar esta calculadora como lead magnet, como herramienta freemium "
                                    "o como pre-venta de una versión premium.",
                                    className="text-muted mb-4",
                                ),
                                dbc.Button(
                                    "Ir a hipoteca",
                                    href=HIPOTECA_URL,
                                    color="primary",
                                    className="rounded-pill px-4 me-2 mb-2",
                                ),
                                dbc.Button(
                                    "Ver comparador",
                                    href=COMPARADOR_URL,
                                    color="light",
                                    className="rounded-pill px-4 border mb-2",
                                ),
                            ]
                        ),
                        className="border-0 shadow-sm rounded-4",
                    ),
                    lg=12,
                ),
            ],
            class_name="pb-4",
        ),

        build_disclaimer() if callable(build_disclaimer) else html.Div(),
    ],
    fluid=True,
    class_name="px-3 px-lg-4",
)


# =========================================================
# CALLBACK
# =========================================================
@callback(
    Output("metric_bruta", "children"),
    Output("metric_neta", "children"),
    Output("metric_cashflow", "children"),
    Output("metric_desembolso", "children"),
    Output("metric_cuota", "children"),
    Output("metric_capital", "children"),
    Output("signal_badge", "children"),
    Output("signal_text", "children"),
    Output("breakdown_chart", "figure"),
    Output("compare_chart", "figure"),
    Output("insights_wrap", "children"),
    Input("precio_compra", "value"),
    Input("gastos_compra", "value"),
    Input("reforma", "value"),
    Input("alquiler_mensual", "value"),
    Input("ocupacion", "value"),
    Input("ibi", "value"),
    Input("comunidad", "value"),
    Input("seguro", "value"),
    Input("mantenimiento", "value"),
    Input("gestion_pct", "value"),
    Input("irpf_pct", "value"),
    Input("usar_hipoteca", "value"),
    Input("ltv_pct", "value"),
    Input("interes_hipoteca", "value"),
    Input("años_hipoteca", "value"),
    Input("sp500_return", "value"),
)
def update_calculator(
    precio_compra,
    gastos_compra,
    reforma,
    alquiler_mensual,
    ocupacion,
    ibi,
    comunidad,
    seguro,
    mantenimiento,
    gestion_pct,
    irpf_pct,
    usar_hipoteca,
    ltv_pct,
    interes_hipoteca,
    años_hipoteca,
    sp500_return,
):
    precio_compra = safe_float(precio_compra)
    gastos_compra = safe_float(gastos_compra)
    reforma = safe_float(reforma)
    alquiler_mensual = safe_float(alquiler_mensual)
    ocupacion = safe_float(ocupacion, 95)
    ibi = safe_float(ibi)
    comunidad = safe_float(comunidad)
    seguro = safe_float(seguro)
    mantenimiento = safe_float(mantenimiento)
    gestion_pct = safe_float(gestion_pct)
    irpf_pct = safe_float(irpf_pct)
    ltv_pct = safe_float(ltv_pct)
    interes_hipoteca = safe_float(interes_hipoteca)
    años_hipoteca = max(int(safe_float(años_hipoteca, 25)), 1)
    sp500_return = safe_float(sp500_return, SP500_RETURN_DEFAULT)

    base = calc_operacion(
        precio_compra=precio_compra,
        gastos_compra=gastos_compra,
        reforma=reforma,
        alquiler_mensual=alquiler_mensual,
        ocupacion_pct=ocupacion,
        ibi=ibi,
        comunidad=comunidad,
        seguro=seguro,
        mantenimiento=mantenimiento,
        gestion_pct=gestion_pct,
        irpf_pct=irpf_pct,
    )

    usar_deuda = usar_hipoteca == "si"
    capital_hipoteca = precio_compra * (ltv_pct / 100.0) if usar_deuda else 0.0
    cuota_mensual = cuota_hipoteca_mensual(capital_hipoteca, interes_hipoteca, años_hipoteca) if usar_deuda else 0.0
    cuota_anual = cuota_mensual * 12.0

    capital_aportado = base["inversion_total"] - capital_hipoteca if usar_deuda else base["inversion_total"]
    capital_aportado = max(capital_aportado, 0.0)

    cashflow_despues_hipoteca = base["cashflow_mensual"] - cuota_mensual
    beneficio_neto_despues_hipoteca = base["beneficio_neto"] - cuota_anual

    rent_sobre_capital = (
        (beneficio_neto_despues_hipoteca / capital_aportado) * 100.0
        if capital_aportado > 0
        else 0.0
    )

    rent_mostrar = rent_sobre_capital if usar_deuda else base["rent_neta"]
    etiqueta, color, mensaje = semaforo(rent_mostrar)

    metric_bruta = metric_card(
        "Rentabilidad bruta",
        fmt_pct(base["rent_bruta"]),
        "Ingresos anuales / inversión total",
        accent=True,
    )

    metric_neta = metric_card(
        "Rentabilidad mostrada",
        fmt_pct(base["rent_neta"]) if not usar_deuda else fmt_pct(rent_sobre_capital),
        "Neta total" if not usar_deuda else "Sobre capital aportado",
    )

    metric_cashflow = metric_card(
        "Cashflow mensual",
        fmt_eur(base["cashflow_mensual"]) if not usar_deuda else fmt_eur(cashflow_despues_hipoteca),
        "Sin deuda" if not usar_deuda else "Después de hipoteca",
    )

    metric_desembolso = metric_card(
        "Desembolso inicial",
        fmt_eur(base["inversion_total"]),
        "Compra + gastos + reforma",
    )

    metric_cuota = metric_card(
        "Cuota hipotecaria",
        fmt_eur(cuota_mensual),
        "Mensual" if usar_deuda else "No aplica",
    )

    metric_capital = metric_card(
        "Capital aportado",
        fmt_eur(capital_aportado),
        "Tu dinero inicial",
    )

    signal_text = html.Div(
        [
            html.P([html.Strong("Ingresos anuales: "), fmt_eur(base["ingresos_anuales"])], className="mb-2"),
            html.P([html.Strong("Gastos + IRPF: "), fmt_eur(base["gastos_anuales"] + base["irpf"])], className="mb-2"),
            html.P(
                [
                    html.Strong("Resultado anual mostrado: "),
                    fmt_eur(base["beneficio_neto"]) if not usar_deuda else fmt_eur(beneficio_neto_despues_hipoteca),
                ],
                className="mb-2",
            ),
            html.P(mensaje, className="mb-0"),
        ]
    )

    insights = [
        html.Li(f"Rentabilidad neta sin deuda: {fmt_pct(base['rent_neta'])}.", className="mb-2"),
    ]

    if usar_deuda:
        insights += [
            html.Li(f"Cuota hipotecaria mensual estimada: {fmt_eur(cuota_mensual)}.", className="mb-2"),
            html.Li(f"Cashflow mensual después de hipoteca: {fmt_eur(cashflow_despues_hipoteca)}.", className="mb-2"),
            html.Li(f"Rentabilidad sobre capital aportado: {fmt_pct(rent_sobre_capital)}.", className="mb-2"),
        ]

    if rent_mostrar >= sp500_return:
        insights.append(
            html.Li(f"La rentabilidad mostrada supera la referencia del S&P 500 ({fmt_pct(sp500_return)}).", className="mb-2")
        )
    else:
        insights.append(
            html.Li(f"La rentabilidad mostrada queda por debajo de la referencia del S&P 500 ({fmt_pct(sp500_return)}).", className="mb-2")
        )

    if usar_deuda and cashflow_despues_hipoteca < 0:
        insights.append(
            html.Li("Con hipoteca, el flujo mensual sale negativo con estos supuestos.", className="mb-2")
        )

    return (
        metric_bruta,
        metric_neta,
        metric_cashflow,
        metric_desembolso,
        metric_cuota,
        metric_capital,
        badge_estado(etiqueta, color),
        signal_text,
        grafico_breakdown(base, cuota_anual if usar_deuda else 0.0),
        grafico_comparativa(base["inversion_total"], base["rent_neta"], rent_sobre_capital, sp500_return, usar_deuda),
        html.Ul(insights, className="mb-0"),
    )
