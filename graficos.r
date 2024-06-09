
library(readr)
library(ggplot2)
library(reshape2)

# Leer el archivo CSV con los resultados
resultados <- read_csv('resultados_estandarizados.csv')



#HEAT MAP 
# Reestructurar los datos para el heatmap
heatmap_data <- dcast(resultados, Pais + Continente ~ Patologia, value.var = "Valor_Estandarizado")

# Crear heatmap
ggplot(melt(heatmap_data, id.vars = c("Pais", "Continente")), aes(x = variable, y = Pais, fill = value)) +
  geom_tile() +
  scale_fill_gradient(low = "white", high = "red") +
  theme_minimal() +
  labs(title = "Heatmap de Muertes por Patologías Cardiovasculares por País",
       x = "Patología",
       y = "País",
       fill = "Valor Estandarizado") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

  #GRAFICO DE BARRAS AGRUPADAS
ggplot(resultados, aes(x = Patologia, y = Valor_Estandarizado, fill = Continente)) +
  geom_bar(stat = "identity", position = "dodge") +
  theme_minimal() +
  labs(title = "Comparación de Muertes por Patologías Cardiovasculares por Continente",
       x = "Patología",
       y = "Valor Estandarizado",
       fill = "Continente") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))


#boxplot
# Boxplot por continente y patología
ggplot(resultados, aes(x = Continente, y = Valor_Estandarizado, fill = Patologia)) +
  geom_boxplot() +
  theme_minimal() +
  labs(title = "Distribución de Muertes por Patologías Cardiovasculares por Continente",
       x = "Continente",
       y = "Valor Estandarizado",
       fill = "Patología") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))


#grafico de lineas: 
# Gráfico de líneas por continente y patología
ggplot(resultados, aes(x = Continente, y = Valor_Estandarizado, color = Patologia, group = Patologia)) +
  geom_line() +
  geom_point() +
  theme_minimal() +
  labs(title = "Tendencia de Muertes por Patologías Cardiovasculares por Continente",
       x = "Continente",
       y = "Valor Estandarizado",
       color = "Patología") +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))
