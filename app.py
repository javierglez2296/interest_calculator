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
            "content": "Calcula cuánto puede crecer tu dinero con esta calculadora de interés compuesto gratis. Simula inversión inicial, aportaciones mensuales, rentabilidad anual, inflación, impuestos y comisiones."
        },
        {"name": "robots", "content": "index, follow"},
        {"name": "theme-color", "content": "#2563eb"},
        {"property": "og:type", "content": "website"},
        {
            "property": "og:title",
            "content": "Calculadora de interés compuesto gratis | Con aportaciones mensuales"
        },
        {
            "property": "og:description",
            "content": "Simula cuánto podría crecer tu inversión con aportaciones periódicas, inflación, impuestos y comisiones."
        },
        {"property": "og:locale", "content": "es_ES"},
        {"name": "twitter:card", "content": "summary_large_image"},
        {
            "name": "twitter:title",
            "content": "Calculadora de interés compuesto gratis"
        },
        {
            "name": "twitter:description",
            "content": "Calcula tu patrimonio futuro estimado con aportaciones mensuales, inflación, impuestos y comisiones."
        }
    ]
)

server = app.server
app.title = "Calculadora de interés compuesto gratis | Con aportaciones mensuales"

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

        <meta name="description" content="Calcula cuánto puede crecer tu dinero con esta calculadora de interés compuesto gratis. Simula inversión inicial, aportaciones mensuales, rentabilidad anual, inflación, impuestos y comisiones.">
        <meta name="robots" content="index, follow">
        <meta name="theme-color" content="#2563eb">

        <meta property="og:type" content="website">
        <meta property="og:title" content="Calculadora de interés compuesto gratis | Con aportaciones mensuales">
        <meta property="og:description" content="Simula cuánto podría crecer tu inversión con aportaciones periódicas, inflación, impuestos y comisiones.">
        <meta property="og:locale" content="es_ES">

        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:title" content="Calculadora de interés compuesto gratis">
        <meta name="twitter:description" content="Calcula tu patrimonio futuro estimado con aportaciones mensuales, inflación, impuestos y comisiones.">

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
BRAND_NAME = "Calculadora de interés compuesto gratis"

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
            ("p", "El interés compuesto es uno de los conceptos más importantes para cualquier persona que quiera ahorrar e invertir mejor. Su idea es simple, pero su impacto a largo plazo puede ser enorme: no solo ganas rentabilidad sobre el dinero que aportas, sino también sobre los beneficios que ya has ido acumulando."),
            ("p", "Dicho de forma sencilla, es el efecto de ganar dinero sobre tu dinero y sobre el dinero que ese dinero ya generó antes. Por eso se suele decir que el interés compuesto puede ser una de las herramientas más potentes para construir patrimonio con el paso de los años."),
            ("h2", "Cómo funciona el interés compuesto"),
            ("p", "Imagina que inviertes 10.000 euros y obtienes una rentabilidad media del 7 % anual. El primer año ganarías 700 euros. Si no retiras ese beneficio, al año siguiente ya no partes de 10.000, sino de 10.700. Y ese segundo año el 7 % se aplica sobre una base mayor."),
            ("p", "Ese es el punto clave: los rendimientos se reinvierten y generan nuevos rendimientos. Con el tiempo, este efecto se acelera. Al principio parece lento, pero conforme pasan los años el crecimiento se vuelve mucho más visible."),
            ("h2", "Diferencia entre interés simple e interés compuesto"),
            ("p", "Con el interés simple, siempre ganas rentabilidad sobre la cantidad inicial. Con el interés compuesto, ganas rentabilidad sobre el capital inicial y también sobre los beneficios acumulados."),
            ("p", "A largo plazo, la diferencia entre ambos sistemas puede ser enorme."),
            ("h2", "Por qué el tiempo es tan importante"),
            ("p", "El interés compuesto necesita tiempo para desplegar su verdadero potencial. Ese es el motivo por el que empezar antes suele ser más importante que intentar aportar cantidades muy grandes más adelante."),
            ("p", "Muchas personas se centran solo en buscar una alta rentabilidad, pero olvidan que el tiempo y la constancia suelen marcar una diferencia igual o incluso mayor."),
            ("h2", "Ejemplo con aportaciones mensuales"),
            ("p", "Supón que empiezas con 5.000 euros iniciales y además aportas 200 euros al mes. Si mantienes esa estrategia durante años y reinviertes los beneficios, el efecto compuesto puede hacer crecer tu patrimonio de forma notable."),
            ("ul", [
                "El capital inicial sigue trabajando.",
                "Las aportaciones mensuales aumentan tu base invertida.",
                "Los rendimientos acumulados generan nuevos rendimientos."
            ]),
            ("h2", "Errores comunes al entender el interés compuesto"),
            ("h3", "1. Pensar que funciona rápido"),
            ("p", "Mucha gente espera grandes resultados en poco tiempo. En realidad, el interés compuesto suele ser discreto al principio y mucho más potente a largo plazo."),
            ("h3", "2. No reinvertir"),
            ("p", "Si retiras continuamente las ganancias, el efecto compuesto pierde fuerza."),
            ("h3", "3. Empezar demasiado tarde"),
            ("p", "Retrasar varios años el inicio puede tener un impacto importante en el resultado final."),
            ("h3", "4. Aportar de forma irregular"),
            ("p", "La constancia suele ser más útil que intentar acertar siempre el mejor momento del mercado."),
            ("h3", "5. Olvidar comisiones e impuestos"),
            ("p", "Comisiones altas, inflación e impuestos pueden reducir bastante el resultado final, así que conviene tenerlos en cuenta."),
            ("h2", "Conclusión"),
            ("p", "El interés compuesto no es magia, pero se le parece bastante cuando se entiende bien y se aplica con paciencia. Su verdadera fuerza está en combinar tres cosas: tiempo, reinversión y constancia."),
            ("p", "No hace falta empezar con muchísimo dinero. Lo importante es comenzar, mantener una estrategia razonable y dejar que el tiempo haga su trabajo.")
        ]
    },
    "/cuanto-dinero-puedes-tener-invirtiendo-200-euros-al-mes": {
        "title": "Cuánto dinero puedes tener invirtiendo 200 euros al mes",
        "description": "Una simulación sencilla para entender cuánto patrimonio podrías acumular invirtiendo 200 euros al mes durante años.",
        "badge": "Simulación práctica",
        "content": [
            ("p", "Una de las preguntas más habituales entre quienes empiezan a invertir es esta: ¿de verdad merece la pena aportar 200 euros al mes? La respuesta corta es sí, especialmente si lo haces durante muchos años y de forma constante."),
            ("p", "La clave no está solo en la cantidad mensual, sino en el tiempo. Cuando aportas 200 euros cada mes y reinviertes los rendimientos, el interés compuesto empieza a trabajar a tu favor."),
            ("h2", "Por qué 200 euros al mes pueden ser más potentes de lo que parecen"),
            ("p", "Muchas personas creen que para invertir hace falta tener mucho dinero. En la práctica, una estrategia periódica con una cantidad asumible puede ser suficiente para empezar a construir patrimonio."),
            ("p", "Invertir 200 euros al mes son 2.400 euros al año. Mantener esa disciplina durante 10, 20 o 30 años puede dar lugar a cifras mucho más altas de lo que parece al principio."),
            ("h2", "Qué variables marcan el resultado final"),
            ("ul", [
                "El número de años durante los que inviertes.",
                "La rentabilidad media anual que consigas.",
                "Si reinviertes o no las ganancias.",
                "Las comisiones y los impuestos.",
                "Si aumentas tus aportaciones con el tiempo."
            ]),
            ("h2", "Ejemplo orientativo"),
            ("p", "Si una persona invierte 200 euros al mes durante 20 años y obtiene una rentabilidad media anual razonable, el patrimonio final podría situarse muy por encima del dinero total aportado. Eso ocurre porque con el paso de los años una parte creciente del crecimiento ya no viene solo de tus aportaciones, sino del capital acumulado."),
            ("p", "A partir de cierto punto, el crecimiento empieza a acelerarse y se vuelve mucho más visible. Por eso las estrategias de inversión a largo plazo suelen recompensar más la constancia que la prisa."),
            ("h2", "Qué pasa si empiezas antes o más tarde"),
            ("p", "Empezar cinco años antes puede marcar una diferencia muy grande. No porque aportes muchísimo más dinero, sino porque das más tiempo al capital para multiplicarse."),
            ("p", "En cambio, esperar demasiado suele salir caro. El coste de retrasar el inicio puede ser mayor que el de invertir una cantidad algo más baja."),
            ("h2", "Cómo usar esta idea de forma útil"),
            ("p", "La mejor manera de saber cuánto podrías tener invirtiendo 200 euros al mes es hacer una simulación con tus propios datos. Puedes probar distintos horizontes temporales, variar la rentabilidad esperada y ver cómo cambian los resultados."),
            ("p", "Eso te permite responder preguntas muy útiles: si te conviene aportar más, si compensa empezar ya o si podrías llegar a una cifra concreta dentro de 15 o 20 años."),
            ("h2", "Conclusión"),
            ("p", "Invertir 200 euros al mes sí puede merecer mucho la pena. No te hará rico de la noche a la mañana, pero puede ayudarte a construir un patrimonio sólido con el paso de los años."),
            ("p", "La diferencia real no suele estar en encontrar la inversión perfecta, sino en empezar, ser constante y dejar que el tiempo haga su trabajo.")
        ]
    },
    "/cuando-se-nota-de-verdad-el-interes-compuesto": {
        "title": "Cuándo se nota de verdad el interés compuesto",
        "description": "El interés compuesto parece lento al principio, pero con el tiempo se acelera. Descubre cuándo suele empezar a notarse de verdad.",
        "badge": "Concepto clave",
        "content": [
            ("p", "Una de las mayores frustraciones al empezar a invertir es sentir que el crecimiento va demasiado despacio. Eso es normal. El interés compuesto no suele impresionar en los primeros años, pero cambia mucho con el paso del tiempo."),
            ("p", "La pregunta importante no es solo cuánto ganas, sino cuándo empieza a notarse de verdad el efecto acumulativo."),
            ("h2", "Por qué al principio parece lento"),
            ("p", "Al comienzo, casi todo el crecimiento de tu patrimonio depende de lo que tú aportas. La rentabilidad existe, pero como la base invertida todavía es pequeña, su impacto absoluto es limitado."),
            ("p", "Eso hace que los primeros años parezcan poco espectaculares. Aun así, esa fase es clave, porque estás construyendo la base sobre la que luego crecerá todo lo demás."),
            ("h2", "El punto de inflexión"),
            ("p", "El interés compuesto suele empezar a notarse más cuando el capital acumulado ya es lo bastante grande como para que sus rendimientos pesen mucho más. En ese momento, el dinero invertido empieza a trabajar con mayor fuerza y la curva se vuelve más empinada."),
            ("p", "No hay una fecha exacta universal, porque depende de la rentabilidad, de las aportaciones y del capital inicial. Pero en horizontes largos, mucha gente empieza a percibir una diferencia clara a partir de los años intermedios del proceso, no al principio."),
            ("h2", "Cómo saber si ya estás entrando en esa fase"),
            ("ul", [
                "Tu cartera empieza a crecer más por la rentabilidad que por nuevas aportaciones.",
                "Un buen año de mercado añade una cantidad relevante a tu patrimonio.",
                "Tus resultados mejoran aunque no aumentes demasiado tus aportaciones.",
                "La diferencia entre seguir invertido y parar se vuelve muy visible."
            ]),
            ("h2", "Qué errores hacen que nunca se note del todo"),
            ("h3", "1. Cambiar de estrategia constantemente"),
            ("p", "Si interrumpes el proceso cada poco tiempo, el interés compuesto no llega a desplegarse."),
            ("h3", "2. Retirar ganancias demasiado pronto"),
            ("p", "Sacar beneficios continuamente limita mucho el crecimiento acumulado."),
            ("h3", "3. Empezar tarde y querer resultados inmediatos"),
            ("p", "La paciencia es una parte esencial del proceso."),
            ("h2", "Qué puedes hacer para acelerarlo razonablemente"),
            ("ul", [
                "Aportar de forma periódica.",
                "Aumentar tus aportaciones cuando puedas.",
                "Reducir comisiones innecesarias.",
                "Mantener una visión de largo plazo.",
                "Evitar decisiones impulsivas."
            ]),
            ("h2", "Conclusión"),
            ("p", "El interés compuesto se nota de verdad cuando le das tiempo suficiente. Al principio avanza despacio, pero luego puede sorprenderte mucho más de lo que parece."),
            ("p", "La mayoría abandona antes de llegar a esa fase. Precisamente por eso, la constancia suele ser una ventaja tan potente.")
        ]
    },
    "/etf-vs-cuenta-remunerada": {
        "title": "ETF vs cuenta remunerada: qué diferencias hay y para quién encaja cada opción",
        "description": "Compara ETF y cuenta remunerada para entender cuál puede encajar mejor según tu plazo, riesgo y objetivo financiero.",
        "badge": "Comparativa",
        "content": [
            ("p", "Muchas personas que empiezan a mover su dinero dudan entre dos opciones muy distintas: invertir en ETF o dejar el dinero en una cuenta remunerada. Ambas pueden ser útiles, pero no sirven exactamente para lo mismo."),
            ("p", "Elegir bien depende sobre todo de tu horizonte temporal, tu tolerancia al riesgo y el uso que vayas a dar a ese dinero."),
            ("h2", "Qué es una cuenta remunerada"),
            ("p", "Una cuenta remunerada es una cuenta bancaria que paga intereses por el dinero depositado. Su principal ventaja es la simplicidad: sabes que tu saldo no debería sufrir grandes oscilaciones y mantienes liquidez alta."),
            ("p", "Suele ser una opción interesante para fondo de emergencia, dinero a corto plazo o personas que todavía no quieren asumir volatilidad."),
            ("h2", "Qué es un ETF"),
            ("p", "Un ETF es un fondo cotizado que puede replicar un índice, un sector o una cesta de activos. Permite invertir de forma diversificada y normalmente se utiliza con un enfoque de medio o largo plazo."),
            ("p", "Su gran ventaja es el potencial de crecimiento, pero a cambio asumes fluctuaciones de mercado. Eso significa que en algunos periodos el valor puede subir mucho y en otros bajar."),
            ("h2", "Diferencias principales"),
            ("ul", [
                "La cuenta remunerada prioriza estabilidad y liquidez.",
                "El ETF prioriza crecimiento potencial a largo plazo.",
                "La cuenta remunerada suele tener menos volatilidad.",
                "El ETF puede ofrecer mejores resultados a largo plazo, pero no garantiza nada.",
                "La cuenta remunerada encaja mejor para plazos cortos; el ETF suele tener más sentido a plazos largos."
            ]),
            ("h2", "Para quién encaja mejor una cuenta remunerada"),
            ("ul", [
                "Para quien necesita el dinero en poco tiempo.",
                "Para un fondo de emergencia.",
                "Para perfiles muy conservadores.",
                "Para quien prioriza tranquilidad sobre rentabilidad potencial."
            ]),
            ("h2", "Para quién encaja mejor un ETF"),
            ("ul", [
                "Para quien invierte a largo plazo.",
                "Para quien acepta oscilaciones del mercado.",
                "Para quien busca crecimiento patrimonial.",
                "Para estrategias de aportación periódica."
            ]),
            ("h2", "¿Y si combinas ambas?"),
            ("p", "De hecho, en muchos casos la mejor solución no es elegir solo una. Puedes mantener una parte del dinero en una cuenta remunerada para seguridad y liquidez, y destinar otra parte a ETF para crecimiento a largo plazo."),
            ("p", "Ese enfoque te permite cubrir necesidades de corto plazo sin renunciar al potencial del interés compuesto en el dinero que no necesitas tocar."),
            ("h2", "Conclusión"),
            ("p", "ETF y cuenta remunerada no son enemigos. Son herramientas distintas para objetivos distintos."),
            ("p", "Si el dinero lo necesitas pronto, la cuenta remunerada suele tener más sentido. Si tu objetivo es construir patrimonio a largo plazo, los ETF suelen ofrecer más potencial, aunque con más volatilidad.")
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
# CÁLCULO
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

# =========================================================
# TABLA
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

# =========================================================
# COMPONENTES SEO / UI
# =========================================================
def structured_data_block():
    json_ld = """
    {
      "@context": "https://schema.org",
      "@type": "WebApplication",
      "name": "Calculadora de interés compuesto gratis",
      "applicationCategory": "FinanceApplication",
      "operatingSystem": "Any",
      "description": "Calculadora de interés compuesto con aportaciones mensuales, inflación, impuestos y comisiones.",
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
        "name": "Calculadora de interés compuesto gratis"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "Calculadora de interés compuesto gratis"
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
                    md=6
                ),
                dbc.Col(
                    html.Div([
                        html.A("Simulador", href="/#simulador", style={"color": COLOR_MUTED, "textDecoration": "none", "fontWeight": "600"}),
                        html.A("Comparativa", href="/#comparativa", style={"color": COLOR_MUTED, "textDecoration": "none", "fontWeight": "600"}),
                        html.A("Artículos", href="/#articulos", style={"color": COLOR_MUTED, "textDecoration": "none", "fontWeight": "600"}),
                        html.A("FAQ", href="/#faq", style={"color": COLOR_MUTED, "textDecoration": "none", "fontWeight": "600"}),
                    ], style={"display": "flex", "justifyContent": "flex-end", "gap": "18px", "flexWrap": "wrap"}),
                    md=6
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
                    dbc.Badge("Calculadora financiera gratis", color="light", text_color="dark", className="mb-3"),
                    html.H1(
                        "Calculadora de interés compuesto con aportaciones mensuales",
                        style={
                            "fontWeight": "800",
                            "lineHeight": "1.1",
                            "marginBottom": "14px",
                            "fontSize": "clamp(1.7rem, 5vw, 2.6rem)",
                            "color": COLOR_TEXT
                        }
                    ),
                    html.P(
                        "Usa esta calculadora de interés compuesto gratis para simular cuánto podría crecer tu inversión con una aportación inicial, aportaciones mensuales, rentabilidad anual, inflación, comisiones e impuestos.",
                        style={
                            "fontSize": "clamp(0.98rem, 2.8vw, 1.08rem)",
                            "color": COLOR_MUTED,
                            "maxWidth": "780px"
                        }
                    ),
                    html.P(
                        "Ideal para estimar escenarios de ahorro e inversión en ETF, fondos indexados, cuentas remuneradas o carteras a largo plazo.",
                        style={
                            "fontSize": "0.98rem",
                            "color": COLOR_MUTED,
                            "maxWidth": "780px",
                            "marginBottom": "0"
                        }
                    ),
                    html.Div([
                        dbc.Button("Calcular mi inversión", id="hero-scroll-btn", color="primary", className="me-2"),
                        html.A(
                            dbc.Button("Ver opciones para invertir", color="success"),
                            href="#cta-afiliacion",
                            style={"textDecoration": "none"}
                        )
                    ], className="mt-3"),
                    html.Div([
                        dbc.Badge("Interés compuesto", color="light", text_color="dark", className="me-2"),
                        dbc.Badge("Aportaciones mensuales", color="light", text_color="dark", className="me-2"),
                        dbc.Badge("ETF y fondos indexados", color="light", text_color="dark")
                    ], className="mt-4")
                ], md=8),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.Div("Ejemplo orientativo", style={"fontWeight": "700", "color": COLOR_MUTED}),
                            html.H3("300 €/mes", style={"fontWeight": "800", "marginTop": "10px", "marginBottom": "4px"}),
                            html.Div("20 años · 7 % anual · 10.000 € iniciales", style={"color": COLOR_MUTED, "fontSize": "0.95rem"}),
                            html.Hr(),
                            html.Div("Resultado estimado", style={"color": COLOR_MUTED}),
                            html.H2("≈ 181.000 €", style={"fontWeight": "800", "color": COLOR_PRIMARY, "marginTop": "8px"}),
                            html.Div("Simulación orientativa no garantizada", style={"color": COLOR_MUTED, "fontSize": "0.82rem"})
                        ]),
                        style={
                            "borderRadius": "22px",
                            "background": "linear-gradient(180deg, #eff6ff 0%, #ffffff 100%)",
                            "border": f"1px solid {COLOR_BORDER}",
                            "boxShadow": "0 12px 30px rgba(37,99,235,0.10)"
                        }
                    )
                ], md=4)
            ])
        ]),
        style={**CARD_STYLE, "marginBottom": "20px"}
    )

def trust_block():
    return dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Rápida y clara", style={"fontWeight": "800"}),
            html.P("Ve una estimación de tu patrimonio futuro en menos de un minuto.", style={"color": COLOR_MUTED, "marginBottom": "0"})
        ]), style=CARD_STYLE), md=4),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Útil para decidir", style={"fontWeight": "800"}),
            html.P("Compara escenarios y detecta el coste real de esperar más tiempo.", style={"color": COLOR_MUTED, "marginBottom": "0"})
        ]), style=CARD_STYLE), md=4),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Lista para monetizar", style={"fontWeight": "800"}),
            html.P("Puedes insertar enlaces de afiliación donde el usuario ya está convencido.", style={"color": COLOR_MUTED, "marginBottom": "0"})
        ]), style=CARD_STYLE), md=4),
    ], className="g-3 mb-4")

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
                lg=3
            )
        )

    return dbc.Card(
        dbc.CardBody([
            html.Div(id="articulos", style={"scrollMarginTop": "90px"}),
            html.H2("Artículos para aprender e invertir mejor", style={"fontWeight": "800", "marginBottom": "8px"}),
            html.P(
                "Estos contenidos están pensados para atraer tráfico desde Google y llevar al usuario hacia la calculadora o tus enlaces de afiliación.",
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
                    html.H3("Captura leads con esta sección", style={"fontWeight": "800", "marginBottom": "8px"}),
                    html.P(
                        "Aquí puedes conectar más adelante un formulario real para enviar la simulación por email. "
                        "Eso te permite hacer seguimiento y monetizar después con afiliación.",
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

def cta_card():
    return dbc.Card(
        dbc.CardBody([
            html.Div(id="cta-afiliacion", style={"scrollMarginTop": "90px"}),

            html.H3("¿Quieres empezar a invertir?", style={"fontWeight": "800"}),
            html.P(
                "Si quieres empezar hoy mismo, puedes abrir cuenta en MyInvestor y dar el primer paso hacia una estrategia de inversión a largo plazo. "
                "Es una opción muy conocida en España para fondos indexados y ahorro invertido.",
                style={"color": COLOR_MUTED}
            ),

            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.H4("MyInvestor", style={"fontWeight": "800", "marginBottom": "10px"}),
                            html.P(
                                "Banco español orientado a inversión y ahorro a largo plazo.",
                                style={"color": COLOR_MUTED, "marginBottom": "10px"}
                            ),
                            html.Ul([
                                html.Li("Fondos indexados y cartera a largo plazo"),
                                html.Li("Opción interesante para empezar a invertir"),
                                html.Li("Proceso de alta online")
                            ], style={"paddingLeft": "18px", "marginBottom": "16px"}),

                            html.A(
                                dbc.Button(
                                    "Abrir cuenta en MyInvestor",
                                    color="success",
                                    size="lg",
                                    className="w-100"
                                ),
                                href=MYINVESTOR_AFFILIATE_URL,
                                target="_blank",
                                rel="noopener noreferrer nofollow sponsored"
                            ),

                            html.Div(
                                "Enlace promocional. Puede generar una comisión o beneficio promocional.",
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

def seo_block():
    return dbc.Card(
        dbc.CardBody([
            html.Div(id="faq", style={"scrollMarginTop": "90px"}),

            html.H2("Calculadora de interés compuesto: cómo usarla", style={"fontWeight": "800", "fontSize": "1.7rem"}),
            html.P(
                "Esta calculadora de interés compuesto te permite estimar cuánto podría crecer una inversión a largo plazo combinando una cantidad inicial, aportaciones periódicas y una rentabilidad anual esperada. "
                "También puedes ajustar inflación, impuestos y comisiones para obtener una simulación más realista."
            ),

            html.H3("Qué es el interés compuesto", style={"fontWeight": "800", "fontSize": "1.25rem", "marginTop": "20px"}),
            html.P(
                "El interés compuesto es el efecto por el que los rendimientos generados por una inversión vuelven a reinvertirse y empiezan a producir nuevas ganancias. "
                "Con el paso del tiempo, este efecto puede hacer que el crecimiento del patrimonio se acelere de forma muy significativa."
            ),

            html.H3("Cómo funciona esta calculadora de inversión", style={"fontWeight": "800", "fontSize": "1.25rem", "marginTop": "20px"}),
            html.P(
                "Introduce tu inversión inicial, la aportación mensual o anual que quieres hacer, la rentabilidad esperada y el número de años. "
                "Después podrás ver el capital aportado, el valor final estimado, el impacto de la inflación y una aproximación del crecimiento neto tras impuestos."
            ),

            html.H3("Ejemplo de interés compuesto con aportaciones mensuales", style={"fontWeight": "800", "fontSize": "1.25rem", "marginTop": "20px"}),
            html.P(
                "Por ejemplo, si inviertes 10.000 € al inicio y aportas 300 € al mes durante 20 años con una rentabilidad anual del 7 %, el capital final estimado puede crecer de forma notable gracias al interés compuesto. "
                "Este tipo de simulación ayuda a entender por qué empezar pronto suele ser más importante que intentar encontrar el activo perfecto."
            ),

            html.H3("Para quién sirve este simulador", style={"fontWeight": "800", "fontSize": "1.25rem", "marginTop": "20px"}),
            html.P(
                "Este simulador de interés compuesto es útil para personas que quieran planificar ahorro a largo plazo, comparar escenarios de inversión en ETF, fondos indexados, cuentas remuneradas o carteras diversificadas, "
                "y visualizar el efecto de aumentar o reducir sus aportaciones periódicas."
            ),

            html.H3("Por qué empezar antes importa", style={"fontWeight": "800", "fontSize": "1.25rem", "marginTop": "20px"}),
            html.P(
                "En muchas estrategias de inversión, el mayor enemigo no es una rentabilidad algo menor, sino retrasar el inicio. "
                "El tiempo es uno de los factores más potentes del interés compuesto, por lo que empezar antes puede marcar una diferencia enorme en el patrimonio futuro estimado."
            ),

            html.H3("Preguntas frecuentes sobre la calculadora de interés compuesto", style={"fontWeight": "800", "fontSize": "1.25rem", "marginTop": "20px"}),

            html.H4("¿Sirve para ETF, fondos indexados o ahorro periódico?", style={"fontWeight": "800", "fontSize": "1.05rem", "marginTop": "16px"}),
            html.P(
                "Sí. Esta herramienta está pensada como simulador orientativo para estrategias de inversión a largo plazo, especialmente útiles en ETF, fondos indexados y planes de aportación periódica."
            ),

            html.H4("¿El resultado está garantizado?", style={"fontWeight": "800", "fontSize": "1.05rem", "marginTop": "16px"}),
            html.P(
                "No. Los resultados que muestra la calculadora son estimaciones basadas en los supuestos introducidos por el usuario. La rentabilidad futura real puede ser distinta."
            ),

            html.H4("¿Por qué incluir inflación, comisiones e impuestos?", style={"fontWeight": "800", "fontSize": "1.05rem", "marginTop": "16px"}),
            html.P(
                "Porque ayudan a acercar la simulación a escenarios más realistas. La inflación reduce poder adquisitivo, las comisiones penalizan la rentabilidad neta y los impuestos afectan al beneficio final."
            ),

            html.H4("¿Qué rentabilidad anual debería usar?", style={"fontWeight": "800", "fontSize": "1.05rem", "marginTop": "16px"}),
            html.P(
                "Lo más útil suele ser probar varios escenarios: uno conservador, uno base y uno más optimista. Así puedes evaluar cómo cambia el resultado final de tu inversión según distintos supuestos."
            ),

            html.H4("¿Cuál es la mejor calculadora de interés compuesto?", style={"fontWeight": "800", "fontSize": "1.05rem", "marginTop": "16px"}),
            html.P(
                "La mejor calculadora será la que te permita modelizar no solo una inversión inicial, sino también aportaciones periódicas, inflación, comisiones e impuestos. "
                "Eso ofrece una visión bastante más útil que una simulación demasiado simple."
            )
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
            trust_block(),
            article_preview_block(),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div(id="simulador", style={"scrollMarginTop": "90px"}),
                            html.Div("Configura tu simulación", style=SECTION_TITLE_STYLE),

                            dbc.Row([
                                dbc.Col(dbc.Button("Conservador", id="preset-conservador", color="light", className="w-100"), md=4),
                                dbc.Col(dbc.Button("Base", id="preset-base", color="light", className="w-100"), md=4),
                                dbc.Col(dbc.Button("Dinámico", id="preset-dinamico", color="light", className="w-100"), md=4),
                            ], className="g-2 mb-3"),

                            input_block(
                                "Inversión inicial (€)",
                                dbc.Input(
                                    id="monto-inicial",
                                    type="text",
                                    inputMode="decimal",
                                    value="10000",
                                    placeholder="Ej: 10.000",
                                    style=INPUT_STYLE
                                )
                            ),
                            input_block(
                                "Aportación periódica (€)",
                                dbc.Input(
                                    id="deposito",
                                    type="text",
                                    inputMode="decimal",
                                    value="300",
                                    placeholder="Ej: 300 o 1.000",
                                    style=INPUT_STYLE
                                )
                            ),
                            input_block(
                                "Rentabilidad anual esperada (%)",
                                dbc.Input(
                                    id="tasa",
                                    type="text",
                                    inputMode="decimal",
                                    value="7",
                                    placeholder="Ej: 7 o 7,5",
                                    style=INPUT_STYLE
                                )
                            ),
                            input_block(
                                "Duración (años)",
                                dbc.Input(id="anos", type="number", min=1, step=1, value=20, style=INPUT_STYLE)
                            ),

                            dbc.Accordion([
                                dbc.AccordionItem([
                                    input_block(
                                        "Comisión anual (%)",
                                        dbc.Input(
                                            id="comision",
                                            type="text",
                                            inputMode="decimal",
                                            value="0.20",
                                            placeholder="Ej: 0,20",
                                            style=INPUT_STYLE
                                        )
                                    ),
                                    input_block(
                                        "Inflación anual (%)",
                                        dbc.Input(
                                            id="inflacion",
                                            type="text",
                                            inputMode="decimal",
                                            value="2.5",
                                            placeholder="Ej: 2,5",
                                            style=INPUT_STYLE
                                        )
                                    ),
                                    input_block(
                                        "Impuestos sobre plusvalías (%)",
                                        dbc.Input(
                                            id="impuestos",
                                            type="text",
                                            inputMode="decimal",
                                            value="19",
                                            placeholder="Ej: 19",
                                            style=INPUT_STYLE
                                        )
                                    ),
                                    input_block(
                                        "Crecimiento anual de aportación (%)",
                                        dbc.Input(
                                            id="crec-aporte",
                                            type="text",
                                            inputMode="decimal",
                                            value="0",
                                            placeholder="Ej: 1,5",
                                            style=INPUT_STYLE
                                        )
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
            ]),

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
                                            dbc.Button("Probar la calculadora", color="primary", size="lg", className="me-2"),
                                            href="/",
                                            style={"textDecoration": "none"}
                                        ),
                                        html.A(
                                            dbc.Button("Ver MyInvestor", color="success", size="lg"),
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
                                                "Prueba ahora la calculadora y descubre cuánto podría crecer tu dinero con aportaciones mensuales, "
                                                "inflación, impuestos y comisiones.",
                                                style={"color": COLOR_MUTED}
                                            ),
                                            html.Div([
                                                html.A(
                                                    dbc.Button("Ir a la calculadora", color="primary", size="lg", className="me-2"),
                                                    href="/",
                                                    style={"textDecoration": "none"}
                                                ),
                                                html.A(
                                                    dbc.Button("Abrir MyInvestor", color="success", size="lg"),
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
                                "Usa la calculadora para ver números reales según tu caso.",
                                style={"color": COLOR_MUTED}
                            ),
                            html.A(
                                dbc.Button("Abrir calculadora", color="primary", className="w-100 mb-2"),
                                href="/",
                                style={"textDecoration": "none"}
                            ),
                            html.A(
                                dbc.Button("Ver MyInvestor", color="success", className="w-100"),
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

        const el = document.getElementById("simulador");
        if (el) {
            const yOffset = 20;
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
# RESULTADOS
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
            html.P(insight, style={"color": COLOR_MUTED, "marginBottom": "0"})
        ]),
        style={**CARD_STYLE, "marginBottom": "18px"}
    )

    comparativa_box = dbc.Card(
        dbc.CardBody([
            html.Div(id="comparativa", style={"scrollMarginTop": "90px"}),
            html.H4("¿Qué pasa si aportas 100 €, 300 € o 500 €?", style={"fontWeight": "800", "marginBottom": "14px"}),
            html.P(
                "Este bloque ayuda mucho a convertir porque deja claro el impacto real de subir la aportación periódica.",
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

        cta_card(),
        email_capture_block(),
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
        <meta name="description" content="Informe generado por la calculadora de interés compuesto con aportaciones mensuales.">
        <title>Calculadora de interés compuesto gratis - Informe</title>
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
