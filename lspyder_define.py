import lspyder
from defines import define, rename


@define
def begin(*args):
    return args[-1]


@define
@rename("if")
def if_else(comp, true, false):
    return true if comp else false


@define
def cast(to, frm):
    return to(frm)
