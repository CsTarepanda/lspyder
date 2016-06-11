defines = {}
specials = {}

defines.update(globals()["__builtins__"])


def define(fnc):
    defines[fnc.__name__] = fnc
    return fnc


def rename(name):
    def deco(fnc):
        fnc.__name__ = name
        return define(fnc)
    return deco


def special(fnc):
    specials[fnc.__name__] = fnc
    return fnc


def register(name, value):
    defines[name] = value
