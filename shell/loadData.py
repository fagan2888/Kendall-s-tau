# created by zhaoliyuan

# load data from wind database

import numpy as np
import pandas as pd
from sqlhelper import database
from sqlhelper.tableToDataFrame import toSQL, toDf
from sqlalchemy import *
from windTables import * 


def loadStockIndex(sdate = '', edate = ''):

    sql = toSQL('wind_db')
    sql = sql.query(aindexeodprices.S_INFO_WINDCODE, aindexeodprices.TRADE_DT, aindexeodprices.S_DQ_CLOSE, aindexeodprices.S_DQ_CHANGE)
    #sql = sql.filter(and_(aindexeodprices.TRADE_DT < sdate, aindexeodprices.TRADE_DT > edate))
    sql = sql.filter(aindexeodprices.S_INFO_WINDCODE.in_(['000001.SH','399001.SZ']))
    sql = sql.statement
    df = toDf('wind_db', sql)
    return df

def loadBondIndex(sdate = '', edate = ''):

    sql = toSQL('wind_db')
    sql = sql.query(cbindexeodprices.S_INFO_WINDCODE, cbindexeodprices.TRADE_DT, cbindexeodprices.S_DQ_CLOSE, cbindexeodprices.S_DQ_CHANGE)
    #sql = sql.filter(and_(cbindexeodprices.TRADE_DT < sdate, cbindexeodprices.TRADE_DT > edate))
    sql = sql.filter(cbindexeodprices.S_INFO_WINDCODE.in_(['h11007.CSI']))
    sql = sql.statement
    df = toDf('wind_db', sql)
    return df



#def loadCPI():
#
#    sql = toSQL('wind_db')
#    sql = sql.query()
#    sql = sql.filter()
#    sql = sql.statement
#    df = toDf('wind_db', sql, parse_dates = '')
#
#def loadPPI():
#
#    sql = toSQL('wind_db')
#    sql = sql.query()
#    sql = sql.filter()
#    sql = sql.statement
#    df = toDf('wind_db', sql, parse_dates = '')
#
#def loadGoods():
#
#    sql = toSQL('wind_db')
#    sql = sql.query()
#    sql = sql.filter()
#    sql = sql.statement
#    df = toDf('wind_db', sql, parse_dates = '')
#
