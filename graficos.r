library(dplyr)
library(readr)
library(tidyr)
library(ggplot2)

# Leer el archivo CSV con los resultados
resultados <- read_csv('resultados_estandarizados.csv')


ggplot(resultados, aes(x = Patologia, y = Valor_Estandarizado, fill = Continente)) +
  geom_bar(stat = "identity", position = "dodge") +
  theme_minimal() +
  labs(title = "Comparación de Muertes por Patologías Cardiovasculares por Continente",
       x = "Patología",
       y = "Valor Estandarizado",
       fill = "Continente") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
