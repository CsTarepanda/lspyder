import lspyder
from defines import special, rename, register


@special
def define(df, val, globals, locals):
    register(df, lspyder.lspyder_eval(val, globals, locals))


@special
def let(binds, proc, globals, locals):
    for bind in binds:
        locals[bind[0]] = lspyder.lspyder_eval(bind[1], globals, locals)
    return lspyder.lspyder_eval(proc, globals, locals)


@special
@rename("lambda")
def lmd(dargs, proc, globals, locals):
    return eval((
        "lambda %s: lspyder.lspyder_eval(proc, globals=globals, locals=locals())" % ", ".join(dargs)), {"globals": globals, "lspyder": lspyder, "proc": proc})


@special
@rename("set!")
def assignment(var, value, globals, locals):
    defs = locals if var in locals else globals if var in globals else None
    if not defs: raise NameError(var)
    defs[var] = lspyder.lspyder_eval(value, globals, locals)


@special
@rename("and")
def _and(left, right, globals, locals):
    return lspyder.lspyder_eval(left, globals, locals) and lspyder.lspyder_eval(right, globals, locals)


@special
@rename("or")
def _or(left, right, globals, locals):
    return lspyder.lspyder_eval(left, globals, locals) or lspyder.lspyder_eval(right, globals, locals)


@special
class quote:
    def __init__(self, val, globals, locals):
        self.val = val


    @staticmethod
    def tostr(ar):
        if type(ar) == str:
            return ar
        return "(%s)" % str(" ".join(map(quote.tostr, ar)))


    def __str__(self):
        return quote.tostr(self.val)

    
    def get(self):
        return self.val


@special
class quote_sub(quote):
    def __init__(self, *val, globals, locals):
        self.val = val


@special
@rename(".")
def dot(cls, val, globals, locals):
    return getattr(lspyder.lspyder_eval(cls, globals, locals), val)
