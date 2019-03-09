import myglobal
from tinter import *

def ex1 (debugging = False):
    ex1Tre = inTre(createTre(title="Ex1", debugging = debugging))
    forms = ['(rule (implies ?ante ?conse) (rule ?ante (assert! ?conse)))',
             '(rule (not (not ?x)) (assert! ?x))']
    runForms(forms)

if __name__ == '__main__':
    ex1(False)
    print(myglobal._tre_.title)