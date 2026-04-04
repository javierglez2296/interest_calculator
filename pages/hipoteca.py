from dash import html, dcc, register_page, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import math

register_page(
    __name__,
    path="/hipoteca",
    name="Calculadora Hipoteca",
    title="Calculadora de hipoteca | interescompuesto.app",
    description="Calcula la cuota mensual de tu hipoteca, intereses totales y coste final del préstamo."
)

# =========================================================
# HELPERS
# =========================================================
def fmt_eur(value):
    try:
        s = f"{value:,.2f}"
        s = s.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{s} €"
    except Exception:
        return "0,00 €"


def calcular_hipoteca(precio_vivienda, entrada_pct, interes_anual, anos, gastos_pct=10):
    entrada_eur = precio_vivienda * (entrada_pct / 100)
    gastos_eur = precio_vivienda * (gastos_pct / 100)
    principal = max(precio_vivienda - entrada_eur, 0)

    n = int(anos * 12)
    r = interes_anual / 100 / 12

    if n <= 0:
        cuota = 0
    elif r == 0:
        cuota = principal / n
    else:
        cuota = principal * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

    total_pagado = cuota * n
    intereses_totales = total_pagado - principal
    desembolso_total = entrada_eur + gastos_eur + total_pagado

    return {
        "entrada_eur": entrada_eur,
        "gastos_eur": gastos_eur,
        "principal": principal,
        "cuota": cuota,
        "total_pagado": total_pagado,
        "intereses_totales": intereses_totales,
        "desembolso_total": desembolso_total,
        "meses": n,
        "interes_mensual": r,
    }


def generar_tabla_amortizacion(principal, interes_mensual, cuota, meses, max_meses=360):
    saldo = principal
    filas = []

    for mes in range(1, min(meses, max_meses) + 1):
        interes_mes = saldo * interes_mensual if interes_mensual > 0 else 0
        amortizacion = cuota - interes_mes if meses > 0 else 0

        if interes_mensual == 0 and meses > 0:
            amortizacion = principal / meses

        saldo = max(saldo - amortizacion, 0)

        filas.append(
            {
                "mes": mes,
                "interes": interes_mes,
                "amortizacion": amortizacion,
                "saldo": saldo,
            }
        )

    return filas


