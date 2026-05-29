import json

import dash
from dash import html, dcc

dash.register_page(__name__, path_template="/hipoteca-<importe>-euros")

SITE_URL = "https://interescompuesto.app"


def calcular_cuota(capital, interes_anual=3.0, anos=30):
    capital = max(float(capital or 0), 0)
    interes_anual = max(float(interes_anual or 0), 0)
    anos = max(int(anos or 0), 0)

    r = interes_anual / 100 / 12
    n = anos * 12

    if n <= 0:
        return 0

    if r == 0:
        return capital / n

    return capital * (r * (1 + r) ** n) / ((1 + r) ** n - 1)


def format_eur(value):
    return f"{float(value):,.0f} €".replace(",", ".")


def faq_schema(importe):
    cuota_30 = calcular_cuota(importe, 3.0, 30)

    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"¿Cuánto se paga al mes por una hipoteca de {format_eur(importe)}?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": (
                        f"La cuota mensual de una hipoteca de {format_eur(importe)} depende del plazo y del tipo de interés. "
                        f"Por ejemplo, a 30 años y con un interés del 3%, la cuota aproximada sería de {format_eur(cuota_30)} al mes."
                    ),
                },
            },
            {
                "@type": "Question",
                "name": f"¿Cuántos intereses se pagan por una hipoteca de {format_eur(importe)}?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": (
                        "Los intereses totales dependen del plazo, del tipo de interés y de si se realizan amortizaciones anticipadas. "
                        "Cuanto mayor sea el plazo, mayor suele ser el coste total de intereses."
                    ),
                },
            },
            {
                "@type": "Question",
                "name": "¿Es mejor una hipoteca a 20, 25 o 30 años?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": (
                        "Una hipoteca a menor plazo suele tener una cuota mensual más alta, pero permite pagar menos intereses totales. "
                        "Una hipoteca a mayor plazo reduce la cuota mensual, aunque aumenta el coste total."
                    ),
                },
            },
        ],
    }


def breadcrumb_schema(importe):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": 1,
                "name": "Inicio",
                "item": SITE_URL,
            },
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Calculadora de hipoteca",
                "item": f"{SITE_URL}/hipoteca",
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": f"Hipoteca de {format_eur(importe)}",
                "item": f"{SITE_URL}/hipoteca-{int(importe)}-euros",
            },
        ],
    }


