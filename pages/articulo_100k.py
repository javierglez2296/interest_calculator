import dash
from dash import html
import dash_bootstrap_components as dbc

from components.disclaimer_afiliados import build_disclaimer

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/cuanto-genera-100000-euros",
    title="Cuánto genera 100.000€ al mes y al año (2026)",
    name="Cuánto genera 100.000€",
    description=(
        "Descubre cuánto dinero pueden generar 100.000€ invertidos al mes y al año. "
        "Ejemplos reales con distintas rentabilidades."
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


def rendimiento_table():
    rows = [
        ("1%", "1.000€", "83€"),
        ("3%", "3.000€", "250€"),
        ("5%", "5.000€", "416€"),
        ("7%", "7.000€", "583€"),
        ("8%", "8.000€", "666€"),
    ]

    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Rentabilidad"),
                        html.Th("Anual"),
                        html.Th("Mensual"),
                    ]
                )
            ),
            html.Tbody(
                [html.Tr([html.Td(r), html.Td(a), html.Td(m)]) for r, a, m in rows]
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
            "Cuánto genera 100.000€ al año y al mes (invertidos)",
            className="fw-bold mb-3",
        ),

        html.Div("Actualizado 2026", className="text-muted small mb-3"),

        p(
            "Tener 100.000€ ahorrados es un gran paso. Pero la pregunta clave es: "
            "¿cuánto dinero puedes generar con ese capital si lo inviertes?"
        ),

        p(
            "La respuesta depende de la rentabilidad, pero hay rangos bastante realistas "
            "que te pueden servir como referencia."
        ),

        section("Resultados rápidos"),

        highlight(
            "100.000€ pueden generar entre 250€ y 600€ al mes aproximadamente",
            "success",
        ),

        p(
            "Esto dependerá del tipo de inversión y del riesgo que estés dispuesto a asumir."
        ),

        section("Tabla de rentabilidad"),

        rendimiento_table(),

        section("Qué significa esto en la práctica"),

        p(
            "Si inviertes 100.000€ con una rentabilidad del 5%, podrías generar unos "
            "5.000€ al año, es decir, unos 416€ al mes."
        ),

        p(
            "Con una rentabilidad del 7%, esa cifra subiría a unos 583€ mensuales."
        ),

        section("¿Se puede vivir con 100.000€?"),

        p(
            "En la mayoría de casos, no. 100.000€ es una base muy buena, pero normalmente "
            "no es suficiente para cubrir todos los gastos mensuales."
        ),

        highlight(
            "Para vivir de rentas necesitarías aproximadamente entre 300.000€ y 600.000€",
            "warning",
        ),

        cta(
            "Calcula cuánto necesitas tú",
            "Descubre tu número exacto para vivir de rentas.",
            "Ir a calculadora FIRE",
            "/fire",
        ),

        section("Cómo hacer crecer esos 100.000€"),

        p(
            "La clave no es solo generar ingresos, sino hacer crecer ese capital con el tiempo."
        ),

        p(
            "Reinvertir beneficios y seguir aportando puede multiplicar el resultado a largo plazo."
        ),

        cta(
            "Simula el crecimiento de tu dinero",
            "Mira cuánto podrían convertirse esos 100.000€ en 10, 20 o 30 años.",
            "Abrir calculadora",
            "/calculadora",
        ),

        section("Dónde invertir en España"),

        p(
            "Para invertir de forma sencilla y con bajas comisiones, necesitas una buena plataforma."
        ),

        cta(
            "Empieza a invertir",
            "Abre cuenta y empieza a sacar rentabilidad a tu dinero.",
            "Abrir cuenta en MyInvestor",
            MYINVESTOR_AFFILIATE_URL,
            external=True,
        ),

        build_disclaimer(),

        section("Errores comunes"),

        html.Ul(
            [
                html.Li("Dejar el dinero parado en el banco"),
                html.Li("Buscar rentabilidades irreales"),
                html.Li("No diversificar"),
                html.Li("Invertir sin estrategia"),
            ]
        ),

        section("Conclusión"),

        p(
            "100.000€ pueden generar ingresos interesantes, pero su verdadero potencial "
            "está en el largo plazo."
        ),

        p(
            "Invertir bien ese capital puede ser el punto de partida hacia la independencia financiera."
        ),

        cta(
            "Calcula tu plan",
            "Descubre cuánto puedes generar y cómo llegar a tu objetivo.",
            "Ir a calculadora",
            "/calculadora",
        ),
    ]
)
