from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal, QVariant
import logging
import pykiwoom

import pkm

logger = logging.getLogger()


class StockBasicInfoController(QObject):
    def __init__(self, qmlContext, parent=None):
        super().__init__(parent)
        self.qmlContext = qmlContext
        self.qmlContext.setContextProperty('stockBasicInfoController', self)

        self._currentStock = {'code': '', 'name': ''}

        self._basicInfo = {
            '신용비율': '',
            "시가총액": '',
            "PER": '',
            "PBR": '',
            "매출액": '',
            "영업이익": '',
            "당기순이익": '',
            "유통주식": '',
            "유통비율": ''
        }

    currentStockChanged = pyqtSignal(dict)

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
        logger.debug(f"name: {self._currentStock['name']}, code: {self._currentStock['code']}")
        self.currentStockChanged.emit(self._currentStock)

    @pyqtSlot(dict)
    def onCurrentStockChanged(self, stock: dict):
        logger.debug(f'stock: {stock}')
        self.currentStock = stock

    @pyqtSlot()
    def getBasicInfo(self):
        logger.debug('getBasicInfo')
        tr_cmd = {
            'rqname': "주식기본정보",
            'trcode': 'opt10001',
            'next': '0',
            'screen': '1000',
            'input': {
                "종목코드": self._currentStock['code']
            },
            'output': list(self._basicInfo.keys())
        }
        km = pkm.pkm()
        km.put_tr(tr_cmd)
        data, remain = km.get_tr()
        print(data)

        data_dict = data.iloc[0].to_dict()
        print(data_dict)





