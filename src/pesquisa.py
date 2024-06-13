import sqlite3
from os import system, name
from beautifultable import BeautifulTable

conn = sqlite3.connect('fisco.sqlite')
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


def formatar_cest(cest: str) -> str:
    return f'{cest[0:2]}.{cest[2:5]}.{cest[5:]}'


def pesquisar_cest(ncm: str) -> list:
    DQL_CEST = """SELECT b.cod_item, 
                         b.cod_cest, 
                         b.descricao_cest, 
                         c.descricao_segmento 
                  FROM cest_vinc_ncm a
                  JOIN cest_descricoes b ON a.fk_cod_cest = b.cod_cest
                  JOIN cest_segmentos c ON b.fk_id_segmento = c.id_segmento
                  WHERE (a.cod_ncm = ? OR
                        a.cod_ncm = ? OR
                        a.cod_ncm = ? OR
                        a.cod_ncm = ? OR
                        a.cod_ncm = ? OR
                        a.cod_ncm = ?) AND revogado = 0"""

    dados = cursor.execute(DQL_CEST, (ncm[:2], ncm[:4], ncm[:5], ncm[:6],
                                      ncm[:7], ncm)).fetchall()
    return dados


def pesquisar_ncm(ncm: str) -> bool:
    DQL_NCM = """SELECT COUNT(*) 
                 FROM ncm_codigos 
                 WHERE numero = ?"""

    ncm_existe = cursor.execute(DQL_NCM, (ncm,)).fetchone()

    if ncm_existe[0] == 1:
        return True
    else:
        return False


def pesquisar_ncm_hierarquia(ncm: str) -> dict:
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
    ncm = input('\nDigite o NCM/SH a procurar (0 para sair): ')
    limpar_tela()

    if ncm == '0':
        exit()
    elif len(ncm) < 8 or not ncm.isnumeric():
        print('NCM/SH Inválido! (incompleto ou contém letras/pontos)')
    else:
        if pesquisar_ncm(ncm):  # verifica se o NCM/SH existe na base
            dados_cest = pesquisar_cest(ncm)
            dados_ncm = pesquisar_ncm_hierarquia(ncm)

            if dados_cest:
                for j in dados_ncm:
                    print(f'{formatar_ncm(j[0])} - {j[1]}')

                print('\n')

                for i in dados_cest:
                    tabela.rows.append([i[0], formatar_cest(i[1]), i[3], i[2]])

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
        else:
            print("* NCM/SH não encontrado na tabela da Siscomex *")
