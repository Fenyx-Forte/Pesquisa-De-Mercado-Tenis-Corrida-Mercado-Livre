from dash import (
    Input,
    Output,
    callback,
    clientside_callback,
    html,
    register_page,
)
from dash_ag_grid import AgGrid

from dashboard.uteis import formatacoes, processamento_dados, traducoes

register_page(
    __name__,
    path="/dados",
    name="Dados",
    title="Dados",
    description="Página Dados",
    image_url="/assets/images/imagem_link.jpg",
)


layout = html.Div(
    [
        html.H1("Página Dados"),
        html.Div("Conteúdo Página Dados"),
        html.Br(),
        html.Button("Exportar CSV", id="botao-exportar-csv", n_clicks=0),
        AgGrid(
            rowData=processamento_dados.retorna_dados_dag(),
            id="meu-dag",
            columnDefs=[
                {
                    "headerName": "Marca",
                    "field": "marca",
                    "headerTooltip": "Marca tênis",
                    "cellDataType": "text",
                },
                {
                    "headerName": "Produto",
                    "field": "produto",
                    "headerTooltip": "Tênis",
                    "cellDataType": "text",
                },
                {
                    "headerName": "Preço Atual",
                    "field": "preco_atual",
                    "headerTooltip": "Preço tênis",
                    "cellDataType": "number",
                    "valueFormatter": {
                        "function": f"{formatacoes.dag_format_pt_br()}.format('$,.2f')(params.value)",
                    },
                },
                {
                    "headerName": "Promoção?",
                    "field": "promocao",
                    "headerTooltip": "Tênis em Promoção",
                    "cellDataType": "boolean",
                },
                {
                    "headerName": "Desconto",
                    "field": "percentual_promocao",
                    "headerTooltip": "Desconto tênis",
                    "cellDataType": "number",
                    "valueFormatter": {
                        "function": f"{formatacoes.dag_format_pt_br()}.format(',.2%')(params.value)",
                    },
                },
            ],
            defaultColDef={
                "resizable": True,
                "filter": True,
                "headerClass": "center-aligned-header",
                "cellClass": "center-aligned-cell",
                "wrapHeaderText": True,
                "autoHeaderHeight": True,
            },
            dashGridOptions={
                "animateRows": False,
                "suppressColumnMoveAnimation": True,
                "pagination": True,
                "tooltipShowDelay": 500,
                "alwaysMultiSort": True,
                "localeText": traducoes.dag_locale_pt_br(),
            },
            columnSize="responsiveSizeToFit",
            csvExportParams={
                "fileName": "ag_grid_test.csv",
            },
            className="ag-theme-quartz meu-dag",
        ),
    ],
    className="pagina",
)


clientside_callback(
    """
    function(nClicks) {
        if (nClicks) {
            return true;
        }
        return false;
    }
    """,
    Output("meu-dag", "exportDataAsCsv"),
    Input("botao-exportar-csv", "n_clicks"),
    prevent_initial_call=True,
)
