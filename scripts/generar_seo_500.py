import os
import re
import json
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "pages" / "seo"

SITE_NAME = "interescompuesto.app"


def slugify(text: str) -> str:
    text = text.lower()
    replacements = {
        "€": "euros",
        "á": "a",
        "é": "e",
        "í": "i",
        "ó": "o",
        "ú": "u",
        "ñ": "n",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def build_related_links(category: str):
    links = [
        ("Calculadora de interés compuesto", "/calculadora"),
        ("Calculadora FIRE", "/fire"),
        ("Calculadora de hipoteca", "/hipoteca"),
        ("Rentabilidad de alquiler", "/rentabilidad-alquiler"),
        ("Comparador de inversión", "/comparador"),
    ]

    if category == "Interés compuesto":
        links += [
            ("Interés compuesto con 100€ al mes durante 20 años", "/interes-compuesto-con-100euros-al-mes-durante-20-anos"),
            ("Interés compuesto con 500€ al mes durante 30 años", "/interes-compuesto-con-500euros-al-mes-durante-30-anos"),
            ("Interés compuesto con 1000€ al mes durante 20 años", "/interes-compuesto-con-1000euros-al-mes-durante-20-anos"),
            ("Interés compuesto con 10.000€ iniciales durante 30 años", "/interes-compuesto-con-10000euros-iniciales-durante-30-anos"),
        ]

    elif category == "FIRE":
        links += [
            ("Cuánto dinero necesitas para vivir con 1000€ al mes", "/cuanto-dinero-necesitas-para-vivir-con-1000euros-al-mes"),
            ("Cuánto dinero necesitas para vivir con 2000€ al mes", "/cuanto-dinero-necesitas-para-vivir-con-2000euros-al-mes"),
            ("Cuánto dinero necesitas para vivir con 3000€ al mes", "/cuanto-dinero-necesitas-para-vivir-con-3000euros-al-mes"),
            ("Invertir para vivir de rentas durante 30 años", "/invertir-para-vivir-de-rentas-durante-30-anos"),
        ]

    elif category == "Hipoteca":
        links += [
            ("Hipoteca para una vivienda de 200.000€", "/hipoteca-para-una-vivienda-de-200000euros"),
            ("Hipoteca para una vivienda de 300.000€", "/hipoteca-para-una-vivienda-de-300000euros"),
            ("Hipoteca para una vivienda de 400.000€", "/hipoteca-para-una-vivienda-de-400000euros"),
            ("Vivienda vs bolsa", "/vivienda-vs-bolsa"),
        ]

    elif category == "Rentabilidad alquiler":
        links += [
            ("Rentabilidad de alquilar un piso de 150.000€ por 800€ al mes", "/rentabilidad-de-alquilar-un-piso-de-150000euros-por-800euros-al-mes"),
            ("Rentabilidad de alquilar un piso de 200.000€ por 1000€ al mes", "/rentabilidad-de-alquilar-un-piso-de-200000euros-por-1000euros-al-mes"),
            ("Rentabilidad de alquilar un piso de 300.000€ por 1200€ al mes", "/rentabilidad-de-alquilar-un-piso-de-300000euros-por-1200euros-al-mes"),
            ("Vivienda vs bolsa", "/vivienda-vs-bolsa"),
        ]

    elif category == "Inversión":
        links += [
            ("Invertir en fondos indexados durante 30 años", "/invertir-en-fondos-indexados-durante-30-anos"),
            ("Invertir en S&P 500 durante 30 años", "/invertir-en-s-p-500-durante-30-anos"),
            ("Invertir a largo plazo durante 30 años", "/invertir-a-largo-plazo-durante-30-anos"),
            ("Invertir para la jubilación durante 30 años", "/invertir-para-la-jubilacion-durante-30-anos"),
        ]

    return links


def build_faq_schema(title: str) -> str:
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "¿Qué rentabilidad anual es razonable usar?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": (
                        "Depende del tipo de inversión. Para simulaciones a largo plazo suele ser mejor "
                        "usar varios escenarios: conservador, medio y optimista."
                    ),
                },
            },
            {
                "@type": "Question",
                "name": "¿Es mejor empezar pronto o invertir más dinero después?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": (
                        "Empezar pronto suele ayudar mucho porque el interés compuesto necesita tiempo "
                        "para multiplicar el capital acumulado."
                    ),
                },
            },
            {
                "@type": "Question",
                "name": "¿Puedo perder dinero invirtiendo?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": (
                        "Sí. Toda inversión con rentabilidad esperada tiene riesgo. Por eso conviene "
                        "diversificar, invertir a largo plazo y no usar dinero necesario a corto plazo."
                    ),
                },
            },
            {
                "@type": "Question",
                "name": "¿Para qué sirve esta simulación?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": (
                        f"Esta simulación sirve para entender un escenario concreto relacionado con {title} "
                        "y compararlo con otros objetivos financieros."
                    ),
                },
            },
        ],
    }

    return json.dumps(schema, ensure_ascii=False)
    
