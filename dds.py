import warnings
from lrules import *
import copy

def solveCryptarithmeticProblem():
    sendMoreMoney = [
        ['column 1 D E Y'],
        ['column 2 N R E'],
        ['column 3 E O N'],
        ['column 4 S M O'],
        ['column 5 :blank :blank M'],
        ['leftmost-column 5']
    ]

    choiceSets = makeLetterChoiceSets(sendMoreMoney)
    return choiceSets

def makeLetterChoiceSets(problem):
    """
    Form a possible choice sets letters
    :param problem:
    :return:
    """
    choiceSets = []

    for letter in set(extractProblemLetters(problem)):
        dict = {}
        letterSet = []
        for i in range(0, 10):
            letterSet.append({letter: i})
        choiceSets.append(letterSet)

    print(choiceSets)
    return choiceSets


def extractProblemLetters(problem):
    """
    Extract all letters inside the problem except ':blank'
    :param problem:
    :return:
    """
    letters = []

    for line in problem:
        for letter in line[0].split()[1:]:
            if letter != ':blank' and letter.isalpha():
                letters.append(letter)

    return letters

def ddSearch(choiceSets, level=0, stack=[[]]):
    #print('level ==> ', level)
    if choiceSets == None or choiceSets == []:
        #print('***********************************************************')
        #print('A feasible ddsearch solution is:')
        #print('level =', level, ' stack =', stack[level-1])
        return
    choices = choiceSets[0]

    for choice in choices:
        if len(stack) >= level + 1:
            if level == 0:
                stack[level] = []
                stack[level].append(reformatPhrase(choice))
            else:
                stack[level] = copy.deepcopy(stack[level-1])
                stack[level].append(reformatPhrase(choice))
        else:
            stack.append([])
            stack[level] = copy.deepcopy(stack[level-1])
            stack[level].append(reformatPhrase(choice))

        # if true, then ddsearch, otherwise, contradition!!!
        if withContradictionHandler(level, stack[level]) == True:
            ddSearch(choiceSets[1:], level+1, stack)

def withContradictionHandler(level, stack):
    #print('level = ', level, ' stack = ', stack)
    flag = 0

    for lst in stack:
        dbclass = getDbClass(lst[0], myglobal._ltre_)
        for nogoodfact in dbclass.notFacts:
            bindings = unify(lst, nogoodfact)
            if bindings != None:
                print('=================================================')
                print('Making Contradition!!!!!!')
                print('level = ', level, ' stack = ', stack)
                tmp = [':not']
                tmp.append(nogoodfact)
                print('Assumption:', lst, ' Facts: ', tmp)
                flag = 1
                break
        if flag:
            break

    return True if flag == 0 else False


#### Need to be modified!!! Because different phrase has different format!!!!!! ####
def reformatPhrase(choice):
    phrases = []
    for attribute, object in choice.items():
        return parse('('+attribute+' '+object+')')



if __name__ == '__main__':
    #solveCryptarithmeticProblem()

    #choiceSets = solveCryptarithmeticProblem()
    #ddSearch(choiceSets)

    ss = [['a','b','c']]
    ss[0] = []
    ss[0].append([1,2,3])
    print(ss)