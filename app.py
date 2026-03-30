import io
from datetime import datetime

import pandas as pd
from dash import Dash, dcc, html, Input, Output, State, dash_table, callback_context
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# =========================================================
# APP
# =========================================================
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX], suppress_callback_exceptions=True)
server = app.server
app.title = "Calculadora de interés compuesto"

# =========================================================
# ESTILO
# =========================================================
BRAND_NAME = "Calculadora de interés compuesto"

COLOR_BG = "#f5f7fb"
COLOR_CARD = "#ffffff"
COLOR_TEXT = "#0f172a"
COLOR_MUTED = "#64748b"
COLOR_BORDER = "#e2e8f0"

COLOR_PRIMARY = "#2563eb"
COLOR_PRIMARY_SOFT = "#eff6ff"
COLOR_SUCCESS = "#16a34a"
COLOR_SUCCESS_SOFT = "#f0fdf4"
COLOR_WARNING = "#d97706"
COLOR_WARNING_SOFT = "#fff7ed"
COLOR_DANGER = "#dc2626"
COLOR_DANGER_SOFT = "#fef2f2"
COLOR_DARK = "#0f172a"
COLOR_CAPITAL = "#94a3b8"
COLOR_REAL = "#0f766e"

CARD_STYLE = {
    "borderRadius": "20px",
    "boxShadow": "0 12px 30px rgba(15, 23, 42, 0.06)",
    "border": f"1px solid {COLOR_BORDER}",
    "backgroundColor": COLOR_CARD
}

SECTION_TITLE_STYLE = {
    "fontWeight": "800",
    "fontSize": "1.15rem",
    "marginBottom": "14px",
    "color": COLOR_TEXT
}

LABEL_STYLE = {
    "fontWeight": "700",
    "marginBottom": "6px",
    "display": "block",
    "color": COLOR_TEXT
}

# =========================================================
# UTILIDADES
# =========================================================
def safe_float(value, default=0.0):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except Exception:
        return default

def safe_int(value, default=0):
    try:
        if value is None or value == "":
            return default
        return int(value)
    except Exception:
        return default

def formatear_euros_es(valor):
    s = f"{float(valor):,.2f}"
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{s} €"

def formatear_pct_es(valor):
    return f"{float(valor):,.2f}".replace(".", ",") + " %"

def obtener_periodos_por_ano(frecuencia):
    return 12 if frecuencia == "mensual" else 1

def obtener_nombre_periodo(frecuencia):
    return "Mes" if frecuencia == "mensual" else "Año"

def annual_to_period_rate(annual_rate_decimal, frecuencia):
    if frecuencia == "mensual":
        return (1 + annual_rate_decimal) ** (1 / 12) - 1
    return annual_rate_decimal

def net_annual_growth_rate(tasa_bruta_anual_pct, comision_anual_pct):
    tasa = safe_float(tasa_bruta_anual_pct) / 100
    comision = safe_float(comision_anual_pct) / 100
    return (1 + tasa) * (1 - comision) - 1

def generar_aporte_periodico(periodo_index, deposito_inicial, crecimiento_aportacion_anual_pct, frecuencia):
    crecimiento_anual = safe_float(crecimiento_aportacion_anual_pct) / 100
    if frecuencia == "anual":
        ano = periodo_index - 1
    else:
        ano = (periodo_index - 1) // 12
    return float(deposito_inicial) * ((1 + crecimiento_anual) ** ano)

def calcular_cagr(valor_inicial, valor_final, anos):
    if valor_inicial <= 0 or valor_final <= 0 or anos <= 0:
        return 0.0
    return (valor_final / valor_inicial) ** (1 / anos) - 1

def validar_inputs(monto_inicial, deposito, tasa, anos, inflacion, impuestos, comision, crecimiento_aporte):
    errores = []
    if monto_inicial is None or safe_float(monto_inicial) < 0:
        errores.append("La inversión inicial debe ser 0 o mayor.")
    if deposito is None or safe_float(deposito) < 0:
        errores.append("La aportación periódica debe ser 0 o mayor.")
    if tasa is None or safe_float(tasa) < 0:
        errores.append("La rentabilidad anual debe ser 0 o mayor.")
    if anos is None or safe_int(anos) < 1:
        errores.append("La duración debe ser al menos de 1 año.")
    if inflacion is None or safe_float(inflacion) < 0:
        errores.append("La inflación debe ser 0 o mayor.")
    if impuestos is None or safe_float(impuestos) < 0:
        errores.append("Los impuestos deben ser 0 o mayores.")
    if comision is None or safe_float(comision) < 0:
        errores.append("La comisión debe ser 0 o mayor.")
    if crecimiento_aporte is None:
        errores.append("El crecimiento anual de aportación no puede estar vacío.")
    return errores

