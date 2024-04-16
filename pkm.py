import sys
import logging
from PyQt5.QtCore import QThread, pyqtSignal, QObject
import kiwoom

logger = logging.getLogger()
_pkm = None


def pkm():
    global _pkm
    if _pkm is None:
        _pkm = kiwoom.KiwoomManager()
    return _pkm
