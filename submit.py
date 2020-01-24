import requests
res = requests.post('http://localhost:5000/submit', json={"mytext":"lalala"})
if res.ok:
    print("The server returned: {}".format(res.json()))
