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


# =========================================================
# CONFIG SEO PAGES
# =========================================================

SEO_PAGES = [
    # Alto potencial: invertir X al mes
    {"slug": "invertir-100-euros-mes", "tipo": "aportacion", "cantidad": 100},
    {"slug": "invertir-200-euros-mes", "tipo": "aportacion", "cantidad": 200},
    {"slug": "invertir-300-euros-mes", "tipo": "aportacion", "cantidad": 300},
    {"slug": "invertir-500-euros-mes", "tipo": "aportacion", "cantidad": 500},
    {"slug": "invertir-700-euros-mes", "tipo": "aportacion", "cantidad": 700},
    {"slug": "invertir-1000-euros-mes", "tipo": "aportacion", "cantidad": 1000},

    # Alto potencial: vivir de rentas
    {"slug": "cuanto-dinero-necesitas-para-vivir-de-rentas-en-espana", "tipo": "rentas", "cantidad": 2000},
    {"slug": "cuanto-dinero-necesitas-para-vivir-con-1000-euros-mes", "tipo": "rentas", "cantidad": 1000},
    {"slug": "cuanto-dinero-necesitas-para-vivir-con-1500-euros-mes", "tipo": "rentas", "cantidad": 1500},
    {"slug": "cuanto-dinero-necesitas-para-vivir-con-2000-euros-mes", "tipo": "rentas", "cantidad": 2000},
    {"slug": "cuanto-dinero-necesitas-para-vivir-con-3000-euros-mes", "tipo": "rentas", "cantidad": 3000},

    # Objetivos de patrimonio
    {"slug": "como-conseguir-100000-euros", "tipo": "objetivo", "cantidad": 100000},
    {"slug": "como-conseguir-200000-euros", "tipo": "objetivo", "cantidad": 200000},
    {"slug": "como-conseguir-500000-euros", "tipo": "objetivo", "cantidad": 500000},
    {"slug": "como-conseguir-un-millon-de-euros", "tipo": "objetivo", "cantidad": 1000000},

    # Capital inicial
    {"slug": "donde-invertir-1000-euros", "tipo": "capital", "cantidad": 1000},
    {"slug": "donde-invertir-5000-euros", "tipo": "capital", "cantidad": 5000},
    {"slug": "donde-invertir-10000-euros", "tipo": "capital", "cantidad": 10000},
    {"slug": "donde-invertir-50000-euros", "tipo": "capital", "cantidad": 50000},

    # Comparativas con potencial
    {"slug": "invertir-en-sp500-o-nasdaq", "tipo": "comparativa", "cantidad": 0},
    {"slug": "myinvestor-opiniones", "tipo": "myinvestor", "cantidad": 0},
]


# =========================================================
# CONTENT GENERATORS
# =========================================================

def build_aportacion_page(cantidad):
    esc_10 = calc_compuesto(0, cantidad, 7, 10)
    esc_20 = calc_compuesto(0, cantidad, 7, 20)
    esc_30 = calc_compuesto(0, cantidad, 7, 30)

    title = f"¿Qué pasa si inviertes {cantidad} € al mes?"
    description = f"Simulación de cuánto podrías acumular invirtiendo {cantidad} € mensuales a largo plazo con interés compuesto."

    return html.Div([
        hero(title, description),

        metric_row([
            ("10 años", fmt_eur(esc_10[0])),
            ("20 años", fmt_eur(esc_20[0])),
            ("30 años", fmt_eur(esc_30[0])),
        ]),

        section("Resultado de invertir cada mes", [
            html.P(f"Si inviertes {cantidad} € al mes durante varios años, el interés compuesto puede hacer que el resultado final sea muy superior al dinero aportado."),
            html.P(f"Con una rentabilidad media estimada del 7% anual, podrías llegar aproximadamente a {fmt_eur(esc_30[0])} en 30 años."),
        ]),

        table([
            ["Horizonte", "Capital final", "Dinero aportado", "Ganancia estimada"],
            ["10 años", fmt_eur(esc_10[0]), fmt_eur(esc_10[1]), fmt_eur(esc_10[2])],
            ["20 años", fmt_eur(esc_20[0]), fmt_eur(esc_20[1]), fmt_eur(esc_20[2])],
            ["30 años", fmt_eur(esc_30[0]), fmt_eur(esc_30[1]), fmt_eur(esc_30[2])],
        ]),

        section("¿Dónde puedes invertir esa cantidad?", [
            html.P("Una opción habitual para inversión a largo plazo son fondos indexados globales, S&P 500, MSCI World o carteras diversificadas."),
            html.P("La clave no es acertar el mejor momento, sino mantener constancia, costes bajos y un horizonte largo."),
        ]),

        cta_calculadora(),
        cta_myinvestor(),
    ])


