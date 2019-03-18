import pandas
import time
import datetime
import urllib.request
from urllib.request import urlopen
from bs4 import BeautifulSoup

periodicos = [{"id": "EN","url": "http://www.el-nacional.com/ultimo-minuto", "lastId":0}, {"id": "EU","url": "http://www.eluniversal.com/buscador", "lastId":0}]
row = {"idPeriodico": 0, "periodico":"", "url":"", "fecha":"", "fechaPublicacion":"", "autor":"", "seccion":"", "palabrasClaves":"", "titular" : "", "subtitular" : "", "imagen":"", "contenido":"", "derecho":""}
categoriesExcluded = ["Entretenimiento", "Arte", "EE UU", "Politica", "entretenimiento", "internacional", "el-universal", "politica", "Fútbol", "Beisbol", "doblevia", "deportes", "Deportes", "Cine", "BBC Mundo", "Música", "Ciencia y Tecnología", "estilo-de-vida", "Europa", "España, Mundo", "Motores"]

def cleanLine(lineText):
    lineText = lineText.replace('\n',' ').replace('\r',' ').replace(';',',').replace(u"\u037E",',').replace(u"\xa0",' ').replace(u"\u25A0",' ').replace("xa0",' ').replace("'",'"')
    #print(lineText)
    return lineText

def getEUContent(url):
    newRow = row.copy()
    try:
        newRow["periodico"] = "EU"
        newRow["url"] = url    
        html = urlopen(url)
        soup = BeautifulSoup(html, 'lxml')
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
            noticiaID = newRow["periodico"] + "_" + newRow["idPeriodico"]
            print(noticiaID + ": revisar noticia sin cuerpo")    
            newRow["contenido"] = content
    except:
        print("ERROR conectando") 
        newRow = None
    return newRow  
        
def getENContent(url):
    newRow = row.copy()
    try:
        newRow["periodico"] = "EN"
        newRow["url"] = url
        html = urlopen(url)
        soup = BeautifulSoup(html, 'lxml')
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
        try:
            subtitle = header.find('div', attrs={'class': 'subtitle'}).text
        except:
            subtitle = ""
        #busco el contenido y fecha de publicacion
        #<div class="detail-body">
        #	<meta itemprop="datePublished" content="2018-10-277T01:15:00-0400" />
        #	<p style="text-align: justify;">..</p>
        # ...
        #	<p style="text-align: justify;">..</p>
        #</div>
        lines = soup.find('div', attrs={'class': 'detail-body'}).find_all('p', recursive=False)
        if not lines:
            lines = soup.find('div', attrs={'class': 'detail-body'}).find_all('p', recursive=True)
            #print(lines)
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
        try:
            newRow["imagen"] = figure[-1]['data-srcset']
        except:
            newRow["imagen"] = ""    
        #print("content:")
        content = []
        for line in lines:
            lineText = line.text.replace("Leer más aquí ","").strip()
            if lineText:
                lineText = cleanLine(lineText)
                content.append(lineText)   
        #newRow["contenido"] = "\n".join(content)      
        newRow["contenido"] = content
    except Exception as e:
        print("ERROR conectando") 
        print(str(e))
        newRow = None
    return newRow

def get_urls():
    urls = []
    rows = []
    #busco los nuevos URL para revisar
    for periodico in periodicos:
        try:
            print("REVISANDO: " + periodico["url"])
            html = urlopen(periodico["url"])
            soup = BeautifulSoup(html, 'lxml')
            tmp = ""
            links = []
            if periodico["id"]=="EN":
                links = soup.find('div', attrs={'class': 'list'}).find_all('a', recursive=True)
            elif (periodico["id"]=="EU"):
                links = soup.find('ul', attrs={'id': 'notas_result'}).find_all('a', recursive=True)
            for link in links:
                href = link.get('href')
                print('.', end='')
                if href != "javascript://;" and href != tmp and href != "#":
                    #print(href)
                    tmp=href
                    urls.append({"idPeriodico": periodico["id"], "href": href})
            print("Listo")        
        except Exception as e:
            print("ERROR conectando url " + periodico["url"])
            print(str(e))
    #de los nuevos urls busco su contenido
    for url in urls:
        print("BAJANDO: " + url["href"])
        newRow = ""
        if url["idPeriodico"] == "EN":
            newRow = getENContent(url["href"])
        elif url["idPeriodico"] == "EU":
            newRow = getEUContent(url["href"])
        #print ("URL: " + url["href"] + ", Periodico: " + newRow["periodico"] + ", Noticia: " + newRow["titular"])
        if newRow != None and newRow["seccion"] not in categoriesExcluded:
            newRow["contenido"] = "|".join(newRow["contenido"])
            rows.append(newRow)
    return rows        

#busco noticias a procesar
def rm_main():
    rows = get_urls()
    return pandas.DataFrame(rows)

#rm_main()
    