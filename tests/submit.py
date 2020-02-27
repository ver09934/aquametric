import requests

json_data = {'event': 'Measurement', 'data': '{"id":"001","battery":4.132500,"stage":100,"temp":4.080159,"conductivity":0.835678,"turbidity":0.201465}', 'published_at': '2020-02-25T00:16:58.228Z', 'coreid': 'e00fce68bc77a626f8b797ea'}

res = requests.post('http://localhost:5000/submit-new', json=json_data)

if res.ok:
    print("The server returned: {}".format(res.json()))
