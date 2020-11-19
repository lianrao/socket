# -*- coding=utf-8 -*-
import sys
from enum import Enum
from enum import auto

'''
commont function used by first and second server
'''

# data directory
DATA_DIR = "data/"

# data seperator
DATA_SEP = ": "

KILL_SREVER = "__kill_server__"

class RESP_CODE(Enum):
    USER_ALREADY_LOGGED = auto()
    LOGGED_IN = auto()
    NOT_LOGGED_IN = auto()
    SUCCESS = auto()

    USERNAME_IS_CORRECT = auto()
    USERNAME_IS_WRONG = auto()
    USERNAME_NOT_INPUT = auto()

    PWD_IS_CORRECT = auto()
    PWD_IS_WRONG = auto()


    COMMAND_SUCCESS = auto()
    COMMAND_ERROR = auto()

    USER_EXIT = auto()

    SERVER_SHUTDOWN = auto()


class REQ_CODE(Enum):
    USERNAME_INPUT = auto()
    PASSWORD_INPUT = auto()
    USER_CREATE = auto()
    COMMAND = auto()  # other command


class RespData:
    def __init__(self, code, data):
        self.code = code
        self.data = data

    def serialize(self):
        return (self.code.name + DATA_SEP + self.data).encode("utf-8")

    @classmethod
    def unserialize(cls, raw_data):
        data = raw_data.decode("utf-8")
        code, sep, content = data.partition(DATA_SEP)
        return cls(RESP_CODE[code], content)


class ReqData:
    def __init__(self, code, op, data):
        self.op = op  # operation char
        self.code = code
        self.data = data

    '''
    encode the data with utf-8 raw data to send with connection
    '''

    def serialize(self):
        return (self.code.name + DATA_SEP + self.op + DATA_SEP + self.data).encode("utf-8")

    '''
    get the raw data from connection , then trasform to RequestData class
    '''

    @classmethod
    def unserialize(cls, raw_data):
        d = raw_data.decode("utf-8")
        #remove newline char
        d = d.replace('\n','').replace('\r','')
        code, sep, content = d.partition(DATA_SEP)
        op, sep, data = content.partition(DATA_SEP)
        #remove left and right space
        data = data.strip()
        return cls(REQ_CODE[code], op, data)


class CmdRspCode(Enum):
    CONTINUE = 1  # client continue run
    EXIT = 2  # client exit
    SHUTDOWN = 3  # server shutdown


class Msg():
    def __init__(self, user, req, session, conn):
        self.user = user
        self.conn = conn
        self.op = req.op
        self.session = session
        self.data = req.data  # the string that remove the operation string
        self.req = req

    def send(self, message):
        self.conn.send(message)


def verify_user(req, session):
    # check if the same user has already login

    #check user whether already logged in
    username = req.data
    res = RespData(RESP_CODE.USERNAME_IS_WRONG,username + " not exists.")
    if username in session:
        conten = username + " has already logged in"
        res = RespData(RESP_CODE.USER_ALREADY_LOGGED, conten)
        print(conten)
        return res

    #check username whetheh is correct
    with open(DATA_DIR + "credentials.txt") as file:
        lines = file.readlines()
        for cred in lines:
            name = cred.split(" ")
            if username == name[0]:
                res = RespData(RESP_CODE.USERNAME_IS_CORRECT,username + " is old user")
                break
    return res



def verify_pwd(username, pwd):
    res = None
    with open(DATA_DIR + "credentials.txt") as file:
        lines = file.readlines()
        for cred in lines:
            arr = cred.rstrip("\n").split(" ")
            if username == arr[0] and pwd == arr[1]:
                res = RespData(RESP_CODE.PWD_IS_CORRECT, username + " is logged in")
                break
    if not res:
        res = RespData(RESP_CODE.PWD_IS_WRONG,"Invalid password")
    return  res


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
