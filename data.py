import myglobal
from tinter import *
import warnings

Symbol = str    # A Lisp Symbol is implemented as a Python str
myglobal._env_ = None

class DbClass(object):

    def __init__(self, name=None, tre=None, facts=[], rules=[]):
        self.name = name
        self.tre = tre
        self.facts = facts
        self.rules = rules


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