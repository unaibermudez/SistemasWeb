import requests
import sys
import urllib
from bs4 import BeautifulSoup

# nombre y apellidos junto con el enlace de las personas encontradas en el directorio de la ehu que se llaman Unai

metodo = 'POST'
uri = 'https://www.ehu.eus//bilatu/buscar/sbilatu.php?lang=es1'
cabeceras = {'Host': 'www.ehu.eus',
             'Content-Type': 'application/x-www-form-urlencoded'}
cuerpo = {'ize': 'unai'}
cuerpo_encoded = urllib.parse.urlencode(cuerpo)
cabeceras['Content-Length'] = str(len(cuerpo_encoded))
respuesta = requests.request(metodo, uri, headers=cabeceras, data=cuerpo_encoded, allow_redirects=False)

codigo = respuesta.status_code
descripcion = respuesta.reason
print(str(codigo) + " " + descripcion)
html = respuesta.content
documento = BeautifulSoup(html, 'html.parser')
#print(documento)


lista_persona = documento.find_all('td', {'class', 'fondo_listado'})
for i in range(len(lista_persona)):
    print(str(i) + "-" + lista_persona[i].text + ": " + "https://www.ehu.eus/" + lista_persona[i].find('a').get('href'))

