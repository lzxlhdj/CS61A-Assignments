# Scheme

## Scheme基础

Scheme由表达式组成

- 初级表达式：2， 3.3， true，+，quotient...
- Combinations组合: (quotient 10 2), (not true)

数字是自我评估的，符号绑定到值

调用表达式：以运算符开头，后跟零个或多个操作数，全都在括号中

````scheme
> (quotient 10 2)  'quotient'是Scheme内置的除法**过程**（即python的函数）
5
> (quotient (+ 8 7) 5)
3
> (+ (* 3			空格和换行并不重要，重要的是括号要关上
        (+ (* 2 4)
           (+ 3 5)))
     (+ (- 10 7)
        6))
````

## 特殊形式 Special Forms

一个组合不是一个调用表达式就是特殊形式

- **If** 表达式：(if < predicate > < consequent > < alternative >)

先评估predicate 在决定评估consequent还是alternative

- **And** and **or**:  (and < e1 > ... < en >), (or < e1 > ... < en >)
- Binding symbals:  (define 变量名 表达式)

````scheme
> (define pi 3.14)
> (* pi 2)
6.28
````

- New procedures(定义一个新**过程**)：(define (过程名  形参)  主体)

````scheme
> (define (abs x)
    (if (< x 0)
    	(- x)
    	x))
> (abs -3)
3
````

在scheme中也可以递归调用

(square是平方过程，average是取平均过程)  (假设已经定义)

````scheme
> (define (sqrt x)
    (define (update guess)
      (if (= (square guess) x)
          guess
          (update (average guess (/ x guess)))))
    (update 1))
> (sqrt 256)
16
````

## Lambda expressions

lambda表达式评估为匿名过程

````scheme
(lambda (<formal-parameters>) <body>)
````

在调用表达式中，操作符本身可以是一个组合

````scheme
((lambda (x y z) (+ x y (square z))) 1 2 3)
````

## 更多Special Forms

### Cond & Begin

cond : 类似 if-elif-else

````scheme
(cond ((> x 10) (print 'big'))
      ((> x 5)  (print 'medium'))
      (else    (print 'small')) )
or
(print 
 	(cond ((> x 10) 'big')
          ((> x 5) 'medium')
          (else 'small') ) )
````

begin sepecial form combines multiple expressions into one expression

in python:

````python
if x > 10:
    print('big')
    print('guy')
else :
    print('small')
    print('fry')
````

in scheme:

````scheme
(if (> x 10) (begin
                (print 'big')
              	(print 'guy'))
    		 (begin
                (print 'small')
				(print 'fry')))
````

### Let Expressions

bind symbals to values temporarily, just for one expression 临时绑定

````scheme
(let ((变量名1 初始值1)
      (变量名2 初始值2))
    (主体代码))
````

当计算出c的值之后 a和b的绑定就消失了

define用于定义永久存在的，经常使用的

否则，如果需要一些临时的信息，一般用let

## 例：Sierpinski's Triangle

````scheme
(define (line) (fd 50))
(define (repeat k fn)
  (fn)
  (if (> k 1) (repeat (- k 1) fn)))
# 重复fn k次
(define (tri fn)
  (repeat 3 (lambda () (fn) (lt 120))))
#一个三角形，fn是画边的函数 比如line
(define (sier d k)
  (tri (lambda () (if (= d 1) (fd k) (leg d k)))))
(define (leg d k)
  (sier (- d 1) (/ k 2))
  (penup) (fd k) (pendown))
````

## Lists in Scheme

- **cons:** 两参数的过程，将一个元素添加到后面的元素的前面 `(cons car cdr)`
- **car:** 返回列表的第一个元素的过程
- **cdr:** 返回the rest of a list的过程
- **nil:** 一个空列表

Scheme 列表的元素用空格分隔，写在括号里，但是所有的Scheme列表都有一个**链表结构**

````scheme
> (define x (cons 1 (cons 2 nil)))
> x
(1 2)
> (car x)
1
> (cdr x)
(2)
````

#### null? 

判断是否是空列表

````scheme
> (null? nil)
#t
````

#### list

创造一个列表，但是本质底层还是链表

````scheme
> (list 1 2 3 4)
(1 2 3 4)
> (cdr (list 1 2 3 4))
(2 3 4)
````

## 符号式编程

symbols 一般指向值，但是你也可以引用symbol

**引用**用于直接引用某个symbol

