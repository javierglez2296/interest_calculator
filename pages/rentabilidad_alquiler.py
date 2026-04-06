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
        "Calcula la rentabilidad bruta y neta de una vivienda en alquiler. "
        "Simula ingresos, gastos, cashflow y compara la inversión con otras alternativas."
    ),
)

# =========================================================
# CONFIG
# =========================================================
HIPOTECA_URL = "/hipoteca"
COMPARADOR_URL = "/comparador"
BLOG_URL = "/blog"
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
        fmt = f"{{:,.{dec}f}} €"
        return fmt.format(value).replace(",", "X").replace(".", ",").replace("X", ".")
    except (TypeError, ValueError):
        return "0,00 €"


def fmt_pct(value, dec=2):
    try:
        return f"{float(value):.{dec}f} %".replace(".", ",")
    except (TypeError, ValueError):
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


def premium_metric_card(title, value, subtitle=None, accent=False):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, className="text-muted small fw-semibold mb-2"),
                html.Div(
                    value,
                    className=f"fw-bold {'text-primary' if accent else ''}",
                    style={
                        "fontSize": "2rem",
                        "lineHeight": "1.0",
                        "letterSpacing": "-0.03em",
                    },
                ),
                html.Div(subtitle, className="text-muted small mt-2") if subtitle else None,
            ]
        ),
        className="border-0 shadow-sm rounded-4 h-100",
        style={
            "background": "linear-gradient(180deg, #ffffff 0%, #fbfcfe 100%)",
        },
    )


def premium_info_card(title, children, eyebrow=None, class_name="h-100"):
    return dbc.Card(
        dbc.CardBody(
            [
                section_eyebrow(eyebrow) if eyebrow else None,
                html.H3(title, className="h5 fw-bold mb-3"),
                children,
            ]
        ),
        className=f"border-0 shadow-sm rounded-4 {class_name}",
    )


def input_eur(label, input_id, value, step=1000, help_text=None):
    content = [
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
        content.append(html.Div(help_text, className="text-muted small"))
    return html.Div(content, className="mb-3")


def input_pct(label, input_id, value, step=0.5, help_text=None):
    content = [
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
                dbc.InputGroupText("%", className="rounded-end-4"),
            ],
            class_name="mb-2",
        ),
    ]
    if help_text:
        content.append(html.Div(help_text, className="text-muted small"))
    return html.Div(content, className="mb-3")


def score_badge(label, color):
    return dbc.Badge(
        label,
        color=color,
        pill=True,
        class_name="px-3 py-2",
        style={"fontSize": "0.95rem"},
    )


def calc_case(
    inversion_total,
    alquiler_mensual,
    ocupacion_pct,
    ibi,
    comunidad,
    seguro,
    mantenimiento,
    gestion_pct,
    irpf_pct,
):
    ingresos_anuales = alquiler_mensual * 12 * (ocupacion_pct / 100.0)
    gasto_gestion = ingresos_anuales * (gestion_pct / 100.0)
    gastos_antes_irpf = ibi + comunidad + seguro + mantenimiento + gasto_gestion
    beneficio_antes_irpf = ingresos_anuales - gastos_antes_irpf
    irpf = max(beneficio_antes_irpf, 0) * (irpf_pct / 100.0)
    beneficio_neto = beneficio_antes_irpf - irpf
    rent_bruta = (ingresos_anuales / inversion_total * 100.0) if inversion_total > 0 else 0
    rent_neta = (beneficio_neto / inversion_total * 100.0) if inversion_total > 0 else 0
    cashflow_mensual = beneficio_neto / 12.0
    return {
        "ingresos_anuales": ingresos_anuales,
        "gasto_gestion": gasto_gestion,
        "gastos_antes_irpf": gastos_antes_irpf,
        "beneficio_antes_irpf": beneficio_antes_irpf,
        "irpf": irpf,
        "beneficio_neto": beneficio_neto,
        "rent_bruta": rent_bruta,
        "rent_neta": rent_neta,
        "cashflow_mensual": cashflow_mensual,
    }


