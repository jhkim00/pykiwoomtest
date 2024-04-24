from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal, QVariant
import logging

import pkm

logger = logging.getLogger()


class MainController(QObject):
    def __init__(self, qmlContext, parent=None):
        super().__init__(parent)
        self.qmlContext = qmlContext
        self.qmlContext.setContextProperty('mainController', self)

        self._codeList = None
        self._codeMasterList = list()
        self._searchedStockList = list()
        self._currentStock = {'code': '', 'name': ''}

        self.qmlContext.setContextProperty("searchedStockList", self._searchedStockList)

    currentStockChanged = pyqtSignal(dict)

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

    @pyqtProperty(QVariant, notify=currentStockChanged)
    def currentStock(self):
        return self._currentStock

    @currentStock.setter
    def currentStock(self, stock: dict):
        if isinstance(stock, dict):
            self._currentStock = stock
        else:
            self._currentStock = stock.toVariant()

        logger.debug(f'self._currentStock: {self._currentStock}')
        self.currentStockChanged.emit(self._currentStock)

    @pyqtSlot(dict)
    def onCurrentStock(self, stock: dict):
        logger.debug(f'stock: {stock}')
        self.currentStock = stock

    @pyqtSlot()
    def login(self):
        logger.debug('')

        pkm.pkm()

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
        km = pkm.pkm()
        km.put_method(("GetCodeListByMarket", "0"))
        km.put_method(("GetCodeListByMarket", "10"))
        kospi = km.get_method()
        kosdaq = km.get_method()
        self._codeList = kospi + kosdaq

        for code in self._codeList:
            km.put_method(('GetMasterCodeName', code))
            masterName = km.get_method()
            self._codeMasterList.append({'code': code, 'name': masterName})

        # logger.debug(self._codeMasterList)

        # self.currentStock = self.codeMasterList[0]
        self.searchedStockList = self.codeMasterList

        self.qmlContext.setContextProperty('codeMasterList', self.codeMasterList)
        self.qmlContext.setContextProperty('searchedStockList', self.searchedStockList)
