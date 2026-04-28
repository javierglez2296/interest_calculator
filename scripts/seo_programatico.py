import dash
from dash import html, dcc
import dash_bootstrap_components as dbc


SITE_URL = "https://interescompuesto.app"
MYINVESTOR_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"


# =========================================================
# HELPERS
# =========================================================

def fmt_eur(n):
    try:
        return f"{n:,.0f} €".replace(",", ".")
    except Exception:
        return "-"


def calc_compuesto(capital_inicial, aportacion_mensual, rentabilidad_anual, anos):
    r = rentabilidad_anual / 100 / 12
    meses = anos * 12
    total = capital_inicial

    for _ in range(meses):
        total = total * (1 + r) + aportacion_mensual

    aportado = capital_inicial + aportacion_mensual * meses
    ganancia = total - aportado

    return round(total), round(aportado), round(ganancia)


def capital_necesario_para_renta(renta_mensual, tasa_retiro=0.04):
    return round((renta_mensual * 12) / tasa_retiro)


def calcular_cuota_hipoteca(capital, interes_anual, anos):
    r = interes_anual / 100 / 12
    n = anos * 12

    if r == 0:
        return round(capital / n)

    cuota = capital * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
    return round(cuota)


def years_to_goal(aportacion_mensual, objetivo, rentabilidad_anual=7):
    r = rentabilidad_anual / 100 / 12
    total = 0
    meses = 0

    while total < objetivo and meses < 12 * 80:
        total = total * (1 + r) + aportacion_mensual
        meses += 1

    return round(meses / 12, 1)


# =========================================================
# SEO PAGE CONFIG
# =========================================================

SEO_PAGES = [
    # Aportaciones mensuales
    {"slug": "invertir-100-euros-mes", "tipo": "aportacion", "cantidad": 100},
    {"slug": "invertir-200-euros-mes", "tipo": "aportacion", "cantidad": 200},
    {"slug": "invertir-300-euros-mes", "tipo": "aportacion", "cantidad": 300},
    {"slug": "invertir-500-euros-mes", "tipo": "aportacion", "cantidad": 500},
    {"slug": "invertir-700-euros-mes", "tipo": "aportacion", "cantidad": 700},
    {"slug": "invertir-1000-euros-mes", "tipo": "aportacion", "cantidad": 1000},

    # Vivir de rentas / FIRE
    {"slug": "cuanto-dinero-necesitas-para-vivir-con-1000-euros-mes", "tipo": "rentas", "cantidad": 1000},
    {"slug": "cuanto-dinero-necesitas-para-vivir-con-1500-euros-mes", "tipo": "rentas", "cantidad": 1500},
    {"slug": "cuanto-dinero-necesitas-para-vivir-con-2000-euros-mes", "tipo": "rentas", "cantidad": 2000},
    {"slug": "cuanto-dinero-necesitas-para-vivir-con-3000-euros-mes", "tipo": "rentas", "cantidad": 3000},
    {"slug": "cuanto-dinero-necesitas-para-vivir-de-rentas-en-espana", "tipo": "rentas", "cantidad": 2000},

    # Objetivos patrimonio
    {"slug": "como-conseguir-100000-euros", "tipo": "objetivo", "cantidad": 100000},
    {"slug": "como-conseguir-200000-euros", "tipo": "objetivo", "cantidad": 200000},
    {"slug": "como-conseguir-500000-euros", "tipo": "objetivo", "cantidad": 500000},
    {"slug": "como-conseguir-un-millon-de-euros", "tipo": "objetivo", "cantidad": 1000000},

    # Satélites SEO alquiler
    {"slug": "calcular-rentabilidad-piso-alquiler", "tipo": "alquiler_sat", "cantidad": 0},
    {"slug": "rentabilidad-bruta-neta-alquiler", "tipo": "alquiler_sat", "cantidad": 0},
    {"slug": "cashflow-inmobiliario", "tipo": "alquiler_sat", "cantidad": 0},
    {"slug": "gastos-comprar-piso-para-alquilar", "tipo": "alquiler_sat", "cantidad": 0},
    {"slug": "comprar-piso-para-alquilar-rentable", "tipo": "alquiler_sat", "cantidad": 0},
    {"slug": "rentabilidad-alquiler-con-hipoteca", "tipo": "alquiler_sat", "cantidad": 0},
    {"slug": "rentabilidad-alquiler-sin-hipoteca", "tipo": "alquiler_sat", "cantidad": 0},
    {"slug": "como-saber-si-un-piso-es-rentable", "tipo": "alquiler_sat", "cantidad": 0},

    # Capital inicial
    {"slug": "donde-invertir-1000-euros", "tipo": "capital", "cantidad": 1000},
    {"slug": "donde-invertir-5000-euros", "tipo": "capital", "cantidad": 5000},
    {"slug": "donde-invertir-10000-euros", "tipo": "capital", "cantidad": 10000},
    {"slug": "donde-invertir-50000-euros", "tipo": "capital", "cantidad": 50000},

    # FIRE por edad
    {"slug": "cuanto-dinero-necesito-para-jubilarme-a-los-40", "tipo": "fire_edad", "cantidad": 40},
    {"slug": "cuanto-dinero-necesito-para-jubilarme-a-los-45", "tipo": "fire_edad", "cantidad": 45},
    {"slug": "cuanto-dinero-necesito-para-jubilarme-a-los-50", "tipo": "fire_edad", "cantidad": 50},
    {"slug": "cuanto-dinero-necesito-para-jubilarme-a-los-55", "tipo": "fire_edad", "cantidad": 55},

    # Hipotecas
    {"slug": "cuanto-se-paga-de-hipoteca-por-100000-euros", "tipo": "hipoteca_importe", "cantidad": 100000},
    {"slug": "cuanto-se-paga-de-hipoteca-por-150000-euros", "tipo": "hipoteca_importe", "cantidad": 150000},
    {"slug": "cuanto-se-paga-de-hipoteca-por-200000-euros", "tipo": "hipoteca_importe", "cantidad": 200000},
    {"slug": "cuanto-se-paga-de-hipoteca-por-250000-euros", "tipo": "hipoteca_importe", "cantidad": 250000},
    {"slug": "cuanto-se-paga-de-hipoteca-por-300000-euros", "tipo": "hipoteca_importe", "cantidad": 300000},
    {"slug": "cuanto-se-paga-de-hipoteca-por-400000-euros", "tipo": "hipoteca_importe", "cantidad": 400000},

    # Vivienda / alquiler
    {"slug": "rentabilidad-alquiler-vivienda-espana", "tipo": "alquiler_rentabilidad", "cantidad": 0},
    {"slug": "es-rentable-comprar-piso-para-alquilar", "tipo": "alquiler_rentabilidad", "cantidad": 0},
    {"slug": "comprar-piso-para-alquilar-o-invertir-en-bolsa", "tipo": "vivienda_vs_bolsa", "cantidad": 0},
    {"slug": "invertir-en-vivienda-o-sp500", "tipo": "vivienda_vs_bolsa", "cantidad": 0},

    # Inversión por edad
    {"slug": "como-invertir-a-los-25-anos", "tipo": "invertir_edad", "cantidad": 25},
    {"slug": "como-invertir-a-los-30-anos", "tipo": "invertir_edad", "cantidad": 30},
    {"slug": "como-invertir-a-los-35-anos", "tipo": "invertir_edad", "cantidad": 35},
    {"slug": "como-invertir-a-los-40-anos", "tipo": "invertir_edad", "cantidad": 40},
    {"slug": "como-invertir-a-los-50-anos", "tipo": "invertir_edad", "cantidad": 50},

    # Comparativas
    {"slug": "invertir-en-sp500-o-nasdaq", "tipo": "comparativa", "cantidad": 0},
    {"slug": "sp500-o-msci-world", "tipo": "comparativa_simple", "cantidad": 0},
    {"slug": "fondos-indexados-o-etfs", "tipo": "comparativa_simple", "cantidad": 0},
    {"slug": "fondos-indexados-o-deposito", "tipo": "comparativa_simple", "cantidad": 0},
    {"slug": "invertir-en-bolsa-o-amortizar-hipoteca", "tipo": "comparativa_simple", "cantidad": 0},
    {"slug": "myinvestor-opiniones", "tipo": "myinvestor", "cantidad": 0},
]


