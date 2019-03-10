import myglobal
from tinter import *
from data import *

Symbol = str    # A Lisp Symbol is implemented as a Python str

class Rule(object):

    def __init__(self, counter=0, dbclass=None, trigger=None,
                 body=None, environment=None):
        self.counter = counter
        self.dbclass = dbclass
        self.trigger = trigger
        self.body = body
        self.environment = environment


def tokenize(chars: str) -> list:
    return chars.replace('(', '( ').replace(')', ' )').split()

def parse(program: str):
    return read_from_tokens(tokenize(program))

def read_from_tokens(tokens: list):
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)
        return L
    elif token == ')':
        raise SyntaxError('unexcepted )')
    else:
        return atom(token)

def atom(token: str):
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)

#### eval
def eval(x):
    # all values in the parse result list are symbol!
    if x[0] == Symbol('rule'):
        addRule(x[1], x[2:])

def addRule(trigger, body):
    # First build the struct
    myglobal._tre_.rule_counter += 1
    rule = Rule(trigger=trigger, body=body,
                counter=myglobal._tre_.rule_counter, environment=myglobal._env_)

    # Now index it
    dbclass = getDbClass(trigger, myglobal._tre_)
    dbclass.rules.append(rule)
    rule.dbclass = dbclass
    print("====== debugging the tre with New Rule =======")
    printRule(rule)

    # Go into the database and see what it might trigger on
    for candidate in getCandidates(trigger, myglobal._tre_):
        pass


def printRule(rule):
    """
    Print representation of rule
    :param rule:
    :return:
    """
    print("Rule #", rule.counter, rule.trigger, rule.body)


if __name__ == '__main__':
    forms = ['(rule (implies ?ante ?conse) (rule ?ante (assert! ?conse)))',
             '(rule (not (not ?x)) (assert! ?x))']

    for form in forms:
        print('form => ', form)
        print("tokenize result ======>")
        print(tokenize(form))
        print("parse result =====> ")
        print(parse(form))