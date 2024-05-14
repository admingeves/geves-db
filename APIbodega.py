import requests
from requests.auth import HTTPBasicAuth

#Llamada de los select a la API
def response(p1,p2,p4,p5):
#URL de la API y parámetros
    url = 'https://appauranet.com/APIAURANETB2B/api/Data/AuranetApiGEXP'
    params = {'key':'S3V5MEl4R1Fqd0NTVWJCL3JFWUpHcE9NM1YvZU1pUTBScVEyZng3VnRJeGtTN3ZMd3NWbXpnQTZBUWc0T21ZTg==',
        'func':'DBQUERYMOVIMIENTOBODEGA',
        'p1':p1,
        'p2':p2,
        'p3':'',
        'p4':p4,
        'p5':p5}

#Credenciales de autenticación
    username = 'zmTd5mveLhKn5qlY5BBxow=='
    password = 'HApGNu8lVd0AOgEIODpmDQ=='

#Llamada a la API con autenticación Basic Auth y parámetros de URL
    response = requests.get(url, params=params, auth=HTTPBasicAuth(username, password))

    return response