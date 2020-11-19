from sys import path

import exceptions
from common import *
import os.path

CMD_SET = {"CRT", "LST", "MSG", "DLT", "RDT", "EDT", "UPD", "DWN", "RMV", "XIT", "SHT"}

THREAD_DIR = "thread/"


def create_thread(msg):
    title = THREAD_DIR + msg.data
    if path.exists(title):
        msg.conn.send("the thread " + title + " is already exists")
    else:
        with open(title, "w") as file:
            file.writelines([msg.user])


def list_threads(msg):
    arr = os.listdir(THREAD_DIR)
    if len(arr) == 0:
        msg.conn.send("No threads to list ")
    else:
        data = "\n".join(arr)
        msg.conn.send(data)


'''
command:    MSG threadtitle message
filedata:   messagenumber username: message
'''


def post_msg(msg):
    title, sep, content = msg.data.partition(" ")
    if not os.path.exists(THREAD_DIR+title):
        msg.conn.send("error")
    else:
        if os.path.exists(THREAD_DIR+title):
            f = open(THREAD_DIR+title, 'a')
            count = len(open(THREAD_DIR+title, 'r').readlines())
            f.write("\n" + str(count) + " " + msg.user + ":" + content)
            msg.conn.send(msg.user + " message post to %s thread" % title)
        else:
            msg.conn.send(msg.user + " threadTitle %s not exists" % title)

'''
command: DLT threadtitle messagenumber
'''
def del_msg(user, msg):
    title, sep, num = msg.data.partition(" ")
    if not os.path.exists(THREAD_DIR+title):
        msg.conn.send("error")
    else:
        if os.path.exists(THREAD_DIR+title):
            f = open(THREAD_DIR+title, 'a')
            lines = open(THREAD_DIR+title, 'r').readlines()
            del(lines[num])
            f.close()
            new_file = open(THREAD_DIR+title, "w+")
            for line in lines:
                new_file.write(line)
            new_file.close()


def read_thread(user, msg):
    pass

'''
command: EDT threadtitle messagenumber message
'''
def edit_msg(user, msg):
    pass


def upload_file(user, msg):
    pass


def download_file(user, msg):
    pass


def remove_thread(user, msg):
    pass


def exit_forumn(user):
    pass


def shutdown_server(user, msg):
    pass


def run_cmd(msg):
    op = msg.op
    print(msg.user + " issued " + msg.op + "command")
    if op not in CMD_SET:
        raise exceptions.InvalidOperation("invalid operation!")
    if op == "CRT":
        create_thread(msg)
    if op == "LST":
        list_threads(msg)
    if op == "MSG":
        post_msg(msg)
    if op == "DLT":
        del_msg(msg)
    if op == "RDT":
        read_thread(msg)
    if op == "EDT":
        edit_msg(msg)
    if op == "UPD":
        upload_file(msg)
    if op == "DWN":
        download_file(msg)
    if op == "RMV":
        remove_thread(msg)
    if op == "XIT":
        exit_forumn(msg)
    if op == "SHT":
        shutdown_server(msg)
