import os
import os.path as path
from pylatex import Document, Section, Subsection, Command, StandAloneGraphic
from pylatex.utils import bold, italic, NoEscape
import pandas
import csv
from datetime import datetime
import ast
import urllib.request

pathRootData = "/Users/mariapaulaherrero/Desktop/MDproyecto/codigo/uso/data/"
pathRoot = "/Users/mariapaulaherrero/Desktop/MDproyecto/codigo/uso/"
noticiaR = {"id": 0, "idPeriodico": 0, "periodico":"", "url":"", "fecha":"", "fechaPublicacion":"", "autor":"", "seccion":"", "palabrasClaves":"", "titular" : "", "subtitular" : "", "imagen":"", "contenido":"", "derecho":"", "otrosDerechos":"", "subDerechos":"", "EP":""}

def crearPDF(noticia):
    noticiaID = noticia["periodico"] + "_" + noticia["idPeriodico"]
    print(noticiaID + ": trabajando la noticia") 
    
    #bajar la imagen
    img =  pathRoot + noticiaID + "." + (noticia["imagen"].split("."))[-1]
    if noticia["imagen"] and not path.exists(img):
        print(noticiaID + ': bajando la imagen de ' + noticia["imagen"] + " en dir: " + img) 
        try:
            urllib.request.urlretrieve(noticia["imagen"], img)
            #print(noticiaID + ': durmiendo 5') 
            #time.sleep(5)
        except Exception as e:
            print(noticiaID + ": ERROR buscando imagen")
            print(str(e))
    print(noticiaID + ": creando archivo PDF") 
    try:
        # Basic document
        geometry_options = {
                "head": "40pt",
                "margin": "0.5in",
                "bottom": "0.6in"
        }
        doc = Document(geometry_options=geometry_options)
        doc.preamble.append(Command('title', bold(noticia["titular"])))
        doc.preamble.append(Command('author', noticia["autor"]))
        doc.preamble.append(Command('date', noticia["fecha"]))
        doc.append(NoEscape(r'\maketitle'))
    
        doc.append(bold('URL: '))
        doc.append(noticia["url"] + "\n")
        doc.append(bold('Periodico: '))
        doc.append(noticia["periodico"] + ', ')
        doc.append('ID: ')
        doc.append(str(noticia["idPeriodico"])  + ', ')
        doc.append('Seccion: ')
        doc.append(noticia["seccion"] + '\n')
        doc.append(bold('Palabras Claves: '))
        doc.append(noticia["palabrasClaves"]+ "\n")
        doc.append(bold('Derecho: '))
        doc.append(noticia["derecho"])
        doc.append('\n')    
    
        doc.append(bold(italic(noticia["subtitular"])))
        doc.append("\n\n")
        if path.exists(img):
            doc.append(StandAloneGraphic(image_options="width=300px",filename=img))
            doc.append("\n")
        for line in noticia["contenido"]:
            doc.append(line)
            doc.append("\n")

        noticiaNombre = noticia["periodico"] + "_(" + noticia["fecha"] + ")_" + noticia["derecho"] + "_"  + noticia["idPeriodico"]
        noticiaNombre = pathRoot + noticiaNombre.replace("/", ".")
        doc.generate_pdf(noticiaNombre, clean_tex=False)
    except:
        print(noticiaID + ": ERROR generando PDF")


os.chdir(pathRootData)
ruta_app = os.getcwd()
#contenido = os.scandir(ruta_app)
contenido = sorted(os.scandir(ruta_app), key=os.path.getmtime, reverse=True)
for elemento in contenido:
    #201903071651Data.csv
    extension = "csv"
    if  elemento.is_file() and elemento.name[-len(extension):] == extension:
        print("Abriendo el archivo: " + elemento.path)
        with open(elemento.path, 'r') as readFile:
            reader = csv.reader(readFile, delimiter=';')
            rows = list(reader)
        readFile.close()
        break

os.chdir(pathRoot)
del rows[0]
for row in rows:
    #[no, autor, contenido,	derecho, fecha,	fechaPublicacion, idPeriodico, imagen, palabrasClaves, periodico, seccion, subtitular, titular,	url]
    rowID = row[9] + "_" + row[6]
    print("Trabajando la linea " + row[0] + ", noticia: " + rowID )
    noticia = noticiaR.copy()
    noticia["periodico"]    = row[9]
    noticia["idPeriodico"]  = row[6]
    noticia["imagen"]       = row[7]
    noticia["derecho"]      = row[3]
    noticia["titular"]      = row[12]
    noticia["autor"]        = row[1]
    noticia["fecha"]        = row[4]
    noticia["url"]          = row[13]
    noticia["seccion"]      = row[10]
    noticia["palabrasClaves"] = row[8]
    noticia["subtitular"]     = row[11]
    noticia["contenido"]    = row[2].split("|")
    #try:
    #    contenido = ast.literal_eval(row[2])
    #except:
    #    print(rowID + ": ERROR: evaluando contenido")
    #    print(row[2])
    #    contenido = []
    
    #noticia["contenido"] = contenido  
    #crear pdf
    crearPDF(noticia)
    