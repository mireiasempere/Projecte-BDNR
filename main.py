
from pymongo import MongoClient
import pandas as pd
import argparse
import openpyxl


Host = 'localhost'
Port = 27017

DSN = "mongodb://{}:{}".format(Host,Port)
connection = MongoClient(DSN)

# Crear el parser d'arguments
parser = argparse.ArgumentParser(description='Processar un fitxer Excel amb les dades')

# Afegir un argument que especifiqui el nom del fitxer Excel
parser.add_argument('-f', '--file', type=str, required=True,
                    help='El nom del fitxer Excel amb les dades')

# Analitzar els arguments de la línia de comandes
args = parser.parse_args()
#print(args)
# Utilitzar l'argument per processar el fitxer Excel
print("El fitxer Excel amb les dades és:", args.file)


#em conecto a la bd
db = connection['projecte']


# Obrir el fitxer Excel
workbook = openpyxl.load_workbook(args.file)

# Seleccionar la primera fulla
fulla = workbook['Colleccions-Publicacions']

colleccio = dict() #key serà el nom
# Llegir les dades de la primera fila i imprimir-les
for row in fulla.iter_rows(min_row=2,values_only=True):
        nomCol = row[4]
        total_exemplars = row[5]
        genere = row[6]
        idioma = row[7]
        any_inici = row[8]
        any_fi =row[9]
        tancada = row[10]
        isbn = row[11] #haurre de comprobar, si ja tinc coleccio guardada, nomes es guarda isbn
        if nomCol in colleccio:
                colleccio[nomCol]["isbn"].append(isbn)
        if nomCol not in colleccio and nomCol != None:
                colleccio[nomCol] = {"total_exemplars":total_exemplars,"genere": genere, "idioma": idioma, "any_inici": any_inici, "any_fi": any_fi, "tancada": tancada, "isbn": [isbn]}
print(colleccio)

# Verificar si la colecció existeix
if "Colleccio" in db.list_collection_names():
    print("La colecció 'Colleccio' ja existeix")
    coll = db.productes
else:
    coll = db.create_collection("Colleccio")
    print("La colecció 'Colleccio' ha sigut creada")

# Tancar el fitxer Excel
workbook.close()
for key in colleccio:
        col = colleccio[key]
        db.Colleccio.insert_one({"nomCol":[nomCol],"total_exemplars":col["total_exemplars"], "genere": col["genere"], "idioma":col["idioma"],"any_inici":col["any_inici"],"any_fi":col["any_fi"],"tancada":col["tancada"],"isbn":col["isbn"]})

#tanquem la colecció
connection.close()
