import json
#import os.path as path
import os

jsonFile = "/Users/mariapaulaherrero/Documents/documentosPersonal/My Documents/ucv/maestria/MD/MDproyecto/dataPDF/data.json"
catDir = "/Users/mariapaulaherrero/Documents/documentosPersonal/My Documents/ucv/maestria/MD/MDproyecto/dataPDF/clasificacion/categorias/"
epDir = "/Users/mariapaulaherrero/Documents/documentosPersonal/My Documents/ucv/maestria/MD/MDproyecto/dataPDF/clasificacion/EP/"

with open(jsonFile, 'r') as readFile:
    noticias = json.load(readFile)
readFile.close()

#os.chdir(catDir)

for noticia in noticias:
    print('Trabajando la noticia ' + noticia["id"]) 
    
    #creo contenido TXT de la noticia
    noticiaNombre = noticia["periodico"] + "_" + noticia["idPeriodico"] + ".txt"
    noticiaTexto = noticia["titular"] + "\n" + noticia["subtitular"] + "\n"
    noticia["contenido"] = noticia["contenido"].split("|")
    for line in noticia["contenido"]:
       noticiaTexto = noticiaTexto + line + "\n"
    
    #defino directorio donde guardarlo, si no existe lo creo
    noticiaDir   = catDir + noticia["derecho"] + '/'
    noticiaDirEP = epDir + noticia["EP"] + '/'
    if not os.path.exists(noticiaDir):
        os.makedirs(noticiaDir)
    if not os.path.exists(noticiaDirEP):
        os.makedirs(noticiaDirEP)    

    #salvar los archivos
    catFile = noticiaDir + noticiaNombre
    with open(catFile, 'w') as writeFile:
        writeFile.write(noticiaTexto)
    writeFile.close()
    print("Creado archivo: " + catFile)
    
    catFile = noticiaDirEP + noticiaNombre
    with open(catFile, 'w') as writeFile:
        writeFile.write(noticiaTexto)
    writeFile.close()
    print("Creado archivo: " + catFile)