"""
    dict服务端
    处理请求逻辑
"""
import signal
import sys
from multiprocessing import Process
from socket import *

from operation_db import Database

# 全局变量
HOST = ""
PORT = 2810
ADDR = (HOST, PORT)


# 网络连接
def main():
    # 创建数据库连接对象
    db = Database()

    # 创建TCP套接字
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(ADDR)
    sockfd.listen(3)

    # 处理僵尸进程
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    # 循环等待客户端连接
    print("Listen the port", PORT)
    while True:
        try:
            connfd, addr = sockfd.accept()
            print("Connect from:", addr)
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit("Server Quit")
        except Exception as e:
            print(e)
            continue
        # 创建子进程
        p = Process(target=do_request, args=(connfd, db))
        p.daemon = True
        p.start()


def do_request(connfd, db):
    db.create_cur()
    while True:
        data = connfd.recv(1024).decode()
        if not data:
            return
        print(connfd.getpeername(),":",data)
        if data[0] == "R":
            do_register(connfd,db,data)
        elif data[0] == "L":
            do_login(connfd,db,data)
        elif data[0] == "Q":
            connfd.close()
            db.close()
            return
        elif data[0] == "F":
            do_find(connfd,db,data)
        elif data[0] =="K":
            do_look(connfd,db,data)


def do_register(connfd,db,data):
    tmp = data.split()
    name = tmp[1]
    passwd = tmp[2]

    if db.register(name,passwd):
        connfd.send(b"OK")
    else:
        connfd.send(b"FAIL")

def do_login(connfd,db,data):
    tmp = data.split()
    name = tmp[1]
    passwd = tmp[2]
    if db.login(name,passwd):
        connfd.send(b"OK")
    else:
        connfd.send(b"FAIL")

def do_find(connfd,db,data):
    tmp = data.split()
    name = tmp[1]
    word = tmp[2]
    re =db.do_find(name, word)
    if re:
        connfd.send(re.encode())
    else:
        connfd.send(b"FAIL")

def do_look(connfd,db,data):
    tmp = data.split()
    name = tmp[1]
    re = db.do_look(name)
    string = ""
    for r in re:
        for c in r:
            string += str(c) + "#"
        string += "&"

    if re:
        connfd.send(string.encode())
    else:
        connfd.send(b'Empty')




if __name__ == '__main__':
    main()
