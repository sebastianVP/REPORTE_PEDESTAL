import os
import re
from datetime import datetime
import h5py
import numpy as np
import matplotlib.pyplot as plt
import csv


################################################
## BUSQUEDA DE DIRECTORIOS DE DATOS DEL PEDESTAL 
## DIARIO
################################################

base_path = "/DATA_RM/DATA"

# Patrón para carpetas que cumplan con HYO@2025-MONTH-DAYT
pattern = r"HYO@2025-\d{2}-\d{2}T"
#pattern = r"HYO@2024-\d{2}-\d{2}T"
# Listar todas las carpetas en el directorio base
filtered_folders = []
for folder in os.listdir(base_path):
    if os.path.isdir(os.path.join(base_path, folder)) and re.match(pattern, folder):
        filtered_folders.append(os.path.join(base_path, folder))


#### El filtro esta aplicado por FECHA
#### PODEMOS COLOCAR LA FECHA DE INTERES
# Obtener la fecha actual en formato "YYYY-MM-DD"
today_date = datetime.now().strftime("%Y-%m-%d")
##################################################
######     FECHA DE INTERES #####################
today_date = "2025-01-16"
#today_date = "2024-12-31"
##################################################
# Filtrar las rutas que contengan la fecha de hoy
routes = filtered_folders
filtered_routes = [route for route in routes if today_date in route]

# Imprimir las rutas filtradas
print("Rutas filtradas para la fecha de hoy:")
for route in filtered_routes:
    print(route)

total_list = []

for rou in filtered_routes:
    full_pedestal= os.path.join(rou,"position")
    file_list = os.listdir(full_pedestal)
    full_total = [os.path.join(full_pedestal,file) for file in file_list]
    total_list.extend(full_total)
print(len(total_list))

print(sorted(total_list))

##################################
#LISTA Y BUCLE FOR PARA PROMEDIAR 
#LA VELOCIDAD
##################################

TOTAL_LIST = sorted(total_list)




# Función para calcular el promedio de 'azi_speed' en un archivo HDF5
def calculate_avg_speed(filename):
    try:
        with h5py.File(filename, "r") as obj:
            for key in obj.keys():
                for key2 in obj[key].keys():
                    if key2 == "azi_speed":
                        param = f"{key}/{key2}"
                        key3  = "utc"
                        time_utc= f"{key}/{key3}"
                        try:
                            data = np.array(obj[param])
                            avg_speed = np.mean(data)
                            time_obj = np.array(obj[time_utc])
                            time_0   = time_obj[0]
                            return avg_speed,time_0
                        except Exception as e:
                            print(f"Error al procesar '{key2}' en {filename}: {e}")
                            return None,None
        print(f"'azi_speed' no encontrado en el archivo {filename}.")
        return None
    except FileNotFoundError:
        print(f"El archivo {filename} no existe.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo {filename}: {e}")
        return None



# Archivo CSV para el log
log_filename = f"azi_speed_log_{today_date}.csv"

# Escribir encabezado en el archivo CSV
with open(log_filename, mode='w', newline='') as log_file:
    csv_writer = csv.writer(log_file)
    csv_writer.writerow(["Timestamp", "Filename", "Average_Azi_Speed"])


for base_path in TOTAL_LIST:
  # Directorio base
  #base_path = "/DATA_RM/DATA/HYO@2025-01-16T00-00-34/position/2025-01-16T14-00-00"
  last_part = os.path.basename(base_path)
  # Listar archivos en el directorio
  file_list = sorted(os.listdir(base_path))
  print("file_list",file_list)
  # Crear rutas completas utilizando os.path.join
  full_paths = [os.path.join(base_path, file) for file in file_list]

  # Calcular los promedios de 'azi_speed' para cada archivo y registrar en el CSV
  average_speeds = []
  valid_files = []

  print("TEST","CHECK")

  for filename in full_paths:
      try:
          avg_speed,time_0 = calculate_avg_speed(filename)
      except:
          print("Error----calculo")
          avg_speed = None
      if avg_speed is not None:
          average_speeds.append(avg_speed)
          valid_files.append(filename)
          # Agregar registro al archivo CSV
          with open(log_filename, mode='a', newline='') as log_file:
              csv_writer = csv.writer(log_file)
              time   = datetime.fromtimestamp(time_0)
              fecha_hora= time
              #timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
              csv_writer.writerow([fecha_hora, os.path.basename(filename), avg_speed])
              #csv_writer.writerow([fecha_hora, os.path.basename(filename), avg_speed])
