import QtQuick 2.15
import QtQuick.Controls 2.15
import "./component"

ApplicationWindow {
    visible: true
    width: 800
    height: 480
    title: "My Application"

    StockInfo {
        id: stockInfo
        width: parent.width
        height: 100
    }

    StockListView {
        anchors.top: stockInfo.bottom
        width: 240
        height: parent.height - stockInfo.height
    }
}
