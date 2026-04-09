import dash
from dash import html
import dash_bootstrap_components as dbc

from components.disclaimer_afiliados import build_disclaimer

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/blog/cuanto-dinero-necesitas-para-vivir-de-rentas-en-espana",
    title="Cuánto dinero necesitas para vivir de rentas en España (2026)",
    name="Cuánto dinero necesitas para vivir de rentas en España",
    description=(
        "Descubre cuánto dinero necesitas para vivir de rentas en España. "
        "Calcula tu independencia financiera con ejemplos reales y simulador."
    ),
)


# =========================================================
# HELPERS
# =========================================================
def article_container(children):
    return dbc.Container(
        children,
        class_name="py-4 py-md-5",
        style={"maxWidth": "860px"},
    )


def section_title(title, subtitle=None):
    return html.Div(
        [
            html.H2(title, className="fw-bold mb-2"),
            html.P(subtitle, className="text-muted mb-0") if subtitle else None,
        ],
        className="mb-4 mt-5",
    )


def paragraph(text):
    return html.P(
        text,
        className="mb-3",
        style={"fontSize": "1.08rem", "lineHeight": "1.85"},
    )


def bullet_list(items):
    return html.Ul(
        [html.Li(item, className="mb-2") for item in items],
        className="mb-4",
        style={"fontSize": "1.05rem", "lineHeight": "1.8"},
    )


def callout_box(title, children, color="#f8fafc", border="#dbe4f0"):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    title,
                    className="fw-bold mb-3",
                    style={"fontSize": "1.1rem", "color": "#101828"},
                ),
                children,
            ]
        ),
        class_name="border-0 shadow-sm mb-4",
        style={
            "background": color,
            "border": f"1px solid {border}",
            "borderRadius": "20px",
        },
    )


def cta_block(title, text, button_text, href, button_color="primary"):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(
                    title,
                    className="fw-bold mb-2",
                    style={"fontSize": "1.15rem", "color": "#101828"},
                ),
                html.P(
                    text,
                    className="text-muted mb-3",
                    style={"fontSize": "1rem", "lineHeight": "1.7"},
                ),
                dbc.Button(
                    button_text,
                    href=href,
                    color=button_color,
                    class_name="rounded-pill px-4 fw-semibold",
                    target="_blank" if href.startswith("http") else None,
                    rel="sponsored noopener noreferrer" if href.startswith("http") else None,
                ),
            ]
        ),
        class_name="border-0 shadow-sm my-4",
        style={
            "borderRadius": "22px",
            "background": "linear-gradient(180deg, #ffffff 0%, #f8fafc 100%)",
        },
    )


def quick_table():
    rows = [
        ("1.000€", "12.000€", "300.000€"),
        ("1.500€", "18.000€", "450.000€"),
        ("2.000€", "24.000€", "600.000€"),
        ("3.000€", "36.000€", "900.000€"),
    ]

    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Gastos mensuales"),
                        html.Th("Gastos anuales"),
                        html.Th("Patrimonio aproximado necesario"),
                    ]
                )
            ),
            html.Tbody(
                [
                    html.Tr(
                        [
                            html.Td(gasto_mes),
                            html.Td(gasto_anual),
                            html.Td(patrimonio),
                        ]
                    )
                    for gasto_mes, gasto_anual, patrimonio in rows
                ]
            ),
        ],
        bordered=False,
        hover=True,
        responsive=True,
        class_name="align-middle mb-0",
        style={"fontSize": "1rem"},
    )


# =========================================================
# SEO / JSON-LD
# =========================================================
json_ld_article = {
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "Cuánto dinero necesitas para vivir de rentas en España (2026)",
    "description": (
        "Descubre cuánto dinero necesitas para vivir de rentas en España. "
        "Calcula tu independencia financiera con ejemplos reales y simulador."
    ),
    "author": {
        "@type": "Organization",
        "name": "interescompuesto.app",
    },
    "publisher": {
        "@type": "Organization",
        "name": "interescompuesto.app",
    },
    "mainEntityOfPage": {
        "@type": "WebPage",
        "@id": "https://interescompuesto.app/blog/cuanto-dinero-necesitas-para-vivir-de-rentas-en-espana",
    },
}

json_ld_breadcrumb = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "Inicio",
            "item": "https://interescompuesto.app/",
        },
        {
            "@type": "ListItem",
            "position": 2,
            "name": "Blog",
            "item": "https://interescompuesto.app/blog",
        },
        {
            "@type": "ListItem",
            "position": 3,
            "name": "Cuánto dinero necesitas para vivir de rentas en España",
            "item": "https://interescompuesto.app/blog/cuanto-dinero-necesitas-para-vivir-de-rentas-en-espana",
        },
    ],
}

