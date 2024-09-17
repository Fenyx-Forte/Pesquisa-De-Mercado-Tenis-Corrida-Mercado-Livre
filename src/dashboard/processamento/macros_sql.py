def macro_dados_completos_por_periodo() -> str:
    query = """
    CREATE OR REPLACE MACRO dados_completos_por_periodo(data_inicio, data_fim) AS TABLE
        SELECT
            dc.marca
            , dc.preco_atual
            , dc.promocao
            , dc.percentual_promocao
            , dc.nota_avaliacao
            , dc.num_avaliacoes
            , dc.data_coleta
        FROM
            dados_completos AS dc
        WHERE
            dc.data_coleta BETWEEN data_inicio AND data_fim;
    """

    return query


def macro_top_10_marcas_periodo() -> str:
    query = """
    CREATE OR REPLACE MACRO top_10_marcas_periodo(periodo, data_inicio, data_fim) AS TABLE
        WITH porcentagem_por_dia AS (
            SELECT
                dcr.marca AS marca
                , (
                    COUNT(*) * 100.0 / (SUM(COUNT(*)) OVER(PARTITION BY dcr.data_coleta))
                ) AS porcentagem
            FROM
                dados_completos_por_periodo(data_inicio, data_fim) AS dcr
            GROUP BY
                dcr.data_coleta
                , dcr.marca
        )
        SELECT
            ppd.marca AS marca
            , AVG(ppd.porcentagem) AS porcentagem
            , periodo AS periodo
        FROM
            porcentagem_por_dia AS ppd
        GROUP BY
            ppd.marca;
    """

    return query


def macro_preco_medio_periodo() -> str:
    query = """
    CREATE OR REPLACE MACRO preco_medio_e_num_produtos_periodo(data_inicio, data_fim) AS TABLE
        WITH preco_medio_por_dia AS (
            SELECT
                dcr.marca AS marca
                , AVG(dcr.preco_atual) AS preco_medio
                , COUNT(*) AS num_produtos
            FROM
                dados_completos_por_periodo(data_inicio, data_fim) AS dcr
            GROUP BY
                dcr.data_coleta
                , dcr.marca
        )
        SELECT
            pmd.marca
            , AVG(pmd.preco_medio) AS preco_medio
            , AVG(pmd.num_produtos) AS num_produtos
        FROM
            preco_medio_por_dia AS pmd
        GROUP BY
            pmd.marca;
    """

    return query


def macro_faixa_preco_periodo() -> str:
    query = """
    CREATE OR REPLACE MACRO faixa_preco_periodo(data_inicio, data_fim) AS TABLE
        WITH faixa_preco_por_dia AS (
            SELECT
                dcr.marca AS marca
                , CASE
                    WHEN dcr.preco_atual < 200 THEN '200'
                    WHEN dcr.preco_atual BETWEEN 200 AND 400 THEN '200_400'
                    ELSE '400'
                  END AS faixa_preco
                , COUNT(*) AS num_produtos
            FROM
                dados_completos_por_periodo(data_inicio, data_fim) AS dcr
            GROUP BY
                dcr.data_coleta
                , dcr.marca
                , faixa_preco
        )
        SELECT
            fpd.marca
            , fpd.faixa_preco
            , AVG(fpd.num_produtos) AS num_produtos
        FROM
            faixa_preco_por_dia AS fpd
        GROUP BY
            fpd.marca
            , fpd.faixa_preco;
    """

    return query


def macro_media_avaliacoes_periodo() -> str:
    query = """
    CREATE OR REPLACE MACRO media_avaliacoes_periodo(data_inicio, data_fim) AS TABLE
        WITH media_avaliacoes_por_dia AS (
            SELECT
                dcr.marca AS marca
                , AVG(dcr.nota_avaliacao) AS media_avaliacao
                , AVG(dcr.num_avaliacoes) AS media_num_avaliacoes
            FROM
                dados_completos_por_periodo(data_inicio, data_fim) AS dcr
            WHERE
                dcr.num_avaliacoes > 0
            GROUP BY
                dcr.data_coleta
                , dcr.marca
        )
        SELECT
            mad.marca
            , AVG(mad.media_avaliacao) AS nota_avaliacao
            , AVG(mad.media_num_avaliacoes) AS num_avaliacoes
        FROM
            media_avaliacoes_por_dia AS mad
        GROUP BY
            mad.marca;
    """

    return query


def macro_media_promocoes_periodo() -> str:
    query = """
    CREATE OR REPLACE MACRO media_promocoes_periodo(data_inicio, data_fim) AS TABLE
        WITH media_promocoes_por_dia AS (
            SELECT
                dcr.marca AS marca
                , COUNT(*) as numero_produtos_em_promocao
                , AVG(dcr.percentual_promocao) AS percentual_medio_desconto
            FROM
                dados_completos_por_periodo(data_inicio, data_fim) AS dcr
            WHERE
                dcr.promocao = true
            GROUP BY
                dcr.data_coleta
                , dcr.marca
        )
        SELECT
            m.marca
            , AVG(m.numero_produtos_em_promocao) AS produtos
            , AVG(m.percentual_medio_desconto * 100) AS desconto
        FROM
            media_promocoes_por_dia AS m
        GROUP BY
            m.marca;
    """

    return query
