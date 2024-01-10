###################
#SOLO PARA PRUEBAS#
###################
"""
from tkinter import messagebox
import requests
import urllib
from urllib.parse import unquote
from bs4 import BeautifulSoup
import time
import helper

username='LDAP'
password = 'CONTRASEÑA'

def print_info(metodo, uri, status, descripcion, location, cookie):
    print("Método: " + str(metodo) + "URI: " + str(uri))
    print("Status: " + str(status) + str(descripcion))
    print("Location: " + str(location) + "Set-Cookie: " + str(cookie))

popup, progress_var, progress_bar = helper.progress("check_credentials", "Logging into eGela...")
progress = 0
progress_var.set(progress)
progress_bar.update()

print("##### 1. PETICION #####")
metodo = 'GET'
uri = "https://egela.ehu.eus/login/index.php"
#############################################
# RELLENAR CON CODIGO DE LA PETICION HTTP
# Y PROCESAMIENTO DE LA RESPUESTA HTTP
#############################################
respuesta = requests.request(metodo, url=uri)
if respuesta.status_code == 200:
    cookie = respuesta.headers['Set-Cookie'].split(";")[0]
    cuerpo = respuesta.content
    print_info(metodo, uri, respuesta.status_code, respuesta.reason, '', cookie)
    soup = BeautifulSoup(cuerpo, 'html.parser')
    logintoken = soup.find("input", {"name": "logintoken"})['value']
else:
    messagebox.showinfo("Alert Message", "Egela not available!")

progress = 25
progress_var.set(progress)
progress_bar.update()
time.sleep(1)

print("\n##### 2. PETICION #####")
#############################################
# RELLENAR CON CODIGO DE LA PETICION HTTP
# Y PROCESAMIENTO DE LA RESPUESTA HTTP
#############################################
headers = {'Host': 'egela.ehu.eus',
           'Content-Type': 'application/x-www-form-urlencoded',
           'Cookie': cookie}
cuerpo = {'logintoken': logintoken,
          'username': username,
          'password': password}
cuerpo_encoded = urllib.parse.urlencode(cuerpo)
headers['Content-Length'] = str(len(cuerpo_encoded))
metodo = 'POST'

respuesta = requests.request(metodo, uri, headers=headers, data=cuerpo_encoded, allow_redirects=False)
new_location = respuesta.headers['location']
print(respuesta.headers)
try:
    new_cookie = respuesta.headers['Set-Cookie'].split(';')[0]
    num = print_info(metodo, uri, respuesta.status_code, respuesta.reason, new_location, new_cookie)
except KeyError:
    print("Error en inicio de sesión: Contraseña incorrecta. SALIENDO")
    exit(0)

progress = 50
progress_var.set(progress)
progress_bar.update()
time.sleep(1)

print("\n##### 3. PETICION #####")
#############################################
# RELLENAR CON CODIGO DE LA PETICION HTTP
# Y PROCESAMIENTO DE LA RESPUESTA HTTP
#############################################
num = print_info(metodo, uri, respuesta.status_code, respuesta.reason, new_location, new_cookie)

metodo = 'GET'
headers = {'Cookie': new_cookie}
respuesta = requests.request(metodo, url=new_location, headers=headers, allow_redirects=False)

progress = 75
progress_var.set(progress)
progress_bar.update()
time.sleep(1)
popup.destroy()

print("\n##### 4. PETICION #####")
#############################################
# RELLENAR CON CODIGO DE LA PETICION HTTP
# Y PROCESAMIENTO DE LA RESPUESTA HTTP
#############################################

progress = 100
progress_var.set(progress)
progress_bar.update()
time.sleep(1)
popup.destroy()

url = 'https://egela.ehu.eus/'
print_info(metodo, uri, respuesta.status_code, respuesta.reason, new_location, new_cookie)
respuesta = requests.request(metodo, url=url, headers=headers, allow_redirects=False)
print_info(metodo, url, respuesta.status_code, respuesta.reason, '', new_cookie)
if respuesta.status_code == 200:
    print("autenticacion correcta")
"""