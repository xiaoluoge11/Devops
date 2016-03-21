#!/usr/bin/env python
# coding:utf-8

from __future__ import unicode_literals
from flask import render_template, request

from app.models import db, ZbHost, Server, Maintenance 
from . import main
import requests
import json
import time
from app.common import api_action 
import app.common.monitor
@main.route("/resource/index", methods=['GET'])
def resource_index():
    return render_template("resource/index.html")



@main.route('/resource/idc', methods=['GET'])
def resource_idc():
    return render_template("resource/server_add_idc.html")

@main.route("/resource/server_list", methods=['GET'])
def resource_server_list():
    servers = api_action("server.get")
    return render_template("resource/server_list.html",
                           servers=servers)

@main.route("/resource/server_asses", methods=['GET'])
def resource_server_asses():
    servers = api_action("server.get")
    return render_template("resource/server_asses.html",
                           servers=servers)



@main.route("/resource/server_add", methods=['GET'])
def resource_server_add():
    # 获取idc信息
    idc_info = api_action("idc.get", {"output": ['name', 'id']})
    status = api_action("status.get", {"outout":["id", "name"]})
    servertype = api_action("servertype.get", {"outout":["id", "type"]})
    cabinet = api_action("cabinet.get", {"outout":["id", "name"]})
    manufacturers = api_action("manufacturers.get", {"outout":["id", "name"]})
    ret = api_action("product.get", {"output":["id","service_name", "pid"]})
    product = [item for item in ret if item['pid'] == 0]
    powers = api_action("power.get")
    raids = api_action("raid.get")
    raidtype = api_action("raidtype.get")
    managementcardtype = api_action("managementcardtype.get")
    supplier = api_action("supplier.get")
    return render_template("resource/server_add.html",
                           idc_info=idc_info,
                           status = status,
                           manufacturers = manufacturers,
                           products = product,
                           powers = powers,
                           raids = raids,
                           raidtypes = raidtype,
                           managementcardtypes = managementcardtype,
                           suppliers = supplier,
			   servertype = servertype,
			   cabinets = cabinet)


@main.route("/resource/server_doadd", methods=['POST'])
def resource_server_doadd():
    print dict(request.form)
    ret = api_action("server.create", dict(request.form))
    if str(ret).isdigit():
        return "操作成功"
    else:
        return "操作失败"


@main.route("/resource/server_sysinfo", methods=['POST'])
def resource_server_sysinfo():
    data = request.json
    print data
    ret = api_action("server.create", data) 
#    if str(ret).isdigit():
#        return "操作成功"
#    else:
#        return "操作失败"
    print ret
    return "1"



"""
    添加IDC页面
"""
@main.route("/resource/server_idc_add", methods=['GET'])
def resource_server_idc_add():
    return render_template("resource/server_add_idc.html")

"""
    执行IDC添加
"""
@main.route("/resource/server_idc_doadd", methods=['POST'])
def resource_server_idc_doadd():
    data = dict(request.form)
    ret = api_action("idc.create", data)
    if str(ret).isdigit():
        return "操作成功"
    else:
        return "操作失败"


"""
    添加服务器状态
"""
@main.route("/resource/server_status_add", methods=['GET'])
def resource_server_status_add():
    return render_template("resource/server_add_status.html")


"""
    执行服务器状态添加
"""
@main.route("/resource/server_status_doadd", methods=['POST'])
def resource_server_status_doadd():
    ret = api_action("status.create", dict(request.form))
    if str(ret).isdigit():
        return "操作成功"
    else:
        return "操作失败"


"""
    添加制造商
"""
@main.route("/resource/server_manufacturers_add", methods=['GET'])
def resource_server_manufacturers_add():
    return render_template("resource/server_add_manufacturers.html")

"""
    执行制造商添加
"""
@main.route("/resource/server_manufacturers_doadd", methods=['POST'])
def resource_server_manufacturers_doadd():
    ret = api_action("manufacturers.create", dict(request.form))
    if str(ret).isdigit():
        return "操作成功"
    else:
        return "操作失败"

"""
    添加服务器类型
"""
@main.route("/resource/server_servertype_add", methods=['GET'])
def resource_server_servertype_add():
    manufacturers = api_action("manufacturers.get", {"outout":["id", "name"]})
    return render_template("resource/server_add_servertype.html",
                           manufacturers=manufacturers)

"""
    执行服务器类型添加
"""
@main.route("/resource/server_servertype_doadd", methods=['POST'])
def resource_server_servertype_doadd():
    ret = api_action("servertype.create", dict(request.form))
    if str(ret).isdigit():
        return "操作成功"
    else:
        return "操作失败"



