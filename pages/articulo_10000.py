import dash
from dash import html
import dash_bootstrap_components as dbc

from components.disclaimer_afiliados import build_disclaimer

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/donde-invertir-10000-euros",
    title="Dónde invertir 10.000€ en España (2026)",
    name="Invertir 10.000€",
    description=(
        "Descubre dónde invertir 10.000€ en España paso a paso. "
        "Opciones reales según tu perfil y objetivos."
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


# =========================================================
# LAYOUT
# =========================================================
layout = container(
    [
        html.H1(
            "Dónde invertir 10.000€ en España (guía realista)",
            className="fw-bold mb-3",
        ),

        html.Div("Actualizado 2026", className="text-muted small mb-3"),

        p(
            "Tener 10.000€ ahorrados es una gran oportunidad. "
            "La diferencia entre dejar ese dinero parado o invertirlo bien puede ser enorme en unos años."
        ),

        p(
            "En esta guía vas a ver las mejores opciones reales en España, según tu perfil "
            "y sin complicaciones innecesarias."
        ),

        section("La clave antes de invertir"),

        highlight(
            "No existe una única mejor inversión. Depende de tu plazo, riesgo y objetivos."
        ),

        p(
            "Antes de decidir dónde invertir, debes tener claro:"
        ),

        html.Ul(
            [
                html.Li("Cuándo vas a necesitar el dinero"),
                html.Li("Cuánto riesgo estás dispuesto a asumir"),
                html.Li("Si vas a seguir aportando dinero"),
            ]
        ),

        section("Opción 1: Fondos indexados (la más recomendable)"),

        p(
            "Para la mayoría de personas, la mejor opción es invertir en fondos indexados "
            "diversificados a largo plazo."
        ),

        p(
            "Ventajas:"
        ),

        html.Ul(
            [
                html.Li("Bajas comisiones"),
                html.Li("Diversificación global"),
                html.Li("No necesitas conocimientos avanzados"),
                html.Li("Históricamente ~6-7% anual"),
            ]
        ),

        highlight(
            "Ideal si tu horizonte es de 5+ años",
            "success",
        ),

        cta(
            "Empieza a invertir fácilmente",
            "Puedes invertir en fondos indexados desde España sin complicaciones.",
            "Abrir cuenta en MyInvestor",
            MYINVESTOR_AFFILIATE_URL,
            external=True,
        ),

        section("Opción 2: Cuenta remunerada (bajo riesgo)"),

        p(
            "Si no quieres asumir riesgo, puedes usar una cuenta remunerada."
        ),

        p(
            "Ventajas:"
        ),

        html.Ul(
            [
                html.Li("Sin volatilidad"),
                html.Li("Liquidez total"),
                html.Li("Rentabilidad baja pero segura"),
            ]
        ),

        highlight(
            "Ideal para corto plazo o fondo de emergencia",
            "warning",
        ),

        section("Opción 3: Inversión combinada (la mejor estrategia)"),

        p(
            "Una de las mejores decisiones es combinar varias opciones."
        ),

        html.Ul(
            [
                html.Li("70% fondos indexados"),
                html.Li("30% liquidez o cuenta remunerada"),
            ]
        ),

        p(
            "Esto te permite crecer a largo plazo sin asumir todo el riesgo."
        ),

        section("¿Cuánto puedes ganar con 10.000€?"),

        p(
            "Depende de la rentabilidad:"
        ),

        html.Ul(
            [
                html.Li("3% → 300€/año"),
                html.Li("5% → 500€/año"),
                html.Li("7% → 700€/año"),
            ]
        ),

        cta(
            "Simula tu inversión",
            "Descubre cuánto pueden crecer tus 10.000€ con el tiempo.",
            "Abrir calculadora",
            "/calculadora",
        ),

        section("Errores comunes"),

        html.Ul(
            [
                html.Li("Dejar el dinero parado"),
                html.Li("Buscar pelotazos rápidos"),
                html.Li("Invertir sin estrategia"),
                html.Li("No diversificar"),
            ]
        ),

        section("Conclusión"),

        p(
            "Invertir 10.000€ bien puede ser el inicio de algo mucho mayor. "
            "La clave es empezar, mantener la constancia y pensar a largo plazo."
        ),

        cta(
            "Calcula tu plan",
            "Descubre cuánto puedes acumular con el tiempo.",
            "Ir a calculadora FIRE",
            "/fire",
        ),

        build_disclaimer(),
    ]
)
