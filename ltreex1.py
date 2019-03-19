import myglobal
from ltinter import *
from lrules import *
from dds import *

_attributes_ = ['plays-piano', 'plays-harp', 'smooth-talker', 'likes-gambling', 'likes-animals']
_objects_ = ['groucho', 'harpo', 'chico']

def makeAttributeChoiceSets(attributes, objects):
    """
    Each attribute is assumed to apply to exactly one of the objects
    :param attributes:
    :param objects:
    :return:
    """
    choiceSets = []
    for attribute in attributes:
        attributeSet = []
        for object in objects:
            attributeSet.append({attribute : object})
        choiceSets.append(attributeSet)
    return choiceSets

def ex1 (debugging = False):
    inLtre(createLtre(title="Ex1", debugging = debugging))
    forms = ['(rassert! (:not (plays-piano plays-harp)))',
             '(rassert! (:not (plays-piano smooth-talker)))',
             '(rassert! (:not (plays-harp smooth-talker)))',
             '(rassert! (:not (likes-money likes-gambling)))',
             '(rassert! (:not (likes-gambling likes-animals)))',
             '(rassert! (:not (smooth-talker likes-gambling)))',
             '(rassert! (same-entity likes-animals plays-harp))',
             '(rassert! (:not (likes-animals groucho)))',
             '(rassert! (:not (smooth-talker harpo)))',
             '(rassert! (plays-piano chico))',
             '(rule ((:not (?attribute1 ?attribute2)) (?attribute1 ?obj) (?attribute2 ?obj)) (rassert! (:not (:and (:not (?attribute1 ?attribute2)) (?attribute1 ?obj) (?attribute2 ?obj)))))']
    runForms(myglobal._ltre_, forms)

    # ddSearch & making Choice Sets
    choiceSets = makeAttributeChoiceSets(_attributes_, _objects_)
    #print(choiceSets)
    ddSearch(choiceSets)

    # ============ Test for get not dbclass facts
    #dbclass = getDbClass('plays-piano', myglobal._ltre_)
    #for data in dbclass.notFacts:
    #    print(data)



if __name__ == '__main__':

    ex1()

    #print('======== Show Rules ========')
    #showRules()
    #print('======== Show Facts ========')
    #showData()

    """
    # Test dds
    choiceSets = makeAttributeChoiceSets(_attributes_, _objects_)
    print('choiceSets ====> ', choiceSets)
    ddSearch(choiceSets)
    """
