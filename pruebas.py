import numpy as np
import matplotlib.pyplot as plt

# Definir los datos
NumPag= [1.09, 0.18, -1.64, 0.18, 0.18]
FreqCrime = [-0.66, -0.87, 1.2, 1, -0.66]

# Crear el gráfico
plt.scatter(FreqCrime, NumPag)

# Agregar etiquetas a los ejes
plt.xlabel('FreqCrime')
plt.ylabel('NumPag')

plt.grid(True)
# Mostrar el gráfico
plt.show()

((300 + 1) / (600 + 2)) * (600 / 1000) / ((300 + 1) / (600 + 2) * (600 / 1000) + (11 + 1) / (400 + 2) * (400 / 1000))