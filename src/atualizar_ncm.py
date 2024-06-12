import json
import sqlite3

conn = sqlite3.connect('fisco.sqlite')
cursor = conn.cursor()

f = open('lista_ncm.json', encoding='utf-8')
data = json.load(f)

cursor.execute("""DELETE FROM ncm_codigos""")
conn.commit()

ncm_capitulos = list()
ncm_posicoes = list()
ncm_subposicoes = list()
ncm_itens = list()
ncm_subitens = list()


def limpar_desc(desc: str):
    desc = desc.replace("<i>", "")
    desc = desc.replace("</i>", "")
    desc = desc.replace("--", "")
    desc = desc.replace("- ", "")
    desc = desc.replace(":", "")
    desc = desc.replace("  ", " ")
    desc = desc.lstrip()

    return desc


for i in data['Nomenclaturas']:
    cod = str(i['Codigo'])
    cod = cod.replace(".", "")
    desc = limpar_desc(i['Descricao'])

    din = i['Data_Inicio']
    dfi = i['Data_Fim']
    tpo = i['Tipo_Ato_Ini']
    nat = i['Numero_Ato_Ini']
    ano = i['Ano_Ato_Ini']

    conn.execute("""INSERT INTO ncm_codigos (numero, descricao, data_inicio, 
                 data_fim, ato_tipo, ato_nro, ato_ano) VALUES (?,?,?,?,?,?,?)""",
                 (cod, desc, din, dfi, tpo, nat, ano))


#     '''
#     CAPÍTULOS
#     '''
#     if len(cod) == 2:
#         ncm_capitulos.append((cod, desc, din, dfi, tpo, nat, ano))

#     '''
#     POSIÇÃO
#     Como regra, serão apresentados os 4 dígitos de cada posição e suas
#     respectivas descrições, bem como será disponibilizada a opção para
#     consultar os desdobramentos de cada posição.

#     Exceções:
#     1. Quando uma posição não tiver desdobramentos em nível de subposição, mas
#         tiver desdobramentos em nível de item, o código da posição será
#         apresentado com 6 dígitos (4 dígitos da posição + 2 zeros);
#     2. Quando uma posição não tiver desdobramentos em nível de suposição, nem
#         em nível de item, o código da posição será apresentado com 8 dígitos
#         (4 dígitos da posição + 4 zeros).
#     '''
#     if (len(cod) == 4 or
#         (len(cod) == 6 and cod.endswith('00')) or
#                 (len(cod) == 8 and cod.endswith('0000'))
#         ):
#         ncm_posicoes.append((cod, desc, din, dfi, tpo, nat, ano))

#     '''
#     SUBPOSIÇÃO
#     '''
#     if len(cod) == 5:
#         ncm_subposicoes.append((cod, desc, din, dfi, tpo, nat, ano))

#     if len(cod) == 6 and not cod.endswith('00'):
#         if desc.startswith(' '):
#             desc = desc[1:]
#         else:
#             ncm_subposicoes.append((cod, desc, din, dfi, tpo, nat, ano))

#     if len(cod) == 8 and not cod.endswith('0000') and cod.endswith('00'):
#         if desc.startswith(' '):
#             desc = desc[1:]
#         else:
#             ncm_subposicoes.append((cod, desc, din, dfi, tpo, nat, ano))

#     '''
#     ITEM
#     '''
#     if len(cod) == 7:
#         ncm_itens.append((cod, desc, din, dfi, tpo, nat, ano))

#     if len(cod) == 8 and not cod.endswith('0000') and not cod.endswith('00') and cod.endswith('0'):
#         ncm_itens.append((cod, desc, din, dfi, tpo, nat, ano))

#     '''
#     SUBITEM
#     '''
#     if len(cod) == 8 and not cod.endswith('0000') and not cod.endswith('00') and not cod.endswith('0'):
#         ncm_subitens.append((cod, desc, din, dfi, tpo, nat, ano))


# # === GRAVANDO OS DADOS NO BANCO =======================================
# for c in ncm_capitulos:
#     conn.execute("""INSERT INTO ncm_capitulos (numero, descricao, data_inicio, data_fim, ato_tipo, ato_nro, ato_ano) VALUES (?,?,?,?,?,?,?)""",
#                  (c[0], c[1], c[2], c[3], c[4], c[5], c[6]))

# for p in ncm_posicoes:
#     conn.execute("""INSERT INTO ncm_posicoes (numero, descricao, data_inicio, data_fim, ato_tipo, ato_nro, ato_ano) VALUES (?,?,?,?,?,?,?)""",
#                  (p[0], p[1], p[2], p[3], p[4], p[5], p[6]))

# for s in ncm_subposicoes:
#     conn.execute("""INSERT INTO ncm_subposicoes (numero, descricao, data_inicio, data_fim, ato_tipo, ato_nro, ato_ano) VALUES (?,?,?,?,?,?,?)""",
#                  (s[0], s[1], s[2], s[3], s[4], s[5], s[6]))

# for i in ncm_itens:
#     conn.execute("""INSERT INTO ncm_itens (numero, descricao, data_inicio, data_fim, ato_tipo, ato_nro, ato_ano) VALUES (?,?,?,?,?,?,?)""",
#                  (i[0], i[1], i[2], i[3], i[4], i[5], i[6]))

# for si in ncm_subitens:
#     conn.execute("""INSERT INTO ncm_subitens (numero, descricao, data_inicio, data_fim, ato_tipo, ato_nro, ato_ano) VALUES (?,?,?,?,?,?,?)""",
#                  (si[0], si[1], si[2], si[3], si[4], si[5], si[6]))


f.close()
conn.commit()
conn.close()
