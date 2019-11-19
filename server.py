import socket,threading,psutil,time
import crypt,sqlite3_mod

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# 创建 socket 对象
host = '0.0.0.0'
port = 12345# 设置端口
s.bind((host, port))# 绑定端口
print(host,port)
c_pool = []#连接池

def en_msg(text):#消息加密并编码
    temp = crypt.encrypt(text)
    return temp

def de_msg(text):#消息解密并解码
    temp = crypt.decrypt(text)
    return temp

def listen():
    s.listen(5)# 等待客户端连接
    while True:
        c, addr = s.accept()# 建立客户端连接。此步骤阻塞
        print ('一个新客户端正在连接，连接对象：'+str(c))
        c_pool.append(c)
        t = threading.Thread(target=message_handle,args=(c,addr))
        t.setDaemon(True)#设置守护线程
        t.start()
        
def message_handle(c,addr):
    global r
    msg = en_msg('服务器连接成功'+str(c))
    c.send(msg)
    time.sleep(0.01)
    c.send(b'$end$')
    while True:
        try:
            r = de_msg(c.recv(1024))
            #print(r)
            #print(addr[0])
            msg = en_msg('已收到信息')
            c.send(msg)
            time.sleep(0.01)
            c.send(b'$end$')#加入尾部识别
        except (ConnectionResetError,BrokenPipeError) as reason:
            c_pool.remove(c)
            #print(c_pool)
            print('连接已关闭'+str(reason))
            print(r)
            sqlite3_mod.insert_data(r,addr[0],int(time.time()))#插入数据库
            break
            #c.close()


if __name__ == '__main__':
    listen()
    #print(msg('服务器连接成功'))
