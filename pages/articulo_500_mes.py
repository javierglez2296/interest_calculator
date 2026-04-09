import dash
from dash import html
import dash_bootstrap_components as dbc

from components.disclaimer_afiliados import build_disclaimer

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/invertir-500-euros-al-mes-30-anos",
    title="Si inviertes 500€ al mes durante 30 años (resultado real)",
    name="Invertir 500€ al mes",
    description=(
        "Descubre cuánto dinero puedes acumular invirtiendo 500€ al mes durante 30 años. "
        "Simulación real con interés compuesto."
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


def scenario_table():
    rows = [
        ("0%", "180.000€"),
        ("3%", "291.000€"),
        ("5%", "416.000€"),
        ("7%", "567.000€"),
        ("8%", "680.000€"),
    ]

    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Rentabilidad"),
                        html.Th("Capital final (30 años)"),
                    ]
                )
            ),
            html.Tbody(
                [html.Tr([html.Td(r), html.Td(v)]) for r, v in rows]
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
            "Si inviertes 500€ al mes durante 30 años: esto es lo que pasa",
            className="fw-bold mb-3",
        ),

        html.Div("Actualizado 2026", className="text-muted small mb-3"),

        p(
            "Invertir 500€ al mes puede parecer poco, pero con el paso del tiempo "
            "y el efecto del interés compuesto, el resultado puede ser sorprendente."
        ),

        p(
            "En este artículo vas a ver exactamente cuánto dinero podrías tener "
            "después de 30 años, con diferentes escenarios de rentabilidad."
        ),

        section("El dato clave (esto cambia todo)"),

        highlight(
            "500€ al mes durante 30 años = 180.000€ aportados"
        ),

        p(
            "Es decir, sin invertir, solo ahorrando, tendrías 180.000€. "
            "Pero la inversión cambia completamente el resultado."
        ),

        section("Qué pasa si inviertes ese dinero"),

        highlight(
            "Con una rentabilidad del 7% anual podrías llegar a ~567.000€",
            "success",
        ),

        scenario_table(),

        p(
            "La diferencia entre no invertir y hacerlo puede ser de cientos de miles de euros."
        ),

        section("Por qué ocurre esto"),

        p(
            "El interés compuesto hace que tus ganancias generen nuevas ganancias. "
            "Al principio el crecimiento es lento, pero con los años se acelera mucho."
        ),

        p(
            "Por eso empezar antes es mucho más importante que invertir grandes cantidades más tarde."
        ),

        cta(
            "Simula tu caso real",
            "Cambia la cantidad mensual, los años y la rentabilidad para ver tu escenario exacto.",
            "Abrir calculadora",
            "/calculadora",
        ),

        section("¿Y si empiezas 5 años más tarde?"),

        p(
            "Retrasar el inicio tiene un impacto enorme. No son solo 5 años menos, "
            "es perder los años donde el interés compuesto más crece."
        ),

        highlight(
            "Empezar tarde puede costarte más de 100.000€ en el largo plazo",
            "danger",
        ),

        section("Cómo invertir esos 500€ al mes"),

        p(
            "La forma más habitual es invertir en fondos indexados diversificados "
            "a largo plazo."
        ),

        p(
            "Esto permite capturar el crecimiento del mercado sin necesidad de seleccionar acciones."
        ),

        section("Dónde invertir en España"),

        p(
            "Necesitas una plataforma sencilla, con bajas comisiones y fácil de usar."
        ),

        cta(
            "Empieza a invertir",
            "Abre cuenta y empieza con aportaciones mensuales desde hoy.",
            "Abrir cuenta en MyInvestor",
            MYINVESTOR_AFFILIATE_URL,
            external=True,
        ),

        build_disclaimer(),

        section("Errores comunes"),

        html.Ul(
            [
                html.Li("Pensar que 500€ es poco"),
                html.Li("Esperar el momento perfecto"),
                html.Li("No ser constante"),
                html.Li("Asustarse con caídas del mercado"),
            ]
        ),

        section("Conclusión"),

        p(
            "Invertir 500€ al mes puede marcar una diferencia enorme en tu futuro financiero. "
            "La clave no es la cantidad inicial, sino el tiempo y la constancia."
        ),

        cta(
            "Calcula cuánto tendrás tú",
            "Descubre tu escenario exacto en menos de un minuto.",
            "Ir a calculadora",
            "/calculadora",
        ),
    ]
)
