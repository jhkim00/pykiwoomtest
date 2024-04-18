import QtQuick 2.15
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4

Rectangle {
    id: root
    height: 50
    border.color: 'black'
    border.width: 1

    property var listView

    Item {
        x: 10
        width: parent.width - x
        height: 18
        Text {
            id: listViewItemTextName
            anchors.verticalCenter: parent.verticalCenter
            text: modelData['name']
            font.pixelSize: 16
            color: 'white'
        }
    }
    Item {
        x: 10
        y: 20
        width: parent.width - x
        height: 14
        Text {
            id: listViewItemTextCode
            anchors.verticalCenter: parent.verticalCenter
            text: modelData['code']
            font.pixelSize: 12
            font.bold: false
            color: 'white'
        }
    }
    Row {
        id: priceRow
        x: 120
        height: parent.height
        anchors.verticalCenter: parent.verticalCenter

        property var priceInfo: modelData['priceInfo']
        property string startPrice: ''
        property string highPrice: ''
        property string lowPrice: ''
        property string currentPrice: ''
        property string refPrice: ''
        property string diffSign: ''
        property string diffPrice: ''
        property string diffRate: ''
        property string volume: ''
        property string volumeRate: ''
        property string priceColor: 'white'

        onPriceInfoChanged: {
            priceRow.updatePriceInfo()
        }

        Connections {
            target: favoriteStockController
            function onFavoriteStockPriceChanged(code, price) {
                console.log('onFavoriteStockPriceChanged code:%1 currentPrice:%2'.arg(code).arg(price['시가']))
                if (code === modelData['code']) {
//                    priceRow.priceInfo = price
                    priceRow.updatePriceInfo()
                }
            }
        }

        function updatePriceInfo() {
            console.log('updatePriceInfo')
            if (priceInfo !== undefined) {
                console.log('priceInfo !== undefined')
                startPrice = priceInfo['시가']
                highPrice = priceInfo['고가']
                lowPrice = priceInfo['저가']
                currentPrice = priceInfo['현재가']
                refPrice = priceInfo['기준가']
                diffSign = priceInfo['대비기호']
                diffPrice = priceInfo['전일대비']
                diffRate = priceInfo['등락율']
                volume = priceInfo['거래량']
                volumeRate = priceInfo['거래대비']

                priceColor = getPriceColor(currentPrice, refPrice)
            }
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

        function getPriceColor(price, refPrice) {
            var nPrice = parseInt(price)
            var nRef = parseInt(refPrice)
            if (nPrice > nRef) {
                return 'red'
            }
            if (nPrice < nRef) {
                return 'blue'
            }
            return 'black'
        }

        function getDiffSignSymbol() {
            switch (diffSign) {
            case '1': return "\u2b61"
            case '2': return "\u25b2"
            case '5': return "\u25bc"
            default: return ""
            }
        }

        VerticalKeyValueLabel {
            width: 80
            keyText: '시가'
            valueText: priceRow.numberStrToFormated(priceRow.startPrice)
            keyColor: 'black'
            valueColor: priceRow.getPriceColor(priceRow.startPrice, priceRow.refPrice)
        }
        VerticalKeyValueLabel {
            width: 80
            keyText: '고가'
            valueText: priceRow.numberStrToFormated(priceRow.highPrice)
            keyColor: 'black'
            valueColor: priceRow.getPriceColor(priceRow.highPrice, priceRow.refPrice)
        }
        VerticalKeyValueLabel {
            width: 80
            keyText: '저가'
            valueText: priceRow.numberStrToFormated(priceRow.lowPrice)
            keyColor: 'black'
            valueColor: priceRow.getPriceColor(priceRow.lowPrice, priceRow.refPrice)
        }
        VerticalKeyValueLabel {
            width: 80
            keyText: '현재가'
            valueText: priceRow.numberStrToFormated(priceRow.currentPrice)
            keyColor: 'black'
            valueColor: priceRow.priceColor
        }
        VerticalKeyValueLabel {
            width: 80
            keyText: '기준가'
            valueText: priceRow.numberStrToFormated(priceRow.refPrice)
            keyColor: 'black'
            valueColor: 'black'
        }
        VerticalKeyValueLabel {
            width: 40
            keyText: ''
            valueText: priceRow.getDiffSignSymbol()
            keyColor: 'black'
            valueColor: priceRow.priceColor
        }
        VerticalKeyValueLabel {
            width: 80
            keyText: '전일대비'
            valueText: priceRow.numberStrToFormated(priceRow.diffPrice)
            keyColor: 'black'
            valueColor: priceRow.priceColor
        }
        VerticalKeyValueLabel {
            width: 80
            keyText: '등락률'
            valueText: priceRow.numberStrToNonAbsFormated(priceRow.diffRate) + ' %'
            keyColor: 'black'
            valueColor: priceRow.priceColor
        }
        VerticalKeyValueLabel {
            keyText: '거래량'
            valueText: priceRow.numberStrToFormated(priceRow.volume)
            keyColor: 'black'
            valueColor: 'black'
        }
        VerticalKeyValueLabel {
            keyText: '거래대비'
            valueText: priceRow.numberStrToFormated(priceRow.volumeRate) + ' %'
            keyColor: 'black'
            valueColor: priceRow.getPriceColor(priceRow.volumeRate, 100)
        }
    }
    MouseArea {
        id: listViewItemMouseArea
        anchors.fill: parent
        onClicked: {
            console.log('onClicked %1'.arg(root.color))
            listView.itemClicked(modelData)
        }
    }

    states: [
        State {
            name: "normal"
            when: !listViewItemMouseArea.containsPress
            PropertyChanges { target: root; color: "white" }
            PropertyChanges { target: listViewItemTextName; color: "black" }
            PropertyChanges { target: listViewItemTextCode; color: "black" }
        },
        State {
            name: "pressed"
            when: listViewItemMouseArea.containsPress
            PropertyChanges { target: root; color: "lightskyblue" }
            PropertyChanges { target: listViewItemTextName; color: "white" }
            PropertyChanges { target: listViewItemTextCode; color: "white" }
        }
    ]
}