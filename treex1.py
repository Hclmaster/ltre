import myglobal
from tinter import *

def ex1 (debugging = False):
    inTre(createTre(title="Ex1", debugging = debugging))
    forms = ['(rule (implies ?ante ?conse) (rule ?ante (assert! ?conse)))',
             '(rule (not (not ?x)) (assert! ?x))',
             '(assert! (implies (human Turing) (mortal Turing)))',
             '(assert! (not (not (human Turing))))']
    runForms(myglobal._tre_, forms)

def ex2 (debugging = False):
    inTre(createTre(title="Ex2", debugging = debugging))
    _parts_ = None
    forms = ['(rule (has-part ?sys ?part) (let ((entry (assoc ?sys _parts_))) (unless entry (push (setq entry (cons ?sys nil)) _parts_)) (pushnew ?part (cdr entry))))',
             '(rule (Car ?c) (assert! (has-part ?c (Engine ?c))) (assert! (has-part ?c (Body ?c))) (assert! (has-part ?c (Chasis ?c))))',
             '(rule (Workstation ?c) (assert! (has-part ?c (Disk ?c))) (assert! (has-part ?c (Screen ?c))) (assert! (has-part ?c (CPU-box ?c))) (assert! (has-part ?c (Keyboard ?c))))',
             '(assert! (Car Ariel))',
             '(assert! (Workstation Hal-9000))']
    runForms(myglobal._tre_, forms)
    print(_parts_)

if __name__ == '__main__':
    # Ex1

    ex1(False)
    print('******** Show Rules Part *********')
    totalRules = showRules()
    print('totalRules =', totalRules)
    print('******** Show Data Part *********')
    totalData = showData()
    print('totalData =', totalData)
    

    # Ex2
    #ex2(False)
    """
    forms = [
        '(rule (has-part ?sys ?part) (let ((entry (assoc ?sys _parts_))) (unless entry (push (setq entry (cons ?sys nil)) _parts_)) (pushnew ?part (cdr entry))))',
        '(rule (Car ?c) (assert! (has-part ?c (Engine ?c))) (assert! (has-part ?c (Body ?c))) (assert! (has-part ?c (Chasis ?c))))',
        '(rule (Workstation ?c) (assert! (has-part ?c (Disk ?c))) (assert! (has-part ?c (Screen ?c))) (assert! (has-part ?c (CPU-box ?c))) (assert! (has-part ?c (Keyboard ?c))))',
        '(assert! (Car Ariel))',
        '(assert! (Workstation Hal-9000))']

    for form in forms:
        print('form =', form)
    """