def crear_figura_amortizacion(filas):
    meses = [f["mes"] for f in filas]
    intereses = [f["interes"] for f in filas]
    amortizaciones = [f["amortizacion"] for f in filas]
    saldo = [f["saldo"] for f in filas]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=meses,
            y=intereses,
            name="Intereses",
            hovertemplate="Mes %{x}<br>Intereses: %{y:,.2f} €<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            x=meses,
            y=amortizaciones,
            name="Amortización",
            hovertemplate="Mes %{x}<br>Amortización: %{y:,.2f} €<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=meses,
            y=saldo,
            name="Saldo pendiente",
            mode="lines",
            yaxis="y2",
            hovertemplate="Mes %{x}<br>Saldo: %{y:,.2f} €<extra></extra>",
        )
    )

    fig.update_layout(
        barmode="stack",
        template="plotly_white",
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h", y=1.08, x=0),
        yaxis=dict(title="Cuota desglosada (€)"),
        yaxis2=dict(
            title="Saldo pendiente (€)",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
        xaxis=dict(title="Mes"),
    )

    return fig


# =========================================================
# SEO JSON-LD
# =========================================================
json_ld = {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "Calculadora de Hipoteca",
    "url": "https://interescompuesto.app/hipoteca",
    "applicationCategory": "FinanceApplication",
    "operatingSystem": "All",
    "description": "Calcula cuota mensual, intereses y coste total de una hipoteca.",
    "inLanguage": "es",
}

# =========================================================
# LAYOUT
# =========================================================
layout = dbc.Container(
    [
        dcc.Location(id="hipoteca-location"),
        dcc.Store(id="hipoteca-store"),
        html.Script(type="application/ld+json", children=str(json_ld).replace("'", '"')),

        dbc.Row(
            dbc.Col(
                [
                    html.H1("Calculadora de hipoteca", className="fw-bold mb-3"),
                    html.P(
                        "Simula tu cuota mensual, el coste total del préstamo y cuánto acabarás pagando en intereses.",
                        className="lead text-muted mb-4",
                    ),
                ],
                lg=10
            ),
            className="pt-4 pt-md-5"
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H2("Datos de la hipoteca", className="h4 mb-4"),

                                dbc.Label("Precio de la vivienda (€)", html_for="hipoteca-precio"),
                                dbc.Input(
                                    id="hipoteca-precio",
                                    type="number",
                                    value=250000,
                                    min=0,
                                    step=1000,
                                    className="mb-3",
                                ),

                                dbc.Label("Entrada (%)", html_for="hipoteca-entrada"),
                                dbc.Input(
                                    id="hipoteca-entrada",
                                    type="number",
                                    value=20,
                                    min=0,
                                    max=100,
                                    step=1,
                                    className="mb-3",
                                ),

                                dbc.Label("Tipo de interés anual (%)", html_for="hipoteca-interes"),
                                dbc.Input(
                                    id="hipoteca-interes",
                                    type="number",
                                    value=3.0,
                                    min=0,
                                    step=0.01,
                                    className="mb-3",
                                ),

                                dbc.Label("Plazo (años)", html_for="hipoteca-anos"),
                                dbc.Input(
                                    id="hipoteca-anos",
                                    type="number",
                                    value=30,
                                    min=1,
                                    step=1,
                                    className="mb-3",
                                ),

                                dbc.Label("Gastos iniciales estimados (%)", html_for="hipoteca-gastos"),
                                dbc.Input(
                                    id="hipoteca-gastos",
                                    type="number",
                                    value=10,
                                    min=0,
                                    step=0.1,
                                    className="mb-4",
                                ),

                                dbc.Button(
                                    "Calcular hipoteca",
                                    id="hipoteca-btn",
                                    color="primary",
                                    className="w-100"
                                ),
                            ]
                        ),
                        className="shadow-sm border-0 rounded-4"
                    ),
                    lg=4,
                    className="mb-4",
                ),

                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.Div("Cuota mensual", className="text-muted small"),
                                                html.Div(id="hipoteca-cuota", className="fs-3 fw-bold"),
                                            ]
                                        ),
                                        className="shadow-sm border-0 rounded-4 h-100"
                                    ),
                                    md=6,
                                    className="mb-3",
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.Div("Intereses totales", className="text-muted small"),
                                                html.Div(id="hipoteca-intereses", className="fs-3 fw-bold"),
                                            ]
                                        ),
                                        className="shadow-sm border-0 rounded-4 h-100"
                                    ),
                                    md=6,
                                    className="mb-3",
                                ),
                            ]
                        ),

                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.Div("Capital financiado", className="text-muted small"),
                                                html.Div(id="hipoteca-principal", className="fs-4 fw-bold"),
                                            ]
                                        ),
                                        className="shadow-sm border-0 rounded-4 h-100"
                                    ),
                                    md=4,
                                    className="mb-3",
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.Div("Entrada", className="text-muted small"),
                                                html.Div(id="hipoteca-entrada-eur", className="fs-4 fw-bold"),
                                            ]
                                        ),
                                        className="shadow-sm border-0 rounded-4 h-100"
                                    ),
                                    md=4,
                                    className="mb-3",
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.Div("Gastos iniciales", className="text-muted small"),
                                                html.Div(id="hipoteca-gastos-eur", className="fs-4 fw-bold"),
                                            ]
                                        ),
                                        className="shadow-sm border-0 rounded-4 h-100"
                                    ),
                                    md=4,
                                    className="mb-3",
                                ),
                            ]
                        ),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H2("Evolución del préstamo", className="h4 mb-3"),
                                    dcc.Graph(id="hipoteca-fig", config={"displayModeBar": False}),
                                ]
                            ),
                            className="shadow-sm border-0 rounded-4"
                        ),
                    ],
                    lg=8,
                ),
            ]
        ),

        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2("Resumen total", className="h4 mb-3"),
                            html.Ul(
                                [
                                    html.Li([html.Strong("Total pagado al banco: "), html.Span(id="hipoteca-total-pagado")]),
                                    html.Li([html.Strong("Desembolso total incluyendo entrada y gastos: "), html.Span(id="hipoteca-desembolso-total")]),
                                    html.Li("Esta simulación es orientativa y no sustituye una oferta vinculante del banco."),
                                ],
                                className="mb-0",
                            ),
                        ]
                    ),
                    className="shadow-sm border-0 rounded-4"
                ),
                className="mb-4"
            )
        ),

        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2("FAQ rápida", className="h4 mb-3"),
                            html.H3("¿Qué cuota es razonable?", className="h6"),
                            html.P(
                                "Como regla general, muchas personas intentan que la cuota no supere el 30%-35% de sus ingresos netos mensuales.",
                                className="text-muted",
                            ),
                            html.H3("¿Qué falta en esta simulación?", className="h6"),
                            html.P(
                                "No incluye seguros, productos vinculados, amortizaciones anticipadas, comisiones de apertura ni cambios futuros del tipo si la hipoteca es variable.",
                                className="text-muted",
                            ),
                            html.H3("¿Sirve para hipoteca fija y variable?", className="h6"),
                            html.P(
                                "Sirve muy bien para fija. Para variable, úsala como referencia con un tipo medio estimado.",
                                className="text-muted mb-0",
                            ),
                        ]
                    ),
                    className="shadow-sm border-0 rounded-4 mb-5"
                )
            )
        ),
    ],
    fluid=True,
    className="py-2 px-3 px-md-4 px-lg-5",
)

