from dash import html, register_page, page_registry
import dash_bootstrap_components as dbc

register_page(
    __name__,
    path="/blog",
    name="Blog",
    title="Blog de finanzas | interescompuesto.app",
    description="Artículos sobre interés compuesto, FIRE, inversión indexada e hipotecas."
)

# =========================================================
# CONFIG
# =========================================================

EXCLUDE_PATHS = {
    "/",
    "/calculadora",
    "/fire",
    "/hipoteca",
    "/rentabilidad-alquiler",
    "/comparador",
    "/blog",
}

# Prioridad de artículos que más convierten
FEATURED_PRIORITY = [
    "/myinvestor-opiniones",
    "/mejor-cuenta-remunerada-espana",
    "/donde-invertir-10000-euros",
    "/invertir-para-ganar-1000-al-mes",
    "/cuanto-genera-100000-euros",
    "/trade-republic-vs-myinvestor",
]

CATEGORY_STYLES = {
    "Interés compuesto": {"bg": "#eef4ff", "color": "#0d6efd"},
    "FIRE": {"bg": "#ecfdf3", "color": "#198754"},
    "Hipoteca": {"bg": "#fff4e5", "color": "#b54708"},
    "Banca": {"bg": "#f5f3ff", "color": "#7c3aed"},
    "Broker": {"bg": "#fff1f3", "color": "#e11d48"},
    "Opiniones": {"bg": "#f3f4f6", "color": "#374151"},
    "Comparativa": {"bg": "#eff6ff", "color": "#1d4ed8"},
    "Inversión": {"bg": "#f8fafc", "color": "#334155"},
}


# =========================================================
# HELPERS DATA
# =========================================================

def clean_title(title: str) -> str:
    if not title:
        return "Artículo"
    return title.replace(" | interescompuesto.app", "").strip()


def infer_category(path: str, title: str) -> str:
    path_lower = (path or "").lower()
    title_lower = (title or "").lower()

    if "hipoteca" in path_lower or "hipoteca" in title_lower:
        return "Hipoteca"
    if "fire" in path_lower or "rentas" in path_lower or "fire" in title_lower:
        return "FIRE"
    if "trade-republic-vs" in path_lower:
        return "Comparativa"
    if "comparativa" in title_lower or "vs" in title_lower:
        return "Comparativa"
    if "broker" in path_lower or "trade" in path_lower:
        return "Broker"
    if "cuenta" in path_lower:
        return "Banca"
    if "myinvestor" in path_lower or "opiniones" in path_lower:
        return "Opiniones"
    if "interes" in path_lower or "interés" in title_lower:
        return "Interés compuesto"
    return "Inversión"


def infer_reading_time(title: str, description: str) -> str:
    words = len(f"{title} {description}".split())
    mins = max(4, round(words / 22))
    return f"{mins} min"


def infer_intent_score(path: str, title: str) -> int:
    text = f"{path} {title}".lower()

    score = 0

    money_terms = [
        "myinvestor",
        "cuenta",
        "broker",
        "opiniones",
        "vs",
        "comparativa",
        "10000",
        "100.000",
        "100000",
        "1000",
        "invertir",
        "genera",
        "rentas",
    ]
    for term in money_terms:
        if term in text:
            score += 2

    if "que es" in text or "qué es" in text:
        score -= 1

    return score


def get_articles():
    articles = []

    for page in page_registry.values():
        path = page.get("path")
        if not path or path in EXCLUDE_PATHS:
            continue

        # Excluye cualquier subruta del blog manual si existiera
        if path.startswith("/blog/"):
            continue

        title = clean_title(page.get("title", "Artículo"))
        description = page.get("description", "").strip()
        category = infer_category(path, title)
        reading_time = infer_reading_time(title, description)
        featured = path in FEATURED_PRIORITY
        intent_score = infer_intent_score(path, title)

        articles.append(
            {
                "title": title,
                "description": description,
                "url": path,
                "category": category,
                "reading_time": reading_time,
                "featured": featured,
                "intent_score": intent_score,
            }
        )

    featured_articles = [a for a in articles if a["featured"]]
    other_articles = [a for a in articles if not a["featured"]]

    featured_articles.sort(
        key=lambda a: FEATURED_PRIORITY.index(a["url"]) if a["url"] in FEATURED_PRIORITY else 999
    )

    # Primero artículos con más intención de conversión
    other_articles.sort(key=lambda a: (a["intent_score"], a["title"]), reverse=True)

    return featured_articles, other_articles