def build_rentas_page(renta):
    capital_4 = capital_necesario_para_renta(renta, 0.04)
    capital_35 = capital_necesario_para_renta(renta, 0.035)
    capital_3 = capital_necesario_para_renta(renta, 0.03)

    title = f"Cuánto dinero necesitas para vivir con {renta} € al mes"
    description = f"Calcula cuánto patrimonio necesitas para generar {renta} € mensuales de forma aproximada."

    return html.Div([
        hero(title, description),

        metric_row([
            ("Regla 4%", fmt_eur(capital_4)),
            ("Regla 3,5%", fmt_eur(capital_35)),
            ("Regla 3%", fmt_eur(capital_3)),
        ]),

        section("Capital necesario para vivir de rentas", [
            html.P(f"Para generar unos {renta} € al mes, necesitarías aproximadamente entre {fmt_eur(capital_4)} y {fmt_eur(capital_3)}, dependiendo de la rentabilidad, inflación, impuestos y margen de seguridad."),
            html.P("La regla del 4% es una referencia habitual, pero no debe tomarse como una garantía. En España conviene ser algo más conservador por impuestos e inflación."),
        ]),

        table([
            ["Escenario", "Tasa de retirada", "Capital necesario"],
            ["Agresivo", "4%", fmt_eur(capital_4)],
            ["Intermedio", "3,5%", fmt_eur(capital_35)],
            ["Conservador", "3%", fmt_eur(capital_3)],
        ]),

        section("Cómo llegar a esa cifra", [
            html.P("El camino habitual combina ahorro mensual, inversión indexada, tiempo e ingresos adicionales."),
            html.P("Cuanto antes empiezas, menos esfuerzo mensual necesitas gracias al interés compuesto."),
        ]),

        cta_fire(),
        cta_myinvestor(),
    ])


