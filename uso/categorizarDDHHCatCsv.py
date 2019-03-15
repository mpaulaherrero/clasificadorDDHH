import pandas
import csv
from datetime import datetime

pathRoot = "/Users/mariapaulaherrero/Documents/documentosPersonal/My Documents/ucv/maestria/MD/MDproyecto/codigo/uso/data/"

def rm_main(category, rows):
    #print(category)
    #print(rows)
    #print(type(rows))
    for index, row in rows.iterrows() :
        #print(category.loc[index, 'prediction(derecho)'],row['titular']) 
        row['derecho'] = category.loc[index, 'prediction(derecho)']
        print(row['derecho'],row['titular']) 
        #print(row['contenido']) 
        rows.loc[index,'derecho'] = category.loc[index, 'prediction(derecho)']
    date_time = datetime.now().strftime("%Y%m%d%H%M")    
    fileName = pathRoot + date_time + "Data"
    rows.to_csv(fileName + ".csv", sep=';', encoding='utf-8', doublequote=False,  escapechar="\\")
    #rows.to_json(fileName + ".json", orient='records')
    return rows
    
