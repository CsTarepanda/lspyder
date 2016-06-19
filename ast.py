def parse(code_lines):
    not_strs = [""]
    not_strs_target = 0
    strs = [""]
    strs_target = 0
    strflg = False
    commentflg = False
    escapeflg = False
    for code in code_lines:
        for i in code:
            if commentflg:
                if i == "\n": commentflg = False
                else: continue
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
                    commentflg = True
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


def _ast(list_ast):
    val = [(_ast(v) if type(v) == list else Value(v)) for v in list_ast]
    if len(val) == 0: return Empty()
    return AST(val[0], *val[1:])


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
    return [_ast(list_ast) for list_ast in result]
