def begin(*args):
    return args[-1]


@rename("if")
def if_else(conditions, true, false):
    return true if conditions else false
