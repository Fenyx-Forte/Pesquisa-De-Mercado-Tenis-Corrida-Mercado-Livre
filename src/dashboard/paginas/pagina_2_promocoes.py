from dash import html, register_page
from dash_ag_grid import AgGrid

register_page(
    __name__,
    path="/promocoes",
    name="Promoções",
    title="Promoções",
    description="Página Promoções",
    image="imagem_link.jpg",
)


layout = html.Div(
    [
        html.H1("Página Promoções"),
        html.Div("Conteúdo Página Promoções"),
    ],
    className="pagina",
)