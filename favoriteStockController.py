from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal, QVariant
import logging
import dbHelper

import pkm

logger = logging.getLogger()


class FavoriteStockController(QObject):
    def __init__(self, qmlContext, parent=None):
        super().__init__(parent)
        self.qmlContext = qmlContext
        self.qmlContext.setContextProperty('favoriteStockController', self)

        self._favoriteList = list()

        self.loadFavoriteStock()

    favoriteStockChanged = pyqtSignal()

    def loadFavoriteStock(self):
        rows = dbHelper.DbHelper.getInstance().selectTableFavorite()
        stockList = list()
        logger.debug(rows)
        for item in rows:
            stockList.append({'name': item[0], 'code': item[1]})

        logger.debug(stockList)
        self.favoriteList = stockList

    @pyqtSlot(str, str)
    def add(self, name: str, code: str):
        dbHelper.DbHelper.getInstance().insertStockToTableFavorite(name, code)
        self.loadFavoriteStock()

    @pyqtSlot(str)
    def delete(self, code: str):
        dbHelper.DbHelper.getInstance().deleteStockFromTableFavorite(code)
        self.loadFavoriteStock()

    @pyqtSlot(str, result=bool)
    def isFavoriteStock(self, code):
        for stock in self._favoriteList:
            if stock['code'] == code:
                return True
        return False

    @property
    def favoriteList(self):
        return self._favoriteList

    @favoriteList.setter
    def favoriteList(self, favoriteList: list):
        self._favoriteList = favoriteList
        self.qmlContext.setContextProperty("favoriteList", self._favoriteList)

        self.favoriteStockChanged.emit()
