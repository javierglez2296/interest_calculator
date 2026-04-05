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
            html.Style(
                """
                .sticky-navbar {
                    position: sticky;
                    top: 0;
                    z-index: 1030;
                    backdrop-filter: blur(10px);
                    -webkit-backdrop-filter: blur(10px);
                    background: rgba(255, 255, 255, 0.88);
                    border-bottom: 1px solid rgba(16, 24, 40, 0.06);
                    transition: background 0.25s ease, border-color 0.25s ease;
                }

                [data-bs-theme="dark"] .sticky-navbar {
                    background: rgba(17, 25, 40, 0.82);
                    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                }

                .brand-mark {
                    width: 14px;
                    height: 14px;
                    border-radius: 999px;
                    background: linear-gradient(135deg, #2563eb 0%, #16a34a 100%);
                    box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.10);
                    flex-shrink: 0;
                }

                .brand-overline {
                    font-size: 0.68rem;
                    text-transform: uppercase;
                    letter-spacing: 0.08em;
                    font-weight: 700;
                    color: #667085;
                    margin-bottom: 0.05rem;
                }

                .brand-text {
                    font-size: 1.02rem;
                    font-weight: 800;
                    letter-spacing: -0.02em;
                    color: #101828;
                }

                [data-bs-theme="dark"] .brand-overline {
                    color: #98a2b3;
                }

                [data-bs-theme="dark"] .brand-text {
                    color: #f8fafc;
                }

                .navbar-links .nav-link-custom,
                .mobile-nav-wrapper .nav-link-custom {
                    border-radius: 999px;
                    padding: 0.55rem 0.95rem !important;
                    color: #475467 !important;
                    transition: all 0.2s ease;
                    border: 1px solid transparent;
                    line-height: 1.1;
                }

                .navbar-links .nav-link-custom:hover,
                .mobile-nav-wrapper .nav-link-custom:hover {
                    background: rgba(37, 99, 235, 0.08);
                    color: #1d4ed8 !important;
                    border-color: rgba(37, 99, 235, 0.10);
                }

                .navbar-links .nav-link-custom.active,
                .mobile-nav-wrapper .nav-link-custom.active {
                    background: rgba(37, 99, 235, 0.12);
                    color: #1d4ed8 !important;
                    border-color: rgba(37, 99, 235, 0.12);
                    box-shadow: inset 0 0 0 1px rgba(37, 99, 235, 0.03);
                }

                [data-bs-theme="dark"] .navbar-links .nav-link-custom,
                [data-bs-theme="dark"] .mobile-nav-wrapper .nav-link-custom {
                    color: #cbd5e1 !important;
                }

                [data-bs-theme="dark"] .navbar-links .nav-link-custom:hover,
                [data-bs-theme="dark"] .mobile-nav-wrapper .nav-link-custom:hover {
                    background: rgba(59, 130, 246, 0.16);
                    color: #dbeafe !important;
                    border-color: rgba(96, 165, 250, 0.18);
                }

                [data-bs-theme="dark"] .navbar-links .nav-link-custom.active,
                [data-bs-theme="dark"] .mobile-nav-wrapper .nav-link-custom.active {
                    background: rgba(59, 130, 246, 0.20);
                    color: #dbeafe !important;
                    border-color: rgba(96, 165, 250, 0.18);
                }

                .nav-link-mobile {
                    font-size: 0.95rem;
                }

                .theme-switch-custom .form-check-label {
                    font-weight: 600;
                    color: #475467;
                    font-size: 0.92rem;
                }

                [data-bs-theme="dark"] .theme-switch-custom .form-check-label {
                    color: #cbd5e1;
                }

                .mobile-nav-wrapper {
                    border-top: 1px solid rgba(16, 24, 40, 0.05);
                    margin-top: 0.15rem;
                }

                [data-bs-theme="dark"] .mobile-nav-wrapper {
                    border-top: 1px solid rgba(255, 255, 255, 0.06);
                }

                @media (max-width: 767.98px) {
                    .brand-text {
                        font-size: 0.98rem;
                    }

                    .brand-overline {
                        font-size: 0.62rem;
                    }

                    .sticky-navbar .container-fluid {
                        padding-left: 1rem;
                        padding-right: 1rem;
                    }
                }
                """
            ),
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