def build_breakdown_chart(base_data):
    beneficio_neto_positive = max(base_data["beneficio_neto"], 0)

    fig = go.Figure()
    fig.add_bar(
        x=["Ingresos", "Gastos", "IRPF", "Beneficio neto"],
        y=[
            base_data["ingresos_anuales"],
            base_data["gastos_antes_irpf"],
            base_data["irpf"],
            beneficio_neto_positive,
        ],
        text=[
            fmt_eur(base_data["ingresos_anuales"], 0),
            fmt_eur(base_data["gastos_antes_irpf"], 0),
            fmt_eur(base_data["irpf"], 0),
            fmt_eur(beneficio_neto_positive, 0),
        ],
        textposition="outside",
    )
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=10, b=20),
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        yaxis_title="Euros / año",
        xaxis_title="",
    )
    return fig


def build_compare_chart(inversion_total, rent_neta, sp500_return):
    valor_inmueble = inversion_total * (1 + rent_neta / 100.0)
    valor_sp500 = inversion_total * (1 + sp500_return / 100.0)

    fig = go.Figure()
    fig.add_bar(
        x=["Vivienda en alquiler", "S&P 500"],
        y=[valor_inmueble, valor_sp500],
        text=[fmt_eur(valor_inmueble, 0), fmt_eur(valor_sp500, 0)],
        textposition="outside",
    )
    fig.update_layout(
        height=330,
        margin=dict(l=20, r=20, t=10, b=20),
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        yaxis_title="Valor tras 1 año",
        xaxis_title="",
    )
    return fig


def scenario_table(rows):
    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Escenario"),
                        html.Th("Rent. neta"),
                        html.Th("Cashflow mensual"),
                        html.Th("Lectura"),
                    ]
                )
            ),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(row["nombre"], className="fw-semibold"),
                            html.Td(fmt_pct(row["rent_neta"])),
                            html.Td(fmt_eur(row["cashflow_mensual"])),
                            html.Td(row["lectura"]),
                        ]
                    )
                    for row in rows
                ]
            ),
        ],
        bordered=False,
        hover=True,
        responsive=True,
        class_name="align-middle mb-0",
    )


def get_signal(rent_neta):
    if rent_neta >= 7:
        return (
            "Muy atractiva",
            "success",
            "La operación pinta muy bien para una primera estimación.",
        )
    if rent_neta >= 5:
        return (
            "Buena",
            "primary",
            "La rentabilidad parece sólida y merece revisión más profunda.",
        )
    if rent_neta >= 3:
        return (
            "Aceptable",
            "warning",
            "Puede encajar, pero va más ajustada y exige afinar mejor los números.",
        )
    return (
        "Floja",
        "danger",
        "Con estos supuestos, la operación parece débil. Revisaría precio, gastos o renta.",
    )


def build_insights(base_data, inversion_total, sp500_return):
    insights = []

    if base_data["rent_neta"] >= sp500_return:
        insights.append(
            f"Con estos datos, la rentabilidad neta estimada ({fmt_pct(base_data['rent_neta'])}) "
            f"supera la referencia del S&P 500 ({fmt_pct(sp500_return)})."
        )
    else:
        insights.append(
            f"Con estos datos, la rentabilidad neta estimada ({fmt_pct(base_data['rent_neta'])}) "
            f"queda por debajo de la referencia del S&P 500 ({fmt_pct(sp500_return)})."
        )

    if base_data["cashflow_mensual"] >= 250:
        insights.append(
            f"El cashflow mensual estimado es cómodo ({fmt_eur(base_data['cashflow_mensual'])})."
        )
    elif base_data["cashflow_mensual"] >= 0:
        insights.append(
            f"El cashflow mensual estimado es positivo, pero ajustado ({fmt_eur(base_data['cashflow_mensual'])})."
        )
    else:
        insights.append(
            f"El cashflow mensual estimado sale negativo ({fmt_eur(base_data['cashflow_mensual'])})."
        )

    if inversion_total > 0:
        payback_years = inversion_total / max(base_data["beneficio_neto"], 1) if base_data["beneficio_neto"] > 0 else None
        if payback_years is not None:
            insights.append(
                f"A este ritmo, recuperar la inversión inicial vía beneficio neto llevaría aproximadamente "
                f"{round(payback_years, 1)} años."
            )
        else:
            insights.append(
                "Con beneficio neto no positivo, no habría recuperación clara de la inversión vía flujo anual."
            )

    return html.Ul(
        [html.Li(text, className="mb-2") for text in insights],
        className="text-muted mb-0",
    )


