import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from components.disclaimer_afiliados import build_disclaimer

dash.register_page(
    __name__,
    path="/vivienda-vs-bolsa",
    name="Vivienda vs bolsa",
    title="Invertir en vivienda vs bolsa: qué es mejor en 2026 | interescompuesto.app",
    description="Comparamos invertir en vivienda para alquilar frente a invertir en bolsa: rentabilidad, liquidez, riesgo, impuestos, esfuerzo y escalabilidad.",
)

layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.Div(
                        "INVERSIÓN · VIVIENDA · BOLSA",
                        className="text-uppercase fw-bold mb-3",
                        style={
                            "letterSpacing": "0.08em",
                            "color": "#64748b",
                            "fontSize": "0.85rem",
                        },
                    ),

                    html.H1(
                        "Invertir en vivienda vs bolsa: qué es mejor en 2026",
                        className="fw-bold mb-4",
                        style={
                            "fontSize": "clamp(2.2rem, 5vw, 4.2rem)",
                            "lineHeight": "1.05",
                            "color": "#0f172a",
                        },
                    ),

                    html.P(
                        "Comprar un piso para alquilar o invertir en bolsa son dos de las formas más populares de construir patrimonio. "
                        "Pero no funcionan igual, no tienen el mismo riesgo y tampoco exigen el mismo nivel de implicación.",
                        className="lead mb-4",
                        style={"color": "#475569"},
                    ),

                    dbc.Alert(
                        [
                            html.Strong("Resumen rápido: "),
                            "la vivienda puede ser interesante si compras bien, usas deuda de forma prudente y aceptas dedicar tiempo. "
                            "La bolsa suele ser más líquida, más escalable y más pasiva, aunque con mayor volatilidad visible."
                        ],
                        color="info",
                        className="rounded-4 border-0 shadow-sm mb-5",
                    ),

                    html.Div(
                        [
                            dbc.Button(
                                "Calcular rentabilidad de un alquiler",
                                href="/rentabilidad-alquiler",
                                color="primary",
                                className="rounded-pill px-4 py-2 me-2 mb-2 fw-bold",
                            ),
                            dbc.Button(
                                "Comparar inversiones",
                                href="/comparador",
                                color="light",
                                className="rounded-pill px-4 py-2 mb-2 fw-bold border",
                            ),
                        ],
                        className="mb-5",
                    ),

                    build_disclaimer(),

                    html.H2("La gran diferencia: activo real vs activo financiero", className="fw-bold mt-5 mb-3"),
                    html.P(
                        "La vivienda es un activo real: puedes verla, tocarla y alquilarla. La bolsa, en cambio, representa participaciones en empresas. "
                        "Ambas pueden generar riqueza, pero la experiencia como inversor es completamente distinta.",
                        className="mb-4",
                    ),

                    html.P(
                        "En vivienda, la rentabilidad depende mucho del precio de compra, la zona, la financiación, los impuestos, la ocupación, los gastos y la gestión. "
                        "En bolsa, la rentabilidad depende principalmente del comportamiento de los mercados y de tu disciplina para mantener la inversión a largo plazo.",
                        className="mb-4",
                    ),

                    html.H2("Ventajas de invertir en vivienda", className="fw-bold mt-5 mb-3"),
                    html.Ul(
                        [
                            html.Li("Puede generar ingresos mensuales relativamente estables si está bien alquilada."),
                            html.Li("Permite usar financiación bancaria, es decir, apalancamiento."),
                            html.Li("Puede proteger parcialmente frente a la inflación si suben los alquileres y el valor del inmueble."),
                            html.Li("Psicológicamente es más fácil de mantener porque no ves una cotización diaria."),
                        ],
                        className="mb-4",
                    ),

                    html.H2("Desventajas de invertir en vivienda", className="fw-bold mt-5 mb-3"),
                    html.Ul(
                        [
                            html.Li("Necesita mucho capital inicial: entrada, impuestos, notaría, reforma y colchón de seguridad."),
                            html.Li("No es una inversión pasiva al 100%: hay inquilinos, averías, seguros, comunidad, IBI y gestión."),
                            html.Li("Es poco líquida: vender un piso puede tardar meses."),
                            html.Li("Está muy concentrada: si compras un solo piso, dependes de una zona, un inmueble y un inquilino."),
                        ],
                        className="mb-4",
                    ),

                    html.H2("Ventajas de invertir en bolsa", className="fw-bold mt-5 mb-3"),
                    html.Ul(
                        [
                            html.Li("Es muy líquida: puedes vender participaciones fácilmente."),
                            html.Li("Permite empezar con poco dinero y aportar cada mes."),
                            html.Li("Es muy diversificada si inviertes mediante fondos indexados o ETF globales."),
                            html.Li("Requiere menos gestión diaria que una vivienda alquilada."),
                        ],
                        className="mb-4",
                    ),

                    html.H2("Desventajas de invertir en bolsa", className="fw-bold mt-5 mb-3"),
                    html.Ul(
                        [
                            html.Li("La volatilidad es visible: puedes ver caídas del 20%, 30% o más en determinados periodos."),
                            html.Li("Exige disciplina para no vender en malos momentos."),
                            html.Li("No genera necesariamente una renta mensual directa salvo que vendas participaciones o cobres dividendos."),
                            html.Li("No puedes controlar el resultado a corto plazo."),
                        ],
                        className="mb-4",
                    ),

                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H3("Ejemplo simple: 100.000€ en vivienda vs bolsa", className="fw-bold mb-3"),
                                html.P(
                                    "Imagina que tienes 100.000€ disponibles. Podrías usarlos como entrada para comprar una vivienda con hipoteca, "
                                    "o invertirlos en una cartera indexada global.",
                                    className="mb-3",
                                ),
                                html.P(
                                    "En vivienda, el resultado dependerá de si compras barato, de cuánto pagas de intereses, del alquiler neto, de los gastos y de la revalorización. "
                                    "En bolsa, el resultado dependerá de la rentabilidad anual media y de tu capacidad para mantenerte invertido.",
                                    className="mb-0",
                                ),
                            ]
                        ),
                        className="rounded-4 border-0 shadow-sm my-5",
                    ),

                    html.H2("Rentabilidad: no mires solo el alquiler bruto", className="fw-bold mt-5 mb-3"),
                    html.P(
                        "Uno de los errores más habituales al analizar una vivienda es fijarse solo en la rentabilidad bruta. "
                        "Por ejemplo, si compras un piso por 200.000€ y lo alquilas por 900€ al mes, podrías pensar que la rentabilidad es del 5,4% anual.",
                        className="mb-4",
                    ),

                    html.P(
                        "Pero de ahí hay que restar gastos: comunidad, IBI, seguros, mantenimiento, posibles meses vacíos, impuestos y financiación. "
                        "La cifra realmente importante es la rentabilidad neta y, si hay hipoteca, el cashflow mensual después de pagar la cuota.",
                        className="mb-4",
                    ),

                    dbc.Alert(
                        [
                            html.Strong("Consejo: "),
                            "antes de comprar una vivienda, calcula siempre la rentabilidad neta, el cashflow mensual y un escenario pesimista con menor ocupación o tipos más altos."
                        ],
                        color="warning",
                        className="rounded-4 border-0 shadow-sm mb-5",
                    ),

                    html.Div(
                        [
                            html.H3("Calcula tu caso concreto", className="fw-bold mb-3"),
                            html.P(
                                "Puedes usar nuestra calculadora para estimar ingresos, gastos, hipoteca, cashflow y rentabilidad real de una vivienda en alquiler.",
                                className="mb-3",
                            ),
                            dbc.Button(
                                "Ir a la calculadora de rentabilidad alquiler",
                                href="/rentabilidad-alquiler",
                                color="success",
                                className="rounded-pill px-4 py-2 fw-bold",
                            ),
                        ],
                        className="p-4 p-md-5 rounded-4 shadow-sm my-5",
                        style={
                            "background": "linear-gradient(135deg, #ecfdf5 0%, #f8fafc 100%)",
                            "border": "1px solid #d1fae5",
                        },
                    ),

                    html.H2("Riesgo: la bolsa parece más arriesgada, pero no siempre lo es", className="fw-bold mt-5 mb-3"),
                    html.P(
                        "La bolsa parece más arriesgada porque el precio cambia cada día. Sin embargo, una vivienda también tiene riesgos: "
                        "impagos, okupación, reformas inesperadas, cambios regulatorios, concentración geográfica, bajadas de precio o dificultad para vender.",
                        className="mb-4",
                    ),

                    html.P(
                        "La diferencia es que el riesgo inmobiliario se ve menos. No recibes una cotización diaria del piso, pero eso no significa que no pueda bajar de valor o generar problemas.",
                        className="mb-4",
                    ),

                    html.H2("Liquidez: aquí gana claramente la bolsa", className="fw-bold mt-5 mb-3"),
                    html.P(
                        "Si necesitas dinero rápido, una cartera de fondos o ETF puede venderse con facilidad. Una vivienda no. "
                        "Vender un inmueble puede tardar meses, implicar negociación, gastos y posibles rebajas de precio.",
                        className="mb-4",
                    ),

                    html.P(
                        "Por eso, antes de comprar vivienda como inversión, conviene mantener un colchón de liquidez suficiente. "
                        "No deberías quedarte sin efectivo después de pagar la entrada, los impuestos y la reforma.",
                        className="mb-4",
                    ),

                    html.H2("Fiscalidad: depende mucho del caso", className="fw-bold mt-5 mb-3"),
                    html.P(
                        "La fiscalidad puede cambiar mucho según el país, la comunidad autónoma, el tipo de activo y tu situación personal. "
                        "En vivienda, hay impuestos de compra, posibles deducciones, tributación del alquiler y tributación de la ganancia en venta. "
                        "En bolsa, normalmente tributas por dividendos, intereses o plusvalías cuando vendes.",
                        className="mb-4",
                    ),

                    html.P(
                        "Por eso no conviene decidir solo por la fiscalidad. Lo importante es comparar la rentabilidad neta después de impuestos, gastos y tiempo dedicado.",
                        className="mb-4",
                    ),

                    html.H2("Escalabilidad: aquí gana la bolsa", className="fw-bold mt-5 mb-3"),
                    html.P(
                        "Invertir 500€ al mes en bolsa es sencillo. Comprar una vivienda cada pocos años es mucho más complejo. "
                        "Necesitas más capital, financiación, análisis, gestión y tolerancia al riesgo concentrado.",
                        className="mb-4",
                    ),

                    html.P(
                        "Por eso muchos inversores combinan ambas estrategias: bolsa para diversificación global y vivienda si aparece una buena oportunidad concreta.",
                        className="mb-4",
                    ),

                    html.H2("Entonces, ¿qué es mejor?", className="fw-bold mt-5 mb-3"),
                    html.P(
                        "No hay una respuesta universal. La vivienda puede ser mejor si compras con descuento, financias bien, consigues buen alquiler y aceptas gestionarla. "
                        "La bolsa puede ser mejor si buscas simplicidad, diversificación, liquidez y escalabilidad.",
                        className="mb-4",
                    ),

                    dbc.Table(
                        [
                            html.Thead(
                                html.Tr(
                                    [
                                        html.Th("Criterio"),
                                        html.Th("Vivienda"),
                                        html.Th("Bolsa"),
                                    ]
                                )
                            ),
                            html.Tbody(
                                [
                                    html.Tr([html.Td("Liquidez"), html.Td("Baja"), html.Td("Alta")]),
                                    html.Tr([html.Td("Gestión"), html.Td("Media/alta"), html.Td("Baja")]),
                                    html.Tr([html.Td("Diversificación"), html.Td("Baja si tienes pocos inmuebles"), html.Td("Alta con fondos globales")]),
                                    html.Tr([html.Td("Capital inicial"), html.Td("Alto"), html.Td("Bajo")]),
                                    html.Tr([html.Td("Apalancamiento"), html.Td("Sí, vía hipoteca"), html.Td("No recomendado para la mayoría")]),
                                    html.Tr([html.Td("Escalabilidad"), html.Td("Media/baja"), html.Td("Alta")]),
                                ]
                            ),
                        ],
                        bordered=False,
                        hover=True,
                        responsive=True,
                        className="my-5",
                    ),

                    html.H2("Mi conclusión", className="fw-bold mt-5 mb-3"),
                    html.P(
                        "Si estás empezando o quieres una estrategia sencilla, la bolsa suele ser más eficiente y escalable. "
                        "Si ya tienes capital, entiendes bien el mercado inmobiliario y encuentras una operación con buenos números, "
                        "la vivienda puede tener sentido como complemento.",
                        className="mb-4",
                    ),

                    html.P(
                        "La clave no es elegir vivienda o bolsa por moda. La clave es hacer números. Y hacerlos con escenarios realistas.",
                        className="mb-4",
                    ),

                    html.Div(
                        [
                            html.H3("Compara tus opciones antes de decidir", className="fw-bold mb-3"),
                            html.P(
                                "Usa nuestras calculadoras para estimar si te conviene más comprar una vivienda para alquilar o invertir el capital en bolsa.",
                                className="mb-4",
                            ),
                            dbc.Button(
                                "Comparar inversiones",
                                href="/comparador",
                                color="primary",
                                className="rounded-pill px-4 py-2 me-2 mb-2 fw-bold",
                            ),
                            dbc.Button(
                                "Calcular rentabilidad alquiler",
                                href="/rentabilidad-alquiler",
                                color="success",
                                className="rounded-pill px-4 py-2 mb-2 fw-bold",
                            ),
                        ],
                        className="p-4 p-md-5 rounded-4 shadow-sm my-5 text-center",
                        style={
                            "background": "linear-gradient(135deg, #eff6ff 0%, #ffffff 100%)",
                            "border": "1px solid #dbeafe",
                        },
                    ),

                    html.H2("Preguntas frecuentes", className="fw-bold mt-5 mb-4"),

                    html.H3("¿Es más segura la vivienda que la bolsa?", className="fw-bold h5"),
                    html.P(
                        "No necesariamente. La vivienda parece más estable porque no cotiza diariamente, pero también tiene riesgos: "
                        "impagos, gastos imprevistos, baja liquidez y concentración.",
                        className="mb-4",
                    ),

                    html.H3("¿Puedo vivir antes de rentas con vivienda?", className="fw-bold h5"),
                    html.P(
                        "Puede ser posible si acumulas suficientes inmuebles con cashflow positivo, pero exige capital, deuda, gestión y tolerancia a problemas operativos.",
                        className="mb-4",
                    ),

                    html.H3("¿Qué opción es más pasiva?", className="fw-bold h5"),
                    html.P(
                        "La bolsa suele ser más pasiva, especialmente usando fondos indexados o ETF diversificados. La vivienda alquilada requiere más gestión.",
                        className="mb-4",
                    ),

                    html.H3("¿Tiene sentido combinar ambas?", className="fw-bold h5"),
                    html.P(
                        "Sí. Para muchos perfiles, una combinación de inversión indexada y algún activo inmobiliario bien comprado puede ser razonable.",
                        className="mb-5",
                    ),

                    html.Div(
                        "Última actualización: 2026",
                        className="text-muted small mb-5",
                    ),
                ],
                lg=8,
                className="mx-auto",
            )
        )
    ],
    fluid=True,
    className="py-5 px-4",
)
