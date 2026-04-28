TAXES_BY_LOCATION = {
    "España": {
        "Andalucía": {"itp": 7.0, "ajd": 1.2, "notaria_registro": 1.0},
        "Aragón": {"itp": 8.0, "ajd": 1.5, "notaria_registro": 1.0},
        "Asturias": {"itp": 8.0, "ajd": 1.2, "notaria_registro": 1.0},
        "Baleares": {"itp": 8.0, "ajd": 1.2, "notaria_registro": 1.0},
        "Canarias": {"itp": 6.5, "ajd": 1.0, "notaria_registro": 1.0},
        "Cantabria": {"itp": 9.0, "ajd": 1.5, "notaria_registro": 1.0},
        "Castilla-La Mancha": {"itp": 9.0, "ajd": 1.5, "notaria_registro": 1.0},
        "Castilla y León": {"itp": 8.0, "ajd": 1.5, "notaria_registro": 1.0},
        "Cataluña": {"itp": 10.0, "ajd": 1.5, "notaria_registro": 1.0},
        "Comunidad Valenciana": {"itp": 10.0, "ajd": 1.5, "notaria_registro": 1.0},
        "Extremadura": {"itp": 8.0, "ajd": 1.5, "notaria_registro": 1.0},
        "Galicia": {"itp": 10.0, "ajd": 1.5, "notaria_registro": 1.0},
        "Madrid": {"itp": 6.0, "ajd": 0.75, "notaria_registro": 1.0},
        "Murcia": {"itp": 8.0, "ajd": 1.5, "notaria_registro": 1.0},
        "Navarra": {"itp": 6.0, "ajd": 0.5, "notaria_registro": 1.0},
        "País Vasco": {"itp": 7.0, "ajd": 0.5, "notaria_registro": 1.0},
        "La Rioja": {"itp": 7.0, "ajd": 1.0, "notaria_registro": 1.0},
        "Ceuta": {"itp": 6.0, "ajd": 0.5, "notaria_registro": 1.0},
        "Melilla": {"itp": 6.0, "ajd": 0.5, "notaria_registro": 1.0},
    },
    "México": {
        "Estimación nacional": {"isai": 3.0, "notaria_registro": 4.0},
        "Ciudad de México": {"isai": 4.5, "notaria_registro": 3.0},
        "Estado de México": {"isai": 2.0, "notaria_registro": 3.0},
        "Jalisco": {"isai": 3.0, "notaria_registro": 3.5},
        "Nuevo León": {"isai": 3.0, "notaria_registro": 3.5},
        "Quintana Roo": {"isai": 3.0, "notaria_registro": 4.0},
    },
}


IRPF_AHORRO_ES = [
    (6000, 0.19),
    (50000, 0.21),
    (200000, 0.23),
    (300000, 0.27),
    (float("inf"), 0.28),
]


def get_paises():
    return list(TAXES_BY_LOCATION.keys())


def get_ubicaciones(pais):
    return list(TAXES_BY_LOCATION.get(pais, {}).keys())


def calcular_gastos_compra(precio, pais, ubicacion, tipo_vivienda="segunda_mano"):
    precio = float(precio or 0)
    pais = pais or "España"
    ubicacion = ubicacion or "Madrid"

    datos = TAXES_BY_LOCATION.get(pais, {}).get(ubicacion)

    if not datos:
        if pais == "México":
            datos = TAXES_BY_LOCATION["México"]["Estimación nacional"]
        else:
            datos = TAXES_BY_LOCATION["España"]["Madrid"]

    if pais == "España":
        if tipo_vivienda == "obra_nueva":
            impuesto = precio * 0.10 + precio * datos["ajd"] / 100
            impuesto_nombre = "IVA + AJD"
        else:
            impuesto = precio * datos["itp"] / 100
            impuesto_nombre = "ITP"

        notaria = precio * datos["notaria_registro"] / 100

    elif pais == "México":
        impuesto = precio * datos["isai"] / 100
        impuesto_nombre = "ISAI"
        notaria = precio * datos["notaria_registro"] / 100

    else:
        impuesto = 0
        impuesto_nombre = "Impuesto estimado"
        notaria = precio * 0.01

    return {
        "impuesto_nombre": impuesto_nombre,
        "impuesto": impuesto,
        "notaria": notaria,
        "total": impuesto + notaria,
    }