def build_objetivo_page(objetivo):
    escenarios_10 = [
        ("300 €/mes", calc_compuesto(0, 300, 7, 10)[0]),
        ("500 €/mes", calc_compuesto(0, 500, 7, 10)[0]),
        ("700 €/mes", calc_compuesto(0, 700, 7, 10)[0]),
        ("1.000 €/mes", calc_compuesto(0, 1000, 7, 10)[0]),
    ]

    escenarios_20 = [
        ("300 €/mes", calc_compuesto(0, 300, 7, 20)[0]),
        ("500 €/mes", calc_compuesto(0, 500, 7, 20)[0]),
        ("700 €/mes", calc_compuesto(0, 700, 7, 20)[0]),
        ("1.000 €/mes", calc_compuesto(0, 1000, 7, 20)[0]),
    ]

    escenarios_30 = [
        ("300 €/mes", calc_compuesto(0, 300, 7, 30)[0]),
        ("500 €/mes", calc_compuesto(0, 500, 7, 30)[0]),
        ("700 €/mes", calc_compuesto(0, 700, 7, 30)[0]),
        ("1.000 €/mes", calc_compuesto(0, 1000, 7, 30)[0]),
    ]

    title = f"Cómo conseguir {fmt_eur(objetivo)} invirtiendo"
    description = (
        f"Guía realista para alcanzar {fmt_eur(objetivo)} mediante ahorro mensual, "
        "inversión a largo plazo e interés compuesto."
    )

    return html.Div([
        hero(title, description),

        metric_row([
            ("A 10 años con 500 €/mes", fmt_eur(calc_compuesto(0, 500, 7, 10)[0])),
            ("A 20 años con 500 €/mes", fmt_eur(calc_compuesto(0, 500, 7, 20)[0])),
            ("A 30 años con 500 €/mes", fmt_eur(calc_compuesto(0, 500, 7, 30)[0])),
        ]),

        section("¿Es posible alcanzar este objetivo?", [
            html.P(
                f"Sí, conseguir {fmt_eur(objetivo)} es posible, pero depende sobre todo "
                "de tres factores: cuánto dinero inviertes cada mes, durante cuántos años "
                "mantienes la inversión y qué rentabilidad media consigues."
            ),
            html.P(
                "El interés compuesto empieza lento, pero con el paso del tiempo el crecimiento "
                "se acelera. Por eso, empezar antes suele ser más importante que intentar encontrar "
                "la inversión perfecta."
            ),
            html.P([
                "Puedes ajustar estos cálculos con tus propios datos en la ",
                dcc.Link("calculadora de interés compuesto", href="/calculadora"),
                "."
            ]),
        ]),

        section(f"Cuánto podrías acumular invirtiendo cada mes", [
            html.P(
                "La siguiente tabla muestra una simulación orientativa usando una rentabilidad media "
                "del 7% anual. No es una garantía, pero sirve para entender el impacto del tiempo."
            ),
        ]),

        table([
            ["Aportación mensual", "A 10 años", "A 20 años", "A 30 años"],
            [
                "300 €/mes",
                fmt_eur(escenarios_10[0][1]),
                fmt_eur(escenarios_20[0][1]),
                fmt_eur(escenarios_30[0][1]),
            ],
            [
                "500 €/mes",
                fmt_eur(escenarios_10[1][1]),
                fmt_eur(escenarios_20[1][1]),
                fmt_eur(escenarios_30[1][1]),
            ],
            [
                "700 €/mes",
                fmt_eur(escenarios_10[2][1]),
                fmt_eur(escenarios_20[2][1]),
                fmt_eur(escenarios_30[2][1]),
            ],
            [
                "1.000 €/mes",
                fmt_eur(escenarios_10[3][1]),
                fmt_eur(escenarios_20[3][1]),
                fmt_eur(escenarios_30[3][1]),
            ],
        ]),

        section("¿Cuánto tiempo se tarda en conseguir esa cantidad?", [
            html.P(
                f"Para llegar a {fmt_eur(objetivo)}, el tiempo necesario cambia mucho según la "
                "aportación mensual. Una persona que invierte 300 € al mes necesitará bastante más "
                "tiempo que alguien que puede invertir 700 € o 1.000 € mensuales."
            ),
            html.P(
                "La clave no es solo ahorrar más, sino mantener el hábito durante muchos años. "
                "En objetivos grandes, el tiempo trabaja a favor del inversor paciente."
            ),
            html.P([
                "También puedes ver escenarios específicos como ",
                dcc.Link("invertir 500 € al mes", href="/invertir-500-euros-mes"),
                " o ",
                dcc.Link("invertir 1.000 € al mes", href="/invertir-1000-euros-mes"),
                "."
            ]),
        ]),

        section("Qué pasa si empiezas más tarde", [
            html.P(
                "Retrasar la inversión puede tener un coste importante. Si empiezas cinco o diez años "
                "más tarde, necesitarás aportar bastante más dinero al mes para llegar al mismo objetivo."
            ),
            html.P(
                "Esto ocurre porque pierdes años de crecimiento compuesto. Al principio parece que la "
                "diferencia es pequeña, pero a largo plazo puede ser enorme."
            ),
        ]),

        section("¿Qué rentabilidad es realista?", [
            html.P(
                "Una rentabilidad media del 7% anual suele usarse como referencia histórica razonable "
                "para inversión en bolsa global o índices amplios a largo plazo, aunque ningún resultado "
                "está garantizado."
            ),
            html.P(
                "Habrá años muy buenos, años malos y caídas fuertes. Por eso es importante invertir con "
                "horizonte largo, diversificar y no depender de ese dinero a corto plazo."
            ),
        ]),

        section("Estrategia sencilla para alcanzar el objetivo", [
            html.P(
                "Una estrategia realista podría consistir en invertir cada mes una cantidad fija, usar "
                "productos diversificados de bajo coste y revisar el plan una o dos veces al año."
            ),
            html.P(
                "Para la mayoría de personas, la constancia, el ahorro automático y los costes bajos "
                "son más importantes que intentar adivinar cuándo subirá o bajará el mercado."
            ),
        ]),

        cta_calculadora(),

        section("Preguntas frecuentes", [
            html.H3(f"¿Es posible conseguir {fmt_eur(objetivo)} sin invertir?", className="fw-bold mt-4"),
            html.P(
                "Sí, pero normalmente sería más lento, porque dependerías solo del ahorro. La inversión "
                "puede acelerar el proceso gracias al interés compuesto."
            ),

            html.H3("¿Qué pasa si el mercado cae?", className="fw-bold mt-4"),
            html.P(
                "Las caídas forman parte de la inversión. Por eso conviene invertir con horizonte largo, "
                "diversificar y no usar dinero que puedas necesitar en pocos años."
            ),

            html.H3("¿Es mejor invertir poco a poco o todo de golpe?", className="fw-bold mt-4"),
            html.P(
                "Invertir poco a poco ayuda psicológicamente y reduce el riesgo de entrar justo antes de "
                "una caída. Invertir todo de golpe puede ser más rentable si el mercado sube, pero exige "
                "más tolerancia al riesgo."
            ),

            html.H3("¿Dónde puedo simular mi caso concreto?", className="fw-bold mt-4"),
            html.P([
                "Puedes usar la ",
                dcc.Link("calculadora de interés compuesto", href="/calculadora"),
                " para cambiar capital inicial, aportación mensual, rentabilidad, inflación y horizonte temporal."
            ]),
        ]),

        section("Otras guías relacionadas", [
            html.Ul([
                html.Li(dcc.Link("Invertir 300 € al mes", href="/invertir-300-euros-mes")),
                html.Li(dcc.Link("Invertir 500 € al mes", href="/invertir-500-euros-mes")),
                html.Li(dcc.Link("Invertir 1.000 € al mes", href="/invertir-1000-euros-mes")),
                html.Li(dcc.Link("Cuánto dinero necesitas para vivir con 2.000 € al mes", href="/cuanto-dinero-necesitas-para-vivir-con-2000-euros-mes")),
            ])
        ]),

        cta_myinvestor(),
    ])