# =========================================================
# COMPONENTS
# =========================================================

def page_shell(children):
    return html.Div(
        children,
        style={
            "background": "linear-gradient(180deg, #ffffff 0%, #f8fafc 100%)",
            "minHeight": "100vh",
        }
    )


def hero(title, description, badge="GUÍA DE INVERSIÓN"):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div(badge, className="text-uppercase fw-bold mb-3", style={
                    "letterSpacing": "0.10em",
                    "color": "#667085",
                    "fontSize": "0.78rem",
                }),
                html.H1(title, className="fw-bold mb-3", style={
                    "fontSize": "clamp(2.1rem, 5vw, 4rem)",
                    "lineHeight": "1.05",
                    "letterSpacing": "-0.04em",
                    "maxWidth": "920px",
                }),
                html.P(description, className="lead", style={
                    "maxWidth": "780px",
                    "fontSize": "1.12rem",
                    "color": "#667085",
                    "lineHeight": "1.75",
                }),
            ], lg=10)
        ])
    ], className="pt-5 pb-4")


def section(title, children):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2(title, className="fw-bold mb-3", style={
                    "letterSpacing": "-0.03em",
                    "fontSize": "clamp(1.65rem, 3vw, 2.35rem)",
                }),
                html.Div(children, style={
                    "color": "#475467",
                    "fontSize": "1.05rem",
                    "lineHeight": "1.85",
                }),
            ], lg=9)
        ])
    ], className="py-4")


def metric_row(items):
    return dbc.Container([
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.Div(label, className="mb-2", style={
                            "color": "#667085",
                            "fontSize": "0.9rem",
                        }),
                        html.H3(value, className="fw-bold mb-0", style={
                            "letterSpacing": "-0.03em",
                        }),
                    ], className="p-4"),
                    className="shadow-sm border-0 rounded-4 h-100"
                ),
                md=4,
                className="mb-3"
            )
            for label, value in items
        ])
    ], className="py-3")


def table(rows):
    header = rows[0]
    body = rows[1:]

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        dbc.Table([
                            html.Thead(html.Tr([html.Th(x) for x in header])),
                            html.Tbody([
                                html.Tr([html.Td(x) for x in row])
                                for row in body
                            ])
                        ], bordered=False, hover=True, responsive=True, className="align-middle mb-0")
                    ], className="p-2 p-md-3"),
                    className="border-0 shadow-sm rounded-4"
                )
            ], lg=10)
        ])
    ], className="py-4")


def faq(items):
    return section("Preguntas frecuentes", [
        html.Div([
            html.H3(q, className="fw-bold mt-4 mb-2", style={"fontSize": "1.22rem"}),
            html.P(a)
        ])
        for q, a in items
    ])


def related_links(items):
    return section("Guías relacionadas", [
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.H4(title, className="fw-bold mb-2", style={"fontSize": "1.05rem"}),
                        dcc.Link("Leer guía →", href=href, className="text-decoration-none fw-semibold"),
                    ]),
                    className="border-0 shadow-sm rounded-4 h-100"
                ),
                md=6,
                lg=3,
                className="mb-3"
            )
            for title, href in items
        ])
    ])


def cta_box(title, text, href, button, external=False):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H3(title, className="fw-bold mb-2"),
                        html.P(text, style={"color": "#667085", "lineHeight": "1.7"}),
                        dbc.Button(button, href=href, target="_blank" if external else None, color="dark"),
                    ], className="p-4 p-md-5"),
                    className="border-0 shadow-sm rounded-4"
                )
            ], lg=9)
        ])
    ], className="py-4")


def cta_calculadora():
    return cta_box(
        "Simula tu caso exacto",
        "Ajusta capital inicial, aportación mensual, años, rentabilidad, inflación y comisiones.",
        "/calculadora",
        "Abrir calculadora"
    )


def cta_fire():
    return cta_box(
        "Calcula tu número FIRE",
        "Descubre cuánto patrimonio necesitas para vivir de tus inversiones según tus gastos mensuales.",
        "/fire",
        "Abrir calculadora FIRE"
    )


def cta_hipoteca():
    return cta_box(
        "Calcula tu hipoteca real",
        "Simula cuota, intereses totales, entrada necesaria y esfuerzo financiero.",
        "/hipoteca",
        "Abrir calculadora de hipoteca"
    )


def cta_alquiler():
    return cta_box(
        "Calcula la rentabilidad de un alquiler",
        "Simula precio de compra, alquiler, gastos, hipoteca, cashflow y rentabilidad neta.",
        "/rentabilidad-alquiler",
        "Abrir calculadora"
    )


def cta_comparador():
    return cta_box(
        "Compara inversiones",
        "Compara bolsa, vivienda, monetarios y otras alternativas con números.",
        "/comparador",
        "Abrir comparador"
    )


def cta_myinvestor():
    return cta_box(
        "Empieza a invertir con MyInvestor",
        "Enlace de afiliado. Puedes abrir cuenta y explorar fondos indexados, carteras y productos de inversión.",
        MYINVESTOR_URL,
        "Ver MyInvestor",
        external=True
    )


