import QtQuick 2.15
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4

Row {
    id: root

    property color textBasicColor: 'black'

    property var code
    property var priceInfo
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
        root.updatePriceInfo()
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
        return textBasicColor
    }

    function updatePriceInfo() {
//            console.log('updatePriceInfo')
        if (priceInfo !== null && priceInfo !== undefined) {
            console.log('priceInfo !== null && priceInfo !== undefined code: %1'.arg(code))
            onPriceInfoInfoChanged(priceInfo.info)
            priceInfo.infoChanged.connect(onPriceInfoInfoChanged)
        }
    }

    function onPriceInfoInfoChanged(info) {
//            console.log('onPriceInfoInfoChanged')
        if (root === null) {
//                console.log('onPriceInfoInfoChanged root === null')
            return
        }
        try {
            root.startPrice = info['시가']
            root.highPrice = info['고가']
            root.lowPrice = info['저가']
            root.currentPrice = info['현재가']
            root.refPrice = info['기준가']
            root.diffSign = info['대비기호']
            root.diffPrice = info['전일대비']
            root.diffRate = info['등락율']
            root.volume = info['거래량']
            root.volumeRate = info['거래대비']

            root.priceColor = getPriceColor(root.currentPrice, root.refPrice)
        } catch (e) {
            console.log('????? An error occurred: ' + e)
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
        keyText: '현재가'
        valueText: root.numberStrToFormated(root.currentPrice)
        keyColor: textBasicColor
        valueColor: root.priceColor
    }
    VerticalKeyValueLabel {
        width: 40
        keyText: ''
        valueText: root.getDiffSignSymbol()
        keyColor: textBasicColor
        valueColor: root.priceColor
    }
    VerticalKeyValueLabel {
        width: 80
        keyText: '등락률'
        valueText: root.numberStrToNonAbsFormated(root.diffRate) + ' %'
        keyColor: textBasicColor
        valueColor: root.priceColor
    }
    VerticalKeyValueLabel {
        width: 80
        keyText: '시가'
        valueText: root.numberStrToFormated(root.startPrice)
        keyColor: textBasicColor
        valueColor: getPriceColor(root.startPrice, root.refPrice)
    }
    VerticalKeyValueLabel {
        width: 80
        keyText: '고가'
        valueText: root.numberStrToFormated(root.highPrice)
        keyColor: textBasicColor
        valueColor: getPriceColor(root.highPrice, root.refPrice)
    }
    VerticalKeyValueLabel {
        width: 80
        keyText: '저가'
        valueText: root.numberStrToFormated(root.lowPrice)
        keyColor: textBasicColor
        valueColor: getPriceColor(root.lowPrice, root.refPrice)
    }
    VerticalKeyValueLabel {
        width: 80
        keyText: '기준가'
        valueText: root.numberStrToFormated(root.refPrice)
        keyColor: textBasicColor
        valueColor: textBasicColor
    }
    VerticalKeyValueLabel {
        width: 80
        keyText: '전일대비'
        valueText: root.numberStrToFormated(root.diffPrice)
        keyColor: textBasicColor
        valueColor: root.priceColor
    }
    VerticalKeyValueLabel {
        keyText: '거래량'
        valueText: root.numberStrToFormated(root.volume)
        keyColor: textBasicColor
        valueColor: textBasicColor
    }
    VerticalKeyValueLabel {
        keyText: '거래대비'
        valueText: root.numberStrToFormated(root.volumeRate) + ' %'
        keyColor: textBasicColor
        valueColor: getPriceColor(root.volumeRate, 100)
    }
}