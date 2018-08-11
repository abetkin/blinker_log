from functools import wraps

from .base import Call

def event(f):
    s = Call.get_signal(f)
    
    @wraps(f)
    def wrapper(*args, **kwargs):
        if s.receivers:
            call = Call(f, args, kwargs)
            s.send(None, event=call)
        return f(*args, **kwargs)
    
    return wrapper
