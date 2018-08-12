import inspect
from functools import wraps
from blinker import signal, ANY

from contextlib import contextmanager

EVENT = signal('EVENT')

class Call(dict):

    def __init__(self, func, args, kwargs):
        self.func = func
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
            if param.kind != param.KEYWORD_ONLY:
                yield v

    def __getitem__(self, key):
        if isinstance(key, int):
            return list(self)[key]
        return super().__getitem__(key)
    
    def __getattr__(self, key):
        # enabe dot access
        return self[key]



class EventLog(list):

    def log_event(self, sender, event=None):
        self.append(event)

    
    @contextmanager
    def __or__(self, when):
        if inspect.isfunction(when) and when.__qualname__ == '<lambda>':
            sender = ANY
            def log_event(sender, event=None):
                if when(event):
                    self.log_event(sender, event=event)
        else:
            sender = when
            log_event = self.log_event
        EVENT.connect(log_event, sender=sender)
        yield self
        EVENT.disconnect(log_event, sender=sender)
        self.clear()

    def log(self, obj):
        sender = type(obj)
        EVENT.send(sender, event=obj)