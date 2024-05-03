import QtQuick 2.15
import QtQuick.Controls 2.15
import "./component"

Rectangle {
    id: root

    color: "#dd333333"
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
    property string sinyongRate: ''

    property bool isFavorite: false

    function updateFavorite() {
        console.log('updateFavorite')
        isFavorite = favoriteStockController.isFavoriteStock(stockCode)
    }

    function numberStrToNonAbsFormated(numberStr) {
        var result = '';
        var strLength = numberStr.length;
        var commaIndex = strLength % 3;

        // 소수점의 위치 파악
        var decimalIndex = numberStr.indexOf('.');
        if (decimalIndex === -1) {
            decimalIndex = strLength; // 소수점이 없으면 문자열의 길이로 설정
        }

        for (var i = 0; i < strLength; i++) {
            result += numberStr[i];
            if (i === commaIndex - 1 && i !== strLength - 1 && i < decimalIndex - 1) {
                result += ',';
                commaIndex += 3;
            }
        }

        return result;
    }

    function numberStrToFormated(numberStr) {
        // 숫자 문자열에서 '+' 또는 '-' 기호 제거
        numberStr = numberStr.replace(/^[-+]/, '');

        return numberStrToNonAbsFormated(numberStr)
    }

    Component.onCompleted: {
        console.log('StockInfo.qml Component.onCompleted.')
        stockName = stockInfoController.currentStock['name']
        stockCode = stockInfoController.currentStock['code']
        stockInfoController.getBasicInfo()
        updateFavorite()
    }

    Connections {
        target: stockInfoController
        function onCurrentStockChanged() {
            console.log('!!!!!!!!!!!onCurrentStockChanged: %1 %2'
                        .arg(stockInfoController.currentStock['name'])
                        .arg(stockInfoController.currentStock['code']))

            stockName = stockInfoController.currentStock['name']
            stockCode = stockInfoController.currentStock['code']

            stockInfoController.getBasicInfo()
            updateFavorite()
        }
        function onBasicInfoChanged() {
            console.log('onBasicInfoChanged')

            sichong = stockInfoController.basicInfo['시가총액']
            per = stockInfoController.basicInfo['PER']
            pbr = stockInfoController.basicInfo['PBR']
            maechul = stockInfoController.basicInfo['매출액']
            operatingProfit = stockInfoController.basicInfo['영업이익']
            netProfit = stockInfoController.basicInfo['당기순이익']
            yootongNumber = stockInfoController.basicInfo['유통주식']
            yootongRate = stockInfoController.basicInfo['유통비율']
            sinyongRate = stockInfoController.basicInfo['신용비율']
        }
    }

    Connections {
        target: favoriteStockController
        function onFavoriteStockChanged() {
            console.log('onFavoriteStockChanged')
            updateFavorite()
        }
    }

    Item {
        id: stockNameAndCode
        anchors.verticalCenter: parent.verticalCenter
        width: 150
        height: parent.height

        Item {
            x: 10
            width: parent.width - x
            height: 20
            anchors.bottom: parent.verticalCenter
            Text {
                anchors.verticalCenter: parent.verticalCenter
                text: stockName
                font.pixelSize: 20
                font.bold: true
                color: 'white'
            }
        }
        Item {
            x: 10
            width: parent.width - x
            height: 14
            anchors.top: parent.verticalCenter
            Text {
                anchors.verticalCenter: parent.verticalCenter
                text: stockCode
                font.pixelSize: 12
                font.bold: false
                color: 'white'
            }
        }
        TextButton {
            id: favoriteBtn
            width: 30
            height: 30
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.rightMargin: 10
            anchors.bottomMargin: 10
            text:  isFavorite ? '-' : '+'
            textSize: 20
            normalColor: 'grey'
            radius: 10
            onBtnClicked: {
                console.log('%1 button clicked.'.arg(text))
                isFavorite ? favoriteStockController.delete(stockCode)
                           : favoriteStockController.add(stockName, stockCode)
            }
        }
    }

    Row {
        id: basicInfo
        height: parent.height * 0.5 - anchors.topMargin
        anchors.top: parent.top
        anchors.topMargin: 10
        anchors.left: stockNameAndCode.right

        VerticalKeyValueLabel {
            keyText: '시가총액'
            valueText: numberStrToFormated(sichong)
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
            valueText: numberStrToFormated(maechul)
        }
        VerticalKeyValueLabel {
            keyText: '영업이익'
            valueText: numberStrToFormated(operatingProfit)
        }
        VerticalKeyValueLabel {
            keyText: '당기순이익'
            valueText: numberStrToFormated(netProfit)
        }
        VerticalKeyValueLabel {
            keyText: '유통주식'
            valueText: numberStrToFormated(yootongNumber)
        }
        VerticalKeyValueLabel {
            keyText: '유통비율'
            valueText: yootongRate + ' %'
        }
        VerticalKeyValueLabel {
            keyText: '신용비율'
            valueText: numberStrToFormated(sinyongRate) + ' %'
        }
    }

    PriceWidget {
        id: priceInfo
        height: basicInfo.height
        anchors.top: basicInfo.bottom
        anchors.topMargin: 10
        anchors.left: basicInfo.left

        textBasicColor: 'white'

        code: stockCode
        priceInfo: stockInfoController.priceInfo
    }
}