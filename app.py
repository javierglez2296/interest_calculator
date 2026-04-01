import io
from datetime import datetime

import pandas as pd
from dash import Dash, dcc, html, Input, Output, State, dash_table, callback_context, clientside_callback
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# =========================================================
# CONFIG GENERAL
# =========================================================
MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"
HIPOTECA_LEAD_URL = "#"  # Sustituye esto por tu partner hipotecario cuando lo tengas

# =========================================================
# APP
# =========================================================
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.LUX],
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        {
            "name": "description",
            "content": "Calculadora de interés compuesto gratis, calculadora FIRE y calculadora de hipoteca. Simula inversión, libertad financiera y cuota hipotecaria."
        },
        {"name": "robots", "content": "index, follow"},
        {"name": "theme-color", "content": "#2563eb"},
        {"property": "og:type", "content": "website"},
        {"property": "og:title", "content": "Calculadora de interés compuesto, FIRE e hipoteca"},
        {
            "property": "og:description",
            "content": "Simula cuánto podría crecer tu inversión, cuándo podrías alcanzar FIRE y cuánto pagarías de hipoteca."
        },
        {"property": "og:locale", "content": "es_ES"},
        {"name": "twitter:card", "content": "summary_large_image"},
        {"name": "twitter:title", "content": "Calculadora de interés compuesto, FIRE e hipoteca"},
        {
            "name": "twitter:description",
            "content": "Calcula tu patrimonio futuro, tu objetivo FIRE y tu hipoteca."
        }
    ]
)

server = app.server
app.title = "Calculadora de interés compuesto, FIRE e hipoteca"

