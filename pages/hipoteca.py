from dash import html, dcc, register_page, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

register_page(
    __name__,
    path="/hipoteca",
    name="Calculadora Hipoteca",
    title="Calculadora de hipoteca | interescompuesto.app",
    description="Calcula la cuota mensual de tu hipoteca, intereses totales, entrada necesaria, esfuerzo financiero y coste final del préstamo."
)

# =========================================================
# HELPERS
# =========================================================
def safe_num(value, default=0):
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default


def fmt_eur(value):
    try:
        s = f"{float(value):,.2f}"
        s = s.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{s} €"
    except Exception:
        return "0,00 €"


def fmt_pct(value):
    try:
        s = f"{float(value):.2f}".replace(".", ",")
        return f"{s} %"
    except Exception:
        return "0,00 %"


def fmt_num(value, decimals=2):
    try:
        s = f"{float(value):,.{decimals}f}"
        return s.replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return "0"


def fmt_meses_anos(meses):
    meses = int(round(max(safe_num(meses), 0)))
    anos = meses // 12
    meses_restantes = meses % 12

    if anos == 0:
        return f"{meses_restantes} meses"
    if meses_restantes == 0:
        return f"{anos} años"
    return f"{anos} años y {meses_restantes} meses"


def calcular_hipoteca(precio_vivienda, entrada_pct, interes_anual, anos, gastos_pct=10):
    precio_vivienda = max(safe_num(precio_vivienda), 0)
    entrada_pct = min(max(safe_num(entrada_pct), 0), 100)
    interes_anual = max(safe_num(interes_anual), 0)
    anos = max(safe_num(anos), 0)
    gastos_pct = max(safe_num(gastos_pct), 0)

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
    ahorro_necesario = entrada_eur + gastos_eur
    porcentaje_intereses_sobre_prestamo = (intereses_totales / principal * 100) if principal > 0 else 0
    porcentaje_desembolso_sobre_precio = (desembolso_total / precio_vivienda * 100) if precio_vivienda > 0 else 0

    return {
        "precio_vivienda": precio_vivienda,
        "entrada_pct": entrada_pct,
        "entrada_eur": entrada_eur,
        "gastos_eur": gastos_eur,
        "principal": principal,
        "cuota": cuota,
        "total_pagado": total_pagado,
        "intereses_totales": intereses_totales,
        "desembolso_total": desembolso_total,
        "meses": n,
        "interes_mensual": r,
        "interes_anual": interes_anual,
        "anos": anos,
        "gastos_pct": gastos_pct,
        "ahorro_necesario": ahorro_necesario,
        "porcentaje_intereses_sobre_prestamo": porcentaje_intereses_sobre_prestamo,
        "porcentaje_desembolso_sobre_precio": porcentaje_desembolso_sobre_precio,
    }


def calcular_principal_desde_cuota(cuota_mensual, interes_anual, anos):
    cuota_mensual = max(safe_num(cuota_mensual), 0)
    interes_anual = max(safe_num(interes_anual), 0)
    anos = max(safe_num(anos), 0)

    n = int(anos * 12)
    r = interes_anual / 100 / 12

    if cuota_mensual <= 0 or n <= 0:
        return 0

    if r == 0:
        return cuota_mensual * n

    return cuota_mensual * (((1 + r) ** n - 1) / (r * (1 + r) ** n))


