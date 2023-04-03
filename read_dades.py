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

coll_publicacio = db.create_collection("Publicacio")
coll_artistes = db.create_collection("Artistes")
coll_personatges = db.create_collection("Personatges")



# llegim el fitcher de les dades i creem diccionaris

file = 'dades/Dades.xlsx'

df_personatges = pd.read_excel(file, sheet_name = "Personatges", engine='openpyxl')
dict_personatges = df_personatges.to_dict(orient = "records" )


for e in dict_personatges:
    ll_del = []
    for k in e:   
        if 'Unnamed' == k[:7]:
            ll_del.append(k)
    for k in ll_del:
        del(e[k])

df_artistes = pd.read_excel(file, sheet_name = "Artistes", engine='openpyxl')
dict_artistes = df_artistes.to_dict(orient = "records" )

df_coll_publ = pd.read_excel(file, sheet_name = "Colleccions-Publicacions", engine='openpyxl')
dict_coll_publ = df_coll_publ.to_dict(orient = "records" )


# inserim els diccionaris a les collecions

coll_personatges.insert_many(dict_personatges)
coll_artistes.insert_many(dict_artistes)
coll_publicacio.insert_many(dict_coll_publ)

connection.close()