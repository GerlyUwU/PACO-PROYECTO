# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

# Leer el archivo CSV con la ruta corregida
df = pd.read_csv('muertes_por_enfermedades.csv')

# Definir listas de países por continente
P_Africa = ["Africa", "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cape Verde", "Central African Republic", "Chad", "Comoros", "Congo", "Democratic Republic of Congo",  "Djibouti",  "Egypt", "Equatorial Guinea",  "Eritrea", "Eswatini", "Ethiopia",  "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Cote d'Ivoire", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", "Senegal", "Seychelles", "Sierra Leone", "Somalia",  "South Africa", "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe"]

P_AmericaNorte = ["North America", "Antigua and Barbuda", "Bahamas", "Barbados", "Belize", "Canada", "Costa Rica", "Cuba", "Dominican Republic", "El Salvador", "Grenada", "Guatemala", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Saint Lucia", "Saint Vincent and the Grenadines", "Trinidad and Tobago", "United States"]

P_AmericaSur = ["South America", "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Guyana", "Paraguay", "Peru", "Suriname", "Uruguay", "Venezuela"]

P_Asia = ["Asia", "Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia", "China", "Cyprus", "East Timor", "Georgia", "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan", "Jordan", "Kazakhstan", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", "Maldives", "Mongolia", "Myanmar", "Nepal", "North Korea", "Oman", "Pakistan", "Philippines", "Qatar", "Saudi Arabia", "Singapore", "South Korea", "Sri Lanka", "Syria", "Tajikistan", "Thailand", "Turkmenistan", "United Arab Emirates", "Uzbekistan", "Vietnam", "Yemen"]

P_Europa = ["Europe", "Albania", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Czechia", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Iceland", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Moldova", "Montenegro", "Netherlands", "North Macedonia", "Norway", "Poland", "Portugal", "Romania", "Russia", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine", "United Kingdom"]

P_Oceania = ["Oceania", "Australia", "Fiji", "Kiribati", "Micronesia (country)", "New Zealand", "Papua New Guinea", "Samoa", "Solomon Islands", "Tonga", "Vanuatu"]

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

# Normalizar datos por continente
valores_estandarizados = {}

for continente, paises in continentes.items():
    for pais in paises:
        df_pais = df[df['Entity'] == pais]
        if not df_pais.empty:
            for patologia in patologias:
                data_patologia = df_pais[patologia]
                media = data_patologia.mean()
                des_est = data_patologia.std()
                nval = (data_patologia - media) / des_est
                patologia_legible = reemplazar_texto(patologia)
                if pais not in valores_estandarizados:
                    valores_estandarizados[pais] = {}
                valores_estandarizados[pais][patologia_legible] = nval.mean()

# Normalizar datos a nivel mundial
for patologia in patologias:
    data_patologia = df[patologia]
    media = data_patologia.mean()
    des_est = data_patologia.std()
    nval = (data_patologia - media) / des_est
    patologia_legible = reemplazar_texto(patologia)
    valores_estandarizados['Mundo'] = {patologia_legible: nval.mean()}

# Crear DataFrame con los resultados normalizados y escribir en un nuevo archivo CSV
resultados = []

for pais, valores in valores_estandarizados.items():
    for patologia, valor in valores.items():
        resultados.append({"Pais": pais, "Patologia": patologia, "Valor Estandarizado": valor})

# Convertir a DataFrame y guardar en CSV
df_resultados = pd.DataFrame(resultados)
df_resultados.to_csv('resultados_estandarizados.csv', index=False)

print("Archivo CSV 'resultados_estandarizados.csv' creado con éxito.")
