import plotly.graph_objects as go

from utils.rentabilidad_alquiler import fmt_eur


def grafico_breakdown(data, cuota_anual_hipoteca=0):
    categorias = ["Ingresos", "Gastos", "IRPF", "Beneficio neto"]
    beneficio_final = data["beneficio_neto"] - cuota_anual_hipoteca
    valores = [
        data["ingresos_anuales"],
        data["gastos_anuales"] + cuota_anual_hipoteca,
        data["irpf"],
        max(beneficio_final, 0),
    ]

    fig = go.Figure()
    fig.add_bar(
        x=categorias,
        y=valores,
        text=[fmt_eur(v, 0) for v in valores],
        textposition="outside",
    )
    fig.update_layout(
        autosize=True,
        height=330,
        margin=dict(l=20, r=20, t=10, b=20),
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        yaxis_title="Euros / año",
    )
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)
    return fig


def grafico_comparativa(
    inversion_total,
    capital_aportado,
    rent_neta_sin_deuda,
    rent_sobre_capital,
    sp500_return,
    usar_hipoteca,
):
    valor_sin_deuda = inversion_total * (1 + rent_neta_sin_deuda / 100)
    valor_sp500 = inversion_total * (1 + sp500_return / 100)

    x = ["Alquiler sin deuda", "S&P 500"]
    y = [valor_sin_deuda, valor_sp500]

    if usar_hipoteca:
        valor_con_hipoteca = capital_aportado * (1 + rent_sobre_capital / 100)
        x.insert(1, "Alquiler con deuda")
        y.insert(1, valor_con_hipoteca)

    fig = go.Figure()
    fig.add_bar(
        x=x,
        y=y,
        text=[fmt_eur(v, 0) for v in y],
        textposition="outside",
    )
    fig.update_layout(
        autosize=True,
        height=330,
        margin=dict(l=20, r=20, t=10, b=20),
        showlegend=False,
        paper_bgcolor="white",
        plot_bgcolor="white",
        yaxis_title="Valor orientativo tras 1 año",
    )
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)
    return fig


def build_pro_years_chart(years, inmueble_vals, sp500_vals):
    fig = go.Figure()
    fig.add_scatter(x=years, y=inmueble_vals, mode="lines+markers", name="Inmueble")
    fig.add_scatter(x=years, y=sp500_vals, mode="lines+markers", name="S&P 500")
    fig.update_layout(
        autosize=True,
        height=360,
        margin=dict(l=20, r=20, t=10, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        yaxis_title="Valor acumulado (€)",
        xaxis_title="Año",
        legend_title="",
    )
    fig.update_xaxes(automargin=True)
    fig.update_yaxes(automargin=True)
    return fig
