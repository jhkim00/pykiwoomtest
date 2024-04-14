import QtQuick 2.15
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import "./component"

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
        Keys.onUpPressed: {
            console.log("onUpPressed")
            if (listViewStock.currentIndex > 0) {
                --listViewStock.currentIndex
            }
            console.log(listViewStock.currentIndex)
        }

        Keys.onDownPressed: {
            console.log("onDownPressed");
            if (listViewStock.currentIndex < listViewStock.model.length - 1) {
                ++listViewStock.currentIndex
            }
            console.log(listViewStock.currentIndex)
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

        TextButton {
            width: 30
            height: 30
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            anchors.rightMargin: 10
            text: "X"
            textSize: 20
            normalColor: 'grey'
            radius: 10
            onBtnClicked: {
                console.log('x button clicked.')
                textFieldInput.text = ''
            }
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