def calcular_capacidad_compra(
    ingresos_netos,
    deudas_mensuales,
    esfuerzo_pct,
    ahorro_disponible,
    entrada_pct,
    gastos_pct,
    interes_anual,
    anos,
):
    ingresos_netos = max(safe_num(ingresos_netos), 0)
    deudas_mensuales = max(safe_num(deudas_mensuales), 0)
    esfuerzo_pct = max(safe_num(esfuerzo_pct), 0)
    ahorro_disponible = max(safe_num(ahorro_disponible), 0)
    entrada_pct = max(safe_num(entrada_pct), 0)
    gastos_pct = max(safe_num(gastos_pct), 0)
    interes_anual = max(safe_num(interes_anual), 0)
    anos = max(safe_num(anos), 0)

    cuota_max = ingresos_netos * (esfuerzo_pct / 100) - deudas_mensuales
    cuota_max = max(cuota_max, 0)

    principal_max = calcular_principal_desde_cuota(cuota_max, interes_anual, anos)

    ratio_entrada = entrada_pct / 100
    ratio_gastos = gastos_pct / 100
    ratio_ahorro_total = ratio_entrada + ratio_gastos

    if ratio_ahorro_total > 0:
        precio_max_por_ahorro = ahorro_disponible / ratio_ahorro_total
    else:
        precio_max_por_ahorro = 0

    if ratio_entrada < 1:
        precio_max_por_financiacion = principal_max / (1 - ratio_entrada)
    else:
        precio_max_por_financiacion = 0

    precio_max_comprable = min(precio_max_por_ahorro, precio_max_por_financiacion)

    entrada_necesaria = precio_max_comprable * ratio_entrada
    gastos_necesarios = precio_max_comprable * ratio_gastos
    ahorro_necesario = entrada_necesaria + gastos_necesarios

    if precio_max_comprable <= 0:
        factor_limitante = "No puedes asumir compra con estos parámetros."
    elif precio_max_por_ahorro < precio_max_por_financiacion:
        factor_limitante = "Tu ahorro disponible limita más que la cuota."
    elif precio_max_por_financiacion < precio_max_por_ahorro:
        factor_limitante = "Tu capacidad de cuota limita más que el ahorro."
    else:
        factor_limitante = "Ahorro y financiación limitan de forma similar."

    return {
        "cuota_max": cuota_max,
        "principal_max": principal_max,
        "precio_max_por_ahorro": precio_max_por_ahorro,
        "precio_max_por_financiacion": precio_max_por_financiacion,
        "precio_max_comprable": precio_max_comprable,
        "entrada_necesaria": entrada_necesaria,
        "gastos_necesarios": gastos_necesarios,
        "ahorro_necesario": ahorro_necesario,
        "factor_limitante": factor_limitante,
    }


def generar_tabla_amortizacion(principal, interes_mensual, cuota, meses, max_meses=480):
    saldo = principal
    filas = []

    for mes in range(1, min(meses, max_meses) + 1):
        interes_mes = saldo * interes_mensual if interes_mensual > 0 else 0
        amortizacion = cuota - interes_mes if meses > 0 else 0

        if interes_mensual == 0 and meses > 0:
            amortizacion = principal / meses

        amortizacion = max(amortizacion, 0)
        saldo = max(saldo - amortizacion, 0)

        filas.append(
            {
                "mes": mes,
                "interes": max(interes_mes, 0),
                "amortizacion": amortizacion,
                "saldo": saldo,
            }
        )

        if saldo <= 0:
            break

    return filas


def resumir_por_ano(filas):
    resumen = []
    if not filas:
        return resumen

    total_anios = int((filas[-1]["mes"] - 1) / 12) + 1

    for ano in range(1, total_anios + 1):
        inicio = (ano - 1) * 12 + 1
        fin = ano * 12
        filas_ano = [f for f in filas if inicio <= f["mes"] <= fin]
        if not filas_ano:
            continue

        interes_ano = sum(f["interes"] for f in filas_ano)
        amort_ano = sum(f["amortizacion"] for f in filas_ano)
        saldo_final = filas_ano[-1]["saldo"]

        resumen.append(
            {
                "ano": ano,
                "interes": interes_ano,
                "amortizacion": amort_ano,
                "saldo": saldo_final,
            }
        )

    return resumen


