import myglobal
from ltinter import *
from lrules import *

def ex1 (debugging = False):
    inLtre(createLtre(title="Ex1", debugging = debugging))
    forms = ['(rassert! (:not plays-piano plays-harp))',
             '(rassert! (:not plays-piano smooth-talker))',
             '(rassert! (:not plays-harp smooth-talker))',
             '(rassert! (:true plays-piano plays-harp))']
    runForms(myglobal._ltre_, forms)

if __name__ == '__main__':
    #ex1()

    forms = [
        '(rule ((:true (value-of ?a ?n)) (:true (value-of ?c ?m))) ' +
        '(when (and (not (eql ?a :blank)) (not (eql ?c :blank)) ' +
        '(not (eql ?a ?c))) (rassert! (:not (:and  (value-of ?a ?n) (value-of ?c ?n))))))',
        '(rassert! ((:true (value-of A 0)) (:true (value-of C 1))))'
    ]

    inLtre(createLtre(title="Ex1", debugging=False))

    for form in forms:
        parsedForm = parse(form)
        #print(parsedForm)
        #eval(parsedForm)
        runForms(myglobal._ltre_, forms)

    showRules()
    showData()