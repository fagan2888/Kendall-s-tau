
# this file helps to realize Kendall's tau algorithm

import numpy as np
import pandas as pd
import math
from itertools import combinations
from scipy.stats import kendalltau
from ipdb import set_trace

listOne = ['a','b','c','d']
listTwo = ['d', 'a', 'c', 'b']

def kendall (listOne, listTwo):
    setOne = list(set(listOne))
    setOne.sort(key = listOne.index)
    setTwo = list(set(listTwo))
    setTwo.sort(key = listTwo.index)
    if len(setOne) != len(setTwo):
        print('error length differs!')
        return -1
    
    length = len(setOne)

#   the first way: define a function
    def comp(setOne):
        element = [0,0]
        result = list()
        for i in range(int(len(setOne)-1)):
            element[0] = setOne[i]
            for j in range(i+1,len(setOne)):
                element[1] = setOne[j]
                newElement = tuple(element.copy())
                result.append(newElement)
        
        return result
    
    pairOne = set(comp(setOne))
    pairTwo = set(comp(setTwo))
    reversions = 2 * len(pairOne.difference(pairTwo))
    kendall = 1 - 2 * reversions / (length*(length-1))

    print(kendall)

#   the second way: we can use combinations in itertools module to help but in this way you have to make sure that combinations does not change sequence of origin list
    reversions = 2 * len(set(combinations(setOne, 2)).difference(set(combinations(setTwo, 2))))
    kendall = 1 - 2 * reversions / (length*(length-1))
 
    print(kendall)

#   the third way: use kendalltau in scipy.stats
    kendall = kendalltau(setOne, setTwo)
    print(kendall)
    
    return kendall

kendall(listOne, listTwo)
