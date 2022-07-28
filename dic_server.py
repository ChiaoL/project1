from socket import *
from multiprocessing import Process
import os,signal
from dict_db import Database
from time import sleep
# 服务器地址
ADDR = ("0.0.0.0",8888)
db = Database()

def do_login(c,data):
    name = data.split(" ")[1]
    password = data.split(" ")[2]
    if db.login(name,password):
        c.send(b"OK")
    else:
        c.send(b"Fail")

def do_query(c,data):
    # data = Q name word
    tmp = data.split(" ")
    name = tmp[1]
    word = tmp[2]
    # 插入历史记录
    db.insert_history(name,word)

    mean = db.query(word)
    if mean:
        msg = "%s : %s"%(word,mean)
    else:
        msg = "没有找到该单词"
    c.send(msg.encode())

def do_register(c,data):
    tmp = data.split(" ") #"R %s %s" % (name,passwd)
    name = tmp[1]
    passwd = tmp[2]
    result =  db.register(name,passwd)
    if result:
        c.send(b"OK")
    else:
        c.send(b"Fail")

def do_history(c,data):
    # "H %s" % name
    name = data.split(" ")[1]
    # 10条
    history_list = db.history(name)
    for hist in history_list:
        #hist (name word time)
        msg = "%s  %-16s %s"%hist # - 左对齐
        sleep(0.1)
        c.send(msg.encode())
    sleep(0.1)
    c.send(b"##")

def handle(c):
    while True:
        # 接收消息
        data = c.recv(1024).decode()
        if data[0] == "L":
            do_login(c,data)
        elif data[0] == "Q":
            do_query(c,data)
        elif data[0] == "R":
            do_register(c,data)
        elif data[0] == "H":
            do_history(c,data)
        elif not data or data[0] == 'E':
            os._exit(0)

def main():
    # 创建监听套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen()

    signal.signal(signal.SIGCHLD,signal.SIG_IGN) # 防止孤儿进程
    print("Listen the port 8888....")
    while True:
    # 循环等待客户端连接
        try:
            c,addr = s.accept()
            print("Connect from",addr)
        except KeyboardInterrupt:
            db.close()
            os._exit(0)
        except Exception as e:
            print(e)
            continue
        # 创建新的进程处理请求
        client = Process(target=handle,args=(c,))
        client.daemon = True
        client.start()

if __name__ == "__main__":
    main()

