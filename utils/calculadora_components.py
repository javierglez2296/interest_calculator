import plotly.graph_objects as go
from dash import html
import dash_bootstrap_components as dbc


# =========================
# FIGURAS
# =========================
def build_empty_figure(message, height=400):
    fig = go.Figure()
    fig.update_layout(
        template="plotly_white",
        height=height,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        annotations=[
            dict(
                text=message,
                x=0.5,
                y=0.5,
                showarrow=False,
                xref="paper",
                yref="paper",
            )
        ],
    )
    return fig


def build_main_figure(evolucion):
    x = [e["año"] for e in evolucion]
    total = [e["total"] for e in evolucion]
    aportado = [e["aportado"] for e in evolucion]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=total, name="Total"))
    fig.add_trace(go.Scatter(x=x, y=aportado, name="Aportado"))

    fig.update_layout(
        template="plotly_white",
        height=420,
        xaxis_title="Años",
        yaxis_title="€",
    )
    return fig


def build_donut(aportado, ganancia):
    fig = go.Figure(
        go.Pie(
            labels=["Aportado", "Ganancia"],
            values=[aportado, ganancia],
            hole=0.7,
        )
    )
    fig.update_layout(template="plotly_white", height=300)
    return fig


def build_montecarlo_chart(mc):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=mc["years"], y=mc["p90"], line=dict(width=0)))
    fig.add_trace(go.Scatter(x=mc["years"], y=mc["p10"], fill="tonexty"))

    fig.add_trace(go.Scatter(x=mc["years"], y=mc["p50"], name="Mediana"))
    fig.add_trace(go.Scatter(x=mc["years"], y=mc["real_p50"], name="Real", line=dict(dash="dash")))

    fig.update_layout(template="plotly_white", height=420)
    return fig


def build_hist(mc):
    fig = go.Figure(
        go.Histogram(x=mc["final_values"], nbinsx=40)
    )
    fig.update_layout(template="plotly_white", height=350)
    return fig


# =========================
# CARDS
# =========================
def metric(title, value):
    return dbc.Card(
        dbc.CardBody(
            [
                html.Div(title, className="text-muted small"),
                html.Div(value, className="fw-bold fs-4"),
            ]
        ),
        className="border-0 shadow-sm rounded-4",
    )


def premium_locked():
    return dbc.Alert(
        "Función premium. Desbloquéala para usar Monte Carlo.",
        color="warning",
        className="rounded-4",
    )
