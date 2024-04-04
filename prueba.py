import json
from pathlib import Path

def cargar_datos(ruta):
    with open(ruta, "r") as contenido:
        info = json.load(contenido)["info"]
        return info

if __name__ == '__main__':
    datos = cargar_datos("configHume.json")
    print(datos)
    hume1 = datos['hume1']
    print(hume1)
#hume2 = datos['hume2']
#hume3 = datos['hume3']

datos = cargar_datos("configTemp.json")
#temp1 = datos['temp1']
#temp2 = datos['temp2']
#temp3 = datos['temp3']

datos = cargar_datos("configHumo.json")
#humo1 = datos['humo1']
#humo2 = datos['humo2']