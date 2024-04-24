from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal, QVariant
import logging
import threading

import pkm
import realConditionWorker

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

    @property
    def conditionList(self):
        return self._conditionList

    @conditionList.setter
    def conditionList(self, conditionList: list):
        self._conditionList = conditionList
        self.qmlContext.setContextProperty("conditionList", self._conditionList)

    @pyqtSlot(str, result=list)
    def getConditionStockList(self, conditionIndex):
        for condition in self._conditionList:
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

        self._realConditionList.append({'name': conditionName, 'code': conditionIndex})

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
            for condition in self._conditionList:
                if int(data['cond_index']) == int(condition['code']):
                    condition['stock'].clear()
                    for code in data['code_list']:
                        km.put_method(('GetMasterCodeName', code))
                        masterName = km.get_method()
                        condition['stock'].append({'code': code, 'name': masterName})

                    logger.debug(condition)
                    break

        return True

    @pyqtSlot(dict)
    def _onRealCondition(self, data: dict):
        logger.debug(data)
        km = pkm.pkm()
        with self._semaphore:
            for condition in self._conditionList:
                if int(data['cond_index']) == int(condition['code']):
                    if data['type'] == 'I':
                        km.put_method(('GetMasterCodeName', data['code']))
                        masterName = km.get_method()
                        condition['stock'].append({'code': data['code'], 'name': masterName})
                    elif data['type'] == 'D':
                        for stock in condition['stock']:
                            if data['code'] == stock['code']:
                                condition['stock'].remove(stock)
                                break

                    # logger.debug(condition)
                    self.conditionStockChanged.emit(condition['code'])
                    break

    @pyqtSlot(str, str)
    def onCurrentStock(self, name, code):
        self.currentStockChanged.emit({'name': name, 'code': code})



