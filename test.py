import requests

url = 'http://localhost:8000/api/roomSearch/'

params = {'code':'CSG001'}

resp = requests.get(url,params=params)

breakpoint()