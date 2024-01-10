import json
import urllib

import requests

USER_API_KEY = "N1CTLPLK8HSHEYRS"

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
    if channels_parse[i]["name"] == "Unai":
        print(channels_parse[i]["api_keys"][1]["api_key"])