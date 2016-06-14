#!/usr/bin/python3
import lspyder
import lspyder_define
import symbol_define
import special_define
from defines import defines, specials
import re
defines.update(defines)
defines.update(specials)


class Lspyder:
    def __init__(self, *local_scopes, global_scope=None):
        if global_scope: self.global_scope = dict(global_scope)
        self.local_scope = {}
        for i in local_scopes:
            self.local_scope.update()

    def get_value(self, var):
        if type(var) == list:
            return lspyder_eval(var, self.local_scope)
        try:
            return self.local_scope[var] if var in self.local_scope else self.global_scope[var]
        except KeyError:
            raise NameError(var)




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
            .replace("'(", "(quote ")\
            .replace("(", " ( ")\
            .replace(")", " ) ")\
            .split()
    not_strs = list(map(fmt, not_strs))

    fmt = lambda n: '"%s"' % n
    strs = list(map(fmt, strs))
    result = not_strs[0]
    for n, s in zip(not_strs[1:], strs):
        result.append(s)
        result += n
    return create_ast(result)


def create_ast(parse_code):
    def sub_create_ast(code, target=1):
        sub_result = []
        code_length = len(code)
        while target < code_length:
            if code[target] == "(":
                sub_ast, tmp = sub_create_ast(code[target:])
                target += tmp
                sub_result.append(sub_ast)
            elif code[target] == ")":
                return sub_result, target
            else:
                sub_result.append(code[target])
            target += 1
        raise SyntaxError("unexpected")
    result = []
    tg = 0
    while parse_code:
        res, tg = sub_create_ast(parse_code)
        parse_code = parse_code[tg + 1:]
        result.append(res)
    print(result)
    return result


peval = eval
pyeval = lambda x, local: peval(x, defines, local)


def get_value(var, locals):
    if type(var) == list:
        return lspyder_eval(var, locals)
    try:
        return locals[var] if var in locals else defines[var]
    except KeyError:
        raise NameError(var)


def lspyder_exec(fnc, args, locals):
    value = get_value(fnc, locals)
    if type(fnc) == str and fnc in specials:
        # return Special(locals, value)(*args)
        return value(*args, locals=locals)
    return value(*[lspyder_eval(x, locals) for x in args])


def lspyder_eval(code, locals):
    if type(code) == list:
        return lspyder_exec(code[0], code[1:], dict(locals))
    return locals[code] if code in locals\
            else\
            defines[code] if code in defines\
            else\
            pyeval(code, dict(locals))


def eval(code, local=None, split=False):
    codes = parse(code if split else code.split("\n"))
    for c in codes[:-1]:
        lspyder_eval(c, local if local else {})
    return lspyder_eval(codes[-1], local if local else {})


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
        except SyntaxError as e:
            print(e)
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
