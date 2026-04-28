import dash
from dash import html, dcc, Input, Output, callback, clientside_callback
import dash_bootstrap_components as dbc

from components.disclaimer_afiliados import build_disclaimer

from utils.impuestos import get_paises, get_ubicaciones, calcular_motor_fiscal_pro
from utils.rentabilidad_alquiler import (
    safe_float,
    fmt_eur,
    fmt_pct,
    cuota_hipoteca_mensual,
    calc_operacion,
    semaforo,
    proyeccion_10_anios,
    calc_payback_years,
)
from utils.graficos_alquiler import (
    grafico_breakdown,
    grafico_comparativa,
    build_pro_years_chart,
)


dash.register_page(
    __name__,
    path="/rentabilidad-alquiler",
    title="Rentabilidad alquiler: cuánto se gana realmente con un piso",
    name="Rentabilidad alquiler",
    description=(
        "Calculadora de rentabilidad de alquiler en España. Calcula rentabilidad bruta, "
        "rentabilidad neta, cashflow mensual, gastos, hipoteca y compara vivienda vs bolsa."
    ),
)

HIPOTECA_URL = "/hipoteca"
COMPARADOR_URL = "/comparador"
SP500_RETURN_DEFAULT = 7.0
STRIPE_PAYMENT_LINK = "https://buy.stripe.com/cNi00kaRr1Ri8sU0tr1VK00"

SEO_RELATED_LINKS = [
    ("Rentabilidad alquiler vivienda España", "/rentabilidad-alquiler-vivienda-espana"),
    ("¿Es rentable comprar piso para alquilar?", "/es-rentable-comprar-piso-para-alquilar"),
    ("Comprar piso o invertir en bolsa", "/comprar-piso-para-alquilar-o-invertir-en-bolsa"),
    ("Invertir en vivienda o S&P 500", "/invertir-en-vivienda-o-sp500"),
    ("Calculadora de hipoteca", "/hipoteca"),
    ("Comparador de inversión", "/comparador"),
]


def section_eyebrow(text):
    return html.Div(
        text,
        className="small fw-bold mb-2",
        style={
            "letterSpacing": "0.08em",
            "textTransform": "uppercase",
            "color": "#0d6efd",
        },
    )


def metric_card(title, value, subtitle=None, accent=False):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, className="text-muted small fw-semibold mb-2"),
                html.Div(
                    value,
                    className=f"fw-bold {'text-primary' if accent else ''}",
                    style={
                        "fontSize": "2rem",
                        "lineHeight": "1.0",
                        "letterSpacing": "-0.03em",
                    },
                ),
                html.Div(subtitle, className="text-muted small mt-2") if subtitle else None,
            ]
        ),
        className="border-0 shadow-sm rounded-4 h-100",
        style={"background": "linear-gradient(180deg, #ffffff 0%, #fbfdff 100%)"},
    )


def input_eur(label, input_id, value, step=1000, help_text=None):
    children = [
        html.Label(label, className="fw-semibold mb-2"),
        dbc.InputGroup(
            [
                dbc.Input(
                    id=input_id,
                    type="number",
                    value=value,
                    step=step,
                    min=0,
                    class_name="rounded-start-4",
                ),
                dbc.InputGroupText("€", className="rounded-end-4"),
            ],
            class_name="mb-2",
        ),
    ]
    if help_text:
        children.append(html.Div(help_text, className="text-muted small"))
    return html.Div(children, className="mb-3")


def input_pct(label, input_id, value, step=0.5, help_text=None, max_value=None):
    children = [
        html.Label(label, className="fw-semibold mb-2"),
        dbc.InputGroup(
            [
                dbc.Input(
                    id=input_id,
                    type="number",
                    value=value,
                    step=step,
                    min=0,
                    max=max_value,
                    class_name="rounded-start-4",
                ),
                dbc.InputGroupText("%", className="rounded-end-4"),
            ],
            class_name="mb-2",
        ),
    ]
    if help_text:
        children.append(html.Div(help_text, className="text-muted small"))
    return html.Div(children, className="mb-3")


def select_input(label, input_id, options, value=None, help_text=None):
    children = [
        html.Label(label, className="fw-semibold mb-2"),
        dbc.Select(
            id=input_id,
            options=options,
            value=value,
            class_name="rounded-4 mb-2",
        ),
    ]
    if help_text:
        children.append(html.Div(help_text, className="text-muted small"))
    return html.Div(children, className="mb-3")


def badge_estado(label, color):
    return dbc.Badge(
        label,
        color=color,
        pill=True,
        class_name="px-3 py-2",
        style={"fontSize": "0.95rem"},
    )


def gastos_genericos_compra(precio_compra):
    return precio_compra * 0.10


def build_tax_teaser_card(precio_compra, pais, ubicacion, tipo_vivienda):
    gastos_estimados = gastos_genericos_compra(precio_compra)

    return dbc.Alert(
        [
            html.Div("Estimación gratuita de gastos de compra", className="fw-bold mb-2"),
            html.Div([html.Strong("Gastos estimados: "), fmt_eur(gastos_estimados)], className="mb-2"),
            html.Div(
                "⚠️ Esta cifra es orientativa. No incluye el cálculo fiscal detallado por comunidad, estado o tipo de vivienda.",
                className="small text-muted mb-2",
            ),
            html.Div(
                [
                    "La versión PRO calcula automáticamente ",
                    html.Strong("ITP, AJD, IVA o ISAI"),
                    f" según {pais or 'España'} · {ubicacion or 'Madrid'}, y compara el coste fiscal contra otra región.",
                ],
                className="small text-muted mb-3",
            ),
            dbc.Button(
                "Ver impuestos reales en PRO",
                href=STRIPE_PAYMENT_LINK,
                target="_self",
                color="primary",
                size="sm",
                className="rounded-pill fw-bold",
            ),
        ],
        color="warning",
        className="rounded-4 mb-0",
    )


