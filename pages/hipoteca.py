from dash import html, dcc, register_page, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

register_page(
    __name__,
    path="/hipoteca",
    name="Calculadora Hipoteca",
    title="Calculadora de hipoteca | interescompuesto.app",
    description="Calcula la cuota mensual de tu hipoteca, intereses totales, entrada necesaria y coste final del préstamo."
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


def fmt_pct(value):
    try:
        s = f"{value:.2f}".replace(".", ",")
        return f"{s} %"
    except Exception:
        return "0,00 %"


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
    porcentaje_intereses_sobre_prestamo = (intereses_totales / principal * 100) if principal > 0 else 0
    porcentaje_desembolso_sobre_precio = (desembolso_total / precio_vivienda * 100) if precio_vivienda > 0 else 0
    ahorro_necesario = entrada_eur + gastos_eur

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
        "porcentaje_intereses_sobre_prestamo": porcentaje_intereses_sobre_prestamo,
        "porcentaje_desembolso_sobre_precio": porcentaje_desembolso_sobre_precio,
        "ahorro_necesario": ahorro_necesario,
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
                "interes": max(interes_mes, 0),
                "amortizacion": max(amortizacion, 0),
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


def crear_figura_coste(data):
    fig = go.Figure(
        data=[
            go.Bar(
                x=["Compra"],
                y=[data["principal"]],
                name="Capital financiado",
                hovertemplate="Capital: %{y:,.2f} €<extra></extra>",
            ),
            go.Bar(
                x=["Compra"],
                y=[data["intereses_totales"]],
                name="Intereses",
                hovertemplate="Intereses: %{y:,.2f} €<extra></extra>",
            ),
            go.Bar(
                x=["Compra"],
                y=[data["gastos_eur"]],
                name="Gastos iniciales",
                hovertemplate="Gastos: %{y:,.2f} €<extra></extra>",
            ),
            go.Bar(
                x=["Compra"],
                y=[data["entrada_eur"]],
                name="Entrada",
                hovertemplate="Entrada: %{y:,.2f} €<extra></extra>",
            ),
        ]
    )

    fig.update_layout(
        barmode="stack",
        template="plotly_white",
        height=420,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h", y=1.12, x=0),
        yaxis=dict(title="Coste acumulado (€)"),
        xaxis=dict(title=""),
    )
    return fig


def crear_figura_comparativa_plazos(precio, entrada_pct, interes_anual, gastos_pct):
    opciones = [20, 25, 30]
    cuotas = []
    intereses = []

    for anos in opciones:
        data = calcular_hipoteca(precio, entrada_pct, interes_anual, anos, gastos_pct)
        cuotas.append(data["cuota"])
        intereses.append(data["intereses_totales"])

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=[f"{x} años" for x in opciones],
            y=cuotas,
            name="Cuota mensual",
            hovertemplate="%{x}<br>Cuota: %{y:,.2f} €<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[f"{x} años" for x in opciones],
            y=intereses,
            name="Intereses totales",
            mode="lines+markers",
            yaxis="y2",
            hovertemplate="%{x}<br>Intereses: %{y:,.2f} €<extra></extra>",
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=420,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h", y=1.1, x=0),
        xaxis=dict(title="Plazo"),
        yaxis=dict(title="Cuota mensual (€)"),
        yaxis2=dict(
            title="Intereses totales (€)",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
    )
    return fig


def crear_figura_comparativa_entradas(precio, interes_anual, anos, gastos_pct):
    opciones = [10, 20, 30]
    cuotas = []
    intereses = []
    ahorro_necesario = []

    for entrada in opciones:
        data = calcular_hipoteca(precio, entrada, interes_anual, anos, gastos_pct)
        cuotas.append(data["cuota"])
        intereses.append(data["intereses_totales"])
        ahorro_necesario.append(data["ahorro_necesario"])

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=[f"{x}%" for x in opciones],
            y=cuotas,
            name="Cuota mensual",
            hovertemplate="Entrada %{x}<br>Cuota: %{y:,.2f} €<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[f"{x}%" for x in opciones],
            y=intereses,
            name="Intereses totales",
            mode="lines+markers",
            yaxis="y2",
            hovertemplate="Entrada %{x}<br>Intereses: %{y:,.2f} €<extra></extra>",
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=420,
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h", y=1.1, x=0),
        xaxis=dict(title="Entrada"),
        yaxis=dict(title="Cuota mensual (€)"),
        yaxis2=dict(
            title="Intereses totales (€)",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
    )

    tabla = dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Entrada"),
                        html.Th("Ahorro inicial necesario"),
                        html.Th("Cuota mensual"),
                        html.Th("Intereses totales"),
                    ]
                )
            ),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(f"{entrada}%"),
                            html.Td(fmt_eur(ahorro)),
                            html.Td(fmt_eur(cuota)),
                            html.Td(fmt_eur(interes)),
                        ]
                    )
                    for entrada, ahorro, cuota, interes in zip(opciones, ahorro_necesario, cuotas, intereses)
                ]
            ),
        ],
        bordered=False,
        hover=True,
        responsive=True,
        class_name="align-middle mb-0",
    )

    return fig, tabla


