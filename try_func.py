from . import event_log as e, event


from blinker import signal

class C:
    
    @event
    def f(self, a, b=5):
        return a + b
    
with e | C.f:
    C().f(1, 3)
    [(self, a, b)] = e
print(self, a, b)
print('e:', e)