def calcular_plan_ahorro(ahorro_objetivo, aportaciones=None):
    ahorro_objetivo = max(safe_num(ahorro_objetivo), 0)
    if aportaciones is None:
        aportaciones = [300, 500, 700, 1000]

    resultados = []
    for aportacion in aportaciones:
        aportacion = max(safe_num(aportacion), 1)
        meses = ahorro_objetivo / aportacion if aportacion > 0 else 0
        resultados.append(
            {
                "aportacion": aportacion,
                "meses": meses,
                "texto": fmt_meses_anos(meses),
            }
        )
    return resultados


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
        margin=dict(l=20, r=20, t=35, b=20),
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
                x=["Coste total"],
                y=[data["principal"]],
                name="Capital financiado",
                hovertemplate="Capital financiado: %{y:,.2f} €<extra></extra>",
            ),
            go.Bar(
                x=["Coste total"],
                y=[data["intereses_totales"]],
                name="Intereses",
                hovertemplate="Intereses: %{y:,.2f} €<extra></extra>",
            ),
            go.Bar(
                x=["Coste total"],
                y=[data["gastos_eur"]],
                name="Gastos iniciales",
                hovertemplate="Gastos: %{y:,.2f} €<extra></extra>",
            ),
            go.Bar(
                x=["Coste total"],
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
        margin=dict(l=20, r=20, t=35, b=20),
        legend=dict(orientation="h", y=1.12, x=0),
        yaxis=dict(title="Euros (€)"),
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
        margin=dict(l=20, r=20, t=35, b=20),
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
        margin=dict(l=20, r=20, t=35, b=20),
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


def crear_figura_sensibilidad_tipos(precio, entrada_pct, interes_anual, anos, gastos_pct):
    base = max(safe_num(interes_anual), 0)
    opciones = [max(base - 1.0, 0), base, base + 1.0]
    etiquetas = [f"{fmt_num(x)} %" for x in opciones]

    cuotas = []
    intereses = []
    for tipo in opciones:
        data = calcular_hipoteca(precio, entrada_pct, tipo, anos, gastos_pct)
        cuotas.append(data["cuota"])
        intereses.append(data["intereses_totales"])

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=etiquetas,
            y=cuotas,
            name="Cuota mensual",
            hovertemplate="Tipo %{x}<br>Cuota: %{y:,.2f} €<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=etiquetas,
            y=intereses,
            mode="lines+markers",
            name="Intereses totales",
            yaxis="y2",
            hovertemplate="Tipo %{x}<br>Intereses: %{y:,.2f} €<extra></extra>",
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=420,
        margin=dict(l=20, r=20, t=35, b=20),
        legend=dict(orientation="h", y=1.1, x=0),
        xaxis=dict(title="Escenario de tipo"),
        yaxis=dict(title="Cuota mensual (€)"),
        yaxis2=dict(
            title="Intereses totales (€)",
            overlaying="y",
            side="right",
            showgrid=False,
        ),
    )
    return fig


def crear_figura_capacidad_compra(precio_objetivo, precio_max_comprable):
    precio_objetivo = max(safe_num(precio_objetivo), 0)
    precio_max_comprable = max(safe_num(precio_max_comprable), 0)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=["Precio objetivo", "Precio máximo estimado"],
            y=[precio_objetivo, precio_max_comprable],
            hovertemplate="%{x}<br>%{y:,.2f} €<extra></extra>",
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=360,
        margin=dict(l=20, r=20, t=35, b=20),
        xaxis=dict(title=""),
        yaxis=dict(title="Euros (€)"),
        showlegend=False,
    )
    return fig


def crear_figura_plan_ahorro(resultados):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=[f"{int(r['aportacion'])} €/mes" for r in resultados],
            y=[r["meses"] for r in resultados],
            hovertemplate="%{x}<br>%{y:.1f} meses<extra></extra>",
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=360,
        margin=dict(l=20, r=20, t=35, b=20),
        xaxis=dict(title="Ahorro mensual"),
        yaxis=dict(title="Meses necesarios"),
        showlegend=False,
    )
    return fig


def calcular_valor_futuro_aportes(aporte_mensual, rentabilidad_anual, anos):
    meses = max(int(anos * 12), 0)
    r = rentabilidad_anual / 100 / 12

    if meses <= 0 or aporte_mensual <= 0:
        return 0

    if r == 0:
        return aporte_mensual * meses

    return aporte_mensual * (((1 + r) ** meses - 1) / r)