app.index_string = """
<!DOCTYPE html>
<html lang="es">
    <head>
        {%metas%}

        <meta name="google-site-verification" content="T-JtHON5w3hyTmxz5G0_uuQmrESyzYM0H3Io-KORWAQ" />
        <title>{%title%}</title>
        <meta name="impact-site-verification" content="2d5539a7-7c67-4e61-8a9d-b7c396a48dc9" />

        <!-- Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-VJS7ZLKTBX"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', 'G-VJS7ZLKTBX', {
            'anonymize_ip': true
          });
        </script>

        <meta name="description" content="Calculadora de interés compuesto gratis, calculadora FIRE y calculadora de hipoteca.">
        <meta name="robots" content="index, follow">
        <meta name="theme-color" content="#2563eb">

        <meta property="og:type" content="website">
        <meta property="og:title" content="Calculadora de interés compuesto, FIRE e hipoteca">
        <meta property="og:description" content="Simula inversión, libertad financiera FIRE y cuota hipotecaria en una sola web.">
        <meta property="og:locale" content="es_ES">

        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:title" content="Calculadora de interés compuesto, FIRE e hipoteca">
        <meta name="twitter:description" content="Calcula tu inversión, tu objetivo FIRE y tu hipoteca.">

        {%favicon%}
        {%css%}

        <style>
            html {
                scroll-behavior: smooth;
            }

            @keyframes resultadoGlow {
                0% {
                    box-shadow: 0 0 0 rgba(37, 99, 235, 0.00);
                    transform: translateY(0);
                }
                30% {
                    box-shadow: 0 0 0 6px rgba(37, 99, 235, 0.10);
                    transform: translateY(-2px);
                }
                100% {
                    box-shadow: 0 0 0 rgba(37, 99, 235, 0.00);
                    transform: translateY(0);
                }
            }

            .resultado-highlight {
                animation: resultadoGlow 1.2s ease;
            }

            .article-content h1,
            .article-content h2,
            .article-content h3,
            .article-content h4 {
                color: #0f172a;
                font-weight: 800;
            }

            .article-content p,
            .article-content li {
                color: #334155;
                font-size: 1.02rem;
                line-height: 1.8;
            }

            .article-content ul {
                padding-left: 22px;
            }

            .article-content a {
                text-decoration: none;
            }

            .custom-tab {
                font-weight: 700 !important;
                font-size: 0.98rem !important;
                padding: 14px 16px !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

# =========================================================
# ESTILO
# =========================================================
BRAND_NAME = "Calculadoras financieras"

COLOR_BG = "#f5f7fb"
COLOR_CARD = "#ffffff"
COLOR_TEXT = "#0f172a"
COLOR_MUTED = "#64748b"
COLOR_BORDER = "#e2e8f0"

COLOR_PRIMARY = "#2563eb"
COLOR_PRIMARY_SOFT = "#eff6ff"
COLOR_SUCCESS = "#16a34a"
COLOR_SUCCESS_SOFT = "#f0fdf4"
COLOR_WARNING = "#d97706"
COLOR_WARNING_SOFT = "#fff7ed"
COLOR_DANGER = "#dc2626"
COLOR_DANGER_SOFT = "#fef2f2"
COLOR_DARK = "#0f172a"
COLOR_CAPITAL = "#94a3b8"
COLOR_REAL = "#0f766e"

CARD_STYLE = {
    "borderRadius": "20px",
    "boxShadow": "0 12px 30px rgba(15, 23, 42, 0.06)",
    "border": f"1px solid {COLOR_BORDER}",
    "backgroundColor": COLOR_CARD
}

SECTION_TITLE_STYLE = {
    "fontWeight": "800",
    "fontSize": "1.15rem",
    "marginBottom": "14px",
    "color": COLOR_TEXT
}

LABEL_STYLE = {
    "fontWeight": "700",
    "marginBottom": "6px",
    "display": "block",
    "color": COLOR_TEXT
}

INPUT_STYLE = {
    "fontSize": "16px"
}

# =========================================================
# ARTÍCULOS
# =========================================================
ARTICLES = {
    "/que-es-el-interes-compuesto": {
        "title": "Qué es el interés compuesto y por qué puede cambiar tu patrimonio a largo plazo",
        "description": "Descubre qué es el interés compuesto, cómo funciona y por qué es una de las claves para hacer crecer tu dinero a largo plazo.",
        "badge": "Guía de inversión",
        "content": [
            ("p", "El interés compuesto es uno de los conceptos más importantes para cualquier persona que quiera ahorrar e invertir mejor. Su idea es simple, pero su impacto a largo plazo puede ser enorme."),
            ("h2", "Cómo funciona el interés compuesto"),
            ("p", "No solo ganas rentabilidad sobre el dinero que aportas, sino también sobre los beneficios acumulados de años anteriores."),
            ("p", "Con el tiempo, el crecimiento se acelera porque el capital sobre el que genera rendimientos cada vez es mayor."),
            ("h2", "Conclusión"),
            ("p", "El interés compuesto no hace magia, pero el efecto del tiempo puede ser enorme si mantienes la constancia.")
        ]
    },
    "/cuanto-dinero-puedes-tener-invirtiendo-200-euros-al-mes": {
        "title": "Cuánto dinero puedes tener invirtiendo 200 euros al mes",
        "description": "Una simulación sencilla para entender cuánto patrimonio podrías acumular invirtiendo 200 euros al mes durante años.",
        "badge": "Simulación práctica",
        "content": [
            ("p", "Invertir 200 euros al mes puede parecer poco al principio, pero a largo plazo puede dar lugar a un patrimonio interesante."),
            ("h2", "La clave está en el tiempo"),
            ("p", "Lo importante no es solo la cantidad, sino cuántos años mantienes la estrategia y si reinviertes los rendimientos."),
            ("h2", "Conclusión"),
            ("p", "Una aportación periódica asequible puede ser suficiente para empezar a construir patrimonio.")
        ]
    },
    "/cuando-se-nota-de-verdad-el-interes-compuesto": {
        "title": "Cuándo se nota de verdad el interés compuesto",
        "description": "El interés compuesto parece lento al principio, pero con el tiempo se acelera. Descubre cuándo suele empezar a notarse de verdad.",
        "badge": "Concepto clave",
        "content": [
            ("p", "Al principio parece que avanza despacio porque la base invertida todavía es pequeña."),
            ("h2", "El punto de inflexión"),
            ("p", "Con los años, los rendimientos empiezan a pesar más que tus nuevas aportaciones y ahí es cuando se nota de verdad."),
            ("h2", "Conclusión"),
            ("p", "La mayoría abandona antes de ver el tramo más potente del interés compuesto.")
        ]
    },
    "/que-es-fire-y-cuanto-necesitas": {
        "title": "Qué es FIRE y cuánto dinero necesitas para alcanzar la libertad financiera",
        "description": "Descubre qué significa FIRE, cómo calcular tu número FIRE y qué capital podrías necesitar para vivir de tus inversiones.",
        "badge": "FIRE",
        "content": [
            ("p", "FIRE significa Financial Independence, Retire Early. El objetivo es acumular un patrimonio suficiente para que tus inversiones cubran tus gastos."),
            ("h2", "Cómo calcular tu número FIRE"),
            ("p", "Una forma conocida es dividir tus gastos anuales entre tu tasa de retirada segura, por ejemplo el 4 %."),
            ("p", "Si necesitas 24.000 € al año y usas una tasa del 4 %, necesitarías aproximadamente 600.000 €."),
            ("h2", "Conclusión"),
            ("p", "FIRE no va solo de dejar de trabajar antes, sino de tener más libertad financiera.")
        ]
    },
    "/regla-del-4-por-ciento": {
        "title": "La regla del 4 %: qué es, cómo funciona y cuándo usarla con prudencia",
        "description": "La regla del 4 % es una referencia clásica para estimar cuánto patrimonio puedes necesitar para vivir de tus inversiones.",
        "badge": "FIRE",
        "content": [
            ("p", "La regla del 4 % es una aproximación usada para estimar cuánto patrimonio podrías necesitar para retirarte."),
            ("h2", "Ejemplo sencillo"),
            ("p", "Si quieres 20.000 € al año, necesitarías en torno a 500.000 € con esa referencia."),
            ("h2", "Usarla con prudencia"),
            ("p", "Conviene probar varios escenarios, como 3,5 %, 4 % y 4,5 %, para no depender de una única hipótesis."),
            ("h2", "Conclusión"),
            ("p", "Es una guía útil, no una garantía.")
        ]
    },
    "/como-calcular-tu-hipoteca": {
        "title": "Cómo calcular tu hipoteca paso a paso antes de comprar vivienda",
        "description": "Aprende a calcular la cuota hipotecaria, los intereses totales y el esfuerzo mensual antes de comprar una vivienda.",
        "badge": "Hipoteca",
        "content": [
            ("p", "Antes de comprar vivienda conviene calcular bien la hipoteca, no solo el precio del inmueble."),
            ("h2", "Qué debes mirar"),
            ("ul", [
                "Importe financiado",
                "Cuota mensual",
                "Intereses totales",
                "Ahorro inicial necesario"
            ]),
            ("h2", "Conclusión"),
            ("p", "Una diferencia pequeña en interés o plazo puede cambiar mucho el coste final.")
        ]
    }
}

# =========================================================
# UTILIDADES
# =========================================================
def parse_number(value, default=0.0):
    if value is None:
        return default

    if isinstance(value, (int, float)):
        return float(value)

    s = str(value).strip()
    if s == "":
        return default

    s = s.replace("€", "").replace("%", "").replace(" ", "")

    if "." in s and "," in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "")
            s = s.replace(",", ".")
        else:
            s = s.replace(",", "")
    else:
        if "," in s:
            partes = s.split(",")
            if len(partes) > 1 and len(partes[-1]) in (1, 2):
                s = s.replace(".", "")
                s = s.replace(",", ".")
            else:
                s = s.replace(",", "")
        elif "." in s:
            partes = s.split(".")
            if len(partes) > 1 and all(len(p) == 3 for p in partes[1:]):
                s = s.replace(".", "")
            elif len(partes) == 2 and len(partes[-1]) in (1, 2):
                pass
            else:
                s = s.replace(".", "")

    try:
        return float(s)
    except Exception:
        return default

def safe_float(value, default=0.0):
    return parse_number(value, default)

def safe_int(value, default=0):
    try:
        return int(round(parse_number(value, default)))
    except Exception:
        return default

def formatear_euros_es(valor):
    if valor is None or valor == "":
        return "0,00 €"

    try:
        if isinstance(valor, (int, float)):
            numero = float(valor)
        else:
            s = str(valor).strip()
            if "," in s:
                s = s.replace(".", "").replace(",", ".")
            else:
                if s.count(".") > 0 and len(s.split(".")[-1]) == 3:
                    s = s.replace(".", "")
            numero = float(s)
    except Exception:
        return "0,00 €"

    s = f"{numero:,.2f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{s} €"

def formatear_pct_es(valor):
    return f"{float(valor):,.2f}".replace(".", ",") + " %"

def obtener_periodos_por_ano(frecuencia):
    return 12 if frecuencia == "mensual" else 1

def obtener_nombre_periodo(frecuencia):
    return "Mes" if frecuencia == "mensual" else "Año"

def annual_to_period_rate(annual_rate_decimal, frecuencia):
    if frecuencia == "mensual":
        return (1 + annual_rate_decimal) ** (1 / 12) - 1
    return annual_rate_decimal

def net_annual_growth_rate(tasa_bruta_anual_pct, comision_anual_pct):
    tasa = safe_float(tasa_bruta_anual_pct) / 100
    comision = safe_float(comision_anual_pct) / 100
    return (1 + tasa) * (1 - comision) - 1

def generar_aporte_periodico(periodo_index, deposito_inicial, crecimiento_aportacion_anual_pct, frecuencia):
    crecimiento_anual = safe_float(crecimiento_aportacion_anual_pct) / 100
    if frecuencia == "anual":
        ano = periodo_index - 1
    else:
        ano = (periodo_index - 1) // 12
    return float(deposito_inicial) * ((1 + crecimiento_anual) ** ano)

def calcular_cagr(valor_inicial, valor_final, anos):
    if valor_inicial <= 0 or valor_final <= 0 or anos <= 0:
        return 0.0
    return (valor_final / valor_inicial) ** (1 / anos) - 1

def validar_inputs(monto_inicial, deposito, tasa, anos, inflacion, impuestos, comision, crecimiento_aporte):
    errores = []
    if monto_inicial is None or safe_float(monto_inicial) < 0:
        errores.append("La inversión inicial debe ser 0 o mayor.")
    if deposito is None or safe_float(deposito) < 0:
        errores.append("La aportación periódica debe ser 0 o mayor.")
    if tasa is None or safe_float(tasa) < 0:
        errores.append("La rentabilidad anual debe ser 0 o mayor.")
    if anos is None or safe_int(anos) < 1:
        errores.append("La duración debe ser al menos de 1 año.")
    if inflacion is None or safe_float(inflacion) < 0:
        errores.append("La inflación debe ser 0 o mayor.")
    if impuestos is None or safe_float(impuestos) < 0:
        errores.append("Los impuestos deben ser 0 o mayores.")
    if comision is None or safe_float(comision) < 0:
        errores.append("La comisión debe ser 0 o mayor.")
    if crecimiento_aporte is None:
        errores.append("El crecimiento anual de aportación no puede estar vacío.")
    return errores

# =========================================================
# CÁLCULO INTERÉS COMPUESTO
# =========================================================
def calcular_escenario(
    nombre_escenario,
    monto_inicial,
    deposito_periodico,
    tasa_interes_anual_pct,
    num_anos,
    frecuencia,
    momento_aportacion,
    inflacion_anual_pct,
    impuesto_plusvalias_pct,
    comision_anual_pct,
    crecimiento_aportacion_anual_pct
):
    monto_inicial = safe_float(monto_inicial)
    deposito_periodico = safe_float(deposito_periodico)
    tasa_interes_neta_anual = net_annual_growth_rate(tasa_interes_anual_pct, comision_anual_pct)
    inflacion_anual = safe_float(inflacion_anual_pct) / 100
    impuesto_plusvalias = safe_float(impuesto_plusvalias_pct) / 100
    num_anos = safe_int(num_anos)

    periodos_por_ano = obtener_periodos_por_ano(frecuencia)
    nombre_periodo = obtener_nombre_periodo(frecuencia)
    tasa_por_periodo = annual_to_period_rate(tasa_interes_neta_anual, frecuencia)
    inflacion_por_periodo = annual_to_period_rate(inflacion_anual, frecuencia)
    total_periodos = num_anos * periodos_por_ano

    saldo_bruto = monto_inicial
    depositos_acumulados = 0.0
    rows = []

    for t in range(1, total_periodos + 1):
        aporte_periodo = generar_aporte_periodico(t, deposito_periodico, crecimiento_aportacion_anual_pct, frecuencia)

        if momento_aportacion == "inicio":
            saldo_bruto += aporte_periodo
            depositos_acumulados += aporte_periodo
            saldo_bruto *= (1 + tasa_por_periodo)
        else:
            saldo_bruto *= (1 + tasa_por_periodo)
            saldo_bruto += aporte_periodo
            depositos_acumulados += aporte_periodo

        capital_aportado = monto_inicial + depositos_acumulados
        interes_bruto = saldo_bruto - capital_aportado
        impuestos_teoricos = max(interes_bruto, 0) * impuesto_plusvalias
        interes_neto = interes_bruto - impuestos_teoricos
        valor_total_neto = capital_aportado + interes_neto

        factor_inflacion = (1 + inflacion_por_periodo) ** t
        valor_real_neto = valor_total_neto / factor_inflacion if factor_inflacion > 0 else valor_total_neto

        rows.append({
            "Escenario": nombre_escenario,
            nombre_periodo: t,
            "Etiqueta": f"{nombre_periodo} {t}",
            "Aporte del período": aporte_periodo,
            "Capital aportado": capital_aportado,
            "Interés bruto": interes_bruto,
            "Impuestos teóricos": impuestos_teoricos,
            "Interés neto": interes_neto,
            "Valor total bruto": saldo_bruto,
            "Valor total neto": valor_total_neto,
            "Valor real neto": valor_real_neto
        })

    return pd.DataFrame(rows), nombre_periodo

def preparar_df_plot(df, frecuencia):
    if frecuencia == "mensual" and len(df) > 24:
        df_plot = df[df["Mes"] % 12 == 0].copy()
        df_plot["Etiqueta"] = df_plot["Mes"].apply(lambda x: f"Año {x // 12}")
        return df_plot, "Año"
    return df.copy(), obtener_nombre_periodo(frecuencia)

# =========================================================
# CÁLCULO FIRE
# =========================================================
def calcular_fire(cartera_actual, aportacion_anual, rentabilidad_anual_pct, inflacion_pct, gasto_anual_hoy, tasa_retirada_pct, max_anos=60):
    cartera_actual = safe_float(cartera_actual)
    aportacion_anual = safe_float(aportacion_anual)
    rentabilidad = safe_float(rentabilidad_anual_pct) / 100
    inflacion = safe_float(inflacion_pct) / 100
    gasto_anual_hoy = safe_float(gasto_anual_hoy)
    tasa_retirada = safe_float(tasa_retirada_pct) / 100

    capital = cartera_actual
    rows = []
    objetivo_ano = None

    for ano in range(0, max_anos + 1):
        gasto_nominal = gasto_anual_hoy * ((1 + inflacion) ** ano)
        numero_fire = gasto_nominal / tasa_retirada if tasa_retirada > 0 else 0
        gap = numero_fire - capital

        rows.append({
            "Año": ano,
            "Capital estimado": capital,
            "Gasto anual objetivo": gasto_nominal,
            "Número FIRE": numero_fire,
            "Distancia al objetivo": gap
        })

        if objetivo_ano is None and capital >= numero_fire:
            objetivo_ano = ano

        capital = capital * (1 + rentabilidad) + aportacion_anual

    return pd.DataFrame(rows), objetivo_ano

# =========================================================
# CÁLCULO HIPOTECA
# =========================================================
def calcular_hipoteca(precio_vivienda, entrada, interes_anual_pct, anos, gastos_compra_pct=10):
    precio_vivienda = safe_float(precio_vivienda)
    entrada = safe_float(entrada)
    interes_anual = safe_float(interes_anual_pct) / 100
    anos = safe_int(anos)
    gastos_compra_pct = safe_float(gastos_compra_pct) / 100

    principal = max(precio_vivienda - entrada, 0)
    meses = max(anos * 12, 1)
    tipo_mensual = interes_anual / 12

    if tipo_mensual == 0:
        cuota = principal / meses
    else:
        cuota = principal * (tipo_mensual * (1 + tipo_mensual) ** meses) / (((1 + tipo_mensual) ** meses) - 1)

    total_pagado = cuota * meses
    intereses_totales = total_pagado - principal
    gastos_compra = precio_vivienda * gastos_compra_pct
    ahorro_necesario_inicial = entrada + gastos_compra

    rows = []
    saldo = principal
    for mes in range(1, meses + 1):
        interes_mes = saldo * tipo_mensual
        amortizacion_mes = cuota - interes_mes
        saldo = max(saldo - amortizacion_mes, 0)

        if mes <= 24 or mes % 12 == 0 or mes == meses:
            rows.append({
                "Mes": mes,
                "Cuota": cuota,
                "Interés": interes_mes,
                "Amortización": amortizacion_mes,
                "Saldo pendiente": saldo
            })

    return {
        "principal": principal,
        "cuota": cuota,
        "total_pagado": total_pagado,
        "intereses_totales": intereses_totales,
        "gastos_compra": gastos_compra,
        "ahorro_necesario_inicial": ahorro_necesario_inicial,
        "tabla": pd.DataFrame(rows)
    }

# =========================================================
# FIGURAS
# =========================================================
def base_layout(fig, titulo, yaxis_title, xaxis_title=None):
    fig.update_layout(
        title={"text": titulo, "x": 0.5},
        template="plotly_white",
        hovermode="x unified",
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
        margin=dict(l=40, r=20, t=90, b=60),
        yaxis_title=yaxis_title,
        xaxis_title=xaxis_title,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )
    return fig

def crear_figura_principal(df_plot):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_plot["Etiqueta"],
        y=df_plot["Capital aportado"],
        mode="lines",
        name="Capital aportado",
        line=dict(width=3, color=COLOR_CAPITAL)
    ))

    fig.add_trace(go.Scatter(
        x=df_plot["Etiqueta"],
        y=df_plot["Valor total neto"],
        mode="lines+markers",
        name="Valor total estimado",
        line=dict(width=4, color=COLOR_PRIMARY),
        marker=dict(size=7)
    ))

    fig.add_trace(go.Scatter(
        x=df_plot["Etiqueta"],
        y=df_plot["Valor real neto"],
        mode="lines",
        name="Valor real estimado",
        line=dict(width=3, dash="dash", color=COLOR_REAL)
    ))

    valor_final = df_plot["Valor total neto"].iloc[-1]
    capital_final = df_plot["Capital aportado"].iloc[-1]
    crecimiento = valor_final - capital_final

    fig.add_annotation(
        x=df_plot["Etiqueta"].iloc[-1],
        y=valor_final,
        text=f"+{formatear_euros_es(crecimiento)}",
        showarrow=True,
        arrowhead=2,
        ax=-55,
        ay=-55,
        bgcolor="white",
        bordercolor=COLOR_BORDER
    )

    base_layout(fig, "Evolución de tu inversión", "Importe (€)")
    if len(df_plot) > 10:
        fig.update_xaxes(tickangle=-35)
    return fig

def crear_figura_comparativa_aportes(monto_inicial, tasa, anos, frecuencia, momento_aportacion, inflacion, impuestos, comision, crec_aporte):
    aportes = [100, 300, 500]
    fig = go.Figure()

    for aporte in aportes:
        df, _ = calcular_escenario(
            f"{aporte} €/periodo",
            monto_inicial, aporte, tasa, anos, frecuencia, momento_aportacion,
            inflacion, impuestos, comision, crec_aporte
        )
        df_plot, _ = preparar_df_plot(df, frecuencia)

        fig.add_trace(go.Scatter(
            x=df_plot["Etiqueta"],
            y=df_plot["Valor total neto"],
            mode="lines",
            name=f"{aporte} €/periodo",
            line=dict(width=3)
        ))

    base_layout(fig, "Comparativa rápida según aportación", "Importe (€)")
    if len(df_plot) > 10:
        fig.update_xaxes(tickangle=-35)
    return fig

def crear_figura_fire(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Año"],
        y=df["Capital estimado"],
        mode="lines+markers",
        name="Capital estimado",
        line=dict(width=4, color=COLOR_PRIMARY)
    ))

    fig.add_trace(go.Scatter(
        x=df["Año"],
        y=df["Número FIRE"],
        mode="lines",
        name="Número FIRE",
        line=dict(width=3, dash="dash", color=COLOR_SUCCESS)
    ))

    base_layout(fig, "Camino hacia FIRE", "Importe (€)", "Año")
    return fig

def crear_figura_hipoteca(tabla):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=tabla["Mes"],
        y=tabla["Saldo pendiente"],
        mode="lines",
        name="Saldo pendiente",
        line=dict(width=4, color=COLOR_PRIMARY)
    ))

    base_layout(fig, "Evolución del saldo pendiente", "Importe (€)", "Mes")
    return fig

# =========================================================
# TABLAS
# =========================================================
def crear_tabla(df):
    df_out = df.copy()
    columnas_euro = [
        "Aporte del período", "Capital aportado", "Interés bruto",
        "Impuestos teóricos", "Interés neto", "Valor total bruto",
        "Valor total neto", "Valor real neto"
    ]
    for col in columnas_euro:
        df_out[col] = df_out[col].map(formatear_euros_es)

    return dash_table.DataTable(
        columns=[{"name": c, "id": c} for c in df_out.columns if c != "Etiqueta"],
        data=df_out.drop(columns=["Etiqueta"]).to_dict("records"),
        page_size=12,
        sort_action="native",
        filter_action="native",
        style_table={"overflowX": "auto"},
        style_cell={
            "textAlign": "center",
            "padding": "8px",
            "fontFamily": "Arial",
            "fontSize": "13px",
            "minWidth": "110px",
            "whiteSpace": "normal"
        },
        style_header={"fontWeight": "700", "backgroundColor": "#f8fafc"},
        style_data_conditional=[{"if": {"row_index": "odd"}, "backgroundColor": "#fbfbfb"}]
    )

def crear_tabla_fire(df):
    df_out = df.copy()
    for col in ["Capital estimado", "Gasto anual objetivo", "Número FIRE", "Distancia al objetivo"]:
        df_out[col] = df_out[col].map(formatear_euros_es)

    return dash_table.DataTable(
        columns=[{"name": c, "id": c} for c in df_out.columns],
        data=df_out.to_dict("records"),
        page_size=10,
        sort_action="native",
        style_table={"overflowX": "auto"},
        style_cell={
            "textAlign": "center",
            "padding": "8px",
            "fontFamily": "Arial",
            "fontSize": "13px",
            "minWidth": "120px",
            "whiteSpace": "normal"
        },
        style_header={"fontWeight": "700", "backgroundColor": "#f8fafc"},
        style_data_conditional=[{"if": {"row_index": "odd"}, "backgroundColor": "#fbfbfb"}]
    )

def crear_tabla_hipoteca(df):
    df_out = df.copy()
    for col in ["Cuota", "Interés", "Amortización", "Saldo pendiente"]:
        df_out[col] = df_out[col].map(formatear_euros_es)

    return dash_table.DataTable(
        columns=[{"name": c, "id": c} for c in df_out.columns],
        data=df_out.to_dict("records"),
        page_size=12,
        sort_action="native",
        style_table={"overflowX": "auto"},
        style_cell={
            "textAlign": "center",
            "padding": "8px",
            "fontFamily": "Arial",
            "fontSize": "13px",
            "minWidth": "120px",
            "whiteSpace": "normal"
        },
        style_header={"fontWeight": "700", "backgroundColor": "#f8fafc"},
        style_data_conditional=[{"if": {"row_index": "odd"}, "backgroundColor": "#fbfbfb"}]
    )

# =========================================================
# COMPONENTES SEO / UI
# =========================================================
def structured_data_block():
    json_ld = """
    {
      "@context": "https://schema.org",
      "@type": "WebApplication",
      "name": "Calculadora de interés compuesto, FIRE e hipoteca",
      "applicationCategory": "FinanceApplication",
      "operatingSystem": "Any",
      "description": "Calculadora de interés compuesto con aportaciones mensuales, calculadora FIRE y calculadora de hipoteca.",
      "offers": {
        "@type": "Offer",
        "price": "0",
        "priceCurrency": "EUR"
      }
    }
    """
    return html.Script(json_ld, type="application/ld+json")

def article_structured_data_block(pathname, title, description):
    json_ld = f"""
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{title}",
      "description": "{description}",
      "author": {{
        "@type": "Organization",
        "name": "Calculadoras financieras"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "Calculadoras financieras"
      }},
      "mainEntityOfPage": {{
        "@type": "WebPage",
        "@id": "{pathname}"
      }}
    }}
    """
    return html.Script(json_ld, type="application/ld+json")

def navbar():
    return html.Div(
        dbc.Container([
            dbc.Row([
                dbc.Col(
                    html.A(
                        html.Div([
                            html.Div("●", style={"color": COLOR_PRIMARY, "fontSize": "20px", "lineHeight": "1"}),
                            html.Div(BRAND_NAME, style={"fontWeight": "800", "color": COLOR_TEXT, "fontSize": "1rem"})
                        ], style={"display": "flex", "alignItems": "center", "gap": "8px"}),
                        href="/",
                        style={"textDecoration": "none"}
                    ),
                    md=5
                ),
                dbc.Col(
                    html.Div([
                        html.A("Calculadoras", href="/#herramientas", style={"color": COLOR_MUTED, "textDecoration": "none", "fontWeight": "600"}),
                        html.A("Artículos", href="/#articulos", style={"color": COLOR_MUTED, "textDecoration": "none", "fontWeight": "600"}),
                        html.A("FAQ", href="/#faq", style={"color": COLOR_MUTED, "textDecoration": "none", "fontWeight": "600"}),
                    ], style={"display": "flex", "justifyContent": "flex-end", "gap": "18px", "flexWrap": "wrap"}),
                    md=7
                )
            ], align="center")
        ], fluid=True),
        style={
            "position": "sticky",
            "top": "0",
            "zIndex": "1000",
            "backgroundColor": "rgba(255,255,255,0.92)",
            "backdropFilter": "blur(8px)",
            "borderBottom": f"1px solid {COLOR_BORDER}",
            "padding": "14px 0"
        }
    )

def metric_card(title, value, subtitle=None, accent=COLOR_PRIMARY, soft_bg="#ffffff"):
    return dbc.Card(
        dbc.CardBody([
            html.Div(title, style={"fontSize": "0.9rem", "color": COLOR_MUTED, "fontWeight": "600"}),
            html.Div(value, style={"fontSize": "clamp(1.2rem, 4vw, 1.55rem)", "fontWeight": "800", "color": accent, "marginTop": "6px"}),
            html.Div(subtitle or "", style={"fontSize": "0.85rem", "color": COLOR_MUTED, "marginTop": "4px"})
        ]),
        style={**CARD_STYLE, "height": "100%", "backgroundColor": soft_bg}
    )

def input_block(label, component):
    return html.Div([
        html.Label(label, style=LABEL_STYLE),
        component
    ], className="mb-3")

def hero_section():
    return dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Badge("Calculadoras financieras gratis", color="light", text_color="dark", className="mb-3"),
                    html.H1(
                        "Calculadora de interés compuesto, FIRE y de hipoteca",
                        style={
                            "fontWeight": "800",
                            "lineHeight": "1.1",
                            "marginBottom": "14px",
                            "fontSize": "clamp(1.7rem, 5vw, 2.8rem)",
                            "color": COLOR_TEXT
                        }
                    ),
                    html.P(
                        "Simula cuánto podría crecer tu inversión, cuándo podrías alcanzar la libertad financiera y cuánto pagarías por una hipoteca.",
                        style={
                            "fontSize": "clamp(0.98rem, 2.8vw, 1.08rem)",
                            "color": COLOR_MUTED,
                            "maxWidth": "780px"
                        }
                    ),
                    html.P(
                        "Usa estas herramientas para comparar escenarios y tomar mejores decisiones con tus números.",
                        style={
                            "fontSize": "0.98rem",
                            "color": COLOR_MUTED,
                            "maxWidth": "780px",
                            "marginBottom": "0"
                        }
                    ),
                    html.Div([
                        dbc.Button("Abrir calculadoras", id="hero-scroll-btn", color="primary", className="me-2"),
                        html.A(
                            dbc.Button("Empieza a invertir hoy", color="success"),
                            href=MYINVESTOR_AFFILIATE_URL,
                            target="_blank",
                            rel="noopener noreferrer nofollow sponsored",
                            style={"textDecoration": "none"}
                        )
                    ], className="mt-3"),
                    html.Div([
                        dbc.Badge("Interés compuesto", color="light", text_color="dark", className="me-2"),
                        dbc.Badge("FIRE", color="light", text_color="dark", className="me-2"),
                        dbc.Badge("Hipoteca", color="light", text_color="dark")
                    ], className="mt-4")
                ], md=12)
            ])
        ]),
        style={**CARD_STYLE, "marginBottom": "20px"}
    )

def article_preview_block():
    cards = []
    for path, article in ARTICLES.items():
        cards.append(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        dbc.Badge(article["badge"], color="light", text_color="dark", className="mb-2"),
                        html.H4(article["title"], style={"fontWeight": "800", "fontSize": "1.15rem", "lineHeight": "1.35"}),
                        html.P(article["description"], style={"color": COLOR_MUTED, "marginTop": "10px", "minHeight": "88px"}),
                        html.A(
                            dbc.Button("Leer artículo", color="primary", className="w-100"),
                            href=path,
                            style={"textDecoration": "none"}
                        )
                    ]),
                    style={**CARD_STYLE, "height": "100%"}
                ),
                md=6,
                lg=4
            )
        )

    return dbc.Card(
        dbc.CardBody([
            html.Div(id="articulos", style={"scrollMarginTop": "90px"}),
            html.H2("Artículos relacionados", style={"fontWeight": "800", "marginBottom": "8px"}),
            html.P(
                "Lee más sobre inversión, FIRE y cálculo hipotecario.",
                style={"color": COLOR_MUTED, "marginBottom": "18px"}
            ),
            dbc.Row(cards, className="g-3")
        ]),
        style={**CARD_STYLE, "marginBottom": "20px"}
    )

def email_capture_block():
    return dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H3("Recibe tu simulación", style={"fontWeight": "800", "marginBottom": "8px"}),
                    html.P(
                        "Puedes añadir aquí más adelante un formulario real para guardar emails y enviar simulaciones.",
                        style={"color": COLOR_MUTED, "marginBottom": "0"}
                    )
                ], md=7),
                dbc.Col([
                    dbc.InputGroup([
                        dbc.Input(type="email", placeholder="Tu email", style=INPUT_STYLE),
                        dbc.Button("Recibir simulación", color="dark")
                    ])
                ], md=5)
            ], align="center")
        ]),
        style={**CARD_STYLE, "marginTop": "18px"}
    )

def cta_card(valor_final=None, deposito=None):
    if valor_final and deposito:
        texto_dinamico = (
            f"Si mantienes una aportación de {formatear_euros_es(deposito)}, "
            f"podrías acercarte a un patrimonio estimado de {formatear_euros_es(valor_final)}. "
            f"Empezar antes suele marcar una diferencia muy importante."
        )
    else:
        texto_dinamico = "El factor más importante no suele ser encontrar la rentabilidad perfecta, sino empezar pronto y ser constante."

    return dbc.Card(
        dbc.CardBody([
            html.Div(id="cta-afiliacion", style={"scrollMarginTop": "90px"}),
            html.H2("Empieza a invertir cuanto antes", style={"fontWeight": "800"}),
            html.P(texto_dinamico, style={"color": COLOR_MUTED}),
            html.Div(
                "Cada año que retrasas empezar puede reducir tu patrimonio futuro potencial.",
                style={"fontWeight": "600", "marginBottom": "12px", "color": COLOR_TEXT}
            ),
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("Empieza hoy con MyInvestor", style={"fontWeight": "800", "marginBottom": "10px"}),
                            html.P(
                                "Una opción conocida en España para inversión a largo plazo y fondos indexados.",
                                style={"color": COLOR_MUTED}
                            ),
                            html.Ul([
                                html.Li("Alta online"),
                                html.Li("Acceso a fondos indexados"),
                                html.Li("Útil para inversión periódica")
                            ], style={"paddingLeft": "18px", "marginBottom": "16px"}),
                            html.A(
                                dbc.Button(
                                    "Abrir cuenta y empezar a invertir",
                                    color="success",
                                    size="lg",
                                    className="w-100"
                                ),
                                href=MYINVESTOR_AFFILIATE_URL,
                                target="_blank",
                                rel="noopener noreferrer nofollow sponsored",
                                style={"textDecoration": "none"}
                            ),
                            html.Div(
                                "Enlace promocional. Puede generar una comisión.",
                                style={
                                    "fontSize": "0.82rem",
                                    "color": COLOR_MUTED,
                                    "marginTop": "10px"
                                }
                            )
                        ]),
                        style={
                            **CARD_STYLE,
                            "background": "linear-gradient(180deg, #f0fdf4 0%, #ffffff 100%)"
                        }
                    )
                ], md=12)
            ], className="g-3")
        ]),
        style={**CARD_STYLE, "marginTop": "18px"}
    )

def fire_cta_card(objetivo_ano=None, numero_fire=None):
    if objetivo_ano is not None:
        texto = f"Con este escenario podrías alcanzar FIRE en unos {objetivo_ano} años. Si quieres acercarte a ese objetivo, empezar o aumentar tu inversión puede ser decisivo."
    else:
        texto = "Con estos supuestos todavía estás lejos del objetivo FIRE. Aumentar aportaciones o empezar cuanto antes puede acercarte mucho más."

    subtitulo = f"Objetivo FIRE orientativo: {formatear_euros_es(numero_fire)}" if numero_fire else "Construye tu cartera con visión de largo plazo"

    return dbc.Card(
        dbc.CardBody([
            html.H4("Empieza a construir tu cartera FIRE", style={"fontWeight": "800"}),
            html.P(texto, style={"color": COLOR_MUTED}),
            html.Div(subtitulo, style={"fontWeight": "600", "marginBottom": "12px"}),
            html.A(
                dbc.Button("Empezar a invertir para FIRE", color="success", size="lg"),
                href=MYINVESTOR_AFFILIATE_URL,
                target="_blank",
                rel="noopener noreferrer nofollow sponsored",
                style={"textDecoration": "none"}
            ),
            html.Div(
                "Enlace promocional. Puede generar una comisión.",
                style={"fontSize": "0.82rem", "color": COLOR_MUTED, "marginTop": "10px"}
            )
        ]),
        style={**CARD_STYLE, "marginTop": "18px", "background": "linear-gradient(180deg, #f0fdf4 0%, #ffffff 100%)"}
    )

def hipoteca_cta_card(cuota=None):
    if cuota:
        texto = f"Con una cuota estimada de {formatear_euros_es(cuota)}, puede tener sentido comparar opciones antes de decidirte."
    else:
        texto = "Comparar varias ofertas hipotecarias puede ayudarte a reducir el coste total de la compra."

    return dbc.Card(
        dbc.CardBody([
            html.H4("Compara hipotecas antes de decidir", style={"fontWeight": "800"}),
            html.P(texto, style={"color": COLOR_MUTED}),
            html.Ul([
                html.Li("Compara varias ofertas"),
                html.Li("Valora fija, variable o mixta"),
                html.Li("Revisa el coste total, no solo la cuota")
            ], style={"paddingLeft": "18px", "marginBottom": "16px"}),
            html.A(
                dbc.Button("Comparar hipotecas", color="primary", size="lg"),
                href=HIPOTECA_LEAD_URL,
                target="_blank",
                rel="noopener noreferrer nofollow sponsored",
                style={"textDecoration": "none"}
            ),
            html.Div(
                "Sustituye este enlace por tu partner hipotecario cuando lo tengas.",
                style={"fontSize": "0.82rem", "color": COLOR_MUTED, "marginTop": "10px"}
            )
        ]),
        style={**CARD_STYLE, "marginTop": "18px", "backgroundColor": COLOR_PRIMARY_SOFT}
    )

def seo_block():
    return dbc.Card(
        dbc.CardBody([
            html.Div(id="faq", style={"scrollMarginTop": "90px"}),

            html.H2("Preguntas frecuentes", style={"fontWeight": "800", "fontSize": "1.7rem"}),

            html.H3("¿Sirve para calcular interés compuesto?", style={"fontWeight": "800", "fontSize": "1.2rem", "marginTop": "18px"}),
            html.P("Sí. Puedes simular inversión inicial, aportaciones periódicas, inflación, impuestos y comisiones."),

            html.H3("¿También sirve para calcular FIRE?", style={"fontWeight": "800", "fontSize": "1.2rem", "marginTop": "18px"}),
            html.P("Sí. La calculadora FIRE estima en cuántos años podrías alcanzar tu objetivo de libertad financiera."),

            html.H3("¿Tiene calculadora de hipoteca?", style={"fontWeight": "800", "fontSize": "1.2rem", "marginTop": "18px"}),
            html.P("Sí. Puedes calcular cuota mensual, intereses totales y ahorro inicial necesario."),

            html.H3("¿Los resultados están garantizados?", style={"fontWeight": "800", "fontSize": "1.2rem", "marginTop": "18px"}),
            html.P("No. Son simulaciones orientativas basadas en los datos que introduzcas.")
        ]),
        style={**CARD_STYLE, "marginTop": "20px"}
    )

def build_article_content(blocks):
    children = []
    for block_type, value in blocks:
        if block_type == "p":
            children.append(html.P(value))
        elif block_type == "h2":
            children.append(html.H2(value))
        elif block_type == "h3":
            children.append(html.H3(value))
        elif block_type == "h4":
            children.append(html.H4(value))
        elif block_type == "ul":
            children.append(html.Ul([html.Li(item) for item in value]))
    return children

def related_articles_block(current_path):
    cards = []
    for path, article in ARTICLES.items():
        if path == current_path:
            continue
        cards.append(
            dbc.Card(
                dbc.CardBody([
                    html.Div(article["title"], style={"fontWeight": "800", "fontSize": "1rem", "marginBottom": "8px"}),
                    html.P(article["description"], style={"color": COLOR_MUTED, "fontSize": "0.95rem", "marginBottom": "12px"}),
                    html.A(
                        dbc.Button("Leer", color="primary", className="w-100"),
                        href=path,
                        style={"textDecoration": "none"}
                    )
                ]),
                style={**CARD_STYLE, "marginBottom": "12px"}
            )
        )
    return cards

# =========================================================
# BLOQUES CALCULADORAS
# =========================================================
def compound_tab():
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div("Configura tu simulación", style=SECTION_TITLE_STYLE),

                    dbc.Row([
                        dbc.Col(dbc.Button("Conservador", id="preset-conservador", color="light", className="w-100"), md=4),
                        dbc.Col(dbc.Button("Base", id="preset-base", color="light", className="w-100"), md=4),
                        dbc.Col(dbc.Button("Dinámico", id="preset-dinamico", color="light", className="w-100"), md=4),
                    ], className="g-2 mb-3"),

                    input_block(
                        "Inversión inicial (€)",
                        dbc.Input(id="monto-inicial", type="text", inputMode="decimal", value="10000", style=INPUT_STYLE)
                    ),
                    input_block(
                        "Aportación periódica (€)",
                        dbc.Input(id="deposito", type="text", inputMode="decimal", value="300", style=INPUT_STYLE)
                    ),
                    input_block(
                        "Rentabilidad anual esperada (%)",
                        dbc.Input(id="tasa", type="text", inputMode="decimal", value="7", style=INPUT_STYLE)
                    ),
                    input_block(
                        "Duración (años)",
                        dbc.Input(id="anos", type="number", min=1, step=1, value=20, style=INPUT_STYLE)
                    ),

                    dbc.Accordion([
                        dbc.AccordionItem([
                            input_block(
                                "Comisión anual (%)",
                                dbc.Input(id="comision", type="text", inputMode="decimal", value="0.20", style=INPUT_STYLE)
                            ),
                            input_block(
                                "Inflación anual (%)",
                                dbc.Input(id="inflacion", type="text", inputMode="decimal", value="2.5", style=INPUT_STYLE)
                            ),
                            input_block(
                                "Impuestos sobre plusvalías (%)",
                                dbc.Input(id="impuestos", type="text", inputMode="decimal", value="19", style=INPUT_STYLE)
                            ),
                            input_block(
                                "Crecimiento anual de aportación (%)",
                                dbc.Input(id="crec-aporte", type="text", inputMode="decimal", value="0", style=INPUT_STYLE)
                            ),
                            input_block(
                                "Frecuencia",
                                dcc.Dropdown(
                                    id="frecuencia",
                                    options=[
                                        {"label": "Mensual", "value": "mensual"},
                                        {"label": "Anual", "value": "anual"}
                                    ],
                                    value="mensual",
                                    clearable=False
                                )
                            ),
                            input_block(
                                "Momento de la aportación",
                                dcc.Dropdown(
                                    id="momento-aportacion",
                                    options=[
                                        {"label": "Al inicio del período", "value": "inicio"},
                                        {"label": "Al final del período", "value": "final"}
                                    ],
                                    value="final",
                                    clearable=False
                                )
                            ),
                        ], title="Opciones avanzadas")
                    ], start_collapsed=True, className="mb-3"),

                    dbc.Row([
                        dbc.Col(dbc.Button("Calcular", id="calcular-boton", color="primary", className="w-100"), md=6),
                        dbc.Col(dbc.Button("Reset", id="reset-boton", color="light", className="w-100"), md=6),
                    ], className="g-2"),

                    html.Hr(),

                    html.Div("Exportar", style=SECTION_TITLE_STYLE),
                    dbc.Row([
                        dbc.Col(dbc.Button("CSV", id="descargar-csv-btn", color="secondary", className="w-100"), md=4),
                        dbc.Col(dbc.Button("Excel", id="descargar-excel-btn", color="secondary", className="w-100"), md=4),
                        dbc.Col(dbc.Button("Informe HTML", id="descargar-html-btn", color="dark", className="w-100"), md=4),
                    ], className="g-2"),

                    dcc.Download(id="descargar-csv"),
                    dcc.Download(id="descargar-excel"),
                    dcc.Download(id="descargar-html"),

                    html.Div(id="mensajes-validacion", className="mt-3")
                ])
            ], style=CARD_STYLE)
        ], md=4),

        dbc.Col([
            html.Div(id="resultado-anchor", style={"scrollMarginTop": "90px"}),
            html.Div(id="resultado-principal")
        ], md=8)
    ])

def fire_tab():
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div("Configura tu objetivo FIRE", style=SECTION_TITLE_STYLE),

                    input_block(
                        "Patrimonio invertido actual (€)",
                        dbc.Input(id="fire-cartera-actual", type="text", inputMode="decimal", value="50000", style=INPUT_STYLE)
                    ),
                    input_block(
                        "Aportación anual (€)",
                        dbc.Input(id="fire-aportacion-anual", type="text", inputMode="decimal", value="7000", style=INPUT_STYLE)
                    ),
                    input_block(
                        "Rentabilidad anual esperada (%)",
                        dbc.Input(id="fire-rentabilidad", type="text", inputMode="decimal", value="7", style=INPUT_STYLE)
                    ),
                    input_block(
                        "Inflación anual (%)",
                        dbc.Input(id="fire-inflacion", type="text", inputMode="decimal", value="2.5", style=INPUT_STYLE)
                    ),
                    input_block(
                        "Gasto anual objetivo de hoy (€)",
                        dbc.Input(id="fire-gasto-anual", type="text", inputMode="decimal", value="24000", style=INPUT_STYLE)
                    ),
                    input_block(
                        "Tasa de retirada segura (%)",
                        dbc.Input(id="fire-retiro", type="text", inputMode="decimal", value="4", style=INPUT_STYLE)
                    ),

                    dbc.Button("Calcular FIRE", id="fire-calcular-boton", color="primary", className="w-100")
                ])
            ], style=CARD_STYLE)
        ], md=4),

        dbc.Col([
            html.Div(id="fire-resultado")
        ], md=8)
    ])

def mortgage_tab():
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div("Configura tu hipoteca", style=SECTION_TITLE_STYLE),

                    input_block(
                        "Precio de la vivienda (€)",
                        dbc.Input(id="hip-precio", type="text", inputMode="decimal", value="250000", style=INPUT_STYLE)
                    ),
                    input_block(
                        "Entrada (€)",
                        dbc.Input(id="hip-entrada", type="text", inputMode="decimal", value="50000", style=INPUT_STYLE)
                    ),
                    input_block(
                        "Interés anual (%)",
                        dbc.Input(id="hip-interes", type="text", inputMode="decimal", value="3.0", style=INPUT_STYLE)
                    ),
                    input_block(
                        "Plazo (años)",
                        dbc.Input(id="hip-anos", type="number", min=1, step=1, value=30, style=INPUT_STYLE)
                    ),
                    input_block(
                        "Gastos de compra (%)",
                        dbc.Input(id="hip-gastos", type="text", inputMode="decimal", value="10", style=INPUT_STYLE)
                    ),

                    dbc.Button("Calcular hipoteca", id="hip-calcular-boton", color="primary", className="w-100")
                ])
            ], style=CARD_STYLE)
        ], md=4),

        dbc.Col([
            html.Div(id="hip-resultado")
        ], md=8)
    ])

def calculators_block():
    return dbc.Card(
        dbc.CardBody([
            html.Div(id="herramientas", style={"scrollMarginTop": "90px"}),
            html.H2("Calculadoras", style={"fontWeight": "800", "marginBottom": "12px"}),
            html.P("Elige la herramienta que quieras usar.", style={"color": COLOR_MUTED, "marginBottom": "18px"}),
            dbc.Tabs(
                [
                    dbc.Tab(compound_tab(), label="Interés compuesto", tabClassName="custom-tab"),
                    dbc.Tab(fire_tab(), label="Calculadora FIRE", tabClassName="custom-tab"),
                    dbc.Tab(mortgage_tab(), label="Calculadora hipoteca", tabClassName="custom-tab"),
                ]
            )
        ]),
        style={**CARD_STYLE, "marginBottom": "20px"}
    )

# =========================================================
# LAYOUT HOME
# =========================================================
def home_layout():
    return html.Div([
        dcc.Store(id="scroll-trigger"),
        dcc.Store(id="resultado-scroll-trigger"),
        structured_data_block(),
        dbc.Container([
            html.Br(),
            hero_section(),
            calculators_block(),
            cta_card(),
            email_capture_block(),
            article_preview_block(),
            seo_block(),
            html.Br()
        ], fluid=True)
    ], style={"backgroundColor": COLOR_BG, "minHeight": "100vh"})

# =========================================================
# LAYOUT ARTÍCULO
# =========================================================
def article_layout(pathname):
    article = ARTICLES[pathname]

    return html.Div([
        article_structured_data_block(pathname, article["title"], article["description"]),
        dbc.Container([
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            dbc.Badge(article["badge"], color="light", text_color="dark", className="mb-3"),
                            html.Div(
                                className="article-content",
                                children=[
                                    html.H1(
                                        article["title"],
                                        style={
                                            "fontSize": "clamp(2rem, 5vw, 2.8rem)",
                                            "lineHeight": "1.15",
                                            "marginBottom": "18px"
                                        }
                                    ),
                                    html.P(
                                        article["description"],
                                        style={"fontSize": "1.08rem", "color": COLOR_MUTED, "marginBottom": "22px"}
                                    ),

                                    html.Div([
                                        html.A(
                                            dbc.Button("Probar las calculadoras", color="primary", size="lg", className="me-2"),
                                            href="/",
                                            style={"textDecoration": "none"}
                                        ),
                                        html.A(
                                            dbc.Button("Empieza a invertir hoy", color="success", size="lg"),
                                            href=MYINVESTOR_AFFILIATE_URL,
                                            target="_blank",
                                            rel="noopener noreferrer nofollow sponsored",
                                            style={"textDecoration": "none"}
                                        )
                                    ], style={"margin": "0 0 26px 0"}),

                                    *build_article_content(article["content"]),

                                    dbc.Card(
                                        dbc.CardBody([
                                            html.H3("Haz tu propia simulación", style={"fontWeight": "800", "marginBottom": "10px"}),
                                            html.P(
                                                "Prueba ahora la calculadora y descubre distintos escenarios según tu caso.",
                                                style={"color": COLOR_MUTED}
                                            ),
                                            html.Div([
                                                html.A(
                                                    dbc.Button("Ir a la web", color="primary", size="lg", className="me-2"),
                                                    href="/",
                                                    style={"textDecoration": "none"}
                                                ),
                                                html.A(
                                                    dbc.Button("Abrir cuenta y empezar", color="success", size="lg"),
                                                    href=MYINVESTOR_AFFILIATE_URL,
                                                    target="_blank",
                                                    rel="noopener noreferrer nofollow sponsored",
                                                    style={"textDecoration": "none"}
                                                )
                                            ])
                                        ]),
                                        style={**CARD_STYLE, "marginTop": "24px", "backgroundColor": COLOR_PRIMARY_SOFT}
                                    )
                                ]
                            )
                        ]),
                        style=CARD_STYLE
                    )
                ], lg=8),

                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("Sigue explorando", style={"fontWeight": "800"}),
                            html.P(
                                "Usa la calculadora para hacer números reales según tu caso.",
                                style={"color": COLOR_MUTED}
                            ),
                            html.A(
                                dbc.Button("Abrir calculadoras", color="primary", className="w-100 mb-2"),
                                href="/",
                                style={"textDecoration": "none"}
                            ),
                            html.A(
                                dbc.Button("Empieza a invertir hoy", color="success", className="w-100"),
                                href=MYINVESTOR_AFFILIATE_URL,
                                target="_blank",
                                rel="noopener noreferrer nofollow sponsored",
                                style={"textDecoration": "none"}
                            )
                        ]),
                        style={**CARD_STYLE, "marginBottom": "18px"}
                    ),

                    dbc.Card(
                        dbc.CardBody([
                            html.H4("Más artículos", style={"fontWeight": "800", "marginBottom": "14px"}),
                            *related_articles_block(pathname)
                        ]),
                        style=CARD_STYLE
                    )
                ], lg=4)
            ]),
            html.Br()
        ], fluid=True)
    ], style={"backgroundColor": COLOR_BG, "minHeight": "100vh"})

# =========================================================
# APP LAYOUT GENERAL CON RUTAS
# =========================================================
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    navbar(),
    html.Div(id="page-content")
], style={"backgroundColor": COLOR_BG, "minHeight": "100vh"})

# =========================================================
# ROUTER
# =========================================================
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page(pathname):
    if pathname in ARTICLES:
        return article_layout(pathname)
    return home_layout()

# =========================================================
# CALLBACK SCROLL HERO
# =========================================================
@app.callback(
    Output("scroll-trigger", "data"),
    Input("hero-scroll-btn", "n_clicks"),
    prevent_initial_call=True
)
def trigger_scroll(n_clicks):
    return {"scroll": n_clicks}

clientside_callback(
    """
    function(data) {
        if (!data) {
            return window.dash_clientside.no_update;
        }

        const el = document.getElementById("herramientas");
        if (el) {
            const yOffset = -70;
            const y = el.getBoundingClientRect().top + window.pageYOffset + yOffset;
            window.scrollTo({ top: y, behavior: "smooth" });
        }

        return "";
    }
    """,
    Output("hero-scroll-btn", "title"),
    Input("scroll-trigger", "data")
)

# =========================================================
# CALLBACK SCROLL RESULTADO + HIGHLIGHT
# =========================================================
@app.callback(
    Output("resultado-scroll-trigger", "data"),
    Input("calcular-boton", "n_clicks"),
    State("monto-inicial", "value"),
    State("deposito", "value"),
    State("tasa", "value"),
    State("anos", "value"),
    State("inflacion", "value"),
    State("impuestos", "value"),
    State("comision", "value"),
    State("crec-aporte", "value"),
    prevent_initial_call=True
)
def trigger_resultado_scroll(n_clicks, monto, deposito, tasa, anos, inflacion, impuestos, comision, crec_aporte):
    errores = validar_inputs(monto, deposito, tasa, anos, inflacion, impuestos, comision, crec_aporte)
    if errores:
        return None
    return {"scroll_to_resultado": n_clicks}

clientside_callback(
    """
    function(data) {
        if (!data) {
            return window.dash_clientside.no_update;
        }

        const el = document.getElementById("resultado-anchor");
        if (el) {
            const yOffset = -85;
            const y = el.getBoundingClientRect().top + window.pageYOffset + yOffset;
            window.scrollTo({ top: y, behavior: "smooth" });

            const resultadoPrincipal = document.getElementById("resultado-principal");
            if (resultadoPrincipal) {
                resultadoPrincipal.classList.remove("resultado-highlight");
                void resultadoPrincipal.offsetWidth;
                resultadoPrincipal.classList.add("resultado-highlight");
            }
        }

        return "";
    }
    """,
    Output("calcular-boton", "title"),
    Input("resultado-scroll-trigger", "data")
)

# =========================================================
# PRESETS
# =========================================================
@app.callback(
    Output("monto-inicial", "value", allow_duplicate=True),
    Output("deposito", "value", allow_duplicate=True),
    Output("tasa", "value", allow_duplicate=True),
    Output("anos", "value", allow_duplicate=True),
    Output("comision", "value", allow_duplicate=True),
    Output("inflacion", "value", allow_duplicate=True),
    Output("impuestos", "value", allow_duplicate=True),
    Output("crec-aporte", "value", allow_duplicate=True),
    Input("preset-conservador", "n_clicks"),
    Input("preset-base", "n_clicks"),
    Input("preset-dinamico", "n_clicks"),
    prevent_initial_call=True
)
def aplicar_preset(n1, n2, n3):
    trigger = callback_context.triggered_id
    if trigger == "preset-conservador":
        return "10000", "200", "4.5", 20, "0.25", "2.0", "19", "0"
    if trigger == "preset-base":
        return "10000", "300", "7.0", 20, "0.20", "2.5", "19", "0"
    if trigger == "preset-dinamico":
        return "10000", "450", "9.0", 20, "0.20", "2.5", "19", "1.5"
    return "10000", "300", "7.0", 20, "0.20", "2.5", "19", "0"

# =========================================================
# RESET
# =========================================================
@app.callback(
    Output("monto-inicial", "value"),
    Output("deposito", "value"),
    Output("tasa", "value"),
    Output("anos", "value"),
    Output("comision", "value"),
    Output("inflacion", "value"),
    Output("impuestos", "value"),
    Output("crec-aporte", "value"),
    Output("frecuencia", "value"),
    Output("momento-aportacion", "value"),
    Input("reset-boton", "n_clicks"),
    prevent_initial_call=True
)
def resetear(n_clicks):
    return "10000", "300", "7", 20, "0.20", "2.5", "19", "0", "mensual", "final"

# =========================================================
# VALIDACIÓN
# =========================================================
@app.callback(
    Output("mensajes-validacion", "children"),
    Input("calcular-boton", "n_clicks"),
    State("monto-inicial", "value"),
    State("deposito", "value"),
    State("tasa", "value"),
    State("anos", "value"),
    State("inflacion", "value"),
    State("impuestos", "value"),
    State("comision", "value"),
    State("crec-aporte", "value"),
    prevent_initial_call=True
)
def mostrar_validacion(n_clicks, monto, deposito, tasa, anos, inflacion, impuestos, comision, crec_aporte):
    errores = validar_inputs(monto, deposito, tasa, anos, inflacion, impuestos, comision, crec_aporte)
    if not errores:
        return html.Div()
    return dbc.Alert([html.Div(e) for e in errores], color="danger")

# =========================================================
# RESULTADOS INTERÉS COMPUESTO
# =========================================================
@app.callback(
    Output("resultado-principal", "children"),
    Input("calcular-boton", "n_clicks"),
    State("monto-inicial", "value"),
    State("deposito", "value"),
    State("tasa", "value"),
    State("anos", "value"),
    State("comision", "value"),
    State("inflacion", "value"),
    State("impuestos", "value"),
    State("crec-aporte", "value"),
    State("frecuencia", "value"),
    State("momento-aportacion", "value")
)
def render_resultado(
    n_clicks, monto_inicial, deposito, tasa, anos, comision,
    inflacion, impuestos, crec_aporte, frecuencia, momento_aportacion
):
    if not n_clicks:
        return dbc.Alert("Pulsa en «Calcular» para ver tu simulación de interés compuesto.", color="info")

    errores = validar_inputs(monto_inicial, deposito, tasa, anos, inflacion, impuestos, comision, crec_aporte)
    if errores:
        return dbc.Alert("Corrige los errores para continuar.", color="warning")

    df, _ = calcular_escenario(
        "Base", monto_inicial, deposito, tasa, anos, frecuencia, momento_aportacion,
        inflacion, impuestos, comision, crec_aporte
    )

    df_plot, eje_x = preparar_df_plot(df, frecuencia)
    fig_principal = crear_figura_principal(df_plot)
    fig_principal.update_xaxes(title=eje_x)

    fig_comparativa = crear_figura_comparativa_aportes(
        monto_inicial, tasa, anos, frecuencia, momento_aportacion,
        inflacion, impuestos, comision, crec_aporte
    )
    fig_comparativa.update_xaxes(title=eje_x)

    valor_final = df["Valor total neto"].iloc[-1]
    valor_real = df["Valor real neto"].iloc[-1]
    capital = df["Capital aportado"].iloc[-1]
    crecimiento = df["Interés neto"].iloc[-1]
    impuestos_pagados = df["Impuestos teóricos"].iloc[-1]
    cagr = calcular_cagr(capital, valor_final, safe_int(anos))

    df_esperar, _ = calcular_escenario(
        "Esperar 3 años",
        0, deposito, tasa, max(1, safe_int(anos) - 3), frecuencia, momento_aportacion,
        inflacion, impuestos, comision, crec_aporte
    )
    coste_esperar = valor_final - df_esperar["Valor total neto"].iloc[-1]

    texto_resumen = (
        f"Si inviertes {formatear_euros_es(monto_inicial)} al inicio y aportas "
        f"{formatear_euros_es(deposito)} por período durante {safe_int(anos)} años, "
        f"podrías alcanzar aproximadamente {formatear_euros_es(valor_final)}."
    )

    insight = (
        f"De ese total, {formatear_euros_es(capital)} serían aportaciones y "
        f"{formatear_euros_es(crecimiento)} crecimiento neto estimado."
    )

    cards = dbc.Row([
        dbc.Col(metric_card("Valor final estimado", formatear_euros_es(valor_final), "Resultado nominal", COLOR_PRIMARY, COLOR_PRIMARY_SOFT), md=6, lg=3),
        dbc.Col(metric_card("Valor real estimado", formatear_euros_es(valor_real), "Descontando inflación", COLOR_REAL, "#f0fdfa"), md=6, lg=3),
        dbc.Col(metric_card("Capital aportado", formatear_euros_es(capital), "Tu dinero invertido", COLOR_DARK, "#f8fafc"), md=6, lg=3),
        dbc.Col(metric_card("CAGR estimado", formatear_pct_es(cagr * 100), "Crecimiento anual compuesto", COLOR_SUCCESS, COLOR_SUCCESS_SOFT), md=6, lg=3),
        dbc.Col(metric_card("Crecimiento neto", formatear_euros_es(crecimiento), "Tras impuestos teóricos", COLOR_SUCCESS, COLOR_SUCCESS_SOFT), md=6, lg=4),
        dbc.Col(metric_card("Impuestos teóricos", formatear_euros_es(impuestos_pagados), "Estimación simplificada", COLOR_WARNING, COLOR_WARNING_SOFT), md=6, lg=4),
        dbc.Col(metric_card("Coste de esperar 3 años", formatear_euros_es(coste_esperar), "Patrimonio futuro potencial perdido", COLOR_DANGER, COLOR_DANGER_SOFT), md=12, lg=4),
    ], className="g-3")

    tabla = crear_tabla(df)

    bloque_resumen = dbc.Card(
        dbc.CardBody([
            html.H2("Resultado de tu simulación de interés compuesto", style={"fontWeight": "800", "fontSize": "1.7rem"}),
            html.P(texto_resumen, style={"fontSize": "1.08rem", "marginBottom": "8px"}),
            html.P(insight, style={"color": COLOR_MUTED, "marginBottom": "14px"}),
            html.Div([
                html.A(
                    dbc.Button("Empezar a invertir ahora", color="success", size="lg"),
                    href=MYINVESTOR_AFFILIATE_URL,
                    target="_blank",
                    rel="noopener noreferrer nofollow sponsored",
                    style={"textDecoration": "none"}
                )
            ])
        ]),
        style={**CARD_STYLE, "marginBottom": "18px"}
    )

    comparativa_box = dbc.Card(
        dbc.CardBody([
            html.H4("¿Qué pasa si aportas 100 €, 300 € o 500 €?", style={"fontWeight": "800", "marginBottom": "14px"}),
            html.P(
                "Compara rápidamente cómo cambia el resultado final al subir tu aportación periódica.",
                style={"color": COLOR_MUTED}
            ),
            dcc.Graph(
                figure=fig_comparativa,
                style={"height": "500px"},
                config={"responsive": True}
            )
        ]),
        style={**CARD_STYLE, "marginTop": "18px"}
    )

    hipotesis = dbc.Card(
        dbc.CardBody([
            html.H4("Hipótesis usadas", style={"fontWeight": "800"}),
            html.Div(f"Frecuencia: {frecuencia.title()}"),
            html.Div(f"Aportación: {'Inicio' if momento_aportacion == 'inicio' else 'Final'} del período"),
            html.Div(f"Rentabilidad bruta anual: {formatear_pct_es(tasa)}"),
            html.Div(f"Comisión anual: {formatear_pct_es(comision)}"),
            html.Div(f"Inflación anual: {formatear_pct_es(inflacion)}"),
            html.Div(f"Impuestos: {formatear_pct_es(impuestos)}"),
            html.Div(f"Crecimiento anual de aportación: {formatear_pct_es(crec_aporte)}")
        ]),
        style={**CARD_STYLE, "marginTop": "18px"}
    )

    return html.Div([
        bloque_resumen,
        cards,

        dbc.Card(
            dbc.CardBody([
                html.H4("Gráfico principal", style={"fontWeight": "800", "marginBottom": "14px"}),
                dcc.Graph(
                    figure=fig_principal,
                    style={"height": "520px"},
                    config={"responsive": True}
                )
            ]),
            style={**CARD_STYLE, "marginTop": "18px"}
        ),

        cta_card(valor_final, deposito),

        comparativa_box,

        dbc.Card(
            dbc.CardBody([
                html.H4("Detalle completo", style={"fontWeight": "800", "marginBottom": "14px"}),
                tabla
            ]),
            style={**CARD_STYLE, "marginTop": "18px"}
        ),

        hipotesis
    ])

# =========================================================
# RESULTADOS FIRE
# =========================================================
@app.callback(
    Output("fire-resultado", "children"),
    Input("fire-calcular-boton", "n_clicks"),
    State("fire-cartera-actual", "value"),
    State("fire-aportacion-anual", "value"),
    State("fire-rentabilidad", "value"),
    State("fire-inflacion", "value"),
    State("fire-gasto-anual", "value"),
    State("fire-retiro", "value")
)
def render_fire(n_clicks, cartera_actual, aportacion_anual, rentabilidad, inflacion, gasto_anual, retiro):
    if not n_clicks:
        return dbc.Alert("Pulsa en «Calcular FIRE» para ver tu escenario.", color="info")

    df_fire, objetivo_ano = calcular_fire(
        cartera_actual,
        aportacion_anual,
        rentabilidad,
        inflacion,
        gasto_anual,
        retiro
    )

    fig = crear_figura_fire(df_fire)
    numero_fire_actual = df_fire.iloc[0]["Número FIRE"]
    distancia_actual = max(numero_fire_actual - safe_float(cartera_actual), 0)

    mensaje = (
        f"Podrías alcanzar FIRE en aproximadamente {objetivo_ano} años."
        if objetivo_ano is not None else
        "Con estos supuestos no alcanzarías FIRE dentro del horizonte simulado de 60 años."
    )

    cards = dbc.Row([
        dbc.Col(metric_card(
            "Número FIRE actual",
            formatear_euros_es(numero_fire_actual),
            "Objetivo orientativo hoy",
            COLOR_PRIMARY,
            COLOR_PRIMARY_SOFT
        ), md=6, lg=4),
        dbc.Col(metric_card(
            "Distancia actual",
            formatear_euros_es(distancia_actual),
            "Lo que te falta hoy",
            COLOR_WARNING,
            COLOR_WARNING_SOFT
        ), md=6, lg=4),
        dbc.Col(metric_card(
            "Años hasta FIRE",
            str(objetivo_ano) if objetivo_ano is not None else "No alcanzado",
            "Según tus supuestos",
            COLOR_SUCCESS,
            COLOR_SUCCESS_SOFT
        ), md=12, lg=4),
    ], className="g-3")

    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.H2("Resultado de tu simulación FIRE", style={"fontWeight": "800", "fontSize": "1.7rem"}),
                html.P(mensaje, style={"fontSize": "1.08rem", "marginBottom": "14px"}),
                html.A(
                    dbc.Button("Empezar a invertir para FIRE", color="success", size="lg"),
                    href=MYINVESTOR_AFFILIATE_URL,
                    target="_blank",
                    rel="noopener noreferrer nofollow sponsored",
                    style={"textDecoration": "none"}
                )
            ]),
            style={**CARD_STYLE, "marginBottom": "18px"}
        ),
        cards,

        dbc.Card(
            dbc.CardBody([
                html.H4("Gráfico FIRE", style={"fontWeight": "800", "marginBottom": "14px"}),
                dcc.Graph(
                    figure=fig,
                    style={"height": "500px"},
                    config={"responsive": True}
                )
            ]),
            style={**CARD_STYLE, "marginTop": "18px"}
        ),

        fire_cta_card(objetivo_ano, numero_fire_actual),

        dbc.Card(
            dbc.CardBody([
                html.H4("Detalle anual", style={"fontWeight": "800", "marginBottom": "14px"}),
                crear_tabla_fire(df_fire.head(25))
            ]),
            style={**CARD_STYLE, "marginTop": "18px"}
        )
    ])

# =========================================================
# RESULTADOS HIPOTECA
# =========================================================
@app.callback(
    Output("hip-resultado", "children"),
    Input("hip-calcular-boton", "n_clicks"),
    State("hip-precio", "value"),
    State("hip-entrada", "value"),
    State("hip-interes", "value"),
    State("hip-anos", "value"),
    State("hip-gastos", "value")
)
def render_hipoteca(n_clicks, precio, entrada, interes, anos, gastos):
    if not n_clicks:
        return dbc.Alert("Pulsa en «Calcular hipoteca» para ver tu escenario.", color="info")

    resultado = calcular_hipoteca(precio, entrada, interes, anos, gastos)
    fig = crear_figura_hipoteca(resultado["tabla"])

    cards = dbc.Row([
        dbc.Col(metric_card("Importe financiado", formatear_euros_es(resultado["principal"]), "Capital del préstamo", COLOR_PRIMARY, COLOR_PRIMARY_SOFT), md=6, lg=3),
        dbc.Col(metric_card("Cuota mensual", formatear_euros_es(resultado["cuota"]), "Pago estimado", COLOR_SUCCESS, COLOR_SUCCESS_SOFT), md=6, lg=3),
        dbc.Col(metric_card("Intereses totales", formatear_euros_es(resultado["intereses_totales"]), "Coste financiero", COLOR_WARNING, COLOR_WARNING_SOFT), md=6, lg=3),
        dbc.Col(metric_card("Ahorro inicial necesario", formatear_euros_es(resultado["ahorro_necesario_inicial"]), "Entrada + gastos", COLOR_DANGER, COLOR_DANGER_SOFT), md=6, lg=3),
    ], className="g-3")

    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.H2("Resultado de tu hipoteca", style={"fontWeight": "800", "fontSize": "1.7rem"}),
                html.P(
                    f"Para una vivienda de {formatear_euros_es(precio)} con una entrada de {formatear_euros_es(entrada)}, "
                    f"la cuota estimada sería de {formatear_euros_es(resultado['cuota'])} al mes.",
                    style={"fontSize": "1.08rem", "marginBottom": "14px"}
                ),
                html.A(
                    dbc.Button("Comparar hipotecas ahora", color="primary", size="lg"),
                    href=HIPOTECA_LEAD_URL,
                    target="_blank",
                    rel="noopener noreferrer nofollow sponsored",
                    style={"textDecoration": "none"}
                )
            ]),
            style={**CARD_STYLE, "marginBottom": "18px"}
        ),
        cards,

        dbc.Card(
            dbc.CardBody([
                html.H4("Gráfico de saldo pendiente", style={"fontWeight": "800", "marginBottom": "14px"}),
                dcc.Graph(
                    figure=fig,
                    style={"height": "500px"},
                    config={"responsive": True}
                )
            ]),
            style={**CARD_STYLE, "marginTop": "18px"}
        ),

        hipoteca_cta_card(resultado["cuota"]),

        dbc.Card(
            dbc.CardBody([
                html.H4("Tabla de amortización resumida", style={"fontWeight": "800", "marginBottom": "14px"}),
                crear_tabla_hipoteca(resultado["tabla"])
            ]),
            style={**CARD_STYLE, "marginTop": "18px"}
        )
    ])

# =========================================================
# EXPORTACIONES
# =========================================================
@app.callback(
    Output("descargar-csv", "data"),
    Input("descargar-csv-btn", "n_clicks"),
    State("monto-inicial", "value"),
    State("deposito", "value"),
    State("tasa", "value"),
    State("anos", "value"),
    State("comision", "value"),
    State("inflacion", "value"),
    State("impuestos", "value"),
    State("crec-aporte", "value"),
    State("frecuencia", "value"),
    State("momento-aportacion", "value"),
    prevent_initial_call=True
)
def descargar_csv(n_clicks, monto, deposito, tasa, anos, comision, inflacion, impuestos, crec_aporte, frecuencia, momento):
    df, _ = calcular_escenario("Base", monto, deposito, tasa, anos, frecuencia, momento, inflacion, impuestos, comision, crec_aporte)
    return dcc.send_data_frame(df.to_csv, "calculadora_interes_compuesto.csv", sep=";", index=False, encoding="utf-8-sig")

@app.callback(
    Output("descargar-excel", "data"),
    Input("descargar-excel-btn", "n_clicks"),
    State("monto-inicial", "value"),
    State("deposito", "value"),
    State("tasa", "value"),
    State("anos", "value"),
    State("comision", "value"),
    State("inflacion", "value"),
    State("impuestos", "value"),
    State("crec-aporte", "value"),
    State("frecuencia", "value"),
    State("momento-aportacion", "value"),
    prevent_initial_call=True
)
def descargar_excel(n_clicks, monto, deposito, tasa, anos, comision, inflacion, impuestos, crec_aporte, frecuencia, momento):
    df, _ = calcular_escenario("Base", monto, deposito, tasa, anos, frecuencia, momento, inflacion, impuestos, comision, crec_aporte)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Simulacion", index=False)

    output.seek(0)
    return dcc.send_bytes(output.getvalue(), "calculadora_interes_compuesto.xlsx")

@app.callback(
    Output("descargar-html", "data"),
    Input("descargar-html-btn", "n_clicks"),
    State("monto-inicial", "value"),
    State("deposito", "value"),
    State("tasa", "value"),
    State("anos", "value"),
    State("comision", "value"),
    State("inflacion", "value"),
    State("impuestos", "value"),
    State("crec-aporte", "value"),
    State("frecuencia", "value"),
    State("momento-aportacion", "value"),
    prevent_initial_call=True
)
def descargar_html(n_clicks, monto, deposito, tasa, anos, comision, inflacion, impuestos, crec_aporte, frecuencia, momento):
    df, _ = calcular_escenario("Base", monto, deposito, tasa, anos, frecuencia, momento, inflacion, impuestos, comision, crec_aporte)

    final_neto = df["Valor total neto"].iloc[-1]
    final_real = df["Valor real neto"].iloc[-1]
    capital = df["Capital aportado"].iloc[-1]
    interes = df["Interés neto"].iloc[-1]

    html_report = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="description" content="Informe generado por la calculadora de interés compuesto.">
        <title>Calculadora de interés compuesto - Informe</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; color: #222; }}
            h1, h2 {{ margin-bottom: 10px; }}
            .card {{ border: 1px solid #ddd; border-radius: 12px; padding: 16px; margin-bottom: 16px; }}
            table {{ border-collapse: collapse; width: 100%; font-size: 13px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
            th {{ background: #f6f6f6; }}
        </style>
    </head>
    <body>
        <h1>Calculadora de interés compuesto</h1>
        <p>Informe generado el {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

        <div class="card">
            <h2>Resumen</h2>
            <p><strong>Capital aportado:</strong> {formatear_euros_es(capital)}</p>
            <p><strong>Crecimiento neto:</strong> {formatear_euros_es(interes)}</p>
            <p><strong>Valor final estimado:</strong> {formatear_euros_es(final_neto)}</p>
            <p><strong>Valor real estimado:</strong> {formatear_euros_es(final_real)}</p>
        </div>

        <div class="card">
            <h2>Detalle</h2>
            {df.to_html(index=False)}
        </div>
    </body>
    </html>
    """
    return dict(content=html_report, filename="informe_calculadora_interes_compuesto.html")

# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":
    app.run(debug=True)
