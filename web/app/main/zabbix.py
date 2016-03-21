#!/usr/bin/env python
# coding:utf-8

from __future__ import unicode_literals
from flask import render_template, request

from . import main
import requests
import json
import time
from app.common import api_action

"""
    获取zabbix 所有host groups

"""
@main.route("/monitor/ajax/get_zabbix_host_groups",methods=['POST'])
def get_zabbix_host_groups():
    from app.common.zabbix import zabbix_server
    hostgroup = zabbix_server.get_hostgroup()
    return json.dumps(hostgroup)

@main.route("/monitor/ajax/get_zabbix_data_by_group", methods=['POST'])
def get_zabbix_data_by_group():
    from app.common.zabbix import get_zabbix_data,init
    init()
    params = dict(request.form)
    hosts = api_action("server.get",{"output":["id"],"where":{"server_purpose": params["server_purpose"][0],
			    "service_id": params["service_id"][0]			
				}})
    ret = get_zabbix_data(hosts)
    return json.dumps(ret)
