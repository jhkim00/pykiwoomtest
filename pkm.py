import logging
import kiwoom
from model.coolDown import CoolDown
from model import realDataWorker, priceInfo

logger = logging.getLogger()
_pkm = None
_coolDown = None


def pkm():
    global _pkm
    if _pkm is None:
        _pkm = kiwoom.KiwoomManager()
    return _pkm


def checkCollDown():
    global _coolDown
    if _coolDown is None:
        _coolDown = CoolDown(limit=1, interval=0.3)

    _coolDown.call()


def getStockPriceInfo(screenNumber: str, stock: dict):
    logger.debug('')
    if 'priceInfo' not in stock:
        logger.debug(f"priceInfo not in stock code: {stock['code']}")
        tr_cmd = {
            'rqname': "주식기본정보",
            'trcode': 'opt10001',
            'next': '0',
            'screen': screenNumber,
            'input': {
                "종목코드": stock['code']
            },
            'output': ['시가', '고가', '저가', '현재가', '기준가', '대비기호', '전일대비', '등락율', '거래량', '거래대비']
        }
        checkCollDown()
        km = pkm()
        km.put_tr(tr_cmd)
        data, remain = km.get_tr()

        _priceInfo = priceInfo.PriceInfo()
        _priceInfo.info = data.iloc[0].to_dict()

        stock['priceInfo'] = _priceInfo


def getStockPriceRealData(screenNumber: str, conditionStockList: list):
    logger.debug('')
    real_cmd = {
        'func_name': "SetRealReg",
        'real_type': '주식체결',
        'screen': screenNumber,
        'code_list': [item['code'] for item in conditionStockList],
        'fid_list': ['20', '10', '11', '12', '13', '14', '15', '16', '17', '18', '25', '30'],
        "opt_type": 0
    }
    km = pkm()
    km.put_real(real_cmd)