def calcular_valor_futuro_aportes(aporte_mensual, rentabilidad_anual, anos):
    meses = max(int(anos * 12), 0)
    r = rentabilidad_anual / 100 / 12

    if meses <= 0 or aporte_mensual <= 0:
        return 0

    if r == 0:
        return aporte_mensual * meses

    return aporte_mensual * (((1 + r) ** meses - 1) / r)


def generar_insights(data, precio_vivienda):
    cuota = data["cuota"]
    principal = data["principal"]
    desembolso_total = data["desembolso_total"]
    pct_intereses = data["porcentaje_intereses_sobre_prestamo"]
    pct_total = data["porcentaje_desembolso_sobre_precio"]

    if principal <= 0:
        insight_1 = "La financiación es 0 €, así que en esta simulación no habría préstamo hipotecario."
    elif pct_intereses < 20:
        insight_1 = "El peso de los intereses es relativamente contenido para el importe financiado."
    elif pct_intereses < 50:
        insight_1 = "El coste financiero ya es relevante: pagarás una parte importante del préstamo solo en intereses."
    else:
        insight_1 = "El coste financiero es alto: terminarías pagando una cantidad muy elevada solo en intereses."

    if cuota <= 700:
        insight_2 = "La cuota mensual está en una zona relativamente cómoda para rentas medias, aunque depende de tus ingresos."
    elif cuota <= 1200:
        insight_2 = "La cuota mensual entra en una franja exigente: conviene compararla con tus ingresos netos y tu colchón de ahorro."
    else:
        insight_2 = "La cuota mensual es alta y puede tensionar bastante tu presupuesto si no tienes ingresos sólidos y estables."

    sobrecoste = desembolso_total - precio_vivienda
    insight_3 = (
        f"Aunque la vivienda cuesta {fmt_eur(precio_vivienda)}, el desembolso total estimado sube a "
        f"{fmt_eur(desembolso_total)}. Eso son {fmt_eur(sobrecoste)} adicionales entre entrada, gastos e intereses."
        if sobrecoste > 0
        else "No aparece sobrecoste frente al precio de compra, algo poco habitual salvo casos sin financiación ni gastos."
    )

    if pct_total < 120:
        insight_4 = "El coste total final no se dispara demasiado respecto al precio de compra."
    elif pct_total < 150:
        insight_4 = "El coste total final ya se aleja bastante del precio de la vivienda."
    else:
        insight_4 = "El coste total final se dispara mucho respecto al precio inicial de la vivienda."

    return [insight_1, insight_2, insight_3, insight_4]


def metric_card(title, value, subtitle=None, highlight=False):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, className="text-muted small text-uppercase fw-semibold mb-2"),
                html.Div(
                    value,
                    className=f"{'text-success' if highlight else ''} fw-bold",
                    style={"fontSize": "1.9rem", "lineHeight": "1.1"},
                ),
                html.Div(subtitle or "", className="text-muted small mt-2"),
            ]
        ),
        className="shadow-sm border-0 rounded-4 h-100"
    )


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
    "description": "Calcula cuota mensual, intereses, entrada necesaria y coste total de una hipoteca.",
    "inLanguage": "es",
}

