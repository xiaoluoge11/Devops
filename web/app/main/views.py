#!/usr/bin/env python
# coding:utf-8
from __future__ import unicode_literals
from flask import render_template

from . import main
from flask import request
import json
from app.core.base import JsonRpc
from datetime import date, datetime  

@main.route('/', methods=['GET','POST'])
def index():
    return render_template("dashboard.html")


@main.route('/api', methods=['GET','POST'])
def api():
    allowed_content = {
        'application/json-rpc': "json-rpc",
        'application/json': "json-rpc",
     }
    if allowed_content.get(request.content_type, None):
        jsonData = json.loads(request.get_json())
        jsonrpc = JsonRpc(jsonData)
        ret = jsonrpc.execute()
        return json.dumps(ret,cls=CJsonEncoder)
    else:
        return "404",404


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
