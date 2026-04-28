import os
import re
import unicodedata
from textwrap import dedent

OUTPUT_DIR = "pages/blog"
CALCULADORA_URL = "/rentabilidad-alquiler"
COMPARADOR_URL = "/comparador"
HIPOTECA_URL = "/hipoteca"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def slugify(text):
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def py_safe_name(slug):
    return slug.replace("-", "_")


ARTICULOS = [
    # Ciudades
    ("Madrid", "ciudad"),
    ("Barcelona", "ciudad"),
    ("Valencia", "ciudad"),
    ("Sevilla", "ciudad"),
    ("Málaga", "ciudad"),
    ("Zaragoza", "ciudad"),
    ("Bilbao", "ciudad"),
    ("Alicante", "ciudad"),
    ("Murcia", "ciudad"),
    ("Valladolid", "ciudad"),
    ("Santander", "ciudad"),
    ("A Coruña", "ciudad"),
    ("Granada", "ciudad"),
    ("Córdoba", "ciudad"),
    ("Toledo", "ciudad"),

    # Precios
    ("100.000 euros", "precio"),
    ("150.000 euros", "precio"),
    ("200.000 euros", "precio"),
    ("250.000 euros", "precio"),
    ("300.000 euros", "precio"),
    ("350.000 euros", "precio"),
    ("400.000 euros", "precio"),
    ("500.000 euros", "precio"),

    # Hipoteca / perfil
    ("con hipoteca", "perfil"),
    ("sin hipoteca", "perfil"),
    ("con 50.000 euros ahorrados", "perfil"),
    ("con 100.000 euros ahorrados", "perfil"),
    ("con 1.000 euros de alquiler", "perfil"),
    ("con cashflow positivo", "perfil"),
    ("con tipos al 3%", "perfil"),
    ("con tipos al 4%", "perfil"),

    # Comparativas
    ("comprar piso o invertir en bolsa", "comparativa"),
    ("vivienda o S&P 500", "comparativa"),
    ("alquiler o fondos indexados", "comparativa"),
    ("inmobiliario u oro", "comparativa"),
    ("comprar piso o dejar el dinero en monetarios", "comparativa"),
    ("comprar vivienda o invertir cada mes", "comparativa"),

    # Preguntas long tail
    ("cuánto se gana alquilando un piso", "pregunta"),
    ("qué rentabilidad neta debe tener un alquiler", "pregunta"),
    ("cuándo merece la pena comprar para alquilar", "pregunta"),
    ("qué gastos tiene un piso alquilado", "pregunta"),
    ("cómo calcular rentabilidad real alquiler", "pregunta"),
    ("qué impuestos se pagan al comprar una vivienda", "pregunta"),
    ("qué es mejor amortizar hipoteca o invertir", "pregunta"),
    ("cuánto hay que pagar de ITP al comprar piso", "pregunta"),
    ("cómo afecta el IRPF al alquiler", "pregunta"),
    ("qué es el cashflow inmobiliario", "pregunta"),
    ("cómo comparar alquiler frente a bolsa", "pregunta"),
    ("qué mirar antes de comprar un piso para alquilar", "pregunta"),
    ("rentabilidad alquiler en España 2026", "pregunta"),
]


def build_title(topic, tipo):
    if tipo == "ciudad":
        return f"Rentabilidad alquiler en {topic} en 2026: ¿merece la pena comprar?"
    if tipo == "precio":
        return f"Rentabilidad de un piso de {topic}: ¿cuánto se gana realmente?"
    if tipo == "perfil":
        return f"¿Es rentable comprar un piso para alquilar {topic}?"
    if tipo == "comparativa":
        return f"¿Qué es mejor: {topic}?"
    return topic.capitalize()


