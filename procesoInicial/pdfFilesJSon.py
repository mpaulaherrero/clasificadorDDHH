import json
import urllib.request
from pylatex import Document, Section, Subsection, Command, StandAloneGraphic
from pylatex.utils import bold, italic, NoEscape

jsonFile = "/Users/mariapaulaherrero/Desktop/MDproyecto/dataPDF/data.json"


with open(jsonFile, 'r') as readFile:
    noticias = json.load(readFile)
readFile.close()

count = 0
for noticia in noticias:
    ''' print(noticia["id"]) 
    print(noticia["idPeriodico"])
    print(noticia["periodico"]) 
    print(noticia["url"])
    print(noticia["fecha"])
    print(noticia["fechaPublicacion"]) 
    print(noticia["autor"]) 
    print(noticia["seccion"]) 
    print(noticia["palabrasClaves"])
    print(noticia["titular"]) 
    print(noticia["subtitular"]) 
    print(noticia["imagen"]) 
    print(noticia["contenido"]) 
    print(noticia["derecho"]) 
    print(noticia["otrosDerechos"])
    print(noticia["subDerechos"]) 
    print(noticia["EP"]) '''
    
    print('Trabajando la noticia ' + noticia["id"]) 
    
    #bajar la imagen
    print('Bajando la imagen de ' + noticia["imagen"]) 
    img = noticia["id"] + "." + (noticia["imagen"].split("."))[-1]
    urllib.request.urlretrieve(noticia["imagen"], img)
    
    print('Creando pdf de ' + noticia["id"]) 
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
    doc.append(noticia["idPeriodico"]  + ', ')
    doc.append('Seccion: ')
    doc.append(noticia["seccion"] + '\n')
    doc.append(bold('Palabras Claves: '))
    doc.append(noticia["palabrasClaves"]+ "\n")
    doc.append(bold('Derecho: '))
    doc.append(noticia["derecho"] + ', ')
    doc.append('Otros Derechos: ')
    doc.append(noticia["otrosDerechos"]  + ', ')
    doc.append('Sub Derechos: ')
    doc.append(noticia["subDerechos"] + '\n')
    doc.append(bold('EP: '))
    doc.append(noticia["EP"]+ "\n\n")
    
    doc.append(bold(italic(noticia["subtitular"])))
    doc.append("\n\n")
    doc.append(StandAloneGraphic(image_options="width=300px",filename=img))
    doc.append("\n")
    for line in noticia["contenido"]:
        doc.append(line)
        doc.append("\n")

    doc.generate_pdf(noticia["id"], clean_tex=False)
    
    count += 1
    #if count>3:
    #    break
    