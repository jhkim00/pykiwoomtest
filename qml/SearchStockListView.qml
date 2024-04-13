import QtQuick 2.15
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4

Rectangle {
    id: root

    property alias inputText: textFieldInput.displayText

    function setStock(stock) {
        console.log("setStock")
        if (typeof(stock) !== 'undefined') {
            mainController.currentStock = stock

            console.log("setStock name:%1, code:%2".arg(stock["name"]).arg(stock["code"]))
            textFieldInput.text = stock["name"]
        }
    }

    TextField {
        id: textFieldInput
        width: parent.width
        height: 50
        placeholderText: "종목명 or 종목코드"
        textColor: 'black'
        style: TextFieldStyle {
            background: Rectangle {
                radius: 4
                color: 'lightgray'
                border.color: 'black'
                border.width: 2
            }
        }
        Keys.onReturnPressed: {
            console.log("onReturnPressed")
            var stock = listViewStock.getCurrentStock()
            if (typeof(stock) !== 'undefined') {
                root.setStock(stock)
            }
        }
        onDisplayTextChanged: {
            console.log('onDisplayTextChanged ' + displayText)
            mainController.onInputTextChanged(displayText)
        }
    }

    StockListView {
        id: listViewStock
        anchors.top: textFieldInput.bottom
        width: parent.width
        height: parent.height - textFieldInput.height
        visible: model != null && model.length > 0
        model: searchedStockList

        onItemClicked: {
            console.log('onItemClicked' + itemData)
            console.log('onItemClicked ' + itemData['name'] + ', '+ itemData['code'])

            root.setStock(itemData)
        }
    }
}