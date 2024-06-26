library(dplyr)
library(readr)
library(tidyr)
library(ggplot2)

# aqui definiremos las patologias (no son gias de patos)
patologias <- c(
    "Deaths - Cause: Rheumatic heart disease - Sex: Both sexes - Age group: ALLAges",
    "Deaths - Cause: Cardiomyopathy, myocarditis, endocarditis - Sex: Both sexes - Age group: ALLAges",
    "Deaths - Cause: Other circulatory diseases - Sex: Both sexes - Age group: ALLAges",
    "Deaths - Cause: Hypertensive heart disease - Sex: Both sexes - Age group: ALLAges",
    "Deaths - Cause: Ischaemic stroke - Sex: Both sexes - Age group: ALLAges",
    "Deaths - Cause: Haemorrhagic stroke - Sex: Both sexes - Age group: ALLAges",
    "Deaths - Cause: Ischaemic heart disease - Sex: Both sexes - Age group: ALLAges"
)


# aqui leeremos el archivo csv
file_path <- "muertes_por_enfermedades.csv"
if (!file.exists(file_path)) {
    stop("el archivo no esta aqui pendejo, busca en otra parte >:C ")
}

df <- read_csv(file_path)

# verificamos que las columnas necesarias existan
required_columns <- c("Entity", patologias)
missing_columns <- setdiff(required_columns, colnames(df))
if (length(missing_columns) > 0) {
    stop(paste("faltan las siguientes columnas en tu archivo CSV:", paste(missing_columns, collapse = " , ")))
} # end of if

# obtendremos una lista unica de paises unicos uwu
paises_unicos <- df %>%
    select(Entity) %>%
    distinct() %>%
    pull()

print(paises_unicos)

# Definir listas de países por continente
P_Africa <- c("Africa", "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi", "Cape Verde", "Central African Republic", "Chad", "Comoros", "Congo", "Democratic Republic of Congo", "Djibouti", "Egypt", "Equatorial Guinea", "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Cote d'Ivoire", "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe", "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa", "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia", "Zimbabwe")

P_AmericaNorte <- c("North America", "Antigua and Barbuda", "Bahamas", "Barbados", "Belize", "Canada", "Costa Rica", "Cuba", "Dominican Republic", "El Salvador", "Grenada", "Guatemala", "Haiti", "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Saint Lucia", "Saint Vincent and the Grenadines", "Trinidad and Tobago", "United States")

P_AmericaSur <- c("South America", "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Guyana", "Paraguay", "Peru", "Suriname", "Uruguay", "Venezuela")

P_Asia <- c("Asia", "Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan", "Brunei", "Cambodia", "China", "Cyprus", "East Timor", "Georgia", "India", "Indonesia", "Iran", "Iraq", "Israel", "Japan", "Jordan", "Kazakhstan", "Kuwait", "Kyrgyzstan", "Laos", "Lebanon", "Malaysia", "Maldives", "Mongolia", "Myanmar", "Nepal", "North Korea", "Oman", "Pakistan", "Philippines", "Qatar", "Saudi Arabia", "Singapore", "South Korea", "Sri Lanka", "Syria", "Tajikistan", "Thailand", "Turkmenistan", "United Arab Emirates", "Uzbekistan", "Vietnam", "Yemen")

