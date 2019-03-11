import myglobal
from tinter import *
import rules as rules
import warnings

Symbol = str    # A Lisp Symbol is implemented as a Python str
myglobal._env_ = None

class DbClass(object):

    def __init__(self, name=None, tre=None, facts=[], rules=[]):
        self.name = name
        self.tre = tre
        self.facts = facts
        self.rules = rules

def showData():
    """
    Print out whole facts
    :return: counter
    """
    counter = 0
    for key,dbclass in myglobal._tre_.dbclassTable.items():
        for datum in dbclass.facts:
            counter += 1
            print("Fact #", counter, "=>", datum)
    return counter

def getDbClass(fact, tre):
    if fact == None:
        warnings.warn("nil can't be a dbclass!")
    elif isinstance(fact, list):
        return getDbClass(fact[0], tre)
    elif isinstance(fact, Symbol):
        dbclass = tre.dbclassTable[fact] if fact in tre.dbclassTable else None
        if dbclass != None:
            return dbclass
        else:
            dbclass = DbClass(name=fact, tre=tre, facts=[], rules=[])
            tre.dbclassTable[fact] = dbclass
            return dbclass

def getCandidates(pattern, tre):
    """
    Retrieve all facts from the dbclass of a given pattern
    :param pattern:
    :param tre:
    :return:
    """
    return getDbClass(pattern, tre).facts

# Installing new facts
def assertFact(fact, tre=None):
    if tre == None:
        tre = myglobal._tre_
    if insertFact(fact, tre) == True:     # When it isn't already there
        rules.tryRules(fact, tre)               # run the rules on it

def insertFact(fact, tre):
    """
    Insert a single fact into the database
    :param fact:
    :param tre:
    :return:
    """
    dbclass = getDbClass(fact, tre)
    if fact not in dbclass.facts:
        if tre.debugging:
            print(tre, 'Inserting',fact,'into database.')
        dbclass.facts.append(fact)
        return True
    return False

if __name__ == '__main__':
    a = [1,3,4]
    b = [[1,2,3], [1,3,4]]
    print(a in b)