# =========================================================
# BUILDERS
# =========================================================

def build_aportacion_page(cantidad):
    esc_10 = calc_compuesto(0, cantidad, 7, 10)
    esc_20 = calc_compuesto(0, cantidad, 7, 20)
    esc_30 = calc_compuesto(0, cantidad, 7, 30)

    return page_shell([
        hero(
            f"Invertir {cantidad} € al mes: cuánto puedes conseguir",
            f"Simulación realista para ver cuánto podrías acumular invirtiendo {cantidad} € mensuales a largo plazo."
        ),

        metric_row([
            ("A 10 años", fmt_eur(esc_10[0])),
            ("A 20 años", fmt_eur(esc_20[0])),
            ("A 30 años", fmt_eur(esc_30[0])),
        ]),

        section(f"Resultado de invertir {cantidad} € al mes", [
            html.P(f"Si inviertes {cantidad} € al mes de forma constante, el interés compuesto puede hacer que el capital final sea muy superior al dinero aportado."),
            html.P(f"Con una rentabilidad media estimada del 7% anual, podrías llegar aproximadamente a {fmt_eur(esc_30[0])} en 30 años."),
            html.P(["Puedes ajustar todos los datos en la ", dcc.Link("calculadora de interés compuesto", href="/calculadora"), "."]),
        ]),

        table([
            ["Horizonte", "Capital final", "Dinero aportado", "Ganancia estimada"],
            ["10 años", fmt_eur(esc_10[0]), fmt_eur(esc_10[1]), fmt_eur(esc_10[2])],
            ["20 años", fmt_eur(esc_20[0]), fmt_eur(esc_20[1]), fmt_eur(esc_20[2])],
            ["30 años", fmt_eur(esc_30[0]), fmt_eur(esc_30[1]), fmt_eur(esc_30[2])],
        ]),

        section("¿Dónde invertir esa cantidad?", [
            html.P("Para largo plazo, una opción habitual son fondos indexados globales, S&P 500, MSCI World o carteras diversificadas."),
            html.P("Lo más importante no es acertar el mejor momento, sino mantener constancia, costes bajos y un horizonte suficiente."),
        ]),

        section("Qué pasa si empiezas tarde", [
            html.P("Cuanto más tardes en empezar, más dinero tendrás que aportar para llegar al mismo resultado."),
            html.P("La ventaja de invertir pronto es que das más años al capital para crecer y reinvertir ganancias."),
        ]),

        faq([
            (f"¿Tiene sentido invertir {cantidad} € al mes?", "Sí, especialmente si tienes horizonte de largo plazo y no necesitas ese dinero a corto plazo."),
            ("¿Es seguro invertir cada mes?", "Toda inversión tiene riesgo. La clave es diversificar, entender lo que compras y no invertir dinero que puedas necesitar pronto."),
            ("¿Qué rentabilidad es realista?", "Un 7% anual es una hipótesis orientativa para bolsa global a largo plazo, no una garantía."),
        ]),

        related_links([
            ("Invertir 300 € al mes", "/invertir-300-euros-mes"),
            ("Invertir 500 € al mes", "/invertir-500-euros-mes"),
            ("Invertir 1.000 € al mes", "/invertir-1000-euros-mes"),
            ("Cómo conseguir 100.000 €", "/como-conseguir-100000-euros"),
        ]),

        cta_calculadora(),
        cta_myinvestor(),
    ])


def build_rentas_page(renta):
    capital_4 = capital_necesario_para_renta(renta, 0.04)
    capital_35 = capital_necesario_para_renta(renta, 0.035)
    capital_3 = capital_necesario_para_renta(renta, 0.03)

    return page_shell([
        hero(
            f"Cuánto dinero necesitas para vivir con {renta} € al mes",
            f"Calcula cuánto patrimonio aproximado necesitarías para generar {renta} € mensuales mediante inversiones."
        ),

        metric_row([
            ("Regla 4%", fmt_eur(capital_4)),
            ("Regla 3,5%", fmt_eur(capital_35)),
            ("Regla 3%", fmt_eur(capital_3)),
        ]),

        section("Capital necesario para vivir de rentas", [
            html.P(f"Para generar unos {renta} € al mes, necesitarías aproximadamente entre {fmt_eur(capital_4)} y {fmt_eur(capital_3)}, según la tasa de retirada utilizada."),
            html.P("La regla del 4% es una referencia conocida, pero en España conviene ser prudente por impuestos, inflación y variabilidad de los mercados."),
        ]),

        table([
            ["Escenario", "Tasa retirada", "Capital necesario"],
            ["Más agresivo", "4%", fmt_eur(capital_4)],
            ["Intermedio", "3,5%", fmt_eur(capital_35)],
            ["Conservador", "3%", fmt_eur(capital_3)],
        ]),

        section("Cómo llegar a esa cifra", [
            html.P("El camino suele combinar ahorro mensual, inversión diversificada, tiempo e ingresos adicionales."),
            html.P("Cuanto antes empiezas, menos esfuerzo mensual necesitas gracias al interés compuesto."),
            html.P(["Puedes calcular tu caso en la ", dcc.Link("calculadora FIRE", href="/fire"), "."]),
        ]),

        faq([
            ("¿La regla del 4% es segura?", "No es una garantía. Es una referencia histórica. Para España puede ser prudente usar escenarios del 3% o 3,5%."),
            ("¿Se puede vivir solo de dividendos?", "Sí, pero requiere mucho capital y una cartera diversificada. También hay que considerar impuestos."),
            ("¿Es mejor vivir de alquileres o fondos indexados?", "Depende de tu perfil. Los alquileres requieren gestión; la bolsa suele ser más líquida y diversificada."),
        ]),

        related_links([
            ("Vivir con 1.500 € al mes", "/cuanto-dinero-necesitas-para-vivir-con-1500-euros-mes"),
            ("Vivir con 2.000 € al mes", "/cuanto-dinero-necesitas-para-vivir-con-2000-euros-mes"),
            ("Jubilarse a los 40", "/cuanto-dinero-necesito-para-jubilarme-a-los-40"),
            ("Vivir de dividendos", "/vivir-de-dividendos-en-espana"),
        ]),

        cta_fire(),
        cta_myinvestor(),
    ])


