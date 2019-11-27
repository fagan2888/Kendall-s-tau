
# this file helps to realize Kendall's tau algorithm

import numpy as np
import pandas as pd
import math
from itertools import combinations
from scipy.stats import kendalltau
from loadData import *
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

    # the first way: define a function
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

    # the second way: we can use combinations in itertools module to help 
    # but in this way you have to make sure that combinations does not change sequence of origin list
    reversions = 2 * len(set(combinations(setOne, 2)).difference(set(combinations(setTwo, 2))))
    kendall = 1 - 2 * reversions / (length*(length-1))
 
    # the third way: use kendalltau in scipy.stats
    kendall = kendalltau(setOne, setTwo)
    
    return kendall

# kendall's tau list based on time delay
def kendallList(x,d):
    L = len(x)
    r = list()
    for i in range(int(L-d)):
        if x[i]<x[i+d]:
            r.append(0)
        else:
            r.append(1)
    m = np.mean(r)
    var = np.var(r)
    
    taus = list()
    sumUp = 0
    for k in range(1,int(L-d)):
        for i in range(int(L-k-d)):
            if x[i+d]>x[i] or x[i+k+d]>x[i+k]:
                rkir = 0
            else:
                rkir = 1
            sumUp = sumUp + rkir
        tau =  1/var*(1/(L-k-d)*sumUp-m*m)
        taus.append(tau)
    
    ks = list(range(1,int(L-d)))
    df = pd.DataFrame({'k': ks, 'tau': taus})
    df.set_index('k', inplace = True)
    
    return df

# N max index list
def Nindexes(df, d, N):
    df.sort_values(by = 'tau', ascending = False, inplace = True)
    indexes = list()
    if len(df)!= 0 :
        indexes.append(df.index[0])
 
    for i in range(1,N-1):
        flag = df.index[0] - i*d
        newDf = df[df.index <= flag].copy()
        if len(newDf) != 0:
            newDf.sort_values(by = 'tau', ascending = False, inplace = True)
            indexes.append(newDf.index[0])

    return indexes

# core map
def core(e, x, maxDelay):
    dCore = list()
    periods = list()
    for d in range(1,maxDelay):
        df = kendallList(x, d)
        N = len(df)//(2*d)
        indexes = Nindexes(df, d, N)
        indexes.sort()
        
        TSum = 0
        for i in range(int(len(indexes)-1)):
            TSum = TSum + (indexes[i+1]-indexes[i])
        T1 = TSum / N
        
        if np.abs(T1/2*d-1) < e:
            periods.append(T1)
            print(periods)
            set_trace()
            dCore.append(d)
        else:
            N = len(df)//(2*d) + 1
            indexes = Nindexes(df, d, N)
            indexes.sort()
            TSum = 0
            for i in range(int(len(indexes)-1)):
                TSum = TSum + (indexes[i+1]-indexes[i])
            T2 = TSum / N
            if np.abs(T2/2*d-1) < e:
                periods.append(T2)
                print(periods)
                set_trace()
                dCore.append(d)
    
    dfCore = pd.DataFrame(columns = ['d','T'])
    dfCore.d = dCore
    dfCore.T = periods

    return dfCore

# centre map
# dc is one single element in dCore list
def center(c, x, maxDelay, dc, N):
    
    df = kendallList(x, dc)
    indexes = Nindexes(df, dc, N)
    indexes.sort()
    TCoreList = list()
    for i in range(int(len(indexes)-1)):
        T = indexes[i+1]-indexes[i]
        TCoreList.append(T)
 
    dCenter = list()
    for d in range(1,maxDelay):
        indexes = Nindexes(df, d, N)
        indexes.sort()
        
        DiffList = list()
        for i in range(int(len(indexes)-1)):
            T = indexes[i+1]-indexes[i]
            diff = T - TCoreList[i]
            DiffList.append(diff)
        
        dist = np.linalg.norm(diffList)
        if dist < c:
            dCenter.append(d)
    
    return dCenter

