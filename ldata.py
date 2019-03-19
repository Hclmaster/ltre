import myglobal
from ltinter import *
import lrules as rules
import warnings

Symbol = str    # A Lisp Symbol is implemented as a Python str
myglobal._lenv_ = None

class DbClass(object):

    def __init__(self, name=None, ltre=None, facts=[], rules=[], notFacts=[]):
        self.name = name
        self.ltre = ltre
        self.facts = facts
        self.rules = rules
        self.notFacts = notFacts

def showData():
    """
    Print out whole facts
    :return: counter
    """
    counter = 0
    for key,dbclass in myglobal._ltre_.dbclassTable.items():
        for datum in dbclass.facts:
            counter += 1
            print("Fact #", counter, "=>", datum)
    return counter

def getDbClass(fact, ltre):
    if fact == None:
        warnings.warn("nil can't be a dbclass!")
    elif isinstance(fact, list):
        return getDbClass(fact[0], ltre)
    elif isinstance(fact, Symbol):
        dbclass = ltre.dbclassTable[fact] if fact in ltre.dbclassTable else None
        if dbclass != None:
            return dbclass
        else:
            dbclass = DbClass(name=fact, ltre=ltre, facts=[], rules=[], notFacts=[])
            ltre.dbclassTable[fact] = dbclass
            return dbclass

def getCandidates(pattern, ltre):
    """
    Retrieve all facts from the dbclass of a given pattern
    :param pattern:
    :param ltre:
    :return:
    """
    return getDbClass(pattern, ltre).facts

# Installing new facts
def assertFact(fact, ltre=None):
    if ltre == None:
        ltre = myglobal._ltre_

    #print('assertFact fact = ', fact)

    #### Store the False facts explicitly (like false node)
    if fact[0] == ':not':
        if insertNoGoodFact(fact[1:][0], ltre) == True:
            rules.tryRules(fact, ltre)

    if insertFact(fact, ltre) == True:     # When it isn't already there
        rules.tryRules(fact, ltre)               # run the rules on it

def insertFact(fact, ltre):
    """
    Insert a single fact into the database
    :param fact:
    :param ltre:
    :return:
    """
    dbclass = getDbClass(fact, ltre)
    if fact not in dbclass.facts:
        if ltre.debugging:
            print(ltre, 'Inserting',fact,'into database.')
        dbclass.facts.append(fact)
        return True
    return False

def insertNoGoodFact(nogoodfact, ltre):
    """
    Insert a single not fact into the database
    :param nogoodfact:
    :param ltre:
    :return:
    """
    dbclass = getDbClass(nogoodfact, ltre)
    if nogoodfact not in dbclass.notFacts:
        if ltre.debugging:
            print(ltre, 'Inserting',nogoodfact,'into database.')
        dbclass.notFacts.append(nogoodfact)
        return True
    return False

if __name__ == '__main__':
    a = [1,3,4]
    b = [[1,2,3], [1,3,4]]
    print(a in b)