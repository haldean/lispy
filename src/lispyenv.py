import copy
import inspect
import lispycode
import lispyenv
import lispylib

class LispyEnv:
    def __init__(self, parent=None):
        self.bindings = {}

        self.symbol_mappings = {
            'print': self.lisp_print,
            '+': sum,
            '-': lispylib.difference,
            '*': lispylib.product,
            '/': lispylib.divide,
            '>=': lispylib.gte,
            '>': lispylib.gt,
            '<': lispylib.lt,
            '<=': lispylib.lte,
            }

        for method in dir(lispylib):
            attr = getattr(lispylib, method)
            if inspect.ismethod(attr):
                self.symbol_mappings[method] = attr

        self.parent = parent
    
    def apply(self, method_symbol, arguments=None):
        method = self.value(method_symbol.symbol)
        if arguments != None:
            arguments = map(self.value, arguments)
            return method(*arguments)
        else:
            return method()

    def value(self, obj):
        if isinstance(obj, lispycode.FutureEval):
            while isinstance(obj, lispycode.FutureEval):
                obj = obj.evaluate(self)
            return obj

        if obj in self.bindings:
            return self.bindings[obj]

        if self.parent:
            try:
                return self.parent.value(obj)
            except NameError:
                pass

        if obj in self.symbol_mappings:
            return self.symbol_mappings[obj]

        try:
            return eval(obj)
        except NameError:
            raise NameError('Symbol %s has no associated mapping.' % obj)

    def lisp_print(self, *objs):
        if len(objs) == 1:
            obj = objs[0]
            if isinstance(obj, lispycode.FutureEval):
                obj = obj.evaluate(self)
            print obj
            return obj
        else:
            print '   '.join(map(self.lisp_print, objs))
            return objs

    def set(self, name, val):
        if isinstance(name, lispycode.SymbolEval):
            name = name.symbol
        self.bindings[name] = val
