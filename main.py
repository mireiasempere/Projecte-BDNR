
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

dades = dict() #key serà el nom
# Llegir les dades de la primera fila i imprimir-les
for row in fulla.iter_rows(min_row=1,values_only=True):
        nomCol = row[4]
        total_exemplars = row[5]
        genere = row[6]
        idioma = row[7]
        any_inici = row[8]
        any_fi =row[9]
        tancada = row[10]
        isbn = row[11] #haurre de comprobar, si ja tinc coleccio guardada, nomes es guarda isbn


# Tancar el fitxer Excel
workbook.close()

#tanquem la colecció
connection.close()