import dash
from dash import html, dcc, Input, Output, callback, clientside_callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from helpers import parse_number, calcular_interes_compuesto, formatear_euros_es
from components.disclaimer_afiliados import build_disclaimer

MYINVESTOR_AFFILIATE_URL = "https://newapp.myinvestor.es/do/signup?promotionalCode=GZKWQ"

dash.register_page(
    __name__,
    path="/calculadora",
    title="Calculadora de interés compuesto",
    name="Calculadora",
)

# =========================================================
# HELPERS UI
# =========================================================
def metric_card(title, value, subtitle=None, highlight=False):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, className="metric-label"),
                html.Div(
                    value,
                    className=f"metric-value {'metric-value-highlight' if highlight else ''}",
                ),
                html.Div(subtitle, className="metric-subtitle") if subtitle else None,
            ]
        ),
        className="shadow-sm border-0 rounded-4 h-100 metric-card",
    )


def input_group(label, input_id, value, input_type="text", hint=None):
    return html.Div(
        [
            dbc.Label(label, className="fw-semibold mb-2"),
            dbc.Input(
                id=input_id,
                value=value,
                type=input_type,
                className="custom-input mb-1",
            ),
            html.Div(hint, className="input-hint mb-3") if hint else None,
        ]
    )


def scenario_card(title, amount, extra=None, highlight=False):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, className="scenario-label"),
                html.Div(
                    amount,
                    className=f"scenario-value {'text-success' if highlight else ''}",
                ),
                html.Div(extra, className="scenario-extra") if extra else None,
            ]
        ),
        className="border-0 shadow-sm rounded-4 h-100 scenario-card",
    )


# =========================================================
# ESTILOS
# =========================================================
custom_styles = html.Style("""
:root {
    --ic-primary: #2563eb;
    --ic-primary-soft: rgba(37, 99, 235, 0.10);
    --ic-success: #16a34a;
    --ic-success-soft: rgba(22, 163, 74, 0.10);
    --ic-text: #101828;
    --ic-text-soft: #667085;
    --ic-border: rgba(16, 24, 40, 0.06);
    --ic-bg-soft: #f8fbff;
}

.calculator-hero {
    background:
        radial-gradient(circle at top left, rgba(37,99,235,0.14), transparent 28%),
        linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
    border: 1px solid rgba(37,99,235,0.08);
}

.hero-badge {
    display: inline-block;
    padding: 0.45rem 0.8rem;
    border-radius: 999px;
    background: rgba(37,99,235,0.10);
    color: #1d4ed8;
    font-weight: 700;
    font-size: 0.82rem;
    margin-bottom: 1rem;
}

.hero-title {
    color: var(--ic-text);
    letter-spacing: -0.03em;
    line-height: 1.05;
}

.hero-subtitle {
    color: var(--ic-text-soft);
    font-size: 1.05rem;
    max-width: 760px;
}

.form-card,
.chart-card,
.message-card,
.interpretation-card,
.cta-card {
    background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
}

.form-card {
    position: sticky;
    top: 90px;
}

.section-title-small {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #1d4ed8;
    font-weight: 800;
    margin-bottom: 0.5rem;
}

.custom-input {
    border-radius: 0.9rem;
    border: 1px solid rgba(16,24,40,0.10);
    padding-top: 0.8rem;
    padding-bottom: 0.8rem;
}

.custom-input:focus {
    border-color: rgba(37,99,235,0.45);
    box-shadow: 0 0 0 0.2rem rgba(37,99,235,0.10);
}

.input-hint {
    color: var(--ic-text-soft);
    font-size: 0.82rem;
}

.metric-card {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.metric-card:hover,
.scenario-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 16px 34px rgba(16,24,40,0.08) !important;
}

.metric-label {
    color: var(--ic-text-soft);
    font-size: 0.85rem;
    margin-bottom: 0.4rem;
}

.metric-value {
    color: var(--ic-text);
    font-weight: 800;
    font-size: 1.7rem;
    letter-spacing: -0.02em;
    line-height: 1.1;
}

.metric-value-highlight {
    color: var(--ic-success);
}

.metric-subtitle {
    color: var(--ic-text-soft);
    font-size: 0.82rem;
    margin-top: 0.5rem;
}

.result-banner {
    background:
        linear-gradient(135deg, rgba(22,163,74,0.10) 0%, rgba(37,99,235,0.08) 100%),
        #ffffff;
    border: 1px solid rgba(16,24,40,0.06);
}

.result-banner-title {
    color: var(--ic-success);
    letter-spacing: -0.02em;
}

.result-banner-text {
    color: var(--ic-text-soft);
    margin-bottom: 0;
}

.interpretation-card {
    border: 1px solid rgba(37,99,235,0.08);
}

.interpretation-list {
    padding-left: 1.1rem;
    color: #475467;
    margin-bottom: 0;
}

.interpretation-list li {
    margin-bottom: 0.6rem;
}

.scenario-card {
    background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.scenario-label {
    color: var(--ic-text-soft);
    font-size: 0.84rem;
    margin-bottom: 0.4rem;
}

.scenario-value {
    color: var(--ic-text);
    font-weight: 800;
    font-size: 1.35rem;
    line-height: 1.1;
}

.scenario-extra {
    color: var(--ic-text-soft);
    font-size: 0.82rem;
    margin-top: 0.5rem;
}

.cta-card {
    background:
        linear-gradient(135deg, rgba(22,163,74,0.12) 0%, rgba(37,99,235,0.08) 100%),
        #ffffff;
    border: 1px solid rgba(16,24,40,0.06);
}

.cta-title {
    color: var(--ic-text);
    letter-spacing: -0.02em;
}

.cta-subtext {
    color: var(--ic-text-soft);
}

.anchor-spacer {
    scroll-margin-top: 100px;
}

@media (max-width: 991.98px) {
    .form-card {
        position: static;
    }
}

@media (max-width: 768px) {
    .hero-title {
        font-size: 2rem !important;
        line-height: 1.08;
    }

    .hero-subtitle {
        font-size: 1rem;
    }

    .metric-value {
        font-size: 1.5rem;
    }
}
""")

