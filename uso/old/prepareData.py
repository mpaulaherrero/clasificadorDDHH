import nltk
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer  
#load PMML model
#import subprocess
from openscoring import Openscoring
#import numpy as np

#from sklearn.naive_bayes import GaussianNB
#from sklearn2pmml import sklearn2pmml
#from sklearn2pmml.pipeline import PMMLPipeline

row = {'idPeriodico': '273239', 'periodico': 'EN', 'url': 'http://www.el-nacional.com/noticias/sociedad/detuvieron-pemon-cuando-trasladaba-ayuda-humanitaria_273239', 'fecha': '03/03/2019', 'fechaPublicacion': '2019-03-62T12:35:00-0400', 'autor': 'EL NACIONAL', 'seccion': 'Sociedad', 'palabrasClaves': 'NO_TIENE', 'titular': 'Detuvieron a un pemón cuando trasladaba ayuda humanitaria', 'subtitular': 'El abogado Gonzalo Himiob informó que\xa0Rufino Martín Pérez Martínez llevaba los insumos para los indígeneas de Santa Elena de Uairén', 'imagen': 'http://en-cdnmed.agilecontent.com//resources/jpg/2/1/1551629934412.jpg', 'contenido': ['Gonzalo Himiob, abogado y director de la ONG\xa0Foro Penal, informó que un indígena pemón fue detenido durante la madrugada de este domingo cuando trasladaba ayuda humanitaria.', 'Himiob indicó que Rufino Martín Pérez Martínez, coordinador de Cultura de San Francisco de Yuruaní, se disponía a trasladar los insumos desde Santa Elena de Uairén para indígenas de la zona.', 'El lunes 25 de febrero,\xa0Alfredo Romero reveló que nueve indígenas de la etnia pemón están desaparecidos. Agregó que un indígena\xa0está detenido en Santa Elena de Uairén.'], 'derecho': ''}

#pasar texto a minusculas
text = (row["titular"] + " " + row["subtitular"] + " " + ''.join(row["contenido"])).lower()
#print(text)
#print("")
#separación del texto en tokens 
words = TextBlob(text).words
#print(words)
#print("")
#Eliminación de palabras no informativas (stop words) y signos de puntuación
stopwords = stopwords.words('spanish')
#print(stopwords)
words = [x for x in words if x not in stopwords]
#print(words)
#print("")
#Lematización aplicando el algoritmo Porter Stemmer
stemmer = SnowballStemmer('spanish')
words = [stemmer.stem(i) for i in words]
print(words)
#wordsLem = [Word(i).lemmatize() for i in words]
#print(wordsLem)

#crear el vector de la noticia a predecir
tfidf = TfidfVectorizer(use_idf = True)
train_vect = tfidf.fit_transform(words).toarray() 
#print(train_vect)

#buscar modelo en PMML
#p = subprocess.Popen('java -jar openscoring-server-executable-1.4.3.jar', shell=True)
os = Openscoring("http://localhost:8080/openscoring")

# Deploying a PMML document as a model:   
# A dictionary of user-specified parameters
kwargs = {"auth" : ("admin", "adminadmin")}
os.deployFile("clasificadorDDHH", "clasificadorDDHH.pmml", **kwargs)

# Evaluating the model with a data record
result = os.evaluate("clasificadorDDHH", train_vect)
print(result)

#assigning predictor and target variables
#x = np.array([[-3,7],[1,5], [1,2], [-2,0], [2,3], [-4,0], [-1,1], [1,1], [-2,2], [2,7], [-4,1], [-2,7]])
#y = np.array([3, 3, 3, 3, 4, 3, 3, 4, 3, 4, 4, 4])
#Create a Gaussian Classifier
#model = GaussianNB()
# Train the model using the training sets 
#model = model.fit(x, y)  

#Predict Output 
#predicted= model.predict([[1,2],[3,4]])
#print predicted

# Prepare data
#iris = load_iris()
#X = pd.DataFrame(iris.data)
#X.columns = np.array(iris.feature_names)
#y = pd.Series(np.array(iris.target_names)[iris.target])
#y.name = "Class"
#Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.33, random_state=123)

#no esto es para salvar no para traer
#pipeline = PMMLPipeline([
#	("classifier", GaussianNB())
#])
#sklearn2pmml(pipeline, "clasificadorDDHHModelPMML.pmml", with_repr = True)


