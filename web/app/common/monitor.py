#!/usr/bin/python
#coding:utf-8
from . import api_action
import json


class Treeview():
    def __init__(self):
        self.idc_info = api_action("idc.get",{"output":['id', 'name']})
        self.product_info = api_action("product.get",{'output':['id', 'module_letter', 'pid']})
        self.data = []

    def get_child_node(self):
        ret = []
        for p in filter(lambda x:  True if x.get('pid', None) == 0 else False, self.product_info):
            node = {}
            node['text'] = p.get('module_letter', None)
            node['id'] = p.get('id', None)
            node['type'] = 'service'
            node['nodes'] = self.get_grant_node(p.get('id', None))
            ret.append(node)
        return ret


    def get_grant_node(self, pid):
        ret = []
        for p in filter(lambda x :True if x.get('pid', None) == pid else False, self.product_info):
            node = {}
            node['text'] = p.get('module_letter', None)
            node['id'] = p.get('id', None)
            node['type'] = 'product'
            node['pid'] = pid
            ret.append(node)
        return ret

    def get(self,idc):
        child = self.get_child_node()
        if not idc:
            return child
        ret = []
        for idc in self.idc_info:
            node = {}
            node['text'] = idc.get('name', None)
            node['id'] = idc.get('id', 0)
            node['type'] = 'idc'
            node['nodes'] = child
            ret.append(node)
        print ret
        return ret



"""
    获取节点树信息
"""
def get_treeview_data(idc=True):
    treeview = Treeview()
    return treeview.get(idc)





