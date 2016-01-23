#coding=utf-8
from app.models import db, Manufacturers
from app.utils import *

def create(**kwargs):
    check_field_exists(Manufacturers,kwargs)
    obj = Manufacturers(**kwargs)
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
 
    check_output_field(Manufacturers, output)
    check_order_by(Manufacturers, order_by)
    check_limit(limit)
  
    data = db.session.query(Manufacturers).order_by(order_by).limit(limit).all()
    db.session.close()
    ret = process_result(data, output)
    return ret



def update(**kwargs):
    data = kwargs.get('data', {})
    where = kwargs.get('where', {})
 
    check_update_params(Manufacturers, data, where)
    ret = db.session.query(Manufacturers).filter_by(**where).update(data)
    try:
        db.session.commit()
    except Exception,e:
        raise Exception(e.message.split(")")[1])
    return ret

