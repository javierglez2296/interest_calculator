import dash
from dash import html
import dash_bootstrap_components as dbc

from components.disclaimer_afiliados import build_disclaimer

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/mejor-cuenta-remunerada-espana",
    title="Mejor cuenta remunerada en España (2026)",
    name="Cuenta remunerada",
    description=(
        "Descubre las mejores cuentas remuneradas en España en 2026. "
        "Comparativa real, ventajas y cómo elegir la mejor opción."
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
                        html.Th("Entidad"),
                        html.Th("Rentabilidad"),
                        html.Th("Liquidez"),
                        html.Th("Ideal para"),
                    ]
                )
            ),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td("MyInvestor"),
                            html.Td("~2-3%"),
                            html.Td("Alta"),
                            html.Td("Ahorradores + inversores"),
                        ]
                    ),
                    html.Tr(
                        [
                            html.Td("Bancos tradicionales"),
                            html.Td("~0-1%"),
                            html.Td("Alta"),
                            html.Td("Conservadores"),
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
            "Mejor cuenta remunerada en España (2026)",
            className="fw-bold mb-3",
        ),

        html.Div("Actualizado 2026", className="text-muted small mb-3"),

        p(
            "Si tienes dinero parado en el banco, probablemente estés perdiendo rentabilidad. "
            "Las cuentas remuneradas permiten generar intereses sin asumir riesgo."
        ),

        p(
            "En este artículo te explico cuál es la mejor opción en España ahora mismo "
            "y cómo elegir la más adecuada según tu situación."
        ),

        section("Qué es una cuenta remunerada"),

        p(
            "Es una cuenta bancaria que te paga intereses por el dinero que tienes depositado."
        ),

        html.Ul(
            [
                html.Li("Sin riesgo de mercado"),
                html.Li("Liquidez total"),
                html.Li("Rentabilidad baja pero estable"),
            ]
        ),

        section("Mejores cuentas remuneradas en España"),

        comparison_table(),

        section("La mejor opción ahora mismo"),

        highlight(
            "Para la mayoría de usuarios, MyInvestor es una de las opciones más interesantes",
            "success",
        ),

        p(
            "Destaca por combinar cuenta remunerada con acceso a inversión en fondos indexados."
        ),

        html.Ul(
            [
                html.Li("Buena rentabilidad frente a bancos tradicionales"),
                html.Li("Sin comisiones"),
                html.Li("Ideal para empezar a invertir"),
            ]
        ),

        cta(
            "Abrir cuenta remunerada",
            "Puedes abrir cuenta gratis y empezar a generar intereses desde hoy.",
            "Abrir cuenta en MyInvestor",
            MYINVESTOR_AFFILIATE_URL,
            external=True,
        ),

        build_disclaimer(),

        section("¿Cuenta remunerada o invertir?"),

        p(
            "Las cuentas remuneradas son útiles, pero tienen una limitación: "
            "la rentabilidad es baja."
        ),

        highlight(
            "Para hacer crecer tu dinero de verdad necesitas invertir",
            "warning",
        ),

        p(
            "Por eso muchas personas combinan ambas estrategias."
        ),

        section("Estrategia recomendada"),

        html.Ul(
            [
                html.Li("Parte en cuenta remunerada (seguridad)"),
                html.Li("Parte en fondos indexados (crecimiento)"),
            ]
        ),

        cta(
            "Simula tu estrategia",
            "Descubre cuánto puedes ganar combinando ahorro e inversión.",
            "Abrir calculadora",
            "/calculadora",
        ),

        section("Errores comunes"),

        html.Ul(
            [
                html.Li("Dejar todo el dinero en cuentas sin remuneración"),
                html.Li("Buscar rentabilidades irreales"),
                html.Li("No comparar opciones"),
            ]
        ),

        section("Conclusión"),

        p(
            "Una cuenta remunerada es un buen primer paso, pero no debería ser tu única estrategia."
        ),

        p(
            "La combinación de ahorro e inversión es lo que realmente marca la diferencia."
        ),

        cta(
            "Empieza ahora",
            "Abre cuenta y empieza a sacar rendimiento a tu dinero.",
            "Abrir cuenta",
            MYINVESTOR_AFFILIATE_URL,
            external=True,
        ),
    ]
)
