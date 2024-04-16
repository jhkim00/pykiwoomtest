import sys
import logging
import time
from PyQt5.QtCore import QThread, pyqtSignal, QObject
import pkm

logger = logging.getLogger()


class RealDataWorker(QThread):
    data_received = pyqtSignal(dict)
    instance = None

    def __init__(self):
        super().__init__()

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = RealDataWorker()
        return cls.instance

    def run(self):
        km = pkm.pkm()
        while True:
            # logger.debug('')
            data = km.get_real()
            # print(data)
            self.data_received.emit(data)

        self.quit()
