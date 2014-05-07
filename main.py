#!/usr/bin/env python


if __name__ == "__main__":

    from numeric.parse import parse

    for eq, expected in [
        ("1.0 + 2.0 * 3.0 - 4.0", "1.0 2.0 3.0 * + 4.0 -"),
        ("sin(2*3)", "2.0 3.0 * sin"),
    ]:
        print "Parse: %s" % (eq)
        print "Got:  %s" % (" ".join(map(str, parse(eq))))
        print "Need: %s" % (expected)