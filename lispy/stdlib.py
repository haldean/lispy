def default_environment():
  return {
      '+': lambda a, b: a + b,
      '-': lambda a, b: a - b,
      '*': lambda a, b: a * b,
      '/': lambda a, b: a / b,
      '%': lambda a, b: a % b,
      }
