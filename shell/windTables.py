# created by zhaoliyuan

# wind tables

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

Base = declarative_base()

indexDict = {
        '上证指数' : ['000001','000001.SH'],
        '深证成指' : ['399001','399001.SZ'],
        '中证国债指数' : ['h11007','h11007.CSI'],
        '恒生指数' : ['HSI','HSCI.HI'],
        'MSCI全球' : ['892400','892400.MI'],
        '纳斯达克100' : ['NDX','NDX.GI'],
        '标普500指数' : ['SPX','SPX.GI'],
        '印度孟买100股票' : ['W00116','W00116'],
        }

class aindexeodprices(Base):

    __tablename__ = 'aindexeodprices'

    OBJECT_ID = Column(String, primary_key = True)
    S_INFO_WINDCODE = Column(String)
    TRADE_DT = Column(String)
    S_DQ_PRECLOSE = Column(Float)
    S_DQ_OPEN = Column(Float)
    S_DQ_HIGH = Column(Float)
    S_DQ_LOW = Column(Float)
    S_DQ_CLOSE = Column(Float)
    S_DQ_CHANGE = Column(Float)
    S_DQ_PCTCHANGE = Column(Float)
    S_DQ_VOLUMNE = Column(Float)
    S_DQ_AMOUNT = Column(Float)

class cbindexeodprices(Base):

    __tablename__ = 'cbindexeodprices'

    OBJECT_ID = Column(String, primary_key = True)
    S_INFO_WINDCODE = Column(String)
    TRADE_DT = Column(String)
    S_DQ_PRECLOSE = Column(Float)
    S_DQ_OPEN = Column(Float)
    S_DQ_HIGH = Column(Float)
    S_DQ_LOW = Column(Float)
    S_DQ_CLOSE = Column(Float)
    S_DQ_CHANGE = Column(Float)
    S_DQ_PCTCHANGE = Column(Float)
    S_DQ_VOLUMNE = Column(Float)
    S_DQ_AMOUNT = Column(Float)




