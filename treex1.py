import myglobal
from tinter import *

def ex1 (debugging = False):
    inTre(createTre(title="Ex1", debugging = debugging))
    forms = ['(rule (implies ?ante ?conse) (rule ?ante (assert! ?conse)))',
             '(rule (not (not ?x)) (assert! ?x))']
    runForms(myglobal._tre_, forms)

if __name__ == '__main__':
    ex1(False)
    print(myglobal._tre_.title)