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
    print('level ==> ', level)
    if choiceSets == None or choiceSets == []:
        warnings.warn('DDS Found no solution!')
        return
    choices = choiceSets[0]

    for choice in choices:
        if len(stack) >= level + 1:
            if level == 0:
                stack[level] = reformatPhrase(choice)
            else:
                stack[level] = copy.deepcopy(stack[level-1])
                stack[level].append(reformatPhrase(choice))
        else:
            stack.append(reformatPhrase(choice))

        # Not implemented yet!!!!
        withContradictionHandler()

        # if true, then ddsearch, otherwise, contradition!!!
        print('ddSearch Stack => ', stack)
        ddSearch(choiceSets[1:], level+1, stack)

def withContradictionHandler():
    pass


#### Need to be modified!!! Because different phrase has different format!!!!!! ####
def reformatPhrase(choice):
    phrases = []
    for attribute, object in choice.items():
        return parse('('+attribute+' '+object+')')

if __name__ == '__main__':
    #solveCryptarithmeticProblem()

    #choiceSets = solveCryptarithmeticProblem()
    #ddSearch(choiceSets)

    ss = [[1,2,3]]
    print(ss[1:]==[])
    print(ss[1:]==None)