def build_pro_compare_teaser_card():
    return dbc.Card(
        dbc.CardBody(
            [
                section_eyebrow("COMPARADOR PRO"),
                html.H4("Compara impuestos entre regiones", className="h6 fw-bold mb-2"),
                html.P(
                    "En PRO podrás comparar cuánto cambia el coste fiscal de comprar el mismo inmueble en otra comunidad, estado o país.",
                    className="text-muted small mb-3",
                ),
                html.Div(
                    [
                        dbc.Badge("Madrid vs Cataluña", color="light", text_color="dark", class_name="me-2 mb-2"),
                        dbc.Badge("España vs México", color="light", text_color="dark", class_name="me-2 mb-2"),
                        dbc.Badge("ITP / AJD / IVA / ISAI", color="light", text_color="dark", class_name="me-2 mb-2"),
                    ],
                    className="mb-3",
                ),
                dbc.Button(
                    "Desbloquear comparador fiscal",
                    href=STRIPE_PAYMENT_LINK,
                    target="_self",
                    color="dark",
                    size="sm",
                    className="rounded-pill fw-bold",
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 mt-3",
    )


def build_tax_preview_card(motor_fiscal, pais, ubicacion, tipo_vivienda):
    compra = motor_fiscal["compra"]
    alquiler = motor_fiscal["alquiler"]

    return dbc.Alert(
        [
            html.Div("Motor fiscal PRO aplicado", className="fw-bold mb-2"),
            html.Div([html.Strong("Zona: "), f"{pais} · {ubicacion}"], className="mb-1"),
            html.Div(
                [
                    html.Strong("Tipo vivienda: "),
                    "Segunda mano" if tipo_vivienda == "segunda_mano" else "Obra nueva",
                ],
                className="mb-1",
            ),
            html.Div([html.Strong(f"{compra.get('impuesto_nombre', 'Impuesto')}: "), fmt_eur(compra.get("impuesto", 0))], className="mb-1"),
            html.Div([html.Strong("Notaría / registro estimado: "), fmt_eur(compra.get("notaria", 0))], className="mb-1"),
            html.Div([html.Strong("Gastos compra estimados: "), fmt_eur(compra.get("total", 0))], className="mb-1"),
            html.Hr(className="my-2"),
            html.Div([html.Strong("Base IRPF alquiler estimada: "), fmt_eur(alquiler.get("base_irpf", 0))], className="mb-1"),
            html.Div([html.Strong("IRPF alquiler estimado: "), fmt_eur(alquiler.get("irpf", 0))], className="mb-0"),
        ],
        color="primary",
        className="rounded-4 mb-0",
    )


def build_tax_comparison_card(motor_actual, motor_comparado, pais_actual, ubicacion_actual, pais_comparado, ubicacion_comparado):
    compra_actual = motor_actual["compra"]
    compra_comparada = motor_comparado["compra"]

    total_actual = compra_actual.get("total", 0)
    total_comparado = compra_comparada.get("total", 0)
    diferencia = total_comparado - total_actual

    if diferencia > 0:
        lectura = f"Comprar en {ubicacion_comparado} sería {fmt_eur(abs(diferencia), 0)} más caro en gastos de compra estimados."
        color = "warning"
    elif diferencia < 0:
        lectura = f"Comprar en {ubicacion_comparado} sería {fmt_eur(abs(diferencia), 0)} más barato en gastos de compra estimados."
        color = "success"
    else:
        lectura = "Ambas ubicaciones tienen un coste fiscal estimado muy similar."
        color = "primary"

    return dbc.Card(
        dbc.CardBody(
            [
                section_eyebrow("COMPARADOR FISCAL PRO"),
                html.H4("Diferencia de impuestos entre regiones", className="h5 fw-bold mb-3"),
                dbc.Row(
                    [
                        dbc.Col(
                            metric_card(
                                f"{pais_actual} · {ubicacion_actual}",
                                fmt_eur(total_actual, 0),
                                f"{compra_actual.get('impuesto_nombre', 'Impuesto')} + notaría / registro",
                                accent=True,
                            ),
                            md=4,
                        ),
                        dbc.Col(
                            metric_card(
                                f"{pais_comparado} · {ubicacion_comparado}",
                                fmt_eur(total_comparado, 0),
                                f"{compra_comparada.get('impuesto_nombre', 'Impuesto')} + notaría / registro",
                            ),
                            md=4,
                        ),
                        dbc.Col(
                            metric_card(
                                "Diferencia fiscal",
                                fmt_eur(diferencia, 0),
                                "Comparado - ubicación actual",
                                accent=diferencia < 0,
                            ),
                            md=4,
                        ),
                    ],
                    class_name="g-4 mb-3",
                ),
                dbc.Alert(lectura, color=color, className="rounded-4 mb-0"),
            ]
        ),
        className="border-0 shadow-sm rounded-4 mb-4",
    )


def decision_final_card(rent_mostrar, cashflow_mensual, sp500_return):
    if cashflow_mensual < 0:
        label = "Cuidado"
        color = "danger"
        titulo = "La operación exige poner dinero cada mes"
        texto = (
            "Aunque la rentabilidad pueda parecer aceptable, el cashflow mensual sale negativo. "
            "Esto aumenta el riesgo si hay meses sin alquilar, averías, derramas o subida de gastos."
        )
    elif rent_mostrar >= max(5, sp500_return - 1):
        label = "Interesante"
        color = "success"
        titulo = "La operación puede merecer análisis profundo"
        texto = (
            "La rentabilidad y el cashflow son razonables. Antes de comprar, conviene revisar "
            "impuestos reales por zona, escenario a 10 años, vacancia, gastos futuros y coste de oportunidad."
        )
    elif rent_mostrar >= 3:
        label = "Dudosa"
        color = "warning"
        titulo = "La operación está ajustada"
        texto = (
            "Puede tener sentido si la zona es muy buena o esperas revalorización, pero los números "
            "no son claramente superiores a una inversión más pasiva."
        )
    else:
        label = "Floja"
        color = "danger"
        titulo = "La rentabilidad no compensa demasiado"
        texto = (
            "Con estos supuestos, revisaría precio de compra, alquiler esperado o gastos. "
            "También compararía contra una alternativa indexada más simple."
        )

    return dbc.Card(
        dbc.CardBody(
            [
                section_eyebrow("DECISIÓN RÁPIDA"),
                dbc.Badge(label, color=color, pill=True, class_name="px-3 py-2 mb-3"),
                html.H3(titulo, className="h4 fw-bold mb-3"),
                html.P(texto, className="text-muted mb-4"),
                html.Div(
                    [
                        dbc.Button("Ver análisis PRO", href="#pro-content", color="primary", className="rounded-pill px-4 me-2 mb-2"),
                        dbc.Button("Comparar con bolsa", href=COMPARADOR_URL, color="light", className="rounded-pill px-4 border mb-2"),
                    ]
                ),
            ]
        ),
        className="border-0 shadow-sm rounded-4 mb-4",
        style={"background": "linear-gradient(180deg, #ffffff 0%, #f8fbff 100%)"},
    )


def build_pro_decision_card(inmueble_final, sp500_final, payback_years, beneficio_neto_anual):
    diferencia = inmueble_final - sp500_final

    if beneficio_neto_anual <= 0:
        label = "No comprar"
        color = "danger"
        texto = "La operación genera beneficio neto no positivo. Con estos supuestos, no parece una buena compra."
    elif diferencia < 0 and (payback_years is None or payback_years > 20):
        label = "No comprar"
        color = "danger"
        texto = "La inversión sale peor que la referencia indexada y tarda demasiado en recuperarse."
    elif diferencia < 0 or (payback_years is not None and payback_years > 15):
        label = "Dudoso"
        color = "warning"
        texto = "La operación no es claramente mala, pero tampoco suficientemente sólida con estos números."
    else:
        label = "Comprar"
        color = "success"
        texto = "Con estos supuestos, la operación parece razonable y mantiene una lectura atractiva."

    return dbc.Card(
        dbc.CardBody(
            [
                section_eyebrow("RECOMENDACIÓN FINAL"),
                dbc.Badge(label, color=color, pill=True, class_name="px-3 py-2 mb-3"),
                html.P(texto, className="text-muted mb-0"),
            ]
        ),
        className="border-0 shadow-sm rounded-4 h-100",
    )


def build_coste_oportunidad_card(inmueble_final, sp500_final):
    diferencia = sp500_final - inmueble_final
    if diferencia > 0:
        return metric_card("Coste de oportunidad", fmt_eur(diferencia, 0), "Lo que dejarías de ganar frente al S&P 500")
    return metric_card("Ventaja frente al S&P 500", fmt_eur(abs(diferencia), 0), "Lo que ganaría el inmueble frente al S&P 500", accent=True)


def build_payback_card(payback_years):
    if payback_years is None:
        return metric_card("Payback estimado", "No recuperable", "Con beneficio neto anual no positivo")

    return metric_card(
        "Payback estimado",
        f"{round(payback_years, 1)} años".replace(".", ","),
        "Tiempo orientativo para recuperar la inversión inicial",
        accent=True if payback_years <= 15 else False,
    )


def build_pro_summary(rows):
    final = rows[-1]
    diff = final["valor_total_inmueble"] - final["valor_sp500"]

    if diff > 0:
        lectura = f"En esta simulación, el inmueble termina por encima del S&P 500 por {fmt_eur(diff)}."
    elif diff < 0:
        lectura = f"En esta simulación, el S&P 500 termina por encima del inmueble por {fmt_eur(abs(diff))}."
    else:
        lectura = "En esta simulación, ambas alternativas terminan prácticamente iguales."

    return html.Div(
        [
            html.P([html.Strong("Valor total estimado del inmueble en año 10: "), fmt_eur(final["valor_total_inmueble"])], className="mb-2"),
            html.P([html.Strong("Valor estimado del S&P 500 en año 10: "), fmt_eur(final["valor_sp500"])], className="mb-2"),
            html.P(lectura, className="mb-0"),
        ]
    )


def build_pro_table(rows):
    return dbc.Table(
        [
            html.Thead(html.Tr([html.Th("Año"), html.Th("Beneficio neto"), html.Th("Valor inmueble"), html.Th("Valor S&P 500")])),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(r["anio"]),
                            html.Td(fmt_eur(r["beneficio_neto"], 0)),
                            html.Td(fmt_eur(r["valor_total_inmueble"], 0)),
                            html.Td(fmt_eur(r["valor_sp500"], 0)),
                        ]
                    )
                    for r in rows
                ]
            ),
        ],
        bordered=False,
        hover=True,
        responsive=True,
        class_name="align-middle mb-0",
    )