# =========================================================
# CÁLCULO
# =========================================================
def calcular_escenario(
    nombre_escenario,
    monto_inicial,
    deposito_periodico,
    tasa_interes_anual_pct,
    num_anos,
    frecuencia,
    momento_aportacion,
    inflacion_anual_pct,
    impuesto_plusvalias_pct,
    comision_anual_pct,
    crecimiento_aportacion_anual_pct
):
    monto_inicial = safe_float(monto_inicial)
    deposito_periodico = safe_float(deposito_periodico)
    tasa_interes_neta_anual = net_annual_growth_rate(tasa_interes_anual_pct, comision_anual_pct)
    inflacion_anual = safe_float(inflacion_anual_pct) / 100
    impuesto_plusvalias = safe_float(impuesto_plusvalias_pct) / 100
    num_anos = safe_int(num_anos)

    periodos_por_ano = obtener_periodos_por_ano(frecuencia)
    nombre_periodo = obtener_nombre_periodo(frecuencia)
    tasa_por_periodo = annual_to_period_rate(tasa_interes_neta_anual, frecuencia)
    inflacion_por_periodo = annual_to_period_rate(inflacion_anual, frecuencia)
    total_periodos = num_anos * periodos_por_ano

    saldo_bruto = monto_inicial
    depositos_acumulados = 0.0
    rows = []

    for t in range(1, total_periodos + 1):
        aporte_periodo = generar_aporte_periodico(t, deposito_periodico, crecimiento_aportacion_anual_pct, frecuencia)

        if momento_aportacion == "inicio":
            saldo_bruto += aporte_periodo
            depositos_acumulados += aporte_periodo
            saldo_bruto *= (1 + tasa_por_periodo)
        else:
            saldo_bruto *= (1 + tasa_por_periodo)
            saldo_bruto += aporte_periodo
            depositos_acumulados += aporte_periodo

        capital_aportado = monto_inicial + depositos_acumulados
        interes_bruto = saldo_bruto - capital_aportado
        impuestos_teoricos = max(interes_bruto, 0) * impuesto_plusvalias
        interes_neto = interes_bruto - impuestos_teoricos
        valor_total_neto = capital_aportado + interes_neto

        factor_inflacion = (1 + inflacion_por_periodo) ** t
        valor_real_neto = valor_total_neto / factor_inflacion if factor_inflacion > 0 else valor_total_neto

        rows.append({
            "Escenario": nombre_escenario,
            nombre_periodo: t,
            "Etiqueta": f"{nombre_periodo} {t}",
            "Aporte del período": aporte_periodo,
            "Capital aportado": capital_aportado,
            "Interés bruto": interes_bruto,
            "Impuestos teóricos": impuestos_teoricos,
            "Interés neto": interes_neto,
            "Valor total bruto": saldo_bruto,
            "Valor total neto": valor_total_neto,
            "Valor real neto": valor_real_neto
        })

    return pd.DataFrame(rows), nombre_periodo

def preparar_df_plot(df, frecuencia):
    if frecuencia == "mensual" and len(df) > 24:
        df_plot = df[df["Mes"] % 12 == 0].copy()
        df_plot["Etiqueta"] = df_plot["Mes"].apply(lambda x: f"Año {x // 12}")
        return df_plot, "Año"
    return df.copy(), obtener_nombre_periodo(frecuencia)

# =========================================================
# FIGURAS
# =========================================================
def base_layout(fig, titulo, yaxis_title, xaxis_title=None):
    fig.update_layout(
        title={"text": titulo, "x": 0.5},
        template="plotly_white",
        hovermode="x unified",
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
        margin=dict(l=40, r=20, t=90, b=60),
        yaxis_title=yaxis_title,
        xaxis_title=xaxis_title,
        paper_bgcolor="white",
        plot_bgcolor="white"
    )
    return fig

def crear_figura_principal(df_plot):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_plot["Etiqueta"],
        y=df_plot["Capital aportado"],
        mode="lines",
        name="Capital aportado",
        line=dict(width=3, color=COLOR_CAPITAL)
    ))

    fig.add_trace(go.Scatter(
        x=df_plot["Etiqueta"],
        y=df_plot["Valor total neto"],
        mode="lines+markers",
        name="Valor total estimado",
        line=dict(width=4, color=COLOR_PRIMARY),
        marker=dict(size=7)
    ))

    fig.add_trace(go.Scatter(
        x=df_plot["Etiqueta"],
        y=df_plot["Valor real neto"],
        mode="lines",
        name="Valor real estimado",
        line=dict(width=3, dash="dash", color=COLOR_REAL)
    ))

    valor_final = df_plot["Valor total neto"].iloc[-1]
    capital_final = df_plot["Capital aportado"].iloc[-1]
    crecimiento = valor_final - capital_final

    fig.add_annotation(
        x=df_plot["Etiqueta"].iloc[-1],
        y=valor_final,
        text=f"+{formatear_euros_es(crecimiento)}",
        showarrow=True,
        arrowhead=2,
        ax=-55,
        ay=-55,
        bgcolor="white",
        bordercolor=COLOR_BORDER
    )

    base_layout(fig, "Evolución de tu inversión", "Importe (€)")
    if len(df_plot) > 10:
        fig.update_xaxes(tickangle=-35)
    return fig

