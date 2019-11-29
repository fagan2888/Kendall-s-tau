
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
#    r = list()
#    for i in range(int(L-d)):
#        if x[i]<x[i+d]:
#            r.append(0)
#        else:
#            r.append(1)
#    m = np.mean(r)
#    var = np.var(r)
#    if var == 0:
#        print('period == %d'%(d))
#        exit()
    taus = list()
#    sumUp = 0
    for k in range(1,int(L-d)):
        r1 = list()
        r2 = list()
        for i in range(int(L-k-d)):
#            if x[i+d]>x[i] or x[i+k+d]>x[i+k]:
#                rkir = 0
#            else:
#                rkir = 1
#            sumUp = sumUp + rkir
#        tau =  1/var*(1/(L-k-d)*sumUp-m*m)
#        tau = 1/(L-k-d)*sumUp
            
            if x[i+d]>x[i]:
                r1.append(0)
            else:
                r1.append(1)
            if x[i+k+d]>x[i+k]:
                r2.append(0)
            else:
                r2.append(1)  
        tau = pd.Series(r1).corr(pd.Series(r2), method = 'kendall')
        taus.append(tau)
    
    ks = list(range(1,int(L-d)))
    df = pd.DataFrame({'k': ks, 'tau': taus})
    df = df.fillna(0)
    df.set_index('k', inplace = True)
    
    return df

# N max index list
def Nindexes(df, d, N):
    df.sort_values(by = 'tau', ascending = False, inplace = True)
    indexes = list()
    if len(df)!= 0 :
        indexes.append(df.index[0])
    else:
        return []
 
    for i in range(1,len(df)):
        if len(indexes) <= N:
            c = df.index[i]
            distance = min([j-c for j in indexes])
            if distance >= d:
                indexes.append(c)

    return indexes

# core map
def core(e, x, maxDelay):
    dCore = list()
    periods = list()
    for d in range(1,maxDelay):
        df = kendallList(x, d)
        N = len(df)//(2*d)
        if N == 0:
            continue
        indexes = Nindexes(df, d, N)
        if len(indexes) < 2:
            continue
        indexes.sort()

        TSum = 0
        for i in range(int(len(indexes)-1)):
            TSum = TSum + (indexes[i+1]-indexes[i])
        T1 = TSum / N
        if np.abs(T1/(2*d)-1) < e:
            periods.append(T1)
            dCore.append(d)
        else:
            N = len(df)//(2*d) + 1
            indexes = Nindexes(df, d, N)
            if len(indexes) < 2:
                continue
            indexes.sort()
            TSum = 0
            for i in range(int(len(indexes)-1)):
                TSum = TSum + (indexes[i+1]-indexes[i])
            T2 = TSum / N
            if np.abs(T2/(2*d)-1) < e:
                periods.append(T2)
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
        if len(indexes) == 0:
            continue
        indexes.sort()
        
        diffList = list()
        for i in range(int(len(indexes)-1)):
            T = indexes[i+1]-indexes[i]
            diff = T - TCoreList[i]
            diffList.append(diff)
        
        dist = np.linalg.norm(diffList)
        if dist < c:
            dCenter.append(d)
    
    return dCenter

# extend map
def extend(delta, x, maxDelay, dCore):
    
    dExtend = list()
    for d in range(1,maxDelay):
        df = kendallList(x, d)
        if len(df) == 0:
            continue
        tau = df['tau']
        distList = list()
        for dc in dCore:
            dfc = kendallList(x, dc)
            tauc = dfc['tau']
            length = min([len(tau),len(tauc)])
            tauc = tauc[0:length]
            tau = tau[0:length]
            dist = np.linalg.norm(np.array(tau)-np.array(tauc)) 
            distList.append(dist)
        distMin = np.min(distList)
        if distMin < delta:
            dExtend.append(d)
    
    return dExtend

# main function
def do(x, dmax, N, e, c, delta):
    
    dfCore = pd.DataFrame(columns = ['d', 'T'])
    while len(dfCore) == 0 and e <= 0.5:
        dfCore = core(e, x, dmax)
        e = e + 0.01
    if e > 0.5:
        print('task failed! it seems like origin data has no feasible period!')
        return -1
    e = e - 0.01
#    dfCore.to_excel('coreData.xlsx')
    print('core map done and error for core map is', e)

    print(dfCore)
    set_trace()

    dfCenter = pd.DataFrame(columns = ['d','T'])
    dCore = list(dfCore.d)
    for dc in dCore:
        dCenter = center(c, x, dmax, dc, N)
        dCenterList = list()
        TCenterList = list()
        for dm in dCenter:
            df = kendallList(x, dm)
            num = len(df)//(2*dm)
            if num == 0:
                continue
            indexes = Nindexes(df, dm, num)
            if len(indexes) < 2:
                continue
            indexes.sort()
        
            TSum = 0
            for i in range(int(len(indexes)-1)):
                TSum = TSum + (indexes[i+1]-indexes[i])
            T = TSum / num

            dCenterList.append(dm)
            TCenterList.append(T)
    
    dfCenter.d = dCenterList
    dfCenter.T = TCenterList
#    dfCenter.to_excel('centerData.xlsx')
    print('center map done')

    print(dfCenter)
    set_trace()

    dfExtend = pd.DataFrame(columns = ['d', 'T'])
    dExtend = extend(delta, x, dmax, dCore)
    dExtendList = list()
    TExtendList = list()
    for de in dExtend:
        df = kendallList(x, de)
        num = len(df)//(2*de)
        if num == 0:
            continue
        indexes = Nindexes(df, de, num)
        if len(indexes) < 2:
            continue
        indexes.sort()
    
        TSum = 0
        for i in range(int(len(indexes)-1)):
            TSum = TSum + (indexes[i+1]-indexes[i])
        T = TSum / num
    
        dExtendList.append(de)
        TExtendList.append(T)
    
    dfExtend.d = dExtendList
    dfExtend.T = TExtendList
#    dfExtend.to_excel('extendData.xlsx')
    print('extend map done')
    print('task finished! data has been saved in kendall-s-T.xlsx')

    print(dfExtend)


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

    x = list(pd.read_excel('fullData.xlsx', sheet_name = '股票').sort_values(by = '日期', ascending = True)['恒生指数'])

#    x = [1,2,3,4,3,2,1,2.1,3,4,3.1,2,1.1,2,3.1,4,3,2.1,1,2,3.1,4,3,2,1,2,3.1,4.1,3,2,1.1,2,3,4.1,3,2.1,1,2]
    # number of the periods we care about
    N = 10
    # max delay period
    dmax = len(x)//2
    # error for selecting core map
    e = 0.02
    # error for selecting center map
    c = 0.05
    # error for selecting extend map
    delta = 1
    
    do(x, dmax, N, e, c, delta)
