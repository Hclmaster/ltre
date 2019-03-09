import myglobal

class Tre(object):

    def __init__(self, title=None, dbclassTable=None,
                 debugging=False, queue=None,
                 rule_counter=0, rules_run=0):
        self.title = title
        self.dbclassTable = dbclassTable
        self.debugging = debugging
        self.queue = queue
        self.rule_counter = rule_counter
        self.rules_run = rules_run


def inTre(tre):
    """
    Set the default tre to a new value.
    :param tre:
    :return:
    """
    myglobal._tre_ = tre


def createTre(title, debugging=False):
    """
    :param title:
    :param debugging:
    :return: create a new Tiny Rule Engine
    """
    return Tre(title=title, dbclassTable={}, debugging=debugging)


def runForms(forms):
    for form in forms:
        print('form => ', form)


if __name__ == "__main__":
    inTre(createTre("Ex1"))
    print(myglobal._tre_.title)

