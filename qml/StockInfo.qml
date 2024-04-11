import QtQuick 2.15
import QtQuick.Controls 2.15
import "./component"

Rectangle {
    id: root

    color: "#dd000000"
    clip: true

    property string stockName: ''
    property string stockCode: ''

    property string sichong: ''
    property string per: ''
    property string pbr: ''
    property string maechul: ''
    property string operatingProfit: ''
    property string netProfit: ''
    property string yootongNumber: ''
    property string yootongRate: ''

    Connections {
        target: stockBasicInfoController
        onCurrentStockChanged: {
            console.log('!!!!!!!!!!!onCurrentStockChanged: %1'.arg(stockBasicInfoController.currentStock['name']))
            console.log('!!!!!!!!!!!onCurrentStockChanged: %1'.arg(stockBasicInfoController.currentStock['code']))

            stockName = stockBasicInfoController.currentStock['name']
            stockCode = stockBasicInfoController.currentStock['code']

            stockBasicInfoController.getBasicInfo()
        }
        onBasicInfoChanged: {
            console.log('!!!!!!!!!!!onBasicInfoChanged')

            sichong = stockBasicInfoController.basicInfo['시가총액']
            per = stockBasicInfoController.basicInfo['PER']
            pbr = stockBasicInfoController.basicInfo['PBR']
            maechul = stockBasicInfoController.basicInfo['매출액']
            operatingProfit = stockBasicInfoController.basicInfo['영업이익']
            netProfit = stockBasicInfoController.basicInfo['당기순이익']
            yootongNumber = stockBasicInfoController.basicInfo['유통주식']
            yootongRate = stockBasicInfoController.basicInfo['유통비율']
        }
    }

    Item {
        id: stockNameAndCode
        width: 100
        height: 50

        Item {
            x: 10
            width: parent.width - x
            height: 18
            Text {
                anchors.verticalCenter: parent.verticalCenter
                text: stockName
                font.pixelSize: 16
                font.bold: true
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

    Row {
        id: basicInfo
        height: 50
        anchors.left: stockNameAndCode.right

        VerticalKeyValueLabel {
            keyText: '시가총액'
            valueText: sichong
        }
        VerticalKeyValueLabel {
            keyText: 'PER'
            valueText: per
        }
        VerticalKeyValueLabel {
            keyText: 'PBR'
            valueText: pbr
        }
        VerticalKeyValueLabel {
            keyText: '매출액'
            valueText: maechul
        }
        VerticalKeyValueLabel {
            keyText: '영업이익'
            valueText: operatingProfit
        }
        VerticalKeyValueLabel {
            keyText: '당기순이익'
            valueText: netProfit
        }
        VerticalKeyValueLabel {
            keyText: '유통주식'
            valueText: yootongNumber
        }
        VerticalKeyValueLabel {
            keyText: '유통비율'
            valueText: yootongRate
        }
    }
}