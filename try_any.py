from . import event_log as e
from blinker import ANY

class MyObject:
    def __init__(self, **kw):
        self.__dict__.update(kw)

class O:
    pass

with e | ANY:
    e.log(MyObject(a=6))
    e.log(O())

    print(e)