def build_pro_card():
    return dbc.Card(
        dbc.CardBody(
            [
                section_eyebrow("VERSIÓN PRO"),
                html.H3("Análisis avanzado para tomar decisiones reales", className="h4 fw-bold mb-3"),
                html.P(
                    "La versión gratuita te sirve para una primera criba. La versión PRO estaría pensada "
                    "para decidir si comprar o no comprar.",
                    className="text-muted mb-3",
                ),
                html.Div(
                    [
                        dbc.Badge("Hipoteca integrada", color="light", text_color="dark", class_name="me-2 mb-2"),
                        dbc.Badge("Rentabilidad sobre capital aportado", color="light", text_color="dark", class_name="me-2 mb-2"),
                        dbc.Badge("Vacancia realista", color="light", text_color="dark", class_name="me-2 mb-2"),
                        dbc.Badge("Revalorización del inmueble", color="light", text_color="dark", class_name="me-2 mb-2"),
                        dbc.Badge("Comparativa a varios años", color="light", text_color="dark", class_name="me-2 mb-2"),
                        dbc.Badge("Informe descargable", color="light", text_color="dark", class_name="me-2 mb-2"),
                    ],
                    className="mb-4",
                ),
                html.Div(
                    [
                        html.Div("Ideal para monetizar como:", className="fw-semibold mb-2"),
                        html.Ul(
                            [
                                html.Li("Pago único por análisis completo"),
                                html.Li("Freemium con desbloqueo PRO"),
                                html.Li("Lead magnet para hipotecas o asesoramiento"),
                            ],
                            className="text-muted mb-4",
                        ),
                    ]
                ),
                dbc.Button(
                    "Próximamente",
                    color="primary",
                    disabled=True,
                    className="rounded-pill px-4",
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 h-100",
        style={
            "background": "linear-gradient(180deg, #ffffff 0%, #f5f9ff 100%)",
        },
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
                            "Calculadora premium de rentabilidad de alquiler",
                            className="fw-bold mb-3",
                            style={
                                "fontSize": "clamp(2.1rem, 5vw, 4rem)",
                                "lineHeight": "1.02",
                                "letterSpacing": "-0.05em",
                                "color": "#101828",
                            },
                        ),
                        html.P(
                            "Analiza de forma clara cuánto puede rendir una vivienda en alquiler. "
                            "Calcula rentabilidad bruta, neta, cashflow, escenarios e incluso una "
                            "comparativa simple contra el S&P 500.",
                            className="lead text-muted mb-4",
                            style={"maxWidth": "760px"},
                        ),
                        html.Div(
                            [
                                dbc.Button(
                                    "Probar calculadora",
                                    href="#calculadora-rentabilidad",
                                    color="primary",
                                    className="rounded-pill px-4 me-2 mb-2",
                                ),
                                dbc.Button(
                                    "Calcular hipoteca",
                                    href=HIPOTECA_URL,
                                    color="light",
                                    className="rounded-pill px-4 border mb-2",
                                ),
                            ]
                        ),
                        html.Div(
                            [
                                dbc.Badge("Gratis", color="light", text_color="dark", class_name="me-2 mt-2"),
                                dbc.Badge("SEO-friendly", color="light", text_color="dark", class_name="me-2 mt-2"),
                                dbc.Badge("Base perfecta para versión PRO", color="light", text_color="dark", class_name="mt-2"),
                            ]
                        ),
                    ],
                    lg=7,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                section_eyebrow("QUÉ CONSIGUES"),
                                html.H2("Criba rápida de operaciones", className="h4 fw-bold mb-3"),
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.Div("✔", className="fw-bold text-primary"),
                                                html.Div("Rentabilidad bruta y neta", className="text-muted"),
                                            ],
                                            className="d-flex gap-2 mb-2",
                                        ),
                                        html.Div(
                                            [
                                                html.Div("✔", className="fw-bold text-primary"),
                                                html.Div("Cashflow mensual estimado", className="text-muted"),
                                            ],
                                            className="d-flex gap-2 mb-2",
                                        ),
                                        html.Div(
                                            [
                                                html.Div("✔", className="fw-bold text-primary"),
                                                html.Div("Escenarios conservador, base y optimista", className="text-muted"),
                                            ],
                                            className="d-flex gap-2 mb-2",
                                        ),
                                        html.Div(
                                            [
                                                html.Div("✔", className="fw-bold text-primary"),
                                                html.Div("Comparativa simple contra indexados", className="text-muted"),
                                            ],
                                            className="d-flex gap-2",
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
                                html.H2("Introduce los datos de la operación", className="h4 fw-bold mb-4"),

                                html.H4("Compra", className="h6 fw-bold mb-3"),
                                input_eur("Precio de compra", "precio_compra", 180000, step=1000),
                                input_eur(
                                    "Impuestos y gastos de compra",
                                    "gastos_compra",
                                    18000,
                                    step=500,
                                    help_text="ITP/IVA, notaría, registro, gestoría...",
                                ),
                                input_eur(
                                    "Reforma y puesta a punto",
                                    "reforma",
                                    10000,
                                    step=500,
                                    help_text="Reforma, mobiliario, electrodomésticos, pintura...",
                                ),

                                html.Hr(className="my-4"),

                                html.H4("Ingresos", className="h6 fw-bold mb-3"),
                                input_eur("Alquiler mensual esperado", "alquiler_mensual", 950, step=25),
                                input_pct(
                                    "Ocupación estimada",
                                    "ocupacion",
                                    95,
                                    step=1,
                                    help_text="Porcentaje del año que el inmueble estaría alquilado.",
                                ),

                                html.Hr(className="my-4"),

                                html.H4("Gastos anuales", className="h6 fw-bold mb-3"),
                                input_eur("IBI anual", "ibi", 450, step=25),
                                input_eur("Comunidad anual", "comunidad", 720, step=25),
                                input_eur("Seguro anual", "seguro", 220, step=10),
                                input_eur("Mantenimiento anual", "mantenimiento", 600, step=25),
                                input_pct(
                                    "Gestión / administración",
                                    "gestion_pct",
                                    0,
                                    step=0.5,
                                    help_text="Si no usas agencia, puedes dejarlo en 0.",
                                ),
                                input_pct(
                                    "IRPF efectivo estimado",
                                    "irpf_pct",
                                    19,
                                    step=1,
                                    help_text="Estimación simplificada para esta versión.",
                                ),

                                html.Hr(className="my-4"),

                                html.H4("Comparativa", className="h6 fw-bold mb-3"),
                                input_pct(
                                    "Rentabilidad anual esperada del S&P 500",
                                    "sp500_return",
                                    SP500_RETURN_DEFAULT,
                                    step=0.5,
                                    help_text="Solo para comparación orientativa.",
                                ),
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
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    section_eyebrow("SEMÁFORO"),
                                    html.Div(id="signal_badge", className="mb-3"),
                                    html.Div(id="signal_text", className="text-muted"),
                                ]
                            ),
                            className="border-0 shadow-sm rounded-4 mb-4",
                        ),
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    section_eyebrow("BREAKDOWN"),
                                    dcc.Graph(
                                        id="breakdown_chart",
                                        config={"displayModeBar": False},
                                    ),
                                ]
                            ),
                            className="border-0 shadow-sm rounded-4 mb-4",
                        ),
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    section_eyebrow("COMPARATIVA"),
                                    html.P(
                                        "Comparación orientativa del valor tras 1 año entre esta inversión "
                                        "y una alternativa indexada simple.",
                                        className="text-muted small mb-3",
                                    ),
                                    dcc.Graph(
                                        id="compare_chart",
                                        config={"displayModeBar": False},
                                    ),
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
                dbc.Col(
                    premium_info_card(
                        title="Escenarios de rentabilidad",
                        eyebrow="ESCENARIOS",
                        children=html.Div(id="scenario_table_wrap"),
                    ),
                    lg=7,
                ),
                dbc.Col(
                    premium_info_card(
                        title="Ideas clave que te devuelve la simulación",
                        eyebrow="INSIGHTS",
                        children=html.Div(id="insights_wrap"),
                    ),
                    lg=5,
                ),
            ],
            class_name="g-4 pb-4",
        ),

        dbc.Row(
            [
                dbc.Col(build_pro_card(), lg=5),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                section_eyebrow("SIGUIENTE PASO"),
                                html.H3("Combínala con la calculadora de hipoteca", className="h4 fw-bold mb-3"),
                                html.P(
                                    "La financiación puede cambiar mucho la operación. Una vivienda que parece "
                                    "atractiva al contado puede no serlo tanto con hipoteca, y viceversa.",
                                    className="text-muted mb-4",
                                ),
                                html.Div(
                                    [
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
                                section_eyebrow("AVISO"),
                                html.P(
                                    "Esta simulación es orientativa. No sustituye asesoramiento financiero, fiscal o inmobiliario. "
                                    "Antes de invertir conviene revisar impuestos reales, financiación, vacancia, mantenimiento "
                                    "y posibles desviaciones de ingresos y gastos.",
                                    className="text-muted mb-0",
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
    Output("signal_badge", "children"),
    Output("signal_text", "children"),
    Output("breakdown_chart", "figure"),
    Output("compare_chart", "figure"),
    Output("scenario_table_wrap", "children"),
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
    sp500_return = safe_float(sp500_return, SP500_RETURN_DEFAULT)

    inversion_total = precio_compra + gastos_compra + reforma

    base = calc_case(
        inversion_total=inversion_total,
        alquiler_mensual=alquiler_mensual,
        ocupacion_pct=ocupacion,
        ibi=ibi,
        comunidad=comunidad,
        seguro=seguro,
        mantenimiento=mantenimiento,
        gestion_pct=gestion_pct,
        irpf_pct=irpf_pct,
    )

    conservador = calc_case(
        inversion_total=inversion_total,
        alquiler_mensual=alquiler_mensual * 0.95,
        ocupacion_pct=max(ocupacion - 8, 75),
        ibi=ibi,
        comunidad=comunidad,
        seguro=seguro,
        mantenimiento=mantenimiento * 1.15,
        gestion_pct=gestion_pct,
        irpf_pct=irpf_pct,
    )

    optimista = calc_case(
        inversion_total=inversion_total,
        alquiler_mensual=alquiler_mensual * 1.05,
        ocupacion_pct=min(ocupacion + 3, 100),
        ibi=ibi,
        comunidad=comunidad,
        seguro=seguro,
        mantenimiento=mantenimiento * 0.95,
        gestion_pct=gestion_pct,
        irpf_pct=irpf_pct,
    )

    metric_bruta = premium_metric_card(
        "Rentabilidad bruta",
        fmt_pct(base["rent_bruta"]),
        "Ingresos anuales / inversión total",
        accent=True,
    )

    metric_neta = premium_metric_card(
        "Rentabilidad neta",
        fmt_pct(base["rent_neta"]),
        "Beneficio neto anual / inversión total",
    )

    metric_cashflow = premium_metric_card(
        "Cashflow mensual",
        fmt_eur(base["cashflow_mensual"]),
        "Beneficio neto anual / 12",
    )

    metric_desembolso = premium_metric_card(
        "Desembolso inicial",
        fmt_eur(inversion_total),
        "Compra + gastos + reforma",
    )

    signal_label, signal_color, signal_msg = get_signal(base["rent_neta"])

    signal_text = html.Div(
        [
            html.P(
                [
                    html.Strong("Ingresos anuales estimados: "),
                    fmt_eur(base["ingresos_anuales"]),
                ],
                className="mb-2",
            ),
            html.P(
                [
                    html.Strong("Gastos anuales + IRPF: "),
                    fmt_eur(base["gastos_antes_irpf"] + base["irpf"]),
                ],
                className="mb-2",
            ),
            html.P(
                [
                    html.Strong("Beneficio neto anual: "),
                    fmt_eur(base["beneficio_neto"]),
                ],
                className="mb-2",
            ),
            html.P(signal_msg, className="mb-0"),
        ]
    )

    scenario_rows = [
        {
            "nombre": "Conservador",
            "rent_neta": conservador["rent_neta"],
            "cashflow_mensual": conservador["cashflow_mensual"],
            "lectura": "Menor renta, menor ocupación y algo más de fricción.",
        },
        {
            "nombre": "Base",
            "rent_neta": base["rent_neta"],
            "cashflow_mensual": base["cashflow_mensual"],
            "lectura": "El escenario central con tus supuestos actuales.",
        },
        {
            "nombre": "Optimista",
            "rent_neta": optimista["rent_neta"],
            "cashflow_mensual": optimista["cashflow_mensual"],
            "lectura": "Mejor renta, mejor ocupación y algo menos de fricción.",
        },
    ]

    return (
        metric_bruta,
        metric_neta,
        metric_cashflow,
        metric_desembolso,
        score_badge(signal_label, signal_color),
        signal_text,
        build_breakdown_chart(base),
        build_compare_chart(inversion_total, base["rent_neta"], sp500_return),
        scenario_table(scenario_rows),
        build_insights(base, inversion_total, sp500_return),
    )