def build_capital_page(cantidad):
    esc_10 = calc_compuesto(cantidad, 0, 7, 10)
    esc_20 = calc_compuesto(cantidad, 0, 7, 20)
    esc_30 = calc_compuesto(cantidad, 0, 7, 30)

    title = f"Dónde invertir {fmt_eur(cantidad)}"
    description = f"Ideas y simulación para invertir {fmt_eur(cantidad)} a largo plazo."

    return html.Div([
        hero(title, description),

        section("Opciones para invertir ese dinero", [
            html.P(f"Si tienes {fmt_eur(cantidad)} para invertir, una opción sencilla es usar fondos indexados o ETFs diversificados."),
            html.P("La decisión depende de tu plazo, tolerancia al riesgo y necesidad de liquidez."),
        ]),

        table([
            ["Horizonte", "Capital estimado al 7% anual"],
            ["10 años", fmt_eur(esc_10[0])],
            ["20 años", fmt_eur(esc_20[0])],
            ["30 años", fmt_eur(esc_30[0])],
        ]),

        cta_calculadora(),
        cta_myinvestor(),
    ])


def build_comparativa_page():
    return html.Div([
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
            ["S&P 500", "Más diversificado", "Menor potencial relativo que Nasdaq"],
            ["Nasdaq 100", "Mayor exposición tecnológica", "Más volatilidad"],
        ]),
        cta_comparador(),
        cta_myinvestor(),
    ])


def build_myinvestor_page():
    return html.Div([
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
        cta_myinvestor(),
    ])


# =========================================================
# COMPONENTS
# =========================================================

def hero(title, description):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div("GUÍA DE INVERSIÓN", className="text-uppercase fw-bold mb-3", style={
                    "letterSpacing": "0.08em",
                    "color": "#667085",
                    "fontSize": "0.85rem",
                }),
                html.H1(title, className="fw-bold mb-3", style={
                    "fontSize": "clamp(2.1rem, 5vw, 4rem)",
                    "lineHeight": "1.05",
                }),
                html.P(description, className="lead text-muted", style={
                    "maxWidth": "760px",
                    "fontSize": "1.15rem",
                }),
            ], lg=10)
        ])
    ], className="py-5")


