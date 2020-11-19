# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 02:46:16 2020

@author: jiyut
python3
"""
import socket
import sys

from clientHandler import enterCommand
serverAddr = "127.0.0.1"
serverPort = 12345

#serverAddr = str(sys.argv[2])
#serverPort = int(sys.argv[3])
#import clientService as cs





def main():
    print(">python Client %s %d"% (serverAddr, serverPort))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((serverAddr, serverPort))
        username = input("Enter username: ")
        password = input("Enter password: ")
        s.send(username+" "+password)
        while True:
            msg = s.recv(1024)

            msg = enterCommand(msg)
            s.send(msg)



if __name__ == "__main__":
    main()
