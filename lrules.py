import myglobal
from ltinter import *
from ldata import *
from lunify import *
import copy

Symbol = str    # A Lisp Symbol is implemented as a Python str

class Rule(object):

    def __init__(self, counter=0, dbclass=None, trigger=None,
                 body=None, environment={}, label=[]):
        self.counter = counter
        self.dbclass = dbclass
        self.trigger = trigger
        self.body = body
        self.environment = environment
        self.label = label

def standard_env():
    """
    An environment with some Lisp standard procedure
    :return:
    """
    pass


def showRules():
    """
    Print a list of all rules within the default ltre.
    :return:
    """
    counter = 0
    for key,dbclass in myglobal._ltre_.dbclassTable.items():
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
    elif x[0] == Symbol('rassert!'):
        assertFact(x[1:][0])

def addRule(trigger, body):
    # First build the struct
    myglobal._ltre_.rule_counter += 1
    rule = Rule(trigger=trigger, body=body,
                counter=myglobal._ltre_.rule_counter, environment=myglobal._env_)

    # Now index it
    dbclass = getDbClass(trigger, myglobal._ltre_)
    dbclass.rules.append(rule)
    rule.dbclass = dbclass
    #print("====== debugging the ltre with New Rule =======")
    #printRule(rule)

    # Go into the database and see what it might trigger on
    for candidate in getCandidates(trigger, myglobal._ltre_):
        tryRuleOn(rule, candidate, myglobal._ltre_)


def printRule(rule):
    """
    Print representation of rule
    :param rule:
    :return:
    """
    print("Rule #", rule.counter, rule.trigger, rule.body)

def tryRules(fact, ltre):
    #print('tryRules Fact => ', fact)
    for rule in getCandidateRules(fact, ltre):
        #printRule(rule)
        tryRuleOn(rule, fact, ltre)

def getCandidateRules(fact, ltre):
    """
    Return lists of all applicable rules for a given fact
    :param fact:
    :param ltre:
    :return:
    """
    return getDbClass(fact, ltre).rules

def tryRuleOn(rule, fact, ltre):
    """
    Try a single rule on a single fact
    If the trigger matches, queue it up
    :param rule:
    :param fact:
    :param ltre:
    :return:
    """
    #print('tryRuleOn ====== ')
    #print('rule trigger => ', rule.trigger, ' fact => ', fact)
    #print('rule environment => ', rule.environment)
    #print('rule len => ', rule.trigger)
    #print('fact len => ', fact)

    if len(rule.trigger) != len(fact):
        return None
    elif len(rule.trigger) > 1:
        bindings = rule.environment
        for idx in range(len(rule.trigger)):
            #print('rule idx => ', rule.trigger[idx])
            #print('fact idx => ', fact[idx])
            #print(len(fact[idx]))
            bindings = unify(fact[idx], rule.trigger[idx], bindings)
    else:
        bindings = unify(fact, rule.trigger, rule.environment)

    #print('bindings ???? ', bindings)

    if bindings != None:
        enqueue([rule.body, bindings], ltre)

def runRules(ltre):
    counter = 0
    #print('runRules length ===> ', len(ltre.queue))
    while len(ltre.queue) > 0:
        rulePair = dequeue(ltre)
        counter += 1
        runRule(rulePair, ltre)

    if ltre.debugging:
        print('Total', counter, 'rules run!')

# It's a LIFO queue
def enqueue(new, ltre):
    ltre.queue.append(new)

def dequeue(ltre):
    if len(ltre.queue) > 0:
        return ltre.queue.pop()
    else:
        return None

def runRule(pair, ltre):
    """
    Here pair is ([body], {bindings})
    :param pair:
    :param ltre:
    :return:
    """
    myglobal._env_ = pair[1]
    myglobal._ltre_ = ltre

    ltre.rules_run += 1

    #print("======= run Rule Part =========")
    #print('body ===> ', pair[0])
    #print('bindings => ', pair[1])
    newBody = copy.deepcopy(pair[0])

    for item in newBody:
        for key, value in pair[1].items():
            if key in item:
                item[item.index(key)] = value

    #print('pair => ', pair)
    #print('newBody => ', newBody)
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