#!/usr/bin/python3
import lspyder
import lspyder_define
import symbol_define
import special_define
from defines import defines, specials
defines.update(defines)
defines.update(specials)


def parse(code):
    not_strs = [""]
    not_strs_target = 0
    strs = [""]
    strs_target = 0
    strflg = False
    escapeflg = False

    for i in code:
        if strflg:
            if i == '"' and not escapeflg:
                strs.append("")
                strs_target += 1
                strflg = False
            elif i == '\\' and not escapeflg:
                escapeflg = True
                strs[strs_target] += i
            else:
                escapeflg = False
                strs[strs_target] += i
        else:
            if i == '"':
                not_strs.append("")
                not_strs_target += 1
                strflg = True
            else:
                not_strs[not_strs_target] += i

    fmt = lambda n: n\
            .replace("'(", "(quote ")\
            .replace("(", " ( ")\
            .replace(")", " ) ")\
            .replace("(  )", "()")\
            .split()
    not_strs = list(map(fmt, not_strs))

    fmt = lambda n: '"%s"' % n
    strs = list(map(fmt, strs))
    result = not_strs[0]
    for n, s in zip(not_strs[1:], strs):
        result.append(s)
        result += n
    return create_sat(result)


def create_sat(parse_code):
    def sub_create_sat(code, target=1):
        sub_result = []
        code_length = len(code)
        while target < code_length:
            if code[target] == "(":
                sub_sat, tmp = sub_create_sat(code[target:])
                target += tmp
                sub_result.append(sub_sat)
            elif code[target] == ")":
                return sub_result, target
            else:
                sub_result.append(code[target])
            target += 1
        raise SyntaxError("unexpected")
    result = sub_create_sat(parse_code)[0]
    return result


def get_value(var, globals, locals):
    if type(var) == list:
        return lspyder_eval(var, globals, locals)
    try:
        return locals[var] if var in locals else globals[var]
    except KeyError:
        raise NameError(var)


def lspyder_exec(fnc, args, globals, locals):
    value = get_value(fnc, globals, locals)
    if type(fnc) == str and fnc in specials:
        return value(*args, globals=globals, locals=locals)
    return value(*[lspyder_eval(x, globals, locals) for x in args])


def lspyder_eval(code, globals, locals):
    if type(code) == list:
        return lspyder_exec(code[0], code[1:], globals, locals)
    result = globals.get(code)
    return result if result else pyeval(code, globals, locals)


pyeval = eval


def eval(code, globals=defines, local=None):
    return lspyder_eval(parse(code), globals, local if local else {})


# eval(open("./define.lspy").read())
# f = open("./define.lspy")
for i in open("./define.lspy"):
    if not i.startswith(";"):
        eval(i)
defines["pyeval"] = pyeval
defines["eval"] = eval


if __name__ == "__main__":
    import signal
    import sys

    def ctr_c(signum, frame):
        print(" Good bye")
        sys.exit()
    signal.signal(signal.SIGINT, ctr_c)

    while True:
        try:
            result = eval(input(">> "))
            print("=>", result)
        except EOFError:
            print(" Good bye")
            sys.exit()
        except Exception as e:
            print("%s: %s" % (e.__class__.__name__, e))
