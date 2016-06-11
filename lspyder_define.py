from defines import define


@define
def begin(*args):
    print(args)
    return args[-1]


@define
def quote(*args):
    return args