def build_objetivo_page(objetivo):
    aportaciones = [300, 500, 700, 1000]
    rows = []

    for ap in aportaciones:
        rows.append([
            f"{ap} €/mes",
            fmt_eur(calc_compuesto(0, ap, 7, 10)[0]),
            fmt_eur(calc_compuesto(0, ap, 7, 20)[0]),
            fmt_eur(calc_compuesto(0, ap, 7, 30)[0]),
            f"{years_to_goal(ap, objetivo)} años",
        ])

    return page_shell([
        hero(
            f"Cómo conseguir {fmt_eur(objetivo)} invirtiendo",
            f"Guía realista para alcanzar {fmt_eur(objetivo)} mediante ahorro mensual, inversión a largo plazo e interés compuesto."
        ),

        metric_row([
            ("Con 300 €/mes", f"{years_to_goal(300, objetivo)} años"),
            ("Con 500 €/mes", f"{years_to_goal(500, objetivo)} años"),
            ("Con 1.000 €/mes", f"{years_to_goal(1000, objetivo)} años"),
        ]),

        section("¿Es posible alcanzar este objetivo?", [
            html.P(f"Sí, conseguir {fmt_eur(objetivo)} es posible, pero depende de cuánto aportas, durante cuántos años inviertes y qué rentabilidad media consigues."),
            html.P("El interés compuesto empieza lento, pero con el paso de los años el crecimiento se acelera."),
            html.P(["Puedes ajustar el escenario en la ", dcc.Link("calculadora de interés compuesto", href="/calculadora"), "."]),
        ]),

        table([
            ["Aportación mensual", "A 10 años", "A 20 años", "A 30 años", "Tiempo aprox. al objetivo"],
            *rows
        ]),

        section("Qué pasa si empiezas más tarde", [
            html.P("Retrasar la inversión puede obligarte a aportar mucho más dinero al mes para llegar al mismo objetivo."),
            html.P("En objetivos grandes, el tiempo es una de las mayores ventajas del inversor particular."),
        ]),

        section("Estrategia sencilla para lograrlo", [
            html.P("Una estrategia razonable puede ser automatizar la aportación mensual, usar productos diversificados de bajo coste y revisar el plan una o dos veces al año."),
            html.P("Lo importante es evitar cambiar de estrategia constantemente por miedo, euforia o ruido de mercado."),
        ]),

        faq([
            (f"¿Es realista conseguir {fmt_eur(objetivo)}?", "Sí, pero el plazo depende mucho de la aportación mensual y del horizonte temporal."),
            ("¿Qué rentabilidad se usa en la simulación?", "La tabla usa un 7% anual como hipótesis orientativa de largo plazo."),
            ("¿Puedo conseguirlo sin invertir?", "Sí, pero normalmente tardarías más porque dependerías solo del ahorro."),
        ]),

        related_links([
            ("Invertir 500 € al mes", "/invertir-500-euros-mes"),
            ("Invertir 1.000 € al mes", "/invertir-1000-euros-mes"),
            ("Cómo conseguir 200.000 €", "/como-conseguir-200000-euros"),
            ("Cómo conseguir 500.000 €", "/como-conseguir-500000-euros"),
        ]),

        cta_calculadora(),
        cta_myinvestor(),
    ])


def build_capital_page(cantidad):
    esc_10 = calc_compuesto(cantidad, 0, 7, 10)
    esc_20 = calc_compuesto(cantidad, 0, 7, 20)
    esc_30 = calc_compuesto(cantidad, 0, 7, 30)

    return page_shell([
        hero(
            f"Dónde invertir {fmt_eur(cantidad)}",
            f"Ideas y simulación para invertir {fmt_eur(cantidad)} a largo plazo con una estrategia sencilla."
        ),

        metric_row([
            ("A 10 años", fmt_eur(esc_10[0])),
            ("A 20 años", fmt_eur(esc_20[0])),
            ("A 30 años", fmt_eur(esc_30[0])),
        ]),

        section("Opciones para invertir ese dinero", [
            html.P(f"Si tienes {fmt_eur(cantidad)} para invertir, puedes valorar fondos indexados, ETFs, monetarios, depósitos o una combinación según tu perfil."),
            html.P("Para largo plazo, la diversificación y los costes bajos suelen ser más importantes que buscar el producto perfecto."),
        ]),

        table([
            ["Horizonte", "Capital estimado al 7% anual"],
            ["10 años", fmt_eur(esc_10[0])],
            ["20 años", fmt_eur(esc_20[0])],
            ["30 años", fmt_eur(esc_30[0])],
        ]),

        faq([
            ("¿Es mejor invertir todo de golpe o poco a poco?", "Depende de tu tolerancia al riesgo. Invertir poco a poco reduce el miedo a entrar antes de una caída."),
            ("¿Qué hago si necesito el dinero pronto?", "Si puedes necesitarlo en pocos años, conviene priorizar seguridad y liquidez frente a rentabilidad."),
            ("¿Puedo combinar fondos y depósitos?", "Sí. De hecho, muchas carteras combinan renta variable, monetarios y liquidez."),
        ]),

        related_links([
            ("Invertir 100 € al mes", "/invertir-100-euros-mes"),
            ("Invertir 500 € al mes", "/invertir-500-euros-mes"),
            ("Fondos indexados o ETFs", "/fondos-indexados-o-etfs"),
            ("S&P 500 o MSCI World", "/sp500-o-msci-world"),
        ]),

        cta_calculadora(),
        cta_myinvestor(),
    ])


def build_fire_edad_page(edad):
    return page_shell([
        hero(
            f"Cuánto dinero necesito para jubilarme a los {edad}",
            f"Guía práctica para calcular cuánto patrimonio necesitas para alcanzar la libertad financiera a los {edad} años.",
            badge="FIRE · LIBERTAD FINANCIERA"
        ),

        metric_row([
            ("1.000 €/mes", fmt_eur(300000)),
            ("2.000 €/mes", fmt_eur(600000)),
            ("3.000 €/mes", fmt_eur(900000)),
        ]),

        section("La respuesta depende de tus gastos", [
            html.P("Para saber cuánto necesitas, lo más importante no es tu edad, sino cuánto dinero necesitas gastar cada mes."),
            html.P("Como referencia, con la regla del 4%, necesitarías multiplicar tus gastos anuales por 25."),
        ]),

        table([
            ["Gasto mensual", "Capital aproximado necesario"],
            ["1.000 €/mes", fmt_eur(300000)],
            ["1.500 €/mes", fmt_eur(450000)],
            ["2.000 €/mes", fmt_eur(600000)],
            ["3.000 €/mes", fmt_eur(900000)],
        ]),

        section("Cómo acelerar el camino", [
            html.P("Las palancas principales son aumentar tu ahorro mensual, invertir de forma constante y evitar que el estilo de vida suba demasiado rápido."),
            html.P(["Calcula tu caso exacto en la ", dcc.Link("calculadora FIRE", href="/fire"), "."]),
        ]),

        related_links([
            ("Vivir con 1.500 € al mes", "/cuanto-dinero-necesitas-para-vivir-con-1500-euros-mes"),
            ("Vivir con 2.000 € al mes", "/cuanto-dinero-necesitas-para-vivir-con-2000-euros-mes"),
            ("Invertir 500 € al mes", "/invertir-500-euros-mes"),
            ("Cómo conseguir 500.000 €", "/como-conseguir-500000-euros"),
        ]),

        cta_fire(),
        cta_myinvestor(),
    ])


