import sys
import os
import requests
import datetime
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from aquametric import util

json_data = {
    'event': 'Measurement',
    'data': '{{"id":"001","battery":{},"stage":{},"temp":{},"conductivity":{},"turbidity":{}}}'.format(
        np.round(np.random.uniform(low=3, high=4.5), 6),
        np.round(np.random.uniform(low=75, high=125), 6),
        np.round(np.random.uniform(low=0, high=10), 6),
        np.round(np.random.uniform(low=0, high=1), 6),
        np.round(np.random.uniform(low=0, high=3.3), 6)
    ),
    'published_at': util.get_fake_timestring(),
    'coreid': 'e00fce68bc77a626f8b797ea'
}

# json_data = "{'event': 'Measurement', 'data': '{\"id\":\"001\",\"battery\":3.887500,\"stage\":101,\"temp\":3.110135,\"conductivity\":0.935604,\"turbidity\":0.255458}', 'published_at': '2020-02-28T11:53:00.694Z', 'coreid': 'e00fce68bc77a626f8b797ea'}"

res = requests.post('http://localhost:5000/submit-new', json=json_data)
# res = requests.post('http://localhost:5000/submit-new', data=json_str, headers={'Content-type': 'application/json', 'Accept': 'text/plain'})

if res.ok:
    print("The server returned: {}".format(res.json()))