def pro_card(unlocked=False):
    if unlocked:
        return dbc.Card(
            dbc.CardBody(
                [
                    section_eyebrow("VERSIÓN PRO"),
                    html.H3("Acceso premium activo", className="h4 fw-bold mb-3"),
                    html.P("Ya tienes desbloqueado el motor fiscal PRO y el análisis completo de esta calculadora.", className="text-muted mb-3"),
                    dbc.Alert("✅ Motor fiscal, comparador de regiones y análisis a 10 años disponibles más abajo.", color="success", className="rounded-4 mb-0"),
                ]
            ),
            className="border-0 shadow-sm rounded-4 h-100",
            style={"background": "linear-gradient(180deg, #ffffff 0%, #f5f9ff 100%)"},
        )

    return dbc.Card(
        dbc.CardBody(
            [
                section_eyebrow("VERSIÓN PRO"),
                html.H3("No compres un piso con números incompletos", className="h4 fw-bold mb-3"),
                html.P(
                    "Los impuestos cambian completamente la rentabilidad. Una diferencia de comunidad autónoma, "
                    "estado o tipo de vivienda puede suponer miles de euros. La versión PRO calcula ITP, AJD, IVA o ISAI "
                    "según la ubicación y compara cuánto pagarías en otra región.",
                    className="text-muted mb-3",
                ),
                html.Div(
                    [
                        dbc.Badge("Motor fiscal", color="light", text_color="dark", class_name="me-2 mb-2"),
                        dbc.Badge("Comparador regiones", color="light", text_color="dark", class_name="me-2 mb-2"),
                        dbc.Badge("ITP / AJD / IVA / ISAI", color="light", text_color="dark", class_name="me-2 mb-2"),
                        dbc.Badge("Rentabilidad fiscal", color="light", text_color="dark", class_name="me-2 mb-2"),
                        dbc.Badge("Comprar / no comprar", color="light", text_color="dark", class_name="me-2 mb-2"),
                    ],
                    className="mb-4",
                ),
                html.Div(
                    [
                        html.Div("✔ Cálculo automático de impuestos por zona", className="small text-muted mb-1"),
                        html.Div("✔ Comparación fiscal entre dos regiones", className="small text-muted mb-1"),
                        html.Div("✔ Impacto real en rentabilidad y cashflow", className="small text-muted mb-1"),
                        html.Div("✔ Proyección a 10 años contra S&P 500", className="small text-muted mb-1"),
                        html.Div("✔ Payback y recomendación final", className="small text-muted mb-3"),
                    ]
                ),
                dbc.Button("Evitar errores de miles de euros por 9€", href=STRIPE_PAYMENT_LINK, target="_self", color="primary", className="rounded-pill px-4 fw-bold"),
            ]
        ),
        className="border-0 shadow-sm rounded-4 h-100",
    )


def locked_preview(unlocked=False):
    return dbc.Card(
        dbc.CardBody(
            [
                section_eyebrow("PREVIEW PRO"),
                html.H3("Lo que desbloquea el análisis premium", className="h5 fw-bold mb-3"),
                html.Div(
                    [
                        html.Div("Motor fiscal + comparador regional", className="fw-semibold mb-2"),
                        html.Div("ITP · AJD · IVA · ISAI", className="display-6 fw-bold text-primary"),
                        html.P(
                            "Calcula gastos de compra, compara regiones, estima rentabilidad fiscal, payback y comparativa frente al S&P 500.",
                            className="text-muted mt-3 mb-0",
                        ),
                    ],
                    style={
                        "filter": "blur(3px)" if not unlocked else "none",
                        "opacity": 0.75 if not unlocked else 1,
                        "borderRadius": "18px",
                        "padding": "1rem",
                        "background": "#f8fafc",
                        "border": "1px solid #e9eef5",
                    },
                ),
                dbc.Button(
                    "Quiero comparar impuestos reales",
                    href=STRIPE_PAYMENT_LINK,
                    target="_self",
                    color="dark",
                    className="rounded-pill px-4 mt-4 w-100 fw-bold",
                ) if not unlocked else dbc.Alert("✅ PRO activo", color="success", className="rounded-4 mt-4 mb-0"),
            ]
        ),
        className="border-0 shadow-sm rounded-4 h-100",
    )


def seo_link_card(title, href):
    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3(title, className="h6 fw-bold mb-2"),
                    dcc.Link("Leer guía →", href=href, className="text-decoration-none fw-semibold"),
                ]
            ),
            className="border-0 shadow-sm rounded-4 h-100",
        ),
        md=4,
        className="mb-3",
    )


def seo_text_block():
    return html.Div(
        dbc.Container(
            [
                section_eyebrow("GUÍA PARA ANALIZAR UN ALQUILER"),
                html.H2("Cómo calcular la rentabilidad real de un piso en alquiler", className="fw-bold mb-3"),
                html.P(
                    "La rentabilidad de un alquiler no se calcula solo dividiendo el alquiler anual entre el precio de compra. "
                    "Para saber si una vivienda es realmente rentable hay que incluir impuestos, gastos de compra, reforma, IBI, "
                    "comunidad, seguro, mantenimiento, posibles meses sin alquilar, gestión e hipoteca.",
                    className="text-muted",
                ),
                html.P(
                    "Esta calculadora estima rentabilidad bruta, rentabilidad neta, cashflow mensual, capital aportado "
                    "y comparación frente a una inversión indexada como el S&P 500.",
                    className="text-muted",
                ),
            ]
        ),
        className="py-5",
    )


def seo_how_to_block():
    return html.Div(
        dbc.Container(
            [
                section_eyebrow("MÉTODO DE CÁLCULO"),
                html.H2("Qué métricas debes mirar antes de comprar para alquilar", className="fw-bold mb-4"),
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(dbc.CardBody([html.H3("Rentabilidad bruta", className="h5 fw-bold"), html.P("Ingresos anuales por alquiler divididos entre inversión total.", className="text-muted small mb-0")]), className="border-0 shadow-sm rounded-4 h-100"), md=4, className="mb-3"),
                        dbc.Col(dbc.Card(dbc.CardBody([html.H3("Rentabilidad neta", className="h5 fw-bold"), html.P("Beneficio real después de gastos, impuestos, mantenimiento e IBI.", className="text-muted small mb-0")]), className="border-0 shadow-sm rounded-4 h-100"), md=4, className="mb-3"),
                        dbc.Col(dbc.Card(dbc.CardBody([html.H3("Cashflow mensual", className="h5 fw-bold"), html.P("Dinero que queda cada mes después de gastos y cuota hipotecaria.", className="text-muted small mb-0")]), className="border-0 shadow-sm rounded-4 h-100"), md=4, className="mb-3"),
                    ]
                ),
            ]
        ),
        className="py-5",
    )


