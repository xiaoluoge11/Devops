#coding=utf-8
from app.models import db, Switch, Idc, Cabinet, Status, Manufacturers, User
from app.utils import *

def create(**kwargs):
    check_field_exists(Switch, kwargs)
    check_value_exists(Idc, "id", kwargs.get("idc_id", None))
    check_value_exists(Cabinet, "id", kwargs.get("cabinet_id", None))
    check_value_exists(Status, "id", kwargs.get("status", None))
    check_value_exists(Manufacturers, "id", kwargs.get("manufacturers", None))
    check_value_exists(User, "id", kwargs.get("last_op_people", None))
    obj = Switch(**kwargs)
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
 
    check_output_field(Switch, output)
    check_order_by(Switch, order_by)
    check_limit(limit)
  
    data = db.session.query(Switch).order_by(order_by).limit(limit).all()
    db.session.close()
    ret = process_result(data, output)
    return ret



def update(**kwargs):
    data = kwargs.get('data', {})
    where = kwargs.get('where', {})
 
    check_update_params(Switch, data, where)
    ret = db.session.query(Switch).filter_by(**where).update(data)
    try:
        db.session.commit()
    except Exception,e:
        raise Exception(e.message.split(")")[1])
    return ret

