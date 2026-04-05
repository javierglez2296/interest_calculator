import math
import numpy as np

# =========================================================
# FORMATEO
# =========================================================

def formatear_euros_es(valor, decimales=2):
    """
    Formatea un número a estilo español.
    Ejemplo: 1234.56 -> 1.234,56 €
    """
    try:
        valor = float(valor)
        formato = f"{{:,.{decimales}f}} €"
        return formato.format(valor).replace(",", "X").replace(".", ",").replace("X", ".")
    except (TypeError, ValueError):
        return "0,00 €"


def formatear_porcentaje(valor, decimales=2, ya_decimal=True):
    """
    Formatea porcentajes en estilo español.

    ya_decimal=True:
        0.07 -> 7,00 %

    ya_decimal=False:
        7 -> 7,00 %
    """
    try:
        valor = float(valor)
        if ya_decimal:
            valor *= 100
        formato = f"{{:,.{decimales}f}} %"
        return formato.format(valor).replace(",", "X").replace(".", ",").replace("X", ".")
    except (TypeError, ValueError):
        return "0,00 %"


# =========================================================
# PARSEO NUMÉRICO
# =========================================================

def parse_number(value):
    """
    Convierte inputs comunes a float de forma robusta.

    Soporta:
    - "1000"
    - "1.000"
    - "1,000"
    - "1.000,50"
    - "1,000.50"
    - "  2 500,75 € "
    - "7%"
    """
    if value is None:
        return 0.0

    if isinstance(value, (int, float, np.integer, np.floating)):
        return float(value)

    s = str(value).strip()

    if s == "":
        return 0.0

    # limpiar símbolos habituales
    s = (
        s.replace("€", "")
         .replace("%", "")
         .replace("\u00a0", "")   # non-breaking space
         .replace(" ", "")
    )

    # si contiene . y , decidimos por la última aparición
    if "." in s and "," in s:
        if s.rfind(",") > s.rfind("."):
            # español: 1.234,56
            s = s.replace(".", "").replace(",", ".")
        else:
            # inglés: 1,234.56
            s = s.replace(",", "")
    elif "," in s:
        # caso con solo coma:
        # si hay una sola coma y parece decimal -> 12,5
        # si no -> miles -> 1,234
        partes = s.split(",")
        if len(partes) == 2 and len(partes[1]) <= 2:
            s = s.replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "." in s:
        # caso con solo punto:
        # si hay un solo punto y parece decimal -> 12.5
        # si no -> miles -> 1.234
        partes = s.split(".")
        if len(partes) == 2 and len(partes[1]) <= 2:
            pass
        else:
            s = s.replace(".", "")

    try:
        return float(s)
    except (TypeError, ValueError):
        return 0.0


# =========================================================
# UTILIDADES FINANCIERAS
# =========================================================

def rentabilidad_mensual_equivalente(rentabilidad_anual):
    """
    Convierte rentabilidad anual efectiva a rentabilidad mensual equivalente.
    Ejemplo: 0.07 -> ~0.005654...
    """
    try:
        rentabilidad_anual = float(rentabilidad_anual)
        return (1 + rentabilidad_anual) ** (1 / 12) - 1
    except (TypeError, ValueError):
        return 0.0


