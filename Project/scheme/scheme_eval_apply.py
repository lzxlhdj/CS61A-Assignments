import sys

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms

##############
# Eval/Apply #
##############

def scheme_eval(expr, env, tail=False): # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.

    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # Evaluate atoms 原子类型，比如单独一个数字或者单独一个字符串这种
    if scheme_symbolp(expr):
        return env.lookup(expr)
    elif self_evaluating(expr):
        return expr

    # All non-atomic expressions are lists (combinations)
    #组合表达式检查

    if not scheme_listp(expr): #格式错误，不是组合 
        raise SchemeError('malformed list: {0}'.format(repl_str(expr)))
    first, rest = expr.first, expr.rest

    #特殊情况
    if scheme_symbolp(first) and first in scheme_forms.SPECIAL_FORMS: 
        need_tail = ['and', 'begin', 'or', 'cond', 'if', 'let']
        if first in need_tail:
            return scheme_forms.SPECIAL_FORMS[first](rest, env, tail)
        else:
            return scheme_forms.SPECIAL_FORMS[first](rest, env)
    #一般函数调用
    else: 
        # BEGIN PROBLEM 3
        "*** YOUR CODE HERE ***"
        operators = scheme_eval(first, env)
        operands = rest.map(lambda x:scheme_eval(x, env, False))
        return scheme_apply(operators, operands, env)
        # END PROBLEM 3

def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    validate_procedure(procedure)
    if not isinstance(env, Frame):
       assert False, "Not a Frame: {}".format(env)
    if isinstance(procedure, BuiltinProcedure):
        # BEGIN PROBLEM 2
        "*** YOUR CODE HERE ***"
        #将args(scheme list,即链表)转化为pythonlist
        args_python = []
        args_scheme = args
        while args_scheme is not nil:
            args_python.append(args_scheme.first)
            args_scheme = args_scheme.rest

        if procedure.need_env == True: #如果需要环境，将环境作为最后一个
            args_python.append(env)
        # END PROBLEM 2
        try:
            # BEGIN PROBLEM 2
            "*** YOUR CODE HERE ***"
            return procedure.py_func(*args_python)
            # END PROBLEM 2
        except TypeError as err:
            raise SchemeError('incorrect number of arguments: {0}'.format(procedure)) #参数数量错误报错在这里，其他写在过程自己里
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        "*** YOUR CODE HERE ***"
        lambda_frame = procedure.env.make_child_frame(procedure.formals, args) #注意!词法作用域！！！
        return eval_all(procedure.body, lambda_frame, True)
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        "*** YOUR CODE HERE ***"
        mu_frame = env.make_child_frame(procedure.formals, args)
        return eval_all(procedure.body, mu_frame, True) #这个是动态作用域
        # END PROBLEM 11
    else:
        assert False, "Unexpected procedure: {}".format(procedure)

def eval_all(expressions, env, tail = False):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last.

    >>> eval_all(read_line("(1)"), create_global_frame())
    1
    >>> eval_all(read_line("(1 2)"), create_global_frame())
    2
    >>> x = eval_all(read_line("((print 1) 2)"), create_global_frame())
    1
    >>> x
    2
    >>> eval_all(read_line("((define x 2) x)"), create_global_frame())
    2
    """
    # BEGIN PROBLEM 6
    last = None
    curr = expressions
    if curr is nil:
        return None
    while curr.rest is not nil:
        last = scheme_eval(curr.first, env)
        curr = curr.rest
    last = scheme_eval(curr.first, env, tail)
    return last
    # END PROBLEM 6


################################
# Extra Credit: Tail Recursion #
################################

class Unevaluated:
    """An expression and an environment in which it is to be evaluated."""

    def __init__(self, expr, env):
        """Expression EXPR to be evaluated in Frame ENV."""
        self.expr = expr
        self.env = env

def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not an Unevaluated."""
    validate_procedure(procedure)
    val = scheme_apply(procedure, args, env)
    if isinstance(val, Unevaluated):
        return scheme_eval(val.expr, val.env)
    else:
        return val

def optimize_tail_calls(unoptimized_scheme_eval):
    """Return a properly tail recursive version of an eval function."""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN OPTIONAL PROBLEM 1
        "*** YOUR CODE HERE ***"
        #此时不是尾调用,或者expr是自评估的或者是name,就正常评估
        while isinstance(result, Unevaluated):
            result = unoptimized_scheme_eval(result.expr, result.env, True) #这里必须传True！！！
            
        return result
        # END OPTIONAL PROBLEM 1
    return optimized_eval














################################################################
# Uncomment the following line to apply tail call optimization #
################################################################

scheme_eval = optimize_tail_calls(scheme_eval)
