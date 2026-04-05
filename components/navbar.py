from dash import html, dcc, clientside_callback, Output, Input, State
import dash_bootstrap_components as dbc

NAV_LINKS = [
    ("Inicio", "/"),
    ("Interés compuesto", "/calculadora"),
    ("FIRE", "/fire"),
    ("Hipoteca", "/hipoteca"),
    ("Comparador", "/comparador"),
    ("Blog", "/blog"),
]


def _build_nav_links(class_name=""):
    return [
        dbc.NavLink(
            label,
            href=href,
            active="exact",
            external_link=False,
            class_name=f"fw-semibold nav-link-custom {class_name}".strip(),
        )
        for label, href in NAV_LINKS
    ]


def build_navbar():
    desktop_links = _build_nav_links()
    mobile_links = _build_nav_links("nav-link-mobile")

    brand = dcc.Link(
        html.Div(
            [
                html.Div(className="brand-mark"),
                html.Div(
                    [
                        html.Span("interescompuesto.app", className="brand-overline d-block"),
                        html.Span("Interés Compuesto", className="brand-text"),
                    ],
                    className="d-flex flex-column lh-sm",
                ),
            ],
            className="d-flex align-items-center gap-2",
        ),
        href="/",
        style={"textDecoration": "none", "color": "inherit"},
    )

    desktop_right = html.Div(
        [
            dbc.Nav(
                desktop_links,
                pills=False,
                class_name="justify-content-end align-items-center flex-wrap gap-2 navbar-links",
            ),
            html.Div(
                dbc.Switch(
                    id="theme-switch",
                    label="Dark",
                    value=False,
                    class_name="theme-switch-custom ms-3 mb-0",
                ),
                className="d-flex align-items-center",
            ),
        ],
        className="d-none d-md-flex justify-content-end align-items-center",
    )

    mobile_block = html.Div(
        [
            dbc.Nav(
                mobile_links,
                pills=False,
                class_name="d-md-none justify-content-center flex-wrap gap-2 pt-2 pb-2 mobile-nav-wrapper",
            ),
            html.Div(
                dbc.Switch(
                    id="theme-switch-mobile",
                    label="Dark mode",
                    value=False,
                    class_name="theme-switch-custom mb-0",
                ),
                className="d-md-none d-flex justify-content-center pb-2",
            ),
        ]
    )

    layout = html.Div(
        [
            dbc.Container(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                brand,
                                xs=12,
                                md=4,
                                class_name="py-3",
                            ),
                            dbc.Col(
                                desktop_right,
                                md=8,
                                class_name="py-3",
                            ),
                        ],
                        align="center",
                        class_name="g-0",
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                mobile_block,
                                width=12,
                            ),
                        ],
                        class_name="g-0",
                    ),
                ],
                fluid=True,
            ),
        ],
        className="sticky-navbar",
    )

    clientside_callback(
        """
        function(desktopValue, mobileValue, currentData) {
            const desktop = Boolean(desktopValue);
            const mobile = Boolean(mobileValue);
            const dark = desktop || mobile;

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
