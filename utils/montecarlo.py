import numpy as np


def first_year_reaching_target(series, target):
    if target is None or target <= 0:
        return None
    for i, value in enumerate(series):
        if value >= target:
            return i
    return None


def montecarlo_interes_compuesto(
    capital_inicial,
    aportacion_mensual,
    anios,
    rentabilidad_media_anual,
    volatilidad_anual,
    inflacion_anual,
    comision_anual,
    n_simulaciones=2000,
    seed=42,
):
    meses = int(anios * 12)
    if meses <= 0:
        return None

    rng = np.random.default_rng(seed)

    rent_m = (1 + rentabilidad_media_anual) ** (1 / 12) - 1
    vol_m = volatilidad_anual / np.sqrt(12)
    infl_m = (1 + inflacion_anual) ** (1 / 12) - 1 if inflacion_anual > -1 else 0
    fee_m = comision_anual / 12

    returns = rng.normal(loc=rent_m, scale=vol_m, size=(n_simulaciones, meses))

    capital = np.zeros((n_simulaciones, meses + 1))
    capital[:, 0] = capital_inicial

    for m in range(1, meses + 1):
        capital[:, m] = capital[:, m - 1] * (1 + returns[:, m - 1])
        capital[:, m] += aportacion_mensual
        capital[:, m] *= (1 - fee_m)
        capital[:, m] = np.clip(capital[:, m], 0, None)

    year_points = [0] + [12 * i for i in range(1, anios + 1)]
    yearly = capital[:, year_points]

    real = np.zeros_like(yearly)
    for i, year in enumerate(range(0, anios + 1)):
        factor = (1 + infl_m) ** (year * 12) if infl_m > -1 else 1
        real[:, i] = yearly[:, i] / factor if factor != 0 else yearly[:, i]

    return {
        "years": list(range(0, anios + 1)),
        "paths": yearly,
        "real_paths": real,
        "final_values": yearly[:, -1],
        "real_final_values": real[:, -1],
        "p10": np.percentile(yearly, 10, axis=0),
        "p50": np.percentile(yearly, 50, axis=0),
        "p90": np.percentile(yearly, 90, axis=0),
        "real_p50": np.percentile(real, 50, axis=0),
    }
