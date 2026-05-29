import json
import dash
from dash import html, dcc


dash.register_page(__name__, path_template="/invertir-<aportacion>-euros-al-mes")


SITE_URL = "https://interescompuesto.app"
RENTABILIDAD_BASE = 7
INFLACION_BASE = 2
COMISION_BASE = 0.2
HORIZONTE_BASE = 30
CAPITAL_INICIAL_BASE = 0


APORTACIONES_RECOMENDADAS = [100, 200, 300, 500, 1000, 1500, 2000]


def safe_int(value, default=300):
    try:
        if value is None:
            return default
        value = str(value).replace(".", "").replace(",", "")
        return max(int(value), 1)
    except Exception:
        return default


def format_eur(value, decimals=0):
    try:
        number = float(value)
        if decimals == 0:
            text = f"{number:,.0f}"
        else:
            text = f"{number:,.{decimals}f}"
        return text.replace(",", "X").replace(".", ",").replace("X", ".") + " €"
    except Exception:
        return "0 €"


def calcular_interes_compuesto_simple(aportacion_mensual, anos=30, rentabilidad=7, capital_inicial=0, inflacion=2, comision=0.2):
    aportacion_mensual = max(float(aportacion_mensual), 0)
    anos = max(int(anos), 1)
    capital = max(float(capital_inicial), 0)
    rentabilidad_neta = max((float(rentabilidad) - float(comision)) / 100, -0.99)
    inflacion = float(inflacion) / 100

    r_mensual = (1 + rentabilidad_neta) ** (1 / 12) - 1
    meses = anos * 12
    aportado = capital

    for _ in range(meses):
        capital = capital * (1 + r_mensual) + aportacion_mensual
        aportado += aportacion_mensual

    valor_final = capital
    ganancia = max(valor_final - aportado, 0)
    valor_real = valor_final / ((1 + inflacion) ** anos) if inflacion > -1 else valor_final

    return {
        "valor_final": valor_final,
        "aportado": aportado,
        "ganancia": ganancia,
        "valor_real": valor_real,
        "anos": anos,
        "rentabilidad": rentabilidad,
        "inflacion": inflacion * 100,
        "comision": comision,
    }


def calculadora_url(aportacion, anos=HORIZONTE_BASE):
    return (
        f"/calculadora?capital={CAPITAL_INICIAL_BASE}"
        f"&aportacion={aportacion}"
        f"&tipo=mensual"
        f"&anios={anos}"
        f"&rent={RENTABILIDAD_BASE}"
        f"&infl={INFLACION_BASE}"
        f"&fee={COMISION_BASE}"
        f"&escenario=base"
    )


def faq_schema(aportacion):
    r20 = calcular_interes_compuesto_simple(aportacion, 20)
    r30 = calcular_interes_compuesto_simple(aportacion, 30)

    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": f"¿Cuánto puedo conseguir invirtiendo {format_eur(aportacion)} al mes?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"Depende del plazo, la rentabilidad, la inflación y las comisiones. Como ejemplo orientativo, invirtiendo {format_eur(aportacion)} al mes durante 30 años al 7% anual, el valor final estimado sería de aproximadamente {format_eur(r30['valor_final'])} antes de impuestos."
                },
            },
            {
                "@type": "Question",
                "name": f"¿Es suficiente invertir {format_eur(aportacion)} al mes?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Puede ser suficiente para crear una base patrimonial relevante si se mantiene durante muchos años. La clave está en el plazo, la constancia, la rentabilidad neta y evitar costes excesivos."
                },
            },
            {
                "@type": "Question",
                "name": f"¿Cuánto tendría en 20 años invirtiendo {format_eur(aportacion)} al mes?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": f"Con una hipótesis orientativa del 7% anual y 0,2% de comisión, invertir {format_eur(aportacion)} al mes durante 20 años podría generar aproximadamente {format_eur(r20['valor_final'])}. Es una simulación orientativa, no una garantía."
                },
            },
        ],
    }


def breadcrumb_schema(aportacion):
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
                "name": "Calculadora de interés compuesto",
                "item": f"{SITE_URL}/calculadora",
            },
            {
                "@type": "ListItem",
                "position": 3,
                "name": f"Invertir {format_eur(aportacion)} al mes",
                "item": f"{SITE_URL}/invertir-{aportacion}-euros-al-mes",
            },
        ],
    }


