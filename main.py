# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io
from scipy.stats import mode
import seaborn as sns

# Leer el archivo CSV con la ruta corregida
try:
    df = pd.read_csv('muertes_por_enfermedades.csv')
except FileNotFoundError:
    print("El archivo no se encontró. Verifica la ruta.")
    exit()

# Verificar que las columnas necesarias existen
required_columns = ['Entity'] + patologias
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    print(f"Faltan las siguientes columnas en el archivo CSV: {missing_columns}")
    exit()

paises = df['Entity']

# Eliminar duplicados y convertirlo a una lista
paises_unicos = paises.drop_duplicates().tolist()

print(paises_unicos)

# Definir listas de países por continente
# (Las listas de países y continentes se mantienen igual)

Mundo = ["World"]

# Definir patologías
patologias = ['Deaths - Cause: Rheumatic heart disease - Sex: Both sexes - Age group: ALLAges',
              'Deaths - Cause: Cardiomyopathy, myocarditis, endocarditis - Sex: Both sexes - Age group: ALLAges',
              'Deaths - Cause: Other circulatory diseases - Sex: Both sexes - Age group: ALLAges',
              'Deaths - Cause: Hypertensive heart disease - Sex: Both sexes - Age group: ALLAges',
              'Deaths - Cause: Ischaemic stroke - Sex: Both sexes - Age group: ALLAges',
              'Deaths - Cause: Haemorrhagic stroke - Sex: Both sexes - Age group: ALLAges',
              'Deaths - Cause: Ischaemic heart disease - Sex: Both sexes - Age group: ALLAges']

# Crear diccionario de continentes
continentes = {"Africa": P_Africa, "America del Norte": P_AmericaNorte, "America del Sur": P_AmericaSur, "Asia": P_Asia, "Europa": P_Europa, "Oceania": P_Oceania, "Mundo": Mundo}

# Definir función para reemplazar texto
def reemplazar_texto(texto):
    reemplazos = {'Deaths - Cause: Rheumatic heart disease - Sex: Both sexes - Age group: ALLAges': 'Muertes por Enfermedad Cardíaca Reumática',
                  'Deaths - Cause: Cardiomyopathy, myocarditis, endocarditis - Sex: Both sexes - Age group: ALLAges': 'Muertes por Cardiomiopatía, Miocarditis y Endocarditis',
                  'Deaths - Cause: Other circulatory diseases - Sex: Both sexes - Age group: ALLAges': 'Muertes por Enfermedades Circulatorias',
                  'Deaths - Cause: Hypertensive heart disease - Sex: Both sexes - Age group: ALLAges': 'Muertes por Enfermedad Cardíaca Hipertensiva',
                  'Deaths - Cause: Ischaemic stroke - Sex: Both sexes - Age group: ALLAges': 'Muertes por Ictus Isquémico',
                  'Deaths - Cause: Haemorrhagic stroke - Sex: Both sexes - Age group: ALLAges': 'Muertes por Ictus Hemorrágico',
                  'Deaths - Cause: Ischaemic heart disease - Sex: Both sexes - Age group: ALLAges': 'Muertes por Enfermedad Cardíaca Isquémica'}
    return reemplazos.get(texto, texto)

# Filtrar datos por continente
# (El filtrado de datos por continente se mantiene igual)

# Diccionarios para almacenar los valores estandarizados
valores_estandarizados_africa = {}
valores_estandarizados_asia = {}
valores_estandarizados_americanorte = {}
valores_estandarizados_americasur = {}
valores_estandarizados_oceania = {}
valores_estandarizados_europa = {}
valores_estandarizados_mundo = {}

# Definir funciones para cálculos estadísticos
def calcular_media_paises(data):
    return np.nanmean(data)

def calcular_varianza_paises(data):
    return np.nanvar(data)

# Normalizar datos por continente
for continente, paises_continente, valores_estandarizados in zip(
        ["Africa", "Asia", "America del Norte", "America del Sur", "Oceania", "Europa"],
        [P_Africa, P_Asia, P_AmericaNorte, P_AmericaSur, P_Oceania, P_Europa],
        [valores_estandarizados_africa, valores_estandarizados_asia, valores_estandarizados_americanorte, valores_estandarizados_americasur, valores_estandarizados_oceania, valores_estandarizados_europa]):
    for pais in paises_continente:
        df_pais = df[df['Entity'] == pais]
        if not df_pais.empty:
            for patologia in patologias:
                if patologia in df_pais.columns:
                    data_patologia = df_pais[patologia]
                    media = calcular_media_paises(data_patologia)
                    des_est = np.sqrt(calcular_varianza_paises(data_patologia))
                    if des_est != 0:
                        nval = (data_patologia - media) / des_est
                        patologia_legible = reemplazar_texto(patologia)
                        if pais not in valores_estandarizados:
                            valores_estandarizados[pais] = {}
                        valores_estandarizados[pais][patologia_legible] = nval.mean()  # Almacenar el promedio de los valores normalizados

# Normalizar datos a nivel mundial
for patologia in patologias:
    if patologia in df.columns:
        data_patologia = df[patologia]
        media = calcular_media_paises(data_patologia)
        des_est = np.sqrt(calcular_varianza_paises(data_patologia))
        if des_est != 0:
            nval = (data_patologia - media) / des_est
            patologia_legible = reemplazar_texto(patologia)
            valores_estandarizados_mundo[patologia_legible] = nval.mean()  # Almacenar el promedio de los valores normalizados

# Crear DataFrame con los resultados normalizados y escribir en un nuevo archivo CSV
resultados = []

for continente, datos in zip(
        ["Africa", "Asia", "America del Norte", "America del Sur", "Oceania", "Europa", "Mundo"],
        [valores_estandarizados_africa, valores_estandarizados_asia, valores_estandarizados_americanorte, valores_estandarizados_americasur, valores_estandarizados_oceania, valores_estandarizados_europa, valores_estandarizados_mundo]):
    for pais, valores in datos.items():
        for patologia, valor in valores.items():
            resultados.append({"Continente": continente, "Pais": pais, "Patologia": patologia, "Valor Estandarizado": valor})

# Convertir a DataFrame y guardar en CSV
df_resultados = pd.DataFrame(resultados)
df_resultados.to_csv('resultados_estandarizados.csv', index=False)

print("Archivo CSV 'resultados_estandarizados.csv' creado con éxito.")