# =========================================================
# CALLBACK
# =========================================================
@callback(
    Output("hipoteca-cuota", "children"),
    Output("hipoteca-intereses", "children"),
    Output("hipoteca-principal", "children"),
    Output("hipoteca-entrada-eur", "children"),
    Output("hipoteca-gastos-eur", "children"),
    Output("hipoteca-total-pagado", "children"),
    Output("hipoteca-desembolso-total", "children"),
    Output("hipoteca-fig", "figure"),
    Input("hipoteca-btn", "n_clicks"),
    Input("hipoteca-precio", "value"),
    Input("hipoteca-entrada", "value"),
    Input("hipoteca-interes", "value"),
    Input("hipoteca-anos", "value"),
    Input("hipoteca-gastos", "value"),
)
def actualizar_hipoteca(_, precio, entrada_pct, interes_anual, anos, gastos_pct):
    precio = precio or 0
    entrada_pct = entrada_pct or 0
    interes_anual = interes_anual or 0
    anos = anos or 0
    gastos_pct = gastos_pct or 0

    data = calcular_hipoteca(
        precio_vivienda=precio,
        entrada_pct=entrada_pct,
        interes_anual=interes_anual,
        anos=anos,
        gastos_pct=gastos_pct,
    )

    filas = generar_tabla_amortizacion(
        principal=data["principal"],
        interes_mensual=data["interes_mensual"],
        cuota=data["cuota"],
        meses=data["meses"],
    )

    fig = crear_figura_amortizacion(filas)

    return (
        fmt_eur(data["cuota"]),
        fmt_eur(data["intereses_totales"]),
        fmt_eur(data["principal"]),
        fmt_eur(data["entrada_eur"]),
        fmt_eur(data["gastos_eur"]),
        fmt_eur(data["total_pagado"]),
        fmt_eur(data["desembolso_total"]),
        fig,
    )
