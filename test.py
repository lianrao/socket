from common import *


def test():
    res = RespData(RESP_CODE.SUCCESS,"test data")
    s = res.serialize()
    print(s)
    u = RespData.unserialize(s)
    print(u.code.name)
    print(u.data)

    req = ReqData(REQ_CODE.PASSWORD_INPUT,"CLS","dlajfljaflj")
    raw = req.serialize()
    print(raw)
    u = ReqData.unserialize(raw)
    print(u.code.name)
    print(u.op + " " + u.data)

if __name__ == '__main__':
    # args = parser_arguments(sys.argv[1:])
    test()