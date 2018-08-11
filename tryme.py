from . import e, event


from blinker import signal

class C:
    
    @event
    def f(self, a, b=5):
        return a + b
    
e | C.f
C().f(1, 3)
print(e.log)