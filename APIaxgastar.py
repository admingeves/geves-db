import requests
from requests.auth import HTTPBasicAuth

def response_avance(p1,p2,avance3,avance4):
#URL de la API y parámetros
    url = 'https://appauranet.com/APIAURANETB2B/api/Data/AuranetApiGEXP'
    parametros = {'key':'S3V5MEl4R1Fqd0NTVWJCL3JFWUpHcE9NM1YvZU1pUTBScVEyZng3VnRJeGtTN3ZMd3NWbXpnQTZBUWc0T21ZTg==',
        'func':'OBTENERAVANCEXGASTAROBRA',
        'p1':p1,
        'p2':p2,
        'p3':avance3,
        'p4':avance4}

    #Credenciales de autenticación
    username = 'zmTd5mveLhKn5qlY5BBxow=='
    password = 'HApGNu8lVd0AOgEIODpmDQ=='

    #Llamada a la API con autenticación Basic Auth y parámetros de URL
    response_avance = requests.get(url, params=parametros, auth=HTTPBasicAuth(username, password))

    return response_avance