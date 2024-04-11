import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: root

    color: "#dd000000"
    clip: true

    property string stockName: stockBasicInfoController.currentStock['name']
    property string stockCode: stockBasicInfoController.currentStock['code']


    Connections {
        target: stockBasicInfoController
        onCurrentStockChanged: {
            console.log('!!!!!!!!!!!onCurrentStockChanged: %1'.arg(stockBasicInfoController.currentStock['name']))
            console.log('!!!!!!!!!!!onCurrentStockChanged: %1'.arg(stockBasicInfoController.currentStock['code']))

            stockName = stockBasicInfoController.currentStock['name']
            stockCode = stockBasicInfoController.currentStock['code']

            stockBasicInfoController.getBasicInfo()
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