import dash
from dash import html
import dash_bootstrap_components as dbc

from components.disclaimer_afiliados import build_disclaimer

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/trade-republic-vs-myinvestor",
    title="Trade Republic vs MyInvestor (2026): comparativa real",
    name="Trade vs MyInvestor",
    description=(
        "Comparativa real entre Trade Republic y MyInvestor en España. "
        "Descubre cuál es mejor según tu perfil de inversión."
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


def comparison_table():
    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Característica"),
                        html.Th("Trade Republic"),
                        html.Th("MyInvestor"),
                    ]
                )
            ),
            html.Tbody(
                [
                    html.Tr(["Tipo inversión", "Acciones / ETFs", "Fondos indexados"]),
                    html.Tr(["Comisiones", "Muy bajas", "Muy bajas"]),
                    html.Tr(["Facilidad", "Muy alta", "Alta"]),
                    html.Tr(["Estrategia ideal", "Activa / ETFs", "Largo plazo"]),
                    html.Tr(["Cuenta remunerada", "Sí", "Sí"]),
                ]
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
            "Trade Republic vs MyInvestor: cuál es mejor para invertir en 2026",
            className="fw-bold mb-3",
        ),

        html.Div("Actualizado 2026", className="text-muted small mb-3"),

        p(
            "Si estás empezando a invertir en España, es muy probable que hayas visto dos opciones: "
            "Trade Republic y MyInvestor."
        ),

        p(
            "Ambas plataformas son populares, pero sirven para cosas diferentes. "
            "Elegir bien puede marcar una gran diferencia en tus resultados."
        ),

        section("Comparativa rápida"),

        comparison_table(),

        section("Diferencia clave"),

        highlight(
            "Trade Republic y MyInvestor no compiten directamente: están pensados para estrategias distintas",
            "primary",
        ),

        html.Ul(
            [
                html.Li("Trade Republic → acciones y ETFs"),
                html.Li("MyInvestor → fondos indexados"),
            ]
        ),

        section("Cuándo elegir Trade Republic"),

        html.Ul(
            [
                html.Li("Quieres invertir en acciones"),
                html.Li("Prefieres ETFs"),
                html.Li("Te interesa operar desde el móvil"),
            ]
        ),

        section("Cuándo elegir MyInvestor"),

        html.Ul(
            [
                html.Li("Quieres invertir a largo plazo"),
                html.Li("Prefieres fondos indexados"),
                html.Li("Buscas estrategia simple"),
            ]
        ),

        highlight(
            "Para la mayoría de personas, la inversión a largo plazo con fondos indexados es la opción más utilizada",
            "success",
        ),

        cta(
            "Empieza con fondos indexados",
            "Si buscas una estrategia sencilla y a largo plazo, esta es la opción más recomendada.",
            "Abrir cuenta en MyInvestor",
            MYINVESTOR_AFFILIATE_URL,
            external=True,
        ),

        build_disclaimer(),

        section("Qué opción es mejor para principiantes"),

        p(
            "Para la mayoría de personas que empiezan, lo más importante es la simplicidad."
        ),

        highlight(
            "Menos decisiones = mejores resultados a largo plazo",
            "warning",
        ),

        p(
            "Por eso muchas personas prefieren empezar con fondos indexados en lugar de elegir acciones individuales."
        ),

        section("Estrategia recomendada"),

        html.Ul(
            [
                html.Li("Empieza con fondos indexados"),
                html.Li("Invierte de forma mensual"),
                html.Li("Mantén la estrategia a largo plazo"),
            ]
        ),

        cta(
            "Simula tu inversión",
            "Descubre cuánto puedes ganar con una estrategia simple.",
            "Abrir calculadora",
            "/calculadora",
        ),

        section("Conclusión"),

        p(
            "Trade Republic y MyInvestor son buenas opciones, pero no para lo mismo."
        ),

        p(
            "Si buscas simplicidad y largo plazo, los fondos indexados suelen ser la opción más recomendable."
        ),

        cta(
            "Empieza ahora",
            "Abre cuenta y da el primer paso en inversión.",
            "Abrir cuenta",
            MYINVESTOR_AFFILIATE_URL,
            external=True,
        ),
    ]
)
