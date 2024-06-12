import json
import sqlite3

conn = sqlite3.connect('fisco.sqlite')
cursor = conn.cursor()

f = open('lista_cest.json', encoding='utf-8')
data = json.load(f)

cursor.execute("""DELETE FROM cest_codigos""")
conn.commit()

try:
    for i in data:
        item = str(i["ITEM"]).replace(' ','')
        cest = str(i['CEST']).replace(' ','')
        ncm = str(i['NCM']).replace(' ','').replace('.','').split('|')
        desc = i['DESCRIÇÃO']
        exce = i['EXCEÇÕES']
        revo = int(i['REVOGADO'])
        segm = int(cest[:2])

        for n in ncm:
            conn.execute("""INSERT INTO cest_codigos (revogado, cod_item, cod_cest, cod_ncm, fk_id_segmento, descricao_cest) VALUES (?,?,?,?,?,?)""",
                    (revo, item, cest, n, segm, desc))
except sqlite3.IntegrityError as e:
    print (e)
    conn.rollback()
        
conn.commit()