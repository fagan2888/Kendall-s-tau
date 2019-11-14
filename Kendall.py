
# this file helps to realize Kendall's tau algorithm

import numpy as np
import pandas as pd
import math
from itertools import combinations
from scipy.stats import kendalltau
from ipdb import set_trace


# three different ways to calculate kendall's tau
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

#   the second way: we can use combinations in itertools module to help but in this way you have to make sure that combinations does not change sequence of origin list
    reversions = 2 * len(set(combinations(setOne, 2)).difference(set(combinations(setTwo, 2))))
    kendall = 1 - 2 * reversions / (length*(length-1))
 
#   the third way: use kendalltau in scipy.stats
    kendall = kendalltau(setOne, setTwo)
    
    return kendall

# kendall's tau list based on time delay
def kendallList(x,d):
    L = len(x)
    m = np.mean(x)
    var = np.var(x)
    taus = list()
    sumUp = 0
    for k in range(len(x)):
        for i in range(int(len(x)-k-d)):
            sumUp = sumUp + x[i+d]*x[i+k+d]
        tau =  1/var*(1/(L-k-d)*sumUp-m*m)
        tauNew = tau.copy()
        taus.append(tauNew)
    
    ks = list(range(len(x)))
    df = pd.DataFrame(columns = ['k', 'tau'])
    df.k = ks
    df.tau = taus

    return df

# N max index list
def Nindexes(df, d, N):

    df.set_index('k', inplace = True)
    df.sort_values(by = 'tau', ascending = False, inplace = True)
    indexes = list()
    indexes.append(df.index[0])
    flag = df.index[0] - d
    newDf = df[df.index <= flag]
    newDf.sort_values(by = 'tau', inplace = True, ascending = False)
 
    for i in range(N-1):
        flag = newDf.index[0] - i*d
        newDf = newDf[newDf.index <= flag]
        newDf.sort_values(by = 'tau', inplace = True, ascending = False)
        indexes.append(newdf.index[0])

    return indexes

# core map
def core():


# centre map
def centre():


# extend map
def extend():
    



if __name__ == '__main__':
    # data for calculate
    x = 
    
    # number of the periods we care about
    N =
    
    # delay period
    d = 

#    listOne = ['a','b','c','d']
#    listTwo = ['d', 'a', 'c', 'b']
#    kendall(listOne, listTwo)