def crear_figura_comparativa_aportes(monto_inicial, tasa, anos, frecuencia, momento_aportacion, inflacion, impuestos, comision, crec_aporte):
    aportes = [100, 300, 500]
    fig = go.Figure()

    for aporte in aportes:
        df, _ = calcular_escenario(
            f"{aporte} €/periodo",
            monto_inicial, aporte, tasa, anos, frecuencia, momento_aportacion,
            inflacion, impuestos, comision, crec_aporte
        )
        df_plot, _ = preparar_df_plot(df, frecuencia)

        fig.add_trace(go.Scatter(
            x=df_plot["Etiqueta"],
            y=df_plot["Valor total neto"],
            mode="lines",
            name=f"{aporte} €/periodo",
            line=dict(width=3)
        ))

    base_layout(fig, "Comparativa rápida según aportación", "Importe (€)")
    if len(df_plot) > 10:
        fig.update_xaxes(tickangle=-35)
    return fig

# =========================================================
# TABLA
# =========================================================
def crear_tabla(df):
    df_out = df.copy()
    columnas_euro = [
        "Aporte del período", "Capital aportado", "Interés bruto",
        "Impuestos teóricos", "Interés neto", "Valor total bruto",
        "Valor total neto", "Valor real neto"
    ]
    for col in columnas_euro:
        df_out[col] = df_out[col].map(formatear_euros_es)

    return dash_table.DataTable(
        columns=[{"name": c, "id": c} for c in df_out.columns if c != "Etiqueta"],
        data=df_out.drop(columns=["Etiqueta"]).to_dict("records"),
        page_size=12,
        sort_action="native",
        filter_action="native",
        style_table={"overflowX": "auto"},
        style_cell={
            "textAlign": "center",
            "padding": "8px",
            "fontFamily": "Arial",
            "fontSize": "13px",
            "minWidth": "110px",
            "whiteSpace": "normal"
        },
        style_header={"fontWeight": "700", "backgroundColor": "#f8fafc"},
        style_data_conditional=[{"if": {"row_index": "odd"}, "backgroundColor": "#fbfbfb"}]
    )

# =========================================================
# COMPONENTES UI
# =========================================================
def navbar():
    return html.Div(
        dbc.Container([
            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.Div("●", style={"color": COLOR_PRIMARY, "fontSize": "20px", "lineHeight": "1"}),
                        html.Div(BRAND_NAME, style={"fontWeight": "800", "color": COLOR_TEXT, "fontSize": "1rem"})
                    ], style={"display": "flex", "alignItems": "center", "gap": "8px"}),
                    md=6
                ),
                dbc.Col(
                    html.Div([
                        html.A("Simulador", href="#simulador", style={"color": COLOR_MUTED, "textDecoration": "none", "fontWeight": "600"}),
                        html.A("Comparativa", href="#comparativa", style={"color": COLOR_MUTED, "textDecoration": "none", "fontWeight": "600"}),
                        html.A("FAQ", href="#faq", style={"color": COLOR_MUTED, "textDecoration": "none", "fontWeight": "600"}),
                    ], style={"display": "flex", "justifyContent": "flex-end", "gap": "18px"}),
                    md=6
                )
            ], align="center")
        ], fluid=True),
        style={
            "position": "sticky",
            "top": "0",
            "zIndex": "1000",
            "backgroundColor": "rgba(255,255,255,0.92)",
            "backdropFilter": "blur(8px)",
            "borderBottom": f"1px solid {COLOR_BORDER}",
            "padding": "14px 0"
        }
    )

def metric_card(title, value, subtitle=None, accent=COLOR_PRIMARY, soft_bg="#ffffff"):
    return dbc.Card(
        dbc.CardBody([
            html.Div(title, style={"fontSize": "0.9rem", "color": COLOR_MUTED, "fontWeight": "600"}),
            html.Div(value, style={"fontSize": "1.55rem", "fontWeight": "800", "color": accent, "marginTop": "6px"}),
            html.Div(subtitle or "", style={"fontSize": "0.85rem", "color": COLOR_MUTED, "marginTop": "4px"})
        ]),
        style={**CARD_STYLE, "height": "100%", "backgroundColor": soft_bg}
    )

def input_block(label, component):
    return html.Div([
        html.Label(label, style=LABEL_STYLE),
        component
    ], className="mb-3")

