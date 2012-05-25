import symbol
from builtins import *

class StopTranslation(Exception): pass

def translate_sexp(env):
  def t(sexp):
    if isinstance(sexp, list):
      return map(t, sexp)

    elif isinstance(sexp, tuple):
      # Method name resolution! The first element in the sexp may need special
      # translation. If not, then it will translate to a function.

      # If this is valid, this will either be a string representing a builtin,
      # or a method.
      method = t(sexp[0])
      args = map(t, sexp[1:])

      try:
        return method(*map(t, sexp[1:]))
      except TypeError as e:
        raise
        # TypeErrors are called when a function is called with the wrong number
        # of arguments. It's possible to screw this up -- the called method may
        # raise a TypeError and this will incorrectly show an error.

        import inspect
        print 'Error: %s requires %d arguments' % (
            sexp[0], len(inspect.getargspec(method).args) - 1)
        print 'Context:', sexp
        raise StopTranslation()

    elif isinstance(sexp, symbol.symbol):
      if sexp.sym in builtins:
        return eval('translate_%s' % sexp)(env)
      try:
        # The translation of a symbol is the associated binding.
        return env[sexp.sym]
      except KeyError:
        print 'No binding for', sexp
        raise StopTranslation()

    else:
      # Either a number or a string literal. Just return the literal.
      return sexp
  return t

def translate_top_level_sexp(env):
  return translate_sexp(env)

def translate(sexps):
  import stdlib
  env = stdlib.default_environment()

  tree = []
  try:
    for sexp in sexps:
      tree.append(translate_top_level_sexp(env)(sexp))
    return tree
  except StopTranslation:
    return None