# =========================================================
# HELPERS UI
# =========================================================

def section_eyebrow(text):
    return html.Div(
        text,
        className="fw-bold mb-2",
        style={
            "fontSize": "0.82rem",
            "letterSpacing": "0.08em",
            "textTransform": "uppercase",
            "color": "#0d6efd",
        },
    )


def badge_category(category):
    style = CATEGORY_STYLES.get(category, CATEGORY_STYLES["Inversión"])
    return html.Span(
        category,
        className="fw-semibold",
        style={
            "display": "inline-block",
            "padding": "0.42rem 0.8rem",
            "borderRadius": "999px",
            "background": style["bg"],
            "color": style["color"],
            "fontSize": "0.8rem",
            "lineHeight": "1",
        },
    )


def metric_chip(text):
    return html.Span(
        text,
        className="text-muted",
        style={
            "fontSize": "0.85rem",
        },
    )


def hero_block():
    return dbc.Row(
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        section_eyebrow("Blog"),
                        html.H1(
                            "Guías prácticas para invertir mejor y tomar decisiones con números reales",
                            className="fw-bold mb-3",
                            style={
                                "fontSize": "clamp(2.15rem, 5vw, 4rem)",
                                "lineHeight": "1.04",
                                "letterSpacing": "-0.04em",
                                "maxWidth": "980px",
                                "color": "#101828",
                            },
                        ),
                        html.P(
                            "Aprende sobre interés compuesto, libertad financiera, hipotecas, brokers y cuentas remuneradas. "
                            "Y cuando quieras pasar de la teoría a la acción, usa nuestras calculadoras gratuitas.",
                            className="mb-4",
                            style={
                                "fontSize": "1.08rem",
                                "lineHeight": "1.85",
                                "maxWidth": "880px",
                                "color": "#475467",
                            },
                        ),
                        dbc.Stack(
                            [
                                dbc.Button(
                                    "Probar calculadora",
                                    href="/calculadora",
                                    color="primary",
                                    class_name="rounded-pill px-4 fw-semibold",
                                ),
                                dbc.Button(
                                    "Calcular mi FIRE",
                                    href="/fire",
                                    color="light",
                                    class_name="rounded-pill px-4 fw-semibold border",
                                ),
                                dbc.Button(
                                    "Calcular hipoteca",
                                    href="/hipoteca",
                                    color="light",
                                    class_name="rounded-pill px-4 fw-semibold border",
                                ),
                            ],
                            direction="horizontal",
                            gap=2,
                            class_name="flex-wrap",
                        ),
                        html.Hr(className="my-4"),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Div("Guías prácticas", className="fw-bold mb-1"),
                                        html.Div(
                                            "Artículos claros para pasar de duda a decisión.",
                                            className="text-muted small",
                                        ),
                                    ],
                                    md=4,
                                    class_name="mb-3 mb-md-0",
                                ),
                                dbc.Col(
                                    [
                                        html.Div("Simuladores gratuitos", className="fw-bold mb-1"),
                                        html.Div(
                                            "Calcula escenarios reales en menos de un minuto.",
                                            className="text-muted small",
                                        ),
                                    ],
                                    md=4,
                                    class_name="mb-3 mb-md-0",
                                ),
                                dbc.Col(
                                    [
                                        html.Div("Enfoque práctico", className="fw-bold mb-1"),
                                        html.Div(
                                            "Menos teoría vacía, más números útiles.",
                                            className="text-muted small",
                                        ),
                                    ],
                                    md=4,
                                ),
                            ]
                        ),
                    ]
                ),
                class_name="border-0 shadow-sm rounded-4",
                style={
                    "background": (
                        "radial-gradient(circle at top left, rgba(13,110,253,0.08), transparent 32%), "
                        "radial-gradient(circle at top right, rgba(25,135,84,0.06), transparent 28%), "
                        "linear-gradient(180deg, #ffffff 0%, #f8fafc 100%)"
                    )
                },
            ),
            lg=12,
        ),
        className="pt-4 pt-md-5 mb-4",
    )


