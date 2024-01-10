import requests
import urllib
import webbrowser
from socket import AF_INET, socket, SOCK_STREAM
import json
import helper

app_key = 'esv5jy6wm5zdv06'
app_secret = 'kb1d7kvrw2x8yk5'
server_addr = "localhost"
server_port = 8090
redirect_uri = "http://" + server_addr + ":" + str(server_port)

class Dropbox:
    _access_token = ""
    _path = "/"
    _files = []
    _root = None
    _msg_listbox = None

    def __init__(self, root):
        self._root = root

    def local_server(self):
        # por el puerto 8090 esta escuchando el servidor que generamos
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((server_addr, server_port))
        server_socket.listen(1)
        print("\tLocal server listening on port " + str(server_port))

        # recibe la redireccio 302 del navegador
        client_connection, client_address = server_socket.accept()
        peticion = client_connection.recv(1024)
        print("\tRequest from the browser received at local server:")
        print (peticion)

        # buscar en solicitud el "auth_code"
        primera_linea =peticion.decode('UTF8').split('\n')[0]
        aux_auth_code = primera_linea.split(' ')[1]
        auth_code = aux_auth_code[7:].split('&')[0]
        print ("\tauth_code: " + auth_code)

        # devolver una respuesta al usuario
        http_response = "HTTP/1.1 200 OK\r\n\r\n" \
                        "<html>" \
                        "<head><title>Proba</title></head>" \
                        "<body>The authentication flow has completed. Close this window.</body>" \
                        "</html>"
        client_connection.sendall(http_response.encode(encoding='utf-8'))
        client_connection.close()
        server_socket.close()

        return auth_code

    def do_oauth(self):
        #############################################
        # RELLENAR CON CODIGO DE LAS PETICIONES HTTP
        # Y PROCESAMIENTO DE LAS RESPUESTAS HTTP
        # PARA LA OBTENCION DEL ACCESS TOKEN
        #############################################
        server = 'www.dropbox.com'
        params = {'response_type': 'code',
                  'client_id': app_key,
                  'redirect_uri': redirect_uri}
        params_encoded = urllib.parse.urlencode(params)
        res = '/oauth2/authorize?' + params_encoded
        uri = 'https://' + server + res
        webbrowser.open_new(uri)
        auth_code = self.local_server()
        params = {'code': auth_code,
                  'grant_type': 'authorization_code',
                  'client_id': app_key,
                  'client_secret': app_secret,
                  'redirect_uri': redirect_uri}
        cabeceras = {'User-Agent': 'Python Client',
                     'Content-Type': 'application/x-www-form-urlencoded'}
        uri = 'https://api.dropboxapi.com/oauth2/token'
        respuesta = requests.post(uri, headers=cabeceras, data=params)
        print(respuesta.status_code)
        json_respuesta = json.loads(respuesta.content)
        self._access_token = json_respuesta['access_token']
        print("Access_Token:" + self._access_token)
        self._root.destroy()

    def list_folder(self, msg_listbox):
        print("/list_folder")
        uri = 'https://api.dropboxapi.com/2/files/list_folder'
        # https://www.dropbox.com/developers/documentation/http/documentation#files-list_folder
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################
        path = self._path
        if path=="/":
            path=""
        datos = {'path': path}
        datos_encoded = json.dumps(datos)
        print("Datuak: " + datos_encoded)
        cabeceras = {'Host': 'api.dropboxapi.com',
                     'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json'}
        respuesta = requests.post(uri, headers=cabeceras, data=datos_encoded, allow_redirects=False)
        status = respuesta.status_code
        print("\tStatus: " + str(status))
        contenido = respuesta.text
        contenido_json = json.loads(contenido)
        print("Ficheros en " + path)
        self._files = helper.update_listbox2(msg_listbox, self._path, contenido_json)

    def transfer_file(self, file_path, file_data):
        print("/upload")
        uri = 'https://content.dropboxapi.com/2/files/upload'
        # https://www.dropbox.com/developers/documentation/http/documentation#files-upload
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################
        metodo = 'POST'
        headers = {'Host': 'content.dropboxapi.com',
                     'Authorization': 'Bearer ' + self._access_token,
                     'Dropbox-API-Arg': '{\"autorename\":false,\"mode\":\"add\",\"mute\":false,\"path\":\"' + str(file_path) +'\",\"strict_conflict\":false}',
                     'Content-Type': 'application/octet-stream'}
        respuesta = requests.request(metodo, uri, headers=headers, data=file_data, allow_redirects=False)
        status = respuesta.status_code
        print(status)

    def delete_file(self, file_path):
        print("/delete_file")
        uri = 'https://api.dropboxapi.com/2/files/delete_v2'
        # https://www.dropbox.com/developers/documentation/http/documentation#files-delete
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################

        datos = {'path': file_path}
        datos_encoded = json.dumps(datos)
        print("Datuak: " + datos_encoded)
        cabeceras = {'Host': 'api.dropboxapi.com',
                     'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json'}
        respuesta = requests.post(uri, headers=cabeceras, data=datos_encoded, allow_redirects=False)
        status = respuesta.status_code
        print("\tStatus: " + str(status))


    def create_folder(self, path):
        print("/create_folder")
        uri = "https://api.dropboxapi.com/2/files/create_folder_v2"
       # https://www.dropbox.com/developers/documentation/http/documentation#files-create_folder
        #############################################
        # RELLENAR CON CODIGO DE LA PETICION HTTP
        # Y PROCESAMIENTO DE LA RESPUESTA HTTP
        #############################################
        datos = {"autorename": False,
                "path": path}
        datos_encoded = json.dumps(datos)
        print("Datuak: " + datos_encoded)
        cabeceras = {'Host': 'api.dropboxapi.com',
                     'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json'}
        respuesta = requests.post(uri, headers=cabeceras, data=datos_encoded, allow_redirects=False)
        status = respuesta.status_code
        print("\tStatus: " + str(status))
        print(respuesta.content)
        print(respuesta.reason)