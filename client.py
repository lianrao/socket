
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
#serverAddr = "127.0.0.1"
#serverPort = 12345

serverAddr = str(sys.argv[2])
serverPort = int(sys.argv[3])
#import clientService as cs


def main():
    print(">python Client %s %d"% (serverAddr, serverPort))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((serverAddr, serverPort))
        username = input("Enter username: ")
        req = ReqData(REQ_CODE.USERNAME_INPUT,REQ_CODE.USERNAME_INPUT,username)
        s.send(req.serialize())
        password = input("Enter password: ")
        req = ReqData(REQ_CODE.PASSWORD_INPUT,REQ_CODE.PASSWORD_INPUT,password)
        s.send(req.serialize())
        while True:
            msg = s.recv(1024)
            enterCommand(s)
            resp = RespData.unserialize(msg)
            if resp.data[0] == 1:
                with open(resp.data[1:resp.data.find(" ")], 'wb') as f:
                    f.write(resp.data[resp.data.find(" ") + 1:])
            else:
                print(resp.data)




if __name__ == "__main__":
    main()
