from datetime import datetime
import uuid
from copy import deepcopy


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
        "favorite": False,
        "data": data,
    }


# =========================
# CRUD
# =========================

def add_simulation(store, calculator_key, nombre, data):
    store = normalize_store(store)
    simulation = build_simulation(nombre, data)
    store[calculator_key] = [simulation] + store[calculator_key]
    return store


def delete_simulation(store, calculator_key, simulation_id):
    store = normalize_store(store)

    store[calculator_key] = [
        sim for sim in store[calculator_key]
        if sim.get("id") != simulation_id
    ]

    return store


def duplicate_simulation(store, calculator_key, simulation_id):
    store = normalize_store(store)

    for sim in store[calculator_key]:
        if sim["id"] == simulation_id:
            new_sim = deepcopy(sim)
            new_sim["id"] = str(uuid.uuid4())
            new_sim["nombre"] = sim["nombre"] + " (copia)"
            new_sim["created_at"] = datetime.utcnow().isoformat()

            store[calculator_key] = [new_sim] + store[calculator_key]
            break

    return store


def rename_simulation(store, calculator_key, simulation_id, new_name):
    store = normalize_store(store)

    for sim in store[calculator_key]:
        if sim["id"] == simulation_id:
            sim["nombre"] = new_name.strip() or sim["nombre"]

    return store


def toggle_favorite(store, calculator_key, simulation_id):
    store = normalize_store(store)

    for sim in store[calculator_key]:
        if sim["id"] == simulation_id:
            sim["favorite"] = not sim.get("favorite", False)

    return store


def get_simulations(store, calculator_key):
    store = normalize_store(store)

    sims = store.get(calculator_key, [])

    # favoritos arriba
    sims_sorted = sorted(
        sims,
        key=lambda x: (not x.get("favorite", False), x.get("created_at", "")),
        reverse=False,
    )

    return sims_sorted