# extend map
def extend(delta, x, maxDelay, dCore):
    
    dExtend = list()
    for d in range(1,maxDelay):
        df = kendallList(x, d)
        tau = df['tau']
        distList = list()
        for dc in dCore:
            dfc = kendallList(x, dc)
            tauc = df['tau']
            dist = np.linalg.norm(np.array(tau)-np.array(tauc)) 
            distList.append(dist)
        if len(distList) == 0:
            return -1
        distMin = np.min(distList)
        if distMin < delta:
            dExtend.append(d)
    
    return dExtend

# main function
def do(x, dmax, N, e, c, delta):
    
    dfCore = pd.DataFrame(columns = ['d', 'T'])
    while len(dfCore) == 0 and e <= 0.5:
        dfCore = core(e, x, dmax)
        print(e)
        e = e + 0.01
    if e > 0.5:
        print('task failed! it seems like origin data has no feasible period!')
        return -1
    e = e - 0.01
    dfCore.to_excel('coreData.xlsx')
    print('core map done and error for core map is', e)

    dfCore = pd.read_excel('coreData.xlsx', index_col = 0)
    print(dfCore)
    set_trace()

    dfCenter = pd.DataFrame(columns = ['d','T'])
    dCore = dfCore.d
    for dc in dCore:
        dCenter = center(c, x, dmax, dc, N)
        dCenterList = list()
        TCenterList = list()
        for dm in dCenter:
            df = kendallList(x, dm)
            num = len(df)//(2*dm)
            indexes = Nindexes(df, dm, num)
            indexes.sort()
        
            TSum = 0
            for i in range(len(indexes)):
                TSum = TSum + (indexes[i+1]-indexes[i])
            T = TSum / num

            dCenterList.append(dm)
            TCenterList.append(T)
    
    dfCenter.to_excel('centerData.xlsx')
    print('center map done')

    dfExtend = pd.DataFrame(columns = ['d', 'T'])
    dExtend = extend(delta, x, dmax, dCore)
    if dExtend == -1:
        print('no regular periods! please lower the criteria!')
        return -1
    for de in dExtend:
        df = kendallList(x, de)
        num = len(df)//(2*de)
        indexes = Nindexes(df, de, num)
        indexes.sort()
    
        TSum = 0
        for i in range(len(indexes)):
            TSum = TSum + (indexes[i+1]-indexes[i])
        T = TSum / num
    
        dExtendList.append(de)
        TExtendList.append(T)
    
    dfExtend.to_excel('extendData.xlsx')
    print('extend map done')
    print('task finished! data has been saved in kendall-s-T.xlsx')


if __name__ == '__main__':

#    sh = pd.read_excel('daily.xlsx', sheet_name = '上证综指日频')
#    sz = pd.read_excel('daily.xlsx', sheet_name = '深证综指日频')
#    sh.sort_values(by = 'TRADE_DT', ascending = True, inplace = True)
#    sz.sort_values(by = 'TRADE_DT', ascending = True, inplace = True)

    # data for calculate
#    x = sh.S_DQ_CHANGE
#    x = sh.WEEK_ON_WEEK_RETURN
#    x = sh.MONTH_ON_MONTH_RETURN
#    x = sh.YEAR_ON_YEAR_RETURN
#    x = sz.S_DQ_CHANGE
#    x = sz.WEEK_ON_WEEK_RETURN
#    x = sz.MONTH_ON_MONTH_RETURN
#    x = sz.YEAR_ON_YEAR_RETURN
#    x = x[366:]
#    x = list(x)

    x = list(pd.read_excel('fullData.xlsx', sheet_name = '股票').sort_values(by = '日期', ascending = True)['标普500'])
    print(x)
    set_trace()

    # number of the periods we care about
    N = 100
    # max delay period
    dmax = 2200
    # error for selecting core map
    e = 0.02
    # error for selecting center map
    c = 0.05
    # error for selecting extend map
    delta = 1

    do(x, dmax, N, e, c, delta)
