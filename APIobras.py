import requests
from requests.auth import HTTPBasicAuth

def response_obras(p1,p2):
# URL de la API y parámetros
    url = 'https://appauranet.com/APIAURANETB2B/api/Data/AuranetApiGEXP'
    params = {'key':'S3V5MEl4R1Fqd0NTVWJCL3JFWUpHcE9NM1YvZU1pUTBScVEyZng3VnRJeGtTN3ZMd3NWbXpnQTZBUWc0T21ZTg==',
              'func':'DBQUERYLISTOBRA',
              'p1':p1,
              'p2':p2}

    # Credenciales de autenticación
    username = 'zmTd5mveLhKn5qlY5BBxow=='
    password = 'HApGNu8lVd0AOgEIODpmDQ=='

    # Realizar la llamada a la API con autenticación Basic Auth y parámetros de URL
    response_obras = requests.get(url, params=params, auth=HTTPBasicAuth(username, password))

    return response_obras