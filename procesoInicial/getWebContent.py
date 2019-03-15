import csv
import json
import time
import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

csvFile = "/Users/mariapaulaherrero/Documents/documentosPersonal/My Documents/ucv/maestria/MD/MDproyecto/dataPDF/data.csv"
jsonFile = "/Users/mariapaulaherrero/Documents/documentosPersonal/My Documents/ucv/maestria/MD/MDproyecto/dataPDF/data.json"
csvFileTexto = "/Users/mariapaulaherrero/Documents/documentosPersonal/My Documents/ucv/maestria/MD/MDproyecto/dataPDF/dataTexto.csv"

row = {"id": 0, "idPeriodico": 0, "periodico":"", "url":"", "fecha":"", "fechaPublicacion":"", "autor":"", "seccion":"", "palabrasClaves":"", "titular" : "", "subtitular" : "", "imagen":"", "contenido":"", "derecho":"", "otrosDerechos":"", "subDerechos":"", "EP":""}
rows = []

def cleanLine(lineText):
    lineText = lineText.replace('\n',' ').replace('\r',' ').replace(';',',').replace(u"\u037E",',').replace(u"\xa0",' ').replace(u"\u25A0",' ').replace("xa0",' ').replace("'",'"')
    #print(lineText)
    return lineText

with open(csvFile, 'r') as readFile:
    reader = csv.reader(readFile, delimiter=';')
    lines = list(reader)
readFile.close()
del lines[0]

count = 0
for line in lines:
    #["No.", "Nombre archivo", "Fecha", "Titular", "Periodico", "Fecha Periodico", "URL", "Derecho PPal", "Otros Derechos", "SubDerechos", "CONTEXTO"]
    url = line[6]
    periodico = line[4]
    
    print(str(count) + ") procesando: " , url)
    try:
        html = urlopen(url)
        soup = BeautifulSoup(html, 'lxml')
        #title = soup.title
        #print(title)
        #text = soup.text
        #print(text)
        newRow = row.copy()
        newRow["id"] = line[0]
        newRow["periodico"] = periodico
        newRow["url"] = url
        #newRow["fecha"] = line[5]
        newRow["derecho"] = line[7]
        newRow["otrosDerechos"] = line[8]
        newRow["subDerechos"] = line[9]
        newRow["EP"] = line[10]
        if periodico == "EN":
            #busco el id del periodico
            partesUrl = url.split('_')
            newRow["idPeriodico"] = partesUrl[1]
            #busco autor, palabras claves y seccion
            #<meta name="author" content="Adriana Fernández | @adrianakfv | afernandez@el-nacional.com" />
            try:
                autor = soup.find('meta', attrs={'name': 'author'})['content']
            except:
                autor = "NO_TIENE"
            #<meta property="article:section" content="Economía" />
            seccion = soup.find('meta', attrs={'property': 'article:section'})['content']
            #<meta property="article:tag" content="Economía, Escasez, Inflación, Sociedad" />
            try:
                palabrasClaves = soup.find('meta', attrs={'property': 'article:tag'})['content']
            except:
                palabrasClaves = "NO_TIENE"
            #busco el titulo y el subtitulo
            #<header class="detail-header">
            #  <h1 class="title">Lo que se ignoró al regular el precio de la carne</h1>
            #  <div class="subtitle"><P>Un productor agropecuario del estado ...</P></div>
            #</header>
            header = soup.find('header', attrs={'class': 'detail-header'})
            title = header.find('h1', attrs={'class': 'title'}).text
            subtitle = header.find('div', attrs={'class': 'subtitle'}).text
            #busco el contenido y fecha de publicacion
            #<div class="detail-body">
            #	<meta itemprop="datePublished" content="2018-10-277T01:15:00-0400" />
            #	<p style="text-align: justify;">..</p>
            # ...
            #	<p style="text-align: justify;">..</p>
            #</div>
            lines = soup.find('div', attrs={'class': 'detail-body'}).find_all('p', recursive=False)
            #print(lines)
            #<meta itemprop="datePublished" content="2018-10-277T01:15:00-0400" />
            fechaPub = soup.find('div', attrs={'class': 'detail-body'}).find('meta', attrs={'itemprop': 'datePublished'})['content']
            #busco la imagen
            #<figure data-component="image" class="thumb photo">
            #   <span class="r16-9">
            #       <picture class="objFitContent">
            #           <source data-srcset="http://en-cdnmed.agilecontent.com//resources/jpg/3/2/1538664560323.jpg" media="(min-width: 1024px)"><!-- void --></source> 
            #       </picture>
            #   </span>
            #</figure>
            figure = soup.find('figure', attrs={'class': 'photo'}).find_all('source')
            #guardo lo encontrado en un json
            newRow["fechaPublicacion"] = fechaPub
            newRow["fecha"] = datetime.datetime.strptime(fechaPub, '%Y-%m-%jT%H:%M:%S%z').strftime("%d/%m/%Y")
            newRow["autor"] = autor
            newRow["seccion"] = seccion
            newRow["palabrasClaves"] = palabrasClaves
            #print("Title:", title)
            newRow["titular"] = title
            #print("Subtitle:", subtitle)
            newRow["subtitular"] = subtitle
            #print("imagen:", figure[-1]['data-srcset'])
            newRow["imagen"] = figure[-1]['data-srcset']
            #print("content:")
            content = []
            for line in lines:
                lineText = line.text.replace("Leer más aquí ","").strip()
                if lineText:
                    lineText = cleanLine(lineText)
                    content.append(lineText)   
            #newRow["contenido"] = "\n".join(content)      
            newRow["contenido"] = content      
        elif periodico == "EU":
            #<span id="autor">CRISBEL VARELA</span>
            autor = soup.find('span', attrs={'id': 'autor'}).text.strip()
            title = soup.find('a', attrs={'id': 'titulo'}).text.strip()
            subtitle = soup.find('p', attrs={'id': 'sumario'}).text.strip()
            partesUrl = url.split('/')
            #print(partesUrl)
            #<meta property="article:published_time" content="20/11/2018 01:53 pm" />
            fechaPub = soup.find('meta', attrs={'property': 'article:published_time'})['content']
            imagen = soup.find('figure', attrs={'class': 'thumb img-bg'}).find('img')['src']
            #buscar el contenido, EU no tiene un formato especifico
            #Puede tener el primer parrafo directo en el div con la ciudad en bold
            #puede estar todo en dentro de div, incluso los twitter que hay que sacarlos
            #puede estar entre p
            content = []
            textsB = ""
            try:
                textsB = soup.find('div', attrs={'id': 'cuerpo'}).find('b', recursive=False).text
            except:
                textsB = ""
            texts = soup.find('div', attrs={'id': 'cuerpo'}).find_all(text=True, recursive=False)
            #print(texts)
            firstLine = True
            for line in texts:
                lineText = line.strip()
                if lineText:
                    if firstLine and textsB:
                        lineText = textsB + lineText
                        firstLine = False
                    lineText = cleanLine(lineText)
                    content.append(lineText)
            lines = soup.find('div', attrs={'id': 'cuerpo'}).find_all('div', recursive=False)
            #print(lines)
            for line in lines:
                #print(line)
                twitter = line.find('blockquote', attrs={'class': 'twitter-tweet'})
                #print("tiene twitter:", twitter)
                if not twitter:
                    lineText = line.text.strip()
                    if lineText:
                        lineText = cleanLine(lineText)
                        content.append(lineText)
                else:
                    #veo si hay otros div dentro de esta linea con contenido
                    lines2 = line.find_all('div', recursive=False)
                    for line2 in lines2:
                        twitter2 = line2.find('blockquote', attrs={'class': 'twitter-tweet'})
                        if not twitter2:
                            lineText2 = line2.text.strip()
                            if lineText2:
                                lineText2 = cleanLine(lineText2)
                                content.append(lineText2)
            lines = soup.find('div', attrs={'id': 'cuerpo'}).find_all('p', recursive=False) 
            for line in lines:           
                lineText = line.text.strip()
                if lineText:
                    lineText = cleanLine(lineText)
                    content.append(lineText)
            newRow["idPeriodico"] = partesUrl[4]        
            newRow["fechaPublicacion"] = fechaPub
            newRow["fecha"] = datetime.datetime.strptime(fechaPub, '%d/%m/%Y %I:%M %p').strftime("%d/%m/%Y")
            newRow["autor"] = autor
            newRow["seccion"] = partesUrl[3]
            newRow["palabrasClaves"] = "NO_TIENE"
            newRow["titular"] = title
            newRow["subtitular"] = subtitle
            newRow["imagen"] = imagen
            if content:
                newRow["contenido"] = content
            else:
                print("revisar noticia sin cuerpo")    
                newRow["contenido"] = content
    except:
        print("error conectando") 
    newRow["contenido"] = "|".join(newRow["contenido"])
    rows.append(newRow)
    #print("listo: " , url)
    count += 1
    #if count>20:
     #   break
    time.sleep(3)