def hero_section():
    return dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    dbc.Badge("Simulador de inversión a largo plazo", color="light", text_color="dark", className="mb-3"),
                    html.H1(
                        "Descubre cuánto podría crecer tu dinero con el interés compuesto",
                        style={"fontWeight": "800", "lineHeight": "1.1", "marginBottom": "14px", "fontSize": "2.6rem", "color": COLOR_TEXT}
                    ),
                    html.P(
                        "Calcula tu patrimonio futuro estimado con aportaciones periódicas, inflación, comisiones e impuestos. "
                        "Pensado para ahorro, ETF, fondos indexados y planificación financiera personal.",
                        style={"fontSize": "1.08rem", "color": COLOR_MUTED, "maxWidth": "780px"}
                    ),
                    html.Div([
                        dbc.Button("Calcular mi inversión", href="#simulador", color="primary", className="me-2"),
                        dbc.Button("Ver opciones para invertir", href="#cta-afiliacion", color="success")
                    ], className="mt-3"),
                    html.Div([
                        dbc.Badge("En euros", color="light", text_color="dark", className="me-2"),
                        dbc.Badge("Comparativas rápidas", color="light", text_color="dark", className="me-2"),
                        dbc.Badge("Preparada para afiliación", color="light", text_color="dark")
                    ], className="mt-4")
                ], md=8),
                dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.Div("Ejemplo orientativo", style={"fontWeight": "700", "color": COLOR_MUTED}),
                            html.H3("300 €/mes", style={"fontWeight": "800", "marginTop": "10px", "marginBottom": "4px"}),
                            html.Div("20 años · 7 % anual · 10.000 € iniciales", style={"color": COLOR_MUTED, "fontSize": "0.95rem"}),
                            html.Hr(),
                            html.Div("Resultado estimado", style={"color": COLOR_MUTED}),
                            html.H2("≈ 181.000 €", style={"fontWeight": "800", "color": COLOR_PRIMARY, "marginTop": "8px"}),
                            html.Div("Solo como simulación orientativa", style={"color": COLOR_MUTED, "fontSize": "0.82rem"})
                        ]),
                        style={
                            "borderRadius": "22px",
                            "background": "linear-gradient(180deg, #eff6ff 0%, #ffffff 100%)",
                            "border": f"1px solid {COLOR_BORDER}",
                            "boxShadow": "0 12px 30px rgba(37,99,235,0.10)"
                        }
                    )
                ], md=4)
            ])
        ]),
        style={**CARD_STYLE, "marginBottom": "20px"}
    )

def trust_block():
    return dbc.Row([
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Rápida y clara", style={"fontWeight": "800"}),
            html.P("Ve una estimación de tu patrimonio futuro en menos de un minuto.", style={"color": COLOR_MUTED, "marginBottom": "0"})
        ]), style=CARD_STYLE), md=4),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Útil para decidir", style={"fontWeight": "800"}),
            html.P("Compara escenarios y detecta el coste real de esperar más tiempo.", style={"color": COLOR_MUTED, "marginBottom": "0"})
        ]), style=CARD_STYLE), md=4),
        dbc.Col(dbc.Card(dbc.CardBody([
            html.H5("Lista para monetizar", style={"fontWeight": "800"}),
            html.P("Puedes insertar enlaces de afiliación donde el usuario ya está convencido.", style={"color": COLOR_MUTED, "marginBottom": "0"})
        ]), style=CARD_STYLE), md=4),
    ], className="g-3 mb-4")

def email_capture_block():
    return dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.H3("Captura leads con esta sección", style={"fontWeight": "800", "marginBottom": "8px"}),
                    html.P(
                        "Aquí puedes conectar más adelante un formulario real para enviar la simulación por email. "
                        "Eso te permite hacer seguimiento y monetizar después con afiliación.",
                        style={"color": COLOR_MUTED, "marginBottom": "0"}
                    )
                ], md=7),
                dbc.Col([
                    dbc.InputGroup([
                        dbc.Input(type="email", placeholder="Tu email"),
                        dbc.Button("Recibir simulación", color="dark")
                    ])
                ], md=5)
            ], align="center")
        ]),
        style={**CARD_STYLE, "marginTop": "18px"}
    )

def cta_card():
    return dbc.Card(
        dbc.CardBody([
            html.H3("¿Quieres pasar a la acción?", style={"fontWeight": "800"}),
            html.P(
                "Este es el mejor punto para colocar tus enlaces de afiliado a brokers, cuentas remuneradas o carteras indexadas. "
                "El usuario ya ha visto su potencial de crecimiento y está más predispuesto a clicar.",
                style={"color": COLOR_MUTED}
            ),
            html.Div([
                dbc.Button("Ver brokers recomendados", color="primary", href="#", className="me-2"),
                dbc.Button("Abrir cuenta remunerada", color="success", href="#", className="me-2"),
                dbc.Button("Empezar con cartera indexada", color="dark", href="#")
            ], id="cta-afiliacion")
        ]),
        style={**CARD_STYLE, "marginTop": "18px"}
    )

