import requests
from requests.auth import HTTPBasicAuth

def response_consumo(p1,p2,par3,par4):
# URL de la API y parámetros
    url = 'https://appauranet.com/APIAURANETB2B/api/Data/AuranetApiGEXP'
    params = {'key':'S3V5MEl4R1Fqd0NTVWJCL3JFWUpHcE9NM1YvZU1pUTBScVEyZng3VnRJeGtTN3ZMd3NWbXpnQTZBUWc0T21ZTg==',
              'func':'DBQUERYDASBOAROBRACONSUMOS',
              'p1':p1,
              'p2':p2,
              'p3':par3,
              'p4':par4,
              'p5':'', 
              'p6': '1'}

    # Credenciales de autenticación
    username = 'zmTd5mveLhKn5qlY5BBxow=='
    password = 'HApGNu8lVd0AOgEIODpmDQ=='

    # Realizar la llamada a la API con autenticación Basic Auth y parámetros de URL
    response_consumo = requests.get(url, params=params, auth=HTTPBasicAuth(username, password))

    return response_consumo