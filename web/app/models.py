#!/usr/bin/env python
# coding:utf-8
from app import db

class User(db.Model):
    __tablename__    = 'user'
    id               = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name             = db.Column(db.String(50), nullable=False)
    username         = db.Column(db.String(50), nullable=False)
    email            = db.Column(db.String(50), nullable=False)
    department_id    = db.Column(db.Integer, index=True,nullable=False)
    is_leader        = db.Column(db.Integer, index=True, default=0)
    phone            = db.Column(db.String(50), index=True, nullable=True)

class Department(db.Model):
    __tablename__    = 'department'
    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    department_name  = db.Column(db.String(50), nullable=False)
    superior         = db.Column(db.Integer, default=0)

class Idc(db.Model):
    __tablename__    = 'idc'
    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name             = db.Column(db.String(10), nullable=False)
    idc_name         = db.Column(db.String(30), nullable=False)
    address          = db.Column(db.String(255), nullable=False)
    phone            = db.Column(db.String(255), nullable=False)
    email            = db.Column(db.String(30), nullable=False)
    user_interface   = db.Column(db.String(50), nullable=False)
    user_phone       = db.Column(db.String(20), nullable=False)
    rel_cabinet_num  = db.Column(db.Integer, nullable=False)
    pact_cabinet_num = db.Column(db.Integer, nullable=False)

class Cabinet(db.Model):
    __tablename__    = 'cabinet'
    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name             = db.Column(db.String(30), nullable=False, unique=True)
    idc_id           = db.Column(db.String(10), index=True, nullable=False)
    power            = db.Column(db.Integer)

class Manufacturers(db.Model):
    __tablename__    = 'manufacturers'
    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name             = db.Column(db.String(50), nullable=False)

class Supplier(db.Model):
    __tablename__    = 'supplier'
    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name             = db.Column(db.String(100), nullable=False)

class Servertype(db.Model):
    __tablename__    = 'servertype'
    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type             = db.Column(db.String(20), nullable=False)
    manufacturers_id = db.Column(db.Integer, nullable=False, index=True)

class Raid(db.Model):
    __tablename__    = 'raid'
    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name             = db.Column(db.String(20), nullable=False)

class Raidtype(db.Model):
    __tablename__    = 'raidtype'
    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name             = db.Column(db.String(50), nullable=False)

class Status(db.Model):
    __tablename__    = 'status'
    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name             = db.Column(db.String(20), nullable=False)

class Product(db.Model):
    __tablename__    = 'product'
    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_name     = db.Column(db.String(20), nullable=False)
    pid              = db.Column(db.Integer, nullable=False, default=0)
    module_letter    = db.Column(db.String(20), nullable=False)
    dev_interface    = db.Column(db.String(200), nullable=False)
    op_interface     = db.Column(db.String(100))

class Power(db.Model):
    __tablename__    = 'power'
    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    server_power     = db.Column(db.Integer, index=True, nullable=False)

class Ipinfo(db.Model):
    __tablename__    = 'ipinfo'
    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip               = db.Column(db.String(20), nullable=False)
    mac              = db.Column(db.String(20), nullable=False)
    device           = db.Column(db.String(20), nullable=False)
    server_id        = db.Column(db.Integer, nullable=False, index=True)
    switch_id        = db.Column(db.Integer, nullable=False, index=True)
    switch_port      = db.Column(db.Integer)

class Server(db.Model):
    __tablename__    = 'server'
    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier         = db.Column(db.Integer, nullable=False, index=True) 
    manufacturers    = db.Column(db.String(50),index=True, nullable=False)
    manufacture_date = db.Column(db.DateTime)
    server_type      = db.Column(db.String(20))
    st               = db.Column(db.String(60), index = True)
    assets_no        = db.Column(db.String(60))
    idc_id           = db.Column(db.String(20), nullable=False, index=True)
    cabinet_id       = db.Column(db.Integer)
    cabinet_pos      = db.Column(db.String(10))
    expire           = db.Column(db.DateTime)
    ups              = db.Column(db.Integer)
    parter           = db.Column(db.String(50)) 
    parter_type      = db.Column(db.String(50))
    server_up_time   = db.Column(db.DateTime)
    os_type          = db.Column(db.String(20))
    os_version       = db.Column(db.String(10))
    hostname         = db.Column(db.String(32), index = True, nullable=False)
    inner_ip         = db.Column(db.String(32), index = True, nullable=False) 
    mac_address      = db.Column(db.String(32))
    ip_info          = db.Column(db.String(300)) 
    server_cpu       = db.Column(db.String(250))
    server_disk      = db.Column(db.String(250)) 
    server_mem       = db.Column(db.String(250)) 
    raid             = db.Column(db.String(10))
    raid_card_type   = db.Column(db.String(50)) 
    remote_card      = db.Column(db.String(32))
    remote_cardip    = db.Column(db.String(32))
    status           = db.Column(db.Integer, nullable=False, index=True)
    remark           = db.Column(db.Text)
    last_op_time     = db.Column(db.DateTime)
    last_op_people   = db.Column(db.Integer)
    monitor_mail_group = db.Column(db.String(32),) 
    service_id       = db.Column(db.Integer, index = True)
    server_purpose   = db.Column(db.Integer, index= True)
    trouble_resolve  = db.Column(db.Integer)
    op_interface_other = db.Column(db.Integer)
    dev_interface    = db.Column(db.Integer)
    check_update_time = db.Column(db.DateTime)
    vm_status        = db.Column(db.Integer, index = True)
    power            = db.Column(db.Integer)
    host             = db.Column(db.Integer, index = True, default=0)

class Managementcardtype(db.Model):
    __tablename__    = 'managementcardtype'
    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    m_type           = db.Column(db.String(50), nullable=False)

    
class Switch(db.Model):
    __tablename__    = 'switch'
    id               = db.Column(db.Integer, primary_key=True, autoincrement=True)
    switch_name      = db.Column(db.String(50), nullable=False)
    switch_type      = db.Column(db.String(50), nullable=False)
    manager_ip       = db.Column(db.String(50), nullable=False)
    category         = db.Column(db.String(50), nullable=False)
    idc_id           = db.Column(db.Integer, nullable=False, index=True)
    cabinet_id       = db.Column(db.Integer, nullable=False, index=True) 
    status           = db.Column(db.Integer, nullable=False)
    expire           = db.Column(db.DateTime)
    remark           = db.Column(db.Text)
    manufacturers    = db.Column(db.Integer, nullable=False, index=True)
    last_op_time     = db.Column(db.DateTime)
    last_op_people   = db.Column(db.Integer, nullable=False)
    switch_port_nums = db.Column(db.Integer) 

class switch_pirpost(db.Model):
    __tablename__       = 'reboot_test'
    id                  = db.Column(db.Integer,primary_key=True)
    purpose             = db.Column(db.String(100),nullable=False,default='')


class test(db.Model):
    __tablename__       = "test"
    id                  = db.Column(db.Integer,primary_key=True)
