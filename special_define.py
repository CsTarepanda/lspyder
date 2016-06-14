import lspyder
from defines import special, rename, register


@special
def define(df, val, locals):
    register(df, lspyder.lspyder_eval(val, locals))


@special
def let(binds, proc, locals):
    for bind in binds:
        locals[bind[0]] = lspyder.lspyder_eval(bind[1], locals)
    return lspyder.lspyder_eval(proc, locals)


@special
@rename("lambda")
class Lambda:
    def __init__(self, args, proc, locals):
        self.args = args if type(args) == list else [args]
        self.proc = proc
        self.scope = locals

    def __call__(self, *args):
        scope = dict(self.scope)
        scope.update(dict(zip(self.args, args)))
        return lspyder.lspyder_eval(self.proc, scope)
# def lmd(dargs, proc, locals):
#     def fnc(*args):
#         print(locals)
#         locals.update(dict(zip(dargs, args)))
#         return lspyder.lspyder_eval(proc, locals)
#     return fnc


@special
@rename("set!")
def assignment(var, value, locals):
    defs = locals if var in locals else globals if var in globals else None
    if not defs: raise NameError(var)
    defs[var] = lspyder.lspyder_eval(value, locals)


@special
@rename("and")
def _and(left, right, locals):
    return lspyder.lspyder_eval(left, locals) and lspyder.lspyder_eval(right, locals)


@special
@rename("or")
def _or(left, right, locals):
    return lspyder.lspyder_eval(left, locals) or lspyder.lspyder_eval(right, locals)


@special
class quote:
    def __init__(self, val, locals):
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
    def __init__(self, val, locals):
        self.val = val


@special
@rename(".")
def dot(cls, val, locals):
    return getattr(lspyder.lspyder_eval(cls, locals), val)
