import QtQuick 2.15
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4

Rectangle {
    id: root

    property string stockName: ""
    property string stockCode: ""
    property alias inputText: textFieldInput.displayText

    signal inputTextCompleted()
    signal showAniamtionEnded()

    function setStock(stock) {
        console.log("setStock")
        if (typeof(stock) !== 'undefined') {
            mainController.currentStock = stock

            root.stockName = stock["name"]
            root.stockCode = stock["code"]
            console.log("setStock name:%1, code:%2".arg(stock["name"]).arg(stock["code"]))
            textFieldInput.text = stock["name"]
            root.inputTextCompleted()
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

    ListView {
        id: listViewStock
        anchors.top: textFieldInput.bottom
        width: parent.width
        height: parent.height - textFieldInput.height
        visible: model != null && model.length > 0
        clip: true
        model: searchedStockList
        boundsBehavior: Flickable.StopAtBounds

        function getCurrentStock() {
            if (model != null && currentIndex >= 0 && currentIndex < model.length) {
                return model[currentIndex]
            }
        }

        onModelChanged: {
            if (typeof(model) !== 'undefined' && model.length > 0) {
                console.log("onModelChanged")
                currentIndex = 0
            }
        }

        Keys.onUpPressed: {
            console.log("onUpPressed")
            if (currentIndex > 0) {
                --currentIndex
            }
            console.log(currentIndex)
        }

        Keys.onDownPressed: {
            console.log("onDownPressed");
            if (currentIndex < model.length - 1) {
                ++currentIndex
            }
            console.log(currentIndex)
        }

        delegate: Rectangle {
            id: listViewItem
            width: listViewStock.width
            height: 50
            border.color: 'black'
            border.width: 1

            Item {
                x: 10
                width: parent.width - x
                height: 18
                Text {
                    id: listViewItemTextName
                    anchors.verticalCenter: parent.verticalCenter
                    text: modelData['name']
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
                    id: listViewItemTextCode
                    anchors.verticalCenter: parent.verticalCenter
                    text: modelData['code']
                    font.pixelSize: 12
                    font.bold: false
                    color: 'red'
                }
            }
            MouseArea {
                id: listViewItemMouseArea
                anchors.fill: parent
                onClicked: {
                    root.setStock(modelData)
                }
            }

            states: [
                State {
                    name: "normal"
                    when: !listViewItemMouseArea.containsPress && listViewStock.currentIndex != index
                    PropertyChanges { target: listViewItem; color: "white" }
                    PropertyChanges { target: listViewItemTextName; color: "black" }
                    PropertyChanges { target: listViewItemTextCode; color: "black" }
                },
                State {
                    name: "pressed"
                    when: listViewItemMouseArea.containsPress
                    PropertyChanges { target: listViewItem; color: "lightskyblue" }
                    PropertyChanges { target: listViewItemTextName; color: "white" }
                    PropertyChanges { target: listViewItemTextCode; color: "white" }
                },
                State {
                    name: "focused"
                    when: listViewStock.currentIndex == index
                    PropertyChanges { target: listViewItem; color: "lightsteelblue" }
                    PropertyChanges { target: listViewItemTextName; color: "white" }
                    PropertyChanges { target: listViewItemTextCode; color: "white" }
                }
            ]
        }
    }
}