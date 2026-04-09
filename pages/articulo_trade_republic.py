import dash
from dash import html
import dash_bootstrap_components as dbc

from components.disclaimer_afiliados import build_disclaimer

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/trade-republic-opiniones",
    title="Trade Republic opiniones (2026): análisis real",
    name="Trade Republic opiniones",
    description=(
        "Opiniones reales de Trade Republic en España: ventajas, desventajas y comparativa. "
        "¿Merece la pena o hay mejores opciones?"
    ),
)


# =========================================================
# HELPERS
# =========================================================
def container(children):
    return dbc.Container(
        children,
        class_name="py-4",
        style={"maxWidth": "900px"},
    )


def section(title):
    return html.H2(title, className="fw-bold mt-5 mb-3")


def p(text):
    return html.P(text, style={"fontSize": "1.08rem", "lineHeight": "1.8"})


def highlight(text, color="primary"):
    return dbc.Alert(text, color=color, class_name="fw-bold")


def cta(title, text, btn, href, external=False):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H4(title, className="fw-bold"),
                html.P(text, className="text-muted"),
                dbc.Button(
                    btn,
                    href=href,
                    color="primary",
                    class_name="rounded-pill px-4",
                    target="_blank" if external else None,
                    rel="sponsored noopener noreferrer" if external else None,
                ),
            ]
        ),
        class_name="my-4 shadow-sm border-0",
    )


# =========================================================
# LAYOUT
# =========================================================
layout = container(
    [
        html.H1(
            "Trade Republic opiniones (2026): ¿merece la pena en España?",
            className="fw-bold mb-3",
        ),

        html.Div("Actualizado 2026", className="text-muted small mb-3"),

        p(
            "Trade Republic es uno de los brokers más populares en Europa, especialmente "
            "para invertir en acciones y ETFs con bajas comisiones."
        ),

        p(
            "Pero la pregunta clave es: ¿realmente merece la pena en España o hay mejores opciones?"
        ),

        section("Qué es Trade Republic"),

        p(
            "Trade Republic es un broker alemán que permite invertir en acciones, ETFs y otros productos "
            "financieros desde el móvil con comisiones muy reducidas."
        ),

        highlight(
            "Se ha hecho popular por su simplicidad y bajas comisiones",
            "success",
        ),

        section("Ventajas de Trade Republic"),

        html.Ul(
            [
                html.Li("Comisiones muy bajas"),
                html.Li("Interfaz simple"),
                html.Li("Acceso a acciones y ETFs"),
                html.Li("Inversión desde pequeñas cantidades"),
            ]
        ),

        section("Desventajas reales"),

        html.Ul(
            [
                html.Li("No ideal para fondos indexados tradicionales"),
                html.Li("Menos variedad que otros brokers"),
                html.Li("Atención al cliente mejorable"),
                html.Li("Enfoque más limitado para largo plazo puro"),
            ]
        ),

        section("Opiniones reales"),

        highlight(
            "Buena opción para acciones y ETFs, pero no para todo el mundo",
            "warning",
        ),

        p(
            "Muchos usuarios valoran la simplicidad, pero otros buscan más herramientas "
            "o mejores opciones para inversión a largo plazo."
        ),

        section("¿Trade Republic o MyInvestor?"),

        highlight(
            "Son plataformas diferentes para objetivos diferentes",
            "primary",
        ),

        html.Ul(
            [
                html.Li("Trade Republic → acciones y ETFs"),
                html.Li("MyInvestor → fondos indexados"),
            ]
        ),

        p(
            "Si tu objetivo es invertir a largo plazo de forma sencilla, muchas personas "
            "prefieren usar fondos indexados."
        ),

        cta(
            "Alternativa para invertir a largo plazo",
            "Si buscas una estrategia más pasiva con fondos indexados, esta opción puede encajar mejor.",
            "Ver MyInvestor",
            MYINVESTOR_AFFILIATE_URL,
            external=True,
        ),

        build_disclaimer(),

        section("Cuál elegir según tu perfil"),

        html.Ul(
            [
                html.Li("Principiante → fondos indexados (MyInvestor)"),
                html.Li("Intermedio → ETFs"),
                html.Li("Avanzado → acciones"),
            ]
        ),

        section("Conclusión"),

        p(
            "Trade Republic es una buena opción si quieres invertir en acciones o ETFs "
            "de forma sencilla."
        ),

        p(
            "Sin embargo, si buscas una estrategia de largo plazo sin complicaciones, "
            "los fondos indexados suelen ser la opción más utilizada."
        ),

        cta(
            "Empieza a invertir",
            "Abre cuenta y empieza con una estrategia a largo plazo.",
            "Abrir cuenta en MyInvestor",
            MYINVESTOR_AFFILIATE_URL,
            external=True,
        ),

        section("Simula antes de decidir"),

        p(
            "Antes de invertir, lo mejor es ver números reales."
        ),

        cta(
            "Simular inversión",
            "Descubre cuánto puedes ganar según tu plan.",
            "Abrir calculadora",
            "/calculadora",
        ),
    ]
)