P_Europa <- c("Europe", "Albania", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria", "Croatia", "Czechia", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece", "Hungary", "Iceland", "Ireland", "Italy", "Latvia", "Lithuania", "Luxembourg", "Malta", "Moldova", "Montenegro", "Netherlands", "North Macedonia", "Norway", "Poland", "Portugal", "Romania", "Russia", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden", "Switzerland", "Ukraine", "United Kingdom")

P_Oceania <- c("Oceania", "Australia", "Fiji", "Kiribati", "Micronesia (country)", "New Zealand", "Papua New Guinea", "Samoa", "Solomon Islands", "Tonga", "Vanuatu")

# pur que añadimos al mundo como una lista??? quien sabe orita checamos que pedo
Mundo <- c("World")

# Crear diccionario de continentes
continentes <- list("Africa" = P_Africa, "America del Norte" = P_AmericaNorte, "America del Sur" = P_AmericaSur, "Asia" = P_Asia, "Europa" = P_Europa, "Oceania" = P_Oceania, "Mundo" = Mundo)

# en la siguiente funcion crearemos un metodo para reemplazar texto:
reemplazar_texto <- function(texto) {
    reemplazos <- c(
        "Deaths - Cause: Rheumatic heart disease - Sex: Both sexes - Age group: ALLAges" = "Muertes por Enfermedad Cardíaca Reumática",
        "Deaths - Cause: Cardiomyopathy, myocarditis, endocarditis - Sex: Both sexes - Age group: ALLAges" = "Muertes por Cardiomiopatía, Miocarditis y Endocarditis",
        "Deaths - Cause: Other circulatory diseases - Sex: Both sexes - Age group: ALLAges" = "Muertes por Enfermedades Circulatorias",
        "Deaths - Cause: Hypertensive heart disease - Sex: Both sexes - Age group: ALLAges" = "Muertes por Enfermedad Cardíaca Hipertensiva",
        "Deaths - Cause: Ischaemic stroke - Sex: Both sexes - Age group: ALLAges" = "Muertes por Ictus Isquémico",
        "Deaths - Cause: Haemorrhagic stroke - Sex: Both sexes - Age group: ALLAges" = "Muertes por Ictus Hemorrágico",
        "Deaths - Cause: Ischaemic heart disease - Sex: Both sexes - Age group: ALLAges" = "Muertes por Enfermedad Cardíaca Isquémica"
    )
    return(reemplazos[texto])
}

# filtramos datos por continente:
filtrar_por_continente <- function(df, paises) {
    df %>% filter(Entity %in% paises)
}

# usamos la funcion recien creada para cada conjunto de datos por region previamente preparado:collapsePaises_Africa <- filtrar_por_continente(df, P_Africa)
Paises_Africa <- filtrar_por_continente(df, P_Africa)
Paises_Asia <- filtrar_por_continente(df, P_Asia)
Paises_AmericaNorte <- filtrar_por_continente(df, P_AmericaNorte)
Paises_AmericaSur <- filtrar_por_continente(df, P_AmericaSur)
Paises_Oceania <- filtrar_por_continente(df, P_Oceania)
Paises_Europa <- filtrar_por_continente(df, P_Europa)

# Definir funciones para cálculos estadísticos
calcular_media_paises <- function(data) {
    mean(data, na.rm = TRUE)
}

calcular_varianza_paises <- function(data) {
    var(data, na.rm = TRUE)
}

# ahora vamos a normalizar los datos por region geografica:
normalizar_datos <- function(df, paises, patologias) {
    valores_estandarizados <- list()
    for (pais in paises) {
        df_pais <- df %>% filter(Entity == pais)
        if (nrow(df_pais) > 0) {
            for (patologia in patologias) {
                if (patologia %in% colnames(df_pais)) {
                    data_patologia <- df_pais[[patologia]]
                    media <- calcular_media_paises(data_patologia)
                    des_est <- sqrt(calcular_varianza_paises(data_patologia))
                    if (des_est != 0) {
                        nval <- (data_patologia - media) / des_est
                    } else {
                        nval <- data_patologia - media
                    }
                    patologia_legible <- reemplazar_texto(patologia)
                    valores_estandarizados[[pais]][[patologia_legible]] <- mean(nval, na.rm = TRUE) # Almacenar el promedio de los valores normalizados
                }
            }
        }
    }
    return(valores_estandarizados)
}

# utilizamos nuestro metodo recien creado en nuestras regiones:
valores_estandarizados_africa <- normalizar_datos(Paises_Africa, P_Africa, patologias)
valores_estandarizados_asia <- normalizar_datos(Paises_Asia, P_Asia, patologias)
valores_estandarizados_americanorte <- normalizar_datos(Paises_AmericaNorte, P_AmericaNorte, patologias)
valores_estandarizados_americasur <- normalizar_datos(Paises_AmericaSur, P_AmericaSur, patologias)
valores_estandarizados_oceania <- normalizar_datos(Paises_Oceania, P_Oceania, patologias)
valores_estandarizados_europa <- normalizar_datos(Paises_Europa, P_Europa, patologias)

# Crear DataFrame con los resultados normalizados y escribir en un nuevo archivo CSV
resultados <- list()

for (continente in names(continentes)) {
    datos <- switch(continente,
        "Africa" = valores_estandarizados_africa,
        "Asia" = valores_estandarizados_asia,
        "America del Norte" = valores_estandarizados_americanorte,
        "America del Sur" = valores_estandarizados_americasur,
        "Oceania" = valores_estandarizados_oceania,
        "Europa" = valores_estandarizados_europa,
    )
    for (pais in names(datos)) {
        valores <- datos[[pais]]
        if (is.list(valores)) {
            for (patologia in names(valores)) {
                resultados <- append(resultados, list(data.frame(Continente = continente, Pais = pais, Patologia = patologia, Valor_Estandarizado = valores[[patologia]])))
            }
        } else {
            warning(paste("Se esperaba un diccionario pero se encontró un", class(valores), "para", pais, "en", continente))
        }
    }
}

df_resultados <- bind_rows(resultados)
output_file <- "resultados_estandarizados.csv"
write_csv(df_resultados, output_file)
cat("Archivo CSV 'resultados_estandarizados.csv' creado con éxito.\n")

#hola el maricon de luis 
# hola otra vez uwu
#hola una vez mas xd
#comentarios 
#mas comentarios 
#un video mas mi gente nos fuimos 
#hola buenos dias 
# mala noticia mi gente, mala noticia
#nos fuimos mi gente