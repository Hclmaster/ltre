Symbol = str    # A Lisp Symbol is implemented as a Python str

def variableOrNot(x):
    """
    True if x is a pattern variable
    :param x:
    :return:
    """
    if Symbol(x) and x[0] == '?':
        return True
    return False


if __name__ == '__main__':
    lst = [1,2,3]
    print(lst[4])