# =========================================================
# LAYOUT
# =========================================================
layout = dbc.Container(
    [
        html.Script(type="application/ld+json", children=str(json_ld).replace("'", '"')),

        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Div("SIMULADOR HIPOTECA", className="small fw-bold text-primary mb-2"),
                            html.H1(
                                "Calcula cuánto pagarás realmente por tu casa",
                                className="fw-bold mb-3",
                                style={"maxWidth": "900px"},
                            ),
                            html.P(
                                "Descubre tu cuota mensual, los intereses, la entrada necesaria y el coste total real de comprar vivienda en España.",
                                className="lead text-muted mb-4",
                                style={"maxWidth": "850px"},
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.Div("✅ Cuota mensual", className="fw-semibold"),
                                                    html.Div("Intereses y capital", className="small text-muted"),
                                                ]
                                            ),
                                            className="border-0 bg-light rounded-4 h-100"
                                        ),
                                        md=4,
                                        className="mb-3",
                                    ),
                                    dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.Div("✅ Entrada y gastos", className="fw-semibold"),
                                                    html.Div("Coste inicial estimado", className="small text-muted"),
                                                ]
                                            ),
                                            className="border-0 bg-light rounded-4 h-100"
                                        ),
                                        md=4,
                                        className="mb-3",
                                    ),
                                    dbc.Col(
                                        dbc.Card(
                                            dbc.CardBody(
                                                [
                                                    html.Div("✅ Coste total real", className="fw-semibold"),
                                                    html.Div("Análisis visual del préstamo", className="small text-muted"),
                                                ]
                                            ),
                                            className="border-0 bg-light rounded-4 h-100"
                                        ),
                                        md=4,
                                        className="mb-3",
                                    ),
                                ]
                            ),
                        ]
                    ),
                    className="shadow-sm border-0 rounded-4"
                ),
                width=12,
            ),
            className="pt-4 pt-md-5 mb-4"
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H2("Introduce los datos", className="h4 mb-4 fw-bold"),

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
                                    className="w-100 rounded-3 fw-semibold"
                                ),

                                html.Hr(className="my-4"),

                                html.Div("Consejo rápido", className="small fw-bold text-uppercase text-muted mb-2"),
                                html.P(
                                    "Como referencia prudente, muchas personas intentan que la cuota no supere el 30%-35% de sus ingresos netos mensuales.",
                                    className="small text-muted mb-0"
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
                                dbc.Col(html.Div(id="metric-cuota"), md=6, className="mb-3"),
                                dbc.Col(html.Div(id="metric-intereses"), md=6, className="mb-3"),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Div(id="metric-principal"), md=4, className="mb-3"),
                                dbc.Col(html.Div(id="metric-entrada"), md=4, className="mb-3"),
                                dbc.Col(html.Div(id="metric-gastos"), md=4, className="mb-3"),
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.Div("Lo que pagarás de más", className="text-muted small text-uppercase fw-semibold mb-2"),
                                                html.Div(id="hipoteca-sobrecoste", className="fw-bold text-danger", style={"fontSize": "1.8rem"}),
                                                html.Div(
                                                    "Diferencia entre el precio de la vivienda y el desembolso total estimado.",
                                                    className="text-muted small mt-2"
                                                ),
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
                                                html.Div("Coste total sobre precio", className="text-muted small text-uppercase fw-semibold mb-2"),
                                                html.Div(id="hipoteca-pct-total", className="fw-bold", style={"fontSize": "1.8rem"}),
                                                html.Div(
                                                    "Cuánto representa el coste total final frente al precio de compra.",
                                                    className="text-muted small mt-2"
                                                ),
                                            ]
                                        ),
                                        className="shadow-sm border-0 rounded-4 h-100"
                                    ),
                                    md=6,
                                    className="mb-3",
                                ),
                            ]
                        ),
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H2("Evolución del préstamo", className="h4 mb-3 fw-bold"),
                                    html.P(
                                        "Visualiza cómo cambia el peso de los intereses, la amortización y el saldo pendiente a lo largo del tiempo.",
                                        className="text-muted small mb-3",
                                    ),
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
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H2("Resumen total de la operación", className="h4 mb-3 fw-bold"),
                                html.Ul(
                                    [
                                        html.Li([html.Strong("Total pagado al banco: "), html.Span(id="hipoteca-total-pagado")]),
                                        html.Li([html.Strong("Desembolso total incluyendo entrada y gastos: "), html.Span(id="hipoteca-desembolso-total")]),
                                        html.Li([html.Strong("Intereses sobre el capital financiado: "), html.Span(id="hipoteca-pct-intereses")]),
                                        html.Li("Esta simulación es orientativa y no sustituye una oferta vinculante del banco."),
                                    ],
                                    className="mb-0",
                                ),
                            ]
                        ),
                        className="shadow-sm border-0 rounded-4 h-100"
                    ),
                    lg=6,
                    className="mb-4",
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H2("Desglose visual del coste", className="h4 mb-3 fw-bold"),
                                html.P(
                                    "Aquí ves cuánto pesa cada parte del coste total de comprar vivienda.",
                                    className="text-muted small"
                                ),
                                dcc.Graph(id="hipoteca-coste-fig", config={"displayModeBar": False}),
                            ]
                        ),
                        className="shadow-sm border-0 rounded-4 h-100"
                    ),
                    lg=6,
                    className="mb-4",
                ),
            ]
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H2("Compara plazos: 20, 25 y 30 años", className="h4 mb-3 fw-bold"),
                                html.P(
                                    "Acortar la hipoteca suele subir la cuota, pero puede reducir mucho los intereses totales.",
                                    className="text-muted small"
                                ),
                                dcc.Graph(id="hipoteca-plazos-fig", config={"displayModeBar": False}),
                            ]
                        ),
                        className="shadow-sm border-0 rounded-4 h-100"
                    ),
                    lg=6,
                    className="mb-4",
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H2("¿Amortizar o invertir?", className="h4 mb-3 fw-bold"),
                                html.P(
                                    "Simulación orientativa: qué valor futuro podría alcanzar una aportación mensual equivalente si la inviertes en vez de destinarla a otra cosa.",
                                    className="text-muted small"
                                ),
                                html.Div(id="hipoteca-inversion-box"),
                            ]
                        ),
                        className="shadow-sm border-0 rounded-4 h-100"
                    ),
                    lg=6,
                    className="mb-4",
                ),
            ]
        ),

        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2("Compara dar un 10%, 20% o 30% de entrada", className="h4 mb-3 fw-bold"),
                            html.P(
                                "Dar más entrada reduce la cuota y los intereses, pero te exige más ahorro inicial antes de comprar.",
                                className="text-muted small mb-3",
                            ),
                            dcc.Graph(id="hipoteca-entradas-fig", config={"displayModeBar": False}),
                            html.Div(id="hipoteca-entradas-tabla", className="mt-3"),
                        ]
                    ),
                    className="shadow-sm border-0 rounded-4 mb-4"
                )
            )
        ),

        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2("Lectura rápida de tu simulación", className="h4 mb-3 fw-bold"),
                            html.Div(id="hipoteca-insights"),
                        ]
                    ),
                    className="shadow-sm border-0 rounded-4 mb-4"
                )
            )
        ),

        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2("¿Cuánto ahorro necesitas para comprar una vivienda?", className="h4 mb-3 fw-bold"),
                            html.P(
                                "Comprar una casa no es solo pagar la cuota. Antes de firmar, normalmente necesitas ahorro para la entrada y para los gastos iniciales.",
                                className="mb-3",
                            ),
                            html.P(
                                "Por ejemplo, si compras una vivienda de 250.000 €, con una entrada del 20% y unos gastos del 10%, podrías necesitar alrededor de 75.000 € antes de pedir la hipoteca.",
                                className="text-muted mb-3",
                            ),
                            html.P(
                                "Cuanto mayor sea tu entrada, menor será el importe financiado y menores serán los intereses que pagarás durante la vida del préstamo.",
                                className="text-muted mb-0",
                            ),
                        ]
                    ),
                    className="shadow-sm border-0 rounded-4 mb-4"
                )
            )
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H2("Errores frecuentes al pedir hipoteca", className="h4 mb-3 fw-bold"),
                                html.Ul(
                                    [
                                        html.Li("Mirar solo la cuota mensual y no el coste total del préstamo."),
                                        html.Li("Agotar todos tus ahorros en la compra y quedarte sin colchón de emergencia."),
                                        html.Li("No comparar varias ofertas hipotecarias antes de firmar."),
                                        html.Li("Ignorar seguros, productos vinculados y otros gastos adicionales."),
                                        html.Li("Asumir una cuota demasiado alta respecto a tus ingresos netos."),
                                    ],
                                    className="mb-0",
                                ),
                            ]
                        ),
                        className="shadow-sm border-0 rounded-4 h-100"
                    ),
                    lg=6,
                    className="mb-4",
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H2("Hipoteca fija vs variable", className="h4 mb-3 fw-bold"),
                                html.P(
                                    "La hipoteca fija ofrece estabilidad: pagarás la misma cuota durante toda la vida del préstamo, salvo cambios por seguros u otros costes externos.",
                                    className="text-muted mb-3",
                                ),
                                html.P(
                                    "La hipoteca variable suele empezar con un tipo inicial o con un diferencial sobre un índice como el euríbor. Puede ser más barata en algunos momentos, pero también implica más incertidumbre.",
                                    className="text-muted mb-3",
                                ),
                                html.P(
                                    "Si valoras previsibilidad y tranquilidad, la fija suele encajar mejor. Si aceptas más riesgo a cambio de posible ahorro futuro, la variable puede interesarte más.",
                                    className="text-muted mb-0",
                                ),
                            ]
                        ),
                        className="shadow-sm border-0 rounded-4 h-100"
                    ),
                    lg=6,
                    className="mb-4",
                ),
            ]
        ),

        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2("Siguiente paso", className="h4 mb-3 fw-bold"),
                            html.P(
                                "Antes de firmar una hipoteca, compara bien tu cuota, el coste total y el impacto sobre tu ahorro e inversión a largo plazo.",
                                className="mb-3"
                            ),
                            dbc.Alert(
                                [
                                    html.Strong("Consejo práctico: "),
                                    "si tu cuota te deja sin margen de ahorro, quizá la operación sea demasiado exigente aunque el banco te la conceda."
                                ],
                                color="light",
                                className="rounded-4 mb-0"
                            ),
                        ]
                    ),
                    className="shadow-sm border-0 rounded-4 mb-4"
                )
            )
        ),

        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2("FAQ rápida", className="h4 mb-3 fw-bold"),

                            html.H3("¿Qué cuota es razonable?", className="h6 fw-bold"),
                            html.P(
                                "Como referencia general, muchas personas intentan que la cuota no supere el 30%-35% de sus ingresos netos mensuales. Cuanto más por debajo estés, mayor margen tendrás para ahorrar e invertir.",
                                className="text-muted",
                            ),

                            html.H3("¿Qué falta en esta simulación?", className="h6 fw-bold"),
                            html.P(
                                "No incluye seguros, productos vinculados, amortizaciones anticipadas, comisiones de apertura, tasación, posibles bonificaciones ni cambios futuros del tipo de interés si la hipoteca es variable.",
                                className="text-muted",
                            ),

                            html.H3("¿Sirve para hipoteca fija y variable?", className="h6 fw-bold"),
                            html.P(
                                "Funciona especialmente bien para hipoteca fija. En variable, úsala como estimación con un tipo medio esperado.",
                                className="text-muted",
                            ),

                            html.H3("¿Por qué el coste total es tan superior al precio de la vivienda?", className="h6 fw-bold"),
                            html.P(
                                "Porque al precio de compra debes sumarle entrada, gastos iniciales e intereses del préstamo. Esa diferencia es la que suele infravalorarse al comprar vivienda.",
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
    Output("metric-cuota", "children"),
    Output("metric-intereses", "children"),
    Output("metric-principal", "children"),
    Output("metric-entrada", "children"),
    Output("metric-gastos", "children"),
    Output("hipoteca-sobrecoste", "children"),
    Output("hipoteca-pct-total", "children"),
    Output("hipoteca-total-pagado", "children"),
    Output("hipoteca-desembolso-total", "children"),
    Output("hipoteca-pct-intereses", "children"),
    Output("hipoteca-fig", "figure"),
    Output("hipoteca-coste-fig", "figure"),
    Output("hipoteca-plazos-fig", "figure"),
    Output("hipoteca-inversion-box", "children"),
    Output("hipoteca-entradas-fig", "figure"),
    Output("hipoteca-entradas-tabla", "children"),
    Output("hipoteca-insights", "children"),
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

    fig_amortizacion = crear_figura_amortizacion(filas)
    fig_coste = crear_figura_coste(data)
    fig_plazos = crear_figura_comparativa_plazos(precio, entrada_pct, interes_anual, gastos_pct)
    fig_entradas, tabla_entradas = crear_figura_comparativa_entradas(precio, interes_anual, anos, gastos_pct)

    sobrecoste = max(data["desembolso_total"] - precio, 0)

    inversion_7 = calcular_valor_futuro_aportes(data["cuota"], 7, anos)
    inversion_5 = calcular_valor_futuro_aportes(data["cuota"], 5, anos)

    inversion_box = dbc.Card(
        dbc.CardBody(
            [
                html.Div("Simulación orientativa", className="text-muted small text-uppercase fw-semibold mb-2"),
                html.Div(
                    f"Si invirtieras una cantidad equivalente a la cuota mensual durante {anos} años:",
                    className="mb-3"
                ),
                html.Ul(
                    [
                        html.Li([html.Strong("Al 5% anual: "), fmt_eur(inversion_5)]),
                        html.Li([html.Strong("Al 7% anual: "), fmt_eur(inversion_7)]),
                    ],
                    className="mb-3"
                ),
                html.P(
                    "No significa que invertir sea siempre mejor que amortizar. Sirve para comparar el coste de oportunidad del dinero.",
                    className="text-muted small mb-0"
                ),
            ]
        ),
        className="border-0 bg-light rounded-4"
    )

    insights = generar_insights(data, precio)
    insights_component = html.Ul(
        [html.Li(texto, className="mb-2") for texto in insights],
        className="mb-0"
    )

    metric_cuota = metric_card(
        "Cuota mensual",
        fmt_eur(data["cuota"]),
        "La cantidad aproximada que pagarías cada mes.",
        highlight=True
    )

    metric_intereses = metric_card(
        "Intereses totales",
        fmt_eur(data["intereses_totales"]),
        "Lo que acabarías pagando al banco solo por financiarte."
    )

    metric_principal = metric_card(
        "Capital financiado",
        fmt_eur(data["principal"]),
        "Importe del préstamo."
    )

    metric_entrada = metric_card(
        "Entrada",
        fmt_eur(data["entrada_eur"]),
        "Aportación inicial estimada."
    )

    metric_gastos = metric_card(
        "Gastos iniciales",
        fmt_eur(data["gastos_eur"]),
        "Impuestos y otros costes estimados."
    )

    return (
        metric_cuota,
        metric_intereses,
        metric_principal,
        metric_entrada,
        metric_gastos,
        fmt_eur(sobrecoste),
        fmt_pct(data["porcentaje_desembolso_sobre_precio"]),
        fmt_eur(data["total_pagado"]),
        fmt_eur(data["desembolso_total"]),
        fmt_pct(data["porcentaje_intereses_sobre_prestamo"]),
        fig_amortizacion,
        fig_coste,
        fig_plazos,
        inversion_box,
        fig_entradas,
        tabla_entradas,
        insights_component,
    )
