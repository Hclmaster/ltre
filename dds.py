import warnings

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

def ddSearch(choiceSets):
    if choiceSets == None:
        warnings.warn('DDS Found no solution!')
    choices = choiceSets[0]

    for choice in choices:
        print('choice => ', choice)


if __name__ == '__main__':
    #solveCryptarithmeticProblem()

    choiceSets = solveCryptarithmeticProblem()
    ddSearch(choiceSets)