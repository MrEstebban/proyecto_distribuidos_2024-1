import json
from datetime import datetime
import statistics

# Función para calcular la diferencia en milisegundos entre dos fechas
def calculate_time_difference(start, end):
    start_dt = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
    end_dt = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
    difference = (start_dt - end_dt).total_seconds() * 1000
    return difference

# Función para calcular el tiempo promedio y desviación estándar
def calculate_communication_times(file_path):
    times = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                data = json.loads(line)
                if data.get('action') == 'get':
                    start_time = data.get('date')
                    end_time = data.get('receivedDate')
                    if start_time and end_time:
                        time_difference = calculate_time_difference(start_time, end_time)
                        times.append(time_difference)
    except Exception as e:
        print(f"Error al leer datos: {e}")
    
    if times:
        average_time = statistics.mean(times)
        stdev_time = statistics.stdev(times)
    else:
        average_time = 0
        stdev_time = 0
    
    return average_time, stdev_time

# Archivo a procesar
cloud_data_file = 'cloud_data.json'

# Calcular tiempos de comunicación
average_time, stdev_time = calculate_communication_times(cloud_data_file)

# Generar reporte
report_file = 'communication_times_report.txt'
with open(report_file, 'w') as report:
    report.write(f"Promedio de tiempos de comunicación: {average_time:.2f} ms\n")
    report.write(f"Desviación estándar de los tiempos de comunicación: {stdev_time:.2f} ms\n")

print(f"Reporte guardado en {report_file}")