def seo_related_block():
    return html.Div(
        dbc.Container(
            [
                section_eyebrow("GUÍAS RELACIONADAS"),
                html.H2("Sigue analizando la inversión inmobiliaria", className="fw-bold mb-3"),
                html.P("Estas guías complementan la calculadora y ayudan a comparar vivienda, bolsa, hipoteca y rentabilidad real.", className="text-muted mb-4"),
                dbc.Row([seo_link_card(title, href) for title, href in SEO_RELATED_LINKS]),
            ]
        ),
        className="py-5",
    )


def seo_faq_block():
    return html.Div(
        dbc.Container(
            [
                section_eyebrow("PREGUNTAS FRECUENTES"),
                html.H2("Dudas habituales sobre rentabilidad de alquiler", className="fw-bold mb-4"),
                dbc.Accordion(
                    [
                        dbc.AccordionItem(html.P("Depende de la ciudad, precio, gastos y alquiler. Como referencia, una rentabilidad neta superior al 5% suele ser interesante.", className="mb-0"), title="¿Qué rentabilidad es buena para un piso en alquiler?"),
                        dbc.AccordionItem(html.P("La rentabilidad bruta solo usa ingresos y precio. La neta descuenta gastos, impuestos, mantenimiento, comunidad, IBI y otros costes.", className="mb-0"), title="¿Qué diferencia hay entre rentabilidad bruta y neta?"),
                        dbc.AccordionItem(html.P("Puede mejorar la rentabilidad sobre capital aportado, pero aumenta riesgo y puede empeorar el cashflow mensual.", className="mb-0"), title="¿Es mejor comprar con hipoteca para alquilar?"),
                        dbc.AccordionItem(html.P("La vivienda puede ofrecer apalancamiento e ingresos. La bolsa suele ser más líquida, diversificada y pasiva.", className="mb-0"), title="¿Es mejor invertir en vivienda o en bolsa?"),
                    ],
                    start_collapsed=True,
                ),
            ]
        ),
        className="py-5",
    )