def calcular_irpf_tramos_ahorro_es(ganancia):
    restante = max(float(ganancia or 0), 0)
    impuesto = 0
    anterior = 0

    for limite, tipo in IRPF_AHORRO_ES:
        tramo = min(restante, limite - anterior)
        if tramo <= 0:
            break
        impuesto += tramo * tipo
        restante -= tramo
        anterior = limite

    return impuesto


def calcular_fiscalidad_alquiler_es(
    ingresos_anuales,
    gastos_deducibles,
    intereses_hipoteca=0,
    reduccion_alquiler_pct=50,
    tipo_marginal_irpf_pct=24,
):
    beneficio_bruto = ingresos_anuales - gastos_deducibles - intereses_hipoteca
    base_irpf = max(beneficio_bruto, 0) * (1 - reduccion_alquiler_pct / 100)
    irpf = base_irpf * tipo_marginal_irpf_pct / 100
    beneficio_neto = beneficio_bruto - irpf

    return {
        "beneficio_bruto": beneficio_bruto,
        "base_irpf": base_irpf,
        "irpf": irpf,
        "beneficio_neto": beneficio_neto,
    }


def calcular_fiscalidad_venta_es(
    precio_compra,
    gastos_compra,
    reforma,
    precio_venta,
    gastos_venta=0,
):
    valor_adquisicion = precio_compra + gastos_compra + reforma
    valor_transmision = precio_venta - gastos_venta
    ganancia = valor_transmision - valor_adquisicion
    irpf_venta = calcular_irpf_tramos_ahorro_es(ganancia)

    return {
        "valor_adquisicion": valor_adquisicion,
        "valor_transmision": valor_transmision,
        "ganancia": ganancia,
        "irpf_venta": irpf_venta,
        "neto_venta": precio_venta - gastos_venta - irpf_venta,
    }


def calcular_motor_fiscal_pro(
    precio_compra,
    pais,
    ubicacion,
    tipo_vivienda,
    alquiler_mensual,
    ocupacion_pct,
    gastos_anuales,
    intereses_hipoteca_anuales=0,
    reforma=0,
    precio_venta_estimado=None,
    gastos_venta_pct=3,
    reduccion_alquiler_pct=50,
    tipo_marginal_irpf_pct=24,
):
    compra = calcular_gastos_compra(
        precio=precio_compra,
        pais=pais,
        ubicacion=ubicacion,
        tipo_vivienda=tipo_vivienda,
    )

    ingresos_anuales = alquiler_mensual * 12 * ocupacion_pct / 100

    if pais == "España":
        alquiler = calcular_fiscalidad_alquiler_es(
            ingresos_anuales=ingresos_anuales,
            gastos_deducibles=gastos_anuales,
            intereses_hipoteca=intereses_hipoteca_anuales,
            reduccion_alquiler_pct=reduccion_alquiler_pct,
            tipo_marginal_irpf_pct=tipo_marginal_irpf_pct,
        )
    else:
        beneficio_bruto = ingresos_anuales - gastos_anuales - intereses_hipoteca_anuales
        alquiler = {
            "beneficio_bruto": beneficio_bruto,
            "base_irpf": beneficio_bruto,
            "irpf": 0,
            "beneficio_neto": beneficio_bruto,
        }

    venta = None
    if precio_venta_estimado and pais == "España":
        venta = calcular_fiscalidad_venta_es(
            precio_compra=precio_compra,
            gastos_compra=compra["total"],
            reforma=reforma,
            precio_venta=precio_venta_estimado,
            gastos_venta=precio_venta_estimado * gastos_venta_pct / 100,
        )

    inversion_total = precio_compra + compra["total"] + reforma

    return {
        "compra": compra,
        "alquiler": alquiler,
        "venta": venta,
        "inversion_total": inversion_total,
        "ingresos_anuales": ingresos_anuales,
        "rentabilidad_neta_fiscal": alquiler["beneficio_neto"] / inversion_total * 100 if inversion_total > 0 else 0,
    }
