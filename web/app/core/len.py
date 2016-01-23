#coding:utf-8
import os
import imp
import json

class AutoLoad():
    def __init__(self, module_name):
        DIR = os.path.abspath(os.path.dirname(__file__))
        self.moduleDir = os.path.join(os.path.dirname(DIR), "modules")   ###获取模块目录
        self.module_name = module_name
        self.method = None

    def isValidModule(self): 
	"""
	    判断模块是否可以加载
	"""
	return self._load_module()
    def isValidMethod(self, func=None):
	"""
	    判断模块是否有该方法
	"""
        self.method = func
        return hasattr(self.module, self.method)  ###获取可执行之后下一步就是执行
    def getCallMethod(self):
	"""
	    执行的方法,打印输出
	"""
	if hasattr(self.module, self.method):
	     return getattr(self.module, self.method)
	return None
 
    def _load_module(self):
	ret = False
	for filename in os.listdir(self.moduleDir):
	    if filename.endswith('.py'):
		module_name = filename.rstrip('.py') ###删除.py ，比如reboot.py就打印reboot
		if self.module_name == module_name:   ####传入的参数
		    fp, pathname, desc =  imp.find_module(module_name, [self.moduleDir]) ##打开文件
		    if not fp:
			continue   #(要是目录不能打开就继续)
		    try:
			self.module = imp.load_module(module_name, fp, pathname, desc) ##模块加载成功
			ret = True
		    finally:
			fp.close()
		    break
		else:
		    print "没有找到"
	return ret

class Response(object):
    """
	定一个response 像
    """
    def __init__(self):
	self.data = None
	self.errorCode = 0
	self.errorMessage = None

class JsonRpc(object):
    def __init__(self, jsonData):
	self._error = True
	self.jsonData = jsonData
	self._response = {}

    def execute(self):
	if not self.jsonData.get('id', None):
	    self.jsonData['id'] = None   

	if self.validate():
	    params = self.jsonData.get('params', None)
	    auth = self.jsonData.get('auth', None) 
	    module, func = self.jsonData.get("method", "").split(".") ##传入的是reboot.get 那么 module= module,func = get
	    ret = self.callMethod(module, func, params, auth)
	    self.processResult(ret)
	return self._response

    def processResult(self, ret):
	if response.errorCode != 0:
	    self.jsonError(self.jsonData.get('id'), response.errorCode, response.errorMessage)
	else:
	    self._response = {
		"jsonrpc": self.VERSOPM,
		"result": response.data
		"id": self.jsonData.get('id')
	}	

    def callMethod(self, module, func, params, auth):
	module_name = module.lower()   ##全部转换成小写
	func = func.lower()
	response = Response()
	autoload = AutoLoad(module_name)
	
	if not autoload.isValidModule():
	    response.errorCode = 106
	    response.errorMessage = "指定module 不存在"
	    return response
	
	if not autoload.isValidMethod(func):
	    response.errorCode = 107
	    response.errMessage = "{}下没有{}该方法".format(module_name, func)
	    return response
	flage = self.requireAuthentication(module_name, func)
	if flag:
	    if auth is None:
		response.errorCode = 108
		response.errorMessage = "该操作没有提供token"
		return response
	    else:
		pass     ###认证通过后面再修改
	try:
	    called = autoload.getCallMethod()
	    if callable(called):
		response.data = called(**params)   ###这里表示讲called return 的结果直接返回response.data里
	    else:
		response.errorCode = 109
		response.errorMessage = "{}.{}不能调用".format(module_name, func)
		return response
	except Exception, e:
	    response.errorCode = -1
	    response.errorMessage = e.message
	    return response
	return response	


    def validate(self):
	if not self.jsonData.get('jsonrpc', None):
	    self.jsonError(self.jsonData.get('id', None), 101, "参数jsonrpc没有传"
	    return False
	if str(self.jsonData.get("jsonrpc")) != self.version:
	    self.jsonData(self.jsonData.get('id', None), 101, "参数jsonrpc 版本不正确，应该为:{}".format(self.VERSION)	    
	    return False
	if not self.jsonData.get('method', None):
	    self.jsonError(self.jsonData.get('id', 0), 102, "参数method没有传")
	    return False
	if "." not in jsonData.get('method', None):
	    self.jsonError(self.jsonData.get('id', 0), 104, "参数格式不正确")
	    return False

	if not self.jsonData.get('params', None) or not isinstance(self.jsonData.get("params", None), dict)
	    self.Error(self.jsonData.get('id', 0), 103, "params 欧米伽个为dict")
	    return False
	return True
	
    def jsonError(self, id, errno, errmsg):
	self._error = True
	format_err = {
	    "jsonrpc": self.VERSION,
	    "error": errmsg,
	    "errno": errno,
	    "id": id,
        }
	
	self._response = format_err



if __name__ == "__main__":
    data = {
	"jsonrpc": 2.0
	

    }
