import csv
import json
import random
import signal
import sys
import time
import psutil
import requests
import urllib.parse

# proyectos personales BERMUDEZ OSABA
# SISTEMAS WEB GL1
# 27 DE FEBRERO 2023
# ENTREGA PRACTICA 1 - CLIENTE IoT
# DESCRIPCION:
# Inicialización: crear un canal de ThingSpeak considerando las excepciones indicadas como requisito B.

# Lazo principal: subir los datos de %CPU y %RAM al canal cada 15 segundos.

# Terminación: cuando se pulsa Ctrl+C, hacer un backup local de las 100 últimas muestras
# en un fichero CSV, vaciar el canal en ThingSpeak y finalizar la ejecución del programa de
# forma ordenada.


USER_API_KEY = "N1CTLPLK8HSHEYRS"


def create_channel(pName):
    metodo = 'POST'
    uri = "https://api.thingspeak.com/channels.json"
    cabeceras = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    cuerpo = {'api_key': USER_API_KEY,
              'name': pName,
              'field1': "%CPU",
              'field2': "%RAM"}
    cuerpo_encoded = urllib.parse.urlencode(cuerpo)
    print(cuerpo_encoded)
    cabeceras['Content-Length'] = str(len(cuerpo_encoded))
    respuesta = requests.request(metodo, uri, headers=cabeceras,
                                 data=cuerpo_encoded, allow_redirects=False)
    codigo = respuesta.status_code
    descripcion = respuesta.reason
    print(str(codigo) + " " + descripcion)
    cuerpo = respuesta.content
    print(cuerpo)
    cuerpo_parse = json.loads(cuerpo)
    id = cuerpo_parse["id"]
    write_api_key = cuerpo_parse["api_keys"][0]["api_key"]
    # print("id= " + str(id))
    # print("WRITE_API_KEY= " + write_api_key)
    with open('sample.txt', 'w') as f:
        f.write('ID: ' + str(id) + '\n')
        f.write('WRITE_API_KEY: ' + str(write_api_key) + '\n')

    print("Subiendo datos...")
    while True:
        subir_datos(write_api_key, psutil.cpu_percent(interval=15), psutil.virtual_memory()[2])
        # time.sleep(15)


def get_channel_names():
    metodo = 'GET'
    uri = "https://api.thingspeak.com/channels.json"
    cabeceras = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    cuerpo = {'api_key': USER_API_KEY}
    cuerpo_encoded = urllib.parse.urlencode(cuerpo)
    cabeceras['Content-Length'] = str(len(cuerpo_encoded))
    respuesta = requests.request(metodo, uri, headers=cabeceras,
                                 data=cuerpo_encoded, allow_redirects=False)
    channels = respuesta.content
    channels_parse = json.loads(channels)
    channel_names = []
    for i in range(len(channels_parse)):
        channel_names.append(channels_parse[i]["name"])
    return channel_names


def subir_datos(pApiKey, pCpu, pRam):
    metodo = 'POST'
    uri = "https://api.thingspeak.com/update"
    cabeceras = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    cuerpo = {'api_key': pApiKey,
              "field1": pCpu,
              "field2": pRam}
    cuerpo_encoded = urllib.parse.urlencode(cuerpo)
    cabeceras['Content-Length'] = str(len(cuerpo_encoded))
    respuesta = requests.request(metodo, uri, headers=cabeceras,
                                 data=cuerpo_encoded, allow_redirects=False)
    codigo = respuesta.status_code
    descripcion = respuesta.reason
    print("CPU: %" + str(pCpu) + "\tRAM: %" + str(pRam))
    # print(str(codigo) + " " + descripcion)


def get_w_api_key(pName):
    # get la write api key del canal con el nombre pName
    metodo = 'GET'
    uri = "https://api.thingspeak.com/channels.json"
    cabeceras = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    cuerpo = {'api_key': USER_API_KEY}
    cuerpo_encoded = urllib.parse.urlencode(cuerpo)
    cabeceras['Content-Length'] = str(len(cuerpo_encoded))
    respuesta = requests.request(metodo, uri, headers=cabeceras,
                                 data=cuerpo_encoded, allow_redirects=False)
    channels = respuesta.content
    channels_parse = json.loads(channels)
    for i in range(len(channels_parse)):
        if channels_parse[i]["name"] == pName:
            return channels_parse[i]["api_keys"][0]["api_key"]


