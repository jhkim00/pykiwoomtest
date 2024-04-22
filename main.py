from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView
# from PyQt5.QtQuick import QQuickWindow

from PyQt5.QtQml import QQmlApplicationEngine

import sys
import logging
from functools import partial

from controller import MainController, CandleChartController, FavoriteStockController, StockBasicInfoController,\
                       ConditionController
from model import CandleSocketServer, RealDataWorker
import realConditionWorker

logger = logging.getLogger()


def _handleQmlWarnings(warnings):
    for warning in warnings:
        print("QML Warning:", warning.toString())


def _onMainWindowClosed(sender, close_):
    logger.debug('')
    for rootObj in engine.rootObjects():
        if rootObj != sender:
            print('onMainWindowClosed 1')
            rootObj.close()
        else:
            print('onMainWindowClosed 2')
            pass


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
    engine.warnings.connect(_handleQmlWarnings)

    mainController = MainController(engine.rootContext(), app)
    stockInfoController = StockBasicInfoController(engine.rootContext(), app)
    conditionController = ConditionController(engine.rootContext(), app)
    candleChartController = CandleChartController(engine.rootContext(), app)
    favoriteStockController = FavoriteStockController(engine.rootContext(), app)

    mainController.currentStockChanged.connect(stockInfoController.onCurrentStockChanged)
    mainController.currentStockChanged.connect(candleChartController.onCurrentStockChanged)

    mainController.login()

    # conditionController.getConditionList()

    favoriteStockController.loadFavoriteStock()

    if len(favoriteStockController.favoriteList) == 0:
        mainController.currentStock = mainController.codeMasterList[0]
    else:
        mainController.currentStock = favoriteStockController.favoriteList[0]

    engine.load(QUrl.fromLocalFile("qml/Main.qml"))
    engine.load(QUrl.fromLocalFile("qml/ConditionWindow.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    main_window = engine.rootObjects()[0]
    main_window.closing.connect(partial(_onMainWindowClosed, main_window))

    RealDataWorker.getInstance().start()
    main_window.closing.connect(RealDataWorker.getInstance().putFinishMsg)

    realConditionWorker.RealConditionWorker.getInstance().start()
    main_window.closing.connect(realConditionWorker.RealConditionWorker.getInstance().putFinishMsg)
    CandleSocketServer.getInstance().start()
    main_window.closing.connect(CandleSocketServer.getInstance().putFinishMsg)

    sys.exit(app.exec_())