def metric(title, value, subtitle=None):
    return html.Div(
        className="seo-invest-metric-card",
        children=[
            html.P(title),
            html.H3(value),
            html.Span(subtitle or ""),
        ],
    )


def related_links(aportacion):
    candidatos = [x for x in APORTACIONES_RECOMENDADAS if x != aportacion]
    cercanos = sorted(candidatos, key=lambda x: abs(x - aportacion))[:6]

    return html.Div(
        className="seo-invest-related",
        children=[
            html.H2("También te puede interesar"),
            html.Div(
                className="seo-invest-related-grid",
                children=[
                    dcc.Link(
                        f"Invertir {format_eur(x)} al mes",
                        href=f"/invertir-{x}-euros-al-mes",
                        className="seo-invest-related-link",
                    )
                    for x in cercanos
                ]
                + [
                    dcc.Link("Calculadora de interés compuesto", href="/calculadora", className="seo-invest-related-link"),
                    dcc.Link("Calculadora FIRE", href="/fire", className="seo-invest-related-link"),
                    dcc.Link("Comparador de inversión", href="/comparador", className="seo-invest-related-link"),
                ],
            ),
        ],
    )


def layout(aportacion=None, **kwargs):
    aportacion = safe_int(aportacion, 300)

    r10 = calcular_interes_compuesto_simple(aportacion, 10)
    r20 = calcular_interes_compuesto_simple(aportacion, 20)
    r30 = calcular_interes_compuesto_simple(aportacion, 30)

    title = f"Invertir {format_eur(aportacion)} al mes: cuánto podrías conseguir a largo plazo"
    description = (
        f"Simula cuánto podrías acumular invirtiendo {format_eur(aportacion)} al mes "
        f"durante 10, 20 o 30 años con interés compuesto."
    )

    return html.Main(
        className="seo-invest-page",
        children=[
            html.Script(type="application/ld+json", children=json.dumps(faq_schema(aportacion), ensure_ascii=False)),
            html.Script(type="application/ld+json", children=json.dumps(breadcrumb_schema(aportacion), ensure_ascii=False)),

            html.Section(
                className="seo-invest-hero",
                children=[
                    html.Div("Interés compuesto", className="seo-invest-eyebrow"),
                    html.H1(title),
                    html.P(description, className="seo-invest-lead"),
                    html.Div(
                        className="seo-invest-hero-metrics",
                        children=[
                            html.Div([html.Span("Aportación mensual"), html.Strong(format_eur(aportacion))]),
                            html.Div([html.Span("Hipótesis base"), html.Strong("7% anual")]),
                            html.Div([html.Span("Horizonte principal"), html.Strong("30 años")]),
                        ],
                    ),
                    html.Div(
                        className="seo-invest-cta-row",
                        children=[
                            dcc.Link(
                                "Calcular mi caso exacto",
                                href=calculadora_url(aportacion, 30),
                                className="seo-invest-btn seo-invest-btn-primary",
                            ),
                            dcc.Link(
                                "Ver calculadora completa",
                                href="/calculadora",
                                className="seo-invest-btn seo-invest-btn-secondary",
                            ),
                        ],
                    ),
                ],
            ),

            html.Section(
                className="seo-invest-card-grid",
                children=[
                    metric("En 10 años", format_eur(r10["valor_final"]), f"Aportado: {format_eur(r10['aportado'])}"),
                    metric("En 20 años", format_eur(r20["valor_final"]), f"Aportado: {format_eur(r20['aportado'])}"),
                    metric("En 30 años", format_eur(r30["valor_final"]), f"Aportado: {format_eur(r30['aportado'])}"),
                ],
            ),

            html.Section(
                className="seo-invest-content",
                children=[
                    html.H2(f"¿Cuánto puedes ganar invirtiendo {format_eur(aportacion)} al mes?"),
                    html.P(
                        f"Invertir {format_eur(aportacion)} al mes puede parecer una cantidad pequeña o grande según tus ingresos, "
                        "pero a largo plazo el resultado depende sobre todo de tres factores: cuánto tiempo mantienes la inversión, "
                        "qué rentabilidad neta consigues y cuántas comisiones pagas por el camino."
                    ),
                    html.P(
                        f"Con una hipótesis orientativa del {RENTABILIDAD_BASE}% anual, inflación del {INFLACION_BASE}% y comisión del {COMISION_BASE}%, "
                        f"la simulación a 30 años da un valor final aproximado de {format_eur(r30['valor_final'])}. "
                        f"De esa cantidad, habrías aportado {format_eur(r30['aportado'])} y el crecimiento estimado sería de {format_eur(r30['ganancia'])}."
                    ),

                    html.H2("Comparativa por plazo"),
                    html.Div(
                        className="seo-invest-table-wrap",
                        children=html.Table(
                            className="seo-invest-table",
                            children=[
                                html.Thead(
                                    html.Tr([
                                        html.Th("Plazo"),
                                        html.Th("Total aportado"),
                                        html.Th("Valor final estimado"),
                                        html.Th("Ganancia estimada"),
                                        html.Th("Valor real aprox."),
                                    ])
                                ),
                                html.Tbody([
                                    html.Tr([html.Td("10 años"), html.Td(format_eur(r10["aportado"])), html.Td(format_eur(r10["valor_final"])), html.Td(format_eur(r10["ganancia"])), html.Td(format_eur(r10["valor_real"]))]),
                                    html.Tr([html.Td("20 años"), html.Td(format_eur(r20["aportado"])), html.Td(format_eur(r20["valor_final"])), html.Td(format_eur(r20["ganancia"])), html.Td(format_eur(r20["valor_real"]))]),
                                    html.Tr([html.Td("30 años"), html.Td(format_eur(r30["aportado"])), html.Td(format_eur(r30["valor_final"])), html.Td(format_eur(r30["ganancia"])), html.Td(format_eur(r30["valor_real"]))]),
                                ]),
                            ],
                        ),
                    ),

                    html.Div(
                        className="seo-invest-highlight-box",
                        children=[
                            html.H2("Lleva esta simulación a la calculadora"),
                            html.P(
                                "Puedes abrir la calculadora con esta aportación ya precargada y cambiar capital inicial, años, rentabilidad, inflación o comisiones."
                            ),
                            dcc.Link(
                                f"Simular {format_eur(aportacion)} al mes en la calculadora",
                                href=calculadora_url(aportacion, 30),
                                className="seo-invest-btn seo-invest-btn-primary",
                            ),
                        ],
                    ),

                    html.H2(f"¿Tiene sentido invertir {format_eur(aportacion)} al mes?"),
                    html.P(
                        "Tiene sentido si forma parte de un plan sostenible. La aportación ideal no es necesariamente la más alta, "
                        "sino la que puedes mantener durante muchos años sin abandonar en una mala racha de mercado."
                    ),
                    html.P(
                        "Para horizontes largos, pequeñas diferencias en rentabilidad neta y comisiones pueden provocar diferencias muy grandes. "
                        "Por eso conviene comparar escenarios y no quedarse solo con una cifra final optimista."
                    ),

                    html.H2("Preguntas frecuentes"),
                    html.H3(f"¿Cuánto tendría en 30 años invirtiendo {format_eur(aportacion)} al mes?"),
                    html.P(
                        f"Con una hipótesis del {RENTABILIDAD_BASE}% anual y {COMISION_BASE}% de comisión, el valor final estimado sería de {format_eur(r30['valor_final'])}. "
                        "La cifra real puede ser mayor o menor según el mercado, los costes y la inflación."
                    ),
                    html.H3(f"¿Es mejor invertir {format_eur(aportacion)} al mes o hacer aportaciones anuales?"),
                    html.P(
                        "Invertir mensualmente suele ayudar a crear hábito y reduce el riesgo de concentrar toda la entrada en un único momento. "
                        "Las aportaciones anuales también pueden funcionar, pero requieren más disciplina y planificación."
                    ),
                    html.H3("¿Esta simulación garantiza la rentabilidad futura?"),
                    html.P(
                        "No. Es una estimación orientativa basada en hipótesis. La rentabilidad real dependerá de los mercados, el producto elegido, las comisiones, los impuestos y el plazo."
                    ),

                    related_links(aportacion),
                ],
            ),
        ],
    )