# =========================================================
# LAYOUT
# =========================================================
layout = dbc.Container(
    [
        custom_styles,

        # HERO
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div("Calculadora principal", className="hero-badge"),
                                html.H1(
                                    "Calcula cuánto dinero podrías tener en el futuro",
                                    className="fw-bold hero-title mb-3",
                                ),
                                html.P(
                                    "Introduce tus datos y simula cómo pueden crecer tus ahorros con aportaciones periódicas, rentabilidad, inflación y comisiones.",
                                    className="hero-subtitle mb-0",
                                ),
                            ]
                        ),
                        className="calculator-hero border-0 rounded-4 shadow-sm mt-4 mb-4",
                    ),
                    width=12,
                )
            ]
        ),

        dbc.Row(
            [
                # INPUTS
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div("Tu simulación", className="section-title-small"),
                                html.H4("Datos de inversión", className="fw-bold mb-3"),

                                input_group(
                                    "Capital inicial (€)",
                                    "ic-capital-inicial",
                                    "10000",
                                    "text",
                                    "Ejemplo: 10.000"
                                ),
                                input_group(
                                    "Aportación mensual (€)",
                                    "ic-aportacion",
                                    "300",
                                    "text",
                                    "Ejemplo: 300 al mes"
                                ),
                                input_group(
                                    "Años",
                                    "ic-anios",
                                    "20",
                                    "number",
                                    "Horizonte temporal de la inversión"
                                ),
                                input_group(
                                    "Rentabilidad anual (%)",
                                    "ic-rentabilidad",
                                    "7",
                                    "text",
                                    "Rentabilidad media esperada"
                                ),
                                input_group(
                                    "Inflación anual (%)",
                                    "ic-inflacion",
                                    "2",
                                    "text",
                                    "Para estimar el poder adquisitivo real"
                                ),
                                input_group(
                                    "Comisión anual (%)",
                                    "ic-comision",
                                    "0.2",
                                    "text",
                                    "Coste anual aproximado del producto"
                                ),

                                dbc.Button(
                                    "💰 Calcular mi dinero futuro",
                                    id="ic-boton",
                                    color="primary",
                                    size="lg",
                                    className="w-100 mt-2 rounded-pill fw-semibold",
                                ),

                                html.Div(
                                    "La simulación es orientativa y no garantiza resultados futuros.",
                                    className="input-hint mt-3"
                                ),
                            ]
                        ),
                        className="form-card shadow border-0 rounded-4",
                    ),
                    lg=4,
                    className="mb-4",
                ),

                # RESULTADOS
                dbc.Col(
                    [
                        html.Div(id="scroll-target", className="anchor-spacer"),

                        dbc.Row(
                            [
                                dbc.Col(html.Div(id="ic-resultado-final"), md=4, className="mb-3"),
                                dbc.Col(html.Div(id="ic-total-aportado"), md=4, className="mb-3"),
                                dbc.Col(html.Div(id="ic-ganancia"), md=4, className="mb-3"),
                            ]
                        ),

                        html.Div(id="ic-mensaje-emocional", className="mb-4"),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Div("Qué significa tu simulación", className="section-title-small"),
                                    html.H4("Interpretación del resultado", className="fw-bold mb-3"),
                                    html.Div(id="ic-interpretacion"),
                                ]
                            ),
                            className="interpretation-card shadow-sm border-0 rounded-4 mb-4",
                        ),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Div("Evolución de tu inversión", className="section-title-small"),
                                    dcc.Graph(id="ic-grafico", config={"displayModeBar": False}),
                                ]
                            ),
                            className="chart-card shadow-sm border-0 rounded-4 mb-4",
                        ),

                        html.Div(id="ic-comparativa", className="mb-4"),

                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.Div("Pasa de simular a actuar", className="section-title-small"),
                                    html.H4("Si esta estrategia te encaja, el siguiente paso es empezar", className="fw-bold cta-title mb-3"),
                                    html.P(
                                        "No necesitas hacerlo perfecto desde el primer día. Lo importante es empezar con criterio, poco a poco y con constancia.",
                                        className="cta-subtext mb-3"
                                    ),
                                    html.P(
                                        "👉 Si inviertes de forma parecida a esta simulación, podrías acercarte a este resultado con el tiempo.",
                                        className="small text-muted mb-4"
                                    ),
                                    dbc.Button(
                                        "Abrir cuenta y empezar a invertir",
                                        href=MYINVESTOR_AFFILIATE_URL,
                                        target="_blank",
                                        color="success",
                                        size="lg",
                                        className="w-100 rounded-pill fw-semibold"
                                    ),
                                ]
                            ),
                            className="cta-card shadow border-0 rounded-4 mb-4",
                        ),

                        build_disclaimer(title="Más opciones para dar el siguiente paso"),
                    ],
                    lg=8,
                ),
            ],
            className="gy-4",
        ),
    ],
    fluid=True,
    className="px-4 px-md-5 pb-5",
)