layout = dbc.Container(
    [
        dcc.Location(id="url", refresh=False),
        dcc.Store(id="gtag-pro-open-store"),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            "INVERSIÓN INMOBILIARIA · ALQUILER · CASHFLOW",
                            className="d-inline-block fw-bold mb-3",
                            style={
                                "fontSize": "0.82rem",
                                "letterSpacing": "0.08em",
                                "textTransform": "uppercase",
                                "color": "#0d6efd",
                                "background": "#eef4ff",
                                "border": "1px solid #d7e6ff",
                                "padding": "0.45rem 0.85rem",
                                "borderRadius": "999px",
                            },
                        ),
                        html.H1(
                            "Calculadora rentabilidad alquiler: bruta, neta y cashflow",
                            className="fw-bold mb-3",
                            style={
                                "fontSize": "clamp(2.1rem, 5vw, 4rem)",
                                "lineHeight": "1.02",
                                "letterSpacing": "-0.05em",
                                "color": "#101828",
                            },
                        ),
                        html.P(
                            "Calcula si un piso para alquilar es rentable. Introduce precio, alquiler, gastos, impuestos e hipoteca para estimar rentabilidad bruta, rentabilidad neta, cashflow mensual y comparativa frente al S&P 500.",
                            className="lead text-muted mb-4",
                            style={"maxWidth": "820px"},
                        ),
                        html.Div(
                            [
                                dbc.Button("Probar calculadora gratis", id="hero-cta-gratis", href="#calculadora-rentabilidad", color="primary", className="rounded-pill px-4 me-2 mb-2"),
                                dbc.Button("Ver calculadora hipoteca", id="hero-cta-hipoteca", href=HIPOTECA_URL, color="light", className="rounded-pill px-4 border mb-2"),
                            ]
                        ),
                    ],
                    lg=7,
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                section_eyebrow("LECTURA RÁPIDA"),
                                html.H2("¿Merece la pena comprar para alquilar?", className="h4 fw-bold mb-3"),
                                html.P("Introduce los datos y mira al instante si la operación tiene una rentabilidad atractiva, cashflow positivo y si mejora o no una alternativa indexada.", className="text-muted mb-3"),
                                html.Ul(
                                    [
                                        html.Li("Rentabilidad bruta y neta"),
                                        html.Li("Estimación gratuita de gastos"),
                                        html.Li("Impuestos reales por zona en PRO"),
                                        html.Li("Comparador fiscal entre regiones en PRO"),
                                    ],
                                    className="text-muted mb-0",
                                ),
                            ]
                        ),
                        className="border-0 shadow-sm rounded-4",
                    ),
                    lg=5,
                ),
            ],
            class_name="py-5 align-items-center",
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div(id="calculadora-rentabilidad"),
                                section_eyebrow("SUPUESTOS"),
                                html.H2("Introduce los datos del inmueble", className="h4 fw-bold mb-4"),

                                html.H4("Compra", className="h6 fw-bold mb-3"),
                                input_eur("Precio de compra", "precio_compra", 180000, step=1000),

                                select_input(
                                    "País",
                                    "pais_fiscal",
                                    options=[{"label": p, "value": p} for p in get_paises()],
                                    value="España",
                                    help_text="En PRO se usa para calcular impuestos reales por país.",
                                ),

                                select_input(
                                    "Comunidad / Estado",
                                    "ubicacion_fiscal",
                                    options=[{"label": u, "value": u} for u in get_ubicaciones("España")],
                                    value="Madrid",
                                    help_text="En PRO se usa para estimar ITP, AJD, ISAI y gastos de compra.",
                                ),

                                select_input(
                                    "Tipo de vivienda",
                                    "tipo_vivienda",
                                    options=[
                                        {"label": "Segunda mano", "value": "segunda_mano"},
                                        {"label": "Obra nueva", "value": "obra_nueva"},
                                    ],
                                    value="segunda_mano",
                                ),

                                html.Hr(className="my-4"),

                                html.H4("Comparador fiscal PRO", className="h6 fw-bold mb-3"),
                                select_input(
                                    "Comparar contra país",
                                    "compare_pais_fiscal",
                                    options=[{"label": p, "value": p} for p in get_paises()],
                                    value="España",
                                    help_text="El comparador fiscal se desbloquea en PRO.",
                                ),

                                select_input(
                                    "Comparar contra comunidad / estado",
                                    "compare_ubicacion_fiscal",
                                    options=[{"label": u, "value": u} for u in get_ubicaciones("España")],
                                    value="Cataluña",
                                    help_text="Ejemplo: compara Madrid contra Cataluña, Valencia, Andalucía o México.",
                                ),

                                input_eur("Reforma y puesta a punto", "reforma", 10000, step=500),
                                html.Div(id="tax_preview_wrap", className="mt-3"),
                                html.Div(id="compare_teaser_wrap"),

                                html.Hr(className="my-4"),

                                html.H4("Ingresos", className="h6 fw-bold mb-3"),
                                input_eur("Alquiler mensual esperado", "alquiler_mensual", 950, step=25),
                                input_pct("Ocupación estimada", "ocupacion", 95, step=1, max_value=100),

                                html.Hr(className="my-4"),

                                html.H4("Gastos anuales", className="h6 fw-bold mb-3"),
                                input_eur("IBI anual", "ibi", 450, step=25),
                                input_eur("Comunidad anual", "comunidad", 720, step=25),
                                input_eur("Seguro anual", "seguro", 220, step=10),
                                input_eur("Mantenimiento anual", "mantenimiento", 600, step=25),
                                input_pct("Gestión / administración", "gestion_pct", 0, step=0.5),
                                input_pct("IRPF efectivo estimado", "irpf_pct", 19, step=1),

                                html.Hr(className="my-4"),

                                html.H4("Hipoteca", className="h6 fw-bold mb-3"),
                                dbc.RadioItems(
                                    id="usar_hipoteca",
                                    options=[
                                        {"label": "Sin hipoteca", "value": "no"},
                                        {"label": "Con hipoteca", "value": "si"},
                                    ],
                                    value="no",
                                    inline=True,
                                    class_name="mb-3",
                                ),
                                input_pct("Porcentaje financiado", "ltv_pct", 70, step=1),
                                input_pct("Tipo de interés", "interes_hipoteca", 3.0, step=0.1),
                                input_eur("Plazo (años)", "años_hipoteca", 25, step=1),

                                html.Hr(className="my-4"),

                                html.H4("Comparativa", className="h6 fw-bold mb-3"),
                                input_pct("Rentabilidad anual esperada del S&P 500", "sp500_return", SP500_RETURN_DEFAULT, step=0.5),
                            ]
                        ),
                        className="border-0 shadow-sm rounded-4 h-100",
                    ),
                    lg=5,
                ),

                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(html.Div(id="metric_bruta"), md=6),
                                dbc.Col(html.Div(id="metric_neta"), md=6),
                            ],
                            class_name="g-4 mb-4",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Div(id="metric_cashflow"), md=6),
                                dbc.Col(html.Div(id="metric_desembolso"), md=6),
                            ],
                            class_name="g-4 mb-4",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(html.Div(id="metric_cuota"), md=6),
                                dbc.Col(html.Div(id="metric_capital"), md=6),
                            ],
                            class_name="g-4 mb-4",
                        ),

                        html.Div(id="decision_final_wrap"),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    section_eyebrow("LECTURA RÁPIDA"),
                                    html.Div(id="signal_badge", className="mb-3"),
                                    html.Div(id="signal_text", className="text-muted"),
                                ]
                            ),
                            className="border-0 shadow-sm rounded-4 mb-4",
                        ),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    section_eyebrow("BREAKDOWN GRATIS"),
                                    dcc.Graph(
                                        id="breakdown_chart",
                                        config={"displayModeBar": False, "responsive": True},
                                        style={"width": "100%", "height": "360px"},
                                        className="dash-graph-responsive",
                                    ),
                                ]
                            ),
                            className="border-0 shadow-sm rounded-4 mb-4",
                        ),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    section_eyebrow("COMPARATIVA GRATIS"),
                                    dcc.Graph(
                                        id="compare_chart",
                                        config={"displayModeBar": False, "responsive": True},
                                        style={"width": "100%", "height": "360px"},
                                        className="dash-graph-responsive",
                                    ),
                                ]
                            ),
                            className="border-0 shadow-sm rounded-4",
                        ),
                    ],
                    lg=7,
                ),
            ],
            class_name="g-4 pb-4",
        ),

        dbc.Row(
            [
                dbc.Col(html.Div(pro_card(False), id="pro-card-dynamic"), lg=5),
                dbc.Col(html.Div(locked_preview(False), id="pro-preview-dynamic"), lg=7),
            ],
            class_name="g-4 pb-4",
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                section_eyebrow("ANÁLISIS PRO"),
                                html.Div(id="pro-unlock-feedback", className="mb-3"),
                                html.Div(id="pro-content"),
                            ]
                        ),
                        className="border-0 shadow-sm rounded-4",
                    ),
                    lg=12,
                ),
            ],
            class_name="pb-4",
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                section_eyebrow("IDEAS CLAVE"),
                                html.Div(id="insights_wrap", className="text-muted"),
                            ]
                        ),
                        className="border-0 shadow-sm rounded-4 h-100",
                    ),
                    lg=12,
                ),
            ],
            class_name="g-4 pb-4",
        ),

        seo_text_block(),
        seo_how_to_block(),
        seo_related_block(),
        seo_faq_block(),

        html.Div(
            dbc.Container(
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    html.Div("Calcula impuestos reales antes de comprar", className="fw-bold"),
                                    html.Div("Motor fiscal PRO: compara ITP, AJD, IVA, ISAI, payback y rentabilidad a 10 años.", className="small text-muted"),
                                ]
                            ),
                            xs=7,
                            md=8,
                        ),
                        dbc.Col(
                            dbc.Button(
                                "Calcular PRO",
                                href=STRIPE_PAYMENT_LINK,
                                target="_self",
                                color="primary",
                                className="rounded-pill w-100 fw-bold",
                            ),
                            xs=5,
                            md=4,
                        ),
                    ],
                    class_name="align-items-center g-2",
                ),
                fluid=False,
            ),
            style={
                "position": "fixed",
                "left": "0",
                "right": "0",
                "bottom": "0",
                "zIndex": "1030",
                "background": "rgba(255,255,255,0.96)",
                "backdropFilter": "blur(8px)",
                "borderTop": "1px solid #e9eef5",
                "padding": "0.8rem 0.9rem",
                "boxShadow": "0 -6px 24px rgba(16,24,40,0.08)",
            },
        ),

        html.Div(id="pro-scroll-trigger", style={"display": "none"}),
        html.Div(style={"height": "88px"}),

        build_disclaimer() if callable(build_disclaimer) else html.Div(),
    ],
    fluid=True,
    class_name="px-3 px-lg-4",
)


@callback(
    Output("ubicacion_fiscal", "options"),
    Output("ubicacion_fiscal", "value"),
    Input("pais_fiscal", "value"),
)
def update_ubicaciones_fiscales(pais):
    ubicaciones = get_ubicaciones(pais or "España")
    options = [{"label": u, "value": u} for u in ubicaciones]
    value = "Madrid" if pais == "España" and "Madrid" in ubicaciones else ubicaciones[0] if ubicaciones else None
    return options, value


@callback(
    Output("compare_ubicacion_fiscal", "options"),
    Output("compare_ubicacion_fiscal", "value"),
    Input("compare_pais_fiscal", "value"),
)
def update_compare_ubicaciones_fiscales(pais):
    ubicaciones = get_ubicaciones(pais or "España")
    options = [{"label": u, "value": u} for u in ubicaciones]
    if pais == "España" and "Cataluña" in ubicaciones:
        value = "Cataluña"
    else:
        value = ubicaciones[0] if ubicaciones else None
    return options, value


@callback(
    Output("gtag-pro-open-store", "data"),
    Input("premium-access", "data"),
    prevent_initial_call=False,
)
def track_pro_interest(premium_access):
    unlocked = bool((premium_access or {}).get("unlocked"))
    if unlocked:
        return {"event": "unlock_rentabilidad_pro"}
    return dash.no_update


@callback(
    Output("pro-unlock-feedback", "children"),
    Output("pro-scroll-trigger", "children"),
    Input("premium-access", "data"),
    prevent_initial_call=False,
)
def sync_unlock_feedback(premium_access):
    unlocked = bool((premium_access or {}).get("unlocked"))
    if unlocked:
        return (
            dbc.Alert("✅ Acceso premium activado correctamente.", color="success", className="rounded-4 mb-0"),
            "scroll",
        )
    return html.Div(), ""


