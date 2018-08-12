from . import event_log as e

class MyObject:
    def __init__(self, **kw):
        self.__dict__.update(kw)

with e | MyObject:
    o = MyObject(a=6)
    e.log(o)

    o = e[-1]
    print(o)

