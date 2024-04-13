from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal, QVariant
import logging

import pkm

logger = logging.getLogger()


class ConditionController(QObject):
    def __init__(self, qmlContext, parent=None):
        super().__init__(parent)
        self.qmlContext = qmlContext
        self.qmlContext.setContextProperty('conditionController', self)

        self._currentCondition = {'code': '', 'name': ''}
        self._conditionList = list()

    currentConditionChanged = pyqtSignal()

    @pyqtProperty(QVariant)
    def currentCondition(self):
        return self._currentCondition

    @currentCondition.setter
    def currentCondition(self, condition: dict):
        logger.debug(f'condition: {condition}')
        if isinstance(condition, dict):
            self._currentCondition = condition
        else:
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

    def getConditionList(self):
        logger.debug('')
        km = pkm.pkm()
        cmd = {
            'func_name': 'GetConditionNameList'
        }
        km.put_cond(cmd)
        conditionList = list()
        conditionListRaw = km.get_cond(method=True)
        logger.debug(conditionListRaw)
        for conditionRaw in conditionListRaw:
            cond = {'code': conditionRaw[0], 'name': conditionRaw[1]}
            conditionList.append(cond)

        self.conditionList = conditionList


