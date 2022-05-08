import requests
from pprint import pprint

json_data = {
        'id': 1,
        'name': 'New Name',
        'about': 'New Super Student',
        'password': 'qwe',
        'city_from': 'Пермь',
        'email': 'qwe@qwe.ru'
}


response = requests.get("http://localhost:5000/api/user/1").json()
pprint(response)
