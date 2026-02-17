# Scheme的尾递归优化

## 主要思想：蹦床优化

项目里提供了一个优化`scheme_eval`的函数，返回一个优化后的`scheme_eval`。这个优化后的`scheme_eval`，会带有tail参数，来判断这次评估是否在尾上下文中。在尾上下文时，先不评估出来，存入Thunk(也就是提供的`Unevaluated`类)，在非尾上下文，要值的时候再循环评估出来。

## 例

````scheme
>>> (define (sum n total) 
  (if (zero? 0) total (sum (- n 1) (+ n total))))
>>> (sum 1001 0)
````

这个的评估流程：

所有用户输入的都会要求出最后的值，所以输入的语句tail都是False，所以直接进入while循环，执行`unoptimized_scheme_eval`

对第一句：

1. 评估发现是define是特殊情况
2. 进入do_define_form进行绑定，绑定了一个lambda函数（这个lambda函数的body只有一句，也就是这个if语句）到sum，返回这个sum。这一句评估结束。

对于第二句:

1. 评估这个sum，不是特殊情况，会进入函数调用

2. 进入`scheme_apply`来应用sum函数。sum绑定到一个lambda函数。

3. 在`eval_all`里面评估这个lambda函数的body，只有一句，这一句是尾上下文，返回一个Unevaluated，这个里面包裹的是if这一整句。

4. 进入while循环，前面的帧都释放了，再开新的帧，来评估if语句，现在也是在尾上下文中评估。

5. 评估发现if是特殊形式，进入`do_if_form`,注意tail(True)作为参数一并传入。

6. 进入`eval_all`评估alternative(tail = True)，返回Unevaluated，里面的语句为`sum(1000 1001)`

7. 进入while循环，释放了帧，再评估unevaluated里面的表达式。

8. 如此循环往复，每次计算完一次都会释放掉帧，不会达到最大递归深度报错。最终计算出结果。

## 实现方法

#### 优化评估函数：

````python
def optimize_tail_calls(unoptimized_scheme_eval):
    """Return a properly tail recursive version of an eval function.返回一个评估函数的尾递归版本"""
    def optimized_eval(expr, env, tail=False):
        """Evaluate Scheme expression EXPR in Frame ENV. If TAIL,
        return an Unevaluated containing an expression for further evaluation.
        """
        #如果是尾上下文的评估且不是原子表达式：直接返回Unevaluated，不算出来
        if tail and not scheme_symbolp(expr) and not self_evaluating(expr):
            return Unevaluated(expr, env)

        result = Unevaluated(expr, env)
        # BEGIN OPTIONAL PROBLEM 1
        "*** YOUR CODE HERE ***"
        #此时不是尾调用,或者是原子表达式，需要把值求出来！
        while isinstance(result, Unevaluated):
            result = unoptimized_scheme_eval(result.expr, result.env, True) 
        #这里必须传True！！！为了避免在评估过程中还是原来的深度递归，而是一样的能够返回这个蹦床循环
            
        return result
        # END OPTIONAL PROBLEM 1
    return optimized_eval
````

#### 原评估函数

对于之前未优化的原评估函数，也有需要修改的地方：

在这里，我们需要加入第三个参数tail：默认为False，别干扰了之前写好的逻辑。而在True时，我们需要将这个参数传入到特殊情况里面(如if, begin等)，这样在特殊情况时能正确触发尾调用逻辑。

````python

def scheme_eval(expr, env, tail=False): # 增加第三个参数tail！
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
            return scheme_forms.SPECIAL_FORMS[first](rest, env, tail) #只对需要tail参数的特殊情况传tail参数
        else:
            return scheme_forms.SPECIAL_FORMS[first](rest, env)
    #一般函数调用
    else: 
        # BEGIN PROBLEM 3
        "*** YOUR CODE HERE ***"
        operators = scheme_eval(first, env)
        operands = rest.map(lambda x:scheme_eval(x, env))
        return scheme_apply(operators, operands, env)
        # END PROBLEM 3
````

#### 优化apply函数

````python
def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    ......
    ......
    elif isinstance(procedure, LambdaProcedure):
        # BEGIN PROBLEM 9
        "*** YOUR CODE HERE ***"
        lambda_frame = procedure.env.make_child_frame(procedure.formals, args) #注意!词法作用域！！！
        return eval_all(procedure.body, lambda_frame, True) #这里必须传True，lambda函数的最后一个表达式都是尾上下文
        # END PROBLEM 9
    elif isinstance(procedure, MuProcedure):
        # BEGIN PROBLEM 11
        "*** YOUR CODE HERE ***"
        mu_frame = env.make_child_frame(procedure.formals, args) #这个是动态作用域
        return eval_all(procedure.body, mu_frame, True) #这里同理
        # END PROBLEM 11
    ......
    ......
````

#### 优化eval_all函数

相应的，在`scheme_apply`函数中，我们调用了`eval_all`函数，这个函数经常用到，而这个函数所评估的最后一个表达式可能会是尾上下文，我们需要加入tail参数进行传递

````python
def eval_all(expressions, env, tail = False):
    """Evaluate each expression in the Scheme list EXPRESSIONS in
    Frame ENV (the current environment) and return the value of the last.
	"""
    ......
    ......
    last = scheme_eval(curr.first, env, tail) #最后一个表达式可能是尾上下文
    return last
````

#### 优化特殊形式

许多特殊形式的最后一句都有可能会是尾调用，需要加入tail参数来判断，具体来说是'and', 'begin', 'or', 'cond', 'if', 'let'。

````python
def do_if_form(expressions, env, tail = False):
    """Evaluate an if form.

    >>> env = create_global_frame()
    >>> do_if_form(read_line("(#t (print 2) (print 3))"), env) # evaluating (if #t (print 2) (print 3))
    2
    >>> do_if_form(read_line("(#f (print 2) (print 3))"), env) # evaluating (if #f (print 2) (print 3))
    3
    """
    validate_form(expressions, 2, 3)
    if is_scheme_true(scheme_eval(expressions.first, env, False)): #注意这个条件不可能是为上下文，要求出来的
        return scheme_eval(expressions.rest.first, env, tail)
    elif len(expressions) == 3:
        return scheme_eval(expressions.rest.rest.first, env, tail)
````

其他类似。

