from functools import wraps


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


# Save references to the builtin functions
builtin_setattr = setattr
builtin_isinstance = isinstance


def custom_setattr(obj, key, value):
    """
    If the object has an Exposer attached, give it the new argument
    before adding it to the object itself.
    """
    if hasattr(obj, "_Exposer__exposer") and not key.startswith("_"):
        if callable(value):
            setattr(getattr(obj, "_Exposer__exposer").func, key, None)
        else:
            setattr(getattr(obj, "_Exposer__exposer").attr, key, None)

    builtin_setattr(obj, key, value)


def custom_isinstance(obj, class_or_tuple):
    """
    If the obj is an Exposer call isinstance on the wrapped object instead of the Exposer.
    """
    if builtin_isinstance(obj, Exposer):
        return isinstance(obj._Exposer__wrapped, class_or_tuple)
    else:
        return builtin_isinstance(obj, class_or_tuple)


# Override the builtin functions
globals()["__builtins__"]["setattr"] = custom_setattr
globals()["__builtins__"]["isinstance"] = custom_isinstance


def wrap_class(cls):
    """
    Override a class' __new__ and __init__ functions to wrap the new object
    with an Exposer before returning it.
    """
    old_new = cls.__new__
    old_init = cls.__init__

    @wraps(old_new)
    def new_new(cls, *args, **kwargs):
        if old_new is object.__new__:
            obj = old_new(cls)
        else:
            obj = old_new(cls, *args, **kwargs)

        old_init(obj, *args, **kwargs)
        return Exposer(obj)

    @wraps(old_init)
    def new_init(self, *args, **kwargs):
        pass

    cls.__new__ = new_new
    cls.__init__ = new_init
