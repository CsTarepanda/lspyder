import lspyder
from defines import special, rename, register


@special
def define(df, val):
    register(df, lspyder.lspyder_eval(val, lspyder.defines, {}))


@special
@rename("lambda")
def lmd(dargs, proc):
    return eval((
        "lambda %s: lspyder.lspyder_eval(proc, globals=lspyder.defines, locals=locals())" % ", ".join(dargs)), {"lspyder": lspyder, "proc": proc})
