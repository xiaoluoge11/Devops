#!/usr/bin/env python
import socket,psutil,subprocess

def command_result(cmd):
    output = subprocess.Popen("%s" %cmd,shell=True,stdout=subprocess.PIPE)
    ret = output.stdout.readlines()
    return ret 

def get_hostname():
    return socket.gethostname()

def get_ipinfo():
    dict = {}
    data = psutil.net_if_addrs()
    for key in data:
        ip = psutil.net_if_addrs()[key][0][1]
        if ip.startswith("1"):
            dict[key]=ip
    return dict

def get_Memtotal():
    with open('/proc/meminfo') as mem_open:
        a = int(mem_open.readline().split()[1])
        return a / 1025

def get_Disktotal(): 
    dict = {}  
    cmd = "fdisk -l"
    line = command_result(cmd) 
    for i in line:
        disk = i.strip('\n')
        if "/dev" in disk and disk.startswith("Disk"):
            data=disk.split()
            dict[data[1]]=data[2]
    return dict

def get_cpuinfo():
    dict = {}
    cpu_count = psutil.cpu_count()
    cmd = "cat /proc/cpuinfo | grep name"
    ret = command_result(cmd)
    data = list(set(ret))
    dict["cpu_logic_num"]=cpu_count
    dict[data[0].split(":")[0]]=data[0].split(":")[1]
    return dict

def get_hardware(): 
    dict = {}
    cmd = "dmidecode  | grep -A6 'System Information'"
    ret = command_result(cmd)
    del ret[0]
    for i in ret:
        i = i.strip("\n,\t")
        ret_list = i.split(":") 
        dict[ret_list[0]]=ret_list[1]
    return dict

def get_release():
    list = []
    cmd = "dmidecode | grep -i release"
    ret = command_result(cmd) 
    data = ret[0].split(":")[1] 
    rel = data.split("/")
    for i in rel:
         list.append(i.strip('\n,\t')) 
    a,b,c = list
    r_list = [c,a,b]
    return "/".join(r_list)

if __name__ == "__main__":
    print get_release()
