#!/usr/bin/env python
# coding:utf-8

from __future__ import unicode_literals
from flask import render_template, request

from . import main
import requests
import json
import time
#from app.common.monitor import *
import app.common.tree
from app.models import db, GraphiteKeys, GraphiteGroupKey
from app.common.performance import get_product 

#@main.route('/monitor/zabbix/index',methods=['GET'])
#def monitor_zabbix():
#    #treeview = app.common.monitor.get_treeview_data(idc=False)
#    treeview = []
#    a = app.common.tree.get_treeview()
#    return render_template("monitor/monitor_zabbix.html",treeview=json.dumps(a))

#@main.route("/monitor/zabbix/get/hosts", methods=['POST'])
#def maintor_get_hosts():
#    print request.form
##    ret = [
#	{'id':1, "hostname":"yz-ms-web-01","template":[{"id": 1, "name": "t1"},{"id": 1, "name": "t1"}]}
#        {'id':2, "hostname":"yz-ms-web-02","template":[{"id": 1, "name": "t1"},{"id": 1, "name": "t1"}]}
#    ]
#    return json.dumps(ret)
@main.route('/monitor/zabbix/index',methods=['GET'])
def monitor_zabbix():
    from app.common.zabbix import zabbix_server
    zb_templates = zabbix_server.zb.template.get(output=["templateid", "name"])  
    template = [{"value": zb["templateid"], "label": zb["name"]} for zb in zb_templates]
    treeview = app.common.monitor.get_treeview_data(idc=False)
    return render_template("monitor/monitor_zabbix.html",
			   treeview=json.dumps(treeview),
			   templates=json.dumps(template))
"""
    grphite keys 管理

"""

@main.route('/monitor/graphite/keys',methods=['GET'])
def monitor_graphite_keys():
    graphite_keys=db.session.query(GraphiteKeys).all()
    return render_template("monitor/monitor_graphite_keys.html",graphite_keys=graphite_keys)


"""
    graphite key 与group关联

"""
@main.route('/monitor/graphite/group_keys',methods=['GET'])
def monitor_graphite_group_keys():
    graphite_keys = db.session.query(GraphiteKeys).all()
    db.session.close()
    keys = []
    for s in graphite_keys:
	keys.append({"value": s.id, "text": s.name})
    treeview = app.common.monitor.get_treeview_data(idc=False)
    return render_template("monitor/graphite_group_keys.html",
		 	   treeview = json.dumps(treeview),
			   hosts = json.dumps(keys))

@main.route("/monitor/graphite/keys/add", methods=['POST'])
def monitor_graphite_keys_add():
    if request.method == "POST":
	data = dict(request.form) 
	graphite_key = GraphiteKeys(**data)
	db.session.add(graphite_key)
        try:
	    db.session.commit()
	    if graphite_key.id:
		return "1"
	except Exception, e:
	    return e.message

    return "500"

"""
    ajax 将graphite key关联到group上
"""
@main.route("/monitor/ajax/graphite/add/key/group", methods=["POST"])
def graphite_add_key_to_group():
    if request.method == "POST":
	data = dict(request.form)
	ret = db.session.query(GraphiteGroupKey).filter_by(**data).all()
	if not ret:
	    groupkey = GraphiteGroupKey(**data)
	    db.session.add(groupkey)
	    try:
		db.session.commit()
		if groupkey.id:
		    return "1"
	    except Exception, e:
		return e.message
    return "0"

"""
    ajax 获取指定group的key

"""
@main.route("/monitor/ajax/graphite/group/get_keys", methods=["POST"])
def get_monitor_graphite_group_key():
    if request.method == "POST":
        data = dict(request.form)
	group_keys = db.session.query(GraphiteGroupKey).filter_by(**data).all()
	key_ids = [str(group_key.key_id) for group_key in group_keys]
	return json.dumps(key_ids)
    return json.dumps("")

"""
     ajax删除指定的groupkey:

"""
@main.route("/monitor/ajax/graphite/del/key/group", methods=["POST"])
def del_key_group():
    if request.method == "POST":
	data = dict(request.form)
	#{'service_id': [u'5'], 'key_id': [u'2']}
	key_id = data["key_id"][0]
	print key_id
        db.session.query(GraphiteGroupKey).filter_by(key_id=key_id).delete()
	db.session.commit()
	return "1"
    return "1"


"""
    性能展示

"""

@main.route("/monitor/performance/produce", methods=["GET"])
def monitor_performance_product():
    data = get_product()
    print (data)
    return render_template("monitor/monitor_graphite_product.html",
			   data = json.dumps(data),
			   graphite_api="http://192.168.10.100/render/?")
