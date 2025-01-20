# Crear DataFrame
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Convertir el atributo a datetime
from datetime import datetime,timedelta
fecha = "2025-01-12"



def generar_fechas(fecha_inicial, dias, fecha_list):
    if dias == 0:  # Caso base: detener la recursión
        return fecha_list
    else:
        nueva_fecha = fecha_inicial + timedelta(days=len(fecha_list))
        fecha_list.append(nueva_fecha.strftime("%Y-%m-%d"))
        return generar_fechas(fecha_inicial, dias - 1, fecha_list)
    

# Parámetros iniciales
fecha_inicial = datetime.strptime("2024-12-28", "%Y-%m-%d")

fecha_list = []

resultado = generar_fechas(fecha_inicial, 4, fecha_list)

print(resultado)


for fecha in resultado:
    #fecha = "2024-12-31"
    filename = f"azi_speed_log_{fecha}.csv"
    try:
        print("FILENAME",filename)
        df = pd.read_csv(filename)


        # Eliminar filas con valores nulos
        df = df.dropna(subset=["Average_Azi_Speed"])



        # Extraer solo la hora (como entero)
        df=df[df["Average_Azi_Speed"]>4.8]
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        #df_excluded = df[df['Timestamp'].dt.year != 2025]
        df_excluded = df[df['Timestamp'].dt.year != 2024]

        print(df_excluded)

        #df = df[df['Timestamp'].dt.year == 2025]
        df = df[df['Timestamp'].dt.year == 2024]

        
        df['Timestamp'] = df['Timestamp'] #-timedelta(hours=5)
        df['Time'] = df['Timestamp'].dt.time
        print(df['Timestamp'])

        #df['Decimal_Hour'] = (df['Time'].apply(lambda x: x.hour + x.minute / 60 + x.second / 3600))
        #plt.plot(df['Decimal_Hour'], df['Average_Azi_Speed'],color="skyblue")
        plt.plot(df['Timestamp'], df['Average_Azi_Speed'],color="skyblue")
        plt.plot(df["Timestamp"],np.ones(len(df["Timestamp"]))*5,color="red")
        #plt.plot(df['Decimal_Hour'])
        # Personalizar gráfico
        plt.title(f"Velocidad Promedio vs Tiempo Fecha: {fecha}")
        plt.xlabel("Tiempo")
        plt.ylabel("Velocidad (m/s)")
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)
        # Mostrar el gráfico
        plt.tight_layout()
        #plt.show()
        #if fecha==resultado[-1]:            
        plt.savefig(f"AZI_VEL-fecha_{fecha}.png")
        plt.clf() ### para chancar todos
        df = pd.DataFrame()
    except:
        print("Not today",filename)
        plt.clf()
        df = pd.DataFrame()
