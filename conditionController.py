from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal, QVariant
import logging
import pykiwoom

logger = logging.getLogger()


class ConditionController(QObject):
    def __init__(self, kiwoomManager: pykiwoom.KiwoomManager, qmlContext, parent=None):
        super().__init__(parent)
        self.qmlContext = qmlContext
        self.qmlContext.setContextProperty('conditionController', self)
        self.km = kiwoomManager

        self._conditionList = list()
        self._getConditionList()
        logger.debug(self._conditionList)

    @property
    def conditionList(self):
        return self._conditionList

    @conditionList.setter
    def conditionList(self, conditionList: list):
        self._conditionList = conditionList
        self.qmlContext.setContextProperty("conditionList", self._conditionList)

    def _getConditionList(self):
        logger.debug('')
        km = self.km
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