def inflacion_mensual_equivalente(inflacion_anual):
    """
    Convierte inflación anual efectiva a inflación mensual equivalente.
    """
    try:
        inflacion_anual = float(inflacion_anual)
        return (1 + inflacion_anual) ** (1 / 12) - 1
    except (TypeError, ValueError):
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
    Devuelve evolución año a año.

    Output:
    [
        {
            "año": 1,
            "total": ...,
            "aportado": ...,
            "ganado": ...,
            "real": ...
        },
        ...
    ]
    """
    capital_inicial = max(parse_number(capital_inicial), 0)
    aportacion_mensual = max(parse_number(aportacion_mensual), 0)
    años = max(int(parse_number(años)), 0)
    rentabilidad_anual = float(rentabilidad_anual or 0)
    inflacion = float(inflacion or 0)
    comision = max(float(comision or 0), 0)

    meses = años * 12
    r_mensual = rentabilidad_mensual_equivalente(rentabilidad_anual)
    inflacion_mensual = inflacion_mensual_equivalente(inflacion)

    capital = capital_inicial
    total_aportado = capital_inicial
    evolucion = []

    for mes in range(1, meses + 1):
        capital *= (1 + r_mensual)
        capital += aportacion_mensual
        total_aportado += aportacion_mensual

        # comisión anual prorrateada mensualmente
        capital *= (1 - comision / 12)

        if mes % 12 == 0:
            factor_inflacion = (1 + inflacion_mensual) ** mes if inflacion_mensual > -1 else 1
            valor_real = capital / factor_inflacion if factor_inflacion != 0 else capital

            evolucion.append({
                "año": mes // 12,
                "total": capital,
                "aportado": total_aportado,
                "ganado": capital - total_aportado,
                "real": valor_real
            })

    return evolucion


# =========================================================
# FIRE
# =========================================================

def calcular_fire(gastos_mensuales, tasa_retiro=0.04):
    """
    Capital necesario para FIRE.
    Fórmula:
        gastos_anuales / tasa_retiro
    """
    gastos_mensuales = max(parse_number(gastos_mensuales), 0)
    tasa_retiro = float(tasa_retiro or 0)

    if tasa_retiro <= 0:
        return 0.0

    gastos_anuales = gastos_mensuales * 12
    return gastos_anuales / tasa_retiro


def años_para_fire(capital_actual, aportacion_mensual, rentabilidad_anual, objetivo, max_años=100):
    """
    Calcula años necesarios para alcanzar FIRE.

    Usa capitalización mensual equivalente a partir de la rentabilidad anual.
    Devuelve float en años.
    Si no es alcanzable dentro de max_años, devuelve math.inf.
    """
    capital_actual = max(parse_number(capital_actual), 0)
    aportacion_mensual = max(parse_number(aportacion_mensual), 0)
    objetivo = max(parse_number(objetivo), 0)
    rentabilidad_anual = float(rentabilidad_anual or 0)

    if objetivo <= 0:
        return 0.0

    if capital_actual >= objetivo:
        return 0.0

    r_mensual = rentabilidad_mensual_equivalente(rentabilidad_anual)
    meses_max = int(max_años * 12)

    capital = capital_actual

    for mes in range(1, meses_max + 1):
        capital *= (1 + r_mensual)
        capital += aportacion_mensual

        if capital >= objetivo:
            return mes / 12

    return math.inf


def capital_en_n_años(capital_actual, aportacion_mensual, rentabilidad_anual, años):
    """
    Calcula el capital estimado tras N años.
    Útil para comparativas FIRE.
    """
    capital_actual = max(parse_number(capital_actual), 0)
    aportacion_mensual = max(parse_number(aportacion_mensual), 0)
    años = max(parse_number(años), 0)
    rentabilidad_anual = float(rentabilidad_anual or 0)

    r_mensual = rentabilidad_mensual_equivalente(rentabilidad_anual)
    meses = int(round(años * 12))

    capital = capital_actual
    for _ in range(meses):
        capital *= (1 + r_mensual)
        capital += aportacion_mensual

    return capital


def generar_curva_fire(capital_actual, aportacion_mensual, rentabilidad_anual, objetivo, max_años=100):
    """
    Genera datos para gráfica FIRE.
    Devuelve:
    years, capitales

    Si no alcanza el objetivo, devuelve igualmente la curva hasta max_años.
    """
    capital_actual = max(parse_number(capital_actual), 0)
    aportacion_mensual = max(parse_number(aportacion_mensual), 0)
    objetivo = max(parse_number(objetivo), 0)
    rentabilidad_anual = float(rentabilidad_anual or 0)

    r_mensual = rentabilidad_mensual_equivalente(rentabilidad_anual)
    capital = capital_actual

    years = [0]
    capitales = [capital_actual]

    for año in range(1, max_años + 1):
        for _ in range(12):
            capital *= (1 + r_mensual)
            capital += aportacion_mensual

        years.append(año)
        capitales.append(capital)

        if objetivo > 0 and capital >= objetivo:
            break

    return years, capitales


# =========================================================
# HIPOTECA
# =========================================================

def calcular_hipoteca(capital, interes_anual, años):
    """
    Cuota mensual hipotecaria.

    interes_anual debe venir en decimal:
    0.03 = 3%
    """
    capital = max(parse_number(capital), 0)
    interes_anual = float(interes_anual or 0)
    años = max(parse_number(años), 0)

    meses = int(años * 12)

    if meses <= 0:
        return 0.0

    interes_mensual = interes_anual / 12

    if interes_mensual == 0:
        return capital / meses

    cuota = capital * (
        interes_mensual * (1 + interes_mensual) ** meses
    ) / (
        (1 + interes_mensual) ** meses - 1
    )

    return cuota


def cuadro_amortizacion(capital, interes_anual, años):
    """
    Devuelve tabla de amortización mensual.
    """
    capital = max(parse_number(capital), 0)
    interes_anual = float(interes_anual or 0)
    años = max(parse_number(años), 0)

    cuota = calcular_hipoteca(capital, interes_anual, años)
    saldo = capital
    interes_mensual = interes_anual / 12

    tabla = []

    for mes in range(1, int(años * 12) + 1):
        interes = saldo * interes_mensual
        amortizacion = cuota - interes
        saldo -= amortizacion

        # blindaje por redondeos al final
        if saldo < 0:
            amortizacion += saldo
            saldo = 0

        tabla.append({
            "mes": mes,
            "cuota": cuota,
            "interes": interes,
            "amortizacion": amortizacion,
            "saldo": saldo
        })

    return tabla