def get_r_api_key(pName):
    # get la read api key del canal con el nombre pName
    metodo = 'GET'
    uri = "https://api.thingspeak.com/channels.json"
    cabeceras = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    cuerpo = {'api_key': USER_API_KEY}
    cuerpo_encoded = urllib.parse.urlencode(cuerpo)
    cabeceras['Content-Length'] = str(len(cuerpo_encoded))
    respuesta = requests.request(metodo, uri, headers=cabeceras,
                                 data=cuerpo_encoded, allow_redirects=False)
    channels = respuesta.content
    channels_parse = json.loads(channels)
    for i in range(len(channels_parse)):
        if channels_parse[i]["name"] == pName:
            return channels_parse[i]["api_keys"][1]["api_key"]


def get_ch_id(pName):
    metodo = 'GET'
    uri = "https://api.thingspeak.com/channels.json"
    cabeceras = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    cuerpo = {'api_key': USER_API_KEY}
    cuerpo_encoded = urllib.parse.urlencode(cuerpo)
    cabeceras['Content-Length'] = str(len(cuerpo_encoded))
    respuesta = requests.request(metodo, uri, headers=cabeceras,
                                 data=cuerpo_encoded, allow_redirects=False)
    channels = respuesta.content
    channels_parse = json.loads(channels)
    for i in range(len(channels_parse)):
        if channels_parse[i]["name"] == pName:
            return channels_parse[i]["id"]


def get_datos(pName):
    metodo = 'GET'
    uri = "https://api.thingspeak.com/channels/" + str(get_ch_id(pName)) + "/feeds.json?api_key=" + str(
        get_r_api_key(pName)) + "&results=100"
    cabeceras = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)
    codigo = respuesta.status_code
    descripcion = respuesta.reason
    print(str(codigo) + " " + descripcion)
    cuerpo = respuesta.content
    cuerpo_parse = json.loads(cuerpo)
    dict_datos = {"datos": []}
    n = len(cuerpo_parse["feeds"])
    for i in range(n):
        dict_datos["datos"].append(
            {"timestamp": cuerpo_parse["feeds"][i]["created_at"],
             "cpu": cuerpo_parse["feeds"][i]["field1"],
             "ram": cuerpo_parse["feeds"][i]["field2"]})

    with open("datos.json", "w") as file_object:
        json.dump(dict_datos, file_object)

    fieldnames = ['timestamp', 'cpu', 'ram']
    with open('datos.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(dict_datos["datos"])


def borrar_datos(pName):
    metodo = 'DELETE'
    uri = "https://api.thingspeak.com/channels/" + str(get_ch_id(pName)) + "/feeds.json?api_key=" + USER_API_KEY
    cabeceras = {'Host': 'api.thingspeak.com',
                 'Content-Type': 'application/x-www-form-urlencoded'}
    respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)
    codigo = respuesta.status_code
    descripcion = respuesta.reason
    print(str(codigo) + " " + descripcion)


def terminacion(sig_num, frame):
    get_datos("Unai")
    borrar_datos("Unai")
    sys.exit(0)


if __name__ == "__main__":
    # Cuando se recibe SIGINT se ejecutará el método "terminacion"
    signal.signal(signal.SIGINT, terminacion)

    print("Creating channel...")
    channel_names = get_channel_names()

    name = "pepe"
    if name in channel_names:
        print("Este canal ya existe")
        print("Subiendo datos...")
        while True:
            subir_datos(get_w_api_key(name), psutil.cpu_percent(interval=15), psutil.virtual_memory()[2])
    else:
        if len(channel_names) == 4:
            print("Numero maximo de canales alcanzado")
        else:
            create_channel(name)
            print("Canal creado")
