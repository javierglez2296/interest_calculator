from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any


SIMULATION_KEYS = [
    "interes_compuesto",
    "fire",
    "hipoteca",
    "rentabilidad_alquiler",
    "comparador",
]


def empty_simulations_store() -> dict[str, list[dict[str, Any]]]:
    """
    Crea la estructura base del store de simulaciones.
    """
    return {key: [] for key in SIMULATION_KEYS}


def normalize_store(store: Any) -> dict[str, list[dict[str, Any]]]:
    """
    Normaliza el store para asegurar que siempre tenga
    la estructura esperada.

    Si el store viene vacío, corrupto o incompleto,
    devuelve una versión válida.
    """
    if not isinstance(store, dict):
        return empty_simulations_store()

    normalized = empty_simulations_store()

    for key in SIMULATION_KEYS:
        value = store.get(key, [])
        normalized[key] = value if isinstance(value, list) else []

    return normalized


def _clean_name(nombre: Any, calculator_key: str) -> str:
    """
    Limpia el nombre de la simulación y genera uno por defecto si falta.
    """
    if isinstance(nombre, str):
        nombre = nombre.strip()
        if nombre:
            return nombre

    default_names = {
        "interes_compuesto": "Simulación interés compuesto",
        "fire": "Simulación FIRE",
        "hipoteca": "Simulación hipoteca",
        "rentabilidad_alquiler": "Simulación rentabilidad alquiler",
        "comparador": "Simulación comparador",
    }
    return default_names.get(calculator_key, "Simulación")


def _build_simulation(nombre: str, data: dict[str, Any]) -> dict[str, Any]:
    """
    Construye el objeto estándar de simulación.
    """
    return {
        "id": str(uuid.uuid4()),
        "nombre": nombre,
        "data": data if isinstance(data, dict) else {},
        "created_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }


def add_simulation(
    store: Any,
    calculator_key: str,
    nombre: Any,
    data: dict[str, Any],
    max_items_per_calculator: int = 20,
) -> dict[str, list[dict[str, Any]]]:
    """
    Añade una simulación al store.

    - Normaliza el store
    - Valida la key
    - Genera id único
    - Limita el número máximo de simulaciones por calculadora
      conservando las más recientes
    """
    normalized = normalize_store(store)

    if calculator_key not in SIMULATION_KEYS:
        return normalized

    clean_name = _clean_name(nombre, calculator_key)
    simulation = _build_simulation(clean_name, data)

    items = normalized[calculator_key][:]
    items.insert(0, simulation)

    if max_items_per_calculator > 0:
        items = items[:max_items_per_calculator]

    normalized[calculator_key] = items
    return normalized


def delete_simulation(
    store: Any,
    calculator_key: str,
    simulation_id: Any,
) -> dict[str, list[dict[str, Any]]]:
    """
    Elimina una simulación por id dentro de una calculadora concreta.
    """
    normalized = normalize_store(store)

    if calculator_key not in SIMULATION_KEYS:
        return normalized

    simulation_id = str(simulation_id)
    normalized[calculator_key] = [
        item
        for item in normalized[calculator_key]
        if str(item.get("id")) != simulation_id
    ]
    return normalized


def get_simulations(
    store: Any,
    calculator_key: str,
) -> list[dict[str, Any]]:
    """
    Devuelve la lista de simulaciones de una calculadora.
    """
    normalized = normalize_store(store)

    if calculator_key not in SIMULATION_KEYS:
        return []

    return normalized.get(calculator_key, [])


def get_simulation_by_id(
    store: Any,
    calculator_key: str,
    simulation_id: Any,
) -> dict[str, Any] | None:
    """
    Busca una simulación concreta por id.
    """
    normalized = normalize_store(store)

    if calculator_key not in SIMULATION_KEYS:
        return None

    simulation_id = str(simulation_id)

    for item in normalized[calculator_key]:
        if str(item.get("id")) == simulation_id:
            return item

    return None


def rename_simulation(
    store: Any,
    calculator_key: str,
    simulation_id: Any,
    nuevo_nombre: Any,
) -> dict[str, list[dict[str, Any]]]:
    """
    Renombra una simulación existente.
    """
    normalized = normalize_store(store)

    if calculator_key not in SIMULATION_KEYS:
        return normalized

    simulation_id = str(simulation_id)
    clean_name = _clean_name(nuevo_nombre, calculator_key)

    updated_items = []
    for item in normalized[calculator_key]:
        if str(item.get("id")) == simulation_id:
            updated_item = dict(item)
            updated_item["nombre"] = clean_name
            updated_items.append(updated_item)
        else:
            updated_items.append(item)

    normalized[calculator_key] = updated_items
    return normalized


def update_simulation_data(
    store: Any,
    calculator_key: str,
    simulation_id: Any,
    new_data: dict[str, Any],
) -> dict[str, list[dict[str, Any]]]:
    """
    Actualiza el bloque data de una simulación.
    """
    normalized = normalize_store(store)

    if calculator_key not in SIMULATION_KEYS:
        return normalized

    simulation_id = str(simulation_id)

    updated_items = []
    for item in normalized[calculator_key]:
        if str(item.get("id")) == simulation_id:
            updated_item = dict(item)
            updated_item["data"] = new_data if isinstance(new_data, dict) else {}
            updated_items.append(updated_item)
        else:
            updated_items.append(item)

    normalized[calculator_key] = updated_items
    return normalized