"""
    添加业务线,产品线
"""
@main.route("/resource/server_product_add", methods=['GET'])
def resource_server_product_add():
    ret = api_action("product.get")
    product = [item for item in ret if item['pid'] == 0]
    return render_template("resource/server_add_product.html",
                           products = product)



"""
    执行业务线,产品线的添加
"""
@main.route("/resource/server_product_doadd", methods=['POST'])
def resource_server_product_doadd():
    ret = api_action("product.create", dict(request.form))
    print ret
    if str(ret).isdigit():
        return "操作成功"
    else:
        return ret




"""
    添加机柜
"""
@main.route("/resource/server_cabinet_add", methods=['GET'])
def resource_server_cabinet_add():
    idcs = api_action("idc.get", {"output":['id', 'name']})
    powers = api_action("power.get")
    return render_template("resource/server_add_cabinet.html",
                           idcs = idcs,
                           powers = powers)



"""
    执行机柜的添加
"""
@main.route("/resource/server_cabinet_doadd", methods=['POST'])
def resource_server_cabinet_doadd():
    ret = api_action("cabinet.create", dict(request.form))
    print ret
    if str(ret).isdigit():
        return "操作成功"
    else:
        return ret




"""
    添加电源功率
"""
@main.route("/resource/server_power_add", methods=['GET'])
def resource_server_power_add():
    return render_template("resource/server_add_power.html")



"""
    执行电源功率添加
"""
@main.route("/resource/server_power_doadd", methods=['POST'])
def resource_server_power_doadd():
    ret = api_action("power.create", dict(request.form))
    if str(ret).isdigit():
        return "操作成功"
    else:
        return ret



"""
    添加raid信息
"""
@main.route("/resource/server_raid_add", methods=['GET'])
def resource_server_raid_add():
    return render_template("resource/server_add_raid.html")

"""
    执行raid信息添加
"""
@main.route("/resource/server_raid_doadd", methods=['POST'])
def resource_server_raid_doadd():
    ret = api_action("raid.create", dict(request.form))
    if str(ret).isdigit():
        return "操作成功"
    else:
        return ret


"""
    添加raid信息
"""
@main.route("/resource/server_raidcardtype_add", methods=['GET'])
def resource_server_raidcardtype_add():
    return render_template("resource/server_add_raidcardtype.html")


"""
    执行raid信息添加
"""
@main.route("/resource/server_raidcardtype_doadd", methods=['POST'])
def resource_server_raidcardtype_doadd():
    ret = api_action("raidtype.create", dict(request.form))
    if str(ret).isdigit():
        return "操作成功"
    else:
        return ret



"""
    添加远程管理卡信息信息
"""
@main.route("/resource/server_managementcardtype_add", methods=['GET'])
def resource_server_managementcardtype_add():
    return render_template("resource/server_add_managementcardtype.html")

"""
    执行远程管理卡添加
"""
@main.route("/resource/server_managementcardtype_doadd", methods=['POST'])
def resource_server_managementcardtype_doadd():
    ret = api_action("managementcardtype.create", dict(request.form))
    if str(ret).isdigit():
        return "操作成功"
    else:
        return ret


"""
    添加供应高
"""
@main.route("/resource/server_supplier_add", methods=['GET'])
def resource_server_supplier_add():
    return render_template("resource/server_add_supplier.html")


"""
    执行添加供应高
"""
@main.route("/resource/server_supplier_doadd", methods=['POST'])
def resource_server_supplier_doadd():
    ret = api_action("supplier.create", dict(request.form))
    if str(ret).isdigit():
        return "操作成功"
    else:
        return ret


"""
    工具函数 , 执行API操作
"""
#def api_action(action, params={}):
#    url = "http://127.0.0.1:5000/api"
#    headers = {"Content-type": "application/json"}
#    data = {
#        "jsonrpc": 2.0,
#        "method" : action,
#        "id": 1,
#        "auth": None,
#        "params": params
#    }
#    r = requests.post(url, headers=headers ,json=json.dumps(data))
#    if str(r.status_code) == "200":
#        ret = json.loads(r.content) 
#    if ret.has_key('result'):
#        return ret['result']
#    else:
#        return ret['error']








"""
    ajax操作
    根据制造商,获取服务器类型
"""
@main.route("/resource/ajax/get_server_type", methods=['GET'])
def resource_ajax_get_servertype():
    if request.method == 'GET':
        manufacturers_id = int(request.args.get('manufacturers_id',0))
        if manufacturers_id:
            servertypes = api_action("servertype.get",{})
            ret = [item for item in servertypes if item['manufacturers_id'] == manufacturers_id]
            return json.dumps(ret)
    return ""