#print(rows)
with open(jsonFile, 'w') as writeFile:
    json.dump(rows, writeFile, indent=4, sort_keys=False)
writeFile.close()
print("Creado archivo: " + jsonFile)

#hago archivo csv
#row = {"id": 0, "periodico":"", "url":"", "fecha":"", "fechaPublicacion":"", "autor":"", "seccion":"", "palabrasClaves":"", "titular" : "", "subtitular" : "", "imagen":"", "contenido":"", "derecho":"", "otrosDerechos":"", "subDerechos":"", "EP":""}
cabeceraCSV = ["id", "idPeriodico", "periodico", "url", "fecha", "fechaPublicacion", "autor", "seccion", "palabrasClaves", "titular", "subtitular", "imagen", "contenido", "derecho", "otrosDerechos", "subDerechos", "EP"]
csvLines = []
csvLines.append(cabeceraCSV)
for row in rows:
    data = []
    data.append(row["id"])
    data.append(row["idPeriodico"])
    data.append(row["periodico"])
    data.append(row["url"])
    data.append(row["fecha"])
    data.append(row["fechaPublicacion"])
    data.append(row["autor"])
    data.append(row["seccion"])
    data.append(row["palabrasClaves"])
    data.append(row["titular"])
    data.append(row["subtitular"])
    data.append(row["imagen"])
    data.append(" ".join(row["contenido"]))
    data.append(row["derecho"])
    data.append(row["otrosDerechos"])
    data.append(row["subDerechos"])
    data.append(row["EP"])
    csvLines.append(data)
#print(csvLines)

with open(csvFileTexto, 'w') as writeFile:
    writer = csv.writer(writeFile, delimiter=';')
    writer.writerows(csvLines)
writeFile.close()
print("Creado archivo: " + csvFileTexto)