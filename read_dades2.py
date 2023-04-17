# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 09:31:13 2023

@author: 34662
"""
import pandas as pd
from pymongo import MongoClient

Host = 'localhost'
Port = 27017

# ens conectem a la base de dades y creem les colleccions

DSN = "mongodb://{}:{}".format(Host,Port)
connection = MongoClient(DSN)
db = connection['projecte']

#python3 main2.py -f Dades.xlsx

parser = argparse.ArgumentParser(description='Processar un fitxer Excel amb les dades')
parser.add_argument('-f', '--file', type=str, required=True,help='El nom del fitxer Excel amb les dades')
parser.add_argument('--delete_all', action='store_true', help='Esborrar tots els continguts de la BD')
parser.add_argument('--bd', type=str, help='El nom de la base de dades')
args = parser.parse_args()
file = args.file
delete_all = args.delete_all
db = args.bd
print("El fitxer Excel amb les dades és:", file)

if delete_all:
    connection.drop_database(db)
    sys.exit(0)
try:
    #file = 'Dades.xlsx'

    # Verificar si la colecció existeix
    if "Publicacio" in db.list_collection_names():
        print("La colecció 'Publicacio' ja existeix")
        coll_publicacio = db.Publicacio
    else:
        coll_publicacio = db.create_collection("Publicacio")
        print("La colecció 'Publicacio' ha sigut creada")

        df_coll_publ = pd.read_excel(file, sheet_name="Colleccions-Publicacions", engine='openpyxl')
        dict_coll_publ = df_coll_publ.to_dict(orient="records")
        # inserim els diccionaris a les collecions
        coll_publicacio.insert_many(dict_coll_publ)

    if "Artistes" in db.list_collection_names():
        print("La colecció 'Artistes' ja existeix")
        coll_artistes = db.Artistes
    else:
        coll_artistes = db.create_collection("Artistes")
        print("La colecció 'Artistes' ha sigut creada")

        df_artistes = pd.read_excel(file, sheet_name="Artistes", engine='openpyxl')
        dict_artistes = df_artistes.to_dict(orient="records")
        # inserim els diccionaris a les collecions
        coll_artistes.insert_many(dict_artistes)

    if "Personatges" in db.list_collection_names():
        print("La colecció 'Personatges' ja existeix")
        coll_personatges = db.Personatges
    else:
        coll_personatges = db.create_collection("Personatges")
        print("La colecció 'Personatges' ha sigut creada")

        df_personatges = pd.read_excel(file, sheet_name="Personatges", engine='openpyxl')
        dict_personatges = df_personatges.to_dict(orient="records")
        # inserim els diccionaris a les collecions
        coll_personatges.insert_many(dict_personatges)

        for e in dict_personatges:
            ll_del = []
            for k in e:
                if 'Unnamed' == k[:7]:
                    ll_del.append(k)
            for k in ll_del:
                del (e[k])


    connection.close()

except  FileNotFoundError:
    connection.drop_database('projecte')
    print("Error en la lectura del fitxer. Base de dades eliminada: projecte.")

except:
    print("Error en l'execució del codi. Base de dades eliminada: projecte.")