@callback(
    Output("pro-card-dynamic", "children"),
    Output("pro-preview-dynamic", "children"),
    Input("premium-access", "data"),
)
def update_pro_blocks(premium_access):
    unlocked = bool((premium_access or {}).get("unlocked"))
    return pro_card(unlocked), locked_preview(unlocked)


clientside_callback(
    """
    function(data) {
        if (!data) { return window.dash_clientside.no_update; }
        if (window.gtag) {
            window.gtag('event', data.event, {
                page: 'rentabilidad_alquiler'
            });
        }
        return '';
    }
    """,
    Output("hero-cta-gratis", "title"),
    Input("gtag-pro-open-store", "data"),
)


clientside_callback(
    """
    function(trigger) {
        if (!trigger) {
            return window.dash_clientside.no_update;
        }
        const el = document.getElementById("pro-content");
        if (el) {
            setTimeout(function() {
                el.scrollIntoView({ behavior: "smooth", block: "start" });
            }, 150);
        }
        return "";
    }
    """,
    Output("pro-scroll-trigger", "title"),
    Input("pro-scroll-trigger", "children"),
)


@callback(
    Output("metric_bruta", "children"),
    Output("metric_neta", "children"),
    Output("metric_cashflow", "children"),
    Output("metric_desembolso", "children"),
    Output("metric_cuota", "children"),
    Output("metric_capital", "children"),
    Output("decision_final_wrap", "children"),
    Output("signal_badge", "children"),
    Output("signal_text", "children"),
    Output("breakdown_chart", "figure"),
    Output("compare_chart", "figure"),
    Output("insights_wrap", "children"),
    Output("tax_preview_wrap", "children"),
    Output("compare_teaser_wrap", "children"),
    Input("premium-access", "data"),
    Input("precio_compra", "value"),
    Input("pais_fiscal", "value"),
    Input("ubicacion_fiscal", "value"),
    Input("tipo_vivienda", "value"),
    Input("compare_pais_fiscal", "value"),
    Input("compare_ubicacion_fiscal", "value"),
    Input("reforma", "value"),
    Input("alquiler_mensual", "value"),
    Input("ocupacion", "value"),
    Input("ibi", "value"),
    Input("comunidad", "value"),
    Input("seguro", "value"),
    Input("mantenimiento", "value"),
    Input("gestion_pct", "value"),
    Input("irpf_pct", "value"),
    Input("usar_hipoteca", "value"),
    Input("ltv_pct", "value"),
    Input("interes_hipoteca", "value"),
    Input("años_hipoteca", "value"),
    Input("sp500_return", "value"),
)
def update_calculator(
    premium_access,
    precio_compra,
    pais_fiscal,
    ubicacion_fiscal,
    tipo_vivienda,
    compare_pais_fiscal,
    compare_ubicacion_fiscal,
    reforma,
    alquiler_mensual,
    ocupacion,
    ibi,
    comunidad,
    seguro,
    mantenimiento,
    gestion_pct,
    irpf_pct,
    usar_hipoteca,
    ltv_pct,
    interes_hipoteca,
    años_hipoteca,
    sp500_return,
):
    unlocked = bool((premium_access or {}).get("unlocked"))

    precio_compra = safe_float(precio_compra)
    reforma = safe_float(reforma)
    alquiler_mensual = safe_float(alquiler_mensual)
    ocupacion = safe_float(ocupacion, 95)
    ibi = safe_float(ibi)
    comunidad = safe_float(comunidad)
    seguro = safe_float(seguro)
    mantenimiento = safe_float(mantenimiento)
    gestion_pct = safe_float(gestion_pct)
    irpf_pct = safe_float(irpf_pct)
    ltv_pct = safe_float(ltv_pct)
    interes_hipoteca = safe_float(interes_hipoteca)
    años_hipoteca = max(int(safe_float(años_hipoteca, 25)), 1)
    sp500_return = safe_float(sp500_return, SP500_RETURN_DEFAULT)

    usar_deuda = usar_hipoteca == "si"

    capital_hipoteca = precio_compra * (ltv_pct / 100) if usar_deuda else 0
    cuota_mensual = cuota_hipoteca_mensual(capital_hipoteca, interes_hipoteca, años_hipoteca) if usar_deuda else 0
    cuota_anual = cuota_mensual * 12
    intereses_anuales_estimados = capital_hipoteca * (interes_hipoteca / 100) if usar_deuda else 0

    ingresos_anuales_estimados = alquiler_mensual * 12 * (ocupacion / 100)
    gasto_gestion = ingresos_anuales_estimados * (gestion_pct / 100)
    gastos_anuales_base = ibi + comunidad + seguro + mantenimiento + gasto_gestion

    motor_fiscal = calcular_motor_fiscal_pro(
        precio_compra=precio_compra,
        pais=pais_fiscal or "España",
        ubicacion=ubicacion_fiscal or "Madrid",
        tipo_vivienda=tipo_vivienda or "segunda_mano",
        alquiler_mensual=alquiler_mensual,
        ocupacion_pct=ocupacion,
        gastos_anuales=gastos_anuales_base,
        intereses_hipoteca_anuales=intereses_anuales_estimados,
        reforma=reforma,
        precio_venta_estimado=None,
        reduccion_alquiler_pct=50,
        tipo_marginal_irpf_pct=irpf_pct,
    )

    if unlocked:
        gastos_compra = motor_fiscal["compra"]["total"]
        tax_card = build_tax_preview_card(
            motor_fiscal=motor_fiscal,
            pais=pais_fiscal or "España",
            ubicacion=ubicacion_fiscal or "Madrid",
            tipo_vivienda=tipo_vivienda or "segunda_mano",
        )
        compare_card = html.Div()
        gastos_label = "Compra + impuestos reales + reforma"
    else:
        gastos_compra = gastos_genericos_compra(precio_compra)
        tax_card = build_tax_teaser_card(
            precio_compra=precio_compra,
            pais=pais_fiscal or "España",
            ubicacion=ubicacion_fiscal or "Madrid",
            tipo_vivienda=tipo_vivienda or "segunda_mano",
        )
        compare_card = build_pro_compare_teaser_card()
        gastos_label = "Compra + gastos estimados + reforma"

    base = calc_operacion(
        precio_compra=precio_compra,
        gastos_compra=gastos_compra,
        reforma=reforma,
        alquiler_mensual=alquiler_mensual,
        ocupacion_pct=ocupacion,
        ibi=ibi,
        comunidad=comunidad,
        seguro=seguro,
        mantenimiento=mantenimiento,
        gestion_pct=gestion_pct,
        irpf_pct=irpf_pct,
    )

    capital_aportado = base["inversion_total"] - capital_hipoteca if usar_deuda else base["inversion_total"]
    capital_aportado = max(capital_aportado, 0)

    cashflow_despues_hipoteca = base["cashflow_mensual"] - cuota_mensual
    beneficio_neto_despues_hipoteca = base["beneficio_neto"] - cuota_anual
    beneficio_neto_economico_con_deuda = base["beneficio_neto"] - intereses_anuales_estimados

    rent_sobre_capital = (
        beneficio_neto_economico_con_deuda / capital_aportado * 100
        if capital_aportado > 0
        else 0
    )

    rent_mostrar = rent_sobre_capital if usar_deuda else base["rent_neta"]
    etiqueta, color, mensaje = semaforo(rent_mostrar)

    metric_bruta = metric_card("Rentabilidad bruta", fmt_pct(base["rent_bruta"]), "Ingresos anuales / inversión total", accent=True)

    metric_neta = metric_card(
        "Rentabilidad neta",
        fmt_pct(rent_mostrar),
        "Sin deuda" if not usar_deuda else "Sobre capital aportado",
        accent=rent_mostrar >= 5,
    )

    metric_cashflow = metric_card(
        "Cashflow mensual",
        fmt_eur(base["cashflow_mensual"]) if not usar_deuda else fmt_eur(cashflow_despues_hipoteca),
        "Sin deuda" if not usar_deuda else "Después de cuota hipotecaria",
    )

    metric_desembolso = metric_card("Desembolso inicial", fmt_eur(base["inversion_total"]), gastos_label)
    metric_cuota = metric_card("Cuota hipotecaria", fmt_eur(cuota_mensual), "Mensual" if usar_deuda else "No aplica")
    metric_capital = metric_card("Capital aportado", fmt_eur(capital_aportado), "Tu dinero inicial")

    decision_final = decision_final_card(
        rent_mostrar=rent_mostrar,
        cashflow_mensual=cashflow_despues_hipoteca if usar_deuda else base["cashflow_mensual"],
        sp500_return=sp500_return,
    )

    signal_text = html.Div(
        [
            html.P([html.Strong("Ingresos anuales: "), fmt_eur(base["ingresos_anuales"])], className="mb-2"),
            html.P([html.Strong("Gastos + IRPF: "), fmt_eur(base["gastos_anuales"] + base["irpf"])], className="mb-2"),
            html.P([html.Strong("Intereses anuales estimados: "), fmt_eur(intereses_anuales_estimados)] if usar_deuda else [html.Strong("Intereses anuales estimados: "), "No aplica"], className="mb-2"),
            html.P([html.Strong("Resultado económico anual: "), fmt_eur(base["beneficio_neto"]) if not usar_deuda else fmt_eur(beneficio_neto_economico_con_deuda)], className="mb-2"),
            html.P([html.Strong("Cashflow anual después de cuota: "), fmt_eur(base["beneficio_neto"]) if not usar_deuda else fmt_eur(beneficio_neto_despues_hipoteca)], className="mb-2"),
            html.P(mensaje, className="mb-0"),
        ]
    )

    if unlocked:
        insights = [
            html.Li(f"Gastos reales de compra calculados por motor fiscal: {fmt_eur(gastos_compra)}.", className="mb-2"),
            html.Li(f"Rentabilidad neta con fiscalidad aplicada: {fmt_pct(base['rent_neta'])}.", className="mb-2"),
        ]
    else:
        insights = [
            html.Li(f"Gastos de compra estimados de forma genérica: {fmt_eur(gastos_compra)}.", className="mb-2"),
            html.Li("El cálculo gratuito no desglosa ITP, AJD, IVA o ISAI por región.", className="mb-2"),
            html.Li("El comparador fiscal entre regiones está incluido en PRO.", className="mb-2"),
            html.Li(f"Rentabilidad neta orientativa: {fmt_pct(base['rent_neta'])}.", className="mb-2"),
        ]

    if usar_deuda:
        spread_apalancamiento = base["rent_neta"] - interes_hipoteca
        insights += [
            html.Li(f"Cuota hipotecaria mensual estimada: {fmt_eur(cuota_mensual)}.", className="mb-2"),
            html.Li(f"Cashflow mensual después de hipoteca: {fmt_eur(cashflow_despues_hipoteca)}.", className="mb-2"),
            html.Li(f"Rentabilidad sobre capital aportado: {fmt_pct(rent_sobre_capital)}.", className="mb-2"),
            html.Li(f"Spread de apalancamiento: {fmt_pct(spread_apalancamiento)}.", className="mb-2"),
        ]

    if rent_mostrar >= sp500_return:
        insights.append(html.Li(f"La rentabilidad mostrada supera la referencia del S&P 500 ({fmt_pct(sp500_return)}).", className="mb-2"))
    else:
        insights.append(html.Li(f"La rentabilidad mostrada queda por debajo de la referencia del S&P 500 ({fmt_pct(sp500_return)}).", className="mb-2"))

    if usar_deuda and cashflow_despues_hipoteca < 0:
        insights.append(html.Li("Con hipoteca, el flujo mensual sale negativo con estos supuestos.", className="mb-2"))

    return (
        metric_bruta,
        metric_neta,
        metric_cashflow,
        metric_desembolso,
        metric_cuota,
        metric_capital,
        decision_final,
        badge_estado(etiqueta, color),
        signal_text,
        grafico_breakdown(base, cuota_anual if usar_deuda else 0),
        grafico_comparativa(base["inversion_total"], capital_aportado, base["rent_neta"], rent_sobre_capital, sp500_return, usar_deuda),
        html.Ul(insights, className="mb-0"),
        tax_card,
        compare_card,
    )


