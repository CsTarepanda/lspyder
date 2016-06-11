from defines import special, rename, register


@special
def define(df, val):
    register(df, val)


@special
@rename("lambda")
def lmd():
    pass


@special
@rename("\"")
def string(*args):
    return " ".join(map(str, args))

