from PyQt5.QtCore import QUrl, QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView
# from PyQt5.QtQuick import QQuickWindow

from PyQt5.QtQml import QQmlApplicationEngine

import sys
import logging

from controller import MainController, CandleChartController, FavoriteStockController, StockBasicInfoController,\
                       ConditionController
from model import CandleSocketServer, RealDataWorker
import realConditionWorker

logger = logging.getLogger()


class WindowManager(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._windowList = list()

    def add_window(self, window):
        for win in self._windowList:
            if win == window:
                return
        self._windowList.append(window)

    @pyqtSlot()
    def onMainWindowClosed(self):
        for win in self._windowList:
            win.close()


def _handleQmlWarnings(warnings):
    for warning in warnings:
        print("QML Warning:", warning.toString())


if __name__ == "__main__":
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.DEBUG)
    rootLogger.propagate = 0
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(thread)d][%(filename)s:%(funcName)s:%(lineno)d]'
                                  ' %(message)s')
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    rootLogger.addHandler(streamHandler)

    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine2 = QQmlApplicationEngine()
    engine.warnings.connect(_handleQmlWarnings)
    engine2.warnings.connect(_handleQmlWarnings)

    mainController = MainController(engine.rootContext(), app)
    stockInfoController = StockBasicInfoController(engine.rootContext(), app)
    candleChartController = CandleChartController(engine.rootContext(), app)
    favoriteStockController = FavoriteStockController(engine.rootContext(), app)

    conditionController = ConditionController(engine2.rootContext(), app)

    mainController.currentStockChanged.connect(stockInfoController.onCurrentStockChanged)
    mainController.currentStockChanged.connect(candleChartController.onCurrentStockChanged)

    conditionController.currentStockChanged.connect(mainController.onCurrentStock)

    mainController.login()

    favoriteStockController.loadFavoriteStock()

    if len(favoriteStockController.favoriteList) == 0:
        mainController.currentStock = mainController.codeMasterList[0]
    else:
        mainController.currentStock = favoriteStockController.favoriteList[0]

    engine.load(QUrl.fromLocalFile("qml/Main.qml"))
    engine2.load(QUrl.fromLocalFile("qml/ConditionWindow.qml"))

    if not engine.rootObjects() or not engine2.rootObjects():
        sys.exit(-1)

    wm = WindowManager(app)

    main_window = engine.rootObjects()[0]
    condition_window = engine2.rootObjects()[0]
    wm.add_window(condition_window)
    main_window.closing.connect(wm.onMainWindowClosed)

    RealDataWorker.getInstance().start()
    main_window.closing.connect(RealDataWorker.getInstance().putFinishMsg)

    CandleSocketServer.getInstance().start()
    main_window.closing.connect(CandleSocketServer.getInstance().putFinishMsg)

    realConditionWorker.RealConditionWorker.getInstance().start()
    condition_window.closing.connect(realConditionWorker.RealConditionWorker.getInstance().putFinishMsg)

    sys.exit(app.exec_())
