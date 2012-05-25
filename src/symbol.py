class symbol(object):
  def __init__(self, sym):
    self.sym = sym.lower()

  def __str__(self):
    return self.sym
  __repr__ = __str__
