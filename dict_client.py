"""
dict 客户端

功能: 根据用户输入,发送请求,得到结果
结构 : 一级界面 --> 注册,登录,退出
      二级界面 --> 查单词  历史记录   注销
请求类型: 注册R　登录L　查单词Q　历史记录H　退出E
"""
from socket import *
from getpass import getpass
import sys

#服务器端地址
ADDR = ('127.0.0.1',8888)
s = socket()
s.connect(ADDR)

def do_register():
    while True:
        name = input("请输入用户名：")
        passwd = getpass()
        passwd1 = getpass("请再次输入密码：")

        if passwd != passwd1:
            print("两次密码不一致")
            continue

        if (" " in name) or (" " in passwd):
            print("用户名密码不可以有空格")
            continue
        # 请求类型
        msg = "R %s %s" % (name,passwd)
        s.send(msg.encode())
        data = s.recv(128).decode() # 有问题
        if data == "OK":
            print("注册成功！")
            login(name) # 二级页面
        else:
            print("注册失败")
        return

def do_query(name):
    while True:
        word = input("Word:")
        if word == "##":
            break
        msg = "Q %s %s" % (name,word)
        s.send(msg.encode())
        data = s.recv(2048).decode()
        print(data)

def do_history(name):
    msg = "H %s" % name
    s.send(msg.encode())
    while True:
        data = s.recv(1024).decode()
        if data == "##":
            break
        print(data)

def login(name):
    while True:
        print("""
        =============Query===============
        1. 查单词　　2.历史记录　　3.注销
        =================================
        """)
        cmd = input("命令：")
        if cmd == '1':
            do_query(name)
        elif cmd == '2':
            do_history(name)
        elif cmd == '3':
            return
        else:
            print("请输入正确选项！")

def do_login():
    name = input("请输入用户名：")
    password = getpass()
    msg = "L %s %s" % (name,password)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == "OK":
        print("登录成功")
        login(name)
    else:
        print("登录失败")

def main():
    while True:
        print("""
        =============Welcome===========
        1. 注册　　　2.　登录　　3. 退出
        ===============================""")
        cmd = input("请输入选项：")
        if cmd == "1":
            do_register()
        elif cmd == "2":
            do_login()
        elif cmd == "3":
            s.send(b'E')
            sys.exit("谢谢使用")
        else:
            print("请输入正确选项")

if __name__ == '__main__':
    main()
