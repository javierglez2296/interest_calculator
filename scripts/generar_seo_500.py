import os
import re
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "pages" / "seo"

SITE_NAME = "interescompuesto.app"


def slugify(text: str) -> str:
    text = text.lower()
    replacements = {
        "€": "euros",
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "ñ": "n",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def build_article(slug, title, category, intro, h2_1, h2_2, cta_url="/calculadora"):
    return f'''import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path="/{slug}",
    title="{title} | {SITE_NAME}",
    name="{title}",
    description="{intro[:155]}",
)

layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.Div("{category}", className="text-uppercase text-muted fw-bold mt-4 mb-2"),
                    html.H1("{title}", className="fw-bold mb-3"),
                    html.P("{intro}", className="lead"),

                    html.H2("{h2_1}", className="fw-bold mt-5"),
                    html.P(
                        "El interés compuesto permite que tu dinero crezca no solo por tus aportaciones, "
                        "sino también por los intereses generados con el paso del tiempo. Cuanto mayor sea "
                        "el plazo, mayor suele ser el efecto acumulado."
                    ),

                    html.H2("{h2_2}", className="fw-bold mt-5"),
                    html.P(
                        "Para hacer una estimación realista conviene tener en cuenta la aportación mensual, "
                        "la rentabilidad esperada, la inflación, los impuestos y el horizonte temporal."
                    ),

                    html.Div(
                        [
                            html.H3("Simula tu caso exacto", className="fw-bold"),
                            html.P("Usa la calculadora gratuita para ver números adaptados a tu situación."),
                            dbc.Button("Ir a la calculadora", href="{cta_url}", color="primary"),
                        ],
                        className="p-4 bg-light rounded-4 my-5",
                    ),

                    html.H2("Preguntas frecuentes", className="fw-bold mt-5"),

                    html.H3("¿Qué rentabilidad anual es razonable usar?"),
                    html.P(
                        "Depende del activo. Para una cartera indexada global muchas simulaciones usan escenarios "
                        "prudentes, medios y optimistas en lugar de una única cifra fija."
                    ),

                    html.H3("¿Es mejor invertir poco tiempo o mucho dinero?"),
                    html.P(
                        "Lo ideal es combinar ambas cosas, pero empezar pronto ayuda mucho porque aumenta el número "
                        "de años en los que el capital puede crecer."
                    ),

                    html.H3("¿Puedo perder dinero invirtiendo?"),
                    html.P(
                        "Sí. Toda inversión con rentabilidad esperada tiene riesgo. Por eso conviene diversificar, "
                        "invertir a largo plazo y no usar dinero que puedas necesitar a corto plazo."
                    ),

                    html.Hr(className="my-5"),

                    html.H2("También te puede interesar", className="fw-bold"),
                    html.Ul(
                        [
                            html.Li(html.A("Calculadora de interés compuesto", href="/calculadora")),
                            html.Li(html.A("Calculadora FIRE", href="/fire")),
                            html.Li(html.A("Calculadora de hipoteca", href="/hipoteca")),
                            html.Li(html.A("Rentabilidad de alquiler", href="/rentabilidad-alquiler")),
                            html.Li(html.A("Comparador de inversión", href="/comparador")),
                        ]
                    ),
                ],
                lg=9,
            )
        )
    ],
    fluid=True,
)
'''


def generate_keywords():
    articles = []

    amounts = [50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 800, 1000, 1200, 1500, 2000]
    years = [5, 10, 15, 20, 25, 30, 35, 40]

    for amount in amounts:
        for year in years:
            title = f"Interés compuesto con {amount}€ al mes durante {year} años"
            articles.append({
                "title": title,
                "category": "Interés compuesto",
                "intro": f"Calcula cuánto podrías acumular invirtiendo {amount}€ al mes durante {year} años con interés compuesto.",
                "h2_1": f"Ejemplo invirtiendo {amount}€ al mes",
                "h2_2": f"Qué tener en cuenta a {year} años",
                "cta_url": "/calculadora",
            })

    initial_amounts = [1000, 2000, 5000, 10000, 15000, 20000, 30000, 50000, 75000, 100000]
    for initial in initial_amounts:
        for year in years:
            title = f"Interés compuesto con {initial}€ iniciales durante {year} años"
            articles.append({
                "title": title,
                "category": "Interés compuesto",
                "intro": f"Simula cuánto podrían crecer {initial}€ invertidos durante {year} años gracias al interés compuesto.",
                "h2_1": f"Ejemplo con {initial}€ iniciales",
                "h2_2": f"Resultado potencial a {year} años",
                "cta_url": "/calculadora",
            })

    fire_incomes = [1000, 1200, 1500, 1800, 2000, 2500, 3000, 4000]
    for income in fire_incomes:
        title = f"Cuánto dinero necesitas para vivir con {income}€ al mes"
        articles.append({
            "title": title,
            "category": "FIRE",
            "intro": f"Calcula el patrimonio aproximado necesario para generar {income}€ al mes y acercarte a la independencia financiera.",
            "h2_1": f"Patrimonio necesario para {income}€ mensuales",
            "h2_2": "Factores que cambian el resultado",
            "cta_url": "/fire",
        })

    mortgage_prices = [150000, 200000, 250000, 300000, 350000, 400000, 450000, 500000]
    for price in mortgage_prices:
        title = f"Hipoteca para una vivienda de {price}€"
        articles.append({
            "title": title,
            "category": "Hipoteca",
            "intro": f"Estima la cuota, entrada necesaria e impuestos aproximados al comprar una vivienda de {price}€.",
            "h2_1": f"Cuota aproximada para una vivienda de {price}€",
            "h2_2": "Gastos que debes tener en cuenta",
            "cta_url": "/hipoteca",
        })

    rents = [600, 700, 800, 900, 1000, 1200, 1500, 1800, 2000]
    prices = [100000, 150000, 200000, 250000, 300000, 400000]
    for rent in rents:
        for price in prices:
            title = f"Rentabilidad de alquilar un piso de {price}€ por {rent}€ al mes"
            articles.append({
                "title": title,
                "category": "Rentabilidad alquiler",
                "intro": f"Analiza si comprar un piso de {price}€ para alquilarlo por {rent}€ al mes puede ser rentable.",
                "h2_1": "Rentabilidad bruta estimada",
                "h2_2": "Gastos que reducen la rentabilidad real",
                "cta_url": "/rentabilidad-alquiler",
            })

    investment_topics = [
        "invertir en fondos indexados",
        "invertir en S&P 500",
        "invertir en Nasdaq 100",
        "invertir en mercados emergentes",
        "invertir en oro",
        "invertir en fondos monetarios",
        "invertir para la jubilación",
        "invertir con poco dinero",
        "invertir a largo plazo",
        "invertir para vivir de rentas",
    ]

    for topic in investment_topics:
        for year in [10, 20, 30]:
            title = f"{topic.capitalize()} durante {year} años"
            articles.append({
                "title": title,
                "category": "Inversión",
                "intro": f"Guía práctica para entender qué puede pasar si decides {topic} durante {year} años.",
                "h2_1": "Ventajas de invertir a largo plazo",
                "h2_2": "Riesgos y escenarios posibles",
                "cta_url": "/comparador",
            })

    return articles[:500]


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    articles = generate_keywords()

    for article in articles:
        slug = slugify(article["title"])
        file_path = OUTPUT_DIR / f"{slug}.py"

        content = build_article(
            slug=slug,
            title=article["title"],
            category=article["category"],
            intro=article["intro"],
            h2_1=article["h2_1"],
            h2_2=article["h2_2"],
            cta_url=article["cta_url"],
        )

        file_path.write_text(content, encoding="utf-8")

    print(f"✅ Generadas {len(articles)} páginas SEO en {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
