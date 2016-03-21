#coding:utf-8
from . import api_action
from app.models import db, GraphiteGroupKey, GraphiteKeys

def get_product():
    products = api_action("product.get", {"output":["module_letter", "id", "pid"]})
    business = [product for product in products if product["pid"] == 0]
    data = []
    for b in business:
	sec_product = get_sec_product(products,b["id"])
	for p in sec_product:
	    performance_data = {}
	    service_id = b["id"]
	    server_purpose = p["id"]
	    performance_data["product"] = "%s/%s"%(b["module_letter"], p["module_letter"])
	    performance_data["hostlist"] = get_hostlist_by_group(service_id, server_purpose)
	    performance_data["item"] = get_graphite_key_by_group(server_purpose)
	    data.append(performance_data)
    return data

def get_graphite_key_by_group(server_purpose):
    graphite_key_ids = db.session.query(GraphiteGroupKey).filter_by(service_id=server_purpose).all()
    key_data = db.session.query(GraphiteKeys).filter(GraphiteKeys.id.in_([graphite.key_id for graphite in graphite_key_ids])).all()
    return [{"key": key.name, "type": key.type, "title": key.title} for key in key_data]

def get_hostlist_by_group(service_id, server_purpose):
    where = {
	"service_id": service_id,
	"server_purpose": server_purpose
	}
    hostlist = api_action("server.get",{"output": ["hostname"], "where": where})
    return [host["hostname"] for host in hostlist]

def get_sec_product(products, pid):
    ret = []
    for product in products:
	if product['pid'] == pid:
	    ret.append(product)
    return ret
