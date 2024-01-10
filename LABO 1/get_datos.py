import json
import csv
import requests
import urllib

USER_API_KEY = "N1CTLPLK8HSHEYRS"


def get_datos():
    metodo = 'GET'
    uri = "https://api.thingspeak.com/channels/2045546/feeds.json?api_key=YOO1M441ZLU8FB72&results=100"
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
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dict_datos["datos"])


if __name__ == "__main__":
    get_datos()
