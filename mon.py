#!/usr/bin/env python
#coding: utf-8
import os
import inspect
import time
import urllib, urllib2
import json
import socket
class mon:
    def __init__(self):
        self.data = {}
    def getLoadAvg(self):
        with open('/proc/loadavg') as load_open:
            a = load_open.read().split()[:3]
            return float(a[0])
    def getMemTotal(self):
        with open('/proc/meminfo') as mem_open:
            a = int(mem_open.readline().split()[1])
            return a / 1024
    def getMemUsage(self, noBufferCache=True):
        if noBufferCache:
            with open ('/proc/meminfo') as mem_open:
                T = int(mem_open.readline().split()[1]) #Total
                F = int(mem_open.readline().split()[1]) #Free
                B = int(mem_open.readline().split()[1]) #Buffer
                C = int(mem_open.readline().split()[1]) #Cache
                return (T-F-B-C)/1024
        else:
            with open ('/proc/meminfo') as mem_open:
                a = int(mem_open.readline().split()[1]) - int(mem_open.readline().split()[1])
                return a / 1024
    def getMemFree(self,noBufferCache=True):
        if noBufferCache:
            with open('/proc/meminfo') as mem_open:
                T = int(mem_open.readline().split()[1])
                F = int(mem_open.readline().split()[1])
                B = int(mem_open.readline().split()[1])
                C = int(mem_open.readline().split()[1])
                return (F+B+C)/1024
        else:
            with open('/proc/meminfo') as mem_open:
                mem_open.readline()
                a = int(mem_open.readline().split()[1])
                return a / 1024
    def getDiskTotal(self):
        disk = os.statvfs("/")
        Total = disk.f_bsize * disk.f_blocks / 1024 /1024
        return Total
    def getDiskFree(self):
        disk = os.statvfs("/")
        Free = disk.f_bsize * disk.f_bavail / 1024 / 1024
        return Free
    def getTraffic(self):
        traffic = {}
        f = open("/proc/net/dev")
        lines = f.readlines()
        f.close()
        for line in lines[3:]:
            con = line.split()
            print con[1]
            intf = dict(
                zip(
                    ('ReceiveBytes','TransmitBytes',),
                    (con[1], int(con[8]),)
                    )
                )
            traffic[con[0].split(":")[0]] = intf
        return traffic
    def getHost(self):
        return socket.gethostname()
    def getTime(self):
        return int(time.time())
    def runAllGet(self):
        for fun in inspect.getmembers(self, predicate=inspect.ismethod):
            if fun[0][:3] == 'get':
                self.data[fun[0][3:]] = fun[1]()
        return self.data
if __name__ == "__main__":
        m = mon()
        data = m.runAllGet()
        print data
