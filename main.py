from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView
# from PyQt5.QtQuick import QQuickWindow

from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import Qt

import sys
from functools import partial


def _handleQmlWarnings(warnings):
    for warning in warnings:
        print("QML Warning:", warning.toString())


def _onMainWindowClosed(sender, close_):
    print('onMainWindowClosed')
    for rootObj in engine.rootObjects():
        if rootObj != sender:
            print('onMainWindowClosed 1')
            rootObj.close()
        else:
            print('onMainWindowClosed 2')
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.warnings.connect(_handleQmlWarnings)
    engine.load(QUrl.fromLocalFile("Main.qml"))
    engine.load(QUrl.fromLocalFile("Sub.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

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

    sys.exit(app.exec_())