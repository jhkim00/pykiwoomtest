from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView
# from PyQt5.QtQuick import QQuickWindow

from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import Qt

import sys
import logging
import time
from functools import partial

import mainController
import conditionController

logger = logging.getLogger()


def _handleQmlWarnings(warnings):
    for warning in warnings:
        print("QML Warning:", warning.toString())


def _onMainWindowClosed(sender, close_):
    logger.debug('onMainWindowClosed')
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

    mainController = mainController.MainController(engine.rootContext(), app)

    engine.load(QUrl.fromLocalFile("qml/Main.qml"))
    engine.load(QUrl.fromLocalFile("qml/ConditionWindow.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    # engine.rootObjects()[0].raise()

    # # QQuickView 생성
    # view = QQuickView()
    # view.setSource(QUrl.fromLocalFile("Sub.qml"))
    #
    # # QQmlApplicationEngine에서 rootContext를 설정
    # view.rootContext().setContextProperty("engine", engine)
    #
    # # QQuickView 표시
    # view.show()

    main_window = engine.rootObjects()[0]
    main_window.closing.connect(partial(_onMainWindowClosed, main_window))

    mainController.login()

    conditionController = conditionController.ConditionController(mainController.km, engine.rootContext(), app)

    sys.exit(app.exec_())