def start_here_block():
    return dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H3(
                                    "Empieza por aquí",
                                    className="fw-bold mb-2",
                                    style={"fontSize": "1.45rem"},
                                ),
                                html.P(
                                    "Si no sabes qué leer primero, estas herramientas y guías suelen ser el mejor punto de partida.",
                                    className="text-muted mb-0",
                                    style={"lineHeight": "1.75"},
                                ),
                            ],
                            lg=7,
                            class_name="mb-3 mb-lg-0",
                        ),
                        dbc.Col(
                            dbc.Stack(
                                [
                                    dbc.Button(
                                        "Interés compuesto",
                                        href="/calculadora",
                                        color="primary",
                                        class_name="rounded-pill px-4 fw-semibold",
                                    ),
                                    dbc.Button(
                                        "FIRE",
                                        href="/fire",
                                        color="success",
                                        class_name="rounded-pill px-4 fw-semibold",
                                    ),
                                    dbc.Button(
                                        "Hipoteca",
                                        href="/hipoteca",
                                        color="light",
                                        class_name="rounded-pill px-4 fw-semibold border",
                                    ),
                                ],
                                direction="horizontal",
                                gap=2,
                                class_name="flex-wrap justify-content-lg-end",
                            ),
                            lg=5,
                            class_name="d-flex align-items-center",
                        ),
                    ]
                )
            ]
        ),
        class_name="border-0 shadow-sm rounded-4 mb-5",
        style={"background": "linear-gradient(180deg, #ffffff 0%, #f8fafc 100%)"},
    )


def featured_card(article):
    style = CATEGORY_STYLES.get(article["category"], CATEGORY_STYLES["Inversión"])

    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        [
                            badge_category(article["category"]),
                            metric_chip(article["reading_time"]),
                        ],
                        className="d-flex align-items-center gap-2 mb-3 flex-wrap",
                    ),
                    html.H2(
                        html.A(
                            article["title"],
                            href=article["url"],
                            className="text-decoration-none stretched-link",
                            style={"color": "#101828"},
                        ),
                        className="mb-3",
                        style={
                            "fontSize": "1.45rem",
                            "lineHeight": "1.2",
                            "letterSpacing": "-0.02em",
                        },
                    ),
                    html.P(
                        article["description"],
                        className="mb-3",
                        style={
                            "color": "#667085",
                            "lineHeight": "1.8",
                            "fontSize": "1rem",
                        },
                    ),
                    html.Div(
                        "Leer artículo →",
                        className="fw-semibold",
                        style={"color": style["color"]},
                    ),
                ]
            ),
            class_name="border-0 shadow-sm rounded-4 h-100 position-relative",
            style={
                "background": "linear-gradient(180deg, #ffffff 0%, #f8fafc 100%)",
                "minHeight": "100%",
            },
        ),
        lg=6,
        class_name="mb-4",
    )


def article_card(article):
    style = CATEGORY_STYLES.get(article["category"], CATEGORY_STYLES["Inversión"])

    return dbc.Col(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        [
                            badge_category(article["category"]),
                            metric_chip(article["reading_time"]),
                        ],
                        className="d-flex align-items-center gap-2 mb-3 flex-wrap",
                    ),
                    html.H3(
                        html.A(
                            article["title"],
                            href=article["url"],
                            className="text-decoration-none stretched-link",
                            style={"color": "#101828"},
                        ),
                        className="h4 mb-3",
                        style={
                            "lineHeight": "1.25",
                            "letterSpacing": "-0.01em",
                        },
                    ),
                    html.P(
                        article["description"],
                        className="mb-3",
                        style={
                            "color": "#667085",
                            "lineHeight": "1.75",
                            "fontSize": "0.98rem",
                        },
                    ),
                    html.Div(
                        "Leer guía →",
                        className="fw-semibold",
                        style={"color": style["color"]},
                    ),
                ]
            ),
            class_name="border-0 shadow-sm rounded-4 h-100 position-relative",
            style={
                "background": "linear-gradient(180deg, #ffffff 0%, #fbfcfe 100%)",
            },
        ),
        md=6,
        lg=4,
        class_name="mb-4",
    )


