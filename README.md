numeric
=======

A brief experiment.


```language=python
>>> from numeric.parse import parse
>>>
>>> node = parse("a + b * c - d")
>>> print node
a + b * c - d
>>>
>>> print node.run(b=5)
a + 5 * c - d
>>> print node.run(c=3)
a + b * 3 - d
>>> print node.run(b=5, c=3)
a + 15 - d
>>> print node.run(a=1, b=2, c=3, d=4)
3
```