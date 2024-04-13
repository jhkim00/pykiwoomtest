from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal, QVariant
import logging

import pkm

logger = logging.getLogger()


class StockBasicInfoController(QObject):
    def __init__(self, qmlContext, parent=None):
        super().__init__(parent)
        self.qmlContext = qmlContext
        self.qmlContext.setContextProperty('stockInfoController', self)

        self._currentStock = {'code': '', 'name': ''}

        self._basicInfo = {
            '신용비율': '',
            '시가총액': '',
            'PER': '',
            'PBR': '',
            '매출액': '',
            '영업이익': '',
            '당기순이익': '',
            '유통주식': '',
            '유통비율': ''
        }

        self._priceInfo = {
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

    currentStockChanged = pyqtSignal(dict)
    basicInfoChanged = pyqtSignal(dict)
    priceInfoChanged = pyqtSignal(dict)

    @pyqtProperty(QVariant)
    def currentStock(self):
        return self._currentStock

    @currentStock.setter
    def currentStock(self, stock: dict):
        logger.debug(f'stock: {stock}')
        if isinstance(stock, dict):
            self._currentStock = stock
        else:
            self._currentStock = stock.toVariant()

        logger.debug(f'self._currentStock: {self._currentStock}')
        self.currentStockChanged.emit(self._currentStock)

    @pyqtProperty(QVariant)
    def basicInfo(self):
        return self._basicInfo

    @basicInfo.setter
    def basicInfo(self, info: dict):
        # logger.debug(f'info: {info}')
        if isinstance(info, dict):
            self._basicInfo = info
        else:
            self._basicInfo = info.toVariant()

        logger.debug(f'self._basicInfo: {self._basicInfo}')
        self.basicInfoChanged.emit(self._basicInfo)

    @pyqtProperty(QVariant)
    def priceInfo(self):
        return self._priceInfo

    @priceInfo.setter
    def priceInfo(self, price: dict):
        # logger.debug(f'price: {price}')
        if isinstance(price, dict):
            self._priceInfo = price
        else:
            self._priceInfo = price.toVariant()

        logger.debug(f'self._priceInfo: {self._priceInfo}')
        self.priceInfoChanged.emit(self._priceInfo)

    @pyqtSlot(dict)
    def onCurrentStockChanged(self, stock: dict):
        logger.debug(f'stock: {stock}')
        self.currentStock = stock

    @pyqtSlot()
    def getBasicInfo(self):
        logger.debug('')
        tr_cmd = {
            'rqname': "주식기본정보",
            'trcode': 'opt10001',
            'next': '0',
            'screen': '1000',
            'input': {
                "종목코드": self._currentStock['code']
            },
            'output': list(self._basicInfo.keys()) + list(self._priceInfo.keys())
        }
        km = pkm.pkm()
        km.put_tr(tr_cmd)
        data, remain = km.get_tr()
        print(data)

        self.basicInfo = data.iloc[0, :len(self.basicInfo)].to_dict()
        self.priceInfo = data.iloc[0, len(self.basicInfo):].to_dict()








