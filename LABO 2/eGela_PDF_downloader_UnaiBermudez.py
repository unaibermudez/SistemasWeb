import csv
import getpass
import os
import sys
import urllib

import requests
from bs4 import BeautifulSoup


# proyectos personales BERMUDEZ OSABA
# SISTEMAS WEB GL1
# 25 DE MARZO 2023
# ENTREGA PRACTICA 2 -  Buscar Información en eGela
# DESCRIPCION:
# 1.- Descargar a una carpeta del ordenador los ficheros PDF que aparecen en la página principal
# de eGela de esta asignatura.

# 2.‐ Crear un documento tareas.csv con todas las tareas a realizar en el curso, la fecha de entrega
# y el enlace a las mismas.


def print_info(num, metodo, uri, cuerpo, status, description, location, cookie):
    print("#######################################################################")
    print("")
    print(f"Petición número: {num}")
    print("SOLICITUD:")
    print(f"Metodo: {metodo} URI: {uri}")
    print(f"Cuerpo: {str(cuerpo)}")
    print("\nRESPUESTA:")
    print(f"Status: {status} {description}")
    print(f"Location: {location} Set-Cookie: {cookie}")
    print("")
    print("#######################################################################")
    print("")


if __name__ == "__main__":
    username = sys.argv[1]
    nombre_apellido = sys.argv[2]  # proyectos personales BERM\xc3\x9aDEZ
    password = getpass.getpass(prompt="contraseña:")
    # password = "Abridge@001"
    uri = "https://egela.ehu.eus/"

    # PRIMERA PETICION
    metodo = 'GET'
    uri = uri + "/login/index.php"
    cabeceras = {'Host': 'egela.ehu.eus'}
    respuesta = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)
    if respuesta.status_code == 200:
        cookie = respuesta.headers['Set-Cookie'].split(";")[0]
        html = respuesta.content
        document = BeautifulSoup(html, 'html.parser')
        logintoken = document.find("input", {"name": "logintoken"})["value"]
        set_cookie = respuesta.headers['Set-Cookie'].split(";")[0]

    print_info(1, metodo, uri, None, respuesta.status_code, respuesta.reason, None, set_cookie)

    # SEGUNDA PETICION
    metodo = 'POST'
    cabeceras = {'Host': 'egela.ehu.eus',
                 'Content-Type': 'application/x-www-form-urlencoded',
                 'Cookie': cookie, }
    cuerpo = {'logintoken': logintoken,
              'username': username,
              'password': password}
    cuerpo_encoded = urllib.parse.urlencode(cuerpo)
    cabeceras['Content-Length'] = str(len(cuerpo_encoded))
    respuesta2 = requests.request(metodo, uri, headers=cabeceras,
                                  data=cuerpo_encoded, allow_redirects=False)
    try:
        respuesta2.headers['Set-Cookie']
    except KeyError:
        print("CONTRASEÑA INCORRECTA")
        exit(1)
    newCookie = respuesta2.headers['Set-Cookie'].split(";")[0]
    location = respuesta2.headers['Location']
    testsession = respuesta2.headers['Location'].split("=")[1]

    print_info(2, metodo, uri, cuerpo, respuesta2.status_code, respuesta2.reason, location, newCookie)

    # TERCERA PETICION
    metodo = 'GET'
    uri = uri + "?testsession=" + testsession
    cabeceras = {'Host': 'egela.ehu.eus',
                 'Cookie': newCookie, }
    respuesta3 = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)
    # print(str(respuesta3.status_code) + " " + respuesta3.reason)
    location = respuesta3.headers['Location']

    print_info(3, metodo, uri, None, respuesta3.status_code, respuesta3.reason, location, newCookie)

    # CUARTA PETICION
    metodo = 'GET'
    uri = "https://egela.ehu.eus"
    cabeceras = {'Host': 'egela.ehu.eus',
                 'Cookie': newCookie, }
    respuesta4 = requests.request(metodo, uri, headers=cabeceras, allow_redirects=False)

    print_info(4, metodo, uri, None, respuesta4.status_code, respuesta4.reason, None, newCookie)

    if nombre_apellido in str(respuesta4.content):
        print("ACCESO CONCEDIDO!")
        input("pulsa cualquier tecla para continuar...")
        soup = BeautifulSoup(respuesta4.content, 'html.parser')
        asignaturas = soup.find("a", {"class": "ehu-visible"}, string="Sistemas Web")
        uri = asignaturas["href"]
        respuesta5 = requests.get(uri, headers=cabeceras, allow_redirects=False)
        soup2 = BeautifulSoup(respuesta5.content, 'html.parser')
        pdf = soup2.find_all("img", {"src": "https://egela.ehu.eus/theme/image.php/ehu/core/1678718742/f/pdf"})
        print("Guardando PDFs...")
        for p in pdf:
            nombre_pdf = str(p.parent.span).split('>')[1].split('<')[0]
            href = p.parent["href"]
            response = requests.get(href, headers=cabeceras, allow_redirects=False)
            soup3 = BeautifulSoup(response.content, "html.parser")
            base_url = urllib.parse.urlparse(href).scheme + "://" + urllib.parse.urlparse(href).hostname
            current_url = urllib.parse.urljoin(base_url, soup3.find("a", href=True)["href"])
            response2 = requests.get(current_url, headers=cabeceras, allow_redirects=False)
            os.makedirs("PDF", exist_ok=True)
            with open(f"./PDF/{nombre_pdf}.pdf", "wb") as f:
                f.write(response2.content)
            print("PDF guardado:", nombre_pdf)

        tareas = soup2.find_all("img",
                                {"src": "https://egela.ehu. eus/theme/image.php/ehu/assign/1678718742/icon"})

        with open('tareas.csv', 'w', newline='') as file:
            file.write(f"nombre; fecha; enlace \n")
        print("TAREAS: \n")
        for t in tareas:
            if t.parent["class"][0] == "aalink":
                nombre_tarea = t.parent.span.text
                enlace = t.parent["href"]
                response = requests.get(enlace, headers=cabeceras)
                soup4 = BeautifulSoup(response.content, "html.parser")
                fecha = soup4.find('th', string=["Entregatze-data", "Fecha de entrega"]).find_next_sibling(
                    'td').text
                with open('tareas.csv', 'a', newline='') as file:
                    file.write(f"{nombre_tarea}; {fecha}; {enlace} \n")
                print(f"nombre: {str(nombre_tarea)}\n fecha: {str(fecha)}\n enlace: {enlace}\n\n")

    else:
        print("ACCESO DENEGADO")
        exit(1)
