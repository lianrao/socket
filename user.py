
class User:
    def __init__(self,username,pwd):
        self.username = username
        self.pwd = pwd
        self.login = False

    def is_login(self):
        return self.login

    def register(self):
        pass