def build_seo_title(title: str, category: str) -> str:
    if category == "Interés compuesto":
        return f"{title}: cuánto tendrías | {SITE_NAME}"

    if category == "FIRE":
        return f"{title}: calcula tu libertad financiera | {SITE_NAME}"

    if category == "Hipoteca":
        return f"{title}: cuota y gastos estimados | {SITE_NAME}"

    if category == "Rentabilidad alquiler":
        return f"{title}: rentabilidad real | {SITE_NAME}"

    if category == "Inversión":
        return f"{title}: simulación a largo plazo | {SITE_NAME}"

    return f"{title} | {SITE_NAME}"


def build_seo_description(title: str, category: str, intro: str) -> str:
    if category == "Interés compuesto":
        return f"{intro} Incluye ejemplo, factores clave y enlace a la calculadora para simular tu caso."

    if category == "FIRE":
        return f"{intro} Estima el capital necesario, escenarios y pasos para acercarte a vivir de tus inversiones."

    if category == "Hipoteca":
        return f"{intro} Revisa cuota, entrada, gastos de compra y factores que afectan al coste total."

    if category == "Rentabilidad alquiler":
        return f"{intro} Calcula rentabilidad bruta, gastos, cashflow y compara la vivienda con otras inversiones."

    if category == "Inversión":
        return f"{intro} Analiza ventajas, riesgos y escenarios frente a otras alternativas de inversión."

    return intro[:155]

def build_article(slug, title, category, intro, h2_1, h2_2, cta_url="/calculadora"):
    faq_schema = build_faq_schema(title)
    related_links = build_related_links(category)
    seo_title = build_seo_title(title, category)
    seo_description = build_seo_description(title, category, intro)

    related_links_code = ",\n                            ".join(
        [
            f'html.Li(html.A("{text}", href="{href}"))'
            for text, href in related_links
        ]
    )

    return f'''import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path="/{slug}",
    title="{seo_title}",
    description="{seo_description}",
)

layout = dbc.Container(
    [
        html.Script(
            type="application/ld+json",
            children={faq_schema!r}
        ),

        dbc.Row(
            dbc.Col(
                [
                    html.Div("{category}", className="text-uppercase text-muted fw-bold mt-4 mb-2"),
                    html.H1("{title}", className="fw-bold mb-3"),
                    html.P("{intro}", className="lead"),

                    html.P(
                        [
                            "Puedes hacer una simulación personalizada usando nuestra ",
                            html.A("calculadora de interés compuesto", href="/calculadora"),
                            ", revisar objetivos FIRE con la ",
                            html.A("calculadora FIRE", href="/fire"),
                            " o comparar alternativas con el ",
                            html.A("comparador de inversión", href="/comparador"),
                            "."
                        ],
                        className="mb-4",
                    ),

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

                    html.H3("¿Es mejor empezar pronto o invertir más dinero después?"),
                    html.P(
                        "Empezar pronto suele ayudar mucho porque el interés compuesto necesita tiempo para "
                        "multiplicar el capital acumulado."
                    ),

                    html.H3("¿Puedo perder dinero invirtiendo?"),
                    html.P(
                        "Sí. Toda inversión con rentabilidad esperada tiene riesgo. Por eso conviene diversificar, "
                        "invertir a largo plazo y no usar dinero que puedas necesitar a corto plazo."
                    ),

                    html.H3("¿Para qué sirve esta simulación?"),
                    html.P(
                        "Esta página sirve para analizar un escenario financiero concreto y compararlo con otras "
                        "opciones como fondos indexados, vivienda, ahorro mensual o independencia financiera."
                    ),

                    html.Hr(className="my-5"),

                    html.H2("Artículos relacionados", className="fw-bold"),
                    html.Ul(
                        [
                            {related_links_code}
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

    print(f"✅ Generadas {len(articles)} páginas SEO con FAQ schema e interlinking automático en {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