# =========================================================
# SCROLL AUTOMÁTICO
# =========================================================
clientside_callback(
    """
    function(n_clicks) {
        if (n_clicks) {
            setTimeout(() => {
                const el = document.getElementById("scroll-target");
                if (el) {
                    el.scrollIntoView({behavior: "smooth", block: "start"});
                }
            }, 120);
        }
        return "";
    }
    """,
    Output("scroll-target", "children"),
    Input("ic-boton", "n_clicks"),
)

# =========================================================
# CALLBACK PRINCIPAL
# =========================================================
@callback(
    Output("ic-resultado-final", "children"),
    Output("ic-total-aportado", "children"),
    Output("ic-ganancia", "children"),
    Output("ic-grafico", "figure"),
    Output("ic-mensaje-emocional", "children"),
    Output("ic-comparativa", "children"),
    Output("ic-interpretacion", "children"),
    Input("ic-boton", "n_clicks"),
    Input("ic-capital-inicial", "value"),
    Input("ic-aportacion", "value"),
    Input("ic-anios", "value"),
    Input("ic-rentabilidad", "value"),
    Input("ic-inflacion", "value"),
    Input("ic-comision", "value"),
)
def actualizar_calculadora(_, capital_inicial, aportacion, anios, rentabilidad, inflacion, comision):
    capital_inicial = parse_number(capital_inicial)
    aportacion = parse_number(aportacion)
    anios = int(anios or 0)
    rentabilidad = parse_number(rentabilidad) / 100
    inflacion = parse_number(inflacion) / 100
    comision = parse_number(comision) / 100

    evolucion = calcular_interes_compuesto(
        capital_inicial=capital_inicial,
        aportacion_mensual=aportacion,
        años=anios,
        rentabilidad_anual=rentabilidad,
        inflacion=inflacion,
        comision=comision,
    )

    fig = go.Figure()

    if not evolucion:
        fig.update_layout(template="plotly_white")
        return (
            metric_card("Valor final", "0 €"),
            metric_card("Aportado", "0 €"),
            metric_card("Ganancia", "0 €"),
            fig,
            "",
            "",
            "",
        )

    anos = [x["año"] for x in evolucion]
    total = [x["total"] for x in evolucion]
    aportado_hist = [x["aportado"] for x in evolucion]
    real = [x["real"] for x in evolucion]

    valor_final = total[-1]
    total_aportado = aportado_hist[-1]
    ganancia = valor_final - total_aportado

    # ESCENARIOS
    evolucion_100 = calcular_interes_compuesto(
        capital_inicial=capital_inicial,
        aportacion_mensual=aportacion + 100,
        años=anios,
        rentabilidad_anual=rentabilidad,
        inflacion=inflacion,
        comision=comision,
    )

    evolucion_500 = calcular_interes_compuesto(
        capital_inicial=capital_inicial,
        aportacion_mensual=aportacion + 200,
        años=anios,
        rentabilidad_anual=rentabilidad,
        inflacion=inflacion,
        comision=comision,
    )

    valor_100 = evolucion_100[-1]["total"] if evolucion_100 else 0
    valor_200 = evolucion_500[-1]["total"] if evolucion_500 else 0

    diferencia_100 = valor_100 - valor_final
    diferencia_200 = valor_200 - valor_final

    # GRAFICO
    fig.add_trace(go.Scatter(
        x=anos,
        y=aportado_hist,
        mode="lines",
        name="Capital aportado",
        line=dict(width=3),
    ))
    fig.add_trace(go.Scatter(
        x=anos,
        y=total,
        mode="lines",
        name="Valor total",
        line=dict(width=4),
    ))
    fig.add_trace(go.Scatter(
        x=anos,
        y=real,
        mode="lines",
        name="Valor real",
        line=dict(width=3, dash="dot"),
    ))

    fig.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis_title="Años",
        yaxis_title="€",
        legend_title="",
        hovermode="x unified",
    )

    mensaje = dbc.Card(
        dbc.CardBody(
            [
                html.H3(
                    f"Podrías tener {formatear_euros_es(valor_final)}",
                    className="fw-bold result-banner-title mb-2"
                ),
                html.P(
                    f"Habrías aportado {formatear_euros_es(total_aportado)} y generado {formatear_euros_es(ganancia)} de crecimiento potencial.",
                    className="result-banner-text"
                ),
            ]
        ),
        className="result-banner border-0 rounded-4 shadow-sm",
    )

    comparativa = html.Div(
        [
            html.Div("Comparativa rápida", className="section-title-small"),
            dbc.Row(
                [
                    dbc.Col(
                        scenario_card(
                            "Tu escenario actual",
                            formatear_euros_es(valor_final),
                            f"{formatear_euros_es(aportacion)} al mes"
                        ),
                        md=4,
                        className="mb-3"
                    ),
                    dbc.Col(
                        scenario_card(
                            "+100€/mes",
                            formatear_euros_es(valor_100),
                            f"{formatear_euros_es(diferencia_100)} más que tu escenario actual",
                            True
                        ),
                        md=4,
                        className="mb-3"
                    ),
                    dbc.Col(
                        scenario_card(
                            "+200€/mes",
                            formatear_euros_es(valor_200),
                            f"{formatear_euros_es(diferencia_200)} más que tu escenario actual",
                            True
                        ),
                        md=4,
                        className="mb-3"
                    ),
                ]
            )
        ]
    )

    interpretacion = html.Ul(
        [
            html.Li(
                f"De los {formatear_euros_es(valor_final)} finales, una parte importante vendría del crecimiento acumulado, no solo de tus aportaciones."
            ),
            html.Li(
                "El tiempo es una de las variables más potentes: cuanto antes empieces, más trabaja el interés compuesto a tu favor."
            ),
            html.Li(
                "Pequeños cambios mensuales pueden tener un impacto grande a largo plazo, como ves en la comparativa de escenarios."
            ),
            html.Li(
                "La inflación y las comisiones importan: por eso conviene revisar costes y mantener expectativas razonables."
            ),
        ],
        className="interpretation-list"
    )

    return (
        metric_card("Valor final", formatear_euros_es(valor_final), "Estimación nominal final", True),
        metric_card("Total aportado", formatear_euros_es(total_aportado), "Lo que habrías puesto tú"),
        metric_card("Ganancia potencial", formatear_euros_es(ganancia), "Diferencia entre aportado y valor final", True),
        fig,
        mensaje,
        comparativa,
        interpretacion,
    )
