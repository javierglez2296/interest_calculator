import dash
from dash import html
import dash_bootstrap_components as dbc

from components.disclaimer_afiliados import build_disclaimer

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/mejor-broker-espana",
    title="Mejor broker para invertir en España (2026)",
    name="Mejor broker España",
    description=(
        "Descubre cuál es el mejor broker para invertir en España en 2026. "
        "Comparativa real, comisiones y cuál elegir según tu perfil."
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
                        html.Th("Broker"),
                        html.Th("Comisiones"),
                        html.Th("Tipo inversor"),
                        html.Th("Lo mejor"),
                    ]
                )
            ),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td("MyInvestor"),
                            html.Td("Muy bajas"),
                            html.Td("Indexados"),
                            html.Td("Fondos sin comisión"),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Td("Trade Republic"),
                            html.Td("Muy bajas"),
                            html.Td("Acciones/ETFs"),
                            html.Td("Simplicidad"),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Td("DEGIRO"),
                            html.Td("Bajas"),
                            html.Td("Intermedio"),
                            html.Td("Variedad"),
                        ]
                    ),
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
            "Mejor broker para invertir en España (2026)",
            className="fw-bold mb-3",
        ),

        html.Div("Actualizado 2026", className="text-muted small mb-3"),

        p(
            "Elegir un buen broker es una de las decisiones más importantes cuando empiezas a invertir. "
            "Las comisiones, la facilidad de uso y los productos disponibles pueden marcar una gran diferencia."
        ),

        p(
            "En esta guía te explico cuál es el mejor broker en España según tu perfil y qué opción elegir."
        ),

        section("Qué debes tener en cuenta"),

        html.Ul(
            [
                html.Li("Comisiones"),
                html.Li("Facilidad de uso"),
                html.Li("Productos disponibles"),
                html.Li("Seguridad"),
            ]
        ),

        section("Mejores brokers en España"),

        comparison_table(),

        section("Mejor broker para empezar"),

        highlight(
            "Para la mayoría de usuarios, empezar con una plataforma simple es la mejor decisión",
            "success",
        ),

        p(
            "Si quieres invertir en fondos indexados, una de las opciones más utilizadas es MyInvestor."
        ),

        html.Ul(
            [
                html.Li("Fondos indexados sin comisión"),
                html.Li("Fácil de usar"),
                html.Li("Ideal para largo plazo"),
            ]
        ),

        cta(
            "Empieza a invertir",
            "Abre cuenta y empieza con fondos indexados fácilmente.",
            "Abrir cuenta en MyInvestor",
            MYINVESTOR_AFFILIATE_URL,
            external=True,
        ),

        build_disclaimer(),

        section("Alternativa para acciones y ETFs"),

        p(
            "Si prefieres invertir en acciones o ETFs, plataformas como Trade Republic o DEGIRO "
            "pueden ser más adecuadas."
        ),

        highlight(
            "No hay un único mejor broker, depende de lo que quieras hacer",
            "warning",
        ),

        section("Estrategia recomendada"),

        html.Ul(
            [
                html.Li("Principiantes → fondos indexados"),
                html.Li("Intermedios → ETFs"),
                html.Li("Avanzados → acciones individuales"),
            ]
        ),

        cta(
            "Simula tu inversión",
            "Descubre cuánto puedes ganar con el tiempo.",
            "Abrir calculadora",
            "/calculadora",
        ),

        section("Errores comunes"),

        html.Ul(
            [
                html.Li("Elegir por moda"),
                html.Li("No mirar comisiones"),
                html.Li("Cambiar constantemente de broker"),
            ]
        ),

        section("Conclusión"),

        p(
            "Elegir un buen broker es el primer paso para invertir bien. "
            "Empieza con una opción sencilla y mejora con el tiempo."
        ),

        cta(
            "Empieza ahora",
            "Abre cuenta y da el primer paso.",
            "Abrir cuenta",
            MYINVESTOR_AFFILIATE_URL,
            external=True,
        ),
    ]
)
