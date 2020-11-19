import re
import sys
#enter username
def enterUsername():
    username = input("Enter username: ")
    return username

def enterPassword():
    password = input("Enter password: ")
    return password

def checkThreadTitle(cmd):
    msg = cmd[4:]
    title = msg[0:msg.find(" ")]
    test_str = re.search(r"\W", title)
    if test_str != "":
        print("Wrong threadTitle")
        enterCommand

def checkMessageNull(msg):
    message = msg[msg.find(" ") + 1:]
    if message == "":
        print("message cannot be null")
        enterCommand()
def receiveFile(cmd):
    with open('received_file', 'wb') as f:
        print
        'file opened'
        while True:
            print('receiving data...')
            data = s.recv(1024)
            print('data=%s', (data))
            if not data:
                break
            # write data to a file
            f.write(data)

    f.close()

def identifyCommand(cmd):
    flag = cmd[0,3]
    if flag == "CRT":
        msg = cmd[4:]
        test_str = re.search(r"\W", msg)
        if test_str != "":
            print("Wrong command")
            enterCommand()
        else:
            return cmd
    elif flag == "MSG":
        checkThreadTitle(cmd)
        checkMessageNull(cmd[4:])
        return cmd
    #DLT: Delete Message
    #DLT threadtitle messagenumber
    elif flag == "DLT":
        checkThreadTitle(cmd)
        checkMessageNull(cmd[4:])
        return cmd
    #EDT: Edit Message
    #EDT threadtitle messagenumber message
    elif flag == "EDT":
        checkThreadTitle(cmd)
        return cmd
    #LST: List Threads
    elif flag == "LST":
        if len(cmd) >3:
            print("wrong command")
            enterCommand()
        else:
            return cmd
    #RDT: Read Thread
    #RDT threadtitle
    elif flag == "RDT":
        checkThreadTitle(cmd)
        return cmd
    #UPD: Upload file
    #UPD threadtitle filename
    elif flag == "UPD":
        checkThreadTitle(cmd)
        return cmd
    #DWN: Download file
    #DWN threadtitle filename
    elif flag == "DWN":
        checkThreadTitle(cmd)
        receiveFile()
        return cmd
    #RMV: Remove Thread
    #RMV threadtitle
    elif flag == "RMV":
        checkThreadTitle(cmd)
        return cmd
    #XIT: Exit
    #XIT
    elif flag == "XIT":
        sys.exit()
    #SHT: Shutdown
    #SHT admin_password
    elif flag == "SHT":
        pass
    else:
        print("Wrong")
        enterCommand()
    return cmd


def enterCommand():
    command = input("Enter one of the following commands: CRT,\
                        MSG, DLT, EDT, LST, RDT, UPD, DWN, RMV,\
                            XIT, SHT:")
    #input cannot be nan
    if not command:
        print("Input cannot be none")
        enterCommand()
    else:
        identifyCommand(command)

