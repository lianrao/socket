from sys import path

import exceptions
from common import *
import os
import shutil

CMD_SET = {"CRT", "LST", "MSG", "DLT", "RDT", "EDT", "UPD", "DWN", "RMV", "XIT", "SHT"}

'''
command:    CRT 3331
'''
def create_thread(msg):
    title = DATA_DIR + msg.data
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
    arr = os.listdir(DATA_DIR)
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
    if not os.path.exists(DATA_DIR + title):
        msg.conn.send("error")
    else:
        if os.path.exists(DATA_DIR + title):
            f = open(DATA_DIR + title, 'a')
            count = len(open(DATA_DIR + title, 'r').readlines())
            f.write("\n" + str(count) + " " + msg.user + ":" + content)
            msg.conn.send(msg.user + " message post to %s thread" % title)
        else:
            msg.conn.send(msg.user + " threadTitle %s not exists" % title)

'''
command: DLT threadtitle messagenumber
'''
def del_msg(msg):
    title, sep, num = msg.data.partition(" ")
    if not os.path.exists(DATA_DIR+title):
        msg.conn.send("error")
    else:
        f = open(DATA_DIR+title, 'a')
        lines = open(DATA_DIR+title, 'r').readlines()
        target_line = lines[num]
        if target_line[target_line.find(" ")+1,target_line.find(":")] == msg.user:
            del(lines[num])
            f.close()
            new_file = open(DATA_DIR+title, "w+")
            for line in lines:
                new_file.write(line)
            new_file.close()
        else: msg.conn.send("no right to delete this message")


def read_thread(msg):
    title = DATA_DIR+msg.data
    if not os.path.exists(title):
        msg.conn.send("error")
    else:
        with open(title, "r") as file:
            msg.conn.send(file.read())


'''
command: EDT threadtitle messagenumber message
'''
def edit_msg(msg):
    title, sep1, num, sep2, message = msg.data.partition(" ")
    if not os.path.exists(DATA_DIR + title):
        msg.conn.send("error")
    else:
        f = open(DATA_DIR + title, 'a')
        lines = open(DATA_DIR + title, 'r').readlines()
        target_line = lines[num]
        if target_line[target_line.find(" ")+1,target_line.find(":")] == msg.user:
            lines[num] = msg.data
            f.close()
            new_file = open(DATA_DIR + title, "w+")
            for line in lines:
                new_file.write(line)
            new_file.close()
        else:
            msg.conn.send("no right to edit this message")


def upload_file(msg):
    threadTitle, spec, filename = msg.data.partition(" ")
    title = DATA_DIR + threadTitle
    if path.exists(title):
        msg.conn.send("the thread " + title + " is already exists")
    else:
        with open(title, "w") as file:
            file.write(filename)
            print(msg.user+" uploaded a file")



def download_file(msg):
    threadTitle, spec, filename = msg.data.partition(" ")
    title = DATA_DIR+threadTitle
    if path.exists(title):
        with open(title,"r") as file:
            msg.conn.send(file.read())

'''
message:    Thread 9331 removed
'''
def remove_thread(msg):
    title = DATA_DIR+ msg.data
    if not os.path.exists(DATA_DIR + title):
        msg.conn.send("error")
    else:
        with open(title,"r") as file:
            user = file.readline
        if user == msg.user:
            os.remove(title)
        else:
            msg.conn.send("no right to remove")



'''
command:  XIT
'''
def exit_forumn(msg):
    res = RespData(RESP_CODE.COMMAND_SUCCESS,"Goodbye")
    msg.send(res.serialize())
    print(msg.user + " exited")

'''
command:    SHT admin_password
'''
def shutdown_server(msg):
    admin_pwd = msg.data
    res = None
    if admin_pwd != "destroy":
        res = RespData(RESP_CODE.COMMAND_ERROR,"Incorrect password")
        print("Incorrect password")
        msg.send(res.serialize())
    else:
        shutil.rmtree(DATA_DIR, ignore_errors=True)
        res = RespData(RESP_CODE.SERVER_SHUTDOWN , "Goodbye. Server shutting down")
        print("Server shutting down")
        msg.session.add(KILL_SREVER)
    return res


def run_cmd(msg,session):
    op = msg.op
    res = None
    if op not in CMD_SET:

        return CmdRspCode.CONTINUE
    #run the correct command
    print(msg.user + " issued " + msg.op + " command")
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
        edit_msg(msg,session)
    if op == "UPD":
        upload_file(msg)
    if op == "DWN":
        download_file(msg)
    if op == "RMV":
        remove_thread(msg)
    if op == "XIT":
        exit_forumn(msg)
        return CmdRspCode.EXIT
    if op == "SHT":
        shutdown_server(msg)
        return CmdRspCode.EXIT

