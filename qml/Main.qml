import QtQuick 2.15
import QtQuick.Controls 2.15
import "./component"

ApplicationWindow {
    visible: true
    width: 1200
    height: 480
    title: "pykiwoomtest"

    StockInfo {
        id: stockInfo
        width: parent.width
        height: 100
    }

    SearchStockListView {
        anchors.top: stockInfo.bottom
        width: 240
        height: parent.height - stockInfo.height
    }
}
