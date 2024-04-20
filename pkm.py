import sys
import logging
from PyQt5.QtCore import QThread, pyqtSignal, QObject
import kiwoom
import coolDown

logger = logging.getLogger()
_pkm = None
_coolDown = None


def pkm():
    global _pkm
    if _pkm is None:
        _pkm = kiwoom.KiwoomManager()
    return _pkm


def checkCollDown():
    global _coolDown
    if _coolDown is None:
        _coolDown = coolDown.CoolDown(limit=1, interval=0.3)

    _coolDown.call()
