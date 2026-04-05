import json
from dash import html, register_page
import dash_bootstrap_components as dbc

register_page(
    __name__,
    path="/blog/cuanto-dinero-necesitas-vivir-de-rentas",
    name="Vivir de rentas",
    title="Cuánto dinero necesitas para vivir de rentas en España [2026]",
    description="Descubre cuánto dinero necesitas para vivir de rentas en España con ejemplos reales y estrategias."
)

# =========================================================
# ENLACES AFILIADOS (YA METIDOS)
# =========================================================
PADRE_RICO = "https://amzn.to/4tzZ9aB"
INVERSOR_INTELIGENTE = "https://amzn.to/4sQ3Lt1"
PSYCHOLOGY_MONEY = "https://amzn.to/4vc02Yt"

MYINVESTOR = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

# =========================================================
# COMPONENTE LIBRO
# =========================================================
def book_card(title, text, link):
    return dbc.Card(
        dbc.CardBody(
            [
                html.H3(title, className="h6 fw-bold mb-2"),
                html.P(text, className="text-muted small mb-3"),
                dbc.Button(
                    "Ver libro",
                    href=link,
                    target="_blank",
                    rel="sponsored noopener noreferrer",
                    color="dark",
                    className="w-100 rounded-pill fw-semibold",
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 h-100",
    )

# =========================================================
# LAYOUT
# =========================================================
layout = dbc.Container(
    [
        html.H1("💰 Cuánto dinero necesitas para vivir de rentas en España", className="fw-bold mb-4"),

        html.P(
            "Vivir de las rentas es uno de los objetivos financieros más buscados. "
            "Pero la pregunta clave es: ¿cuánto dinero necesitas realmente?"
        ),

        html.H2("📊 Regla del 4%", className="mt-4"),
        html.P(
            "Una de las formas más utilizadas para estimar el capital necesario es la regla del 4%. "
            "Consiste en retirar un 4% anual de tu patrimonio sin agotarlo a largo plazo."
        ),

        dbc.Alert(
            "Capital necesario = gastos anuales ÷ 0,04",
            color="light",
            className="rounded-4 border-0 fw-semibold",
        ),

        html.H3("Ejemplo real", className="mt-4"),
        html.Ul([
            html.Li("Gastos mensuales: 2.000€"),
            html.Li("Gastos anuales: 24.000€"),
            html.Li("Capital necesario: 600.000€"),
        ]),

        dbc.Button(
            "👉 Calcular mi número FIRE",
            href="/fire",
            color="primary",
            className="mt-3"
        ),

        # =========================================================
        # BLOQUE LIBROS (AQUÍ MONETIZAS)
        # =========================================================
        html.H2("📚 Libros recomendados para empezar", className="mt-5"),

        dbc.Row(
            [
                dbc.Col(
                    book_card(
                        "Padre Rico, Padre Pobre",
                        "El libro perfecto para cambiar tu mentalidad sobre dinero y activos.",
                        PADRE_RICO,
                    ),
                    md=4,
                    className="mb-3",
                ),
                dbc.Col(
                    book_card(
                        "El inversor inteligente",
                        "Referencia clásica para aprender a invertir con criterio.",
                        INVERSOR_INTELIGENTE,
                    ),
                    md=4,
                    className="mb-3",
                ),
                dbc.Col(
                    book_card(
                        "The Psychology of Money",
                        "Uno de los mejores libros para mejorar tu mentalidad financiera.",
                        PSYCHOLOGY_MONEY,
                    ),
                    md=4,
                    className="mb-3",
                ),
            ]
        ),

        html.H2("📈 Cómo llegar a ese capital", className="mt-5"),
        html.P(
            "La clave no es solo ahorrar, sino invertir de forma constante durante años."
        ),

        dbc.Button(
            "👉 Simular interés compuesto",
            href="/calculadora",
            color="dark",
            className="mt-3"
        ),

        html.H2("🚀 Empieza cuanto antes", className="mt-5"),
        html.P(
            "Cuanto antes empieces, más efecto tendrá el interés compuesto. "
            "El tiempo es el factor más importante."
        ),

        dbc.Alert(
            "💡 Puedes empezar hoy con plataformas reguladas y sin comisiones de mantenimiento.",
            color="light",
            className="mt-3"
        ),

        dbc.Button(
            "👉 Empezar a invertir",
            href=MYINVESTOR,
            color="success",
            className="mt-2"
        ),

        html.H2("⚠️ Errores comunes", className="mt-5"),
        html.Ul([
            html.Li("Subestimar gastos"),
            html.Li("No tener en cuenta inflación"),
            html.Li("No invertir de forma constante"),
            html.Li("Esperar demasiado para empezar"),
        ]),

        html.H2("📌 Conclusión", className="mt-5"),
        html.P(
            "Vivir de rentas es posible, pero requiere planificación, disciplina y tiempo. "
            "Lo importante es empezar cuanto antes y mantener la constancia."
        ),

        dbc.Button(
            "👉 Ver calculadora",
            href="/calculadora",
            color="primary",
            className="mt-3"
        ),
    ],
    className="py-5",
)
