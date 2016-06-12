#!/usr/bin/python3
import lspyder
import lspyder_define
import symbol_define
import special_define
from defines import defines, specials
import re
defines.update(defines)
defines.update(specials)


def parse(code_lines):
    not_strs = [""]
    not_strs_target = 0
    strs = [""]
    strs_target = 0
    strflg = False
    escapeflg = False
    for code in code_lines:
        for i in code:
            if i == "\n": continue
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
                elif i == ";":
                    break
                else:
                    not_strs[not_strs_target] += i

    fmt = lambda n: n\
            .replace("'(", "(quote_sub ")\
            .replace("(", " ( ")\
            .replace(")", " ) ")\
            .split()
            # .replace("(  )", "()")\
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
    result = []
    tg = 0
    while parse_code:
        res, tg = sub_create_sat(parse_code)
        parse_code = parse_code[tg + 1:]
        result.append(res)
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


def eval(code, globals=defines, local=None, split=False):
    codes = parse(code if split else code.split("\n"))
    for c in codes[:-1]:
        lspyder_eval(c, globals, local if local else {})
    return lspyder_eval(codes[-1], globals, local if local else {})


# eval(open("./define.lspy").read())
# f = open("./define.lspy")
def fileread(name):
    eval(open(name).readlines(), split=True)


fileread("./define.lspy")
defines["pyeval"] = pyeval
defines["eval"] = eval


if __name__ == "__main__":
    import signal
    import sys

    if len(sys.argv) == 2:
        fileread(sys.argv[1])
        sys.exit()

    def ctr_c(signum, frame):
        print(" Good bye")
        sys.exit()
    signal.signal(signal.SIGINT, ctr_c)

    inp = ""
    inp_symbol = ">> "
    while True:
        try:
            inp += input(inp_symbol)
            result = eval(inp)
            print("=>", result)
        except SyntaxError:
            print(inp)
            if inp.endswith(":q"):
                inp = ""
                inp_symbol = ">> "
                continue
            elif not inp.endswith(" "):
                inp += " "
            inp_symbol = ".. "
            continue
        except EOFError:
            print(" Good bye")
            sys.exit()
        except Exception as e:
            print("%s: %s" % (e.__class__.__name__, e))
        inp = ""
        inp_symbol = ">> "
