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

def get_treeview():
    data = _get_node()
    print json.dumps(data)
    ret = []
    return ret


def _get_node():
    idc_info = api_action("idc.get",{"output":["id", "name"]})
    child = _get_child_node()
    ret = []
    for idc in idc_info:
	node = {}
	node['text'] = idc['name']
	node['id'] = idc['id']
	node['type'] = 'idc'
	node['nodes'] = child
	ret.append(node)
    return ret

def _get_child_node():
    ret = []
    product_info = api_action("product.get", {"output":["id", "module_letter", "pid"]})
    for product in product_info:
	if product['pid'] == 0:
	    node = {}
	    node['text'] = product['module_letter']
	    node['id'] = product['id']
	    node['type'] = 'service'
	    node['nodes'] = _get_grantchild_node(product['id'])
	    ret.append(node)
    return ret

def _get_grantchild_node(id):
    ret = []
    product_info = api_action("product.get", {"output": ["id", "module_letter", "pid"]})
    for product in product_info:
	if product['pid'] == id:
	    node = {}
	    node['text'] = product['module_letter']
	    node['id'] = product['id']
	    node['type'] = 'product'
	    ret.append(node)
    return ret


if __name__ == "__main__":
    print get_treeview()