def seo_block():
    return dbc.Card(
        dbc.CardBody([
            html.Div(id="faq"),
            html.H2("Qué es el interés compuesto", style={"fontWeight": "800", "fontSize": "1.6rem"}),
            html.P(
                "El interés compuesto es el efecto por el que tus ganancias generan nuevas ganancias con el paso del tiempo. "
                "A largo plazo, la diferencia entre empezar pronto y empezar tarde puede ser enorme."
            ),
            html.H3("Cómo funciona esta calculadora", style={"fontWeight": "800", "fontSize": "1.2rem", "marginTop": "18px"}),
            html.P(
                "Introduce una inversión inicial, una aportación periódica, una rentabilidad anual estimada y el número de años. "
                "Después puedes ajustar inflación, impuestos y comisiones para tener una simulación más realista."
            ),
            html.H3("Por qué empezar antes importa", style={"fontWeight": "800", "fontSize": "1.2rem", "marginTop": "18px"}),
            html.P(
                "Muchas veces el mayor error no es invertir poco, sino esperar demasiado. "
                "La constancia y el tiempo suelen tener más peso que buscar la rentabilidad perfecta."
            ),
            html.H3("Preguntas frecuentes", style={"fontWeight": "800", "fontSize": "1.2rem", "marginTop": "18px"}),
            html.P("• ¿Sirve para ETF, fondos indexados o ahorro periódico? Sí, como simulación orientativa."),
            html.P("• ¿El resultado está garantizado? No, es solo una estimación."),
            html.P("• ¿Incluye impuestos reales? No, usa una aproximación simple."),
            html.P("• ¿Por qué se muestra un valor real? Porque la inflación reduce el poder adquisitivo."),
            html.P("• ¿Qué rentabilidad debería usar? Conviene probar varios escenarios, desde prudente a optimista.")
        ]),
        style={**CARD_STYLE, "marginTop": "20px"}
    )

# =========================================================
# LAYOUT
# =========================================================
app.layout = html.Div([
    navbar(),
    dbc.Container([
        html.Br(),
        hero_section(),
        trust_block(),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div(id="simulador"),
                        html.Div("Configura tu simulación", style=SECTION_TITLE_STYLE),

                        dbc.Row([
                            dbc.Col(dbc.Button("Conservador", id="preset-conservador", color="light", className="w-100"), md=4),
                            dbc.Col(dbc.Button("Base", id="preset-base", color="light", className="w-100"), md=4),
                            dbc.Col(dbc.Button("Dinámico", id="preset-dinamico", color="light", className="w-100"), md=4),
                        ], className="g-2 mb-3"),

                        input_block(
                            "Inversión inicial (€)",
                            dbc.Input(id="monto-inicial", type="number", min=0, step=100, value=10000)
                        ),
                        input_block(
                            "Aportación periódica (€)",
                            dbc.Input(id="deposito", type="number", min=0, step=50, value=300)
                        ),
                        input_block(
                            "Rentabilidad anual esperada (%)",
                            dbc.Input(id="tasa", type="number", min=0, step=0.1, value=7)
                        ),
                        input_block(
                            "Duración (años)",
                            dbc.Input(id="anos", type="number", min=1, step=1, value=20)
                        ),

                        dbc.Accordion([
                            dbc.AccordionItem([
                                input_block(
                                    "Comisión anual (%)",
                                    dbc.Input(id="comision", type="number", min=0, step=0.05, value=0.20)
                                ),
                                input_block(
                                    "Inflación anual (%)",
                                    dbc.Input(id="inflacion", type="number", min=0, step=0.1, value=2.5)
                                ),
                                input_block(
                                    "Impuestos sobre plusvalías (%)",
                                    dbc.Input(id="impuestos", type="number", min=0, step=0.5, value=19)
                                ),
                                input_block(
                                    "Crecimiento anual de aportación (%)",
                                    dbc.Input(id="crec-aporte", type="number", step=0.25, value=0)
                                ),
                                input_block(
                                    "Frecuencia",
                                    dcc.Dropdown(
                                        id="frecuencia",
                                        options=[
                                            {"label": "Mensual", "value": "mensual"},
                                            {"label": "Anual", "value": "anual"}
                                        ],
                                        value="mensual",
                                        clearable=False
                                    )
                                ),
                                input_block(
                                    "Momento de la aportación",
                                    dcc.Dropdown(
                                        id="momento-aportacion",
                                        options=[
                                            {"label": "Al inicio del período", "value": "inicio"},
                                            {"label": "Al final del período", "value": "final"}
                                        ],
                                        value="final",
                                        clearable=False
                                    )
                                ),
                            ], title="Opciones avanzadas")
                        ], start_collapsed=True, className="mb-3"),

                        dbc.Row([
                            dbc.Col(dbc.Button("Calcular", id="calcular-boton", color="primary", className="w-100"), md=6),
                            dbc.Col(dbc.Button("Reset", id="reset-boton", color="light", className="w-100"), md=6),
                        ], className="g-2"),

                        html.Hr(),

                        html.Div("Exportar", style=SECTION_TITLE_STYLE),
                        dbc.Row([
                            dbc.Col(dbc.Button("CSV", id="descargar-csv-btn", color="secondary", className="w-100"), md=4),
                            dbc.Col(dbc.Button("Excel", id="descargar-excel-btn", color="secondary", className="w-100"), md=4),
                            dbc.Col(dbc.Button("Informe HTML", id="descargar-html-btn", color="dark", className="w-100"), md=4),
                        ], className="g-2"),

                        dcc.Download(id="descargar-csv"),
                        dcc.Download(id="descargar-excel"),
                        dcc.Download(id="descargar-html"),

                        html.Div(id="mensajes-validacion", className="mt-3")
                    ])
                ], style=CARD_STYLE)
            ], md=4),

            dbc.Col([
                html.Div(id="resultado-principal")
            ], md=8)
        ]),

        seo_block(),
        html.Br()
    ], fluid=True)
], style={"backgroundColor": COLOR_BG, "minHeight": "100vh"})

