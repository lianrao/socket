from sys import path

import exceptions
from common import *
import os

CMD_SET = {"CRT", "LST", "MSG", "DLT", "RDT", "EDT", "UPD", "DWN", "RMV", "XIT", "SHT"}

THREAD_DIR = "data/"


'''
command:    CRT 3331
'''
def create_thread(msg):
    title = THREAD_DIR + msg.data
    if os.path.isfile(title):
        msg.send("the thread " + title + " is already exists")
    else:
        with open(title, "w") as file:
            file.writelines([msg.user])
        print(msg.user + "create thread " + title + " success")
        msg.send("create thread " + title + " success")

'''
res_msg:    
The list of active threads:
3331
9331
'''
def list_threads(msg):
    arr = os.listdir(THREAD_DIR)
    if len(arr) == 0:
        msg.send("No threads to list ")
    else:
        data = "\n".join(["The list of active threads"] + arr)
        msg.send(data)


'''
command:    MSG threadtitle message
filedata:   messagenumber username: message
message:    Message posted to 3331 thread
'''
def post_msg(msg):
    title, sep, content = msg.data.partition(" ")
    if not os.path.exists(THREAD_DIR+title):
        msg.send("The thread " + title + " does't exist")
    with open(THREAD_DIR + title,"a+") as f:
        lines = f.readlines()
        msg_num = len(lines)
        line = str(msg_num) + " " + msg.user + ": " + content
        f.writelines([line])
    msg.send("Message posted to " + title + " thread")


'''
command: DLT threadtitle messagenumber
'''
def del_msg(msg):
    pass


def read_thread(msg):
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


'''
message:    Thread 9331 removed
'''
def remove_thread(user, msg):
    pass


def exit_forumn(user):
    pass


def shutdown_server(user, msg):
    pass


def run_cmd(msg):
    op = msg.op
    print(msg.user + " issued " + msg.op + " command")
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
