#!/usr/bin/env python


if __name__ == "__main__":

    from numeric import tree
    from numeric.parse import parse
    from numeric.parse import simplify
    from numeric.parse import polish

    for eq, expected in [
        ("1.0 + 2.0 * 3.0 - 4.0", "1.0 2.0 3.0 * + 4.0 -"),
        ("sin(2*3)", "2.0 3.0 * sin"),
    ]:
        print "Parse: %s" % (eq)
        print "Got:  %s" % (" ".join(map(str, polish(eq))))
        print "Need: %s" % (expected)


    expr = tree.Multiply('*', tree.ConstantExpression(5), tree.Divide('/', tree.ConstantExpression(12), tree.ConstantExpression(4)))
    print expr
    print expr.run()

    node = parse("1.0 + 2.0 * 3.0 - 4.0")
    print node

    node = parse("a + b * c - d")
    print node

    ##
    print node.run(b=5)
    print node.run(c=3)
    print node.run(b=5, c=3)
    print node.run(b=5, c=3, d=7)
    print parse('sin(c)').run(c=34)
    print parse('5c').run(c=3)
    print parse('5c3').run(c=3)
    print parse('5c3').run(c=3)
    print parse('5c * sin(3)').run(c=3)

    print parse('4234.23428394 * 293847').run()