def layout(importe=None, **kwargs):
    try:
        importe = int(importe)
    except Exception:
        importe = 150000

    if importe <= 0:
        importe = 150000

    cuota_20 = calcular_cuota(importe, 3.0, 20)
    cuota_25 = calcular_cuota(importe, 3.0, 25)
    cuota_30 = calcular_cuota(importe, 3.0, 30)

    intereses_20 = cuota_20 * 20 * 12 - importe
    intereses_25 = cuota_25 * 25 * 12 - importe
    intereses_30 = cuota_30 * 30 * 12 - importe

    calculator_href = f"/hipoteca?capital={importe}&plazo=30&interes=3&entrada=20&gastos=10"

    title = f"Hipoteca de {format_eur(importe)}: cuota mensual, intereses y coste total"
    description = (
        f"Calcula cuánto pagarías al mes por una hipoteca de {format_eur(importe)} "
        f"a 20, 25 o 30 años. Comparativa de cuota, intereses y coste total."
    )

    return html.Main(
        className="seo-page",
        children=[
            html.Script(
                type="application/ld+json",
                children=json.dumps(faq_schema(importe), ensure_ascii=False),
            ),
            html.Script(
                type="application/ld+json",
                children=json.dumps(breadcrumb_schema(importe), ensure_ascii=False),
            ),

            html.Section(
                className="seo-hero",
                children=[
                    html.P("Calculadora de hipoteca", className="section_eyebrow"),
                    html.H1(title),
                    html.P(description, className="seo-lead"),
                    html.Div(
                        className="seo-cta-row",
                        children=[
                            dcc.Link(
                                "Calcular esta hipoteca",
                                href=calculator_href,
                                className="btn btn-primary",
                            ),
                            dcc.Link(
                                "Ver guía de hipotecas",
                                href="/blog/hipoteca",
                                className="btn btn-secondary",
                            ),
                        ],
                    ),
                ],
            ),

            html.Section(
                className="seo-card-grid",
                children=[
                    html.Div(
                        className="metric_card",
                        children=[
                            html.P("A 20 años"),
                            html.H3(format_eur(cuota_20)),
                            html.Span(f"Intereses aprox.: {format_eur(intereses_20)}"),
                        ],
                    ),
                    html.Div(
                        className="metric_card",
                        children=[
                            html.P("A 25 años"),
                            html.H3(format_eur(cuota_25)),
                            html.Span(f"Intereses aprox.: {format_eur(intereses_25)}"),
                        ],
                    ),
                    html.Div(
                        className="metric_card",
                        children=[
                            html.P("A 30 años"),
                            html.H3(format_eur(cuota_30)),
                            html.Span(f"Intereses aprox.: {format_eur(intereses_30)}"),
                        ],
                    ),
                ],
            ),

            html.Section(
                className="seo-content",
                children=[
                    html.H2(f"¿Cuánto cuesta una hipoteca de {format_eur(importe)}?"),
                    html.P(
                        f"Una hipoteca de {format_eur(importe)} puede tener cuotas muy distintas según el plazo elegido, "
                        "el tipo de interés, las comisiones y la evolución del euríbor si es variable. "
                        "Por eso conviene comparar varios escenarios antes de tomar una decisión."
                    ),

                    html.H2("Comparativa por plazo"),
                    html.Table(
                        className="seo-table",
                        children=[
                            html.Thead(
                                html.Tr(
                                    [
                                        html.Th("Plazo"),
                                        html.Th("Cuota mensual aprox."),
                                        html.Th("Intereses aprox."),
                                        html.Th("Coste total aprox."),
                                    ]
                                )
                            ),
                            html.Tbody(
                                [
                                    html.Tr(
                                        [
                                            html.Td("20 años"),
                                            html.Td(format_eur(cuota_20)),
                                            html.Td(format_eur(intereses_20)),
                                            html.Td(format_eur(cuota_20 * 20 * 12)),
                                        ]
                                    ),
                                    html.Tr(
                                        [
                                            html.Td("25 años"),
                                            html.Td(format_eur(cuota_25)),
                                            html.Td(format_eur(intereses_25)),
                                            html.Td(format_eur(cuota_25 * 25 * 12)),
                                        ]
                                    ),
                                    html.Tr(
                                        [
                                            html.Td("30 años"),
                                            html.Td(format_eur(cuota_30)),
                                            html.Td(format_eur(intereses_30)),
                                            html.Td(format_eur(cuota_30 * 30 * 12)),
                                        ]
                                    ),
                                ]
                            ),
                        ],
                    ),

                    html.Div(
                        className="seo-cta-inline",
                        children=[
                            html.H2(f"Calcula tu caso exacto para {format_eur(importe)}"),
                            html.P(
                                "Los números anteriores son una estimación rápida. Puedes abrir la calculadora completa ya precargada "
                                "con este importe, plazo de 30 años, entrada del 20% e interés del 3%."
                            ),
                            dcc.Link(
                                f"Calcular hipoteca de {format_eur(importe)}",
                                href=calculator_href,
                                className="btn btn-primary",
                            ),
                        ],
                    ),

                    html.H2("Preguntas frecuentes"),
                    html.H3(f"¿Cuánto se paga por una hipoteca de {format_eur(importe)}?"),
                    html.P(
                        f"Con un tipo orientativo del 3% a 30 años, la cuota aproximada sería de "
                        f"{format_eur(cuota_30)} al mes. La cifra real dependerá de las condiciones del banco."
                    ),

                    html.H3("¿Qué plazo conviene elegir?"),
                    html.P(
                        "Si eliges un plazo corto, pagarás más cuota mensual pero menos intereses. "
                        "Si eliges un plazo largo, la cuota será más baja, pero el coste total será mayor."
                    ),

                    html.H3("¿Cómo puedo calcular mi caso exacto?"),
                    html.P(
                        "Puedes usar la calculadora completa de hipoteca para modificar el importe, plazo, tipo de interés, "
                        "entrada inicial y otros supuestos."
                    ),

                    html.Div(
                        className="internal-links-box",
                        children=[
                            html.H2("También te puede interesar"),
                            html.Ul(
                                [
                                    html.Li(dcc.Link("Calculadora de hipoteca", href="/hipoteca")),
                                    html.Li(dcc.Link("Guía completa sobre hipotecas", href="/blog/hipoteca")),
                                    html.Li(dcc.Link("Rentabilidad de alquilar un piso", href="/rentabilidad-alquiler")),
                                    html.Li(dcc.Link("Comparador de inversión", href="/comparador")),
                                ]
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
