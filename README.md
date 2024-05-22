# Sistema Distribuido de Detección de Incendios

Este repositorio contiene la implementación de un sistema distribuido para la detección de incendios utilizando una arquitectura Edge, Fog, y Cloud. El sistema incluye sensores simulados para medir temperatura, humedad y humo, un proxy para procesamiento intermedio y una capa cloud para almacenamiento y análisis de datos.

## Instrucciones para la Ejecución

### Requisitos Previos

- Python 3.7 o superior
- Librerías Python: `zmq`, `json`, `datetime`, `statistics`
- Archivos de configuración: `configHume.json`, `configTemp.json`, `configHumo.json`

### Instalación de Dependencias

Asegúrate de tener instaladas las librerías necesarias. Puedes instalarlas utilizando pip:

```bash
pip install pyzmq
```

## Ejecución de los Componentes

Sigue los pasos en el orden indicado para ejecutar cada componente del sistema.

### 1. Iniciar la Capa Cloud
La capa Cloud recibe datos del proxy, calcula la humedad mensual y almacena toda la información para el análisis.

```bash
python Cloud.py
```

### 2. Iniciar el Proxy Principal

El proxy principal es responsable de recibir datos de los sensores y enviarlos a la capa Cloud. También realiza verificaciones de salud para garantizar su funcionamiento continuo.

```bash
python Proxy.py
```

### 3. Iniciar el Proxy de Respaldo
El proxy de respaldo monitoriza el proxy principal y toma el control en caso de fallo. Escucha en un puerto diferente y verifica regularmente la salud del proxy principal.

```bash
python Proxy_backup.py
```

### 4. Iniciar los Sensores
Los sensores simulan la medición de temperatura, humedad y humo. Generan datos y los envían al proxy principal (o al de respaldo en caso de fallo).

```bash
python Sensores.py
```


## Notas
- Asegúrate de que los archivos de configuración (configHume.json, configTemp.json, configHumo.json) están en el mismo directorio que los scripts de los sensores.
- Los sensores se conectan inicialmente al proxy principal, pero pueden redirigirse al proxy de respaldo en caso de fallo. Esta implementación asegura que el sistema pueda manejar fallas en el proxy principal y continuar funcionando sin interrupciones significativas.
- La capa Cloud almacena los datos en un archivo cloud_data.json para su análisis posterior.
- El proxy principal y el de respaldo monitorean la disponibilidad utilizando mensajes de "ping".
- Los sensores se conectan inicialmente al proxy principal, pero el proxy de respaldo puede asumir el control en caso de fallas.

## Estructura del Proyecto
- sensor.py: Script para simular los sensores de temperatura, humedad y humo.
- proxy.py: Script del proxy principal.
- proxy_backup.py: Script del proxy de respaldo.
- cloud.py: Script de la capa Cloud para el almacenamiento y análisis de datos.
- configHume.json, configTemp.json, configHumo.json: Archivos de configuración para los sensores.

## Contribución
Si deseas contribuir a este proyecto, por favor abre un issue o crea un pull request en el repositorio.

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.
