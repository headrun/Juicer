from juicer.utils import *

class login:
    def __init__(self, id, pas):
        import pdb;pdb.set_trace()
        self.id = id
        self.pas = pas

    def check(self, id, pas):
        import pdb;pdb.set_trace()
        print self.id
        if self.id == id and self.pas == pas:
            print "Login success!"

log = login("sravanthi0894@gmail.com", "sravs@5")
log.check(raw_input("Enter Login ID:"),
          raw_input("Enter password: "))
