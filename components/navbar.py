from dash import html, dcc, clientside_callback, Output, Input
import dash_bootstrap_components as dbc

NAV_LINKS = [
    ("Inicio", "/"),
    ("Interés compuesto", "/calculadora"),
    ("FIRE", "/fire"),
    ("Hipoteca", "/hipoteca"),
    ("Blog", "/blog"),
]

def build_navbar():
    links = [
        dbc.NavLink(label, href=href, class_name="fw-semibold")
        for label, href in NAV_LINKS
    ]

    layout = html.Div(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Link(
                                html.Div(
                                    [
                                        html.Span("●", style={"color": "#2563eb", "fontSize": "20px"}),
                                        html.Span(
                                            "Interés Compuesto",
                                            style={"fontWeight": "800", "fontSize": "1rem"},
                                        ),
                                    ],
                                    style={"display": "flex", "alignItems": "center", "gap": "8px"},
                                ),
                                href="/",
                                style={"textDecoration": "none", "color": "inherit"},
                            ),
                            md=4,
                            xs=7,
                        ),
                        dbc.Col(
                            dbc.Nav(
                                links,
                                pills=False,
                                class_name="justify-content-end flex-wrap gap-2",
                            ),
                            md=6,
                            xs=5,
                            class_name="d-none d-md-block",
                        ),
                        dbc.Col(
                            dbc.Switch(
                                id="theme-switch",
                                label="Dark",
                                value=False,
                                class_name="d-flex justify-content-end",
                            ),
                            md=2,
                            class_name="d-none d-md-block",
                        ),
                    ],
                    align="center",
                    class_name="py-3",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Nav(
                                links,
                                pills=True,
                                class_name="d-md-none justify-content-center flex-wrap gap-2 pb-2",
                            ),
                            width=12,
                        ),
                        dbc.Col(
                            dbc.Switch(
                                id="theme-switch-mobile",
                                label="Dark mode",
                                value=False,
                                class_name="d-md-none justify-content-center pb-2",
                            ),
                            width=12,
                        ),
                    ]
                ),
            ],
            fluid=True,
        ),
        className="sticky-navbar",
    )

    clientside_callback(
        """
        function(desktopValue, mobileValue, currentData) {
            const dark = Boolean(desktopValue || mobileValue);
            document.body.classList.toggle("dark-mode", dark);
            document.documentElement.setAttribute("data-bs-theme", dark ? "dark" : "light");
            return {"dark": dark};
        }
        """,
        Output("theme-store", "data"),
        Input("theme-switch", "value"),
        Input("theme-switch-mobile", "value"),
        Input("theme-store", "data"),
        prevent_initial_call=False,
    )

    clientside_callback(
        """
        function(data) {
            const dark = Boolean(data && data.dark);
            return dark;
        }
        """,
        Output("theme-switch", "value"),
        Input("theme-store", "data"),
        prevent_initial_call=False,
    )

    clientside_callback(
        """
        function(data) {
            const dark = Boolean(data && data.dark);
            return dark;
        }
        """,
        Output("theme-switch-mobile", "value"),
        Input("theme-store", "data"),
        prevent_initial_call=False,
    )

    return layout
