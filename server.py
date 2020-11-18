# -*- coding=utf-8 -*-
import argparse
import sys
import socket
import traceback
import time
from common import *
import threading
from exceptions import *
from cmd import run_cmd


def server(host="", port=12345):
    address = (host, port)
    time_now = time.strftime("%Y-%m-%d %H:%S:%M", time.localtime())

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(address)
    s.listen(1)
    session = dict()

    i = 0
    while True:
        i += 1
        print("Waiting for clients")
        conn, addr = s.accept()
        print("%s Client connected", addr)
        work = myThread(conn, session, i)
        work.start()
        print("session count " + str(len(session)))


class myThread(threading.Thread):  #
    def __init__(self, conn, session, counter):
        threading.Thread.__init__(self)
        self.conn = conn
        self.counter = counter
        self.session = session

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting " + self.name)
        work(self.conn, self.session)
        print("Exiting " + self.name)


def login(user, pwd, data, conn, session):
    if not user:
        user = data
        # check if the same user has already login
        if session[user]:
            resp = (user + " has already logged in")
            print(resp)
            conn.send(resp)
        if verify_user(user):
            conn.send("user".encode("utf-8"))
        return False
    if not pwd:
        if verify_pwd(user, data):
            pwd = data
            conn.send("login".encode("utf-8"))
            print(user + " successfully login")
            session[user] = 1
            return True
        else:
            user = None  # password incorrect , so need reenter the user name
            conn.send("Invalid password")
            print("Incorrect password")
            return False


def work(conn, session):
    user, pwd = None, None

    try:
        print("Got connection from", conn.getpeername())
        while True:
            try:
                buf = conn.recv(1024)
                msg = buf.decode("utf-8")
                if not login(user, pwd, conn, session):
                    continue
                c_msg = Msg(user, msg, session, conn)
                run_cmd(c_msg)

            except InvalidOperation:
                conn.send("Invalid command")
                continue
            except UserExit:
                print(user + "exited")
                conn.close()
                del session[user]
                break
    except:
        pass


def parser_arguments(argv):
    """
    不应该在这里定义，先放在这里
    :param argv:
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("operate", type=str, help="r: 运行抢票程序, c: 过滤cdn, t: 测试邮箱和server酱，server酱需要打开开关")

    return parser.parse_args(argv)


if __name__ == '__main__':
    # args = parser_arguments(sys.argv[1:])
    server()
