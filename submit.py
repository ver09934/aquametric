import requests
# res = requests.post('http://localhost:5000/submit', json={"mytext":"lalala"})
res = requests.post('http://aquametric.menon.pro/submit', json={"Ian": "is testing this."})
if res.ok:
    print("The server returned: {}".format(res.json()))
