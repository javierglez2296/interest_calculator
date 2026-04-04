import json
from dash import html, register_page
import dash_bootstrap_components as dbc

register_page(
    __name__,
    path="/blog/hipoteca",
    name="Hipoteca artículo",
    title="Cómo calcular una hipoteca | interescompuesto.app",
    description="Aprende a calcular una hipoteca, entender la cuota mensual y evitar errores al comprar vivienda."
)

json_ld = {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Cómo calcular una hipoteca y no cometer errores al comprar vivienda",
    "description": "Guía básica para entender la cuota, los intereses y el coste real de una hipoteca.",
    "author": {
        "@type": "Person",
        "name": "interescompuesto.app"
    },
    "publisher": {
        "@type": "Organization",
        "name": "interescompuesto.app"
    },
    "mainEntityOfPage": "https://interescompuesto.app/blog/hipoteca"
}

layout = dbc.Container(
    [
        html.Script(type="application/ld+json", children=json.dumps(json_ld, ensure_ascii=False)),

        dbc.Row(
            dbc.Col(
                [
                    html.Div("Hipoteca · 8 min de lectura", className="text-muted mb-3"),
                    html.H1("Cómo calcular una hipoteca y no cometer errores al comprar vivienda", className="fw-bold mb-4"),
                    html.P(
                        "Cuando miras una vivienda, no basta con fijarse en el precio. Lo importante es entender cuánto capital vas a financiar, "
                        "qué cuota mensual asumirás y cuánto terminarás pagando realmente a lo largo de los años.",
                        className="lead"
                    ),
                ],
                lg=8
            ),
            className="pt-4 pt-md-5"
        ),

        dbc.Row(
            dbc.Col(
                [
                    html.H2("Los 4 datos básicos", className="h3 mb-3"),
                    html.Ul(
                        [
                            html.Li("Precio de compra."),
                            html.Li("Entrada que puedes aportar."),
                            html.Li("Tipo de interés."),
                            html.Li("Plazo del préstamo."),
                        ]
                    ),
                    html.P(
                        "Con esos datos puedes estimar la cuota mensual. Pero además debes sumar gastos iniciales como impuestos, notaría, gestoría "
                        "y otros costes asociados a la compra."
                    ),
                    html.H2("El error más común", className="h3 mt-4 mb-3"),
                    html.P(
                        "Muchas personas calculan solo si pueden pagar la cuota. Eso es importante, pero no suficiente. "
                        "También hay que mirar cuánto dinero total vas a inmovilizar en entrada y gastos, y cuánto pagarás en intereses."
                    ),
                    html.H2("Qué cuota suele ser prudente", className="h3 mt-4 mb-3"),
                    html.P(
                        "Como referencia general, suele recomendarse que la cuota no consuma más del 30% al 35% de los ingresos netos del hogar. "
                        "Aun así, esto depende de tu estabilidad laboral, ahorro previo y otros gastos fijos."
                    ),
                    html.H2("Hipoteca fija o variable", className="h3 mt-4 mb-3"),
                    html.P(
                        "La fija da estabilidad porque sabes lo que pagarás cada mes. La variable puede empezar más baja o más alta según el momento, "
                        "pero asumes incertidumbre futura."
                    ),
                    html.P(
                        "Si estás comparando opciones, conviene simular varios escenarios y no quedarte solo con la oferta inicial del banco."
                    ),
                    html.H2("Conclusión", className="h3 mt-4 mb-3"),
                    html.P(
                        "Comprar vivienda no es solo una decisión emocional, también financiera. Hacer números antes de firmar puede evitar errores caros "
                        "durante muchos años. Usa la calculadora de hipoteca para tener una estimación clara y realista."
                    ),
                ],
                lg=8
            ),
            className="pb-5"
        )
    ],
    fluid=True,
    className="py-2 px-3 px-md-4 px-lg-5"
)
