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
    title = msg.data
    res = None
    if os.path.isfile(DATA_DIR + title):
        res = RespData(RESP_CODE.COMMAND_ERROR,"Thread " + title + " exists")
    else:
        with open(DATA_DIR + title, "w") as file:
            file.writelines([msg.user])
        print("Thread "+ title + " created",flush=True)
        res = RespData(RESP_CODE.COMMAND_SUCCESS,"Thread "+ title + " created")
    return res

'''
res_msg:    
The list of active threads:
3331
9331
'''
def list_threads(msg):
    arr = os.listdir(DATA_DIR)
    arr.remove("credentials.txt")
    res = None
    if len(arr) == 0:
        res = RespData(RESP_CODE.COMMAND_SUCCESS,"No threads to list")
    else:
        data = "\n".join(["The list of active threads"] + arr)
        res = RespData(RESP_CODE.COMMAND_SUCCESS,data)
    return res


'''
command:    MSG threadtitle message
filedata:   messagenumber username: message
message:    Message posted to 3331 thread
'''
def post_msg(msg):
    title, sep, content = msg.data.partition(" ")

    res = None
    if not os.path.exists(DATA_DIR + title):
       res = RespData(RESP_CODE.COMMAND_ERROR,"the thread " + title + " not exsits")
    else:
        f = open(DATA_DIR + title, 'a')
        count = len(open(DATA_DIR + title, 'r').readlines())
        f.write("\n" + str(count) + " " + msg.user + ":" + content)
        res = RespData(RESP_CODE.COMMAND_SUCCESS,msg.user + " message post to %s thread" % title)
    return res

'''
command: DLT threadtitle messagenumber
'''
def del_msg(msg):
    title, sep, num = msg.data.partition(" ")
    res = None
    if not os.path.exists(DATA_DIR+title):
        res = RespData(RESP_CODE.COMMAND_ERROR, "the thread " + title + " not exsits")
    else:
        f = open(DATA_DIR+title, 'a')
        lines = open(DATA_DIR+title, 'r').readlines()
        target_line = lines[int(num)]
        if target_line[target_line.find(" ")+1:target_line.find(":")] == msg.user:
            del(lines[int(num)])
            f.close()
            new_file = open(DATA_DIR+title, "w+")
            for line in lines:
                new_file.write(line)
            new_file.close()
            res = RespData(RESP_CODE.COMMAND_SUCCESS,"Message has been deleted")
        else:
            res = RespData(RESP_CODE.COMMAND_ERROR,"The message belongs to another user and cannot be deleted")
            print("Message cannot be deleted",flush=True)

    return  res



def read_thread(msg):
    title = DATA_DIR+msg.data
    res = None
    if not os.path.exists(title):
        res = RespData(RESP_CODE.COMMAND_ERROR, "the thread " + title + " not exsits")
    else:
        with open(title, "r") as file:
            res = RespData(RESP_CODE.COMMAND_SUCCESS,"\n".join(file.readlines()))
            print("Thread " + title +" read",flush=True)

    return res


'''
command: EDT threadtitle messagenumber message
'''
def edit_msg(msg):
    title, sep1, content = msg.data.partition(" ")
    num,sep2,message = content.partition(" ")
    res = None
    if not os.path.exists(DATA_DIR + title):
        res = RespData(RESP_CODE.COMMAND_ERROR, "the thread " + title + " not exsits")
    else:
        f = open(DATA_DIR + title, 'a')
        lines = open(DATA_DIR + title, 'r').readlines()
        target_line = lines[int(num)]
        if target_line[target_line.find(" ")+1:target_line.find(":")] == msg.user:
            lines[int(num)] = num + " " + msg.user + ":" +message
            f.close()
            new_file = open(DATA_DIR + title, "w+")
            for line in lines:
                new_file.write(line)
            new_file.close()
            res = RespData(RESP_CODE.COMMAND_SUCCESS,"The message has been edited")
            print("Message has been edited",flush=True)
        else:
            res = RespData(RESP_CODE.COMMAND_ERROR,"The message belongs to another user and cannot be edited")
            print("Message cannot be edited",flush=True)

    return res


def upload_file(msg):
    threadTitle, spec, filename = msg.data.partition(" ")
    title = DATA_DIR + threadTitle
    if path.exists(title):
        msg.conn.send("the thread " + title + " is already exists")
    else:
        with open(title, "w") as file:
            file.write(filename)
            print(msg.user+" uploaded a file",flush=True)



def download_file(msg):
    threadTitle, spec, filename = msg.data.partition(" ")
    title = DATA_DIR + threadTitle
    if path.exists(title):
        res = RespData(RESP_CODE.DOWNLOAD_FILE, "DLT", filename)
        msg.conn.send(res.serialize())
        with open(title, "rb") as file:
            data = file.read()
            msg.conn.send(data)

'''
message:    Thread 9331 removed
'''
def remove_thread(msg):
    title = msg.data
    res = None
    if not os.path.exists(DATA_DIR + title):
        res = RespData(RESP_CODE.COMMAND_ERROR, "the thread " + title + " not exsits")
    else:
        with open(DATA_DIR + title,"r") as file:
            user = file.readline()
            user = user.replace("\n","").replace("\r","")
        if user == msg.user:
            os.remove(DATA_DIR + title)
            res = RespData(RESP_CODE.COMMAND_SUCCESS,"The thread has been removed")
            print("Thread "+ title +" removed",flush=True)
        else:
            res = RespData(RESP_CODE.COMMAND_ERROR,"The thread was created by another user and cannot be removed")
            print("Thread " + title +" cannot be removed",flush=True)

    return res



'''
command:  XIT
'''
def exit_forumn(msg):
    res = RespData(RESP_CODE.USER_EXIT,"Goodbye")
    print(msg.user + " exited",flush=True)
    return res

'''
command:    SHT admin_password
'''
def shutdown_server(msg):
    admin_pwd = msg.data
    res = None
    if admin_pwd != "destroy":
        res = RespData(RESP_CODE.COMMAND_ERROR,"Incorrect password")
        print("Incorrect password",flush=True)
        msg.send(res.serialize())
    else:
        shutil.rmtree(DATA_DIR, ignore_errors=True)
        res = RespData(RESP_CODE.SERVER_SHUTDOWN , "Goodbye. Server shutting down")
        print("Server shutting down",flush=True)
        msg.session.add(KILL_SREVER)
    return res


def run_cmd(msg):
    op = msg.op
    res = None
    if op not in CMD_SET:
        res = RespData(RESP_CODE.COMMAND_ERROR," Invalid command")
        return res
    #run the correct command
    print(msg.user + " issued " + msg.op + " command",flush=True)
    if op == "CRT":
       return create_thread(msg)
    if op == "LST":
        return list_threads(msg)
    if op == "MSG":
        return post_msg(msg)
    if op == "DLT":
        return  del_msg(msg)
    if op == "RDT":
        return read_thread(msg)
    if op == "EDT":
        return edit_msg(msg)
    if op == "UPD":
        return upload_file(msg)
    if op == "DWN":
        return download_file(msg)
    if op == "RMV":
        return  remove_thread(msg)
    if op == "XIT":
        return  exit_forumn(msg)
    if op == "SHT":
        return shutdown_server(msg)

