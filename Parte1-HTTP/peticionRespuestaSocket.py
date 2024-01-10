import socket

HOST = "www.httpwatch.com"
PORT = 80
# socket.AF_INET --- IPv4.
# socket.SOCK_STREAM --- protocolo TCP

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print("Local socket:", s.getsockname())

metodo = 'GET'
camino = "/httpgallery/chunked/chunkedimage.aspx"
primera_linea = metodo + ' ' + camino + ' ' + 'HTTP/1.1\r\n'

cabeceras = { 'Host': 'www.httpwatch.com' }
cadena_cabeceras = ''
for each in cabeceras:
    cadena_cabeceras = each + ': ' + cabeceras[each] + '\r\n'

cuerpo = ''

cadena_cabeceras_http = primera_linea + cadena_cabeceras + '\r\n' + cuerpo
cadena_cabeceras_http_bytes = bytes(cadena_cabeceras_http, 'utf-8')
print('##### HTTP peticion #####')
print(cadena_cabeceras_http_bytes )

s.sendall(cadena_cabeceras_http_bytes )
data = s.recv(1024)
print('##### HTTP respuesta #####')
print(data)

s.close()