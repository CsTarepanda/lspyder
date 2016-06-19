#!/usr/bin/python3
import re
import pyfunc

pyfunc.update(globals())


def direct(*filenames):
    for filename in filenames:
        with open(filename + ("" if filename.endswith(".py") else ".py")) as f:
            exec(f.read(), globals())


direct("ast", "defines", "function_define", "symbol_define", "special_define")


class AST:
    def __init__(self, fnc_ast, *args_ast):
        self.fnc_ast = fnc_ast
        self.args_ast = args_ast

    def eval(self, scope):
        fnc = self.fnc_ast.eval(dict(scope))
        if fnc.__name__ != None and fnc.__name__ in specials:
            return fnc(scope, *self.args_ast)
        return fnc(*[arg.eval(dict(scope)) for arg in self.args_ast])

    def integrate(self):
        return [self.fnc_ast] + list(self.args_ast)

#     def tostr(self, num):
#         return """%s=>{
# %s%s
# %s}""" % (
#                 self.fnc_ast.tostr(num + 1) if isinstance(self.fnc_ast, AST) else str(self.fnc_ast),
#                 "\t"*(num + 1),
#                 ("\n%s" % ("\t"*(num))).join([s.tostr(num + 1) if isinstance(s, AST) else str(s) for s in self.args_ast]),
#                 "\t"*(num),
#                 )

    def __str__(self):
        return "(%s %s)" % (str(self.fnc_ast), " ".join(map(str, self.args_ast)))
        # return self.tostr(0)
        # return "%s=>{\n\t%s\n}" % (
        #         self.tostr(0) if isinstance(self.fnc_ast, AST) else str(self.fnc_ast),
        #         str("\n\t".join([s.tostr(1) if isinstance(s, AST) else str(s) for s in self.args_ast]))
                # )



start_matches = [r"[+-]?\d", "\""]
all_matches = ["True", "False"]
class Value:
    def __init__(self, val):
        if re.match(r'^(%s)' % "|".join(start_matches), val) or val in all_matches:
            self.val = eval(val)
            self.raw = True
        else:
            self.val = val
            self.raw = False
        
    def eval(self, scope):
        if self.raw:
            return self.val
        else:
            return Lspyder.get_value(self.val, scope)

    def name(self):
        if self.raw: raise SyntaxError("can't assign to literal")
        return self.val

    def __str__(self):
        if not self.raw: return "[ %s ]" % str(self.val)
        return "< %s >" % str(self.val)


class Empty:
    def eval(self, scope):
        return None

    def name(self):
        return None

    def __str__(self):
        return "< None >"
# {{{

class Function:
    def __init__(self, fnc):
        self.fnc = fnc

    def eval(self, scope):
        return Lspyder.get_value(self.fnc, scope)

    def name(self):
        return self.fnc

    def __str__(self):
        return "[ %s ]" % str(self.fnc)# }}}


class Lspyder(dict):
    def __init__(self, *local_scopes):
        for scope in local_scopes:
            self.update(scope)

    @staticmethod
    def get_value(var, scope):
        try:
            return scope[var] if var in scope else globals()[var]
        except KeyError:
            raise NameError(var)

    def file(self, filename):
        with open(filename) as f:
            self.compile(f.read())
        return self

    def exec(self, code=None):
        pass

    def eval(self, code=None):
        codes = parse(code) if code else self.code
        for c in codes: yield c.eval(dict(self))

    def compile(self, code):
        self.code = parse(code)
        return self

lspyder = Lspyder({})
lspyder.file("./define.lspy")
for i in lspyder.eval(): pass

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
            result = lspyder.eval(inp)
            print("=>", list(result)[-1])
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