# =========================================================
# PRESETS
# =========================================================
@app.callback(
    Output("monto-inicial", "value", allow_duplicate=True),
    Output("deposito", "value", allow_duplicate=True),
    Output("tasa", "value", allow_duplicate=True),
    Output("anos", "value", allow_duplicate=True),
    Output("comision", "value", allow_duplicate=True),
    Output("inflacion", "value", allow_duplicate=True),
    Output("impuestos", "value", allow_duplicate=True),
    Output("crec-aporte", "value", allow_duplicate=True),
    Input("preset-conservador", "n_clicks"),
    Input("preset-base", "n_clicks"),
    Input("preset-dinamico", "n_clicks"),
    prevent_initial_call=True
)
def aplicar_preset(n1, n2, n3):
    trigger = callback_context.triggered_id
    if trigger == "preset-conservador":
        return 10000, 200, 4.5, 20, 0.25, 2.0, 19, 0
    if trigger == "preset-base":
        return 10000, 300, 7.0, 20, 0.20, 2.5, 19, 0
    if trigger == "preset-dinamico":
        return 10000, 450, 9.0, 20, 0.20, 2.5, 19, 1.5
    return 10000, 300, 7.0, 20, 0.20, 2.5, 19, 0

# =========================================================
# RESET
# =========================================================
@app.callback(
    Output("monto-inicial", "value"),
    Output("deposito", "value"),
    Output("tasa", "value"),
    Output("anos", "value"),
    Output("comision", "value"),
    Output("inflacion", "value"),
    Output("impuestos", "value"),
    Output("crec-aporte", "value"),
    Output("frecuencia", "value"),
    Output("momento-aportacion", "value"),
    Input("reset-boton", "n_clicks"),
    prevent_initial_call=True
)
def resetear(n_clicks):
    return 10000, 300, 7, 20, 0.20, 2.5, 19, 0, "mensual", "final"

# =========================================================
# VALIDACIÓN
# =========================================================
@app.callback(
    Output("mensajes-validacion", "children"),
    Input("calcular-boton", "n_clicks"),
    State("monto-inicial", "value"),
    State("deposito", "value"),
    State("tasa", "value"),
    State("anos", "value"),
    State("inflacion", "value"),
    State("impuestos", "value"),
    State("comision", "value"),
    State("crec-aporte", "value"),
    prevent_initial_call=True
)
def mostrar_validacion(n_clicks, monto, deposito, tasa, anos, inflacion, impuestos, comision, crec_aporte):
    errores = validar_inputs(monto, deposito, tasa, anos, inflacion, impuestos, comision, crec_aporte)
    if not errores:
        return html.Div()
    return dbc.Alert([html.Div(e) for e in errores], color="danger")

