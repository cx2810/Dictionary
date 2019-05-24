"""
    dict客户端
"""
from getpass import getpass
from socket import *

# 创建网络连接
ADDR = ('176.215.155.118', 2810)
sockfd = socket()
sockfd.connect(ADDR)


def main():
    while True:
        print("""
        ===========Welcom============
           1.注册   2.登录    3.退出
        =============================        
        """)
        cmd = input("输入选项:")
        if cmd == "1":
            do_register()
        elif cmd == "2":
            do_login()
        elif cmd == "3":
            sockfd.send(b"E")
            sockfd.close()
            return
        else:
            print("请输入正确选项")


def do_register():
    while True:
        name = input("Name:")
        passwd = getpass()
        passwd_again = getpass()
        # passwd = input("Passwd:")
        # passwd_again = input("Passwd_again:")
        if " " in name or " " in passwd:
            print("用户名或密码不能有空格")
            continue
        if passwd != passwd_again:
            print("两次密码不一致")
            continue

        mgs = f"R {name} {passwd}"
        # 发送请求
        sockfd.send(mgs.encode())
        # 接收反馈
        data = sockfd.recv(128).decode()
        if data == "OK":
            print("注册成功")
            login(name)
        else:
            print("注册失败")
        return


def do_login():
    name = input("User:")
    # passwd = getpass()
    passwd = input("Passwd:")
    mgs = f"L {name} {passwd}"
    sockfd.send(mgs.encode())
    # 等待反馈
    data = sockfd.recv(128).decode()
    if data == "OK":
        print("登录成功")
        login(name)
    else:
        print("登录失败")


def login(name):
    while True:
        print("""
        ============Query============
          1.查单词  2.历史记录  3.注销
        =============================        
        """)
        cmd = input("输入选项:")
        if cmd == "1":
            do_find(name)
        elif cmd == "2":
            do_look(name)
        elif cmd == "3":
            return
        else:
            print("请输入正确选项")


def do_find(name):
    """
        循环查找单词,输入'##'退出查询,
    :param name:
    :return:
        找到单词，返回单词解释
        找不到单词，返回'Not Found'
    """
    while True:
        word = input("输入查找单词:")
        if word == "##":  # 结束单词查询
            break
        msg = f"Q {name} {word}"
        sockfd.send(msg.encode())
        data = sockfd.recv(2048).decode()
        if data == "FAIL":
            print("Not Found", word)
        else:
            print(word, ":", data)


def do_look(name):
    mgs = f"H {name}"
    sockfd.send(mgs.encode())
    data = sockfd.recv(128).decode()
    if data == "OK":
        while True:
            data = sockfd.recv(4096).decode()
            if data == "##":
                break
            print(data)
    else:
        print("用户%s没有查找记录" % name)


if __name__ == '__main__':
    main()
