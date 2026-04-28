# utils/impuestos.py

# ============================================
# TABLA DE IMPUESTOS
# ============================================

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


# ============================================
# FUNCIÓN PRINCIPAL
# ============================================

def calcular_gastos_compra(precio, pais, ubicacion, tipo_vivienda="segunda_mano"):
    """
    Calcula impuestos y gastos de compra según país y región.

    Parámetros:
    - precio: precio del inmueble
    - pais: "España" o "México"
    - ubicacion: comunidad autónoma o estado
    - tipo_vivienda: "segunda_mano" o "obra_nueva" (solo España)

    Devuelve:
    dict con impuesto, notaria y total
    """

    pais_data = TAXES_BY_LOCATION.get(pais)

    if not pais_data:
        # fallback
        return {
            "impuesto": 0,
            "notaria": precio * 0.01,
            "total": precio * 0.01,
        }

    datos = pais_data.get(ubicacion)

    if not datos:
        # fallback por país
        if pais == "España":
            datos = pais_data["Madrid"]
        elif pais == "México":
            datos = pais_data["Estimación nacional"]

    # =========================
    # ESPAÑA
    # =========================
    if pais == "España":
        if tipo_vivienda == "segunda_mano":
            impuesto = precio * (datos["itp"] / 100)
        else:
            iva = precio * 0.10
            ajd = precio * (datos["ajd"] / 100)
            impuesto = iva + ajd

        notaria_registro = precio * (datos["notaria_registro"] / 100)

    # =========================
    # MÉXICO
    # =========================
    elif pais == "México":
        impuesto = precio * (datos["isai"] / 100)
        notaria_registro = precio * (datos["notaria_registro"] / 100)

    else:
        impuesto = 0
        notaria_registro = precio * 0.01

    total = impuesto + notaria_registro

    return {
        "impuesto": impuesto,
        "notaria": notaria_registro,
        "total": total,
    }


# ============================================
# HELPERS (opcionales para UI)
# ============================================

def get_paises():
    return list(TAXES_BY_LOCATION.keys())


def get_ubicaciones(pais):
    return list(TAXES_BY_LOCATION.get(pais, {}).keys())