def generar_insights(data, ingreso_neto_mensual):
    cuota = data["cuota"]
    precio = data["precio_vivienda"]
    principal = data["principal"]
    intereses = data["intereses_totales"]
    desembolso_total = data["desembolso_total"]
    pct_intereses = data["porcentaje_intereses_sobre_prestamo"]
    pct_total = data["porcentaje_desembolso_sobre_precio"]

    insights = []

    if principal <= 0:
        insights.append("La financiación es 0 €, así que en esta simulación no habría préstamo hipotecario.")
    elif pct_intereses < 20:
        insights.append("El peso de los intereses es relativamente contenido para el importe financiado.")
    elif pct_intereses < 50:
        insights.append("El coste financiero ya es relevante: pagarás una parte importante del préstamo solo en intereses.")
    else:
        insights.append("El coste financiero es alto: terminarías pagando una cantidad muy elevada solo en intereses.")

    sobrecoste = desembolso_total - precio
    if sobrecoste > 0:
        insights.append(
            f"Aunque la vivienda cuesta {fmt_eur(precio)}, el desembolso total estimado sube a {fmt_eur(desembolso_total)}. "
            f"Eso son {fmt_eur(sobrecoste)} adicionales entre entrada, gastos e intereses."
        )

    if pct_total < 120:
        insights.append("El coste total final no se dispara demasiado respecto al precio de compra.")
    elif pct_total < 150:
        insights.append("El coste total final ya se aleja bastante del precio de la vivienda.")
    else:
        insights.append("El coste total final se dispara mucho respecto al precio inicial de la vivienda.")

    ingreso_neto_mensual = safe_num(ingreso_neto_mensual)
    if ingreso_neto_mensual > 0:
        ratio = (cuota / ingreso_neto_mensual) * 100 if ingreso_neto_mensual > 0 else 0
        if ratio < 25:
            insights.append("La cuota representa una parte bastante manejable de tus ingresos netos mensuales.")
        elif ratio <= 35:
            insights.append("La cuota entra en una zona razonable, aunque conviene mantener ahorro y margen para imprevistos.")
        elif ratio <= 45:
            insights.append("La cuota ya es exigente para tu nivel de ingresos. Hay riesgo de ir demasiado justo.")
        else:
            insights.append("La cuota parece demasiado alta para tus ingresos netos mensuales y puede tensionar mucho tus finanzas.")

    if intereses > principal:
        insights.append("En esta simulación pagarías más en intereses que la mitad del capital financiado, señal de un préstamo caro o muy largo.")

    return insights


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


def build_amort_table(resumen_anual):
    if not resumen_anual:
        return dbc.Alert("No hay datos suficientes para generar la tabla de amortización.", color="light", class_name="rounded-4 mb-0")

    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Año"),
                        html.Th("Intereses pagados"),
                        html.Th("Capital amortizado"),
                        html.Th("Saldo pendiente"),
                    ]
                )
            ),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(r["ano"]),
                            html.Td(fmt_eur(r["interes"])),
                            html.Td(fmt_eur(r["amortizacion"])),
                            html.Td(fmt_eur(r["saldo"])),
                        ]
                    )
                    for r in resumen_anual
                ]
            ),
        ],
        bordered=False,
        hover=True,
        responsive=True,
        class_name="align-middle mb-0",
    )


def build_esfuerzo_box(cuota, ingreso_neto_mensual):
    ingreso_neto_mensual = safe_num(ingreso_neto_mensual)
    if ingreso_neto_mensual <= 0:
        return dbc.Alert(
            "Añade tus ingresos netos mensuales para estimar si la cuota encaja con tu presupuesto.",
            color="light",
            class_name="rounded-4 mb-0",
        )

    ratio = (cuota / ingreso_neto_mensual) * 100 if ingreso_neto_mensual > 0 else 0

    if ratio < 25:
        color = "success"
        etiqueta = "Muy razonable"
        comentario = "La cuota deja margen para ahorrar, invertir y afrontar imprevistos."
    elif ratio <= 35:
        color = "primary"
        etiqueta = "Razonable"
        comentario = "Está en una zona normalmente aceptable, pero conviene no apurar el presupuesto."
    elif ratio <= 45:
        color = "warning"
        etiqueta = "Exigente"
        comentario = "La cuota ya puede presionar bastante tus finanzas mensuales."
    else:
        color = "danger"
        etiqueta = "Muy exigente"
        comentario = "La cuota parece demasiado alta para tus ingresos netos mensuales."

    return dbc.Card(
        dbc.CardBody(
            [
                html.Div("Esfuerzo financiero", className="text-muted small text-uppercase fw-semibold mb-2"),
                html.Div(f"{fmt_pct(ratio)} de tus ingresos", className="fw-bold mb-2", style={"fontSize": "1.7rem"}),
                dbc.Progress(value=min(ratio, 100), color=color, class_name="mb-3", style={"height": "12px"}),
                html.Div(etiqueta, className=f"fw-semibold text-{color} mb-1"),
                html.Div(comentario, className="text-muted small"),
            ]
        ),
        className="shadow-sm border-0 rounded-4 h-100"
    )


