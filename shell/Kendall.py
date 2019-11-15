
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
def core(e, x, maxDelay):
    dCore = list()
    periods = list()
    for d in range(maxDelay):
        df = kendallList(x, d)
        N = len(df)//(2*d)
        indexes = Nindexes(df, d, N)
        indexes.sort()
        
        TSum = 0
        for i in range(len(indexes):
            TSum = TSum + (indexes[i+1]-indexes[i])
        T1 = TSum / N
        
        if np.abs(T1/(2*d-1)) < e:
            periods.append(T1)
            dCore.append(d)
        else:
            N = len(df)//(2*d) + 1
            indexes = Nindexes(df, d, N)
            indexes.sort()
            TSum = 0
            for i in range(len(indexes):
                TSum = TSum + (indexes[i+1]-indexes[i])
            T2 = TSum / N
            if np.abs(T2/(2*d-1)) < e:
                periods.append(T2)
                dCore.append(d)
    
    dfCore = pd.DataFrame(columns = ['d','T'])
    dfCore.d = dCore
    dfCore.T = periods

    return dfCore

# centre map
# dc is one single element in dCore list
# df here equals kendallList(x, dc)
def center(c, df, maxDelay, dc, N):
    
    indexes = Nindexes(df, dc, N)
    indexes.sort()
    TCoreList = list()
    for i in range(len(indexes):
        T = indexes[i+1]-indexes[i]
        TCoreList.append(T)
 
    dCenter = list()
    for d in range(maxDelay):
        indexes = Nindexes(df, d, N)
        indexes.sort()
        
        DiffList = list()
        for i in range(len(indexes):
            T = indexes[i+1]-indexes[i]
            diff = T - TCoreList[i]
            DiffList.append(diff)
        
        dist = np.linalg.norm(diffList)
        if dist < c:
            dCenter.append(d)
    
    return dCenter

# extend map
# dc is one single element in dCore list
# df here equals kendallList(x, dc) 
def extend(delta, maxDelay, dCore):
    
    dExtend = list()
    for d in range(maxDelay):
        df = kendallList(x, d)
        tau = df['tau']
        distList = list()
        for dc in dCore:
            dfc = kendallList(x, dc)
            tauc = df['tau']
            dist = np.linalg.norm(np.array(tau)-np.array(tauc)) 
            distList.append(dist)
        
        distMin = np.min(distList)
        if distMin < delta:
            dExtend.append(d)
    
    return dExtend

# main function
def do(x, dmax, N, e, c, delta):
    
    excel = pd.ExcelWriter('kendall-s-T.xlsx')
    dfCore = core(e, x, dmax)
    print(dfCore)
    dfCore.to_excel(excel, sheet_name = 'coreData')
    print('core map done')
    
    dfCenter = pd.DataFrame(columns = ['d','T'])
    for dc in dCore:
        dCenter = center(c, df, dmax, dc, N)
        dCenterList = list()
        TCenterList = list()
        for dm in dCenter:
            df = kendallList(x, dm)
            num = len(df)//(2*dm)
            indexes = Nindexes(df, dm, num)
            indexes.sort()
        
            TSum = 0
            for i in range(len(indexes):
                TSum = TSum + (indexes[i+1]-indexes[i])
            T = TSum / num

            dCenterList.append(dm)
            TCenterList.append(T)
    
    print(dfCenter)
    dfCenter.to_excel(excel, sheet_name = 'centerData')
    print('center map done')

    dfExtend = pd.DataFrame(columns = ['d', 'T'])
    dExtend = extend(delta, dmax, dCore)
    for de in dExtend:
        df = kendallList(x, de)
        num = len(df)//(2*de)
        indexes = Nindexes(df, de, num)
        indexes.sort()
    
        TSum = 0
        for i in range(len(indexes):
            TSum = TSum + (indexes[i+1]-indexes[i])
        T = TSum / num
    
        dExtendList.append(de)
        TExtendList.append(T)
    
    print(dfExtend)
    dfExtend.to_excel(excel, sheet_name = 'extendData')
    excel.save()
    print('extend map done')
    print('task finished! data has been saved in kendall-s-T.xlsx')


if __name__ == '__main__':

    # load basic data
    df = loadStockIndex()
    sh000001 = df[df['S_INFO_WINDCODE'] == '000001.SH']
    sh000001['TRADE_DT'] = sh000001['TRADE_DT'].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))
    sh000001.sort_values('TRADE_DT', ascending = True, inplace = True)
    sh000001.reset_index(inplace = True, drop = True)

    sz399001 = df[df['S_INFO_WINDCODE'] == '399001.SZ']
    sz399001['TRADE_DT'] = sz399001['TRADE_DT'].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))
    sz399001.sort_values('TRADE_DT', ascending = True, inplace = True)
    sz399001.reset_index(inplace = True, drop = True)

    h11007 = loadBondIndex()
    h11007['TRADE_DT'] = h11007['TRADE_DT'].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))
    h11007.sort_values('TRADE_DT', ascending = True, inplace = True)
    h11007.reset_index(inplace = True, drop = True)

    # data for calculate
    x = 
    
    # number of the periods we care about
    N =
    
    # max delay period
    dmax =

    # error for selecting core map
    e = 

    # error for selecting center map
    c = 

    # error for selecting extend map
    delta = 

    do(x, dmax, N, e, c, delta)
