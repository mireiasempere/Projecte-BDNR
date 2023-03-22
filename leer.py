import pandas as pd
from pymongo import MongoClient

Host = 'localhost'
Port = 27017

# ens conectem a la base de dades y creem les colleccions

DSN = "mongodb://{}:{}".format(Host,Port)
connection = MongoClient(DSN)
db = connection['projecte']

coll_colleccio = db.create_collection("Colleccio")
coll_publicacio = db.create_collection("Publicació")
coll_artistes = db.create_collection("Artistes")
coll_personatges = db.create_collection("Personatges")


# llegim el fitcher de les dades i creem diccionaris

file = 'dades/Dades.xlsx'

df_personatges = pd.read_excel(file, sheet_name = "Personatges", engine='openpyxl')
dict_personatges = df_personatges.to_dict(orient = "records" )

df_artistes = pd.read_excel(file, sheet_name = "Artistes", engine='openpyxl')
dict_artistes = df_artistes.to_dict(orient = "records" )

df_coll_publ = pd.read_excel(file, sheet_name = "Personatges", engine='openpyxl')
dict_coll_publ = df_coll_publ.to_dict(orient = "records" )


# inserim els diccionaris a les collecions

coll_personatges.insert_many(dict_personatges)
coll_artistes.insert_many(dict_artistes)

connection.close()