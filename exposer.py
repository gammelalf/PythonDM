class PointBack:
    """
    It's basicly a namespace which just gives any actual request for a function
    or method back to the ´master´ object.
    """
    
    def __init__(self, master):
        self._master = master

    def __getattribute__(self, key):
        if key.startswith("_"):
            return super().__getattribute__(key)
        else:
            return getattr(super().__getattribute__("_master"), key)

    def __repr__(self):
        return "\n".join([key for key in self.__dir__() if not key.startswith("_")])


class Exposer(object):
    """
    Wrapper function for anything the ordinary interactive user is allowed to see.

    Any function or attribute just points to the orignal object.
    And there are the ´func´ and ´attr´ functions for lookup and tab completion
    of possible functions and arguments the original object provides.
    """

    def __init__(self, wrapped):
        self.__wrapped = wrapped
        wrapped.__exposer = self
        super().__setattr__("func", PointBack(self))
        super().__setattr__("attr", PointBack(self))
        for key in wrapped.__dir__():
            if key.startswith("_"):
                continue
            elif callable(getattr(self.__wrapped, key)):
                setattr(self.func, key, None)
            else:
                setattr(self.attr, key, None)

    def __setattr__(self, key, value):
        if key.startswith("_"):
            super().__setattr__(key, value)
        else:
            setattr(self.__wrapped, key, value)

    def __getattr__(self, key):
        return getattr(self.__wrapped, key)

    def __repr__(self):
        return str(self.__wrapped)


builtin_setattr = setattr


def custom_setattr(obj, key, value):
    if hasattr(obj, "_Exposer__exposer") and not key.startswith("_"):
        if callable(value):
            setattr(getattr(obj, "_Exposer__exposer").func, key, None)
        else:
            setattr(getattr(obj, "_Exposer__exposer").attr, key, None)
    builtin_setattr(obj, key, value)


globals()["__builtins__"]["setattr"] = custom_setattr
