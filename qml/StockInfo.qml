import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: root

    color: "#dd000000"
    clip: true

    property string stockName: ''
    property string stockCode: ''

    Connections {
        target: mainController
        onCurrentStockChanged: {
            console.log('onCurrentStockChanged name:' + mainController.currentStock['name'])
            console.log('onCurrentStockChanged code:' + mainController.currentStock['code'])
            stockName = mainController.currentStock['name']
            stockCode = mainController.currentStock['code']
        }
    }

    Item {
        id: stockNameAndCode
        width: 200
        height: 50

        Item {
            x: 10
            width: parent.width - x
            height: 18
            Text {
                anchors.verticalCenter: parent.verticalCenter
                text: stockName
                font.pixelSize: 16
                color: 'green'
            }
        }
        Item {
            x: 10
            y: 20
            width: parent.width - x
            height: 14
            Text {
                anchors.verticalCenter: parent.verticalCenter
                text: stockCode
                font.pixelSize: 12
                font.bold: false
                color: 'red'
            }
        }
    }
}