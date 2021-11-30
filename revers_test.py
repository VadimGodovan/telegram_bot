import requests
from pprint import pprint

url = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
headers = {'Authorization': f'OAuth AQAAAAALZcGmAAYckUkJZfxH-ETrpZPoMxouw4k'}
payload = {'from_date': 0}

# Делаем GET-запрос к эндпоинту url с заголовком headers и параметрами params
homework_statuses = requests.get(url, headers=headers, params=payload)

# Печатаем ответ API в формате JSON
#print(homework_statuses.text)
result_status = (homework_statuses.json())
result_status = result_status["homeworks"][0]
pprint(result_status['status'])

# А можно ответ в формате JSON привести к типам данных Python и напечатать и его
# print(homework_statuses.json())