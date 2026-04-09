import dash
from dash import html
import dash_bootstrap_components as dbc

from components.disclaimer_afiliados import build_disclaimer

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/myinvestor-opiniones",
    title="MyInvestor opiniones (2026): análisis real",
    name="MyInvestor opiniones",
    description=(
        "Opiniones reales de MyInvestor: ventajas, desventajas y si merece la pena en 2026. "
        "Análisis completo para invertir en España."
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
            "MyInvestor opiniones (2026): ¿merece la pena o no?",
            className="fw-bold mb-3",
        ),

        html.Div("Actualizado 2026", className="text-muted small mb-3"),

        p(
            "MyInvestor es uno de los neobancos más populares en España para invertir en fondos indexados. "
            "Pero la pregunta clave es: ¿realmente merece la pena o hay mejores opciones?"
        ),

        p(
            "En este análisis te doy una opinión real, con ventajas, desventajas y para quién es buena opción."
        ),

        section("Qué es MyInvestor"),

        p(
            "MyInvestor es un neobanco español enfocado en inversión, creado por Andbank España "
            "y supervisado por el Banco de España y la CNMV. :contentReference[oaicite:0]{index=0}"
        ),

        p(
            "Esto significa que no es una app cualquiera: es una entidad regulada y con garantía "
            "de depósitos hasta 100.000€."
        ),

        highlight(
            "Es una de las plataformas más utilizadas en España para invertir en fondos indexados",
            "success",
        ),

        section("Ventajas de MyInvestor"),

        html.Ul(
            [
                html.Li("Comisiones muy bajas o inexistentes en fondos"),
                html.Li("Acceso a fondos indexados (Vanguard, etc.)"),
                html.Li("Cuenta remunerada sin comisiones"),
                html.Li("Inversión desde cantidades muy bajas"),
                html.Li("Plataforma 100% online"),
            ]
        ),

        p(
            "Uno de sus puntos fuertes es que permite invertir con costes muy reducidos, "
            "algo clave para el largo plazo. :contentReference[oaicite:1]{index=1}"
        ),

        section("Desventajas reales"),

        html.Ul(
            [
                html.Li("Atención al cliente mejorable"),
                html.Li("Problemas técnicos ocasionales"),
                html.Li("App no siempre estable"),
                html.Li("Procesos lentos en algunos casos"),
            ]
        ),

        p(
            "Muchos usuarios destacan problemas con el soporte o incidencias técnicas, "
            "especialmente cuando la plataforma crece. :contentReference[oaicite:2]{index=2}"
        ),

        section("Opiniones reales de usuarios"),

        highlight(
            "La experiencia es mixta: muy buena en costes, peor en soporte",
            "warning",
        ),

        p(
            "Algunos usuarios valoran la facilidad para invertir y las comisiones bajas, "
            "mientras que otros critican la atención al cliente o incidencias con la app. :contentReference[oaicite:3]{index=3}"
        ),

        section("¿Para quién es buena opción?"),

        html.Ul(
            [
                html.Li("Principiantes que quieren invertir fácil"),
                html.Li("Personas que buscan fondos indexados"),
                html.Li("Inversores a largo plazo"),
            ]
        ),

        section("¿Para quién NO es ideal?"),

        html.Ul(
            [
                html.Li("Traders activos"),
                html.Li("Usuarios que necesitan soporte rápido"),
                html.Li("Personas que buscan herramientas avanzadas"),
            ]
        ),

        section("Conclusión: ¿merece la pena?"),

        highlight(
            "Sí, pero con matices",
            "success",
        ),

        p(
            "MyInvestor es una de las mejores opciones en España para empezar a invertir, "
            "especialmente en fondos indexados."
        ),

        p(
            "Sin embargo, no es perfecta, y su mayor punto débil suele ser la atención al cliente."
        ),

        cta(
            "Abrir cuenta en MyInvestor",
            "Si quieres empezar a invertir con fondos indexados, puedes hacerlo aquí.",
            "Abrir cuenta",
            MYINVESTOR_AFFILIATE_URL,
            external=True,
        ),

        build_disclaimer(),

        section("Alternativa: simula antes de invertir"),

        p(
            "Antes de invertir, lo mejor que puedes hacer es simular diferentes escenarios."
        ),

        cta(
            "Simular inversión",
            "Descubre cuánto puedes ganar según tu ahorro mensual.",
            "Abrir calculadora",
            "/calculadora",
        ),
    ]
)
