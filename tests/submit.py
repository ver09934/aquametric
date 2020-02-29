import requests
import datetime
import numpy as np

now = datetime.datetime.now()
nowstr = now.strftime("%Y-%m-%dT%H:%M:%S.{:03d}Z").format(round(int(now.strftime("%f")) / 10**3))

# NOTE: For going in reverse, take the string, insert "000" before the Z, and use this format:
# "%Y-%m-%dT%H:%M:%S.%fZ"

# '2020-02-25T00:16:58.228Z'

json_data = {
    'event': 'Measurement',
    'data': '{{"id":"002","battery":{},"stage":{},"temp":{},"conductivity":{},"turbidity":{}}}'.format(
        np.round(np.random.uniform(low=3, high=4.5), 6),
        np.round(np.random.uniform(low=75, high=125), 6),
        np.round(np.random.uniform(low=0, high=10), 6),
        np.round(np.random.uniform(low=0, high=1), 6),
        np.round(np.random.uniform(low=0, high=3.3), 6)
    ),
    'published_at': nowstr,
    'coreid': 'e00fce68bc77a626f8b797ea'
}

print(json_data)
# json_data = "{'event': 'Measurement', 'data': '{\"id\":\"001\",\"battery\":3.887500,\"stage\":101,\"temp\":3.110135,\"conductivity\":0.935604,\"turbidity\":0.255458}', 'published_at': '2020-02-28T11:53:00.694Z', 'coreid': 'e00fce68bc77a626f8b797ea'}"

# res = requests.post('http://localhost:5000/submit-new', data=json_data) # ONLY WORKS TO USE DATA IF DATA IS STRING, NOT DICT!
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
