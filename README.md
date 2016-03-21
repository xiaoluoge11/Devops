# Devops
主要是基于python的一些脚本互相交流学习<br/>
开源项目CMDB加以改进，以API接口的方式进行调用，代码持续更新中<br/>
CMDB运维平台已初步完成，基于api接口调用，模仿zabbix 的API调用方式<br/>
所有的操作都记忆api与模块方便调用<br/>
脚本定时收集硬件更新到前端已完成<br/>
CMDB开发已完成。实现半自动化的方式，一些人为信息需要人工通过API方式录入<br/>
硬件资产信息每隔10分钟采集一次更新到数据库并展示<br/>

##zabbix;
已完成CMDB同步主机到zabbix<br/>
zabbix批量模板绑定<br/>
zabbix 添加维护周期<br/>
zabbix 获取历史数据<br/>

##graphite;
根据业务自定义出图，通业务再一组图形前端展示<br/>
