# -*- coding: utf-8 -*-

from os.path import basename
from psutil import net_connections,Process
import socket,threading,time
import crypt

def test():
    for conn in net_connections('all'):
        laddr,raddr,status,pid = conn[3:]
        if not raddr:
            continue
        try:
            filename = basename(Process(pid).exe())
        except:
            pass
        else:
            msg = '''程序文件名：{}\n本地地址：{}\n远程地址：{}\n连接状态：{}'''.format(filename,laddr,raddr,status)
            print(msg)


def search(name):
    ip_temp = []
    for conn in net_connections('all'):
        laddr, raddr, status, pid = conn[3:]
        if not raddr:
            continue
        try:
            filename = basename(Process(pid).exe())
        except:
            pass
        else:
            if filename == name:
                #print('远程地址：'+str(raddr))
                if raddr.ip != '127.0.0.1':
                    ip_temp.append(raddr.ip)
    return ip_temp

def run(exe_list):
    name_en = input('请输入游戏英文名（按回车跳过）：')
    name_zh = input('请输入游戏中文名（按回车默认为{}），注意！这将影响到SSTAP显示的名称！：'.format(str(exe_list)))
    if name_en == '':
        name_en = 'none'
    if name_zh == '':
        name_zh = str(exe_list)
    f = open('{}.rules'.format(str(exe_list)), 'wb')
    f.write('#{},{},0,0,1,0,1,0,By-ip_crawl_tool\n'.format(name_en,name_zh).encode())
    f.close()
    l = local()#添加传输线程
    run_socket = threading.Thread(target=l.update_data,args=(exe_list,name_en,name_zh))#添加传输线程
    run_socket.start()#添加传输线程
    ip_list = []
    print('正在检测{}远程ip,可随时关闭窗口停止终止程序。\n现在你可以打开SSTAP全局，并启动游戏，发现的ip将会自动记录到当前目录的rules文件中'.format(str(exe_list)))
    while True:
        time.sleep(0.2)#加入阻塞降低cpu占用
        for name in exe_list:
            ip_temp = search(name)
            if ip_temp != []:
                for i in ip_temp:
                    if i not in ip_list and ':' not in i:#:用于过滤ipv6
                        ip_list.append(i)
                        print('发现{}新ip'.format(name))
                        print(i)
                        f = open('{}.rules' .format(str(exe_list)), 'ab+')
                        i = i.split('.')
                        i[3] = '0'
                        i = '.'.join(i)
                        if i not in ip_list:#避免重复写入
                            f.write(i.encode() +b'/24\n')
                            ip_list.append(i)
                        f.close()


class local():
    global s
    s = socket.socket()# 创建 socket 对象

    def en_msg(self,text):#消息加密并编码
        temp = crypt.encrypt(text)
        return temp

    def de_msg(self,text):#消息解密并解码
        temp = crypt.decrypt(text)
        return temp

    def rec(self):#循环收取内容
        fulldata = b''
        while True:
            data = s.recv(1024)
            if data == b'$end$':
                break
            else:
                fulldata = fulldata + data
        return fulldata

    def update_data(self,exe_list,name_en,name_zh):
        host = '127.0.0.1'
        port = 12345# 设置端口号
        s.connect((host,port))
        #print(s.recv(1024))
        #print(self.de_msg(self.rec()))
        temp = '#{},{},0,0,1,0,1,0,By-ip_crawl_tool\n'.format(name_en,name_zh)
        while True:
            time.sleep(1)
            f = open("{}.rules".format(str(exe_list)), 'r',encoding='utf-8')
            f_temp = f.read()
            if f_temp != temp:#判断和上次传送结果是否重复，降低服务器压力
                temp = f_temp
                msg = self.en_msg(f_temp)
                s.send(msg)
                f.close()
                continue
        s.close() 


def main():
    #test()
    print('ip_crawl_toolv3.0')
    print('3.0版增加上传规则至服务器进行共享，如不想进行规则上传，请使用2.0版')
    print('快速版规则请访问 http://23.101.14.221:5001')
    a = input('请输入游戏进程名（可启动游戏后在任务管理器 进程 中查询）\n如果有多个进程请使用英文逗号分隔开：')
    exe_list = a.split(',')
    print('将检测以下程序')
    for exe in exe_list:
        print(exe)
    print('请核对名称是否正确，如不正确请重新启动输入')
    run(exe_list)
    
if __name__ == '__main__':
    main()

