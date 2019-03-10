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
        dbclass = tre.dbclassTable[fact]
        if dbclass != None:
            return dbclass
        else:
            dbclass = DbClass(name=fact, tre=tre, facts=[], rules=[])
            tre.dbclassTable[fact] = dbclass

"""
if __name__ == '__main__':
    v = '?x'
    print(isinstance(v, Symbol))
    v = [1,2,3]
    print(isinstance(v, list))
    v = []
    v.append(1)
    print(v)
"""