from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal, QVariant
import logging
import pandas as pd

from model import CandleSocketServer
import pkm

logger = logging.getLogger()


class CandleChartController(QObject):
    def __init__(self, qmlContext, parent=None):
        super().__init__(parent)
        self.qmlContext = qmlContext
        self.qmlContext.setContextProperty('candleChartController', self)

        self._currentStock = {'code': '', 'name': ''}
        self._dailyChart = None

        CandleSocketServer.getInstance().client_connected.connect(self.onChartClientConnected)

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
    def onChartClientConnected(self):
        logger.debug('')
        if self.currentStock['code'] != '' and self._dailyChart is not None:
            CandleSocketServer.getInstance().putData(self._dailyChart)

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
        pkm.checkCollDown()
        km = pkm.pkm()
        km.put_tr(tr_cmd)
        data, remain = km.get_tr()
        # print(data)
        if data.loc[0, '종목코드'] != self.currentStock['code']:
            logger.debug('code is different from current stock!!!!!!!!!!!!!!!!!!')
            return
        columns_to_keep = ['종목코드', '현재가', '거래량', '거래대금', '일자', '시가', '고가', '저가']
        data_ = data[columns_to_keep]
        new_column_names = {'종목코드': 'code', '현재가': 'close', '거래량': 'volume', '거래대금': 'transaction_amount',
                            '일자': 'date', '시가': 'open', '고가': 'high', '저가': 'low'}
        data_ = data_.rename(columns=new_column_names)
        data_['date'] = pd.to_datetime(data_['date'], format='%Y%m%d').astype(str)
        data_.loc[0, 'name'] = self.currentStock['name']
        print(data_)

        self._dailyChart = data_

        CandleSocketServer.getInstance().putData(data_)