def build_plan_ahorro_table(resultados):
    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Ahorro mensual"),
                        html.Th("Meses estimados"),
                        html.Th("Tiempo aproximado"),
                    ]
                )
            ),
            html.Tbody(
                                [
                    html.Tr(
                        [
                            html.Td(f"{int(r['aportacion'])} €/mes"),
                            html.Td(f"{fmt_num(r['meses'], 1)} meses"),
                            html.Td(r["texto"]),
                        ]
                    )
                    for r in resultados
                ]
            ),
        ],
        bordered=False,
        hover=True,
        responsive=True,
        class_name="align-middle mb-0",
    )


def section_title(title, subtitle=None):
    return html.Div(
        [
            html.H2(title, className="fw-bold mb-2"),
            html.P(subtitle, className="text-muted mb-0") if subtitle else None,
        ],
        className="mb-4",
    )


def input_block(label, input_id, value, type_="number", step=None, min_=None, max_=None, suffix=None):
    input_group_children = [
        dbc.Input(
            id=input_id,
            type=type_,
            value=value,
            step=step,
            min=min_,
            max=max_,
            class_name="rounded-3",
        )
    ]

    if suffix:
        input_group_children.append(dbc.InputGroupText(suffix))

    return dbc.Col(
        [
            dbc.Label(label, html_for=input_id, class_name="fw-semibold mb-2"),
            dbc.InputGroup(input_group_children, class_name="mb-3"),
        ],
        md=6,
        lg=4,
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
                            [
                                html.Span("Calculadora de hipoteca", className="badge bg-light text-dark rounded-pill px-3 py-2 mb-3"),
                                html.H1("Calcula tu hipoteca y el coste real de comprar vivienda", className="display-5 fw-bold mb-3"),
                                html.P(
                                    "Simula cuota mensual, intereses, entrada, gastos, esfuerzo financiero, capacidad de compra y plan de ahorro previo.",
                                    className="lead text-muted mb-0",
                                ),
                            ],
                            className="py-4 py-lg-5",
                        )
                    ],
                    lg=8,
                )
            ]
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    section_title(
                        "1. Datos de la vivienda y financiación",
                        "Introduce tus hipótesis para estimar la cuota, el coste total y el ahorro inicial necesario.",
                    ),
                    dbc.Row(
                        [
                            input_block("Precio de la vivienda", "hip-precio", 250000, step=1000, min_=0, suffix="€"),
                            input_block("Entrada", "hip-entrada", 20, step=1, min_=0, max_=100, suffix="%"),
                            input_block("Tipo de interés anual", "hip-interes", 3.0, step=0.1, min_=0, suffix="%"),
                            input_block("Plazo", "hip-anos", 30, step=1, min_=1, suffix="años"),
                            input_block("Gastos iniciales estimados", "hip-gastos", 10, step=0.5, min_=0, suffix="%"),
                            input_block("Ingresos netos mensuales", "hip-ingresos", 2100, step=50, min_=0, suffix="€"),
                        ]
                    ),
                ]
            ),
            class_name="shadow-sm border-0 rounded-4 mb-4",
        ),

        dbc.Row(
            id="hip-metricas-principales",
            class_name="g-3 mb-4",
        ),

        dbc.Row(
            class_name="g-4 mb-4",
            children=[
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                section_title("Esfuerzo financiero", "Qué parte de tus ingresos se iría a la cuota."),
                                html.Div(id="hip-esfuerzo-box"),
                            ]
                        ),
                        class_name="shadow-sm border-0 rounded-4 h-100",
                    ),
                    lg=5,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                section_title("Lectura rápida", "Conclusiones útiles para interpretar la simulación."),
                                html.Div(id="hip-insights"),
                            ]
                        ),
                        class_name="shadow-sm border-0 rounded-4 h-100",
                    ),
                    lg=7,
                ),
            ],
        ),

        dbc.Row(
            class_name="g-4 mb-4",
            children=[
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                section_title("Desglose del coste total", "Entrada, gastos, capital e intereses."),
                                dcc.Graph(id="hip-fig-coste", config={"displayModeBar": False}),
                            ]
                        ),
                        class_name="shadow-sm border-0 rounded-4 h-100",
                    ),
                    lg=6,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                section_title("Amortización mes a mes", "Cómo evoluciona tu hipoteca con el tiempo."),
                                dcc.Graph(id="hip-fig-amortizacion", config={"displayModeBar": False}),
                            ]
                        ),
                        class_name="shadow-sm border-0 rounded-4 h-100",
                    ),
                    lg=6,
                ),
            ],
        ),

        dbc.Row(
            class_name="g-4 mb-4",
            children=[
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                section_title("Comparativa por plazo", "Más plazo baja cuota, pero suele elevar intereses."),
                                dcc.Graph(id="hip-fig-plazos", config={"displayModeBar": False}),
                            ]
                        ),
                        class_name="shadow-sm border-0 rounded-4 h-100",
                    ),
                    lg=6,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                section_title("Sensibilidad a tipos", "Cómo cambia la hipoteca si sube o baja el interés."),
                                dcc.Graph(id="hip-fig-tipos", config={"displayModeBar": False}),
                            ]
                        ),
                        class_name="shadow-sm border-0 rounded-4 h-100",
                    ),
                    lg=6,
                ),
            ],
        ),

        dbc.Row(
            class_name="g-4 mb-4",
            children=[
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                section_title("Comparativa por entrada", "Ver cuánto cambia la cuota e intereses según tu aportación inicial."),
                                dcc.Graph(id="hip-fig-entradas", config={"displayModeBar": False}),
                            ]
                        ),
                        class_name="shadow-sm border-0 rounded-4 h-100",
                    ),
                    lg=7,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                section_title("Resumen de escenarios de entrada"),
                                html.Div(id="hip-tabla-entradas"),
                            ]
                        ),
                        class_name="shadow-sm border-0 rounded-4 h-100",
                    ),
                    lg=5,
                ),
            ],
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    section_title(
                        "2. Tabla de amortización anual",
                        "Resumen año a año con intereses pagados, capital amortizado y saldo pendiente.",
                    ),
                    html.Div(id="hip-tabla-amortizacion"),
                ]
            ),
            class_name="shadow-sm border-0 rounded-4 mb-4",
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    section_title(
                        "3. ¿Qué vivienda podrías permitirte?",
                        "Estimación aproximada en función de ingresos, deudas, ahorro disponible y condiciones de financiación.",
                    ),
                    dbc.Row(
                        [
                            input_block("Deudas mensuales", "cap-deudas", 0, step=50, min_=0, suffix="€"),
                            input_block("Esfuerzo máximo deseado", "cap-esfuerzo", 35, step=1, min_=0, max_=100, suffix="%"),
                            input_block("Ahorro disponible", "cap-ahorro", 60000, step=1000, min_=0, suffix="€"),
                            input_block("Precio objetivo", "cap-precio-objetivo", 250000, step=1000, min_=0, suffix="€"),
                        ],
                        class_name="mb-2",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(html.Div(id="cap-metricas"), lg=6),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.Div("Factor limitante", className="text-muted small text-uppercase fw-semibold mb-2"),
                                            html.Div(id="cap-factor-limitante", className="fw-semibold"),
                                        ]
                                    ),
                                    class_name="bg-light border-0 rounded-4 h-100",
                                ),
                                lg=6,
                            ),
                        ],
                        class_name="g-3 mb-4",
                    ),
                    dcc.Graph(id="cap-fig", config={"displayModeBar": False}),
                ]
            ),
            class_name="shadow-sm border-0 rounded-4 mb-4",
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    section_title(
                        "4. Plan de ahorro para la entrada",
                        "Cuánto tiempo tardarías en reunir la entrada más gastos si ahorras de forma constante.",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.Div("Ahorro objetivo estimado", className="text-muted small text-uppercase fw-semibold mb-2"),
                                            html.Div(id="ahorro-objetivo", className="fw-bold", style={"fontSize": "1.9rem"}),
                                            html.Div("Se calcula con la entrada y los gastos iniciales.", className="text-muted small mt-2"),
                                        ]
                                    ),
                                    class_name="bg-light border-0 rounded-4 h-100",
                                ),
                                lg=4,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.Div("Si invirtieras ese ahorro al 7% anual", className="text-muted small text-uppercase fw-semibold mb-2"),
                                            html.Div(id="coste-oportunidad", className="fw-bold", style={"fontSize": "1.9rem"}),
                                            html.Div("Valor futuro aproximado de aportar 500 €/mes durante el mismo periodo.", className="text-muted small mt-2"),
                                        ]
                                    ),
                                    class_name="bg-light border-0 rounded-4 h-100",
                                ),
                                lg=8,
                            ),
                        ],
                        class_name="g-3 mb-4",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            dcc.Graph(id="plan-ahorro-fig", config={"displayModeBar": False}),
                                        ]
                                    ),
                                    class_name="border-0 rounded-4 h-100",
                                ),
                                lg=6,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.Div(id="plan-ahorro-tabla"),
                                        ]
                                    ),
                                    class_name="border-0 rounded-4 h-100",
                                ),
                                lg=6,
                            ),
                        ],
                        class_name="g-4",
                    ),
                ]
            ),
            class_name="shadow-sm border-0 rounded-4 mb-5",
        ),

        dbc.Card(
            dbc.CardBody(
                [
                    section_title("Preguntas rápidas", "Reglas orientativas, no asesoramiento personalizado."),
                    dbc.Row(
                        [
                            dbc.Col(
                                dbc.Alert(
                                    [
                                        html.Div("• Muchos bancos miran que la cuota no supere aproximadamente el 30%-35% de tus ingresos netos."),
                                        html.Div("• A mayor entrada, menor cuota y menor coste total en intereses."),
                                        html.Div("• Un plazo más largo puede hacer la cuota más cómoda, pero encarece la hipoteca."),
                                        html.Div("• Ten siempre colchón adicional aparte de entrada y gastos."),
                                    ],
                                    color="light",
                                    class_name="rounded-4 mb-0 h-100",
                                ),
                                md=6,
                            ),
                            dbc.Col(
                                dbc.Alert(
                                    [
                                        html.Div("• Los gastos iniciales pueden variar según comunidad, perfil y operación."),
                                        html.Div("• Esta simulación no incluye productos vinculados, comisiones o amortizaciones anticipadas."),
                                        html.Div("• Úsala para comparar escenarios y tomar decisiones con más contexto."),
                                    ],
                                    color="light",
                                    class_name="rounded-4 mb-0 h-100",
                                ),
                                md=6,
                            ),
                        ],
                        class_name="g-3",
                    ),
                ]
            ),
            class_name="shadow-sm border-0 rounded-4 mb-5",
        ),
    ],
    fluid=True,
    class_name="py-3 py-lg-4",
)


