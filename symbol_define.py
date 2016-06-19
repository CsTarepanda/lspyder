@rename("*")
def multiply(*args):
    result = 1
    for i in args:
        result *= i
    return result


@rename("/")
def div(*args):
    result = args[0]
    for i in args[1:]:
        result /= i
    return result


@rename("+")
def plus(*args):
    return sum(args)


@rename("-")
def minus(*args):
    result = 0
    for i in args:
        result -= i
    return result


@rename("%")
def mod(*args):
    result = args[0]
    for i in args[1:]:
        result %= i
    return result


@rename("**")
def power(*args):
    result = args[0]
    for i in args[1:]:
        result **= i
    return result


@rename("|")
def _or(*args):
    result = args[0]
    for i in args[1:]:
        result |= i
    return result


@rename("&")
def _and(*args):
    result = args[0]
    for i in args[1:]:
        result &= i
    return result


@rename("^")
def xor(*args):
    result = args[0]
    for i in args[1:]:
        result ^= i
    return result


@rename("++")
def inc(arg):
    return arg + 1


@rename("--")
def dec(arg):
    return arg - 1


@rename("//")
def intdiv(*args):
    result = args[0]
    for i in args[1:]:
        result //= i
    return result


@rename("<<")
def left_shift(*args):
    result = args[0]
    for i in args[1:]:
        result <<= i
    return result


@rename(">>")
def right_shift(*args):
    result = args[0]
    for i in args[1:]:
        result >>= i
    return result


@rename("~")
def bitwise_negate(arg):
    return ~arg


@rename("[]")
def _list(*args):
    return list(args)


@rename("<>")
def _tuple(*args):
    return args


@rename("{}")
def _set(*args):
    return set(args)

@rename("{:}")
def _dict(*args):
    list1 = args[::2]
    list2 = args[1::2]
    return dict(zip(list1, list2))


@rename("!")
def equals(value):
    return not value

@rename("==")
def equals(left, right):
    return left == right


@rename("!=")
def equals(left, right):
    return left != right


@rename(">=")
def gt(left, right):
    return left >= right


@rename("<=")
def gt(left, right):
    return left <= right


@rename(">")
def gt(left, right):
    return left > right


@rename("<")
def gt(left, right):
    return left < right