def build_hipoteca_importe_page(importe):
    cuota_25 = calcular_cuota_hipoteca(importe, 3.0, 25)
    cuota_30 = calcular_cuota_hipoteca(importe, 3.0, 30)
    cuota_35 = calcular_cuota_hipoteca(importe, 3.0, 35)

    return page_shell([
        hero(
            f"Cuánto se paga de hipoteca por {fmt_eur(importe)}",
            f"Simulación de cuota mensual para una hipoteca de {fmt_eur(importe)} según plazo y tipo de interés.",
            badge="HIPOTECA · VIVIENDA"
        ),

        metric_row([
            ("25 años al 3%", fmt_eur(cuota_25)),
            ("30 años al 3%", fmt_eur(cuota_30)),
            ("35 años al 3%", fmt_eur(cuota_35)),
        ]),

        section("Cuota estimada", [
            html.P(f"Para una hipoteca de {fmt_eur(importe)}, la cuota mensual dependerá sobre todo del tipo de interés y del plazo."),
            html.P("Alargar el plazo baja la cuota mensual, pero normalmente aumenta los intereses totales pagados."),
        ]),

        table([
            ["Plazo", "Tipo", "Cuota mensual estimada"],
            ["25 años", "3%", fmt_eur(cuota_25)],
            ["30 años", "3%", fmt_eur(cuota_30)],
            ["35 años", "3%", fmt_eur(cuota_35)],
        ]),

        section("Qué debes mirar además de la cuota", [
            html.P("La cuota mensual es importante, pero no es lo único. También debes mirar intereses totales, entrada, impuestos, seguros, gastos de compraventa y esfuerzo financiero."),
            html.P("Una hipoteca cómoda no debería dejarte sin margen para ahorrar, invertir o afrontar imprevistos."),
        ]),

        related_links([
            ("Hipoteca de 150.000 €", "/cuanto-se-paga-de-hipoteca-por-150000-euros"),
            ("Hipoteca de 200.000 €", "/cuanto-se-paga-de-hipoteca-por-200000-euros"),
            ("Hipoteca de 300.000 €", "/cuanto-se-paga-de-hipoteca-por-300000-euros"),
            ("Comprar piso o invertir en bolsa", "/comprar-piso-para-alquilar-o-invertir-en-bolsa"),
        ]),

        cta_hipoteca(),
    ])


def build_invertir_edad_page(edad):
    anos_65 = max(65 - edad, 5)
    esc_300 = calc_compuesto(0, 300, 7, anos_65)
    esc_500 = calc_compuesto(0, 500, 7, anos_65)
    esc_1000 = calc_compuesto(0, 1000, 7, anos_65)

    return page_shell([
        hero(
            f"Cómo invertir a los {edad} años",
            f"Estrategia orientativa para empezar a invertir a los {edad}, con ejemplos de interés compuesto."
        ),

        metric_row([
            ("300 €/mes hasta 65", fmt_eur(esc_300[0])),
            ("500 €/mes hasta 65", fmt_eur(esc_500[0])),
            ("1.000 €/mes hasta 65", fmt_eur(esc_1000[0])),
        ]),

        section("Qué estrategia suele tener sentido", [
            html.P(f"A los {edad} años, el horizonte temporal es una de las variables más importantes."),
            html.P("Si inviertes a largo plazo, puedes aceptar más volatilidad que si necesitas el dinero pronto."),
        ]),

        table([
            ["Aportación mensual", f"Capital estimado a los 65 años"],
            ["300 €/mes", fmt_eur(esc_300[0])],
            ["500 €/mes", fmt_eur(esc_500[0])],
            ["1.000 €/mes", fmt_eur(esc_1000[0])],
        ]),

        section("Errores habituales", [
            html.P("Los errores más comunes son no empezar nunca, concentrar demasiado el dinero en una sola inversión, vender en caídas o cambiar de estrategia continuamente."),
            html.P("Una estrategia sencilla, automatizada y diversificada suele ser más sostenible."),
        ]),

        related_links([
            ("Invertir 300 € al mes", "/invertir-300-euros-mes"),
            ("Invertir 500 € al mes", "/invertir-500-euros-mes"),
            ("S&P 500 o MSCI World", "/sp500-o-msci-world"),
            ("Fondos indexados o ETFs", "/fondos-indexados-o-etfs"),
        ]),

        cta_calculadora(),
        cta_myinvestor(),
    ])


def build_alquiler_rentabilidad_page():
    return page_shell([
        hero(
            "Rentabilidad de alquiler de vivienda en España",
            "Cómo calcular si comprar un piso para alquilar puede ser rentable.",
            badge="VIVIENDA · ALQUILER"
        ),

        section("Qué debes calcular", [
            html.P("La rentabilidad real no es solo alquiler dividido entre precio de compra."),
            html.P("Debes incluir impuestos, comunidad, IBI, seguro, mantenimiento, vacancia, financiación y posibles reformas."),
        ]),

        table([
            ["Concepto", "Impacto"],
            ["IBI y comunidad", "Reduce la rentabilidad neta"],
            ["Vacancia", "Meses sin ingresos"],
            ["Hipoteca", "Puede aumentar o reducir el cashflow"],
            ["Reformas", "Aumentan inversión inicial"],
            ["Impuestos", "Reducen la rentabilidad final"],
        ]),

        section("Vivienda frente a bolsa", [
            html.P("La vivienda puede ser atractiva por el apalancamiento y el ingreso mensual, pero exige gestión y tiene menos liquidez."),
            html.P("La bolsa indexada suele ser más líquida, diversificada y pasiva, aunque más volátil a corto plazo."),
        ]),

        related_links([
            ("Comprar piso o invertir en bolsa", "/comprar-piso-para-alquilar-o-invertir-en-bolsa"),
            ("Invertir en vivienda o S&P 500", "/invertir-en-vivienda-o-sp500"),
            ("Calculadora alquiler", "/rentabilidad-alquiler"),
            ("Comparador de inversión", "/comparador"),
        ]),

        cta_alquiler(),
    ])


