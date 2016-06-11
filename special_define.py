from defines import special, symbol, register


@special
def define(df, val):
    register(df, val)


@special
@symbol("\"")
def string(*args):
    return " ".join(map(str, args))

