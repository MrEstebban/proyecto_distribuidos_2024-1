import json
import matplotlib.pyplot as plt

# Función para contar mensajes enviados en un archivo
def count_sent_messages(file_path):
    count = 0
    try:
        with open(file_path, 'r') as file:
            for line in file:
                #print(line)
                data = json.loads(line)
                if data.get('action') == 'alert':
                    count += 1
    except Exception as e:
        print(f"Error al leer datos: {e}")
    return count

# Archivos a procesar
cloud_data_file = 'cloud_data.json'

# Contar mensajes enviados en cada archivo
total_messages_sent = 0
total_messages_sent += count_sent_messages(cloud_data_file)


# Datos para el gráfico de barras
labels = ['Cloud', 'Capa Fog', 'Capa Edge']
values = [total_messages_sent, 0, 0,]

# Crear el gráfico de barras
plt.bar(labels, values, color=['blue', 'green', 'red'])
plt.xlabel('Categorias')
plt.ylabel('Número de mensajes')
plt.title('Reporte de Mensajes Enviados')

# Guardar el gráfico en un archivo
#plt.savefig('messages_report.png')

plt.show()