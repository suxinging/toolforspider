#!/usr/bin/python
#coding:utf-8

'''
Created on 2015年10月29日

@author: sherwel
'''

import sys
import nmap   
import os
import time
import SQLTool
import config
from numpy.numarray.numerictypes import IsType
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入   
class SniffrtTool(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        try:
            self.nma = nmap.PortScanner()                                     # instantiate nmap.PortScanner object

            self.params='-A -P0   -Pn  -sC  -R -v  -O '

        except nmap.PortScannerError:
            print('Nmap not found', sys.exc_info()[0])

        except:
            print('Unexpected error:', sys.exc_info()[0])
        self.config=config.Config
        self.sqlTool=SQLTool.DBmanager()
    def scaninfo(self,hosts='localhost', port='', arguments=''):
        orders=''
        if port!='':
            orders+=port
        else :
            orders='1'
        try:

            print '我在这里49'
            scan_result=self.nma.scan(hosts=hosts,ports= orders,arguments=self.params+arguments)
            print '我在这里50'
            return self.callback_result( scan_result) 


        except nmap.PortScannerError,e:
            print e
            print '我在这里55'
            return ''

        except:
            print('Unexpected error:', sys.exc_info()[0])
            print '我在这里59'
            return ''
    def callback_result(self,scan_result):
        print '我在这里61'
        print '——————'
        tmp=scan_result
        print scan_result
        for i in tmp['scan'].keys():
            host=i
            result=''
            try:
                result =  u"ip地址:%s 主机名:%s  ......  %s\n" %(host,tmp['scan'][host]['hostname'],tmp['scan'][host]['status']['state'])
                self.sqlTool.connectdb()
           
                if 'osclass' in tmp['scan'][host].keys():
                    result +=u"系统信息 ： %s %s %s   准确度:%s  \n" % (str(tmp['scan'][host]['osclass']['vendor']),str(tmp['scan'][host]['osclass']['osfamily']),str(tmp['scan'][host]['osclass']['osgen']),str(tmp['scan'][host]['osclass']['accuracy']))
                temphosts=str(host)
                tempvendor=str(tmp['scan'][host]['osclass'].get('vendor','null'))
                temposfamily=str(tmp['scan'][host]['osclass'].get('osfamily','null'))
                temposgen=str(tmp['scan'][host]['osclass'].get('osgen','null'))
                tempaccuracy=str(tmp['scan'][host]['osclass'].get('accuracy','null'))
                localtime=str(time.strftime("%Y-%m-%d %X", time.localtime()))
                temphostname=str(tmp['scan'][host].get('hostname','null'))
                tempstate=str(tmp['scan'][host]['status'].get('state','null'))
#                 print temphosts,tempvendor,temposfamily,temposgen,tempaccuracy,localtime
                self.sqlTool.replaceinserttableinfo_byparams(self.config.iptable, ['ip','vendor','osfamily','osgen','accurate','updatetime','hostname','state'], [(temphosts,tempvendor,temposfamily,temposgen,tempaccuracy,localtime,temphostname,tempstate)])         
                if 'tcp' in  tmp['scan'][host].keys():
                    ports = tmp['scan'][host]['tcp'].keys()

                    for port in ports:
#                     portinfo = " port : %s  name:%s  state : %s  product : %s version :%s  script:%s \n" %(port,tmp['scan'][host]['tcp'][port].get('name',''),tmp['scan'][host]['tcp'][port].get('state',''),   tmp['scan'][host]['tcp'][port].get('product',''),tmp['scan'][host]['tcp'][port].get('version',''),tmp['scan'][host]['tcp'][port].get('script',''))
                        tempport=str(port)
                        tempportname=str(tmp['scan'][host]['tcp'][port].get('name',''))
                        tempportstate=str(tmp['scan'][host]['tcp'][port].get('state',''))
                        tempproduct=str(tmp['scan'][host]['tcp'][port].get('product',''))
                        tempportversion=str(tmp['scan'][host]['tcp'][port].get('version',''))
                        tempscript=str(tmp['scan'][host]['tcp'][port].get('script',''))
                        self.sqlTool.replaceinserttableinfo_byparams(self.config.porttable, ['ip','port','timesearch','state','name','product','version','script'], [(temphosts,tempport,localtime,tempportstate,tempportname,tempproduct,tempportversion,tempscript)])         


                elif 'udp' in  tmp['scan'][host].keys():
                    ports = tmp['scan'][host]['udp'].keys()
                    for port in ports:
#                         portinfo = " port : %s  name:%s  state : %s  product : %s version :%s  script:%s \n" %(port,tmp['scan'][host]['udp'][port].get('name',''),tmp['scan'][host]['udp'][port].get('state',''),   tmp['scan'][host]['udp'][port].get('product',''),tmp['scan'][host]['udp'][port].get('version',''),tmp['scan'][host]['udp'][port].get('script',''))
#                         result = result + portinfo
                        tempport=str(port)
                        tempportname=str(tmp['scan'][host]['udp'][port].get('name',''))
                        tempportstate=str(tmp['scan'][host]['udp'][port].get('state',''))
                        tempproduct=str(tmp['scan'][host]['udp'][port].get('product',''))
                        tempportversion=str(tmp['scan'][host]['udp'][port].get('version',''))
                        tempscript=str(tmp['scan'][host]['udp'][port].get('script',''))
                        self.sqlTool.replaceinserttableinfo_byparams(self.config.porttable, ['ip','port','timesearch','state','name','product','version','script'], [(temphosts,tempport,localtime,tempportstate,tempportname,tempproduct,tempportversion,tempscript)])         

            except Exception,e:
                print e
            except IOError,e:
                print '错误IOError'+str(e)
            except KeyError,e:
                print '不存在该信息'+str(e)
            finally:
#                 print result
                return str(scan_result)
    def scanaddress(self,hosts=[], ports=[],arguments=''):
        temp=''
        for i in range(len(hosts)):
            print '我在这里asd'
            if len(ports)<=i:
                print '我在这里123'
                temp+=self.scaninfo(hosts=hosts[i],arguments=arguments)
            else:
                print '我在这里126'
                temp+=self.scaninfo(hosts=hosts[i], port=ports[i],arguments=arguments)
        return temp
    def isrunning(self):
        return self.nma.has_host(self.host)
def callback_resultl(host, scan_result):
    print scan_result
    print '——————'
    tmp=scan_result
    result=''

    try:
        result =  u"ip地址:%s 主机名:%s  ......  %s\n" %(host,tmp['scan'][host]['hostname'],tmp['scan'][host]['status']['state'])
        if 'osclass' in tmp['scan'][host].keys():
            result +=u"系统信息 ： %s %s %s   准确度:%s  \n" % (str(tmp['scan'][host]['osclass']['vendor']),str(tmp['scan'][host]['osclass']['osfamily']),str(tmp['scan'][host]['osclass']['osgen']),str(tmp['scan'][host]['osclass']['accuracy']))
        if 'tcp' in  tmp['scan'][host].keys():
            ports = tmp['scan'][host]['tcp'].keys()
            for port in ports:

                portinfo = " port : %s  name:%s  state : %s  product : %s version :%s  script:%s \n" %(port,tmp['scan'][host]['tcp'][port]['name'],tmp['scan'][host]['tcp'][port]['state'],   tmp['scan'][host]['tcp'][port]['product'],tmp['scan'][host]['tcp'][port]['version'],tmp['scan'][host]['tcp'][port]['script'])
                print portinfo
                result+=  portinfo
        elif 'udp' in  tmp['scan'][host].keys():
            ports = tmp['scan'][host]['udp'].keys()
            for port in ports:
                portinfo = " port : %s  name:%s  state : %s  product : %s  version :%s  script:%s \n" %(port,tmp['scan'][host]['udp'][port]['name'],tmp['scan'][host]['udp'][port]['state'],   tmp['scan'][host]['udp'][port]['product'],tmp['scan'][host]['udp'][port]['version'],tmp['scan'][host]['udp'][port]['script'])
                result += portinfo
    except Exception,e:
        print e
    except IOError,e:
        print '错误IOError'+str(e)
    except KeyError,e:
        print '不存在该信息'+str(e)
    finally:
            return result
    
"""
def callback_resultl(host, scan_result):
    print scan_result
    print scan_result['scan']
    f = open('abc.xml','w+')
    f.write(str(scan_result))
    f.close()
"""


order=' -P0 -sV -sC  -sU  -O -v  -R -sT  '
orderq='-A -P0   -Pn  -sC  -p '


if __name__ == "__main__":   

    temp=SniffrtTool()
#     hosts=['www.cctv.com','localhost','www.baidu.com']'www.cctv.com' www.vip.com
    hosts=['www.cctv.com']
    temp.scanaddress(hosts,ports=['443-500'],arguments='')


            
        


#     print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))


