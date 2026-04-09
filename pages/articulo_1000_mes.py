import dash
from dash import html
import dash_bootstrap_components as dbc

from components.disclaimer_afiliados import build_disclaimer

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/invertir-para-ganar-1000-al-mes",
    title="Cuánto necesitas invertir para ganar 1.000€ al mes (2026)",
    name="Ganar 1000€ al mes",
    description=(
        "Descubre cuánto dinero necesitas invertir para generar 1.000€ al mes. "
        "Ejemplos reales y simulación paso a paso."
    ),
)


# =========================================================
# HELPERS
# =========================================================
def container(children):
    return dbc.Container(
        children,
        class_name="py-4",
        style={"maxWidth": "850px"},
    )


def section(title):
    return html.H2(title, className="fw-bold mt-5 mb-3")


def p(text):
    return html.P(text, style={"fontSize": "1.08rem", "lineHeight": "1.8"})


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


def table():
    rows = [
        ("500€", "6.000€", "150.000€"),
        ("1.000€", "12.000€", "300.000€"),
        ("1.500€", "18.000€", "450.000€"),
        ("2.000€", "24.000€", "600.000€"),
    ]

    return dbc.Table(
        [
            html.Thead(html.Tr([html.Th("Ingreso mensual"), html.Th("Anual"), html.Th("Capital necesario")])),
            html.Tbody(
                [html.Tr([html.Td(a), html.Td(b), html.Td(c)]) for a, b, c in rows]
            ),
        ],
        hover=True,
        responsive=True,
        class_name="mb-4",
    )


# =========================================================
# LAYOUT
# =========================================================
layout = container(
    [
        html.H1(
            "Cuánto necesitas invertir para ganar 1.000€ al mes",
            className="fw-bold mb-3",
        ),

        html.Div("Actualizado 2026", className="text-muted small mb-3"),

        p(
            "Ganar 1.000€ al mes con inversiones es uno de los objetivos más comunes. "
            "La pregunta es: ¿cuánto dinero necesitas realmente para conseguirlo?"
        ),

        p(
            "La respuesta depende de la rentabilidad, pero hay una regla simple que te da "
            "una aproximación bastante realista."
        ),

        section("La regla clave"),

        p(
            "Si quieres generar ingresos pasivos de forma sostenible, puedes usar una "
            "retirada aproximada del 4% anual."
        ),

        dbc.Alert(
            "Capital necesario = ingresos anuales ÷ 0,04",
            color="primary",
            class_name="fw-bold",
        ),

        p(
            "Si quieres ganar 1.000€ al mes, necesitas generar 12.000€ al año."
        ),

        dbc.Alert(
            "👉 Necesitas aproximadamente 300.000€ invertidos",
            color="success",
            class_name="fw-bold",
        ),

        section("Tabla rápida"),

        table(),

        section("¿Es realista conseguirlo?"),

        p(
            "Sí. No necesitas tener ese dinero hoy. Puedes construirlo con el tiempo "
            "mediante inversión constante."
        ),

        p(
            "Ejemplo real: si inviertes 500€ al mes durante 25-30 años, podrías "
            "acercarte mucho a ese objetivo."
        ),

        cta(
            "Calcula cuánto puedes acumular",
            "Usa la calculadora para ver cuánto dinero tendrás según tu ahorro mensual.",
            "Abrir calculadora",
            "/calculadora",
        ),

        section("Cómo invertir para conseguirlo"),

        p(
            "La estrategia más utilizada es invertir en fondos indexados diversificados "
            "a largo plazo."
        ),

        p(
            "Históricamente, mercados como el S&P 500 han dado rentabilidades cercanas al 7% anual."
        ),

        section("Dónde invertir en España"),

        p(
            "Para empezar necesitas una plataforma sencilla y con bajas comisiones."
        ),

        cta(
            "Empieza a invertir",
            "Puedes abrir cuenta fácilmente y empezar con pequeñas cantidades.",
            "Abrir cuenta en MyInvestor",
            MYINVESTOR_AFFILIATE_URL,
            external=True,
        ),

        build_disclaimer(),

        section("Errores comunes"),

        html.Ul(
            [
                html.Li("Pensar que necesitas millones"),
                html.Li("No invertir y solo ahorrar"),
                html.Li("Empezar tarde"),
                html.Li("No ser constante"),
            ]
        ),

        section("Conclusión"),

        p(
            "Ganar 1.000€ al mes es alcanzable con una estrategia correcta. "
            "La clave es empezar cuanto antes y mantener la constancia."
        ),

        cta(
            "Calcula tu objetivo ahora",
            "Descubre cuánto necesitas y cuánto tardarás.",
            "Ir a calculadora FIRE",
            "/fire",
        ),
    ]
)
