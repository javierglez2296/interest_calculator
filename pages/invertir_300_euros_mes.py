import dash
from dash import html
import dash_bootstrap_components as dbc

from components.disclaimer_afiliados import build_disclaimer

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/invertir-300-euros-mes",
    title="Invertir 300 euros al mes: cuánto puedes ganar en 10, 20 y 30 años",
    name="Invertir 300 euros al mes",
    description=(
        "Descubre cuánto puedes acumular invirtiendo 300€ al mes con interés compuesto. "
        "Ejemplos reales a 10, 20 y 30 años y cómo empezar paso a paso."
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
            "Invertir 300 euros al mes: cuánto puedes ganar en 10, 20 y 30 años",
            className="fw-bold mb-3",
        ),

        html.Div("Actualizado 2026", className="text-muted small mb-3"),

        p(
            "Invertir 300 euros al mes puede parecer una cantidad modesta, "
            "pero con el tiempo y el interés compuesto puede convertirse en un patrimonio muy relevante."
        ),

        p(
            "Muchas personas creen que para invertir hace falta empezar con grandes cantidades. "
            "La realidad es que lo más importante suele ser la constancia, el tiempo y mantener una estrategia sencilla."
        ),

        highlight(
            "Con 300€/mes, una rentabilidad media del 7% y 30 años por delante, podrías superar los 350.000€",
            "success",
        ),

        section("Cuánto puedes acumular invirtiendo 300€ al mes"),

        p(
            "Vamos a ver un ejemplo sencillo y realista para entender el potencial de una aportación mensual de 300 euros."
        ),

        html.Ul(
            [
                html.Li("Aportación mensual: 300€"),
                html.Li("Rentabilidad media anual: 7%"),
                html.Li("Plazo de inversión: 30 años"),
            ]
        ),

        p(
            "Con estas hipótesis, el resultado aproximado supera los 350.000 euros."
        ),

        p(
            "Lo más interesante es que no todo ese capital sale de tu bolsillo. "
            "En 30 años habrías aportado 108.000€, y el resto sería crecimiento generado por la inversión."
        ),

        highlight(
            "El interés compuesto hace que una parte muy importante del resultado final venga del crecimiento acumulado, no solo de tus aportaciones",
            "primary",
        ),

        cta(
            "Calcula tu caso exacto",
            "No todos los escenarios son iguales. Prueba con tus años, aportaciones y rentabilidad.",
            "Abrir calculadora",
            "/calculadora",
        ),

        section("Qué pasa en 10, 20 y 30 años"),

        p(
            "Una de las mejores formas de entender el interés compuesto es ver cómo evoluciona el patrimonio con el tiempo."
        ),

        html.Ul(
            [
                html.Li("En 10 años: alrededor de 52.000€"),
                html.Li("En 20 años: alrededor de 156.000€"),
                html.Li("En 30 años: alrededor de 365.000€"),
            ]
        ),

        p(
            "Los primeros años el crecimiento parece lento, y eso hace que muchas personas infravaloren el largo plazo."
        ),

        p(
            "Sin embargo, a partir de cierto punto el patrimonio empieza a crecer mucho más rápido. "
            "Ese efecto bola de nieve es una de las grandes ventajas de empezar cuanto antes."
        ),

        section("Por qué 300 euros al mes pueden marcar la diferencia"),

        p(
            "300 euros al mes no te harán rico de un día para otro, pero sí pueden cambiar de forma importante tu situación financiera futura."
        ),

        p(
            "La clave está en que se trata de una cantidad asumible para muchas personas, "
            "lo que hace más fácil mantenerla durante años."
        ),

        p(
            "En inversión a largo plazo, ser constante suele ser más importante que intentar encontrar la inversión perfecta o el mejor momento para entrar."
        ),

        section("Qué rentabilidad puedes esperar"),

        p(
            "Nadie puede garantizar una rentabilidad futura exacta, pero para hacer simulaciones puedes trabajar con escenarios prudentes."
        ),

        html.Ul(
            [
                html.Li("Escenario conservador: 5%"),
                html.Li("Escenario base: 6%–7%"),
                html.Li("Escenario optimista: 8%"),
            ]
        ),

        p(
            "Para una cartera diversificada de largo plazo, usar un 6% o un 7% como hipótesis suele ser razonable para hacer números sin caer en expectativas exageradas."
        ),

        section("Dónde invertir 300 euros al mes"),

        p(
            "Si estás empezando, no necesitas productos complicados. Las opciones más habituales para invertir 300 euros al mes son:"
        ),

        html.Ul(
            [
                html.Li("Fondos indexados"),
                html.Li("ETFs"),
                html.Li("Robo-advisors"),
            ]
        ),

        p(
            "Lo importante suele ser mantener costes bajos, tener una buena diversificación y automatizar las aportaciones."
        ),

        p(
            "Para muchas personas que invierten en España, una de las puertas de entrada más conocidas para empezar con fondos indexados es MyInvestor."
        ),

        cta(
            "Empezar a invertir",
            "Si quieres ver una opción para invertir en indexados y empezar con aportaciones periódicas, puedes revisar MyInvestor.",
            "Abrir cuenta",
            MYINVESTOR_AFFILIATE_URL,
            external=True,
        ),

        build_disclaimer(),

        section("Qué pasa si empiezas antes"),

        p(
            "El tiempo es uno de los factores más poderosos en cualquier estrategia de inversión."
        ),

        p(
            "No es lo mismo empezar con 25 años que con 35. "
            "Aunque la aportación mensual sea la misma, una década adicional puede suponer una diferencia enorme en el resultado final."
        ),

        highlight(
            "Empezar antes suele tener más impacto que intentar exprimir una rentabilidad algo mayor",
            "warning",
        ),

        section("Errores comunes al invertir cada mes"),

        html.Ul(
            [
                html.Li("Esperar al momento perfecto para empezar"),
                html.Li("Dejar de invertir cuando el mercado cae"),
                html.Li("Cambiar de estrategia constantemente"),
                html.Li("Pensar demasiado en el corto plazo"),
                html.Li("No tener en cuenta comisiones"),
            ]
        ),

        p(
            "Muchas veces el principal enemigo del inversor no es el mercado, sino la falta de constancia."
        ),

        p(
            "Una estrategia simple, diversificada y mantenida en el tiempo suele funcionar mejor que intentar hacer movimientos perfectos."
        ),

        section("Cómo empezar paso a paso"),

        html.Ul(
            [
                html.Li("Define una cantidad mensual sostenible"),
                html.Li("Elige una plataforma o entidad para invertir"),
                html.Li("Selecciona una cartera simple y diversificada"),
                html.Li("Automatiza la aportación mensual"),
                html.Li("Mantén la estrategia durante años"),
            ]
        ),

        p(
            "Automatizar es especialmente útil porque reduce la fricción y evita depender de la motivación de cada mes."
        ),

        section("Conclusión: ¿merece la pena invertir 300 euros al mes?"),

        highlight(
            "Sí: 300 euros al mes pueden convertirse en una base muy sólida para construir patrimonio a largo plazo",
            "success",
        ),

        p(
            "Invertir 300 euros al mes no parece espectacular al principio, pero puede dar resultados muy importantes cuando lo mantienes durante 10, 20 o 30 años."
        ),

        p(
            "La combinación de tiempo, constancia e interés compuesto es mucho más potente de lo que la mayoría imagina."
        ),

        p(
            "Si quieres ver cuánto podrías acumular según tu caso concreto, lo mejor es hacer una simulación personalizada."
        ),

        cta(
            "Simular inversión",
            "Descubre cuánto puedes acumular según tu ahorro mensual, rentabilidad, inflación y plazo.",
            "Abrir calculadora",
            "/calculadora",
        ),
    ]
)
