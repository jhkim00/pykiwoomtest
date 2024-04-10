from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal
import logging
import pykiwoom
import time

logger = logging.getLogger()


class MainController(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.km = None
        self._test = 'test'
        self.codeList = None
        self._codeMasterList = list()
        self.codeMasterDict = dict()
        self._searchedStockList = list()
        self.qmlContext = None

    @pyqtProperty(str)
    def test(self):
        return self._test

    @property
    def codeMasterList(self):
        return self._codeMasterList

    @property
    def searchedStockList(self):
        return self._searchedStockList

    @searchedStockList.setter
    def searchedStockList(self, stockList: list):
        self._searchedStockList = stockList
        self.qmlContext.setContextProperty("searchedStockList", self._searchedStockList)

    @pyqtSlot()
    def login(self):
        logger.debug('login')
        if self.km is None:
            self.km = pykiwoom.KiwoomManager()

        self._getCodeList()

    @pyqtSlot(str)
    def onInputTextChanged(self, inputText):
        logger.debug(inputText)

        if len(inputText) == 0 or inputText == ' ':
            self.searchedStockList = self.codeMasterList
        else:
            self.searchedStockList = list(map(lambda x: x,
                                              list(filter(lambda x: x["name"].lower().find(inputText.lower()) != -1
                                                   or x["code"].lower().find(inputText.lower()) != -1,
                                                   self.codeMasterList))))

    def _getCodeList(self):
        km = self.km
        km.put_method(("GetCodeListByMarket", "0"))
        km.put_method(("GetCodeListByMarket", "10"))
        kospi = km.get_method()
        kosdaq = km.get_method()
        self.codeList = kospi + kosdaq
        # logger.debug(self.codeList)
        for code in self.codeList:
            km.put_method(('GetMasterCodeName', code))
            masterName = km.get_method()
            self._codeMasterList.append({'code': code, 'name': masterName})
            # self.codeMasterDict[code] = masterName

        # logger.debug(self._codeMasterList)

        self.searchedStockList = self.codeMasterList

        self.qmlContext.setContextProperty('codeMasterList', self.codeMasterList)
        self.qmlContext.setContextProperty('searchedStockList', self.searchedStockList)
