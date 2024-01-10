import requests
import sys
import urllib

'''
metodo = 'GET'
uri_base = "http://gae-sw-2017.appspot.com/processForm"
cabeceras = {'Host': 'gae-sw-2017.appspot.com'}
query = {'dni': sys.argv[1]}
query_encoded = urllib.parse.urlencode(query)
uri= uri_base + '?' + query_encoded
respuesta = requests.request(metodo, uri,
headers=cabeceras, allow_redirects=False)

codigo = respuesta.status_code
descripcion = respuesta.reason
print(str(codigo) + " " + descripcion)
for cabecera in respuesta.headers:
    print(cabecera + ": " + respuesta.headers[cabecera])
cuerpo = respuesta.content
print(cuerpo)
'''


metodo = 'POST'
uri = "http://gae-sw-2017.appspot.com/processForm"
cabeceras = {'Host': 'gae-sw-2017.appspot.com',
             'Content-Type': 'application/x-www-form-urlencoded'}
cuerpo = {'dni': sys.argv[1]}
cuerpo_encoded = urllib.parse.urlencode(cuerpo)
cabeceras['Content-Length'] = str(len(cuerpo_encoded))
respuesta = requests.request(metodo, uri, data=cuerpo_encoded,
                             headers=cabeceras, allow_redirects=False)

codigo = respuesta.status_code
descripcion = respuesta.reason
print(str(codigo) + " " + descripcion)
for cabecera in respuesta.headers:
    print(cabecera + ": " + respuesta.headers[cabecera])
cuerpo = respuesta.content
print(cuerpo)
