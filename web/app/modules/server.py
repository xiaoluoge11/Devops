#coding=utf-8
from app.models import db, Server, Supplier, Raid, Status, User, Product, Idc, Cabinet, Manufacturers, Power
from app.utils import *

def create(**kwargs):
    check_field_exists(Server, kwargs)
    print kwargs.get("raid", None)  
    check_value_exists(Supplier, 'id', kwargs.get("supplier", None))
    check_value_exists(Raid, 'name', kwargs.get("raid", None))
    check_value_exists(Status, 'id', kwargs.get("status", None))
    check_value_exists(User, 'id', kwargs.get("last_op_people", None))
    check_value_exists(Product, 'id', kwargs.get("service_id", None))
    check_value_exists(Product, 'id', kwargs.get("server_purpose", None))
    check_value_exists(User, 'id', kwargs.get("trouble_resolve", None))
    check_value_exists(User, 'id', kwargs.get("op_interface_other", None))
    check_value_exists(User, 'id', kwargs.get("dev_interface", None))
    check_value_exists(Power, 'id', kwargs.get("power", None))

    obj = Server(**kwargs)
    db.session.add(obj)
    try:
	db.session.commit()
    except Exception,e:
	raise Exception(e.message.split(")")[1])
    return obj.id

def get(**kwargs): 
    output = kwargs.get('output', [])
    limit = kwargs.get('limit', 10)
    order_by = kwargs.get('order_by', 'id desc')
 
    check_output_field(Server, output)
    check_order_by(Server, order_by)
    check_limit(limit)
  
    data = db.session.query(Server).order_by(order_by).limit(limit).all()
    db.session.close()
    ret = process_result(data, output)
    return ret



def update(**kwargs):
    data = kwargs.get('data', {})
    where = kwargs.get('where', {})
 
    check_update_params(Server, data, where)
    ret = db.session.query(Server).filter_by(**where).update(data)
    try:
        db.session.commit()
    except Exception,e:
        raise Exception(e.message.split(")")[1])
    return ret

