import pandas as pd
from pymongo import MongoClient
import argparse

#python3 main2.py -f Dades.xlsx

parser = argparse.ArgumentParser(description='Processar un fitxer Excel amb les dades')
parser.add_argument('-f', '--file', type=str, required=True, 
                    help='El nom del fitxer Excel amb les dades')
args = parser.parse_args()
file = args.file
print("El fitxer Excel amb les dades és:", file)


########################################### Data Personatges

df_personatges = pd.read_excel(file, sheet_name = "Personatges", engine='openpyxl')
data_personatges = df_personatges.to_dict(orient = "records" )

characters = {}
for record in data_personatges:
    name,role,book = record["nom"],record["tipus"],int(record["isbn"])
    if name not in characters:
        characters[name] = {"_id": name, "tipus": role, "isbn": [book]}
    else:
        characters[name]["isbn"].append(book)
data_personatges = list(characters.values())

########################################### Data Artistes

df_artistes = pd.read_excel(file, sheet_name = "Artistes", engine='openpyxl')
data_artistes = df_artistes.to_dict(orient = "records" )
for data in data_artistes:
    data['_id'] = data.pop("Nom_artistic")


df_edi_coll_publ = pd.read_excel(file, sheet_name = "Colleccions-Publicacions", engine='openpyxl')

########################################### Data Editorials

data_editorial = df_edi_coll_publ[['NomEditorial','resposable','adreca','pais','NomColleccio']].to_dict('records')

editoriales = {}
for record in data_editorial:
    name, role, address, country, collection = record["NomEditorial"], record["resposable"], record["adreca"], record["pais"], record["NomColleccio"]
    
    if name not in editoriales:
        editoriales[name] = {"_id": name, "resposable": role, "adreca": address, "pais": country,"colecciones": [collection]}
    else:
        editoriales[name]["colecciones"].append(collection)

data_editorial = list(editoriales.values())
for editorial in data_editorial:
    editorial["colecciones"] = list(set(editorial["colecciones"]))

########################################### Data Colleccions

colleccio_data = df_edi_coll_publ[['NomColleccio','total_exemplars','genere','idioma','any_inici','any_fi','tancada','ISBN']].to_dict('records')

colecciones = {}
for record in colleccio_data:
    name, total_exemplars, genre, language, year_start, year_end, closed, isbn = record["NomColleccio"], record["total_exemplars"], record["genere"], record["idioma"], record["any_inici"], record["any_fi"], record["tancada"], int(record["ISBN"])
    
    if name not in colecciones:
        colecciones[name] = {"_id": name, "total_exemplars": total_exemplars, "genere": genre, "idioma": language, "any_inici": year_start, "any_fi": year_end, "tancada": closed, "publicaciones": [isbn]}
    else:
        colecciones[name]["publicaciones"].append(isbn)
        
colleccio_data = list(colecciones.values())
for coleccion in colleccio_data:
    colecciones["publicaciones"] = list(set(coleccion["publicaciones"]))


########################################### Data Publicación

publicacion_data = df_edi_coll_publ[['ISBN','titol','stock','autor','preu','num_pagines','guionistes','dibuixants']].to_dict('records')
for data in publicacion_data:
    data['_id'] = data.pop("ISBN")
    data['guionistes'] = data['guionistes'].strip("[]").split(", ")
    data['dibuixants'] = data['dibuixants'].strip("[]").split(", ")

########################################### Crear connexio base de dades

Host = 'localhost'
Port = 27017

DSN = "mongodb://{}:{}".format(Host,Port)
connection = MongoClient(DSN)
db = connection['projecte']

lista_colecciones = ["Editorial","Colleccio","Publicació","Artistes","Personatges"]
for i in lista_colecciones:
    db.drop_collection(i)

########################################### Crear coleccions i inserir data

coll_personatges = db["Personatges"]
coll_personatges.insert_many(data_personatges)

coll_artistes = db["Artistes"]
coll_artistes.insert_many(data_artistes)

coll_editorial = db['Editorial']
coll_editorial.insert_many(data_editorial)

coll_colleccio = db['Colleccio']
coll_colleccio.insert_many(colleccio_data)

coll_publicacion = db['Publicació']
coll_publicacion.insert_many(publicacion_data)

connection.close()