# =========================================================
# RESULTADOS
# =========================================================
@app.callback(
    Output("resultado-principal", "children"),
    Input("calcular-boton", "n_clicks"),
    State("monto-inicial", "value"),
    State("deposito", "value"),
    State("tasa", "value"),
    State("anos", "value"),
    State("comision", "value"),
    State("inflacion", "value"),
    State("impuestos", "value"),
    State("crec-aporte", "value"),
    State("frecuencia", "value"),
    State("momento-aportacion", "value")
)
def render_resultado(
    n_clicks, monto_inicial, deposito, tasa, anos, comision,
    inflacion, impuestos, crec_aporte, frecuencia, momento_aportacion
):
    if not n_clicks:
        return dbc.Alert("Pulsa en «Calcular» para ver tu simulación.", color="info")

    errores = validar_inputs(monto_inicial, deposito, tasa, anos, inflacion, impuestos, comision, crec_aporte)
    if errores:
        return dbc.Alert("Corrige los errores para continuar.", color="warning")

    df, _ = calcular_escenario(
        "Base", monto_inicial, deposito, tasa, anos, frecuencia, momento_aportacion,
        inflacion, impuestos, comision, crec_aporte
    )

    df_plot, eje_x = preparar_df_plot(df, frecuencia)
    fig_principal = crear_figura_principal(df_plot)
    fig_principal.update_xaxes(title=eje_x)

    fig_comparativa = crear_figura_comparativa_aportes(
        monto_inicial, tasa, anos, frecuencia, momento_aportacion,
        inflacion, impuestos, comision, crec_aporte
    )
    fig_comparativa.update_xaxes(title=eje_x)

    valor_final = df["Valor total neto"].iloc[-1]
    valor_real = df["Valor real neto"].iloc[-1]
    capital = df["Capital aportado"].iloc[-1]
    crecimiento = df["Interés neto"].iloc[-1]
    impuestos_pagados = df["Impuestos teóricos"].iloc[-1]
    cagr = calcular_cagr(capital, valor_final, safe_int(anos))

    df_esperar, _ = calcular_escenario(
        "Esperar 3 años",
        0, deposito, tasa, max(1, safe_int(anos) - 3), frecuencia, momento_aportacion,
        inflacion, impuestos, comision, crec_aporte
    )
    coste_esperar = valor_final - df_esperar["Valor total neto"].iloc[-1]

    texto_resumen = (
        f"Si inviertes {formatear_euros_es(monto_inicial)} al inicio y aportas "
        f"{formatear_euros_es(deposito)} por período durante {safe_int(anos)} años, "
        f"podrías alcanzar aproximadamente {formatear_euros_es(valor_final)}."
    )

    insight = (
        f"De ese total, {formatear_euros_es(capital)} serían aportaciones y "
        f"{formatear_euros_es(crecimiento)} crecimiento neto estimado."
    )

    cards = dbc.Row([
        dbc.Col(metric_card("Valor final estimado", formatear_euros_es(valor_final), "Resultado nominal", COLOR_PRIMARY, COLOR_PRIMARY_SOFT), md=6, lg=3),
        dbc.Col(metric_card("Valor real estimado", formatear_euros_es(valor_real), "Descontando inflación", COLOR_REAL, "#f0fdfa"), md=6, lg=3),
        dbc.Col(metric_card("Capital aportado", formatear_euros_es(capital), "Tu dinero invertido", COLOR_DARK, "#f8fafc"), md=6, lg=3),
        dbc.Col(metric_card("CAGR estimado", formatear_pct_es(cagr * 100), "Crecimiento anual compuesto", COLOR_SUCCESS, COLOR_SUCCESS_SOFT), md=6, lg=3),
        dbc.Col(metric_card("Crecimiento neto", formatear_euros_es(crecimiento), "Tras impuestos teóricos", COLOR_SUCCESS, COLOR_SUCCESS_SOFT), md=6, lg=4),
        dbc.Col(metric_card("Impuestos teóricos", formatear_euros_es(impuestos_pagados), "Estimación simplificada", COLOR_WARNING, COLOR_WARNING_SOFT), md=6, lg=4),
        dbc.Col(metric_card("Coste de esperar 3 años", formatear_euros_es(coste_esperar), "Patrimonio futuro potencial perdido", COLOR_DANGER, COLOR_DANGER_SOFT), md=12, lg=4),
    ], className="g-3")

    tabla = crear_tabla(df)

    bloque_resumen = dbc.Card(
        dbc.CardBody([
            html.H2("Resultado de tu simulación", style={"fontWeight": "800", "fontSize": "1.7rem"}),
            html.P(texto_resumen, style={"fontSize": "1.08rem", "marginBottom": "8px"}),
            html.P(insight, style={"color": COLOR_MUTED, "marginBottom": "0"})
        ]),
        style={**CARD_STYLE, "marginBottom": "18px"}
    )

    comparativa_box = dbc.Card(
        dbc.CardBody([
            html.Div(id="comparativa"),
            html.H4("¿Qué pasa si aportas 100 €, 300 € o 500 €?", style={"fontWeight": "800", "marginBottom": "14px"}),
            html.P(
                "Este bloque ayuda mucho a convertir porque deja claro el impacto real de subir la aportación periódica.",
                style={"color": COLOR_MUTED}
            ),
            dcc.Graph(figure=fig_comparativa, style={"height": "500px"})
        ]),
        style={**CARD_STYLE, "marginTop": "18px"}
    )

    hipotesis = dbc.Card(
        dbc.CardBody([
            html.H4("Hipótesis usadas", style={"fontWeight": "800"}),
            html.Div(f"Frecuencia: {frecuencia.title()}"),
            html.Div(f"Aportación: {'Inicio' if momento_aportacion == 'inicio' else 'Final'} del período"),
            html.Div(f"Rentabilidad bruta anual: {formatear_pct_es(tasa)}"),
            html.Div(f"Comisión anual: {formatear_pct_es(comision)}"),
            html.Div(f"Inflación anual: {formatear_pct_es(inflacion)}"),
            html.Div(f"Impuestos: {formatear_pct_es(impuestos)}"),
            html.Div(f"Crecimiento anual de aportación: {formatear_pct_es(crec_aporte)}")
        ]),
        style={**CARD_STYLE, "marginTop": "18px"}
    )

    return html.Div([
        bloque_resumen,
        cards,

        dbc.Card(
            dbc.CardBody([
                html.H4("Gráfico principal", style={"fontWeight": "800", "marginBottom": "14px"}),
                dcc.Graph(figure=fig_principal, style={"height": "520px"})
            ]),
            style={**CARD_STYLE, "marginTop": "18px"}
        ),

        cta_card(),
        email_capture_block(),
        comparativa_box,

        dbc.Card(
            dbc.CardBody([
                html.H4("Detalle completo", style={"fontWeight": "800", "marginBottom": "14px"}),
                tabla
            ]),
            style={**CARD_STYLE, "marginTop": "18px"}
        ),

        hipotesis
    ])

