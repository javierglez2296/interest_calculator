from dash import html, dcc, clientside_callback, Output, Input, State
import dash_bootstrap_components as dbc

NAV_LINKS = [
    ("Inicio", "/"),
    ("Interés compuesto", "/calculadora"),
    ("FIRE", "/fire"),
    ("Hipoteca", "/hipoteca"),
    ("Blog", "/blog"),
]


def _build_nav_links(class_name=""):
    return [
        dbc.NavLink(
            label,
            href=href,
            active="exact",
            class_name=f"fw-semibold nav-link-custom {class_name}".strip(),
        )
        for label, href in NAV_LINKS
    ]


def create_navbar():
    desktop_links = _build_nav_links()
    mobile_links = _build_nav_links()

    brand = dcc.Link(
        html.Div(
            [
                html.Span("●", className="brand-dot"),
                html.Span("Interés Compuesto", className="brand-text"),
            ],
            className="d-flex align-items-center gap-2",
        ),
        href="/",
        style={"textDecoration": "none", "color": "inherit"},
    )

    layout = html.Div(
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            brand,
                            xs=8,
                            md=4,
                        ),
                        dbc.Col(
                            dbc.Nav(
                                desktop_links,
                                pills=False,
                                class_name="justify-content-end align-items-center flex-wrap gap-3",
                            ),
                            md=6,
                            class_name="d-none d-md-block",
                        ),
                        dbc.Col(
                            html.Div(
                                dbc.Switch(
                                    id="theme-switch",
                                    label="Dark",
                                    value=False,
                                ),
                                className="d-flex justify-content-end",
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
                                mobile_links,
                                pills=True,
                                class_name="d-md-none justify-content-center flex-wrap gap-2 pb-2",
                            ),
                            width=12,
                        ),
                        dbc.Col(
                            html.Div(
                                dbc.Switch(
                                    id="theme-switch-mobile",
                                    label="Dark mode",
                                    value=False,
                                ),
                                className="d-md-none d-flex justify-content-center pb-2",
                            ),
                            width=12,
                        ),
                    ]
                ),
            ],
            fluid=True,
        ),
        className="sticky-navbar border-bottom bg-body",
    )

    clientside_callback(
        """
        function(desktopValue, mobileValue, currentData) {
            const desktop = Boolean(desktopValue);
            const mobile = Boolean(mobileValue);

            let dark = false;

            if (desktop !== mobile) {
                dark = desktop || mobile;
            } else if (currentData && typeof currentData.dark !== "undefined") {
                dark = desktop;
            } else {
                dark = false;
            }

            document.body.classList.toggle("dark-mode", dark);
            document.documentElement.setAttribute("data-bs-theme", dark ? "dark" : "light");

            return {dark: dark};
        }
        """,
        Output("theme-store", "data"),
        Input("theme-switch", "value"),
        Input("theme-switch-mobile", "value"),
        State("theme-store", "data"),
        prevent_initial_call=False,
    )

    clientside_callback(
        """
        function(data) {
            return Boolean(data && data.dark);
        }
        """,
        Output("theme-switch", "value"),
        Input("theme-store", "data"),
        prevent_initial_call=False,
    )

    clientside_callback(
        """
        function(data) {
            return Boolean(data && data.dark);
        }
        """,
        Output("theme-switch-mobile", "value"),
        Input("theme-store", "data"),
        prevent_initial_call=False,
    )

    return layout
