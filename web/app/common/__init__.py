#!/usr/bin/env python
import requests
import json

def api_action(action, params={}):
    url = "http://127.0.0.1:5000/api"
    headers = {"Content-type": "application/json"}
    data = {
        "jsonrpc": 2.0,
        "method" : action,
        "id": 1,
        "auth": None,
        "params": params
    } 
    r = requests.post(url, headers=headers ,json=json.dumps(data))
    if str(r.status_code) == "200":
        ret = json.loads(r.content)
    if ret.has_key('result'):
        return ret['result']
    else:
        return ret['error']
