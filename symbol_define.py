from defines import symbol


@symbol("*")
def multiply(*args):
    result = 1
    for i in args:
        result *= i
    return result


@symbol("/")
def div(*args):
    result = args[0]
    for i in args[1:]:
        result /= i
    return i


@symbol("+")
def plus(*args):
    return sum(args)


@symbol("-")
def minus(*args):
    result = 0
    for i in args:
        result -= i
    return result


@symbol("%")
def mod(*args):
    result = args[0]
    for i in args[1:]:
        result %= i
    return result


@symbol("**")
def power(*args):
    result = args[0]
    for i in args[1:]:
        result **= i
    return result


@symbol("|")
def _or(*args):
    result = args[0]
    for i in args[1:]:
        result |= i
    return result


@symbol("&")
def _and(*args):
    result = args[0]
    for i in args[1:]:
        result &= i
    return result


@symbol("^")
def xor(*args):
    result = args[0]
    for i in args[1:]:
        result ^= i
    return result


@symbol("++")
def inc(arg):
    return arg + 1


@symbol("--")
def dec(arg):
    return arg - 1


@symbol("//")
def intdiv(*args):
    result = args[0]
    for i in args[1:]:
        result //= i
    return result


@symbol("<<")
def left_shift(*args):
    result = args[0]
    for i in args[1:]:
        result <<= i
    return result


@symbol(">>")
def right_shift(*args):
    result = args[0]
    for i in args[1:]:
        result >>= i
    return result


@symbol("~")
def bitwise_negate(arg):
    return ~arg


@symbol("[]")
def _list(*args):
    return list(args)


@symbol("()")
def _tuple(*args):
    return args


@symbol("{}")
def _set(*args):
    return set(args)

@symbol("{:}")
def _dict(*args):
    list1 = args[::2]
    list2 = args[1::2]
    return dict(zip(list1, list2))
