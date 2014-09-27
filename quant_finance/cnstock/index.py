#coding:utf8


'''
http://stock.sina.com.cn/missing.html

沪市指数
上证指数(1A0001)	A股指数 (1A0002)	B股指数 (1A0003)	工业指数(1B0001)
商业指数(1B0002)	地产指数(1B0004)	公用指数(1B0005)	综合指数(1B0006)
上证180 (1B0007)	基金指数(1B0008)	国债指数(1B0009)	


深市指数
深证成指(399001)	成分A指 (399002)	成分B指 (399003)	深证100 (399004)
深证综指(399106)	深证A指 (399107)	深证B指 (399108)	农林指数(399110)
采掘指数(399120)	制造指数(399130)	食品指数(399131)	纺织指数(399132)
木材指数(399133)	造纸指数(399134)	石化指数(399135)	电子指数(399136)
金属指数(399137)	机械指数(399138)	医药指数(399139)	水电指数(399140)
建筑指数(399150)	运输指数(399160)	IT指数 (399170)	批零指数(399180)
金融指数(399190)	地产指数(399200)	服务指数(399210)	传播指数(399220)
综企指数(399230)	基金指数(399305)	企债指数(399481)	
'''

INDEXE_SYMBOL_OLD = {
    'SH': '1A0001 1A0002 1A0003 1B0001 1B0002 1B0004 1B0005 1B0006 1B0007 1B0008 1B0009 1B0007'.split()
}

INDEXE_SYMBOL_NEW = {
    'SH': 'SH000001 SH000002 SH000003 SH000004 SH000005 SH000006 SH000007 SH00008 SH000009 SH000010 SH000011 SH000012'.split()
}

INDEXE_NAME = {
    'SH': '上证指数 A股指数 B股指数 工业指数 商业指数 地产指数 公用指数 综合指数 上证180 基金指数 国债指数'.split()
}


INDEXE_SYMBOL_OLD_TO_NEW = {}
INDEXE_SYMBOL_NEW_TO_OLD = {}
INDEXE_SYMBOL_NEW_TO_NAME = {}

def _setup():
    for k in ['SH']:
        INDEXE_SYMBOL_OLD_TO_NEW[k] = {}
        INDEXE_SYMBOL_NEW_TO_OLD[k] = {}
        n = len(INDEXE_SYMBOL_OLD[k])
        for i in range(n):
            old = INDEXE_SYMBOL_OLD[k][i]
            new = INDEXE_SYMBOL_NEW[k][i]
            INDEXE_SYMBOL_OLD_TO_NEW[k][old] = new
            INDEXE_SYMBOL_NEW_TO_OLD[k][new] = k + old
        

_setup()

#TODO: SZ index symbol
def index_symbol_old_to_new(s):
    t = s.upper()
    if t[:2]=='SH':
        t = t[2:]
    if not t in INDEXE_SYMBOL_OLD['SH']:
        return s
    else:
        return INDEXE_SYMBOL_OLD_TO_NEW['SH'][t]

def index_symbol_new_to_old(s):
    t = s.upper()
    if t[:2]=='SH':
        t = t[2:]
    if not s in INDEXE_SYMBOL_NEW['SH']:
        return s
    else:
        return INDEXE_SYMBOL_NEW_TO_OLD['SH'][s]

