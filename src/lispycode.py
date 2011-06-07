import lispyenv

class FutureEval:
    def __init__(self, provider):
        self.provider = provider

    def evaluate(self, env):
        self.env = env
        return self.provider()

class NilEval(FutureEval):
    def __init__(self):
        FutureEval.__init__(self, lambda: None)

class SetqEval(FutureEval):
    def __init__(self, obj, val):
        def setq():
            return self.env.set(obj, val)
        FutureEval.__init__(self, setq)

class ListEval(FutureEval):
    def __init__(self, exprs):
        def eval_list():
            if len(exprs) > 1:
                car, cdr = exprs[0], exprs[1:]
                return self.env.apply(car, cdr)
            else:
                return self.env.apply(exprs[0])
        FutureEval.__init__(self, eval_list)

class IfEval(FutureEval):
    def __init__(self, cond, true, false):
        def eval_if():
            if cond.evaluate(self.env): 
                return true.evaluate(self.env)
            else: 
                return false.evaluate(self.env)
        FutureEval.__init__(self, eval_if)

class PrognEval(FutureEval):
    def __init__(self, evals):
        def eval_all():
            for e in evals:
                last = self.env.value(e)
            return last
        FutureEval.__init__(self, eval_all)

class SymbolEval(FutureEval):
    def __init__(self, symbol):
        self.symbol = symbol
        def eval_symbol():
            return self.env.value(symbol)

        FutureEval.__init__(self, eval_symbol)

class CondEval(FutureEval):
    def __init__(self, conds):
        def eval_cond():
            for cond, ret in conds:
                if self.env.value(cond): 
                    return self.env.value(ret)
            return None
        FutureEval.__init__(self, eval_cond)

class DefunEval(FutureEval):
    def __init__(self, name, args, body):
        def eval_defun():
            def fun(*funargs):
                fun_env = lispyenv.LispyEnv(self.env)

                if len(funargs) != len(args):
                    raise TypeError('%s expects %d arguments, got %d'
                                    % (name, len(args), len(funargs)))
                for argname, argval in zip(args, funargs):
                    fun_env.set(argname, argval)

                return body.evaluate(fun_env)

            self.env.set(name, fun)

        FutureEval.__init__(self, eval_defun)

class LetEval(FutureEval):
    def __init__(self, assign, body):
        def eval_let():
            env = lispyenv.LispyEnv(self.env)
            for var, val in assign:
                env.set(var, val)
            return body.evaluate(env)
        FutureEval.__init__(self, eval_let)

class LiteralEval(FutureEval):
    def __init__(self, obj):
        self.obj = obj
        
        def remove_literal_tag(objs):
            if isinstance(objs, LiteralEval):
                objs = objs.obj
            if isinstance(objs, list):
                objs = map(remove_literal_tag, objs)
            return objs

        if isinstance(self.obj, list):
            self.obj = remove_literal_tag(self.obj)

        FutureEval.__init__(self, self.value)

    def value(self):
        return self.obj
            
    def __repr__(self):
        return '<literal %s>' % repr(self.obj) 

    def __str__(self):
        return '<literal %s>' % str(self.obj)

