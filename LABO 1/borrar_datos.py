import json
import csv
import requests
import urllib

USER_API_KEY = "N1CTLPLK8HSHEYRS"


def borrar_datos():
    metodo = 'DELETE'
    uri = "https://api.thingspeak.com/channels/2045546/feeds.json?api_key=" + USER_API_KEY
    cabeceras = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)
    codigo = respuesta.status_code
    descripcion = respuesta.reason
    print(str(codigo) + " " + descripcion)



if __name__ == "__main__":
    borrar_datos()
