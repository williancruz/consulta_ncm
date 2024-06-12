import sqlite3
from os import system, name
from beautifultable import BeautifulTable

conn = sqlite3.connect('src/fisco.sqlite')
cursor = conn.cursor()


def limpar_tela():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def formatar_ncm(ncm: str) -> str:
    if len(ncm) == 2:
        return f'CAPÍTULO {ncm}'
    elif len(ncm) == 4:
        return f'{ncm[:2]}.{ncm[2:]}'
    elif len(ncm) == 5 or len(ncm) == 6:
        return f'{ncm[:4]}.{ncm[4:]}'
    elif len(ncm) == 7 or len(ncm) == 8:
        return f'{ncm[:4]}.{ncm[4:6]}.{ncm[6:]}'


def pesquisar_cest(ncm: str) -> list:
    DQL_CEST = """SELECT a.cod_item, 
                        a.cod_cest, 
                        a.descricao_cest, 
                        b.descricao_segmento 
                FROM cest_codigos a 
                    JOIN cest_segmentos b 
                    ON a.fk_id_segmento=b.id_segmento
                WHERE (cod_ncm IS ? OR 
                        cod_ncm IS ? OR 
                        cod_ncm IS ? OR 
                        cod_ncm IS ? OR 
                        cod_ncm IS ? OR 
                        cod_ncm IS ?) 
                        AND revogado IS '0'
               """

    dados = cursor.execute(DQL_CEST, (ncm[:2], ncm[:4], ncm[:5], ncm[:6],
                                      ncm[:7], ncm)
                           ).fetchall()
    return dados


def pesquisar_ncm(ncm: str) -> dict:
    DQL_NCM = """SELECT numero, descricao 
                 FROM ncm_codigos 
                 WHERE numero = ? OR 
                       numero = ? OR 
                       numero = ? OR 
                       numero = ? OR 
                       numero = ? OR 
                       numero = ?
              """
    dados = cursor.execute(DQL_NCM, (ncm[:2], ncm[:4], ncm[:5], ncm[:6],
                                     ncm[:7], ncm)).fetchall()

    return dados


tabela = BeautifulTable(maxwidth=120)
tabela.columns.header = ['ITEM', 'CEST', 'SEGMENTO', 'DESCRIÇÃO']
tabela.columns.alignment['ITEM'] = BeautifulTable.ALIGN_CENTER
tabela.columns.alignment['CEST'] = BeautifulTable.ALIGN_CENTER
tabela.columns.alignment['SEGMENTO'] = BeautifulTable.ALIGN_LEFT
tabela.columns.alignment['DESCRIÇÃO'] = BeautifulTable.ALIGN_LEFT
tabela.set_style(BeautifulTable.STYLE_COMPACT)

while True:
    tabela.clear()
    ncm = input('Digite o NCM/SH a procurar (0 para sair): ')
    limpar_tela()

    if ncm == '0':
        exit()
    elif len(ncm) < 8 or not ncm.isnumeric():
        print('NCM/SH Inválido! (incompleto ou contém letras/pontos)\n')
    else:
        dados_cest = pesquisar_cest(ncm)
        dados_ncm = pesquisar_ncm(ncm)

        if dados_cest:
            for j in dados_ncm:
                print(f'{formatar_ncm(j[0])} - {j[1]}')

            print('\n')

            for i in dados_cest:
                tabela.rows.append([i[0], i[1], i[3], i[2]])

            print(tabela)
        else:
            print("* Nenhum CEST definido para este NCM/SH * \n")

            tabela.rows.append(['999.0', '01.999.00', 'Autopeças',
                                "Outras peças, partes e acessórios para "
                                "veículos automotores não relacionados nos "
                                "demais itens deste anexo."])

            tabela.rows.append(['999.0', '28.999.00',
                                'Venda de mercadorias pelo sistema porta a porta',
                                'Outros produtos comercializados pelo sistema '
                                'de marketing direto porta-a-porta a '
                                'consumidor final não relacionados em outros '
                                'itens deste anexo.'])
            print(tabela)