# =========================================================
# CALLBACKS
# =========================================================
@callback(
    Output("hip-metricas-principales", "children"),
    Output("hip-esfuerzo-box", "children"),
    Output("hip-insights", "children"),
    Output("hip-fig-coste", "figure"),
    Output("hip-fig-amortizacion", "figure"),
    Output("hip-fig-plazos", "figure"),
    Output("hip-fig-tipos", "figure"),
    Output("hip-fig-entradas", "figure"),
    Output("hip-tabla-entradas", "children"),
    Output("hip-tabla-amortizacion", "children"),
    Output("ahorro-objetivo", "children"),
    Output("coste-oportunidad", "children"),
    Output("plan-ahorro-fig", "figure"),
    Output("plan-ahorro-tabla", "children"),
    Input("hip-precio", "value"),
    Input("hip-entrada", "value"),
    Input("hip-interes", "value"),
    Input("hip-anos", "value"),
    Input("hip-gastos", "value"),
    Input("hip-ingresos", "value"),
)
def update_hipoteca(precio, entrada_pct, interes_anual, anos, gastos_pct, ingresos):
    data = calcular_hipoteca(precio, entrada_pct, interes_anual, anos, gastos_pct)
    filas = generar_tabla_amortizacion(
        data["principal"],
        data["interes_mensual"],
        data["cuota"],
        data["meses"],
    )
    resumen_anual = resumir_por_ano(filas)
    insights = generar_insights(data, ingresos)
    resultados_ahorro = calcular_plan_ahorro(data["ahorro_necesario"])

    metrics = [
        dbc.Col(
            metric_card(
                "Cuota mensual",
                fmt_eur(data["cuota"]),
                subtitle=f"{int(data['meses'])} meses · {fmt_num(data['interes_anual'])} % TIN aprox.",
                highlight=True,
            ),
            sm=6,
            xl=3,
        ),
        dbc.Col(
            metric_card(
                "Capital financiado",
                fmt_eur(data["principal"]),
                subtitle=f"Entrada: {fmt_eur(data['entrada_eur'])}",
            ),
            sm=6,
            xl=3,
        ),
        dbc.Col(
            metric_card(
                "Intereses totales",
                fmt_eur(data["intereses_totales"]),
                subtitle=f"{fmt_pct(data['porcentaje_intereses_sobre_prestamo'])} sobre el préstamo",
            ),
            sm=6,
            xl=3,
        ),
        dbc.Col(
            metric_card(
                "Desembolso total",
                fmt_eur(data["desembolso_total"]),
                subtitle=f"{fmt_pct(data['porcentaje_desembolso_sobre_precio'])} del precio de compra",
            ),
            sm=6,
            xl=3,
        ),
    ]

    insights_ui = dbc.ListGroup(
        [
            dbc.ListGroupItem(text, class_name="border-0 px-0 py-2")
            for text in insights
        ],
        flush=True,
    )

    anos_ahorro_500 = (data["ahorro_necesario"] / 500) / 12 if data["ahorro_necesario"] > 0 else 0
    coste_oportunidad = calcular_valor_futuro_aportes(500, 7, anos_ahorro_500)

    fig_coste = crear_figura_coste(data)
    fig_amort = crear_figura_amortizacion(filas)
    fig_plazos = crear_figura_comparativa_plazos(precio, entrada_pct, interes_anual, gastos_pct)
    fig_tipos = crear_figura_sensibilidad_tipos(precio, entrada_pct, interes_anual, anos, gastos_pct)
    fig_entradas, tabla_entradas = crear_figura_comparativa_entradas(precio, interes_anual, anos, gastos_pct)
    tabla_amort = build_amort_table(resumen_anual)
    esfuerzo_box = build_esfuerzo_box(data["cuota"], ingresos)
    fig_plan_ahorro = crear_figura_plan_ahorro(resultados_ahorro)
    tabla_plan_ahorro = build_plan_ahorro_table(resultados_ahorro)

    return (
        metrics,
        esfuerzo_box,
        insights_ui,
        fig_coste,
        fig_amort,
        fig_plazos,
        fig_tipos,
        fig_entradas,
        tabla_entradas,
        tabla_amort,
        fmt_eur(data["ahorro_necesario"]),
        fmt_eur(coste_oportunidad),
        fig_plan_ahorro,
        tabla_plan_ahorro,
    )


