import os

import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
    uri = "https://www.ehu.eus/es/web/graduak/grado-ingenieria-tecnologia-de-telecomunicacion/profesorado"
    cabeceras = {'Host': 'www.ehu.eus'}
    respuesta = requests.get(uri, headers=cabeceras, allow_redirects=False)
    if respuesta.status_code == 200:
        soup = BeautifulSoup(respuesta.content, 'html.parser')
        ul_tag = soup.find("ul", {"class": "list-links"})
        lista_profesores = ul_tag.find_all("li")

        for profesor in lista_profesores:
            uri_profesor = uri + profesor.a["href"]
            respuesta2 = requests.get(uri_profesor, headers=cabeceras, allow_redirects=False)
            soup2 = BeautifulSoup(respuesta2.content, 'html.parser')
            uri_fichaCompleta = uri + soup2.find('a', {"class": "bullet bullet-url"}, string="Ficha completa")["href"]
            respuesta3 = requests.get(uri_fichaCompleta, headers=cabeceras, allow_redirects=False)
            soup3 = BeautifulSoup(respuesta3.content, 'html.parser')
            try:
                nombre = soup3.find('div', {"class": "bg-white p-20 profesorado"}).h2.text
            except AttributeError:
                pass
            try:
                foto = soup3.find('div', {"class": "row col-lg-4 foto-profesor"}).img["src"]
                respuesta4 = requests.get(foto)
                os.makedirs("FOTOS_TELECO", exist_ok=True)
                if respuesta4.status_code == 200:
                    with open(f"./FOTOS_TELECO/{nombre}.jpg", 'wb') as f:
                        f.write(respuesta4.content)
                    print(f'Successfully saved image of {nombre}')

            except AttributeError:
                print(f"{nombre} No tiene foto")
                with open('sinfoto.csv', 'a') as f:
                    f.write(f"{nombre} NO TIENE FOTO\n")
        print("fin")
