#!/usr/bin/env python
# coding:utf-8

from __future__ import unicode_literals
from flask import render_template, request

from . import main
import requests
import json


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
    print ret
    return "111"
#    if str(ret).isdigit():
#        return "操作成功"
#    else:
#        return "操作失败"



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
def api_action(action, params={}):
    url = "http://127.0.0.1:5000/api"
    headers = {"Content-type": "application/json"}
    data = {
        "jsonrpc": 2.0,
        "method" : action,
        "id": 1,
        "auth": None,
        "params": params
    }
    r = requests.post(url, headers=headers ,json=json.dumps(data))
    if str(r.status_code) == "200":
        ret = json.loads(r.content) 
    if ret.has_key('result'):
        return ret['result']
    else:
        return ret['error']








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


