from . import event_log as e

class Super:
    pass

class MyObject(Super):
    def __init__(self, **kw):
        self.__dict__.update(kw)

e | (lambda obj: isinstance(obj, Super))
o = MyObject(a=6)
e.log(o)

o = e[-1]
print(o)

