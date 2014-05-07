import math

## EXPRESSION

class Expression(object):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return "(%s %s %s)" % (self.left, self.op.name, self.right)

    def run(self):
        return self.op.run(self.left.run(), self.right.run())


##  VALUES

class Value(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "%s" % (self.name)


class ConstantValue(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def run(self):
        return self.value


class NumericValue(ConstantValue):
    def __init__(self, value):
        super(NumericValue, self).__init__(value, value)


## OPS

class Op(object):
    #precedence = 0
    #left_assoc = 0
    #name = ""
    pass


class Mult(Op):
    precedence = 3
    left_assoc = True
    name = "*"

    @classmethod
    def run(cls, left, right):
        return left.run() * right.run()


class Div(Op):
    precedence = 3
    left_assoc = True
    name = "/"

    @classmethod
    def run(cls, left, right):
        return left.run() / right.run()


class Plus(Op):
    precedence = 2
    left_assoc = True
    name = "+"

    @classmethod
    def run(cls, left, right):
        return left.run() + right.run()


class Minus(Op):
    precedence = 2
    left_assoc = True
    name = "-"

    @classmethod
    def run(cls, left, right):
        return left.run() - right.run()


class Power(Op):
    precedence = 4
    left_assoc = False
    name = "^"

    @classmethod
    def run(cls, left, right):
        return left.run() ** right.run()


## FUNCS

class Func(object):
    def __init__(self, name, *args):
        self.name = name
        self.args = args

    def __str__(self):
        return "%s(%s)" % (self.name, ", ".join(map(str, self.args)))


class Sin(Func):
    def __init__(self, expr):
        super(Cos, self).__init__("sin", expr)

    def run(self):
        return math.sin(self.expr.run())


class Cos(Func):
    def __init__(self, expr):
        super(Cos, self).__init__("cos", expr)

    def run(self):
        return math.cos(self.expr.run())