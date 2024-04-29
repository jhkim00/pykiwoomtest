from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty, pyqtSignal, QVariant, QMetaObject
import logging
import pandas as pd
import time

from model import CandleSocketServer, realDataWorker
import pkm

logger = logging.getLogger()


class CandleChartController(QObject):
    def __init__(self, qmlContext, parent=None):
        super().__init__(parent)
        self.qmlContext = qmlContext
        self.qmlContext.setContextProperty('candleChartController', self)

        self._currentStock = {'code': '', 'name': ''}
        self._dailyChart = None
        self._minuteChart = None
        self._chartUpdateTime = time.time()

        CandleSocketServer.getInstance().client_connected.connect(self.onChartClientConnected)
        realDataWorker.RealDataWorker.getInstance().data_received.connect(self._onRealData)

    currentStockChanged = pyqtSignal()

    @pyqtProperty(QVariant, notify=currentStockChanged)
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
        self.currentStockChanged.emit()

    @pyqtSlot(dict)
    def onCurrentStockChanged(self, stock: dict):
        logger.debug(f'stock: {stock}')
        self.currentStock = stock

        CandleSocketServer.getInstance().clearData()

        self.getDailyChart()
        self.getMinuteChart()

    @pyqtSlot()
    def onChartClientConnected(self):
        logger.debug('')
        if self.currentStock['code'] != '':
            if self._dailyChart is not None:
                CandleSocketServer.getInstance().putData(('day', self._dailyChart))
            if self._minuteChart is not None:
                CandleSocketServer.getInstance().putData(('minute', self._minuteChart))

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
        # print(data_)

        self._dailyChart = data_

        CandleSocketServer.getInstance().putData(('day', self._dailyChart))

    @pyqtSlot()
    def getMinuteChart(self):
        logger.debug('')
        tr_cmd = {
            'rqname': "주식분봉차트",
            'trcode': 'opt10080',
            'next': '0',
            'screen': '1001',
            'input': {
                "종목코드": self._currentStock['code'],
                "틱범위": "1"
            },
            'output': ['현재가', '거래량', '체결시간', '시가', '고가', '저가']
        }
        pkm.checkCollDown()
        km = pkm.pkm()
        km.put_tr(tr_cmd)
        data, remain = km.get_tr()
        # print(data)
        new_column_names = {'현재가': 'close', '거래량': 'volume', '체결시간': 'chegyeol_time',
                            '시가': 'open', '고가': 'high', '저가': 'low'}
        data_ = data.rename(columns=new_column_names)
        data_['chegyeol_time'] = pd.to_datetime(data_['chegyeol_time'], format='%Y%m%d%H%M%S')\
            .dt.strftime("%Y-%m-%d %H:%M")

        def remove_sign(x):
            import re
            return re.sub(r'[+-]', '', x)
        priceCols = ['close', 'open', 'high', 'low']
        data_[priceCols] = data_[priceCols].applymap(remove_sign)
        data_.loc[0, 'name'] = self.currentStock['name']
        data_.loc[0, 'code'] = self.currentStock['code']
        # print(data_)

        self._minuteChart = data_

        CandleSocketServer.getInstance().putData(('minute', self._minuteChart))
        self._chartUpdateTime = time.time()

    @pyqtSlot(dict)
    def _onRealData(self, data: dict):
        import re
        from datetime import datetime
        # logger.debug(data)
        if self._dailyChart is None:
            return

        if data['code'] == self._currentStock['code']:
            if data['rtype'] == '주식체결':
                if time.time() - self._chartUpdateTime < 1:
                    return

                _priceInfo = {
                    'code': '',
                    'close': '',
                    'open': '',
                    'high': '',
                    'low': '',
                    'volume': '',
                    'transaction_amount': ''
                    'chegyeol_time'
                }
                _priceInfo['close'] = re.sub(r'[+-]', '', data['10'])
                _priceInfo['volume'] = data['13']
                _priceInfo['transaction_amount'] = data['14']
                _priceInfo['open'] = re.sub(r'[+-]', '', data['16'])
                _priceInfo['high'] = re.sub(r'[+-]', '', data['17'])
                _priceInfo['low'] = re.sub(r'[+-]', '', data['18'])

                today_datetime = datetime.strptime(self._minuteChart.loc[0, 'chegyeol_time'], "%Y-%m-%d %H:%M")
                hour = int(data['20'][:2])
                minute = int(data['20'][2:4])
                new_datetime = today_datetime.replace(hour=hour, minute=minute)
                _priceInfo['chegyeol_time'] = new_datetime.strftime("%Y-%m-%d %H:%M")

                # logger.debug(f"before {self._dailyChart.iloc[0]}")

                self._dailyChart.loc[0, 'close'] = _priceInfo['close']
                self._dailyChart.loc[0, 'volume'] = _priceInfo['volume']
                self._dailyChart.loc[0, 'transaction_amount'] = _priceInfo['transaction_amount']
                self._dailyChart.loc[0, 'open'] = _priceInfo['open']
                self._dailyChart.loc[0, 'high'] = _priceInfo['high']
                self._dailyChart.loc[0, 'low'] = _priceInfo['low']

                # logger.debug(f"after {self._dailyChart.iloc[0]}")

                CandleSocketServer.getInstance().putData(('day', self._dailyChart))

                # logger.debug(f"before {self._minuteChart.iloc[0]}")

                time1 = datetime.strptime(self._minuteChart.loc[0, 'chegyeol_time'], "%Y-%m-%d %H:%M")
                time2 = datetime.strptime(_priceInfo['chegyeol_time'], "%Y-%m-%d %H:%M")

                logger.debug(f"_minuteChart time: {self._minuteChart.loc[0, 'chegyeol_time']}")
                logger.debug(f"_priceInfo time: {_priceInfo['chegyeol_time']}")

                if time1 != time2:
                    logger.debug("chegyeol_time is changed")
                    QMetaObject.invokeMethod(self, "getMinuteChart")
                    return

                self._minuteChart.loc[0, 'close'] = _priceInfo['close']
                volumeStr = re.sub(r'[+-]', '', data['15'])
                self._minuteChart.loc[0, 'volume'] = str(int(self._minuteChart.loc[0, 'volume']) + int(volumeStr))
                if _priceInfo['close'] > self._minuteChart.loc[0, 'high']:
                    self._minuteChart.loc[0, 'high'] = _priceInfo['close']
                if _priceInfo['close'] < self._minuteChart.loc[0, 'low']:
                    self._minuteChart.loc[0, 'low'] = _priceInfo['close']

                logger.debug(f"after {self._minuteChart.iloc[0]}")

                CandleSocketServer.getInstance().putData(('minute', self._minuteChart))

                self._chartUpdateTime = time.time()


