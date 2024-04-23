from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, QVariant
import logging

logger = logging.getLogger()


class PriceInfo(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._info = {
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

    infoChanged = pyqtSignal(QVariant)

    @pyqtProperty(QVariant, notify=infoChanged)
    def info(self):
        return self._info

    @info.setter
    def info(self, val):
        self._info = val
        self.infoChanged.emit(self._info)
