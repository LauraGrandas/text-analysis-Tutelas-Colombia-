# -*- coding: utf-8 -*-
"""
Created on Wed May 26 18:27:37 2021

@author: Laura Grandas
"""

import os
import PyPDF2
import slate3k as slate
import pandas as pd
import numpy as np
import string

# para las stopwords
import nltk
from nltk.corpus import stopwords
spanish_stopwords = stopwords.words('spanish') # estoy hay que descargarlo la primera vez
from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer('spanish')



#MATRIX TÉRMINO-DOCUMENTO
from sklearn.feature_extraction.text import CountVectorizer # Vectorizador de palabras y DTM
spanish_stopwords = stopwords.words('spanish')
from sklearn.decomposition import LatentDirichletAllocation # Modelo de LDA


# LDA esta vaina no está corriendo en python 3.9 
import pyLDAvis 
from pyLDAvis import sklearn as sklearnlda #EXPORTAR EL MODELO (VISUALIZACIÓN)


#%%



path = r'C:\Users\laura\Dropbox\UNIANDES\tesis_derecho'
path_txt = r'C:\Users\laura\Dropbox\UNIANDES\tesis_derecho\textos\10_Tutelas 2019-2 a 2021-1 - copy'

os.chdir(path_txt)

files_name = os.listdir(path_txt)



#%% SCRAPE DE UN SOLO ARCHIVO DE PDF CON PyPDF2

archivo_bien = '34_AT_2019_606.pdf'
archivo_paila = '16_AT_2019_672dup.pdf'
archivo_paila2 = '170_AT_2020-0083.pdf'


file = open(archivo_paila, 'rb')
reader = PyPDF2.PdfFileReader(file, strict=False)
page1 = reader.getPage(0)
print('no. pgs :', reader.numPages)
pdfData = page1.extractText()
print(pdfData)



#%% SCRAPE DE TODOS LOS ARCHIVOS CON PyPDF2

# para que me guarde cada tutela como un string muy largo voy a necesitar esto
# Es una función para que las listas de listas se vuelvan una sola lista de strings
def aplanar(elemento):
    string=[]
    for i in elemento:
        if type(i)==str:
            string.append(i)
        else:
            #Para este punto i no es un string
            for elementoDeI in i :#Aca va a separar en conjuntos
                for elementito in aplanar(elementoDeI):    
                    string.append(elementito)
    return string

# para leer todos los archivos en la carpeta

files_name = os.listdir(path_txt)
outputs = []
file_texto = []


    
for j in files_name:
     try:
     
         if j != '16_AT_2019_672dup.pdf':
             print(j)
             pdfReader = PyPDF2.PdfFileReader(j)
             count = pdfReader.numPages
             output = []
            
             # para leer todas las paginas de cada archivo
             for i in range(count):
                 page = pdfReader.getPage(i)
                 output.append(page.extractText())
                 output = aplanar(output)
                 # lista_enmodo_string = ' '.join(map(str, output))
                 # output = lista_enmodo_string
             outputs.append(output)
                
             juntos = [str(j), output]
             file_texto.append(juntos)                                          
     except:
         pass
            # outputs.append('nada')
            # juntos = (str(j),'nada')
            # file_texto.append(juntos)
         
lista_enmodo_string = ' '.join(map(str, output))


#%% sobre la lista de outputs1

outputs_planos = []

for i in range(len(outputs)):
    output_plano = aplanar(outputs[i])
    outputs_planos.append(output_plano)


#%% SCRAPE DE UN SOLO ARCHIVO DE PDF CON SLATE3K


with open(archivo_bien,'rb') as f:
    extracted_text = slate.PDF(f)
    bup = str(extracted_text)
    
print(extracted_text)


#%% SCRAPE DE TODOS LOS ARCHIVOS CON SLATE3K
outputs2 = []
file_texto2 = []
buenos2 = []

counter = 1


for j in files_name:
    
    print('VAMOS EN EL ARCHIVO ', counter)
    try:
        with open(j,'rb') as f:
            print(j, ' que es el número ', counter)
            output2 = slate.PDF(f)
            outputs2.append(str(output2))
            juntos2 = [str(j),str(output2)]
            file_texto2.append(juntos2)
            
            buenos2.append(juntos2)
    except:
        outputs2.append('nada')
        juntos2 = (str(j),'nada')
        file_texto.append(juntos2)
    
    counter=counter+1



#%% VOLVER OUTPUTS Y FILES 1 (LOS DE PYPDF2) COSAS QUE PUEDA TOKENIZAR
longitudes = []
num_strings = []

for i in range(len(outputs)):
    longitud = len(outputs[i])
    longitudes.append(longitud)
    print('TENGO ', longitud, 'ELEMENTOS EN LA LISTA')
    print('-----------------------')
    
    for j in range(len(outputs[i])):
        cuenta = len(outputs[i][j])
        num_strings.append(cuenta)
        print('TENGO ', cuenta, 'PALABRAS')
        
        

    # for j in range(len(outputs[i])):
    #     letras = ''.join(map(str, outputs[j][i]))


