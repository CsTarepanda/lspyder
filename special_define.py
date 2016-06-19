# from defines import special, rename
#

@special
def define(scope, name, val):
    if name.raw: raise SyntaxError("can't assign to literal")
    globals()[name.val] = val.eval(scope)


def bind(scope, bind_ast):
    scope[bind_ast.fnc_ast.name()] = bind_ast.args_ast[0].eval(scope)

@special
def let(scope, binds_ast, proc):
    for b in binds_ast.integrate():
        bind(scope, b)
    return proc.eval(scope)


@special
@rename("lambda")
class Lambda:
    def __init__(self, scope, args, proc=None):
        if proc == None:
            self.proc = args
            self.args = []
        elif isinstance(args, Empty):
            self.proc = proc
            self.args = []
        else:
            self.args =  [arg.name() for arg in args.integrate()] if isinstance(args, AST) else [args.name()]
            self.proc = proc
        self.scope = scope

    def __call__(self, *args):
        scope = dict(self.scope)
        scope.update(dict(zip(self.args, args)))
        return self.proc.eval(scope)

    __name__ = None


@special
@rename("set!")
def assignment(var, value, locals):
    defs = locals if var in locals else globals if var in globals else None
    if not defs: raise NameError(var)
    defs[var] = lspyder.lspyder_eval(value, locals)


@special
@rename("and")
def _and(scope, left, right):
    return left.eval(scope) and right.eval(scope)


@special
@rename("or")
def _or(scope, left, right):
    return left.eval(scope) or right.eval(scope)


@special
class quote:
    def __init__(self, scope, ast):
        self.scope = scope
        self.ast = ast


    def __str__(self):
        return str(self.ast)

    
    def get(self):
        return self.ast

    def eval(self):
        return self.ast.eval(self.scope)


@special
@rename(".")
def dot(scope, cls, name):
    return getattr(cls.eval(scope), name.val)
