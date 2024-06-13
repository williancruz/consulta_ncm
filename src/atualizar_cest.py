import json
import sqlite3

conn = sqlite3.connect('fisco.sqlite')
cursor = conn.cursor()

f = open('lista_cest.json', encoding='utf-8')
dados = json.load(f)

cursor.execute("""DELETE FROM cest_descricoes""")
cursor.execute("""DELETE FROM cest_vinc_ncm""")

try:
    for anexo in dados:
        dados_anexo = dados.get(anexo)

        for i in dados_anexo:
            item = str(i['ITEM']).replace(' ', '')

            item = str(i['ITEM']).replace(' ', '')
            cest = str(i['CEST']).replace(' ', '').replace('.', '')
            ncm = str(i['NCM']).replace(' ', '').replace('.', '').split('|')
            desc = i['DESCRIÇÃO']
            revo = int(i['REVOGADO'])
            segm = int(cest[:2])

            conn.execute('INSERT INTO cest_descricoes (cod_item, cod_cest, '
                        'fk_id_segmento, descricao_cest) VALUES (?,?,?,?)',
                        (item, cest, segm, desc))
            
            for n in ncm:
                conn.execute('INSERT INTO cest_vinc_ncm (fk_cod_cest, cod_ncm, '
                             'revogado) VALUES (?,?,?)', (cest, n, revo))

except sqlite3.IntegrityError as e:
    print(e)
    conn.rollback()

conn.commit()
