# -*- coding: UTF-8 -*-
from tkinter import messagebox
import requests
import urllib
from urllib.parse import unquote
from bs4 import BeautifulSoup
import time
import helper

class eGela:
    _login = 0
    _cookie = ""
    _curso = ""
    _refs = []
    _root = None

    def __init__(self, root):
        self._root = root

    def print_info(self, metodo, uri, status, descripcion, location, cookie):
        print("Método: " + str(metodo) + "URI: " + str(uri))
        print("Status: " + str(status) + str(descripcion))
        print("Location: " + str(location) + " Set-Cookie: " + str(cookie))

    def check_credentials(self, username, password, event=None):
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
            self.print_info(metodo, uri, respuesta.status_code, respuesta.reason, '', cookie)
            soup = BeautifulSoup(cuerpo, 'html.parser')
            logintoken = soup.find("input", {"name": "logintoken"})['value']

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
        self.print_info(metodo, uri, respuesta.status_code, respuesta.reason, new_location, "new_cookie")
        try:
            new_cookie = respuesta.headers['Set-Cookie'].split(';')[0]
        except KeyError:
            print("Error en inicio de sesión: Contraseña incorrecta. SALIENDO")
            messagebox.showinfo("Alert Message", "Login incorrect!")
            return


        progress = 50
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(1)

        print("\n##### 3. PETICION #####")
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################
        num = self.print_info(metodo, uri, respuesta.status_code, respuesta.reason, new_location, new_cookie)

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
        self.print_info(metodo, uri, respuesta.status_code, respuesta.reason, new_location, new_cookie)
        respuesta = requests.request(metodo, url=url, headers=headers, allow_redirects=False)
        self.print_info(metodo, url, respuesta.status_code, respuesta.reason, '', new_cookie)
        if respuesta.status_code==200:
            self._login=True
            self._cookie=new_cookie
            print("autenticacion correcta")
            soup2 = BeautifulSoup(respuesta.content, 'html.parser')
            links = soup2.findAll("a", {'class': 'ehu-visible'})
            for x in links:
                if "Sistemas Web" in x.text:
                    self._curso = x['href']
            self._root.destroy()
        else:
            messagebox.showinfo("Alert Message", "Login incorrect!")

    def get_pdf_refs(self):
        popup, progress_var, progress_bar = helper.progress("get_pdf_refs", "Downloading PDF list...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("\n##### 4. PETICION (Página principal de la asignatura en eGela) #####")
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################
        metodo = 'GET'
        headers = {'Cookie': self._cookie}
        respuesta = requests.request(metodo, url=self._curso, headers=headers, allow_redirects=False)
        self.print_info(metodo, self._curso, respuesta.status_code, respuesta.reason, '', self._cookie)

        print("\n##### Analisis del HTML... #####")
        #############################################
        # ANALISIS DE LA PAGINA DEL AULA EN EGELA
        # PARA BUSCAR PDFs
        #############################################
        soup3 = BeautifulSoup(respuesta.content, "html.parser")
        e = soup3.find_all("img", {"role": "presentation"})
        pdfs=[]
        for x in e:
            if "pdf" in str(x):
                pdfs.append(x)

        # INICIALIZA Y ACTUALIZAR BARRA DE PROGRESO
        # POR CADA PDF ANIADIDO EN self._refs
        self._refs = []
        progress_step = float(100.0 / len(pdfs))
        for x in pdfs:
            response = requests.request('GET', url=x.parent['href'], headers=headers, allow_redirects=False)
            # self.print_info(metodo, x.parent['href'], response.status_code, response.reason, '', self._cookie)
            loc = response.headers['Location']
            nombre =loc.split("/")[-1]
            print(nombre)
            print(loc)
            pdf = [nombre, loc]
            self._refs.append(pdf)
            progress += progress_step
            progress_var.set(progress)
            progress_bar.update()
            time.sleep(0.1)
        popup.destroy()
        return self._refs

    def get_pdf(self, selection):
        print("\t##### descargando  PDF... #####")
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################
        loc = self._refs[selection][1]
        pdf_name = self._refs[selection][0]
        metodo = 'GET'
        headers = {'Cookie': self._cookie}
        response = requests.request(metodo, url=loc, headers=headers, allow_redirects=False)
        #self.print_info(metodo, loc, response.status_code, response.reason, '', self._cookie)
        pdf_content = response.content
        return pdf_name, pdf_content