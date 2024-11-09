'''
cmd: curl -X POST -H "Content-Type: application/json" -d "{\"username\": \"teste3\", \"password\": \"Senha123^*\"}" http://127.0.0.1:8000/user/login/
cmd: curl -X GET -H "Content-Type: application/json" -d "{\"username\": \"teste3\", \"password\": \"Senha123^*\"}" http://127.0.0.1:8000/pc/

basic authentication
curl -u "teste3:Senha123*" -X GET http://127.0.0.1:8000/pc/

curl -X GET http://127.0.0.1:8000/pc/ -H "Authorization: access_token 52e1163164e4ad0a47f204a5e65bbad80baabca3"
curl -X GET http://127.0.0.1:8000/pc/ -H "Authorization: Token 52e1163164e4ad0a47f204a5e65bbad80baabca3"
curl -X GET http://127.0.0.1:8000/pc/ -H "Authorization: Token 52e1163164e4ad0a47f204a5e65bbad80baabca3"
'''
#TODO REFATORAR O CLIENT
import requests
import json
from time import sleep
from getpass import getpass
from PyLibreHardwareMonitor import Computer

def get_token():
    url = 'http://192.168.1.88:8000/user/login/'

    user = str(input('Username: '))
    password = getpass()

    # myobj = {'username': 'teste3','password': 'Senha123*'}
    myobj = {'username': user,'password': password}

    x = requests.post(url, json = myobj)
    json = x.json()
    token = json['token']
    return token

token = get_token()

headers = {'Authorization': f'Token {token}'}

response = requests.get('http://192.168.1.88:8000/pc/active', headers=headers)
json_data = response.json()
results = json_data

#TODO FAZER TRATAMENTO DE ERROS E FALTA DE CONEXÃO COM O SERVIDOR
i=1
pc_list = {}
print('Lista de computadores ativos:')
for item in results:
    print(f'{i} - {item['name']} - {item['id']}')
    pc_list[i] = item
    i+=1

option = int(input('Digite a opção numerica referente ao computador em uso: '))
print(pc_list[option]['id'])
pc_uuid = pc_list[option]['id']

url = 'http://192.168.1.88:8000/post-data/'
headers = {
    'Authorization': f'Token {token}',
    'Content-Type': 'application/json'
}


# computer = Computer()
while True:
    computer = Computer()
    data = {
        "cpu_json": computer.cpu,
        "gpu_json": computer.gpu,
        "memory_json": computer.memory,
        "pc_uuid": pc_uuid,
    }

    # print()
    # print(type(data))

    response = requests.post(url, headers=headers, json=data)
    print(response)

    sleep(60)