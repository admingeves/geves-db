import requests
from requests.auth import HTTPBasicAuth

def response_kardex(p1,p2,par3,kardex4,kardex5,kardex6):
#URL de la API y parámetros
    url = 'https://appauranet.com/APIAURANETB2B/api/Data/AuranetApiGEXP'
    parametros = {'key':'S3V5MEl4R1Fqd0NTVWJCL3JFWUpHcE9NM1YvZU1pUTBScVEyZng3VnRJeGtTN3ZMd3NWbXpnQTZBUWc0T21ZTg==',
        'func':'DBQUERYKARDEXOBRA',
        'p1':p1,
        'p2':p2,
        'p3':par3,
        'p4':kardex4,
        'p5':kardex5,
        'p6':kardex6}

    #Credenciales de autenticación
    username = 'zmTd5mveLhKn5qlY5BBxow=='
    password = 'HApGNu8lVd0AOgEIODpmDQ=='

    #Llamada a la API con autenticación Basic Auth y parámetros de URL
    response_kardex = requests.get(url, params=parametros, auth=HTTPBasicAuth(username, password))

    return response_kardex