def conversion_block():
    return dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H3(
                                    "No te quedes solo en la teoría",
                                    className="fw-bold mb-2",
                                    style={"fontSize": "1.55rem"},
                                ),
                                html.P(
                                    "Haz una simulación en menos de un minuto y toma decisiones con una referencia mucho más clara.",
                                    className="text-muted mb-0",
                                    style={"lineHeight": "1.8", "fontSize": "1.02rem"},
                                ),
                            ],
                            lg=7,
                            class_name="mb-3 mb-lg-0",
                        ),
                        dbc.Col(
                            dbc.Stack(
                                [
                                    dbc.Button(
                                        "Simular interés compuesto",
                                        href="/calculadora",
                                        color="primary",
                                        class_name="rounded-pill px-4 fw-semibold",
                                    ),
                                    dbc.Button(
                                        "Abrir calculadora FIRE",
                                        href="/fire",
                                        color="success",
                                        class_name="rounded-pill px-4 fw-semibold",
                                    ),
                                ],
                                direction="horizontal",
                                gap=2,
                                class_name="flex-wrap justify-content-lg-end",
                            ),
                            lg=5,
                            class_name="d-flex align-items-center",
                        ),
                    ]
                )
            ]
        ),
        class_name="border-0 shadow-sm rounded-4 mt-2 mb-5",
        style={
            "background": (
                "radial-gradient(circle at bottom right, rgba(13,110,253,0.06), transparent 30%), "
                "linear-gradient(180deg, #ffffff 0%, #f8fafc 100%)"
            )
        },
    )


def newsletter_style_strip():
    return dbc.Row(
        dbc.Col(
            html.Div(
                [
                    html.Div(
                        "Ideas clave",
                        className="fw-bold mb-2",
                        style={"fontSize": "1.2rem"},
                    ),
                    html.P(
                        "Los artículos con más intención de acción suelen ser comparativas, opiniones, cuánto necesito invertir y dónde invertir una cantidad concreta.",
                        className="text-muted mb-0",
                        style={"lineHeight": "1.8"},
                    ),
                ],
                className="mb-4",
            )
        )
    )


# =========================================================
# LAYOUT
# =========================================================

def layout():
    featured_articles, other_articles = get_articles()

    return dbc.Container(
        [
            hero_block(),
            start_here_block(),

            html.Div(
                "Artículos destacados",
                className="fw-bold mb-3",
                style={
                    "fontSize": "1.45rem",
                    "letterSpacing": "-0.02em",
                    "color": "#101828",
                },
            ),
            html.P(
                "Las guías con mayor intención de búsqueda y más útiles para empezar.",
                className="text-muted mb-4",
                style={"lineHeight": "1.7"},
            ),
            dbc.Row([featured_card(article) for article in featured_articles], className="mb-2"),

            newsletter_style_strip(),

            html.Div(
                "Todas las guías",
                className="fw-bold mb-3",
                style={
                    "fontSize": "1.45rem",
                    "letterSpacing": "-0.02em",
                    "color": "#101828",
                },
            ),
            html.P(
                "Explora artículos sobre inversión, FIRE, brokers, cuentas remuneradas e hipotecas.",
                className="text-muted mb-4",
                style={"lineHeight": "1.7"},
            ),
            dbc.Row([article_card(article) for article in other_articles], className="pb-2"),

            conversion_block(),
        ],
        fluid=True,
        className="py-2 px-3 px-md-4 px-lg-5",
        style={"maxWidth": "1600px"},
    )
