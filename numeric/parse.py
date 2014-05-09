from numeric import tree


class ParseException(Exception): pass


class InvalidOperatorError(ParseException): pass


class ParenthesisException(ParseException): pass


class NumberFormatException(ParseException): pass


OPS = {
    "*": tree.Multiply,
    "+": tree.Add,
    "-": tree.Subtract,
    "^": tree.Exponent,
    "/": tree.Divide,
}

CONSTANTS = {
    "pi": 3.14159265359,
    "e": 2.71828182845,
}

FUNCS = {
    "sin": tree.Sin,
    "cos": tree.Cos,
}

EXPRESSIONS = dict(OPS)
EXPRESSIONS.update(FUNCS)

STATE_NONE = 0
STATE_CHAR = 1
STATE_NUM = 2


def gen_tokens(string):
    # split by commas and spaces
    string = string.lower()
    current = ''
    state = 0
    has_decimal = 0
    for index, char in enumerate(string):
        if char == " ":
            # yield current and continue
            if current:
                yield current
                current = ""
            state = STATE_NONE
        elif char in "(),":
            # yield current and char and continue
            if current:
                yield current
                current = ""
            yield char
            state = STATE_NONE
        elif char in '0123456789.':
            if state == STATE_CHAR:
                # automatic multiply
                if current:
                    yield current
                    if current not in OPS:
                        yield "*"
                current = ""
                # end mode
                state == STATE_NONE
            if state == STATE_NONE:
                # enter num mode
                state = STATE_NUM
                has_decimal = False
            if char == '.':
                if has_decimal:
                    raise NumberFormatException("Too many decimals")
                has_decimal = True
            # Append char to current number
            current += char
        # have char
        elif char in OPS:
            if current:
                yield current
                current = ""
            yield char
            state = STATE_NONE
        # var name or function name
        else:
            if state == STATE_NUM:
                # automatic multiply
                if current:
                   yield current
                if char not in OPS:
                    yield "*"
                current = ""
                # end mode
                state = STATE_NONE
            if state == STATE_NONE:
                # enter char mode
                state = STATE_CHAR
            # append char to current token
            current += char
    if current:
        yield current


def polish(string):
    ops = []

    def get_op(key):
        try:
            return OPS[key]
        except IndexError:
            raise InvalidOperatorError("Invalid operator %r" % (key))

    def check_left_paren():
        if not ops or ops[-1] != "(":
            raise ParenthesisException("Matching parenthesis not found")

    for token in gen_tokens(string):
        # function
        if token in FUNCS:
            ops.append(token)
        # comma
        elif token == ",":
            # yield until left paren
            while ops and ops[-1] != "(":
                yield ops.pop()
            check_left_paren()
        # operator
        elif token in OPS:
            o1 = get_op(token)
            while ops and ops[-1] in OPS:
                o2 = get_op(ops[-1])
                if (o1.left_assoc and o1.precedence == o2.precedence) or (o1.precedence < o2.precedence):
                    yield ops.pop()
                else:
                    break
            ops.append(token)
        # left paren
        elif token == "(":
            # push left paren onto stack
            ops.append(token)
        # right paren
        elif token == ")":
            # yield until left paren
            while ops and ops[-1] != "(":
                yield ops.pop()
            check_left_paren()
            ops.pop()
            # if its a func, yield the function token to the output (function special case)
            if ops[-1] in FUNCS:
                yield ops.pop()
        # numeric value, constant, variable
        else:
            try:
                yield float(token)
            except ValueError:
                yield token
    while ops:
        if ops[-1] in ("(", ")"):
            raise ParenthesisException("Mismatched Parenthesis")
        yield ops.pop()


def parse(string):
    stack = []
    print list(polish(string))
    for token in polish(string):
        if token in EXPRESSIONS:
            klass = EXPRESSIONS[token]
            n = klass.num_args
            args = stack[-n:]
            stack = stack[:-n]
            print klass, token, args
            expr = klass(token, *args)
            stack.append(expr)
        elif isinstance(token, float):
            stack.append(tree.ConstantExpression(token))
        elif token in CONSTANTS:
            stack.append(tree.NamedConstantExpression(token, CONSTANTS[token]))
        else:
            stack.append(tree.VariableExpression(token))
    if len(stack) != 1:
        raise ParseException("Invalid formula")
    return stack[0]




