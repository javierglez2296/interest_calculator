from dash import html
import dash_bootstrap_components as dbc

def create_footer():
    return html.Footer(
        dbc.Container(
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Hr(),
                            html.P(
                                "© 2026 interescompuesto.app · Simuladores financieros en español",
                                className="text-center muted mb-1",
                            ),
                            html.P(
                                "La información es orientativa y no constituye asesoramiento financiero personalizado.",
                                className="text-center muted small",
                            ),
                        ],
                        width=12,
                    )
                ]
            ),
            fluid=True,
        ),
        className="py-3",
    )
