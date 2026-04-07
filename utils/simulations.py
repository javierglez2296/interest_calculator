from datetime import datetime
import uuid


SIMULATION_KEYS = [
    "interes_compuesto",
    "fire",
    "hipoteca",
    "rentabilidad_alquiler",
    "comparador",
]


def empty_simulations_store():
    return {key: [] for key in SIMULATION_KEYS}


def normalize_store(store):
    if not isinstance(store, dict):
        return empty_simulations_store()

    normalized = empty_simulations_store()
    for key in SIMULATION_KEYS:
        value = store.get(key, [])
        normalized[key] = value if isinstance(value, list) else []
    return normalized


def build_simulation(nombre, data):
    return {
        "id": str(uuid.uuid4()),
        "nombre": nombre.strip() if nombre else "Simulación sin nombre",
        "created_at": datetime.utcnow().isoformat(),
        "data": data,
    }


def add_simulation(store, calculator_key, nombre, data):
    store = normalize_store(store)
    simulation = build_simulation(nombre, data)
    store[calculator_key] = [simulation] + store[calculator_key]
    return store
