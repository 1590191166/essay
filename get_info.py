#!coding:utf-8
#!
import  logging
import requests
import re
import threading
logging.basicConfig(filename='./debug.log',propagate=0,level=logging.INFO)
input = open('data', 'a+')
list=[]
threads=[]
event=threading.Event()

def find_name(response_str):
    first=re.findall(r'"Account":".*?"',response_str)
    second=re.findall(r':".*?"',str(first))
    third=re.findall(r'".*?"',str(second))
    for i in range(0,len(third)):
        d = re.sub('"', '', third[i])
        list.append(d)

def get_name():
    headers1={
                'Host':'',
                'Accept': '*/*',
                'X-Requested-With':'XMLHttpRequest',
                'Accept-Language':'zh-CN,en-US;q=0.8',  #zh-Hans-CN, zh-Hans; q=0.5
                'Connection':'close'
             }
    for dpt in range(1680,1880):
        url_1 = ''
        r1 = requests.get(url_1, headers=headers1)
        if(len(r1.content)>4):
            find_name(r1.content)
        else:
            pass           #

def get_info(list):
    event.wait()
    url2=''
    for en_name in range(0,len(list)):
        print '[*]'+str(threading.currentThread().getName())+' start '+str(en_name)
        headers2 = {
            'Host': '',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
            'Cookie': '',
            'Connection': 'close'
        }
        r2=requests.get(url2,headers=headers2)
        if(r2.status_code==200 and r2.headers['Content-Type']=='application/json; charset=utf-8'):
            input.write(r2.content+'\n')

def use_threading(list):
    list1=list[0:len(list)/2]
    list2=list[len(list)/2:len(list)]
    t1=threading.Thread(target=get_info,args=(list1,))
    t2=threading.Thread(target=get_info,args=(list2,))
    threads.append(t1)
    threads.append(t2)
    t1.start()
    t2.start()
    for t in threads:
        t.join()

def main():
    get_name()
    global list
    use_threading(list)
    event.set()
    print 'start'

if __name__=='__main__':
    main()