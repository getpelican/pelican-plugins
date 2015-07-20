import inspect
import six

# Modifies class methods (or instances of them) on the fly
# http://blog.ianbicking.org/2007/08/08/opening-python-classes/
# http://svn.colorstudy.com/home/ianb/recipes/magicset.py
# including python 3 fixes for func_name => __name__ and types.ClassType => type

def magic_set(obj):
    """
Adds a function/method to an object. Uses the name of the first
argument as a hint about whether it is a method (``self``), class
method (``cls`` or ``klass``), or static method (anything else).
Works on both instances and classes.

>>> class color:
... def __init__(self, r, g, b):
... self.r, self.g, self.b = r, g, b
>>> c = color(0, 1, 0)
>>> c # doctest: +ELLIPSIS
<__main__.color instance at ...>
>>> @magic_set(color)
... def __repr__(self):
... return '<color %s %s %s>' % (self.r, self.g, self.b)
>>> c
<color 0 1 0>
>>> @magic_set(color)
... def red(cls):
... return cls(1, 0, 0)
>>> color.red()
<color 1 0 0>
>>> c.red()
<color 1 0 0>
>>> @magic_set(color)
... def name():
... return 'color'
>>> color.name()
'color'
>>> @magic_set(c)
... def name(self):
... return 'red'
>>> c.name()
'red'
>>> @magic_set(c)
... def name(cls):
... return cls.__name__
>>> c.name()
'color'
>>> @magic_set(c)
... def pr(obj):
... print obj
>>> c.pr(1)
1
"""
    def decorator(func):
        is_class = isinstance(obj, six.class_types)
        args, varargs, varkw, defaults = inspect.getargspec(func)
        if not args or args[0] not in ('self', 'cls', 'klass'):
            # Static function/method
            if is_class:
                replacement = staticmethod(func)
            else:
                replacement = func
        elif args[0] == 'self':
            if is_class:
                replacement = func
            else:
                def replacement(*args, **kw):
                    return func(obj, *args, **kw)
                try:
                    replacement.__name__ = func.__name__
                except:
                    pass
        else:
            if is_class:
                replacement = classmethod(func)
            else:
                def replacement(*args, **kw):
                    return func(obj.__class__, *args, **kw)
                try:
                    replacement.__name__ = func.__name__
                except:
                    pass
        setattr(obj, func.__name__, replacement)
        return replacement
    return decorator

if __name__ == '__main__':
    import doctest
    doctest.testmod()