def section(title, children):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2(title, className="fw-bold mb-3"),
                html.Div(children, className="text-muted fs-5"),
            ], lg=9)
        ])
    ], className="py-4")


def metric_row(items):
    return dbc.Container([
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        html.Div(label, className="text-muted mb-2"),
                        html.H3(value, className="fw-bold mb-0"),
                    ]),
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
                dbc.Table([
                    html.Thead(html.Tr([html.Th(x) for x in header])),
                    html.Tbody([
                        html.Tr([html.Td(x) for x in row])
                        for row in body
                    ])
                ], bordered=False, hover=True, responsive=True, className="align-middle")
            ], lg=10)
        ])
    ], className="py-4")


def cta_calculadora():
    return cta_box(
        "Simula tu caso exacto",
        "Usa la calculadora de interés compuesto para ajustar capital inicial, aportaciones, rentabilidad e inflación.",
        "/calculadora",
        "Abrir calculadora"
    )


def cta_fire():
    return cta_box(
        "Calcula tu número FIRE",
        "Descubre cuánto necesitas para vivir de tus inversiones según tus gastos mensuales.",
        "/fire",
        "Abrir calculadora FIRE"
    )


def cta_comparador():
    return cta_box(
        "Compara inversiones",
        "Compara bolsa, vivienda, monetarios y otras alternativas según tu horizonte.",
        "/comparador",
        "Abrir comparador"
    )


def cta_myinvestor():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.Div("ENLACE DE AFILIADO", className="text-uppercase fw-bold mb-2", style={
                            "fontSize": "0.75rem",
                            "letterSpacing": "0.08em",
                            "color": "#667085",
                        }),
                        html.H3("Empieza a invertir con MyInvestor", className="fw-bold"),
                        html.P("Puedes abrir cuenta y explorar fondos indexados, carteras y productos de inversión."),
                        dbc.Button("Ver MyInvestor", href=MYINVESTOR_URL, target="_blank", color="dark"),
                    ]),
                    className="border-0 shadow-sm rounded-4"
                )
            ], lg=9)
        ])
    ], className="py-4")


def cta_box(title, text, href, button):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card(
                    dbc.CardBody([
                        html.H3(title, className="fw-bold"),
                        html.P(text, className="text-muted"),
                        dbc.Button(button, href=href, color="primary"),
                    ]),
                    className="border-0 shadow-sm rounded-4"
                )
            ], lg=9)
        ])
    ], className="py-4")


# =========================================================
# PAGE FACTORY
# =========================================================

def make_layout(cfg):
    tipo = cfg["tipo"]
    cantidad = cfg["cantidad"]

    if tipo == "aportacion":
        return lambda **kwargs: build_aportacion_page(cantidad)

    if tipo == "rentas":
        return lambda **kwargs: build_rentas_page(cantidad)

    if tipo == "objetivo":
        return lambda **kwargs: build_objetivo_page(cantidad)

    if tipo == "capital":
        return lambda **kwargs: build_capital_page(cantidad)

    if tipo == "comparativa":
        return lambda **kwargs: build_comparativa_page()

    if tipo == "myinvestor":
        return lambda **kwargs: build_myinvestor_page()

    return lambda **kwargs: html.Div("Página no encontrada")


def make_title(cfg):
    tipo = cfg["tipo"]
    cantidad = cfg["cantidad"]

    if tipo == "aportacion":
        return f"Invertir {cantidad} euros al mes: cuánto puedes ganar"

    if tipo == "rentas":
        return f"Cuánto dinero necesitas para vivir con {cantidad} euros al mes"

    if tipo == "objetivo":
        return f"Cómo conseguir {fmt_eur(cantidad)} invirtiendo: guía realista"

    if tipo == "capital":
        return f"Dónde invertir {fmt_eur(cantidad)}: opciones y simulación"

    if tipo == "comparativa":
        return "Invertir en S&P 500 o Nasdaq 100: comparativa"

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

    if tipo == "comparativa":
        return "Comparativa entre S&P 500 y Nasdaq 100 para inversión a largo plazo."

    if tipo == "myinvestor":
        return "Opiniones sobre MyInvestor, ventajas, límites y para qué tipo de inversor puede tener sentido."

    return "Guía de inversión."


# =========================================================
# REGISTER PROGRAMMATIC PAGES
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