# =========================================================
# EXPORTACIONES
# =========================================================
@app.callback(
    Output("descargar-csv", "data"),
    Input("descargar-csv-btn", "n_clicks"),
    State("monto-inicial", "value"),
    State("deposito", "value"),
    State("tasa", "value"),
    State("anos", "value"),
    State("comision", "value"),
    State("inflacion", "value"),
    State("impuestos", "value"),
    State("crec-aporte", "value"),
    State("frecuencia", "value"),
    State("momento-aportacion", "value"),
    prevent_initial_call=True
)
def descargar_csv(n_clicks, monto, deposito, tasa, anos, comision, inflacion, impuestos, crec_aporte, frecuencia, momento):
    df, _ = calcular_escenario("Base", monto, deposito, tasa, anos, frecuencia, momento, inflacion, impuestos, comision, crec_aporte)
    return dcc.send_data_frame(df.to_csv, "calculadora_interes_compuesto.csv", sep=";", index=False, encoding="utf-8-sig")

@app.callback(
    Output("descargar-excel", "data"),
    Input("descargar-excel-btn", "n_clicks"),
    State("monto-inicial", "value"),
    State("deposito", "value"),
    State("tasa", "value"),
    State("anos", "value"),
    State("comision", "value"),
    State("inflacion", "value"),
    State("impuestos", "value"),
    State("crec-aporte", "value"),
    State("frecuencia", "value"),
    State("momento-aportacion", "value"),
    prevent_initial_call=True
)
def descargar_excel(n_clicks, monto, deposito, tasa, anos, comision, inflacion, impuestos, crec_aporte, frecuencia, momento):
    df, _ = calcular_escenario("Base", monto, deposito, tasa, anos, frecuencia, momento, inflacion, impuestos, comision, crec_aporte)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Simulacion", index=False)

    output.seek(0)
    return dcc.send_bytes(output.getvalue(), "calculadora_interes_compuesto.xlsx")

@app.callback(
    Output("descargar-html", "data"),
    Input("descargar-html-btn", "n_clicks"),
    State("monto-inicial", "value"),
    State("deposito", "value"),
    State("tasa", "value"),
    State("anos", "value"),
    State("comision", "value"),
    State("inflacion", "value"),
    State("impuestos", "value"),
    State("crec-aporte", "value"),
    State("frecuencia", "value"),
    State("momento-aportacion", "value"),
    prevent_initial_call=True
)
def descargar_html(n_clicks, monto, deposito, tasa, anos, comision, inflacion, impuestos, crec_aporte, frecuencia, momento):
    df, _ = calcular_escenario("Base", monto, deposito, tasa, anos, frecuencia, momento, inflacion, impuestos, comision, crec_aporte)

    final_neto = df["Valor total neto"].iloc[-1]
    final_real = df["Valor real neto"].iloc[-1]
    capital = df["Capital aportado"].iloc[-1]
    interes = df["Interés neto"].iloc[-1]

    html_report = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Calculadora de interés compuesto - Informe</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; color: #222; }}
            h1, h2 {{ margin-bottom: 10px; }}
            .card {{ border: 1px solid #ddd; border-radius: 12px; padding: 16px; margin-bottom: 16px; }}
            table {{ border-collapse: collapse; width: 100%; font-size: 13px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: center; }}
            th {{ background: #f6f6f6; }}
        </style>
    </head>
    <body>
        <h1>Calculadora de interés compuesto</h1>
        <p>Informe generado el {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

        <div class="card">
            <h2>Resumen</h2>
            <p><strong>Capital aportado:</strong> {formatear_euros_es(capital)}</p>
            <p><strong>Crecimiento neto:</strong> {formatear_euros_es(interes)}</p>
            <p><strong>Valor final estimado:</strong> {formatear_euros_es(final_neto)}</p>
            <p><strong>Valor real estimado:</strong> {formatear_euros_es(final_real)}</p>
        </div>

        <div class="card">
            <h2>Detalle</h2>
            {df.to_html(index=False)}
        </div>
    </body>
    </html>
    """
    return dict(content=html_report, filename="informe_calculadora_interes_compuesto.html")

# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":
    app.run(debug=True)