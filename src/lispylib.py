from functools import reduce
def difference(*nums):
    return reduce(lambda a, b: a-b, nums)

def product(*nums):
    return reduce(lambda a, b: a*b, nums)

def divide(*nums):
    return reduce(lambda a, b: a/b, nums)

def gt(a, b):
    return a > b

def gte(a, b):
    return a >= b

def equal(a, b):
    return a == b

def lte(a, b):
    return a <= b

def lt(a, b):
    return a < b

def list(*args):
    return args

def car(lst):
    return lst[0]

def cdr(lst):
    return lst[1:]

def cons(first, second):
    return [first] + second

def symbolp(x):
    return isinstance(x, str)

def listp(x):
    return isinstance(x, list)

def null(x):
    return nullp(x)

def nullp(x):
    return x == None

def append(lst, item):
    lst.append(item)

def inv(x):
    return not x
