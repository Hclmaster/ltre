import math
import operator as op
from collections import ChainMap as Environment

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
    env.update({
        'mod':op.mod,
        '+':op.add, '-':op.sub, '*':op.mul, '/':op.truediv,
        '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq,
        'eql':op.eq
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
        if x in env:
            return env[x]
        else:
            return x
    elif not isinstance(x, List):  # constant literal
        return x
    elif x[0] == 'if':             # (if test conseq alt)
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)
    elif x[0] == 'when':
        (_, test, conseq) = x
        exp = (conseq if eval(test, env) else None)
        return eval(exp, env)
    else:                          # (proc arg...)
        proc = eval(x[0], env)
        args = [eval(exp, env) for exp in x[1:]]
        return proc(*args)


if __name__ == '__main__':
    #print(global_env)
    print(parse("(when (eql sam sam) (* pi (* 3 3)))"))
    print(eval(parse("(when (eql sam sam) (* 4 (* 3 3)))")))
    #print(eval(parse("(if (> 10 20) (+ 1 1) (+ 3 3))")))