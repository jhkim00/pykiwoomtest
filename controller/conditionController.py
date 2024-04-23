from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal, QVariant
import logging

import pkm
import realConditionWorker

logger = logging.getLogger()


class ConditionController(QObject):
    def __init__(self, qmlContext, parent=None):
        super().__init__(parent)
        self.qmlContext = qmlContext
        self.qmlContext.setContextProperty('conditionController', self)

        self._currentCondition = {'code': '', 'name': ''}
        self._conditionList = list()

        realConditionWorker.RealConditionWorker.getInstance().data_received.connect(self._onRealCondition)

    currentConditionChanged = pyqtSignal()

    @pyqtProperty(QVariant)
    def currentCondition(self):
        logger.debug('')
        return self._currentCondition

    @currentCondition.setter
    def currentCondition(self, condition: QVariant):
        logger.debug(f'condition: {condition}')
        if isinstance(condition, dict):
            self._currentCondition = condition
        else:
            self._currentCondition = condition.toVariant()

        logger.debug(f'self._currentCondition: {self._currentCondition}')
        logger.debug(f"name: {self._currentCondition['name']}, code: {self._currentCondition['code']}")
        self.currentConditionChanged.emit()

    @pyqtSlot(QVariant)
    def setCurrentCondition(self, condition: QVariant):
        logger.debug(f'condition: {condition}')
        if isinstance(condition, dict):
            logger.debug('000')
            self._currentCondition = condition
        else:
            logger.debug('111')
            self._currentCondition = condition.toVariant()

        logger.debug(f'self._currentCondition: {self._currentCondition}')
        logger.debug(f"name: {self._currentCondition['name']}, code: {self._currentCondition['code']}")
        self.currentConditionChanged.emit()

    @property
    def conditionList(self):
        return self._conditionList

    @conditionList.setter
    def conditionList(self, conditionList: list):
        self._conditionList = conditionList
        self.qmlContext.setContextProperty("conditionList", self._conditionList)

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

    @pyqtSlot()
    def getCondition(self):
        logger.debug(f"name: {self._currentCondition['name']}, code: {self._currentCondition['code']}")
        pkm.checkCollDown()
        km = pkm.pkm()
        cmd = {
            'func_name': 'SendCondition',
            'screen': '2000',
            'cond_name': self._currentCondition['name'],
            'index': int(self._currentCondition['code']),
            'search': 1
        }
        km.put_cond(cmd)

        data = km.get_cond()
        logger.debug(data)
        for condition in self._conditionList:
            if int(data['cond_index']) == int(condition['code']):
                for code in data['code_list']:
                    km.put_method(('GetMasterCodeName', code))
                    masterName = km.get_method()
                    condition['stock'].append({'code': code, 'name': masterName})

                logger.debug(condition)
                break

    @pyqtSlot(dict)
    def _onRealCondition(self, data: dict):
        logger.debug(data)
        km = pkm.pkm()
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

                logger.debug(condition)
                break