````scheme
> (define a 1)
> (define b 2)
> (list a b)
(1 2)
> (list 'a 'b)
(a b)
> (list 'a b)
(a 2)
'a和'b本质是(quote a),(quote b)的缩写
表示引用的表达式本身就是值，不需要对其进行求值
````
引用也可以用于组合来构建列表(其中的表达式都被引用)

````scheme
> '(a b c)
(a b c)
> '(1 a)
(1 a)
````

## 列表处理过程

- **(append s  t): **将s，t两个列表的元素全部放到一个列表中(也可以多个)
- **(map f s): **对s的每一个元素调用f，返回列表
- **(filter f s):** 返回对s的元素调用f为真的元素的列表
- **(apply f s): **将s的所有元素作为f的参数

````scheme
> (define s (cons 1 (cons 2 nil)))
> s
(1 2)
> (append s s)
(1 2 1 2)
> (map even? s)
(#f #t)
> (filter even? s)
(2)
> (apply quotient '(10 5))
2
> (apply + '(1 2 3 4))
10
````

## 偶数子集

s的非空子集：包含s的一些元素的列表

even-subsets: 返回所有子集组成的列表，这些子集内部元素的和都为偶数

递归过程：s的偶数和子集包括...

- 所有偶数和子集of the rest of s
- s的第一个元素 跟着 s剩下部分的偶数/奇数和子集
- 只有s的第一个元素，如果它是偶数

````scheme
(define (even-subsets s)
  (if (null? s) nil 
      			(append (even-subsets (cdr s)) 
                        (map (lambda (t) (cons (car s) t)) 
                             (if (even? (cas s))
                                    (even-subsets (cdr s))
                                    (odd-subsets (cdr s)) ))
                        (if (even? (car s)) (list (list (car s))) nil))))

(define (odd-subsets s)
  (if (null? s) nil 
      			(append (odd-subsets (cdr s)) 
                        (map (lambda (t) (cons (car s) t)) 
                             (if (odd? (cas s))
                                    (even-subsets (cdr s))
                                    (odd-subsets (cdr s)) ))
                        (if (odd? (car s)) (list (list (car s))) nil))))
````

# Exceptions 异常

### python里的异常

````python
raise <expression> #提出某个异常
````

expression必须是异常基类的子类或者是异常类的实例

异常和其他对象的构造方式一样

````python
TypeError('Bad argument!')
````

- TypeError: 参数数量或者类型错误
- NameError: name找不到
- KeyError: 字典里没有这个key
- RecursionError: 递归次数太多

一般会自动触发，也可用raise手动触发

#### Try语句

用Try语句来处理异常

````python
try:
    <try suite>
except <exception class> as <name>:
    <except suite>
...
````

执行规则：

- 先执行< try suite >, 如果没有错误，就结束了
- 如果引发了异常：在引发异常处中断，如果这个异常在except里面：将这个异常赋值给name，执行这个except里面的语句，且不会报错。否则就报错

````python
>>> try :
		x = 1 / 0
    except ZeroDivisionError as e:
        print('handling a', type(e))
        x = 0
        
handling a <class 'ZeroDivisionError'>
>>> x
0
````

# 编程语言与解释器

高级语言提供抽象的手段，如函数等

编程语言有：

- 语法syntax：合法的语句和表达式
- 语义Semantics：执行规则for语句和表达式

创建一个新编程语言需要：

- 规范：一个文档描述具体的语法和语义
- 实现：一个该语言的解释器或者编译器

## Parsing 解析

### 解析Scheme列表

一个Scheme列表被以括号的形式写出来(< 元素0 >< 元素1 >...< 元素n >)

内部结构都是链表的结构

每个元素都可以是组合或者基本元素

解析语言的任务要将一串字符串表示，转化为表达式

### 一个解析器接受文本返回表达式

![image-20260201201501319](.\screenshot\image-20260201201501319.png)

语法解释是一种树型递归过程

它分析表达式的层级结构

每次调用scheme_read消耗一个token

'(', '+', 1, '(', '-', 23, ')', '(', '*', 4, 5.6, ')', ')'

**基本情况**：symbols和数字

**递归调用**：scheme_read子表达式并组合他们 

## Read-Eval-Print Loop

一个interactive interpreter:

- Print a prompt显示提示
- **Read** text input
- Prase the text into an expression
- **Evaluate** the expression
- 如果发生错误报告错误，否则
- **Print** the value of the expression and repeat

## 处理异常 Handling Exceptions

一个交互式解释器打印信息关于每个报错

一个良好的交互式解释器不应该崩溃因为一个报错，应该停止评估该表达式并打印错误，以便用户能重新修改错误

## 引用

引用不会被评估

````scheme
(quote <expression>)
==
'<expression> ...简写
````

实际在read时会将'expression转化为(quote < expression >)

## 作用域Scope

- Lexical scope词法作用域：帧的父级是过程被**defined**的环境
- Dynamic scope动态作用域：帧的父级是过程被**called**的环境

 大多数都是词法作用域 包括python和scheme

# 函数式编程

只用函数完成编程，这些函数是模块化的，可以以有趣的方式组合

- 所有函数是纯函数，无副作用
- 没有重新赋值，没有可变数据类型
- 名称-值绑定是永久的

好处：

- 表达式的值与子表达式评估的顺序无关
- 如果有多个不同的处理单元，可以并行评估子表达式
- 引用透明性：当用一个子表达式的值替换表达式的这个子表达式时，表达式的值不会改变(可进行记忆化等操作)

但是...没有for/while语句！如何让迭代更快？（递归很慢）

## 递归和迭代 在python

在python，每次递归调用会创建新帧，导致递归的空间复杂度会比迭代大

## 尾递归 tail recursion

Scheme的实现必须是尾递归，在Scheme中的递归占用的空间复杂度应该和迭代是一样的！

做法：淘汰中间不需要的帧

## 尾调用

如果除了返回表达式的值以外没有其他任何事情做，则为尾调用

一个尾调用是一个在尾上下文中的调用表达式。

- lambda表达式中的最后一个子表达式(确定返回值的)
- 如果整个 `if` 表达式本身处于“尾上下文”中，那么它的第 2 个和第 3 个参数也自动处于“尾上下文”中。
- 尾上下文中非谓词(predicate)cond表达式的每个字句的最后一个调用
- 尾上下文中and or的最后一个表达式
- 尾上下文中begin的最后一个表达式

一个调用不是尾调用，如果在调用时还要进行计算，比如

````scheme
(define (length s)
  (if (null? s) 0
      (+ 1 (length (cdr s)))))
````

这个的最后一句不是尾调用，因为还要加1，要有空间来存这个加1

把它变成尾调用：

````scheme
(define (length-tail s)
  (define (length-iter s n)
    (if (null? s) n
      (length-iter (cdr s) (+ 1 n) ) ) ) 
  (length-iter s 0))
````

## 蹦床(Trampolining)优化实现尾递归

在python中，是不支持尾调用优化的，要实现尾调用，可以使用蹦床优化。

他将处于尾上下文的函数调用出储存为Thunk，先不调用，在需要的时候才执行这些Thunk。

该方法的基本单元是 Thunk，它代表一个未求值的操作。最简单的Thunk：

````python
my_thunk = lambda: sqrt(16384) + 22
my_thunk2 = lambda: some_costly_operation(1000)
````

而在后续为了拆开这些自动嵌套的Thunk，我们常写一个循环:

````python
def trampoline(value):
    while callable(value): #只要还是Thunk(一个未执行的函数)
        value = value()
    return value
````

实现python的阶乘尾递归优化：

````python
def thunk_factorial(n, so_far=1):
    def thunk():
        if n == 0:
            return so_far
        return thunk_factorial(n - 1, so_far * n)
    return thunk

def factorial(n):
    value = thunk_factorial(n)
    while callable(value):
        value = value()
    return value
````

#  程序是数据

Scheme程序由表达式组成，表达式可以是：

- 基本表达式
- 组合

内置list数据结构(类似链表)可以表示组合

所以可以用scheme**写一个写程序的程序**

````scheme
>>> (list '+ 1 2)
(+ 1 2)
>>> (eval (list '+ 1 2)) ;要个+前面带个'，让解释器把它当成一个符号不评估，否则解释器会评估+导致再评估的时候评估不了了
3
````

````scheme
(define (fact n)
  (if (= 0 n) 1 (* n (fact (- n 1)))))
;计算阶乘的函数(计算出结果)
(define (fact-exp n) 
  (if (= 0 n) 1 (list '* n (fact (- n 1)))))
;返回一个计算阶乘的表达式

scm> (fact 5)
120
scm> (fact-exp 5)
(* 5 (* 4 (* 3 (* 2 (* 1 1)))))
scm> (eval(fact-exp 5))
120
````

## 准引用 Quasiquotation

两种引用方法：

- **Quote:** `'(a b)` => `(a b)`
- **Quasiquotaion:** ``(a b)` => `(a b)`

大部分时候一样，但是准引用表达式的一部分是可以被 **`,`**取消引用的

例：

`(define b 4)`

- **Quote:** `'(a ,(+ b 1))` => `(a (unquote (+ b 1)))`将这个取消引用也引引用了
- **Quasiquote:** ``(a ,(+ b 1))` => `(a 5)` 

准引用对生成Scheme表达式很方便

#### 例：While语句

如果你要写while语句来计算和，比如计算平方小于50的数的和，或者计算小于10的偶数的平方和，你可以写一个泛化的程序

````scheme
(define (sum-while initial-x condition add-to-total update-x)
  `(begin 
   (define (f x total)
     (if ,condition
         (f ,update-x (+ total ,add-to-total))
         total) 
     )
   (f ,initial-x 0))
  )
;返回一个begin表达式，这是一个列表，也是一个程序(可以被评估)
;注意传入的需要是引用
````

取消引用：这是因为在最前面添加了`，所以返回的是一个引用，如果不解引用，返回的就会变成原原本本的condition而不是你传入的参数的语句了，所以要解除引用。

传入的参数：必须也是一个引用，不然在评估的时候就要报错了

例：

````scheme
scm> (sum-while 2 '(< x 10) '(* x x) '(+ x 2))
(begin (define (f x total) (if (< x 10) (f (+ x 2) (+ total (* x x))) total)) (f 2 0))

scm> (eval (sum-while 2 '(< x 10) '(* x x) '(+ x 2)))
120
````

# Macros 宏

可以创造新的特殊形式，创建新的评估方式

## 宏执行代码转换

宏是程序的源代码在**被评估之前**对其做的操作。

Scheme有一个特殊形式：**define-macro**，允许定义源代码的转换

````scheme
(define-macro (twice expr)
              (list 'begin expr expr))
````

````scheme
>(twice (print 2)) ;=> (begin (print 2) (print 2))
2
2
````

在评估之前就转换为了后面那个，再评估的

评估宏调用表达式：

1. 评估operaor子表达式，评估为一个macro
2. 对operands调用这个macro procedure，先不评估operands
3. 评估从macro procedure返回的整个表达式

总之是先变了表达式再评估

````scheme
(define-macro (check expr) (list 'if expr ''passed 
                           (list 'quote(list 'failed: expr))))
````

等价于：

````scheme
(define-macro (check expr) `(if ,expr 'passed 
                                '(failed: ,expr)))
````

````scheme
scm> (define x -2)
x
scm> (check (> x 0))
(failed: (> x 0))
````

如果去掉-macro,使用普通define：

````scheme
(define (check expr) `(if ,expr 'passed 
                                '(failed: ,expr)))
````

````scheme
scm> (check '(> x 0))
(if (> x 0) (quote passed) (quote (failed: (> x 0))))
scm> (eval (check '(> x 0)))
(failed: (> x 0))
````

返回的是一个列表，要再评估才能得到我们想要的

## 例：创建for宏

我们像定义一个宏，对序列内每个值调用表达式

map过程：

````scheme
(define (map fn vals)
  (if (null? vals) ()
      (cons (fn (car vals))
            (map fn (cdr vals)))))
````

````scheme
scm> (map (lambda (x) (* x x)) '(2 3 4 5))
(4 9 16 25)
````

使用宏：

````scheme
(define-macro (for sym vals expr)
              `(map (lambda (,sym) ,expr) ,vals))
;or;
(define-macro (for sym vals expr)
              (list 'map (list 'lambda (list sym) expr) vals))
````

````scheme
scm> (for x '(2 3 4 5) (* x x))
(4 9 16 25)
````

## 例：Trace

在python中我们用装饰器实现Trace：

````python
def trace(fn):
    def traced(n):
        print(f'{fn.__name__}({n})')
        return fn(n)
    return traced

@trace
def fact(n):
    if n == 0:
        return 1
    else :
        return n * fact(n - 1)
````

在scheme中:

````scheme
(define (fact n) (if (zero? n) 1 (* n (fact (- n 1)))))
(define original fact)
(define (fact n) (print `(fact ,n)) (original n) )
````

````scheme
scm> (fact 5)
(fact 5)
(fact 4)
(fact 3)
(fact 2)
(fact 1)
(fact 0)
120
````

(如果original符号被赋值为其他，这个fact就废了)

宏：

````scheme
(define-macro (trace expr) ;(trace (fact 5))
  (define operator (car expr)) ;fact
  `(begin 
		(define original ,operator)
    	(define ,operator (lambda (n)
                            (print (list ',operator n))
                            (original n)))
    	(define result ,expr)
    	(define ,operator original)
    	result))
````

## 例：repeat

````scheme
 (define-macro (my-repeat times expr) 
               (cond ((= 1 times) expr) 
                     (else (list 'begin expr `(my-repeat ,(- times 1) ,expr)))))
````

