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
        id: searchStockListView
        anchors.top: stockInfo.bottom
        width: 240
        height: parent.height - stockInfo.height
    }

    StockListView {
        anchors.top: stockInfo.bottom
        anchors.left: searchStockListView.right
        width: parent.width - searchStockListView.width
        height: searchStockListView.height
        model: favoriteList

        onItemClicked: {
            console.log('onItemClicked ' + itemData['name'] + ', '+ itemData['code'])
            mainController.currentStock = itemData
        }
    }
}
