import re
import sys
import os
from common import ReqData, RespData, REQ_CODE

def is_cmd_right(cmd,num):
    if not cmd :
        return False
    strs = cmd.split()
    if len(strs) < num :
        return False
    return True


#enter username
def enterUsername():
    username = input("Enter username: ")
    req = ReqData(REQ_CODE.USERNAME_INPUT, REQ_CODE.USERNAME_INPUT, username)
    return(req.serialize())

def enterPassword():
    password = input("Enter password: ")
    req = ReqData(REQ_CODE.PASSWORD_INPUT, REQ_CODE.PASSWORD_INPUT, password)
    return (req.serialize())

def checkThreadTitle(cmd):
    msg = cmd[4:]
    title = msg[0:msg.find(" ")]
    test_str = re.search(r"\w", title)
    if test_str != title:
        print("Wrong threadTitle",flush=True)
        enterCommand()

def checkMessageNull(msg):
    message = msg[msg.find(" ") + 1:]
    if message == "":
        print("message cannot be null",flush=True)
        enterCommand()


def send_cmd(cmd, s):
    flag = cmd[0: 3]
    if flag == "CRT":
        if not is_cmd_right(cmd,2):
            print("Wrong command",flush=True)
            return False
        else:
            req = ReqData(REQ_CODE.COMMAND, "CRT", cmd[4:])
            s.send(req.serialize())
    elif flag == "MSG":
        if not is_cmd_right(cmd,3):
            print("Wrong command",flush=True)
            return False
        msg = cmd[4:]
        req = ReqData(REQ_CODE.COMMAND, "MSG",msg)
        s.send(req.serialize())
    #DLT: Delete Message
    #DLT threadtitle messagenumber
    elif flag == "DLT":
        if not is_cmd_right(cmd,3):
            print("Wrong command",flush=True)
            return False
        msg = cmd[4:]
        req = ReqData(REQ_CODE.COMMAND, "DLT", msg)
        s.send(req.serialize())
    #EDT: Edit Message
    #EDT threadtitle messagenumber message
    elif flag == "EDT":
        if not is_cmd_right(cmd,3):
            print("Wrong command",flush=True)
            return False
        msg = cmd[4:]
        req = ReqData(REQ_CODE.COMMAND, "EDT", msg)
        s.send(req.serialize())
    #LST: List Threads
    elif flag == "LST":
        if len(cmd) > 3:
            print("wrong command",flush=True)
            return False
        else:
            req = ReqData(REQ_CODE.COMMAND, "LST","")
            s.send(req.serialize())
    #RDT: Read Thread
    #RDT threadtitle
    elif flag == "RDT":
        if not is_cmd_right(cmd,2):
            print("Wrong command")
            return False
        req = ReqData(REQ_CODE.COMMAND, "RDT", cmd[4:])
        s.send(req.serialize())
    #UPD: Upload file
    #UPD threadtitle filename
    elif flag == "UPD":
        if not is_cmd_right(cmd,2):
            print("Wrong command")
            return False
        threadTitle, spec, filename = cmd[4:].partition(" ")
        if os.path.exists(filename):
            with open(filename, "r") as file:
                req = ReqData(REQ_CODE.COMMAND, "UDP", threadTitle+file.read())
                s.send(req.serialize())
    #DWN: Download file
    #DWN threadtitle filename
    elif flag == "DWN":
        checkThreadTitle(cmd)
        threadTitle, spec, filename = cmd[4:].partition(" ")
        req = ReqData(REQ_CODE.COMMAND, "DWN", threadTitle + filename)
        s.send(req.serialize())
    #RMV: Remove Thread
    #RMV threadtitle
    elif flag == "RMV":
        if not is_cmd_right(cmd,2):
            print("Wrong command")
            return False
        req = ReqData(REQ_CODE.COMMAND, "RMV", cmd[4:])
        s.send(req.serialize())
    #XIT: Exit
    #XIT
    elif flag == "XIT":
        req = ReqData(REQ_CODE.COMMAND, "XIT","")
        s.send(req.serialize())
    #SHT: Shutdown
    #SHT admin_password
    elif flag == "SHT":
        if not is_cmd_right(cmd,2):
            print("Wrong command")
            return False
        req = ReqData(REQ_CODE.COMMAND, "SHT", cmd[4:])
        s.send(req.serialize())
    else:
        print("Wrong")
        return False
    return True


def enterCommand(s):
    while True:
        command = input("Enter one of the following commands: CRT, MSG, DLT, EDT, LST, RDT, UPD, DWN, RMV, XIT, SHT:")
        if not command:
            print("Input cannot be none")
            continue
        else:
            if send_cmd(str(command), s):
                break


