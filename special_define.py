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
