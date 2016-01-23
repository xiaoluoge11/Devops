#coding=utf-8
from app.models import db, Idc
from app.utils import *

def create(**kwargs):
    check_field_exists(Idc,kwargs)
    obj = Idc(**kwargs)
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
 
    check_output_field(Idc, output)
    check_order_by(Idc, order_by)
    check_limit(limit)
  
    data = db.session.query(Idc).order_by(order_by).limit(limit).all()
    db.session.close()
    ret = process_result(data, output)
    return ret



def update(**kwargs):
    data = kwargs.get('data', {})
    where = kwargs.get('where', {})
 
    check_update_params(Idc, data, where)
    ret = db.session.query(Idc).filter_by(**where).update(data)
    try:
        db.session.commit()
    except Exception,e:
        raise Exception(e.message.split(")")[1])
    return ret

