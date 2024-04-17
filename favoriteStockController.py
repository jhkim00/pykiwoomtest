from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal, QVariant
import logging
import dbHelper

import pkm
import realDataWorker

logger = logging.getLogger()


class FavoriteStockController(QObject):
    def __init__(self, qmlContext, parent=None):
        super().__init__(parent)
        self.qmlContext = qmlContext
        self.qmlContext.setContextProperty('favoriteStockController', self)

        self._favoriteList = list()

        self.loadFavoriteStock()

        realDataWorker.RealDataWorker.getInstance().data_received.connect(self._onRealData)

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

        self._getRealData()

    def _getRealData(self):
        real_cmd = {
            'func_name': "SetRealReg",
            'real_type': '주식체결',
            'screen': '1000',
            'code_list': [item['code'] for item in self._favoriteList],
            'fid_list': ['20', '10', '11', '12', '13', '16', '17', '18', '25', '30'],
            "opt_type": 1
        }
        km = pkm.pkm()
        km.put_real(real_cmd)

    @pyqtSlot(dict)
    def _onRealData(self, data: dict):
        # logger.debug(data)
        code_list = [item['code'] for item in self._favoriteList]
        if data['code'] in code_list:
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

                logger.debug(f"code: {data['code']}")
                logger.debug(_priceInfo)


