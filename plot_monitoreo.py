import pandas as pd
import matplotlib.pyplot as plt

filename = "azi_speed_log_2025-01-07.csv"
# Crear DataFrame
df = pd.read_csv(filename)
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Eliminar filas con valores nulos
df = df.dropna(subset=["Average_Azi_Speed"])
print("######################################")
print(df["Timestamp"])
# Graficar la velocidad
plt.figure(figsize=(10, 6))
plt.plot(df["Timestamp"], df["Average_Azi_Speed"], label="Velocidad", color="b")

# Añadir línea horizontal en y=5
plt.axhline(y=5, color='r', linestyle='--', label="Velocidad = 5")

# Personalizar gráfico
plt.title("Velocidad Promedio vs Tiempo")
plt.xlabel("Tiempo")
plt.ylabel("Velocidad (m/s)")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)

# Mostrar el gráfico
plt.tight_layout()
plt.show()