@callback(
    Output("cap-metricas", "children"),
    Output("cap-factor-limitante", "children"),
    Output("cap-fig", "figure"),
    Input("hip-ingresos", "value"),
    Input("cap-deudas", "value"),
    Input("cap-esfuerzo", "value"),
    Input("cap-ahorro", "value"),
    Input("hip-entrada", "value"),
    Input("hip-gastos", "value"),
    Input("hip-interes", "value"),
    Input("hip-anos", "value"),
    Input("cap-precio-objetivo", "value"),
)
def update_capacidad_compra(
    ingresos_netos,
    deudas_mensuales,
    esfuerzo_pct,
    ahorro_disponible,
    entrada_pct,
    gastos_pct,
    interes_anual,
    anos,
    precio_objetivo,
):
    data = calcular_capacidad_compra(
        ingresos_netos,
        deudas_mensuales,
        esfuerzo_pct,
        ahorro_disponible,
        entrada_pct,
        gastos_pct,
        interes_anual,
        anos,
    )

    metrics = dbc.Row(
        [
            dbc.Col(
                metric_card(
                    "Cuota máxima estimada",
                    fmt_eur(data["cuota_max"]),
                    subtitle="Después de descontar deudas mensuales",
                    highlight=True,
                ),
                md=6,
            ),
            dbc.Col(
                metric_card(
                    "Precio máximo comprable",
                    fmt_eur(data["precio_max_comprable"]),
                    subtitle=f"Ahorro necesario: {fmt_eur(data['ahorro_necesario'])}",
                ),
                md=6,
            ),
            dbc.Col(
                metric_card(
                    "Límite por ahorro",
                    fmt_eur(data["precio_max_por_ahorro"]),
                    subtitle=f"Entrada: {fmt_eur(data['entrada_necesaria'])}",
                ),
                md=6,
                class_name="mt-3",
            ),
            dbc.Col(
                metric_card(
                    "Límite por financiación",
                    fmt_eur(data["precio_max_por_financiacion"]),
                    subtitle=f"Gastos: {fmt_eur(data['gastos_necesarios'])}",
                ),
                md=6,
                class_name="mt-3",
            ),
        ],
        class_name="g-3",
    )

    fig = crear_figura_capacidad_compra(precio_objetivo, data["precio_max_comprable"])

    return metrics, data["factor_limitante"], fig
