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
        th = myThread(conn, session, i)
        th.start()
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


def loggedin(cred, data, conn, session):
    if not cred["user"]:
        cred["user"] = data
        # check if the same user has already login
        if cred["user"] in session:
            resp = (cred.user + " has already logged in")
            print(resp)
            conn.send(resp)
        if verify_user(cred["user"]):
            conn.send("user".encode("utf-8"))
        return False
    if not cred["pwd"]:
        if verify_pwd(cred["user"], data):
            cred["pwd"] = data
            cred["logged"] = True
            conn.send("login".encode("utf-8"))
            print(cred["user"] + " successfully login")
            session[cred["user"]] = 1
            return True
        else:
            cred["user"] = None  # password incorrect , so need reenter the user name
            conn.send("Invalid password".encode("utf-8"))
            print("Incorrect password")
            return False


def work(conn, session):

    creds = {"user":None,"pwd":None,"logged":False}

    try:
        print("Got connection from", conn.getpeername())
        while True:
            try:
                buf = conn.recv(1024)
                msg = buf.decode("utf-8")
                if not creds["logged"]:
                    loggedin(creds, msg, conn, session)
                    continue
                c_msg = Msg(creds["user"], msg, session, conn)
                run_cmd(c_msg)

            except InvalidOperation:
                conn.send("Invalid command")
                continue
            except UserExit:
                print(creds["user"] + "exited")
                conn.close()
                del session[creds["user"]]
                break
    except :
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc()



def parser_arguments(argv):
    """
    不应该在这里定义，先放在这里
    :param argv:
    :return:
    """
    parser = argparse.ArgumentParser()

    return parser.parse_args(argv)


if __name__ == '__main__':
    # args = parser_arguments(sys.argv[1:])
    server()
