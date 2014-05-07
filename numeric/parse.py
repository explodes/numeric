from numeric import tree


class ParseException(Exception): pass


class InvalidOperatorError(ParseException): pass


class ParenthesisException(ParseException): pass


class NumberFormatException(ParseException): pass


OPS = {
    "*": tree.Mult,
    "+": tree.Plus,
    "-": tree.Minus,
    "^": tree.Power,
    "/": tree.Div,
}

CONSTANTS = {
    "pi": 3.14159265359,
    "e": 2.71828182845,
}

FUNCS = {
    "sin": tree.Sin,
    "cos": tree.Cos,
}

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
        else:
            # have char
            if state == STATE_NUM:
                # automatic multiply
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


def parse(string):
    ops = []

    def get_op(key):
        try:
            return OPS[key]
        except IndexError:
            raise InvalidOperatorError("Invalid operator %r" % (key))

    def check_left_paren():
        if not ops or ops[-1] != "(":
            raise ParenthesisException("Matching parenthesis not found")

    print "TOKENS", list(gen_tokens(string))


    for token in gen_tokens(string):

        # function
        if token in FUNCS:
            # print "function", "op-push1", token
            ops.append(token)
        # comma
        elif token == ",":
            # yield until left paren
            while ops and ops[-1] != "(":
                # print "comma", "op-pop1", ops[-1]
                yield ops.pop()
            check_left_paren()
        # operator
        elif token in OPS:
            o1 = get_op(token)
            while ops and ops[-1] in OPS:
                o2 = get_op(ops[-1])
                if (o1.left_assoc and o1.precedence == o2.precedence) or (o1.precedence < o2.precedence):
                    # print "operator", "op-pop1", ops[-1]
                    yield ops.pop()
                else:
                    break
            # print "operator", "op-push1", token
            ops.append(token)
        # left paren
        elif token == "(":
            # push left paren onto stack
            # print "left-paren", "op-push1", token
            ops.append(token)
        # right paren
        elif token == ")":
            # yield until left paren
            while ops and ops[-1] != "(":
                # print "right-paren", "op-pop1", ops[-1]
                yield ops.pop()
            check_left_paren()
            ops.pop()
            # if its a func, yield the function token to the output (function special case)
            if ops[-1] in FUNCS:
                # print "right-paren", "op-pop2", ops[-1]
                yield ops.pop()
        # numeric value
        elif token in CONSTANTS:
            # token is a number/constant
            # print "constant", "yield1", token
            yield token
        # numeric value
        else:
            # token is a number, maybe
            try:
                # print "numeric", "yield1", token
                yield float(token)
            except ValueError:
                raise ParseException("Invalid token: %s" % (token))
    while ops:
        if ops[-1] in ("(", ")"):
            raise ParenthesisException("Mismatched Parenthesis")
        # print "extras", "op-pop1", ops[-1]
        yield ops.pop()




