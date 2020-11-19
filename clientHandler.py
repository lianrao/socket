import re
import sys
import os
from common import ReqData, RespData, REQ_CODE
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
    test_str = re.search(r"\W", title)
    if test_str != "":
        print("Wrong threadTitle")
        enterCommand()

def checkMessageNull(msg):
    message = msg[msg.find(" ") + 1:]
    if message == "":
        print("message cannot be null")
        enterCommand()


def identifyCommand(cmd,s):
    flag = cmd[0,3]
    if flag == "CRT":
        msg = cmd[4:]
        test_str = re.search(r"\W", msg)
        if test_str != "":
            print("Wrong command")
            enterCommand()
        else:
            req = ReqData(REQ_CODE.COMMAND, "CRT", msg)
            s.send(req.serialize())
    elif flag == "MSG":
        checkThreadTitle(cmd)
        msg= cmd[4:]
        threadTitle= msg[0:msg.find(" ")]
        message = msg[msg.find(" ")+1,:]
        checkMessageNull(cmd[4:])
        req = ReqData(REQ_CODE.COMMAND, "MSG", threadTitle + message)
        s.send(req.serialize())
    #DLT: Delete Message
    #DLT threadtitle messagenumber
    elif flag == "DLT":
        checkThreadTitle(cmd)
        msg = cmd[4:]
        threadTitle = msg[0:msg.find(" ")]
        num = msg[msg.find(" ") + 1, :]
        checkMessageNull(cmd[4:])
        req = ReqData(REQ_CODE.COMMAND, "DLT", threadTitle + num)
        s.send(req.serialize())
    #EDT: Edit Message
    #EDT threadtitle messagenumber message
    elif flag == "EDT":
        checkThreadTitle(cmd)
        threadTitle,seq, num, mes = cmd[4:].partition(" ")
        req = ReqData(REQ_CODE.COMMAND, "EDT", threadTitle + num + mes)
        s.send(req.serialize())
    #LST: List Threads
    elif flag == "LST":
        if len(cmd) >3:
            print("wrong command")
            enterCommand()
        else:
            req = ReqData(REQ_CODE.COMMAND, "LST")
            s.send(req.serialize())
    #RDT: Read Thread
    #RDT threadtitle
    elif flag == "RDT":
        checkThreadTitle(cmd)
        req = ReqData(REQ_CODE.COMMAND, "RDT", cmd[4:])
        s.send(req.serialize())
    #UPD: Upload file
    #UPD threadtitle filename
    elif flag == "UPD":
        checkThreadTitle(cmd)
        threadTitle, spec, filename = cmd[4:].partition(" ")
        if os.path.exists(filename):
            with open(filename, "r") as file:
                req = ReqData(REQ_CODE.COMMAND, "UDP", +threadTitle+file.read())
                s.send(req.serialize())
    #DWN: Download file
    #DWN threadtitle filename
    elif flag == "DWN":
        checkThreadTitle(cmd)
        threadTitle, spec, filename = cmd[4:].partition(" ")
        req = ReqData(REQ_CODE.COMMAND, "DWN", +threadTitle + filename)
        s.send(req.serialize())
    #RMV: Remove Thread
    #RMV threadtitle
    elif flag == "RMV":
        checkThreadTitle(cmd)
        req = ReqData(REQ_CODE.COMMAND, "RMV", +cmd[4:])
        s.send(req.serialize())
    #XIT: Exit
    #XIT
    elif flag == "XIT":
        req = ReqData(REQ_CODE.COMMAND, "XIT")
        s.send(req.serialize())
        sys.exit()
    #SHT: Shutdown
    #SHT admin_password
    elif flag == "SHT":
        req = ReqData(REQ_CODE.COMMAND, "SHT",+cmd[4:])
        s.send(req.serialize())
        sys.exit()
    else:
        print("Wrong")
        enterCommand()
    return cmd


def enterCommand(s):
    command = input("Enter one of the following commands: CRT,\
                        MSG, DLT, EDT, LST, RDT, UPD, DWN, RMV,\
                            XIT, SHT:")
    #input cannot be nan
    if not command:
        print("Input cannot be none")
        enterCommand(s)
    else:
        identifyCommand(command,s)

