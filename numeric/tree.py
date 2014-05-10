import math


class InvalidFunctionCall(Exception): pass

## EXPRESSIONS

class Expression(object):
    """
    Base Expression
    """
    num_args = 0

    @property
    def name(self):
        return "null"

    def __str__(self):
        return self.name

    def run(self, **variables):
        return ConstantExpression(float('nan'))

    def is_complete(self):
        return False


class ConstantExpression(Expression):
    num_args = 0

    def __init__(self, value):
        self.value = value

    @property
    def name(self):
        return str(self.value)

    def run(self, **variables):
        return self

    def is_complete(self):
        return isinstance(self.value, (int, float, long))


class NamedConstantExpression(ConstantExpression):
    num_args = 0

    def __init__(self, name, value):
        super(NamedConstantExpression, self).__init__(value)
        self._name = name

    @property
    def name(self):
        return self._name

    def run(self, **variables):
        return self


class VariableExpression(Expression):
    num_args = 0

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def run(self, **variables):
        print variables
        if self.name in variables:
            return ConstantExpression(variables[self.name])
        else:
            return self


## OPERATOR EXPRESSIONS

class OperatorExpression(Expression):
    num_args = 2

    def __init__(self, name, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return "(%s %s %s)" % (self.left, self.name, self.right)


class Multiply(OperatorExpression):
    name = "*"
    precedence = 3
    left_assoc = True

    def run(self, **variables):
        left_val = self.left.run(**variables)
        right_val = self.right.run(**variables)
        if left_val.is_complete() and right_val.is_complete():
            return ConstantExpression(left_val.value * right_val.value)
        else:
            return Multiply(self.name, left_val, right_val)


class Divide(OperatorExpression):
    name = "/"
    precedence = 3
    left_assoc = True

    def run(self, **variables):
        left_val = self.left.run(**variables)
        right_val = self.right.run(**variables)
        if left_val.is_complete() and right_val.is_complete():
            return ConstantExpression(left_val.value / right_val.value)
        else:
            return Divide(self.name, left_val, right_val)


class Add(OperatorExpression):
    name = "+"
    precedence = 2
    left_assoc = True

    def run(self, **variables):
        left_val = self.left.run(**variables)
        right_val = self.right.run(**variables)
        if left_val.is_complete() and right_val.is_complete():
            return ConstantExpression(left_val.value + right_val.value)
        else:
            return Add(self.name, left_val, right_val)


class Subtract(OperatorExpression):
    name = "-"
    precedence = 2
    left_assoc = True

    def run(self, **variables):
        left_val = self.left.run(**variables)
        right_val = self.right.run(**variables)
        if left_val.is_complete() and right_val.is_complete():
            return ConstantExpression(left_val.value - right_val.value)
        else:
            return Subtract(self.name, left_val, right_val)


class Exponent(OperatorExpression):
    name = "^"
    precedence = 4
    left_assoc = False

    def run(self, **variables):
        left_val = self.left.run(**variables)
        right_val = self.right.run(**variables)
        if left_val.is_complete() and right_val.is_complete():
            return ConstantExpression(left_val.value ** right_val.value)
        else:
            return Exponent(self.name, left_val, right_val)


## FUNCTIONS


class FunctionExpression(Expression):
    def __init__(self, name, *args):
        if len(args) != self.num_args:
            raise InvalidFunctionCall("Wrong number of arguments")
        self.args = args

    def __str__(self):
        return "%s(%s)" % (self.name, ", ".join(map(str, self.args)))

    def exec_args(self, **variables):
        return [arg.run(**variables) for arg in self.args]


class Sin(FunctionExpression):
    num_args = 1
    name = "sin"

    def __init__(self, name, expr):
        super(Sin, self).__init__(name, expr)

    def run(self, **variables):
        val, = self.exec_args(**variables)
        if val.is_complete():
            return ConstantExpression(math.sin(val.value))
        else:
            return Sin(self.name, val.run(**variables))


class Cos(FunctionExpression):
    num_args = 1
    name = "cos"

    def __init__(self, name, expr):
        super(Cos, self).__init__(name, expr)

    def run(self, **variables):
        val, = self.exec_args(**variables)
        if val.is_complete():
            return ConstantExpression(math.cos(val.value))
        else:
            return Cos(self.name, val.run(**variables))


