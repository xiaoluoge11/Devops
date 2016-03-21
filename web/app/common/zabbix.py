#coding:utf8
from zabbix_client import ZabbixServerProxy
from flask import current_app
from app.models import ZbHost, db, Server
from app.common import api_action

conf = current_app.config


ZABBIX_URL = conf.get("SQLALCHEMY_ZABBIX_API_URL")
ZABBIX_USER = conf.get("SQLALCHEMY_ZABBIX_API_USER")
ZABBIX_PASS = conf.get("SQLALCHEMY_ZABBIX_API_PASS")

class Zabbix():
    def __init__(self):
	self.zb = ZabbixServerProxy(ZABBIX_URL)
	self.zb.user.login(user=ZABBIX_USER, password=ZABBIX_PASS)
    
    def get_hosts(self):
	return self.zb.host.get(output=['hostid','host'])

    def get_interface(self, hostids):
	data = self.zb.hostinterface.get(hostids=hostids, output=['hostid','ip'])
	ret = {}
	for d in data:
	    ret[d['hostid']] = d['ip']
	return ret

    def get_hostgroup(self):
	return self.zb.hostgroup.get(output=['groupid','name'])

    def create_host(self, params):
	return self.zb.host.create(**params) 

    def get_template(self, hostid): 
	ret =  self.zb.template.get(hostids=hostid, output=["templateid","name"])
#	print ret
	return  ret

    def link_template(self, hostid, templateids):
	templates = []
	for id in templateids:
	    templates.append({"templateid": id})
	    print templates
	    print hostid
	try:
	    ret = self.zb.host.update(hostid=hostid, templates=templates)
	    return ret
	except Exception as e:
	    return e.message
    
    def unlink_template(self, hostid, templateid):
	return self.zb.host.update(hostid=hostid, templates_clear = [{"templateid":templateid}])

    def create_maintenance(self, params):
	return self.zb.maintenance.create(**params)

    def get_maintenance(self, params):
	return self.zb.maintenance.get(**params)

    def del_maintenance(self, params):
	return self.zb.maintenance.delete(*params)

    def get_trigger(self, params):
	return self.zb.trigger.get(**params)

    def get_alerts(self, params):
	return self.zb.alert.get(**params)

    def host_status(self, hostid, status):
	return self.zb.host.update(hostid=hostid, status = status)

zabbix_server = Zabbix()



def init():
    db.session.execute("truncate {0}".format(ZbHost.__tablename__))
    init_zabbix() 
    init_cmdb()

def init_cmdb():
    #取host (在server表里)
    hosts = api_action("server.get")
    for h in hosts:
	data = {'cmdb_hostid':h['id']}
	db.session.query(ZbHost).filter_by(ip=h['inner_ip']).update(data)
    db.session.commit()
    
    #更新到cache表， ip
    

def init_zabbix():
    #第一步 取出所有host,要ip,host,id
    zb_hosts =  zabbix_server.get_hosts()
    zb_hosts_interface = zabbix_server.get_interface([z['hostid'] for z in zb_hosts])
#    data = []
    for h in zb_hosts:
	h['ip'] = zb_hosts_interface[h['hostid']]
#	data.append(h)
    ###数据插入数据库
        db.session.add(ZbHost(**h))
    db.session.commit()	

def get_zabbix_data(hosts):
    """
	获取zabbix的机器以及模板信息
	params hosts:
	rreturn
    """
    ret = []
    zabbix_data = db.session.query(ZbHost).filter(ZbHost.cmdb_hostid.in_([h["id"] for h in hosts])).all()
    db.session.close()
    for zb_host in zabbix_data:
	tmp = {}
	tmp['hostname'] = zb_host.host
	tmp['templates'] = zabbix_server.get_template(zb_host.hostid)
        tmp['hostid'] = zb_host.hostid
    	ret.append(tmp)
    return ret

def create_zabbix_host(hostids,groupid):
    servers = db.session.query(Server).filter(Server.id.in_(hostids)).all()
    ret = []
    for host in servers:
	data = {
        "host": host.hostname,
        "interfaces": [
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": host.inner_ip,
                "dns": "",
                "port": "10050"
            }
        ],
        "groups": [
            {
                "groupid": groupid
            }
        ]
       }
    
        ret.append(zabbix_server.create_host(data))
    return ret

def link_template(hostids, templates):
    ret = []
    for hostid in hostids:
	linked_template_ids = [t['templateid'] for t in  zabbix_server.get_template(hostid)]
	linked_template_ids.extend(templates)
	ret.append(zabbix_server.link_template(hostid,linked_template_ids))
    return ret

def create_maintenance(name,hostids,time):
    data =  {
        "name": name,
        "active_since": 1458142800,
        "active_till": 1489678800,
        "hostids": [
            hostids
        ],
        "timeperiods": [
            {
                "timeperiod_type": 0,
                "period": time
            } 
        ]
    }
    ret = zabbix_server.create_maintenance(data)
    return ret

def get_maintenance(hostids):
    data = {
	"output": "extend",
	"hostids":hostids 
	}
    ret = zabbix_server.get_maintenance(data)
    return ret
