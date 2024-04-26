from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal, QVariant
import logging
import threading

import pkm
import realConditionWorker
from model import realDataWorker, priceInfo

logger = logging.getLogger()


class ConditionController(QObject):
    currentStockChanged = pyqtSignal(dict)
    conditionStockChanged = pyqtSignal(str)

    def __init__(self, qmlContext, parent=None):
        super().__init__(parent)
        self.qmlContext = qmlContext
        self.qmlContext.setContextProperty('conditionController', self)

        self._conditionList = list()
        self._semaphore = threading.Semaphore(1)
        self._realConditionList = list()

        realConditionWorker.RealConditionWorker.getInstance().data_received.connect(self._onRealCondition)
        realDataWorker.RealDataWorker.getInstance().data_received.connect(self._onRealData)

    @property
    def conditionList(self):
        return self._conditionList

    @conditionList.setter
    def conditionList(self, conditionList: list):
        self._conditionList = conditionList
        self.qmlContext.setContextProperty("conditionList", self._conditionList)

    @pyqtSlot(str, result=list)
    def getConditionStockList(self, conditionIndex):
        for condition in self._realConditionList:
            if int(condition['code']) == int(conditionIndex):
                return condition['stock']

    @pyqtSlot()
    def getConditionList(self):
        logger.debug('')
        pkm.checkCollDown()
        km = pkm.pkm()
        cmd = {
            'func_name': 'GetConditionNameList'
        }
        km.put_cond(cmd)
        conditionList = list()
        conditionListRaw = km.get_cond(method=True)
        logger.debug(conditionListRaw)
        for conditionRaw in conditionListRaw:
            cond = {'code': conditionRaw[0], 'name': conditionRaw[1], 'stock': list()}
            conditionList.append(cond)

        self.conditionList = conditionList

    @pyqtSlot(str, result=bool)
    def registerCondition(self, conditionIndex: str):
        if len(self._realConditionList) >= 10:
            logger.warning('real condition can only register up to 10.')
            return False

        conditionName = ''
        for cond in self._conditionList:
            if int(cond['code']) == int(conditionIndex):
                conditionName = cond['name']
                break

        if conditionName == '':
            logger.debug(f"condition {conditionIndex} is not found in condition list.")
            return False

        logger.debug(f"name: {conditionName}, index: {conditionIndex}")

        for condition in self._realConditionList:
            if int(conditionIndex) == int(condition['code']):
                logger.debug(f"condition {conditionName} is already registered.")
                return False

        self._realConditionList.append({'name': conditionName, 'code': conditionIndex, 'stock': list()})

        logger.debug(f"real condition list: {self._realConditionList}")

        pkm.checkCollDown()
        km = pkm.pkm()
        cmd = {
            'func_name': 'SendCondition',
            'screen': '2000',
            'cond_name': conditionName,
            'index': int(conditionIndex),
            'search': 1
        }
        km.put_cond(cmd)
        data = km.get_cond()
        logger.debug(data)
        with self._semaphore:
            for condition in self._realConditionList:
                if int(data['cond_index']) == int(condition['code']):
                    condition['stock'].clear()
                    for code in data['code_list']:
                        km.put_method(('GetMasterCodeName', code))
                        masterName = km.get_method()
                        condition['stock'].append({'code': code, 'name': masterName})

                    for stock in condition['stock']:
                        self._getStockPriceInfo(stock)

                    self._getRealData(condition['stock'])

                    logger.debug(condition)
                    break

        return True

    @pyqtSlot(dict)
    def _onRealCondition(self, data: dict):
        logger.debug(data)
        km = pkm.pkm()
        with self._semaphore:
            for condition in self._realConditionList:
                if int(data['cond_index']) == int(condition['code']):
                    if data['type'] == 'I':
                        km.put_method(('GetMasterCodeName', data['code']))
                        masterName = km.get_method()
                        stock = {'code': data['code'], 'name': masterName}
                        condition['stock'].append(stock)
                        self._getStockPriceInfo(stock)
                    elif data['type'] == 'D':
                        for stock in condition['stock']:
                            if data['code'] == stock['code']:
                                condition['stock'].remove(stock)
                                break

                    self._getRealData(condition['stock'])

                    # logger.debug(condition)
                    self.conditionStockChanged.emit(condition['code'])
                    break

    @pyqtSlot(str, str)
    def onCurrentStock(self, name, code):
        self.currentStockChanged.emit({'name': name, 'code': code})

    @staticmethod
    def _getStockPriceInfo(stock):
        logger.debug('')
        if 'priceInfo' not in stock:
            logger.debug(f"priceInfo not in stock code: {stock['code']}")
            tr_cmd = {
                'rqname': "주식기본정보",
                'trcode': 'opt10001',
                'next': '0',
                'screen': '1001',
                'input': {
                    "종목코드": stock['code']
                },
                'output': ['시가', '고가', '저가', '현재가', '기준가', '대비기호', '전일대비', '등락율', '거래량', '거래대비']
            }
            pkm.checkCollDown()
            km = pkm.pkm()
            km.put_tr(tr_cmd)
            data, remain = km.get_tr()

            _priceInfo = priceInfo.PriceInfo()
            _priceInfo.info = data.iloc[0].to_dict()

            stock['priceInfo'] = _priceInfo
            return True

        return False

    @staticmethod
    def _getRealData(conditionStockList: list):
        logger.debug('')
        real_cmd = {
            'func_name': "SetRealReg",
            'real_type': '주식체결',
            'screen': '2000',
            'code_list': [item['code'] for item in conditionStockList],
            'fid_list': ['20', '10', '11', '12', '13', '16', '17', '18', '25', '30'],
            "opt_type": 0
        }
        km = pkm.pkm()
        km.put_real(real_cmd)

    @pyqtSlot(dict)
    def _onRealData(self, data: dict):
        # logger.debug(data)
        isIn = False
        for condition in self._realConditionList:
            for stock in condition['stock']:
                if data['code'] == stock['code']:
                    isIn = True
                    if data['rtype'] == '주식체결':
                        _priceInfo = {
                            '시가': '',
                            '고가': '',
                            '저가': '',
                            '현재가': '',
                            '기준가': '',
                            '대비기호': '',
                            '전일대비': '',
                            '등락율': '',
                            '거래량': '',
                            '거래대비': ''
                        }
                        _priceInfo['현재가'] = data['10']
                        _priceInfo['전일대비'] = data['11']
                        _priceInfo['등락율'] = data['12']
                        _priceInfo['거래량'] = data['13']
                        _priceInfo['시가'] = data['16']
                        _priceInfo['고가'] = data['17']
                        _priceInfo['저가'] = data['18']
                        _priceInfo['대비기호'] = data['25']
                        _priceInfo['거래대비'] = data['30']
                        _priceInfo['기준가'] = stock['priceInfo'].info['기준가']

                        # logger.debug(f"code: {data['code']}")
                        # logger.debug(_priceInfo)

                        stock['priceInfo'].info = _priceInfo
                        break

        # if not isIn:
        #     logger.debug(f"code: {data['code']} isIn:{isIn}")

