import json
import urllib.request
import os.path as path
from pylatex import Document, Section, Subsection, Command, StandAloneGraphic
from pylatex.utils import bold, italic, NoEscape

jsonFile = "/Users/mariapaulaherrero/Documents/documentosPersonal/My Documents/ucv/maestria/MD/MDproyecto/dataPDF/data.json"


with open(jsonFile, 'r') as readFile:
    noticias = json.load(readFile)
readFile.close()

count = 0
for noticia in noticias:
    if count > 375:
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
    
        print(noticia["id"] + ': Trabajando la noticia ') 
    
        #bajar la imagen 
        print(noticia["id"] + ': Bajando la imagen de ' + noticia["imagen"]) 
        img = noticia["id"] + "." + (noticia["imagen"].split("."))[-1]
        if noticia["imagen"] and not path.exists(img):
            try:
                urllib.request.urlretrieve(noticia["imagen"], img)
            except Exception as e:
                print(noticia["id"] + ": ERROR buscando imagen")
                print(str(e))
        print(noticia["id"] + ': Creando pdf') 
        # Basic document
        try:
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
            doc.append(noticia["derecho"])
            doc.append(', Otros Derechos: ')
            if noticia["otrosDerechos"]:
                doc.append(noticia["otrosDerechos"])
            else:
                doc.append('NO_TIENE')    
            doc.append(', Sub Derechos: ')
            if noticia["subDerechos"]:
                doc.append(noticia["subDerechos"])
            else:
                doc.append('NO_TIENE')
            doc.append('\n')    
            doc.append(bold('EP: '))
            doc.append(noticia["EP"]+ "\n\n")
    
            doc.append(bold(italic(noticia["subtitular"])))
            doc.append("\n\n")
            if path.exists(img):
                doc.append(StandAloneGraphic(image_options="width=300px",filename=img))
                doc.append("\n")
            noticia["contenido"] = noticia["contenido"].split("|")
            for line in noticia["contenido"]:
                doc.append(line)
                doc.append("\n")

            doc.generate_pdf(noticia["id"], clean_tex=False)
        except:
            print(noticia["id"] + ": ERROR generando PDF")
    
    count += 1
    if count>376:
        break
    