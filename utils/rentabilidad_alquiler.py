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
        txt = f"{value:,.{dec}f}"
        txt = txt.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"{txt} €"
    except Exception:
        return "0,00 €"


def fmt_pct(value, dec=2):
    try:
        return f"{float(value):.{dec}f} %".replace(".", ",")
    except Exception:
        return "0,00 %"


def cuota_hipoteca_mensual(capital, interes_anual_pct, años):
    capital = safe_float(capital)
    interes_anual_pct = safe_float(interes_anual_pct)
    años = max(int(safe_float(años, 25)), 1)

    if capital <= 0:
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
    ingresos_anuales = alquiler_mensual * 12 * (ocupacion_pct / 100)
    gasto_gestion = ingresos_anuales * (gestion_pct / 100)
    gastos_anuales = ibi + comunidad + seguro + mantenimiento + gasto_gestion
    beneficio_antes_irpf = ingresos_anuales - gastos_anuales
    irpf = max(beneficio_antes_irpf, 0) * (irpf_pct / 100)
    beneficio_neto = beneficio_antes_irpf - irpf

    return {
        "inversion_total": inversion_total,
        "ingresos_anuales": ingresos_anuales,
        "gasto_gestion": gasto_gestion,
        "gastos_anuales": gastos_anuales,
        "beneficio_antes_irpf": beneficio_antes_irpf,
        "irpf": irpf,
        "beneficio_neto": beneficio_neto,
        "rent_bruta": ingresos_anuales / inversion_total * 100 if inversion_total > 0 else 0,
        "rent_neta": beneficio_neto / inversion_total * 100 if inversion_total > 0 else 0,
        "cashflow_mensual": beneficio_neto / 12,
    }


def semaforo(rent_neta):
    if rent_neta >= 7:
        return "Muy atractiva", "success", "La operación parece muy interesante para una primera estimación."
    if rent_neta >= 5:
        return "Buena", "primary", "La rentabilidad parece sólida y merece análisis más profundo."
    if rent_neta >= 3:
        return "Aceptable", "warning", "Puede tener sentido, pero está más ajustada."
    return "Floja", "danger", "Con estos supuestos, revisaría precio, gastos o renta esperada."


def proyeccion_10_anios(
    inversion_inicial,
    alquiler_mensual,
    ocupacion_pct,
    gastos_anuales,
    irpf_pct,
    crecimiento_alquiler_pct,
    crecimiento_gastos_pct,
    revalorizacion_inmueble_pct,
    sp500_pct,
):
    years = list(range(1, 11))
    alquiler_actual = alquiler_mensual
    gastos_actuales = gastos_anuales
    valor_inmueble = inversion_inicial
    valor_sp500 = inversion_inicial
    inmueble_vals = []
    sp500_vals = []
    rows = []
    cash_acumulado = 0.0

    for y in years:
        ingresos = alquiler_actual * 12 * (ocupacion_pct / 100)
        beneficio_antes_irpf = ingresos - gastos_actuales
        irpf = max(beneficio_antes_irpf, 0) * (irpf_pct / 100)
        beneficio_neto = beneficio_antes_irpf - irpf

        cash_acumulado += beneficio_neto
        valor_inmueble *= 1 + revalorizacion_inmueble_pct / 100
        valor_total_inmueble = valor_inmueble + cash_acumulado
        valor_sp500 *= 1 + sp500_pct / 100

        inmueble_vals.append(valor_total_inmueble)
        sp500_vals.append(valor_sp500)

        rows.append(
            {
                "anio": y,
                "ingresos": ingresos,
                "gastos": gastos_actuales,
                "beneficio_neto": beneficio_neto,
                "valor_total_inmueble": valor_total_inmueble,
                "valor_sp500": valor_sp500,
            }
        )

        alquiler_actual *= 1 + crecimiento_alquiler_pct / 100
        gastos_actuales *= 1 + crecimiento_gastos_pct / 100

    return years, inmueble_vals, sp500_vals, rows


def calc_payback_years(inversion_inicial, beneficio_neto_anual):
    if beneficio_neto_anual <= 0:
        return None
    return inversion_inicial / beneficio_neto_anual