@callback(
    Output("pro-content", "children"),
    Input("premium-access", "data"),
    Input("precio_compra", "value"),
    Input("pais_fiscal", "value"),
    Input("ubicacion_fiscal", "value"),
    Input("tipo_vivienda", "value"),
    Input("compare_pais_fiscal", "value"),
    Input("compare_ubicacion_fiscal", "value"),
    Input("reforma", "value"),
    Input("alquiler_mensual", "value"),
    Input("ocupacion", "value"),
    Input("ibi", "value"),
    Input("comunidad", "value"),
    Input("seguro", "value"),
    Input("mantenimiento", "value"),
    Input("gestion_pct", "value"),
    Input("irpf_pct", "value"),
    Input("sp500_return", "value"),
)
def render_pro_content(
    premium_access,
    precio_compra,
    pais_fiscal,
    ubicacion_fiscal,
    tipo_vivienda,
    compare_pais_fiscal,
    compare_ubicacion_fiscal,
    reforma,
    alquiler_mensual,
    ocupacion,
    ibi,
    comunidad,
    seguro,
    mantenimiento,
    gestion_pct,
    irpf_pct,
    sp500_return,
):
    unlocked = bool((premium_access or {}).get("unlocked"))

    if not unlocked:
        return html.Div(
            [
                html.H3("Calcula impuestos reales por zona antes de comprar", className="h5 fw-bold mb-3"),
                html.P(
                    "No es lo mismo comprar en Madrid, Cataluña, Valencia, Andalucía o México. "
                    "La versión PRO ajusta automáticamente los gastos de compra según la ubicación "
                    "y compara el coste fiscal contra otra región.",
                    className="text-muted mb-3",
                ),
                html.Div(
                    [
                        html.Div("Motor fiscal PRO bloqueado", className="fw-semibold mb-2"),
                        html.Div("ITP · AJD · IVA · ISAI", className="display-6 fw-bold text-primary"),
                        html.P(
                            "Desbloquea impuestos por región, comparador fiscal, rentabilidad fiscal, proyección a 10 años, payback, coste de oportunidad y recomendación final.",
                            className="text-muted mt-3 mb-0",
                        ),
                    ],
                    style={
                        "padding": "1rem",
                        "borderRadius": "16px",
                        "background": "#f8fafc",
                        "border": "1px dashed #cbd5e1",
                        "filter": "blur(2px)",
                        "opacity": 0.8,
                    },
                ),
                html.Div(
                    [
                        dbc.Badge("Impuestos por región", color="light", text_color="dark", class_name="me-2 mt-3"),
                        dbc.Badge("Comparador fiscal", color="light", text_color="dark", class_name="me-2 mt-3"),
                        dbc.Badge("Gastos compra reales", color="light", text_color="dark", class_name="me-2 mt-3"),
                        dbc.Badge("Rentabilidad fiscal", color="light", text_color="dark", class_name="me-2 mt-3"),
                        dbc.Badge("Decisión final", color="light", text_color="dark", class_name="me-2 mt-3"),
                    ],
                    className="mb-4",
                ),
                dbc.Button(
                    "Desbloquear análisis fiscal PRO por 9€",
                    href=STRIPE_PAYMENT_LINK,
                    target="_self",
                    color="primary",
                    className="rounded-pill px-4 fw-bold mt-2",
                ),
            ]
        )

    precio_compra = safe_float(precio_compra)
    reforma = safe_float(reforma)
    alquiler_mensual = safe_float(alquiler_mensual)
    ocupacion = safe_float(ocupacion, 95)
    ibi = safe_float(ibi)
    comunidad = safe_float(comunidad)
    seguro = safe_float(seguro)
    mantenimiento = safe_float(mantenimiento)
    gestion_pct = safe_float(gestion_pct)
    irpf_pct = safe_float(irpf_pct)
    sp500_return = safe_float(sp500_return, SP500_RETURN_DEFAULT)

    ingresos_base = alquiler_mensual * 12 * (ocupacion / 100)
    gasto_gestion = ingresos_base * (gestion_pct / 100)
    gastos_anuales = ibi + comunidad + seguro + mantenimiento + gasto_gestion

    motor_fiscal = calcular_motor_fiscal_pro(
        precio_compra=precio_compra,
        pais=pais_fiscal or "España",
        ubicacion=ubicacion_fiscal or "Madrid",
        tipo_vivienda=tipo_vivienda or "segunda_mano",
        alquiler_mensual=alquiler_mensual,
        ocupacion_pct=ocupacion,
        gastos_anuales=gastos_anuales,
        intereses_hipoteca_anuales=0,
        reforma=reforma,
        precio_venta_estimado=precio_compra * (1.02 ** 10),
        reduccion_alquiler_pct=50,
        tipo_marginal_irpf_pct=irpf_pct,
    )

    motor_comparado = calcular_motor_fiscal_pro(
        precio_compra=precio_compra,
        pais=compare_pais_fiscal or "España",
        ubicacion=compare_ubicacion_fiscal or "Cataluña",
        tipo_vivienda=tipo_vivienda or "segunda_mano",
        alquiler_mensual=alquiler_mensual,
        ocupacion_pct=ocupacion,
        gastos_anuales=gastos_anuales,
        intereses_hipoteca_anuales=0,
        reforma=reforma,
        precio_venta_estimado=precio_compra * (1.02 ** 10),
        reduccion_alquiler_pct=50,
        tipo_marginal_irpf_pct=irpf_pct,
    )

    gastos_compra = motor_fiscal["compra"]["total"]
    inversion_inicial = precio_compra + gastos_compra + reforma

    years, inmueble_vals, sp500_vals, rows = proyeccion_10_anios(
        inversion_inicial=inversion_inicial,
        alquiler_mensual=alquiler_mensual,
        ocupacion_pct=ocupacion,
        gastos_anuales=gastos_anuales,
        irpf_pct=irpf_pct,
        crecimiento_alquiler_pct=2.0,
        crecimiento_gastos_pct=2.0,
        revalorizacion_inmueble_pct=2.0,
        sp500_pct=sp500_return,
    )

    inmueble_final = inmueble_vals[-1]
    sp500_final = sp500_vals[-1]
    beneficio_neto_anual_base = rows[0]["beneficio_neto"] if rows else 0
    payback_years = calc_payback_years(inversion_inicial, beneficio_neto_anual_base)

    return html.Div(
        [
            html.H3("Versión PRO desbloqueada", className="h5 fw-bold mb-3"),
            html.P("Aquí ves una lectura mucho más útil para decidir si el inmueble merece la pena o no.", className="text-muted mb-4"),

            dbc.Card(
                dbc.CardBody(
                    [
                        section_eyebrow("MOTOR FISCAL PRO"),
                        html.H4("Impuestos y fiscalidad estimada", className="h5 fw-bold mb-3"),
                        dbc.Row(
                            [
                                dbc.Col(
                                    metric_card(
                                        motor_fiscal["compra"].get("impuesto_nombre", "Impuesto compra"),
                                        fmt_eur(motor_fiscal["compra"].get("impuesto", 0), 0),
                                        f"{pais_fiscal or 'España'} · {ubicacion_fiscal or 'Madrid'}",
                                        accent=True,
                                    ),
                                    md=4,
                                ),
                                dbc.Col(
                                    metric_card(
                                        "Gastos compra totales",
                                        fmt_eur(motor_fiscal["compra"].get("total", 0), 0),
                                        "Impuestos + notaría / registro",
                                        accent=True,
                                    ),
                                    md=4,
                                ),
                                dbc.Col(
                                    metric_card(
                                        "IRPF alquiler estimado",
                                        fmt_eur(motor_fiscal["alquiler"].get("irpf", 0), 0),
                                        "Según beneficio fiscal estimado",
                                    ),
                                    md=4,
                                ),
                            ],
                            class_name="g-4",
                        ),
                        html.Div(
                            [
                                html.P([html.Strong("Base fiscal alquiler: "), fmt_eur(motor_fiscal["alquiler"].get("base_irpf", 0))], className="mb-2 mt-4"),
                                html.P([html.Strong("Beneficio neto fiscal alquiler: "), fmt_eur(motor_fiscal["alquiler"].get("beneficio_neto", 0))], className="mb-2"),
                                html.P([html.Strong("Rentabilidad neta fiscal: "), fmt_pct(motor_fiscal.get("rentabilidad_neta_fiscal", 0))], className="mb-0"),
                            ],
                            className="text-muted",
                        ),
                    ]
                ),
                className="border-0 shadow-sm rounded-4 mb-4",
            ),

            build_tax_comparison_card(
                motor_actual=motor_fiscal,
                motor_comparado=motor_comparado,
                pais_actual=pais_fiscal or "España",
                ubicacion_actual=ubicacion_fiscal or "Madrid",
                pais_comparado=compare_pais_fiscal or "España",
                ubicacion_comparado=compare_ubicacion_fiscal or "Cataluña",
            ),

            dbc.Row(
                [
                    dbc.Col(build_pro_decision_card(inmueble_final, sp500_final, payback_years, beneficio_neto_anual_base), lg=4),
                    dbc.Col(build_coste_oportunidad_card(inmueble_final, sp500_final), lg=4),
                    dbc.Col(build_payback_card(payback_years), lg=4),
                ],
                class_name="g-4 mb-4",
            ),

            dbc.Row(
                [
                    dbc.Col(metric_card("Valor inmueble año 10", fmt_eur(inmueble_final, 0), "Revalorización + cashflow acumulado", accent=True), md=4),
                    dbc.Col(metric_card("Valor S&P 500 año 10", fmt_eur(sp500_final, 0), "Capital inicial capitalizado"), md=4),
                    dbc.Col(metric_card("Diferencia final", fmt_eur(inmueble_final - sp500_final, 0), "Inmueble - S&P 500"), md=4),
                ],
                class_name="g-4 mb-4",
            ),

            dbc.Card(
                dbc.CardBody(
                    dcc.Graph(
                        figure=build_pro_years_chart(years, inmueble_vals, sp500_vals),
                        config={"displayModeBar": False, "responsive": True},
                        style={"width": "100%", "height": "390px"},
                        className="dash-graph-responsive",
                    )
                ),
                className="border-0 shadow-sm rounded-4 mb-4",
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody([section_eyebrow("RESUMEN"), build_pro_summary(rows)]),
                            className="border-0 shadow-sm rounded-4 h-100",
                        ),
                        lg=5,
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody([section_eyebrow("TABLA ANUAL"), build_pro_table(rows)]),
                            className="border-0 shadow-sm rounded-4 h-100",
                        ),
                        lg=7,
                    ),
                ],
                class_name="g-4",
            ),
        ]
    )
