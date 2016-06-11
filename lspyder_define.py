from defines import define, rename


@define
def begin(*args):
    print(args)
    return args[-1]


@define
def quote(*args):
    return args


@define
@rename("if")
def if_else(comp, true, false):
    return true if comp else false
