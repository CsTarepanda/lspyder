defines = {}
symbols = {}
specials = {}

defines.update(globals()["__builtins__"])


def define(fnc):
    defines[fnc.__name__] = fnc
    return fnc


def symbol(name):
    def deco(fnc):
        symbols[name] = fnc
        fnc.__name__ = name
        return fnc
    return deco


def special(fnc):
    specials[fnc.__name__] = fnc
    return fnc


def register(name, value):
    defines[name] = value
