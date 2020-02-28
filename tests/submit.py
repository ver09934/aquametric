import requests
import datetime

now = datetime.datetime.now()
nowstr = now.strftime("%Y-%m-%dT%H:%M:%S.{:03d}Z").format(round(int(now.strftime("%f")) / 10**3))

# NOTE: For going in reverse, take the string, insert "000" before the Z, and use this format:
# "%Y-%m-%dT%H:%M:%S.%fZ"

# '2020-02-25T00:16:58.228Z'

json_data = {'event': 'Measurement', 'data': '{"id":"001","battery":4.132500,"stage":100,"temp":4.080159,"conductivity":0.835678,"turbidity":0.201465}', 'published_at': nowstr, 'coreid': 'e00fce68bc77a626f8b797ea'}

res = requests.post('http://localhost:5000/submit-new', json=json_data)
# res = requests.post('http://localhost:5000/submit-new', json={'a': 'b'})
# res = requests.post('http://localhost:5000/submit-new', json='{"a": "b"}')
# res = requests.post('http://localhost:5000/submit-new', json="{'a': 'b'}")
# res = requests.post('http://localhost:5000/submit-new', data="{'a': 'b'}")

# res = requests.post('http://localhost:5000/submit-new', data='{"a": "b"}', headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
# res = requests.post('http://localhost:5000/submit-new', data="{'a': 'b'}", headers={'Content-type': 'application/json', 'Accept': 'text/plain'})
# res = requests.post('http://localhost:5000/submit-new', data="{'a': 'b'}")

if res.ok:
    print("The server returned: {}".format(res.json()))
