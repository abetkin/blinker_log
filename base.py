import inspect
from functools import wraps
from blinker import signal


class Call(dict):

    def __init__(self, func, args, kwargs):
        sig = self.signature = inspect.signature(func)
        bound_args = sig.bind(*args, **kwargs).arguments
        
        for name, parameter in sig.parameters.items():
            if name in bound_args:
                self[name] = bound_args[name]
            elif parameter.default is not inspect._empty:
                self[name] = parameter.default

    def __iter__(self):
        for k, v in self.items():
            param = self.signature.parameters[k]
            if not param.kind == param.KEYWORD_ONLY:
                yield v

    def __getitem__(self, key):
        if isinstance(key, int):
            return list(self)[key]
        return super().__getitem__(key)
    
    @classmethod
    def get_signal(cls, func):
        qualname = f"{func.__module__}.{func.__qualname__}"
        return signal(qualname)



class EventLog:

    def __init__(self):
        self.log = []
    
    def __iter__(self):
        return iter(self.log[-1])
    
    def __getitem__(self, key):
        return self.log[-1][key]
    
    def log_event(self, sender, event=None):
        self.log.append(event)

    def __or__(self, func):
        s = Call.get_signal(func)
        s.connect(self.log_event)
        return self
