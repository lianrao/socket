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


def client(host="localhost", port=12345):
    # 创建套接字
    tcpClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('socket---%s' % tcpClientSocket)
    # 链接服务器
    serverAddr = (host,port)
    tcpClientSocket.connect(serverAddr)
    print('connect success!')

    while True:
        # 发送数据
        sendData = input('please input data:')

        if len(sendData) > 0:
            tcpClientSocket.send(sendData.encode("utf-8"))

        else:
            break

            # 接收数据
        recvData = tcpClientSocket.recv(1024)
        # 打印接收到的数据
        print('the receive message is:%s' % recvData)

    # 关闭套接字
    tcpClientSocket.close()
    print('close socket!')


if __name__ == '__main__':
    # args = parser_arguments(sys.argv[1:])
    client()