json_ld_faq = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
        {
            "@type": "Question",
            "name": "¿Cuánto dinero necesito para vivir de rentas en España?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": (
                    "Depende de tus gastos anuales. Una referencia habitual es la regla del 4%, "
                    "que estima el patrimonio necesario dividiendo tus gastos anuales entre 0,04."
                ),
            },
        },
        {
            "@type": "Question",
            "name": "¿Se puede vivir de rentas con fondos indexados?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": (
                    "Sí, muchas estrategias de independencia financiera se basan en una cartera "
                    "diversificada de fondos indexados a largo plazo."
                ),
            },
        },
        {
            "@type": "Question",
            "name": "¿Qué es la regla del 4%?",
            "acceptedAnswer": {
                "@type": "Answer",
                "text": (
                    "Es una referencia popular para estimar cuánto patrimonio necesitas para retirar "
                    "aproximadamente un 4% al año y cubrir tus gastos."
                ),
            },
        },
    ],
}


# =========================================================
# LAYOUT
# =========================================================
layout = html.Div(
    [
        html.Script(type="application/ld+json", children=str(json_ld_article).replace("'", '"')),
        html.Script(type="application/ld+json", children=str(json_ld_breadcrumb).replace("'", '"')),
        html.Script(type="application/ld+json", children=str(json_ld_faq).replace("'", '"')),

        article_container(
            [
                dbc.Breadcrumb(
                    items=[
                        {"label": "Inicio", "href": "/"},
                        {"label": "Blog", "href": "/blog"},
                        {
                            "label": "Vivir de rentas en España",
                            "active": True,
                        },
                    ],
                    class_name="mb-4",
                ),

                html.Div(
                    "INDEPENDENCIA FINANCIERA",
                    className="small fw-bold text-primary mb-3",
                    style={"letterSpacing": "0.08em"},
                ),

                html.H1(
                    "Cuánto dinero necesitas para vivir de rentas en España (calculadora incluida)",
                    className="fw-bold mb-3",
                    style={
                        "fontSize": "clamp(2rem, 5vw, 3.2rem)",
                        "lineHeight": "1.08",
                        "letterSpacing": "-0.03em",
                        "color": "#101828",
                    },
                ),

                html.P(
                    "Descubre cuánto patrimonio necesitas para cubrir tus gastos con tus inversiones, "
                    "con ejemplos reales, regla del 4% y simulador gratuito.",
                    className="text-muted mb-4",
                    style={"fontSize": "1.12rem", "lineHeight": "1.8"},
                ),

                callout_box(
                    "Qué vas a ver en este artículo",
                    bullet_list(
                        [
                            "Cuánto dinero necesitas realmente para vivir de rentas en España.",
                            "Cómo usar la regla del 4% con ejemplos sencillos.",
                            "Qué estrategia suele usar la gente que busca la independencia financiera.",
                            "Cómo calcular tu caso exacto con una calculadora gratuita.",
                        ]
                    ),
                ),

                paragraph(
                    "¿Te has preguntado alguna vez cuánto dinero necesitas para dejar de trabajar "
                    "y vivir de tus inversiones? La idea de vivir de rentas, o alcanzar la "
                    'independencia financiera, no es solo para personas con un patrimonio enorme. '
                    "Con tiempo, constancia y una estrategia razonable, es un objetivo que se puede planificar."
                ),

                paragraph(
                    "La clave está en entender cuánto gastas, cuánto patrimonio necesitas y cuánto "
                    "tiempo tardarías en construirlo. A partir de ahí, ya puedes tomar decisiones "
                    "mucho más realistas."
                ),

                section_title("Cuánto dinero necesitas para vivir de rentas"),

                paragraph(
                    "La referencia más conocida para hacer este cálculo es la llamada regla del 4%. "
                    "No es una garantía matemática, pero sí un punto de partida muy útil para estimar "
                    "el patrimonio necesario."
                ),

                callout_box(
                    "Fórmula básica",
                    html.Div(
                        [
                            html.Div(
                                "Patrimonio necesario = gastos anuales ÷ 0,04",
                                className="fw-bold",
                                style={"fontSize": "1.25rem", "color": "#101828"},
                            ),
                            html.Div(
                                "Ejemplo: si gastas 24.000€ al año, necesitarías alrededor de 600.000€.",
                                className="text-muted mt-2",
                            ),
                        ]
                    ),
                    color="#eef4ff",
                    border="#d7e6ff",
                ),

                paragraph(
                    "La idea detrás de esta regla es que, si tu cartera está bien diversificada, "
                    "podrías retirar aproximadamente un 4% al año para cubrir tus gastos sin agotar "
                    "tu patrimonio demasiado rápido."
                ),

                section_title("Ejemplos reales según tus gastos"),

                html.Div(
                    quick_table(),
                    className="mb-4",
                ),

                paragraph(
                    "Por ejemplo, si tus gastos son de 1.500€ al mes, estaríamos hablando de unos "
                    "18.000€ al año. Aplicando la regla del 4%, necesitarías unos 450.000€ invertidos."
                ),

                paragraph(
                    "Si quisieras vivir con 2.000€ al mes, el objetivo subiría a unos 600.000€. "
                    "Y si tu estilo de vida requiere 3.000€ mensuales, ya estaríamos más cerca "
                    "de los 900.000€."
                ),

                cta_block(
                    "Calcula tu número FIRE en 1 minuto",
                    "Usa la calculadora FIRE para estimar cuánto dinero necesitas, cuánto tardarías "
                    "en conseguirlo y cómo cambia el resultado si ahorras más o empiezas antes.",
                    "Ir a la calculadora FIRE",
                    "/fire",
                    "primary",
                ),

                section_title("Cuánto tardas en conseguirlo"),

                paragraph(
                    "Una vez sabes tu objetivo, la siguiente pregunta es cuánto tardarías en llegar. "
                    "Aquí entran en juego tres variables principales: tu ahorro mensual, la rentabilidad "
                    "media de tu cartera y el tiempo."
                ),

                bullet_list(
                    [
                        "Ahorro mensual: cuanto más ahorres, más rápido avanzas.",
                        "Rentabilidad: una cartera invertida suele crecer más que el dinero parado.",
                        "Tiempo: empezar antes marca una diferencia enorme.",
                    ]
                ),

                callout_box(
                    "Ejemplo sencillo",
                    html.Div(
                        [
                            html.P(
                                "Si inviertes 500€ al mes durante 30 años con una rentabilidad media del 7%, "
                                "podrías acumular alrededor de 600.000€.",
                                className="mb-2",
                                style={"fontSize": "1.05rem", "lineHeight": "1.8"},
                            ),
                            html.P(
                                "Eso significa que una estrategia constante puede acercarte de verdad a vivir de rentas, "
                                "aunque hoy no partas de una gran cantidad.",
                                className="mb-0 text-muted",
                            ),
                        ]
                    ),
                ),

                cta_block(
                    "Simula cuánto puede crecer tu dinero",
                    "Si quieres ver el efecto del interés compuesto sobre tu patrimonio, prueba la "
                    "calculadora y ajusta aportaciones, rentabilidad, inflación y plazo.",
                    "Abrir calculadora de interés compuesto",
                    "/calculadora",
                    "secondary",
                ),

                section_title("Cómo invertir para vivir de rentas"),

                paragraph(
                    "Ahorrar es importante, pero por sí solo suele ser insuficiente para construir un patrimonio "
                    "grande. Por eso muchas personas que buscan independencia financiera se apoyan en una "
                    "estrategia de inversión a largo plazo."
                ),

                paragraph(
                    "Una de las opciones más extendidas es invertir en fondos indexados globales de bajo coste. "
                    "La lógica es sencilla: diversificación, bajas comisiones y disciplina durante muchos años."
                ),

                bullet_list(
                    [
                        "Invertir de forma periódica todos los meses.",
                        "Reducir comisiones y evitar productos complejos.",
                        "Mantener una cartera diversificada.",
                        "Pensar a largo plazo y no en movimientos de corto plazo.",
                    ]
                ),

                section_title("Dónde invertir en España para empezar"),

                paragraph(
                    "Si estás empezando, lo más importante es que la plataforma sea sencilla, barata "
                    "y te permita automatizar la inversión sin demasiadas fricciones."
                ),

                callout_box(
                    "Opción práctica para empezar",
                    html.Div(
                        [
                            html.P(
                                "MyInvestor suele ser una de las plataformas que más interés despierta "
                                "entre quienes quieren invertir en fondos indexados en España.",
                                className="mb-2",
                                style={"fontSize": "1.05rem", "lineHeight": "1.8"},
                            ),
                            html.P(
                                "Puede tener sentido si buscas una opción simple para empezar con una estrategia "
                                "de largo plazo.",
                                className="mb-0 text-muted",
                            ),
                        ]
                    ),
                    color="#f5fff8",
                    border="#d6f5df",
                ),

                cta_block(
                    "Empieza a invertir",
                    "Si quieres dar el siguiente paso, puedes abrir cuenta y explorar opciones de inversión "
                    "para construir tu cartera poco a poco.",
                    "Abrir cuenta en MyInvestor",
                    MYINVESTOR_AFFILIATE_URL,
                    "success",
                ),

                build_disclaimer(),

                section_title("Errores comunes al buscar vivir de rentas"),

                bullet_list(
                    [
                        "Pensar que necesitas ser millonario para empezar.",
                        "No invertir y dejar todo el dinero parado.",
                        "Empezar demasiado tarde por creer que ya no merece la pena.",
                        "No revisar tus gastos reales y calcular mal tu objetivo.",
                        "Cambiar de estrategia constantemente y no dar tiempo al plan.",
                    ]
                ),

                section_title("Conclusión"),

                paragraph(
                    "Vivir de rentas en España no depende solo de tener mucho dinero hoy. "
                    "Depende de cuánto gastas, cuánto ahorras, cómo inviertes y cuánto tiempo "
                    "dejas trabajar al interés compuesto."
                ),

                paragraph(
                    "La buena noticia es que puedes calcular tu caso con bastante claridad y empezar "
                    "a dar pasos concretos desde ya. Incluso pequeñas aportaciones mensuales, mantenidas "
                    "durante años, pueden cambiar por completo tu situación financiera futura."
                ),

                callout_box(
                    "Siguiente paso recomendado",
                    html.Div(
                        [
                            html.P(
                                "Calcula primero cuánto necesitas y luego simula cuánto tardarías en llegar.",
                                className="mb-3",
                                style={"fontSize": "1.05rem"},
                            ),
                            dbc.Stack(
                                [
                                    dbc.Button(
                                        "Calcular mi objetivo FIRE",
                                        href="/fire",
                                        color="primary",
                                        class_name="rounded-pill px-4 fw-semibold",
                                    ),
                                    dbc.Button(
                                        "Simular interés compuesto",
                                        href="/calculadora",
                                        color="light",
                                        class_name="rounded-pill px-4 fw-semibold border",
                                    ),
                                ],
                                direction="horizontal",
                                gap=2,
                                class_name="flex-wrap",
                            ),
                        ]
                    ),
                    color="#eef4ff",
                    border="#d7e6ff",
                ),

                section_title("Preguntas frecuentes"),

                html.H3("¿Cuánto dinero necesito para vivir de rentas en España?", className="h5 fw-bold mt-4"),
                paragraph(
                    "Depende de tus gastos anuales. Como referencia rápida, muchas personas usan la regla del 4%, "
                    "que consiste en dividir tus gastos anuales entre 0,04."
                ),

                html.H3("¿Se puede vivir de rentas con fondos indexados?", className="h5 fw-bold mt-4"),
                paragraph(
                    "Sí, es una de las estrategias más populares dentro de la independencia financiera. "
                    "La clave está en la diversificación, el largo plazo y la constancia."
                ),

                html.H3("¿Qué pasa si empiezo tarde?", className="h5 fw-bold mt-4"),
                paragraph(
                    "Seguir puede mereciendo la pena, pero empezar antes suele marcar una diferencia enorme. "
                    "Precisamente por eso es útil hacer simulaciones con distintos escenarios."
                ),

                html.Hr(className="my-5"),

                html.Div(
                    [
                        html.Div(
                            "También te puede interesar",
                            className="fw-bold mb-3",
                            style={"fontSize": "1.1rem"},
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H4(
                                                    "Calculadora FIRE",
                                                    className="h5 fw-bold",
                                                ),
                                                html.P(
                                                    "Descubre cuánto necesitas para alcanzar la independencia financiera.",
                                                    className="text-muted mb-3",
                                                ),
                                                dbc.Button(
                                                    "Abrir",
                                                    href="/fire",
                                                    color="primary",
                                                    class_name="rounded-pill px-3",
                                                ),
                                            ]
                                        ),
                                        class_name="border-0 shadow-sm h-100",
                                        style={"borderRadius": "18px"},
                                    ),
                                    md=6,
                                    class_name="mb-3",
                                ),
                                dbc.Col(
                                    dbc.Card(
                                        dbc.CardBody(
                                            [
                                                html.H4(
                                                    "Interés compuesto",
                                                    className="h5 fw-bold",
                                                ),
                                                html.P(
                                                    "Simula cómo puede crecer tu dinero con aportaciones periódicas.",
                                                    className="text-muted mb-3",
                                                ),
                                                dbc.Button(
                                                    "Abrir",
                                                    href="/calculadora",
                                                    color="secondary",
                                                    class_name="rounded-pill px-3",
                                                ),
                                            ]
                                        ),
                                        class_name="border-0 shadow-sm h-100",
                                        style={"borderRadius": "18px"},
                                    ),
                                    md=6,
                                    class_name="mb-3",
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        ),
    ]
)