def build_vivienda_vs_bolsa_page():
    return page_shell([
        hero(
            "Comprar piso para alquilar o invertir en bolsa",
            "Comparativa entre inversión inmobiliaria y fondos indexados a largo plazo.",
            badge="VIVIENDA VS BOLSA"
        ),

        section("No gana siempre la vivienda ni siempre la bolsa", [
            html.P("La vivienda puede ofrecer apalancamiento, ingresos por alquiler y posible revalorización."),
            html.P("La bolsa suele ofrecer más liquidez, menos gestión y mayor diversificación."),
        ]),

        table([
            ["Opción", "Ventaja", "Desventaja"],
            ["Vivienda", "Apalancamiento e ingresos mensuales", "Gestión, gastos y poca liquidez"],
            ["Bolsa indexada", "Diversificación y liquidez", "Volatilidad y caídas temporales"],
        ]),

        section("Qué opción puede encajar mejor", [
            html.P("Si quieres una inversión más pasiva, diversificada y líquida, la bolsa puede ser más sencilla."),
            html.P("Si aceptas gestionar inquilinos, gastos, reformas y financiación, la vivienda puede tener sentido en buenas operaciones."),
        ]),

        related_links([
            ("Rentabilidad alquiler vivienda", "/rentabilidad-alquiler-vivienda-espana"),
            ("Invertir en vivienda o S&P 500", "/invertir-en-vivienda-o-sp500"),
            ("Invertir 500 € al mes", "/invertir-500-euros-mes"),
            ("Comparador de inversión", "/comparador"),
        ]),

        cta_comparador(),
    ])


def build_comparativa_page():
    return page_shell([
        hero(
            "Invertir en S&P 500 o Nasdaq 100",
            "Comparativa sencilla entre dos de los índices más populares para invertir a largo plazo."
        ),

        section("Diferencia principal", [
            html.P("El S&P 500 está más diversificado por sectores. El Nasdaq 100 tiene más peso tecnológico y suele ser más volátil."),
            html.P("Para muchos inversores, el S&P 500 puede ser una base más equilibrada, mientras que el Nasdaq puede servir como complemento si aceptas más riesgo."),
        ]),

        table([
            ["Índice", "Ventaja", "Riesgo"],
            ["S&P 500", "Más diversificado", "Menor exposición tecnológica"],
            ["Nasdaq 100", "Mayor exposición tecnológica", "Más volatilidad"],
        ]),

        related_links([
            ("S&P 500 o MSCI World", "/sp500-o-msci-world"),
            ("Fondos indexados o ETFs", "/fondos-indexados-o-etfs"),
            ("Invertir 500 € al mes", "/invertir-500-euros-mes"),
            ("MyInvestor opiniones", "/myinvestor-opiniones"),
        ]),

        cta_comparador(),
        cta_myinvestor(),
    ])


def build_comparativa_simple_page(slug):
    data = {
        "fondos-indexados-o-etfs": ("Fondos indexados o ETFs", "Comparativa entre fondos indexados y ETFs para invertir a largo plazo."),
        "fondos-indexados-o-deposito": ("Fondos indexados o depósito", "Comparativa entre buscar rentabilidad a largo plazo o priorizar seguridad y liquidez."),
        "sp500-o-msci-world": ("S&P 500 o MSCI World", "Comparativa entre invertir solo en Estados Unidos o diversificar globalmente."),
        "invertir-en-bolsa-o-amortizar-hipoteca": ("Invertir en bolsa o amortizar hipoteca", "Comparativa entre reducir deuda o buscar rentabilidad invirtiendo."),
    }

    title, desc = data.get(slug, ("Comparativa de inversión", "Comparativa práctica para tomar mejores decisiones de inversión."))

    return page_shell([
        hero(title, desc),

        section("Diferencia principal", [
            html.P("La mejor opción depende de tu horizonte temporal, tolerancia al riesgo, fiscalidad y necesidad de liquidez."),
            html.P("No hay una respuesta universal: lo importante es comparar escenarios con números."),
        ]),

        table([
            ["Opción", "Cuándo puede tener sentido"],
            ["Opción A", "Si buscas mayor potencial a largo plazo"],
            ["Opción B", "Si priorizas seguridad, liquidez o menor volatilidad"],
        ]),

        section("Cómo decidir", [
            html.P("Antes de elegir, conviene comparar rentabilidad esperada, riesgo, liquidez, impuestos y esfuerzo de gestión."),
            html.P("Una buena decisión no es necesariamente la más rentable en teoría, sino la que puedes mantener durante años."),
        ]),

        related_links([
            ("Invertir 500 € al mes", "/invertir-500-euros-mes"),
            ("S&P 500 o Nasdaq", "/invertir-en-sp500-o-nasdaq"),
            ("Dónde invertir 10.000 €", "/donde-invertir-10000-euros"),
            ("Comparador de inversión", "/comparador"),
        ]),

        cta_comparador(),
        cta_myinvestor(),
    ])


def build_myinvestor_page():
    return page_shell([
        hero(
            "MyInvestor opiniones: ¿merece la pena?",
            "Análisis práctico de MyInvestor para invertir en fondos indexados y gestionar tu dinero."
        ),

        section("Por qué muchos inversores usan MyInvestor", [
            html.P("MyInvestor se ha popularizado en España por ofrecer acceso a fondos indexados, carteras y productos de ahorro con costes competitivos."),
            html.P("Para un inversor que empieza, la ventaja principal es poder invertir de forma sencilla y automatizada."),
        ]),

        section("Cuándo puede tener sentido", [
            html.P("Puede tener sentido si quieres invertir a largo plazo, usar fondos indexados y mantener una estrategia sencilla."),
            html.P("No es una recomendación personalizada. Antes de invertir conviene entender riesgos, costes y fiscalidad."),
        ]),

        table([
            ["Punto", "Valoración"],
            ["Fondos indexados", "Interesante para inversión a largo plazo"],
            ["Simplicidad", "Buena opción para empezar"],
            ["Riesgo", "Depende de los productos elegidos"],
            ["Fiscalidad", "Conviene revisar cada caso"],
        ]),

        related_links([
            ("Invertir 500 € al mes", "/invertir-500-euros-mes"),
            ("Fondos indexados o ETFs", "/fondos-indexados-o-etfs"),
            ("S&P 500 o MSCI World", "/sp500-o-msci-world"),
            ("Dónde invertir 10.000 €", "/donde-invertir-10000-euros"),
        ]),

        cta_myinvestor(),
    ])

