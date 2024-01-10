import time

import requests
import urllib.parse
import random


def subir_datos(pCpu, pRam):
    metodo = 'POST'
    uri = "https://api.thingspeak.com/update"
    cabeceras = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    cuerpo = {'api_key': "EEFNA1MBTCOO39EK",
              "field1": pCpu,
              "field2": pRam}
    cuerpo_encoded = urllib.parse.urlencode(cuerpo)
    cabeceras['Content-Length'] = str(len(cuerpo_encoded))
    respuesta = requests.request(metodo, uri, headers=cabeceras,
                                 data=cuerpo_encoded, allow_redirects=False)
    codigo = respuesta.status_code
    descripcion = respuesta.reason
    print(str(codigo) + " " + descripcion)


if __name__ == "__main__":
    cpu = random.randint(0, 100)
    ram = random.randint(0, 100)
    subir_datos(cpu, ram)

