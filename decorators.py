from functools import wraps
from blinker import signal

from .base import Call

def event(f):
    EVENT = signal('EVENT')

    @wraps(f)
    def wrapper(*args, **kwargs):
        if EVENT.receivers:
            call = Call(f, args, kwargs)
            EVENT.send(wrapper, event=call)
        return f(*args, **kwargs)
    
    return wrapper