def build_alquiler_sat_page(slug):
    data = {
        "calcular-rentabilidad-piso-alquiler": {
            "title": "Cómo calcular la rentabilidad de un piso en alquiler",
            "desc": "Aprende a calcular rentabilidad bruta, neta, cashflow, gastos e hipoteca antes de comprar un piso para alquilar.",
        },
        "rentabilidad-bruta-neta-alquiler": {
            "title": "Rentabilidad bruta y neta de un alquiler",
            "desc": "Diferencias entre rentabilidad bruta y rentabilidad neta al analizar una vivienda en alquiler.",
        },
        "cashflow-inmobiliario": {
            "title": "Qué es el cashflow inmobiliario",
            "desc": "Calcula si un piso deja dinero cada mes después de gastos, impuestos e hipoteca.",
        },
        "gastos-comprar-piso-para-alquilar": {
            "title": "Gastos al comprar un piso para alquilar",
            "desc": "Lista de gastos que debes incluir antes de comprar una vivienda para ponerla en alquiler.",
        },
        "comprar-piso-para-alquilar-rentable": {
            "title": "Cómo saber si comprar un piso para alquilar es rentable",
            "desc": "Guía práctica para decidir si una operación inmobiliaria merece la pena.",
        },
        "rentabilidad-alquiler-con-hipoteca": {
            "title": "Rentabilidad de alquiler con hipoteca",
            "desc": "Cómo afecta la financiación a la rentabilidad, cashflow y riesgo de una vivienda en alquiler.",
        },
        "rentabilidad-alquiler-sin-hipoteca": {
            "title": "Rentabilidad de alquiler sin hipoteca",
            "desc": "Cómo calcular la rentabilidad neta de una vivienda comprada sin financiación.",
        },
        "como-saber-si-un-piso-es-rentable": {
            "title": "Cómo saber si un piso es rentable",
            "desc": "Checklist para analizar precio, alquiler, gastos, cashflow y rentabilidad neta.",
        },
    }

    info = data.get(slug, data["calcular-rentabilidad-piso-alquiler"])

    return page_shell([
        hero(
            info["title"],
            info["desc"],
            badge="INVERSIÓN INMOBILIARIA · ALQUILER"
        ),

        metric_row([
            ("Métrica principal", "Rentabilidad neta"),
            ("Riesgo clave", "Cashflow negativo"),
            ("Herramienta", "Calculadora"),
        ]),

        section("La rentabilidad real no es solo el alquiler mensual", [
            html.P(
                "Para analizar bien una vivienda en alquiler no basta con mirar el precio de compra y el alquiler mensual. "
                "También hay que incluir gastos de compra, reforma, impuestos, IBI, comunidad, seguro, mantenimiento, vacancia, gestión e hipoteca."
            ),
            html.P([
                "Puedes hacer el cálculo completo en la ",
                dcc.Link("calculadora de rentabilidad de alquiler", href="/rentabilidad-alquiler"),
                "."
            ]),
        ]),

        table([
            ["Concepto", "Por qué importa"],
            ["Precio de compra", "Marca la inversión principal"],
            ["Gastos de compra", "Aumentan el capital necesario"],
            ["Reforma", "Reduce rentabilidad inicial, pero puede aumentar alquiler"],
            ["Alquiler mensual", "Es la fuente principal de ingresos"],
            ["IBI y comunidad", "Reducen la rentabilidad neta"],
            ["Seguro y mantenimiento", "Evitan sorpresas en el cashflow"],
            ["Vacancia", "Meses sin cobrar alquiler"],
            ["Hipoteca", "Puede mejorar rentabilidad sobre capital, pero empeorar cashflow"],
        ]),

        section("Rentabilidad bruta, neta y cashflow", [
            html.P(
                "La rentabilidad bruta sirve como primer filtro, pero la rentabilidad neta es mucho más útil porque descuenta gastos reales."
            ),
            html.P(
                "El cashflow mensual es clave: te dice si la operación deja dinero cada mes o si tendrás que poner dinero de tu bolsillo."
            ),
        ]),

        table([
            ["Métrica", "Fórmula simple", "Para qué sirve"],
            ["Rentabilidad bruta", "Alquiler anual / inversión total", "Filtro rápido"],
            ["Rentabilidad neta", "Beneficio neto anual / inversión total", "Medir rentabilidad real"],
            ["Cashflow", "Ingresos - gastos - cuota", "Ver si deja dinero cada mes"],
            ["Rentabilidad sobre capital", "Beneficio / dinero aportado", "Analizar operaciones con hipoteca"],
        ]),

        section("Cuándo puede ser una buena operación", [
            html.P(
                "Una operación empieza a ser interesante cuando combina precio razonable, demanda de alquiler, gastos controlados, rentabilidad neta suficiente y cashflow positivo."
            ),
            html.P(
                "También conviene comparar el resultado frente a alternativas como bolsa indexada, fondos monetarios o amortizar deuda."
            ),
        ]),

        section("Errores habituales", [
            html.Ul([
                html.Li("No incluir impuestos y gastos de compra."),
                html.Li("Olvidar comunidad, IBI, seguro y mantenimiento."),
                html.Li("Suponer ocupación del 100% todos los años."),
                html.Li("No calcular cashflow después de hipoteca."),
                html.Li("No comparar contra bolsa u otras alternativas."),
                html.Li("Mirar solo rentabilidad bruta y no rentabilidad neta."),
            ])
        ]),

        cta_box(
            "Calcula tu caso exacto",
            "Introduce precio, alquiler, gastos, hipoteca e impuestos para calcular rentabilidad bruta, rentabilidad neta y cashflow.",
            "/rentabilidad-alquiler",
            "Abrir calculadora de alquiler"
        ),

        related_links([
            ("Rentabilidad alquiler vivienda España", "/rentabilidad-alquiler-vivienda-espana"),
            ("Comprar piso o invertir en bolsa", "/comprar-piso-para-alquilar-o-invertir-en-bolsa"),
            ("Invertir en vivienda o S&P 500", "/invertir-en-vivienda-o-sp500"),
            ("Calculadora de hipoteca", "/hipoteca"),
        ]),

        faq([
            ("¿Qué rentabilidad neta es buena en un alquiler?", "Depende de la zona y del riesgo, pero una rentabilidad neta superior al 5% suele ser más interesante que una operación por debajo del 3%."),
            ("¿Es mejor comprar con hipoteca?", "La hipoteca puede mejorar la rentabilidad sobre capital aportado, pero también aumenta riesgo y puede empeorar el cashflow mensual."),
            ("¿Qué es más importante: rentabilidad o cashflow?", "Las dos importan. La rentabilidad mide eficiencia; el cashflow mide si la operación deja dinero cada mes."),
            ("¿Dónde puedo calcularlo?", "Puedes usar la calculadora de rentabilidad de alquiler para simular precio, alquiler, gastos, impuestos e hipoteca."),
        ]),

        cta_alquiler(),
    ])
# =========================================================
# ROUTING
# =========================================================

