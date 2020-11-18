# -*- coding=utf-8 -*-
import sys
from enum import Enum

'''
commont function used by first and second server
'''

RESP_CODE ={"duplicate_user": "the user has already logged in ",
            "logged_in":"you has logged in "
            }
class RespCode(Enum):
    USER_ALREADY_LOGGED = 1
    LOGGED_IN = 2
    SUCCESS = 3

class Msg():
    def __init__(self, user, msg, session, conn):
        self.user = user
        self.msg = msg      #the whole sent string
        self.conn = conn
        op, sep, mg = msg.partition(" ")
        self.op = op
        self.session = session
        self.data = mg      #the string that remove the operation string

    def send(self,message):
        self.conn.send(message.encode("utf-8"))




def verify_user(username):
    with open("credentials.txt") as file:
        lines = file.readlines()
        for cred in lines:
            name = cred.split(" ")
            if username == name[0]:
                return True
        return False


def verify_pwd(user, pwd):
    with open("credentials.txt") as file:
        lines = file.readlines()
        for cred in lines:
            arr = cred.rstrip("\n").split(" ")
            if user == arr[0] and pwd == arr[1]:
                return True
        return False


def check_user_with_pass(usernanme, password):
    # TODO

    pass


def add_user(username, password):
    pass


def save_file(file):
    pass


def list_cmds():
    return "CRT: Create Thread, LST: List Threads, MSG: Post Message, DLT: Delete Message,\
            RDT: Read Thread, EDT: Edit Message, UPD: Upload File, DWN: Download File, RMV:\
            Remove Thread, XIT: Exit, SHT: Shutdown Server."
