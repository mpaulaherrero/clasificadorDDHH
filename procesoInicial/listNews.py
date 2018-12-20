import os
import csv
from tika import parser

dir = "/Users/mariapaulaherrero/Desktop/MDproyecto/dataPDF/toda"
csvFile = "/Users/mariapaulaherrero/Desktop/MDproyecto/dataPDF/data.csv"

#periodicos = ["EN", "EU", "UN", "LR", "RE", "ENP", "QD", "EM", "Question", "LRE", "TAL", "2001", "AJ", "OP", "Vea"]
periodicos = ["EN", "EU"]
periodicosNombre = ["El Nacional","El Universal"]
periodicosURL = ["http://www.el-nacional.com", "http://www.eluniversal.com"]
clasificacion = ["1.10", "1.1", "1.2", "1.3", "1.4", "1.7", "2.10", "2.1", "2.2", "2.3", "2.6", "2.8", "2.9", "3.1", "3.2", "4.3", "5", "11.9", "12", "15", "17", "18","19","20", "CONTEXTO"]
clasificacionDesc = ["Derecho a la justicia", "Derecho a la vida", "Derecho a la libertad personal", "Derecho a la Integridad personal", "Derecho a la seguridad ciudadana", "Derecho a la libertad de expresión e información", "Derecho a la alimentación", "Derecho a la Salud", "Derecho a la Educación", "Derecho al trabajo", "Derecho a la seguridad social", "Derecho a la Vivienda", "Derecho de los Pueblos Indios", "Derecho a la tierra", "Derecho al ambiente", "Derecho a manifestar pacíficamente", "Actividades de las ONG nacionales e internacionales de ddhh en Venezuela", "Partiticpación", "Manifestaciones Violentas", "Provea en prensa", "Zona Fronteriza", "Instancias internacionales de ddhh", "Leyes", "Estados de excepción", "CONTEXTO"]

cabeceraCSV = ["No.", "Nombre archivo", "Fecha", "Titular", "Periodico", "Fecha Periodico", "URL", "Derecho PPal", "Otros Derechos", "SubDerechos", "EP"]
row = {"No.": 0, "Nombre archivo": "", "Fecha": "", "Titular" : "", "Periodico":"", "Fecha Periodico":"", "URL":"", "PeriodicoURL":"", "Derechos":[], "SubDerechos":[], "CONTEXTO":""}
rows = []

csvLines = []
csvLines.append(cabeceraCSV)

os.chdir(dir)
ruta_app = os.getcwd()
contenido = os.listdir(ruta_app)
contenido = os.scandir(ruta_app)

archivos = 0
linea = '-' * 40

for elemento in contenido:
    if  elemento.is_file() and elemento.name != ".DS_Store":
        newRow = row.copy()
        newRow["Derechos"] = []
        newRow["SubDerechos"] = []
        newRow["EP"] = "NO"
        archivos +=1
        #print(str(archivos) + ')')
        newRow["No."] = str(archivos)
        #print('Nombre archivo:', elemento.name)
        newRow["Nombre archivo"] = elemento.name
        datos = elemento.name.replace("(1).pdf","").replace(".pdf","").split(" ")
        #revisar datos sacados del nombre del archivo
        for dato in datos:
            if dato:
                if dato in periodicos:
                    #print("Periodico:", dato)
                    newRow["Periodico"] = dato
                elif "(" in dato:
                    aux = dato.replace("(","").replace(")","")
                    #print("Fecha:", aux)
                    newRow["Fecha"] = aux
                elif "EP" in dato:
                    #print("EP: si")    
                    newRow["EP"] = "SI"
                else:
                    clas = dato.rstrip('.')    
                    if clas in clasificacion:
                        #print("Clasificacion:", clas)
                        newRow["Derechos"].append(clas)
                    else:
                        encontro = False
                        for aux in clasificacion:
                            if clas.startswith(aux + "."):
                                #print("Clasificacion:", aux)
                                newRow["Derechos"].append(aux)
                                #print("Subclasificacion:", clas)
                                newRow["SubDerechos"].append(clas)
                                encontro = True
                                break
                        #if not encontro:
                        #    print(clas)    
                    
        try:
            parsedPDF = parser.from_file(elemento.path)
            #print("Procesando: ", elemento.path)
            tokens = parsedPDF["content"].split("\n")
            for token in tokens:
                if token:
                    if not "http" in token:
                        datos = token.split(" ")
                        #print("Fecha periodico:",datos[0])
                        newRow["Fecha Periodico"] = datos[0]
                        del datos[0]
                        tit = " ".join(datos)
                        #print("Titular:",tit)
                        newRow["Titular"] = tit
                if "http" in token:
                    urlD = token.split(" ")
                    #print("URL: ", urlD[0])
                    newRow["URL"] = urlD[0]
                    if newRow["URL"].startswith(periodicosURL[0]):
                        newRow["PeriodicoURL"] = periodicos[0]
                    elif newRow["URL"].startswith(periodicosURL[1]):
                        newRow["PeriodicoURL"] = periodicos[1]
                    break
        except UnicodeEncodeError as e:
            if elemento.name == "EN   (10.10.2018)   EP   2.3.4.   2.8.1.  Protestan en Táchira contra el gobierno de Nicolás Maduro.pdf":
                newRow["Fecha Periodico"] = "10/10/2018"
                newRow["Titular"] = "Protestan en Táchira contra el gobierno de Nicolás Maduro"
                newRow["URL"] = "http://www.el-nacional.com/noticias/protestas/protestaron-tachira-contra-gobierno-nicolas-maduro_255204"
                newRow["PeriodicoURL"] = "EN"
            else:
                print("Error de encoding:", elemento.path)
                
        rows.append(newRow)
        #print(linea)

#print(rows)
for row in rows:
    data = []
    #["No.", "Nombre archivo", "Fecha", "Titular", "Periodico", "Fecha Periodico", "URL", "Derecho PPal", "Otros Derechos", "SubDerechos", "CONTEXTO"]
    data.append(row["No."])
    data.append(row["Nombre archivo"])
    data.append(row["Fecha"])
    data.append(row["Titular"])
    data.append(row["PeriodicoURL"])
    data.append(row["Fecha Periodico"])
    data.append(row["URL"])
    data.append(row["Derechos"][0])
    del row["Derechos"][0]
    data.append(", ".join(row["Derechos"]))
    data.append(", ".join(row["SubDerechos"]))
    data.append(row["EP"])
    csvLines.append(data)
#print(csvLines)

with open(csvFile, 'w') as writeFile:
    writer = csv.writer(writeFile, delimiter=';')
    writer.writerows(csvLines)
writeFile.close()
print("Creado archivo: " + csvFile)
