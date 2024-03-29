import math
import operator as op
from collections import ChainMap as Environment
import myglobal
import copy
from ltinter import *

Symbol = str          # A Lisp Symbol is implemented as a Python str
List   = list         # A Lisp List   is implemented as a Python list
Number = (int, float) # A Lisp Number is implemented as a Python int or float

class Procedure(object):
    "A user-defined Scheme procedure."
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env
    def __call__(self, *args):
        env =  Environment(dict(zip(self.parms, args)), self.env)
        return eval(self.body, env)

################ Global Environment

def standard_env():
    "An environment with some Scheme standard procedures."
    env = {}
    env.update(vars(math)) # sin, cos, sqrt, pi, ...
    env.update({
        '+':op.add, '-':op.sub, '*':op.mul, '/':op.truediv,
        '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq,
        'abs':     abs,
        'append':  op.add,
        'apply':   lambda proc, args: proc(*args),
        'begin':   lambda *x: x[-1],
        'car':     lambda x: x[0],
        'cdr':     lambda x: x[1:],
        'cons':    lambda x,y: [x] + y,
        'eq?':     op.is_,
        'equal?':  op.eq,
        'length':  len,
        'list':    lambda *x: list(x),
        'list?':   lambda x: isinstance(x,list),
        'map':     lambda *args: list(map(*args)),
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?':   lambda x: x == [],
        'number?': lambda x: isinstance(x, Number),
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env

global_env = standard_env()

################ Parsing: parse, tokenize, and read_from_tokens

def parse(program):
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(program))

def tokenize(s):
    "Convert a string into a list of tokens."
    return s.replace('(',' ( ').replace(')',' ) ').split()

def read_from_tokens(tokens):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token):
    "Numbers become numbers; every other token is a symbol."
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)

################ Interaction: A REPL

def repl(prompt='lis.py> '):
    "A prompt-read-eval-print loop."
    while True:
        val = eval(parse(input(prompt)))
        if val is not None:
            print(lispstr(val))

def lispstr(exp):
    "Convert a Python object back into a Lisp-readable string."
    if isinstance(exp, List):
        return '(' + ' '.join(map(lispstr, exp)) + ')'
    else:
        return str(exp)

################ eval

def eval(x, env=global_env):
    "Evaluate an expression in an environment."
    if isinstance(x, Symbol):      # variable reference
        return env[x]
    elif not isinstance(x, List):  # constant literal
        return x
    elif x[0] == 'quote':          # (quote exp)
        (_, exp) = x
        return exp
    elif x[0] == 'if':             # (if test conseq alt)
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == 'define':         # (define var exp)
        (_, var, exp) = x
        env[var] = eval(exp, env)
    elif x[0] == 'lambda':         # (lambda (var...) body)
        (_, parms, body) = x
        return Procedure(parms, body, env)
    else:                          # (proc arg...)
        proc = eval(x[0], env)
        args = [eval(exp, env) for exp in x[1:]]
        return proc(*args)

def bindVar(lst, bindings):
    for item in lst:
        for key, value in bindings.items():
            if key in item:
                item[item.index(key)] = value
        if any(isinstance(item, list) for i in item):
            item = bindVar(item, bindings)

    return lst

def change(ltre):
    ltre = 3


if __name__ == '__main__':
    #print(global_env)
    #print(parse("(begin (define r 10) (* pi (* r r)))"))
    #print(eval(parse("(if (> 10 20) (+ 1 1) (+ 3 3))")))
    #print(eval(parse("(eq? 1 1)")))

    """
    bindings = {'?a': 'sam', '?b': 'sam'}
    lst = ['when', ['eql', '?a', '?b'], ['rassert!', [':not', [':and', ['plays-piano', '?a'], ['plays-harp', '?b']]]]]

    print(bindVar(lst, bindings))

    aa = ['rassert!', [':not', [':and', ['plays-piano', '?a'], ['plays-harp', '?b']]]]
    ff = 'when'
    print(any(isinstance(i, list) for i in ff))
    print(any(isinstance(i, list) for i in aa))
    """

    ex1 = createLtre(title="Ex1", debugging=False)
    print(ex1.title)

    ex2 = copy.deepcopy(ex1)
    ex2.title = "Ex2"

    lst = []
    lst.append(ex1)

    idx = len(lst)

    lst.append(copy.deepcopy(lst[idx-1]))
    print(lst)

    lst[1].title = 'hahah'

    print(lst[0].title)

    global t;
    t = 1
    change(t)
    print(t)