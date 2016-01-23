#!/usr/bin/env python
# coding:utf-8

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class config:
    SECRET_KEY = os.environ.get("SECRET_KDY") or "abcdefg"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "mysql://reboot:123456@127.0.0.1/reboot"
    SQLALCHEMY_POOL_SIZE = 0
    SQLALCHEMY_ZABBIX_API_URL = "http://42.62.73.236/zabbix/api_jsonrpc.php"
    SQLALCHEMY_ZABBIX_API_USER = "Admin"
    SQLALCHEMY_ZABBIX_API_PASS = "zabbix"
    SQLALCHEMY_ZABBIX_API_HEADERS = {'Content-Type': 'application/json-rpc'}

class ProductionConfig(config):
    SQLALCHEMY_DATABASE_URI = "mysql://reboot:123456@127.0.0.1/reboot"
    SQLALCHEMY_POOL_SIZE = 0


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