"""
    ajax 操作
    要怕一级业务线,获取它的二级业务线
"""
@main.route("/resource/ajax/get_server_product", methods=['GET'])
def resource_ajax_get_product():
    if request.method == 'GET':
        pid = int(request.args.get('pid',0))
        if pid:
            servertypes = api_action("product.get",{"output": ["id", "service_name", "pid"]})
            ret = [item for item in servertypes if item['pid'] == pid]
            return json.dumps(ret)
    return ""

"""
    ajax 操作
    根据idc条件,获取机柜信息,
"""
@main.route("/resource/ajax/get_cabinet", methods=['GET'])
def resource_ajax_get_cabinet():
    if request.method == 'GET':
        idc_id = request.args.get('idc_id',0)
        if idc_id:
            cabinets = api_action("cabinet.get", {"output":['id', 'name', "idc_id"]})
            ret = [item for item in cabinets if item['idc_id'] == idc_id]
            return json.dumps(ret)
    return ''


"""
    采集数据并入库

"""
@main.route("/resource/server/auto/collection", methods=['POST'])
def resource_server_collection():
    # 1、接收传过来的主机数据
    # 2 更新数据
    # 3 插入数据
    if request.method == "POST":
	data = dict(request.form)
	data['check_update_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
	print data
	ret = api_action("server.update", {"where":{'uuid': data['uuid']}, 'data': data})
	print ret
	if int(ret) == 0:
	    api_action("server.create", data)
        return "成功更新"

"""
    cache文件

"""
#@main.route("/cache", methods=['GET'])
#def cache():
##    from app.common.zabbix import init_zabbix,init_cmdb
#    init_cmdb() 
#    return ''

'''
   获取不在zabbix里的所有主机

'''
@main.route("/resource/monitor/ajax/get_sync_zabbix_hosts", methods=['POST'])
def get_sync_zabbix_host():
    from app.common.zabbix import init
    init()
 
    zabbix_hosts = db.session.query(ZbHost).all()
    db.session.close()
    #不在cache表里的数据
#    select * from server where id not in zabbix_hosts_cmdb_id
    hostid = [zb.cmdb_hostid for zb in zabbix_hosts]  #在缓存表里的服务器id
    servers = db.session.query(Server).filter(~Server.id.in_(hostid)).all() ##~表示取反    
    return json.dumps([{"hostname":s.hostname, "id":s.id} for s in servers]) 

#@main.route("/monitor/ajax/get_zabbix_host_groups",methods=['POST'])
#def get_zabbix_host_groups():

"""
同步主机到zabbix

"""
@main.route("/resource/monitor/ajax/sync_host_to_zabbix", methods=['POST'])
def sync_host_to_zabbix():
    #接收参数
    #hostid groupid
    if request.method == "POST":
	from app.common.zabbix import create_zabbix_host
	params = dict(request.form)
	hostids = params['hostids'][0].split(',')
	ret = create_zabbix_host(hostids=params['hostids'][0].split(','),groupid=params['groupid'][0])
	if len(ret) == len(hostids):
	    return '1'
	else:
	    return json.dumps(ret)	
	
    return "500"

@main.route("/resource/server_group", methods=["GET"])
def resource_server_group():
    #获取所有的主机
#    import app.common.monitor
    servers = api_action("server.get",{})
    host = []
    for s in servers:
	if not s['service_id'] and not s['server_purpose']:
	    host.append({"value":s['id'],"text": s['hostname']}) 
    treeview = app.common.monitor.get_treeview_data(idc=False)
#    print treeview 
    return render_template("resource/server_hostgroup.html",
			   treeview=json.dumps(treeview),
			   host=json.dumps(host))

"""
    ajax 把机器加到指定分组

"""
@main.route("/resource/ajax/host_to_hostgroup",methods=['POST'])
def host_to_hostgroup():
    params = dict(request.form)
    print params
    where = {'id':params['id'][0]}
    data = {
	"server_purpose": params['server_purpose'][0],
	"service_id": params['service_id'][0],
	"check_update_time": time.strftime("%Y-%m-%d %H:%I:%S", time.localtime(time.time()))
     }
    print data
    ret = api_action("server.update",{"where":where,"data": data})
    if ret == 1:
	return str(ret)
    return "500"

"""
    ajax 获取分组里的机器
"""
@main.route("/resources/ajax/gethostsbyhostgroup",methods=['POST'])
def get_hosts_bygroup():
    data = dict(request.form)
    where = {
	"server_purpose": data['server_purpose'][0],
        "service_id": data['service_id'][0],
	}
    ret = api_action("server.get",{"where":where})
    hosts = []
    for r in ret:
	hosts.append({"value": r['id'], "text": r['hostname']})
    return json.dumps(hosts)
   

"""
    ajax把机器从分组中删除

"""
@main.route("/resources/ajax/del_host_from_group", methods=['POST'])
def del_host_from_group():
    data = dict(request.form)
    server_id = data['id'][0]
    ret = api_action("server.update",{"where":{"id": server_id},"data":{
        "server_purpose": None,
        "service_id": None
	}})
    if ret == 1:
	return str(ret)
    return "500"

"""
   绑定zabbix模板 

"""

@main.route("/monitor/ajax/link_zabbix_template", methods=['POST'])
def link_zabbix_template():
    from app.common.zabbix import link_template
    if request.method == "POST":
	#1、获取前端数据
        params = dict(request.form)
        #{'hostids': [u'10106'], 'template_ids': [u'10001']}
	hostids = params['hostids'][0].split(',')
	template_ids = params['template_ids'][0].split(',')
	ret_data = link_template(hostids, template_ids)	
	error = None
	for r in ret_data:
	    try:
		hostids.remove(r['hostids'][0])
	    except Exception, e:
		error = e.message
	if not hostids:
	    return "1"
	else:
	    return error
    return "500"

"""
    解绑模板

"""
@main.route("/monitor/ajax/unlink_zabbix_template", methods=['POST'])
def unlink_zabbix_template():
    from app.common.zabbix import zabbix_server
    if request.method == "POST":
        #1、获取前端数据
        params = dict(request.form)
	hostid = params['hostid'][0]
	templateid = params['templateid'][0]
        ret = zabbix_server.unlink_template(hostid, templateid)
	if ret:
	    return "1"
	else:
	    return json.dumps(ret)
    return "500" 
 

"""
    维护周期
"""
@main.route("/zabbix_maintenance", methods=['GET'])
def get_zabbix_maintenance():
    hostlist = []
    servers = api_action("server.get",{"output":["hostname"]})
    data = Maintenance.query.all()
    return render_template("monitor/zabbix_maintenance.html",hostlist=servers,data=data)

"""
    接收页面传过来的ajax产生，添加维护周期
"""
@main.route("/monitor/zabbix/maintenance/add", methods=["POST"])
def maintenance_add():
    from app.common.zabbix import zabbix_server
    from app.common.zabbix import create_maintenance
    data = dict(request.form)
    #{'name': [u'mail.shihuasuan.com'], 'time': [u'1']}
    maintenance_name = data['maintenance_name'][0]
    hostname = data["name"][0]
    time_to_go = data["time"][0]
    time_long = int(time_to_go) * 60 *60 
    ret = zabbix_server.get_hosts()
    for host in ret:
	if hostname == host["host"]:
	    hostids = host["hostid"]
	    try:
	        result = create_maintenance(maintenance_name,hostids,time_long) 
		result_data = zabbix_server.host_status(hostid=hostids, status="1")
	    except:
		return "check your maintenance_name"
	    update_time = time.strftime("%Y-%m-%d %H:%I:%S", time.localtime(time.time()))
	    add_data = {"maintenance_name":maintenance_name, "hostname":hostname, "maintenance_time":time_to_go,"update_time":update_time}
	    obj = Maintenance(**add_data)
	    db.session.add(obj)
	    try:
        	db.session.commit()
    	    except Exception,e:
        	raise Exception(e.message.split(")")[1]) 
	    return "1"
    return "200"

"""
    根据页面传过来的信息，删除维护周期
"""
@main.route("/maintenance/del/", methods=["GET"])
def maintenance_del(id=None):
    try:
        hostlist = []
        from app.common.zabbix import zabbix_server 
        from app.common.zabbix import get_maintenance
        id = request.args.get("id")
        data = Maintenance.query.filter(Maintenance.id == id).first()  
        hostname = data.hostname  
        ret = zabbix_server.get_hosts()
        for host in ret:
	    if hostname == host["host"]:
	        hostids=host["hostid"]
	        ret = get_maintenance(hostids)
                maintenanceid = ret[0]['maintenanceid']
                ret = zabbix_server.del_maintenance([maintenanceid])
		result_data = zabbix_server.host_status(hostid=hostids, status="0")
		print result_data
		try: 
	            db.session.query(Maintenance).filter_by(id=id).delete()
                    db.session.commit()	
		except Exception,e:
		    raise e.message
	        servers = api_action("server.get",{"output":["hostname"]})
                data = Maintenance.query.all()
	        return render_template("monitor/zabbix_maintenance.html",hostlist=servers,data=data) 
        return "200"
    except:
	servers = api_action("server.get",{"output":["hostname"]})
        data = Maintenance.query.all()
	return render_template("monitor/zabbix_maintenance.html",hostlist=servers,data=data)

@main.route("/get_alerts", methods=["GET"])
def zabbix_alerts_get():
    from app.common.zabbix import get_alerts
    data = {
        "output": "extend",
        "actionids": 7
    }
    ret = zabbix_server.get_alerts(data)
    print ret
    return ""
