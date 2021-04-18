import requests

url = 'http://localhost:8000/api/directions/'

params = {'start':'main', 'end':'Computer Science'}

resp = requests.get(url,params=params)

breakpoint()