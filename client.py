
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 02:46:16 2020

@author: jiyut
python3
"""
import socket
import sys
from common import *

from clientHandler import enterCommand
serverAddr = "127.0.0.1"
serverPort = 12346

# serverAddr = str(sys.argv[2])
# serverPort = int(sys.argv[3])
#import clientService as cs


def login(socket):
    # login
    s = socket
    while True:
        username = input("Enter username: ")
        req = ReqData(REQ_CODE.USERNAME_INPUT, REQ_CODE.USERNAME_INPUT.name, username)
        s.send(req.serialize())
        m = s.recv(1024)
        res = RespData.unserialize(m)
        print(res.data)

        if res.code == RESP_CODE.NEW_USER:
            pwd = input("pls Enter the new password")
            req = ReqData(REQ_CODE.USER_CREATE, REQ_CODE.USER_CREATE.name, username + " " + pwd)
        else:
            password = input("Enter password: ")
            req = ReqData(REQ_CODE.PASSWORD_INPUT, REQ_CODE.PASSWORD_INPUT.name, password)
        s.send(req.serialize())
        m = s.recv(1024)
        res = RespData.unserialize(m)
        print(res.data)
        if res.code == RESP_CODE.LOGGED_IN:
            break


def main():
    print(">python Client %s %d"% (serverAddr, serverPort))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect((serverAddr, serverPort))
        login(s)

        #run command
        while True:

            enterCommand(s)
            msg = s.recv(1024)
            resp = RespData.unserialize(msg)
            if resp.code == RESP_CODE.NOT_LOGGED_IN:
                login(s)
            if resp.code == RESP_CODE.USER_EXIT :
                print("Gooodbye")
                break

            if resp.data[0] == 1:
                with open(resp.data[1:resp.data.find(" ")], 'wb') as f:
                    f.write(resp.data[resp.data.find(" ") + 1:])
            else:
                print(resp.data)




if __name__ == "__main__":
    main()
