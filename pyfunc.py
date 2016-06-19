builtins = globals()["__builtins__"]
def update(scope):
    del builtins["__name__"]
    scope.update(builtins)
