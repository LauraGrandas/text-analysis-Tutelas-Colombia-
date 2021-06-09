# -*- coding: utf-8 -*-
"""
Created on Thu May 20 12:08:06 2021

@author: laura
"""

import pandas as pd
import os
import numpy as np


path = r'C:\Users\laura\Dropbox\UNIANDES\tesis_derecho'
os.chdir(path)
#%%

df = pd.read_excel('Relación acciones de tutela 2019-al 2021-1.xlsx' )
df = df.drop(df.columns[19:], axis=1)

df.columns = df.iloc[0]
df = df.rename(columns={df.columns[0]:'indice', df.columns[1]:'abogada', df.columns[3]:'derecho_fundamental', df.columns[8]:'fecha'})
df = df.iloc[1:,:]

# un truquito para que me lea bioen esas fechas que estaban sucias 
df.to_excel('resumen_headersordenados.xlsx')
df = pd.read_excel('resumen_headersordenados.xlsx', parse_dates=['fecha'])

df1 =df



#%% LIMPIANDO STRINGS: 
    
# LE QUITO TILDES

# SI QUISIERA HACER ENCODING DE TODAS LAS VARIABLES:
# df2 = df.drop(df.columns[16:], axis=1)

# print(df2.columns)
# cols = df.select_dtypes(include=[np.object]).columns
# df[cols] = df[cols].apply(lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))

# PERO COMO SOLO ME IMPORTA derecho_fundamental entonces solo hago encoding de esta
df['derecho_fundamental'] = df['derecho_fundamental'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')


# LE QUITO Y y E PARA VOLVER TODO COMAS Y PODER USAR SPLIT
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace('Y',',')
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace(' E ',' , ')
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace('-',',')
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace(' ,',',')
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace(', ',',')
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace(', ',',')
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace('  ',' ')


# LE QUITO "DERECHO FUNDAMENTAL"
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace('DERECHO','')
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace('FUNDAMENTAL','')

# PREPOSICIONES
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace('A LA','')
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace(' AL ','')
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace('AL T','T')
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace('AL M','M')
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace('A VI','VI')
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace('A SER','SER')


df['derecho_fundamental'] = df['derecho_fundamental'].str.replace('A UNA','')
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace('A UN','')


# ESPACIOS
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace('DE PETICION','PETICION')
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace('PETICION ','PETICION')
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace(' PETICION','PETICION')

df['derecho_fundamental'] = df['derecho_fundamental'].str.replace('PROCESO ','PROCESO')
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace('PROCESO ','PROCESO')

df['derecho_fundamental'] = df['derecho_fundamental'].str.replace('DIGNA ','DIGNA')
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace('IGUALDAD ','IGUALDAD')
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace('MINIMO VITAL ','MINIMO VITAL')


# TYPOS
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace('PRPCESO','PROCESO')
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace('S PETICION','PETICION')
df['derecho_fundamental'] = df['derecho_fundamental'].str.replace('ESTABILIDAD LABORMINIMO VITALSALUD,VIDA DIGNA','ESTABILIDAD LABORAL,MINIMO VITAL,SALUD,VIDA DIGNA')

# PARA QUITAR ESPACIOS AL COMIENZO Y FINAL DEL STRING
df['derecho_fundamental'] = df['derecho_fundamental'].str.strip()

# UN GROUPBY CRUDO PARA IR VIENDO FRECUENCIA DE RECLAMACION DE DERECHOS
gb1 = df.groupby('derecho_fundamental').count()


#%% DATAFRAMES POR CADA PALABRA CLAVE
principales_name = ['PETICION', 'DEBIDO', 'CONSULTA', 'TRABAJO', 'DIGNIDAD', 'VIDA', 'VITAL', 'ACCESO', 'DEFENSA', 'AGUA', 'VIVIENDA', 'SALUD', 'AMBIENTE']


# LOOP DE DATAFRAMES
particiones = []
for i in range(len(principales_name)):
    k = df[df['derecho_fundamental'].str.contains(principales_name[i], na=False)]
    particiones.append(k)

# LOOP DE TAMANOS DE MUESTRA
muestra_principales = []
for i in range(len(particiones)):
    k = particiones[i].shape[0]
    muestra_principales.append(k)

# ZIP PARA HACER UNA TABLITA: DE DICCIONARIO A DATAFRAME: LA TABLA SE LLAMA df_frec_principales
frec_principales = dict(zip(principales_name, muestra_principales))
df_frec_principales = pd.DataFrame(list(frec_principales.items()),columns = ['Derecho','Frecuencia'])
print(frec_principales)
df_frec_principales = df_frec_principales.sort_values(['Frecuencia'], ascending=False)

# TOP 3 DE DERECHOS 

top3_name = df_frec_principales['Derecho']
top3_name = top3_name[:3].tolist()
#%% DUMMIES PARA CADA DERECHO IMPORTANTE EN MI DATAFRAME PRINCIPAL

df['derecho_cat'] = np.nan

# EJEMPLO CON PETICION
df['derecho_fundamental'].map(lambda x: True if 'PETICION' in str(x) else False)


# este loop tiene el problema de que solo me deja uno de los valores que puede tomar principales, eso no me sirve
for i in range(len(principales_name)):
    a = df['derecho_fundamental'].map(lambda x: True if principales_name[i] in str(x) else False)
    df['derecho_cat'] = np.where(a,i,df['derecho_cat'])
    
# mejor voy a crear un array de dummies para cada derecho principal

cats_dummies = []

for i in range(len(principales_name)):
    a = df['derecho_fundamental'].map(lambda x: True if principales_name[i] in str(x) else False)
    cats_dummies.append(a)

df_cats = pd.concat(cats_dummies, axis=1)
df_cats.columns = principales_name

df = pd.concat([df,df_cats], axis=1)

#%% DERECHOS TUTELADOS POR AÑO Y MES

temporales = ['year', 'month']
gb2 = df.groupby(temporales)[principales_name].sum()


# aparentemente, la mayoría de las tutelas son al final del año

gb2.to_excel('derechos_anomes.xlsx')


#%% para ver derechos más tutelados en cada año

gb3 = df.groupby('year')[principales_name]


# PARTICIONES POR AÑO

# PARA LAS LINEGRAPHS
particiones_year = []
sums_year = []
sumstop3_year = []

for year, year_df in gb3:
    print(year)
    print(year_df)
    particiones_year.append(year_df)
    print(particiones_year)
    suma = year_df.groupby('month')[principales_name].sum()
    sumatop3 = year_df.groupby('month')[top3_name].sum()
    sums_year.append(suma)
    sumstop3_year.append(sumatop3)

# PARA LOS PIECHARTS

anuales = []
gb4 = df.groupby('year')[principales_name]
for year, year_df in gb4:
    print(year)
    k = year_df.groupby('year').sum()
    anuales.append(k)
    

#%% dummy de que existe segunda instancia


ar = df["Despacho de Segunda Instancia"]
    
a = df['Despacho de Segunda Instancia'].map(lambda x: True if ' ' in str(x) else False)
df['instancia2'] = np.where(a,True,False)

gb5 = df.groupby('instancia2')[principales_name].mean()
df5 = gb5.transpose()






#%%
import seaborn as sns
import plotly.express as px
import chart_studio.plotly as py
import cufflinks as cf



