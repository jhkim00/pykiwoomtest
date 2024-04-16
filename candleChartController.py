from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal, QVariant
import logging

import pkm
import webSocketServer

logger = logging.getLogger()


class CandleChartController(QObject):
    def __init__(self, qmlContext, parent=None):
        super().__init__(parent)
        self.qmlContext = qmlContext
        self.qmlContext.setContextProperty('candleChartController', self)

        self._currentStock = {'code': '', 'name': ''}

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
        self.currentStockChanged.emit(self._currentStock)

    @pyqtSlot(dict)
    def onCurrentStockChanged(self, stock: dict):
        logger.debug(f'stock: {stock}')
        self.currentStock = stock

        self.getDailyChart()

    @pyqtSlot()
    def getDailyChart(self):
        logger.debug('')
        tr_cmd = {
            'rqname': "주식일봉차트",
            'trcode': 'opt10081',
            'next': '0',
            'screen': '1001',
            'input': {
                "종목코드": self._currentStock['code']
            },
            'output': ['종목코드', '현재가', '거래량', '거래대금', '일자', '시가', '고가', '저가', '수정주가구분', '수정비율', '대업종구분',
                       '소업종구분', '종목정보', '수정주가이벤트', '전일종가']
        }
        km = pkm.pkm()
        km.put_tr(tr_cmd)
        data, remain = km.get_tr()
        print(data)
        columns_to_keep = ['종목코드', '현재가', '거래량', '거래대금', '일자', '시가', '고가', '저가']
        data_ = data[columns_to_keep]
        new_column_names = {'종목코드': 'code', '현재가': 'close', '거래량': 'volume', '거래대금': 'transaction_amount',
                            '일자': 'date', '시가': 'open', '고가': 'high', '저가': 'low'}
        data_ = data_.rename(columns=new_column_names)
        print(data_)
        webSocketServer.WebSocketServer.getInstance().putData(data_)