def build_article(topic, tipo):
    title = build_title(topic, tipo)
    slug = slugify(title)

    if tipo == "ciudad":
        intro = f"Comprar un piso para alquilar en {topic} puede parecer una inversión sencilla, pero la rentabilidad real depende del precio de compra, el alquiler esperado, los gastos, los impuestos y la financiación."
        h2 = f"Cómo analizar una inversión en alquiler en {topic}"
        body = f"""
        Para calcular si un piso en {topic} merece la pena, no basta con dividir el alquiler anual entre el precio de compra.

        Hay que tener en cuenta:

        - precio de compra
        - impuestos de compra
        - reforma inicial
        - IBI
        - comunidad
        - seguro
        - mantenimiento
        - posibles meses sin alquilar
        - IRPF sobre el alquiler
        - hipoteca, si existe

        Una vivienda puede parecer rentable en bruto, pero dejar de serlo cuando se añaden todos los gastos reales.
        """

    elif tipo == "precio":
        intro = f"Un piso de {topic} puede parecer una buena oportunidad, pero la clave está en saber cuánto alquiler puede generar y qué gastos reales soporta."
        h2 = f"Ejemplo de rentabilidad para un piso de {topic}"
        body = f"""
        En una inversión inmobiliaria, el precio de compra no es el único coste. Además del precio del inmueble, hay que sumar impuestos, notaría, registro, reforma y gastos recurrentes.

        Por eso, un piso de {topic} puede tener una rentabilidad muy diferente según la ciudad, el alquiler esperado y el estado del inmueble.

        La rentabilidad bruta suele parecer atractiva, pero la rentabilidad neta es la que realmente importa.
        """

    elif tipo == "perfil":
        intro = f"Comprar un piso para alquilar {topic} puede mejorar la rentabilidad, pero también puede aumentar el riesgo si los números no están bien calculados."
        h2 = f"Qué tener en cuenta al invertir {topic}"
        body = f"""
        Antes de comprar, conviene revisar si el alquiler cubre los gastos, si el cashflow mensual es positivo y si la operación supera el coste de oportunidad frente a otras inversiones.

        En especial, debes mirar:

        - desembolso inicial
        - cuota hipotecaria
        - gastos anuales
        - impuestos
        - rentabilidad sobre capital aportado
        - cashflow mensual
        - comparación frente a bolsa o fondos indexados
        """

    elif tipo == "comparativa":
        intro = f"La comparación entre {topic} depende de rentabilidad, riesgo, liquidez, fiscalidad y tiempo de gestión."
        h2 = f"Cómo comparar correctamente {topic}"
        body = f"""
        La vivienda ofrece apalancamiento, ingresos por alquiler y posible revalorización. Pero también exige gestión, gastos, impuestos y menor liquidez.

        La inversión financiera suele ser más pasiva y diversificada, aunque también tiene volatilidad.

        La decisión correcta depende de los números reales, no de intuiciones.
        """

    else:
        intro = f"{topic.capitalize()} es una de las dudas más habituales antes de invertir en vivienda para alquilar."
        h2 = "Cómo calcularlo correctamente"
        body = """
        Para responder bien, hay que analizar ingresos, gastos, impuestos, financiación, ocupación esperada y coste de oportunidad.

        Muchos inversores se quedan solo con la rentabilidad bruta, pero la rentabilidad neta y el cashflow mensual son mucho más importantes.
        """

    description = (
        f"{title}. Calcula rentabilidad bruta, neta, cashflow, impuestos, hipoteca "
        "y compara vivienda frente al S&P 500."
    )

    content = f'''
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path="/{slug}",
    title="{title}",
    name="{title}",
    description="{description}",
)


def paragraph(text):
    return html.P(text, className="text-muted", style={{"fontSize": "1.05rem", "lineHeight": "1.75"}})


layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.Div(
                        "GUÍA INVERSIÓN INMOBILIARIA",
                        className="fw-bold mb-3",
                        style={{
                            "fontSize": "0.8rem",
                            "letterSpacing": "0.08em",
                            "textTransform": "uppercase",
                            "color": "#0d6efd",
                        }},
                    ),
                    html.H1(
                        "{title}",
                        className="fw-bold mb-4",
                        style={{
                            "fontSize": "clamp(2rem, 5vw, 3.5rem)",
                            "lineHeight": "1.05",
                            "letterSpacing": "-0.04em",
                        }},
                    ),
                    paragraph("{intro}"),
                    dbc.Alert(
                        [
                            html.Strong("Resumen rápido: "),
                            "no analices solo la rentabilidad bruta. Calcula rentabilidad neta, cashflow, impuestos y coste de oportunidad antes de comprar."
                        ],
                        color="primary",
                        className="rounded-4 my-4",
                    ),
                ],
                lg=9,
            ),
            class_name="py-5",
        ),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H2("{h2}", className="fw-bold mt-4 mb-3"),
                        *[paragraph(p.strip()) for p in """{body}""".strip().split("\\n\\n")],

                        html.H2("Rentabilidad bruta vs rentabilidad neta", className="fw-bold mt-5 mb-3"),
                        paragraph(
                            "La rentabilidad bruta solo tiene en cuenta el alquiler anual frente al precio de compra. "
                            "La rentabilidad neta descuenta gastos, impuestos, mantenimiento, comunidad, seguro, IBI y otros costes."
                        ),
                        paragraph(
                            "Por eso dos pisos con la misma rentabilidad bruta pueden tener resultados reales muy distintos."
                        ),

                        html.H2("El papel de los impuestos", className="fw-bold mt-5 mb-3"),
                        paragraph(
                            "Los impuestos de compra pueden cambiar mucho según la comunidad autónoma, el tipo de vivienda "
                            "y el país. En España no es lo mismo comprar en Madrid que en Cataluña, Valencia o Andalucía."
                        ),
                        paragraph(
                            "La versión PRO de la calculadora permite estimar impuestos por región y ver cómo afectan a la rentabilidad real."
                        ),

                        html.H2("Comparar vivienda frente a bolsa", className="fw-bold mt-5 mb-3"),
                        paragraph(
                            "Comprar para alquilar puede tener sentido si la rentabilidad neta, el cashflow y la revalorización esperada compensan "
                            "frente a una inversión más pasiva como un fondo indexado al S&P 500."
                        ),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H3("Calcula tu caso real", className="h4 fw-bold mb-3"),
                                    paragraph(
                                        "Introduce precio, alquiler, gastos, hipoteca e impuestos para ver si la operación realmente merece la pena."
                                    ),
                                    dbc.Button(
                                        "Usar calculadora de rentabilidad alquiler",
                                        href="{CALCULADORA_URL}",
                                        color="primary",
                                        className="rounded-pill px-4 fw-bold me-2 mb-2",
                                    ),
                                    dbc.Button(
                                        "Comparar con bolsa",
                                        href="{COMPARADOR_URL}",
                                        color="light",
                                        className="rounded-pill px-4 border mb-2",
                                    ),
                                ]
                            ),
                            className="border-0 shadow-sm rounded-4 my-5",
                        ),

                        html.H2("Conclusión", className="fw-bold mt-5 mb-3"),
                        paragraph(
                            "La clave no es saber si comprar para alquilar es bueno o malo en general. "
                            "La clave es analizar la operación concreta con todos los gastos, impuestos y alternativas sobre la mesa."
                        ),
                    ],
                    lg=8,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("Herramientas útiles", className="h5 fw-bold mb-3"),
                                html.Ul(
                                    [
                                        html.Li(dcc.Link("Calculadora rentabilidad alquiler", href="{CALCULADORA_URL}")),
                                        html.Li(dcc.Link("Calculadora hipoteca", href="{HIPOTECA_URL}")),
                                        html.Li(dcc.Link("Comparador de inversión", href="{COMPARADOR_URL}")),
                                    ],
                                    className="mb-0",
                                ),
                            ]
                        ),
                        className="border-0 shadow-sm rounded-4 sticky-top",
                        style={{"top": "90px"}},
                    ),
                    lg=4,
                ),
            ],
            class_name="pb-5",
        ),
    ],
    fluid=False,
)
'''
    return slug, content


for topic, tipo in ARTICULOS:
    title = build_title(topic, tipo)
    slug, content = build_article(topic, tipo)
    filename = f"{py_safe_name(slug)}.py"
    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(dedent(content).strip() + "\n")

    print(f"✅ Generado: /{slug}")

print(f"\nTotal artículos generados: {len(ARTICULOS)}")
print(f"Carpeta: {OUTPUT_DIR}")