#%% limpiando y tokenizando outputs2

ejemplo = outputs2[12]


sobran = [r"\n", '.', ',',':', '-', '(', ')', '[', ']', '"', 'cid9', '—', ';',
          '•', '*', "'", r"\xc", 'cid', '\x0c', 'negrete', ' canscanner ', 
          ' cc ', ' fecha ', ' señor', ' radicado ', 'derecho', ' fundamental ', 
          'fundamentales', 'solicitud', ' caso ', 
          ' ley ', ' auto ', ' ón', 'abril', 'mayo', 'agencia', 'nacional', ' corte ',
          'tutela', 'sentencia', 'scanned', '$','xc', 'iván', 'miguel', ' cc ',
          ' ia ', ' to ', ' id ', ' ad ', ' an ', ' ci ', ' ro ', ' ca ', 'ani',
          'tribunal', 'https', ' io ', ' io ', 'constitucional', ' ae ', ' ii '
          ' cia ', ' ce ', ' ea ', ' ie ', 'camscanner', ' by ', 'deech', ' aa '
          ' mp ', ' ser ', ' do '
          ]
# ahora lo que veo que sobra en los lda

numeros = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
sobran.append(numeros)
sobran = aplanar(sobran)



def caracteres(objeto):
    for i in range(len(sobran)):
        objeto = objeto.replace(sobran[i], '')
    return objeto
    

outputs2_clean = []
for j in range(len(outputs2)):
    minusculas = outputs2[j].lower()
    limpios = caracteres(minusculas)
    outputs2_clean.append(limpios)
    
    
print('LIMPIO', outputs2_clean[22][2000:4000])

#%%


example = 'xc yadayada esto no me . Nunca JAMAS agencia negrete sirve xc xc'
# print(caracteres(example))

print(caracteres(example).lower())



#%% aplanando outputs1
# outputs_limpios = []

# for i in range(len(output)):
#     output_limpio = output[i].replace(r'\n', '')
#     outputs_limpios.append(output_limpio)
    
#%% tokenizing
# ejemplo = outputs2[12]

# spanish_stopwords.append('xc')


ejemplo = outputs2_clean


n_vocab=5000 # máximo tamaño de vocabulario
tf_vectorizer = CountVectorizer( max_features=n_vocab, stop_words=spanish_stopwords, ngram_range=(1,4))

# ejemplo = [ejemplo]

tf = tf_vectorizer.fit_transform(ejemplo)
print(tf)

path_html = r'C:\Users\laura\Dropbox\UNIANDES\tesis_derecho\lda_limpio'
os.chdir(path_html)



for i in range(4,31):
    lda = LatentDirichletAllocation(n_components=i, max_iter=11,doc_topic_prior=0.1, topic_word_prior=0.1, n_jobs=-1,random_state=353, verbose=1) #CONSTRUYO EL MODELO
    lda.fit(tf) # Esti
    LDAvis_prepared=sklearnlda.prepare(lda, tf, tf_vectorizer ) # Preparo el modelo y sus resultados para la visualización
    pyLDAvis.save_html(LDAvis_prepared, f'LDA_{i}.html')
    
    

#%% PREPARANDO DATAFRAMES LIMPIOS PARA LLEGAR A LAS MATRICES

df = pd.DataFrame(file_texto, columns= ['name_file', 'texto'])
df2 = pd.DataFrame(file_texto2, columns= ['name_file', 'texto'])

lista_enmodo_string = ' '.join(map(str, output))

df["strings"] =  ' '.join(map(str, df.texto))



#%%


df.texto=df.texto.str.lower()  #mayúsculas
df.texto=df.texto.str.replace('[,\.!?\-!?\n\)\(\r]', ' ') # Borro Puntuaciones
df.texto=df.texto.str.replace('[0-9]', ' ') # Quito números
df.texto=df.texto.str.replace(' +', ' ') # Quito espacios innecesarios


#%%

df.tweet=df.tweet.str.lower()  #mayusulas
df.tweet=df.tweet.str.replace('[,\.!?\-!?\n\)\(\r]', ' ') # Borro Puntuaciones
df.tweet=df.tweet.str.replace('[0-9]', ' ') # Quito números


#%% función de calidad por caracteres
def calidad(doc):
    aciertos=0
    contador=0
    for j in doc:
        for i in j:
            contador+=1
            if (i in string.ascii_letters):
                aciertos+=1
    return aciertos/contador



#%% 
path_destino = r'C:\Users\laura\Dropbox\UNIANDES\tesis_derecho\textos\destino'
os.chdir(path_destino)

df.to_csv('df1.csv')
df2.to_csv('df2.csv')
