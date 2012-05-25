import translate

builtins = set(['if', 'when', 'unless'])

def curry_with_env(func):
  def outer(env):
    def inner(*args):
      return func(env, *args)
    return inner
  return outer

@curry_with_env
def translate_if(env, condition, iftrue, iffalse):
  if translate.translate_sexp(env)(condition):
    return translate.translate_sexp(env)(iftrue)
  else:
    return translate.translate_sexp(env)(iffalse)

@curry_with_env
def translate_when(env, condition, iftrue):
  if translate.translate_sexp(env)(condition):
    return translate.translate_sexp(env)(iftrue)
  else: return None

@curry_with_env
def translate_unless(env, condition, iffalse):
  if not translate.translate_sexp(env)(condition):
    return translate.translate_sexp(env)(iffalse)
  else: return None

