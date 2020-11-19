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
import os.path
import sys
from concurrent.futures import ThreadPoolExecutor

'''
init the data diretory
'''
serverPort = int(sys.argv[2])
serverAdmin = sys.argv[3]

def init():
    if not os.path.isdir(DATA_DIR):
        os.mkdir(DATA_DIR)


def server(host="", port=12345):
    init()
    address = (host, port)
    time_now = time.strftime("%Y-%m-%d %H:%S:%M", time.localtime())

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(address)
    s.listen(1)
    session = set()

    print("Server started , Waiting for clients")
    th = AcceptThread(s,session)
    th.start()
    while True:
        if KILL_SREVER in session:
            break
        time.sleep(1)
    print("server has shutting down")



class AcceptThread(threading.Thread):
    def __init__(self, socket,session):
        threading.Thread.__init__(self)
        self.socket = socket
        self.session = session
        self.server_down = False

    def run(self):
        ths = []
        while True:
            conn, addr = self.socket.accept()
            th = WorkThread(conn, self.session)
            th.start()
            ths.append(th)

    def shutdown(self):
        self.server_down = True

    def is_shutdown(self):
        return self.server_down

class WorkThread(threading.Thread):  #
    def __init__(self, conn, session):
        threading.Thread.__init__(self)
        self.conn = conn
        self.session = session
        self.server_down = False

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting " + self.name)
        self.work()
        print("Exiting " + self.name)

    def shutdown(self):
        self.server_down = True

    def is_shutdown(self):
        return self.server_down


    def work(self):
        username = None
        loggedin = False
        conn =self.conn
        session = self.session
        try:
            print("Got connection from", conn.getpeername())
            while not self.is_shutdown():
                buf = conn.recv(1024)
                req = ReqData.unserialize(buf)

                res = None
                #input username
                if req.code == REQ_CODE.USERNAME_INPUT:
                    res = verify_user(req,session)
                    #if the username is correct , then store it
                    if res.code == RESP_CODE.USERNAME_IS_CORRECT:
                        username = req.data
                #input password
                elif req.code == REQ_CODE.PASSWORD_INPUT:
                    if not username :
                       res = RespData(RESP_CODE.USERNAME_NOT_INPUT,"please input your username first")
                    else :
                       pwd = req.data
                       res = verify_pwd(username,pwd)
                       if res.code == RESP_CODE.PWD_IS_CORRECT:
                            #if logged in , then add the user to session
                            session.add(username)
                            loggedin = True
                #create a new user with input password
                elif req.code == REQ_CODE.USER_CREATE :
                    res = add_user(username,req.data)
                else:
                    #command process
                    if not loggedin :
                        res = RespData(RESP_CODE.NOT_LOGGED_IN,"please logging in first")
                    else:
                        c_msg = Msg(username , req, session, conn)
                        res = run_cmd(c_msg)
                conn.send(res.serialize())
                if res.code == RESP_CODE.USER_EXIT or res.code == RESP_CODE.SERVER_SHUTDOWN :
                    break
        except:
            print("Unexpected error:", sys.exc_info()[0])
            traceback.print_exc()
        finally:
            if self.server_down :
                print("Server shutting down")
                res = RespData(RESP_CODE.SERVER_SHUTDOWN,"Goodbye. Server shutting down")
                self.conn.send(res.serialize())
            conn.close()
            session.remove(str(username))


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
