#coding:utf-8
import os
import imp
import json

class AutoLoad():
    def __init__(self, module_name):
        DIR = os.path.abspath(os.path.dirname(__file__))
        self.moduleDir = os.path.join(os.path.dirname(DIR), "modules")
        self.module_name = module_name
        self.method = None

    def isValidModule(self):
        return self._load_module()

    def isValidMethod(self, func=None):
        self.method = func
        return hasattr(self.module, self.method)
     
    def getCallMethod(self):
        if hasattr(self.module, self.method):
            return getattr(self.module, self.method)
        return None

    def _load_module(self):
        ret = False
        for filename in  os.listdir(self.moduleDir):
            if filename.endswith(".py"):
                module_name = filename.rstrip(".py")
                if self.module_name == module_name:
                    fp, pathname, desc = imp.find_module(module_name, [self.moduleDir]) ##打开文件返回对象
                    if not fp:
                        continue
                    try:
                        self.module = imp.load_module(module_name, fp, pathname, desc) ##加载这个模块，保存为self.module,判断是否加载成功
                        ret = True
                    finally:
                        fp.close()
                else:
                    print "没有找到"
             
        return ret

class Response(object):
    def __init__(self):
        self.data = None     ##返回数据
        self.errorCode = 0   ##错误码
        self.errorMessage = None   ##错误信息


class JsonRpc(object):
    def __init__(self, jsonData):
        self.VERSION = "2.0"
        self.jsonData = jsonData
        self._error = True
        self._response = {}

    def execute(self):
        """
            执行指定的方法
            返回执行后的结果
            通过执行request方法传入id值确认，执行的次序
        """
        if not self.jsonData.get('id', None):
            self.jsonData['id'] = None

        if self.validate():
            params = self.jsonData.get('params', None)
            auth = self.jsonData.get('auth', None)
            module, func = self.jsonData.get("method", "").split(".")
            ret = self.callMethod(module, func, params, auth)
            self.processResult(ret)
        return self._response

    def callMethod(self, module, func, params, auth):
        """
           加载模块
           验证权限
           执行方法
           返回response
         """ 
	module_name = module.lower()
	func = func.lower()
	response = Response()
	autoload = AutoLoad(module_name)
	
	
        if  not autoload.isValidModule():
            response.errorCode = 106
            response.errorMessage = "指定的模块不存在"
            return response

        if not autoload.isValidMethod(func):
            response.errorCode = 107
            response.errorMessage = "{}下没有{}该方法".format(module_name, func)
            return response

        flag = self.requiresAuthentication(module_name, func)
        if flag:
            if auth is None:
                response.errorCode = 108
                response.errorMessage = "该操作需要提供token"
                return response
            else:
                pass
        try:
            called = autoload.getCallMethod()
            if callable(called):
                response.data = called(**params)
            else:
                response.errorCode = 109
                response.errorMessage = "{}.{} 不能调用".format(module_name, func)
        except Exception, e:
            response.errorCode = -1
            response.errorMessage = e.message
            return response
        return response


    def processResult(self, response):
        if response.errorCode != 0: 
            self.jsonError(self.jsonData.get('id'), response.errorCode, response.errorMessage)
        else:
            self._response = {
                "jsonrpc": self.VERSION,
                "result": response.data,
                "id" : self.jsonData.get('id')
      }

 
    def requiresAuthentication(self, module, func): 
        """
           判断需要执行的API是否需要验证
        """
        if module == "user" and func == "login":
            return False
	if module == "reboot":
	    return False
        return False

    def validate(self):
        """
           验证json,以及json传参数，遍历json数据并验证
        """
        if not self.jsonData.get('jsonrpc', None):
            self.jsonError(self.jsonData.get('id', 0), 101, "参数jsonrpc没有传")
            return False 
        if str(self.jsonData.get("jsonrpc")) != self.VERSION:
            self.jsonError(self.jsonData.get('id', 0), 101, "参数jsonrpc版本不正确，应该为%s"%(self.VERSION))
            return False
        if not self.jsonData.get('method', None):
            self.jsonError(self.jsonData.get('id', 0), 102, "参数method 没有传")
            return False
   
        if "." not in self.jsonData.get('method'):
	    self.jsonError(self.jsonData.get('id', 0), 104, "参数method格式不正确")
	    return False
        if self.jsonData.get("params", None) is None:
            self.jsonError(self.jsonData.get('id', 0), 103, "params is not True")
            return False
	if not isinstance(self.jsonData.get("params"),dict):
	    self.jsonError(self.jsonData.get('id', 0), 105, "params 应该为dict")
	    return False

        return True

    def jsonError(self, id, errno, errmsg):
        self._error = True
        format_err = {
           "jsonrpc": self.VERSION,
           "error": errmsg,
           "errno": errno,
           "id" : id
        }

        self._response = format_err
            

"""  
    101 jsonrpc 版本，或没有个参数
    102, "参数method 没有传"
    103, "params没有传"
    104, "参数method 格式不正确"
    105, "params应该为dict"
    106, "指定的module不存在"
    107， {} 下没有{}该方法
    108, 该操作需要提供token
    109, 不能调用
    -1   api里有except

"""






if __name__ == "__main__":
#    at = AutoLoad("reboot") 
#    at.isValidModule()
#    print at.isValidMethod("get")
#    func = at.getCallMethod()
##    func()
    data = {
        "jsonrpc": 2.0,
        "method": "idc.get",
        "params": {}
        }
    jrpc = JsonRpc(data)
    ret = jrpc.execute()
    print ret