def make_layout(cfg):
    tipo = cfg["tipo"]
    cantidad = cfg["cantidad"]

    if tipo == "alquiler_sat":
        return lambda **kwargs: build_alquiler_sat_page(cfg["slug"])

    if tipo == "aportacion":
        return lambda **kwargs: build_aportacion_page(cantidad)

    if tipo == "rentas":
        return lambda **kwargs: build_rentas_page(cantidad)

    if tipo == "objetivo":
        return lambda **kwargs: build_objetivo_page(cantidad)

    if tipo == "capital":
        return lambda **kwargs: build_capital_page(cantidad)

    if tipo == "fire_edad":
        return lambda **kwargs: build_fire_edad_page(cantidad)

    if tipo == "hipoteca_importe":
        return lambda **kwargs: build_hipoteca_importe_page(cantidad)

    if tipo == "invertir_edad":
        return lambda **kwargs: build_invertir_edad_page(cantidad)

    if tipo == "alquiler_rentabilidad":
        return lambda **kwargs: build_alquiler_rentabilidad_page()

    if tipo == "vivienda_vs_bolsa":
        return lambda **kwargs: build_vivienda_vs_bolsa_page()

    if tipo == "comparativa":
        return lambda **kwargs: build_comparativa_page()

    if tipo == "comparativa_simple":
        return lambda **kwargs: build_comparativa_simple_page(cfg["slug"])

    if tipo == "myinvestor":
        return lambda **kwargs: build_myinvestor_page()

    return lambda **kwargs: html.Div("Página no encontrada")
    


def make_title(cfg):
    tipo = cfg["tipo"]
    cantidad = cfg["cantidad"]

    if tipo == "alquiler_sat":
        titles = {
            "calcular-rentabilidad-piso-alquiler": "Calcular rentabilidad piso alquiler: guía y calculadora",
            "rentabilidad-bruta-neta-alquiler": "Rentabilidad bruta y neta alquiler: diferencias",
            "cashflow-inmobiliario": "Cashflow inmobiliario: qué es y cómo calcularlo",
            "gastos-comprar-piso-para-alquilar": "Gastos comprar piso para alquilar: lista completa",
            "comprar-piso-para-alquilar-rentable": "Comprar piso para alquilar: cómo saber si es rentable",
            "rentabilidad-alquiler-con-hipoteca": "Rentabilidad alquiler con hipoteca: cálculo real",
            "rentabilidad-alquiler-sin-hipoteca": "Rentabilidad alquiler sin hipoteca: cálculo neto",
            "como-saber-si-un-piso-es-rentable": "Cómo saber si un piso es rentable para alquilar",
        }
        return titles.get(cfg["slug"], "Rentabilidad alquiler: guía práctica")

    if tipo == "aportacion":
        return f"Invertir {cantidad} euros al mes: cuánto puedes ganar"

    if tipo == "rentas":
        return f"Cuánto dinero necesitas para vivir con {cantidad} euros al mes"

    if tipo == "objetivo":
        return f"Cómo conseguir {fmt_eur(cantidad)} invirtiendo: guía realista"

    if tipo == "capital":
        return f"Dónde invertir {fmt_eur(cantidad)}: opciones y simulación"

    if tipo == "fire_edad":
        return f"Cuánto dinero necesito para jubilarme a los {cantidad}"

    if tipo == "hipoteca_importe":
        return f"Cuánto se paga de hipoteca por {fmt_eur(cantidad)}"

    if tipo == "invertir_edad":
        return f"Cómo invertir a los {cantidad} años"

    if tipo == "alquiler_rentabilidad":
        return "Rentabilidad alquiler vivienda España: guía y cálculo"

    if tipo == "vivienda_vs_bolsa":
        return "Comprar piso para alquilar o invertir en bolsa"

    if tipo == "comparativa":
        return "Invertir en S&P 500 o Nasdaq 100: comparativa"

    if tipo == "comparativa_simple":
        titles = {
            "fondos-indexados-o-etfs": "Fondos indexados o ETFs: qué es mejor",
            "fondos-indexados-o-deposito": "Fondos indexados o depósito: comparativa",
            "sp500-o-msci-world": "S&P 500 o MSCI World: qué elegir",
            "invertir-en-bolsa-o-amortizar-hipoteca": "Invertir en bolsa o amortizar hipoteca",
        }
        return titles.get(cfg["slug"], "Comparativa de inversión")

    if tipo == "myinvestor":
        return "MyInvestor opiniones: análisis para invertir"

    return "Guía de inversión"


def make_description(cfg):
    tipo = cfg["tipo"]
    cantidad = cfg["cantidad"]

    if tipo == "aportacion":
        return f"Calcula cuánto podrías conseguir invirtiendo {cantidad} euros al mes a largo plazo."

    if tipo == "rentas":
        return f"Calcula cuánto patrimonio necesitas para vivir con {cantidad} euros mensuales de rentas."

    if tipo == "objetivo":
        return f"Simulación para alcanzar {fmt_eur(cantidad)} mediante ahorro mensual e interés compuesto."

    if tipo == "capital":
        return f"Ideas y simulación para invertir {fmt_eur(cantidad)} a largo plazo."

    if tipo == "fire_edad":
        return f"Calcula cuánto dinero necesitas para jubilarte a los {cantidad} años."

    if tipo == "hipoteca_importe":
        return f"Simula cuánto pagarías al mes por una hipoteca de {fmt_eur(cantidad)}."

    if tipo == "invertir_edad":
        return f"Guía práctica para empezar a invertir a los {cantidad} años."

    if tipo == "alquiler_rentabilidad":
        return "Aprende a calcular la rentabilidad real de una vivienda en alquiler."

    if tipo == "vivienda_vs_bolsa":
        return "Compara comprar vivienda para alquilar frente a invertir en bolsa."

    if tipo == "comparativa":
        return "Comparativa entre S&P 500 y Nasdaq 100 para inversión a largo plazo."

    if tipo == "comparativa_simple":
        return "Comparativa práctica para tomar mejores decisiones de inversión."

    if tipo == "myinvestor":
        return "Opiniones sobre MyInvestor, ventajas, límites y para qué tipo de inversor puede tener sentido."

    if tipo == "alquiler_sat":
        return "Guía práctica para calcular rentabilidad de alquiler, cashflow, gastos, hipoteca y rentabilidad neta de una vivienda."

    return "Guía de inversión."


# =========================================================
# REGISTER PAGES
# =========================================================

for cfg in SEO_PAGES:
    dash.register_page(
        module=f"pages.seo_programatico.{cfg['slug']}",
        path=f"/{cfg['slug']}",
        name=make_title(cfg),
        title=make_title(cfg),
        description=make_description(cfg),
        layout=make_layout(cfg),
    )
