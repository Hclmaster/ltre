import myglobal
from tinter import *
from data import *
from unify import *

Symbol = str    # A Lisp Symbol is implemented as a Python str

class Rule(object):

    def __init__(self, counter=0, dbclass=None, trigger=None,
                 body=None, environment={}):
        self.counter = counter
        self.dbclass = dbclass
        self.trigger = trigger
        self.body = body
        self.environment = environment

def showRules():
    """
    Print a list of all rules within the default tre.
    :return:
    """
    counter = 0
    for key,dbclass in myglobal._tre_.dbclassTable.items():
        for rule in dbclass.rules:
            counter += 1
            printRule(rule)
    return counter

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
    elif x[0] == Symbol('assert!'):
        assertFact(x[1:][0])

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
        tryRuleOn(rule, candidate, myglobal._tre_)


def printRule(rule):
    """
    Print representation of rule
    :param rule:
    :return:
    """
    print("Rule #", rule.counter, rule.trigger, rule.body)

def tryRules(fact, tre):
    #print('tryRules Fact => ', fact)
    for rule in getCandidateRules(fact, tre):
        #printRule(rule)
        tryRuleOn(rule, fact, tre)

def getCandidateRules(fact, tre):
    """
    Return lists of all applicable rules for a given fact
    :param fact:
    :param tre:
    :return:
    """
    return getDbClass(fact, tre).rules

def tryRuleOn(rule, fact, tre):
    """
    Try a single rule on a single fact
    If the trigger matches, queue it up
    :param rule:
    :param fact:
    :param tre:
    :return:
    """
    #print('tryRuleOn ====== ')
    #print('rule trigger => ', rule.trigger, ' fact => ', fact)
    #print('rule environment => ', rule.environment)
    bindings = unify(fact, rule.trigger, rule.environment)
    print('bindings => ', bindings)

    if bindings != None:
        enqueue([rule.body, bindings], tre)

def runRules(tre):
    counter = 0
    while len(tre.queue) > 0:
        rulePair = dequeue(tre)
        counter += 1
        runRule(rulePair, tre)

    if tre.debugging:
        print('Total', counter, 'rules run!')

# It's a LIFO queue
def enqueue(new, tre):
    tre.queue.append(new)

def dequeue(tre):
    if len(tre.queue) > 0:
        return tre.queue.pop()
    else:
        return None

def runRule(pair, tre):
    """
    Here pair is ([body], {bindings})
    :param pair:
    :param tre:
    :return:
    """
    myglobal._env_ = pair[1]
    myglobal._tre_ = tre

    tre.rules_run += 1

    print("======= run Rule Part =========")
    print('pair[0] => ', pair[0])
    print('pair[1] => ', pair[1])

    newBody = pair[0].copy()
    for item in newBody:
        for key, value in pair[1].items():
            if key in item:
                item[item.index(key)] = value

    print('pair => ', pair)
    print('newBody => ', newBody)
    eval(newBody[0])


if __name__ == '__main__':
    forms = ['(rule (implies ?ante ?conse) (rule ?ante (assert! ?conse)))',
             '(rule (not (not ?x)) (assert! ?x))']
    """
    for form in forms:
        print('form => ', form)
        print("tokenize result ======>")
        print(tokenize(form))
        print("parse result =====> ")
        print(parse(form))
    """

    print('========================')
    t = []
    lst = [['implies', '?ante', '?conse'], {'?x': 1, '?y': 2}]
    t.append(lst)
    print(t)

    t.append(lst)
    print(t)