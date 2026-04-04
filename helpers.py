import numpy as np

# =========================================================
# FORMATEO
# =========================================================

def formatear_euros_es(valor):
    """
    Formatea número a estilo español: 1.234,56 €
    """
    try:
        return f"{valor:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "0,00 €"


def formatear_porcentaje(valor):
    """
    Convierte 0.07 -> 7,00 %
    """
    try:
        return f"{valor*100:,.2f} %".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "0,00 %"


# =========================================================
# PARSEO NUMÉRICO (CLAVE PARA INPUTS)
# =========================================================

def parse_number(value):
    """
    Convierte inputs tipo:
    - "1.000"
    - "1,000"
    - "1000"
    - "1.000,50"

    a float correcto
    """
    if value is None or value == "":
        return 0.0

    if isinstance(value, (int, float)):
        return float(value)

    value = str(value).strip()

    # Caso español: 1.234,56
    if "." in value and "," in value:
        value = value.replace(".", "").replace(",", ".")
    # Caso europeo simple: 1.234
    elif "." in value:
        value = value.replace(".", "")
    # Caso inglés: 1,234
    elif "," in value:
        value = value.replace(",", "")

    try:
        return float(value)
    except:
        return 0.0


# =========================================================
# INTERÉS COMPUESTO
# =========================================================

def calcular_interes_compuesto(
    capital_inicial,
    aportacion_mensual,
    años,
    rentabilidad_anual,
    inflacion=0.0,
    comision=0.0
):
    """
    Devuelve evolución año a año
    """

    meses = años * 12
    r_mensual = (1 + rentabilidad_anual) ** (1/12) - 1
    inflacion_mensual = (1 + inflacion) ** (1/12) - 1

    capital = capital_inicial
    total_aportado = capital_inicial

    evolucion = []

    for mes in range(1, meses + 1):
        capital = capital * (1 + r_mensual)
        capital += aportacion_mensual

        total_aportado += aportacion_mensual

        # aplicar comisión anual prorrateada
        capital *= (1 - comision / 12)

        # guardar por año
        if mes % 12 == 0:
            valor_real = capital / ((1 + inflacion_mensual) ** mes)

            evolucion.append({
                "año": mes // 12,
                "total": capital,
                "aportado": total_aportado,
                "real": valor_real
            })

    return evolucion


# =========================================================
# FIRE
# =========================================================

def calcular_fire(
    gastos_mensuales,
    tasa_retiro=0.04
):
    """
    Capital necesario para FIRE
    """
    gastos_anuales = gastos_mensuales * 12
    capital_objetivo = gastos_anuales / tasa_retiro
    return capital_objetivo


def años_para_fire(
    capital_actual,
    aportacion_mensual,
    rentabilidad,
    objetivo
):
    """
    Calcula años necesarios para alcanzar FIRE
    """

    capital = capital_actual
    meses = 0

    while capital < objetivo and meses < 1000 * 12:
        capital = capital * (1 + rentabilidad / 12)
        capital += aportacion_mensual
        meses += 1

    return meses / 12


# =========================================================
# HIPOTECA
# =========================================================

def calcular_hipoteca(
    capital,
    interes_anual,
    años
):
    """
    Cuota mensual hipotecaria
    """

    meses = años * 12
    interes_mensual = interes_anual / 12

    if interes_mensual == 0:
        return capital / meses

    cuota = capital * (
        interes_mensual * (1 + interes_mensual) ** meses
    ) / (
        (1 + interes_mensual) ** meses - 1
    )

    return cuota


def cuadro_amortizacion(
    capital,
    interes_anual,
    años
):
    """
    Devuelve tabla de amortización
    """

    cuota = calcular_hipoteca(capital, interes_anual, años)
    saldo = capital
    interes_mensual = interes_anual / 12

    tabla = []

    for mes in range(1, años * 12 + 1):
        interes = saldo * interes_mensual
        amortizacion = cuota - interes
        saldo -= amortizacion

        tabla.append({
            "mes": mes,
            "cuota": cuota,
            "interes": interes,
            "amortizacion": amortizacion,
            "saldo": max(saldo, 0)
        })

    return tabla
