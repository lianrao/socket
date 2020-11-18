class InvalidOperation(ValueError):
    def __init__(self, arg):
        self.args = arg


class UserExit(UserWarning):
    def __init__(self, arg):
        self.args = arg
