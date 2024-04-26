from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal
import logging

from model import dbHelper, realDataWorker
import pkm

logger = logging.getLogger()


class FavoriteStockController(QObject):
    def __init__(self, qmlContext, parent=None):
        super().__init__(parent)
        self.qmlContext = qmlContext
        self.qmlContext.setContextProperty('favoriteStockController', self)

        self._favoriteList = list()

        # self.loadFavoriteStock()

        realDataWorker.RealDataWorker.getInstance().data_received.connect(self._onRealData)

    favoriteStockChanged = pyqtSignal()

    def loadFavoriteStock(self):
        rows = dbHelper.DbHelper.getInstance().selectTableFavorite()
        stockList = list()
        logger.debug(rows)
        for item in rows:
            stockList.append({'name': item[0], 'code': item[1]})

        logger.debug(stockList)

        for stock in stockList:
            pkm.getStockPriceInfo('1001', stock)

        self.favoriteList = stockList

        pkm.getStockPriceRealData('1001', self._favoriteList)

    @pyqtSlot(str, str)
    def add(self, name: str, code: str):
        for stock in self._favoriteList:
            if stock['code'] == code:
                return

        dbHelper.DbHelper.getInstance().insertStockToTableFavorite(name, code)

        km = pkm.pkm()
        km.put_method(('SetRealRemove', '1001', 'ALL'))
        result = km.get_method()
        logger.debug(f'SetRealRemove result:{result}')

        stock = {'name': name, 'code': code}
        pkm.getStockPriceInfo('1001', stock)
        self._favoriteList.append(stock)

        pkm.getStockPriceRealData('1001', self._favoriteList)

        self.qmlContext.setContextProperty("favoriteList", self._favoriteList)
        self.favoriteStockChanged.emit()

    @pyqtSlot(str)
    def delete(self, code: str):
        stockToRemove = None
        for stock in self._favoriteList:
            if stock['code'] == code:
                dbHelper.DbHelper.getInstance().deleteStockFromTableFavorite(code)
                stockToRemove = stock
                break

        km = pkm.pkm()
        km.put_method(('SetRealRemove', '1001', 'ALL'))
        result = km.get_method()
        logger.debug(f'SetRealRemove result:{result}')

        self._favoriteList.remove(stockToRemove)

        pkm.getStockPriceRealData('1001', self._favoriteList)

        self.qmlContext.setContextProperty("favoriteList", self._favoriteList)
        self.favoriteStockChanged.emit()

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
        logger.debug('')
        self._favoriteList = favoriteList
        self.qmlContext.setContextProperty("favoriteList", self._favoriteList)

        self.favoriteStockChanged.emit()

    @pyqtSlot(dict)
    def _onRealData(self, data: dict):
        # logger.debug(data)
        isIn = False
        for stock in self._favoriteList:
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
