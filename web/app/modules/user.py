#coding=utf-8
from app.models import db, User, Department
from app.utils import *

def create(**kwargs):
    check_field_exists(User,kwargs)
    check_value_exists(Department, "id", kwargs.get("department_id", None))
    obj = User(**kwargs)
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
 
    check_output_field(User, output)
    check_order_by(User, order_by)
    check_limit(limit)
  
    data = db.session.query(User).order_by(order_by).limit(limit).all()
    db.session.close()
    ret = process_result(data, output)
    return ret



def update(**kwargs):
    data = kwargs.get('data', {})
    where = kwargs.get('where', {})
 
    check_update_params(User, data, where)
    ret = db.session.query(User).filter_by(**where).update(data)
    try:
        db.session.commit()
    except Exception,e:
        raise Exception(e.message.split(")")[1])
    return ret

