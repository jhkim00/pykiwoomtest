import QtQuick 2.15
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4

Rectangle {
    id: root
    height: 40
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
    PriceWidget {
        id: priceRow
        x: 120
        height: parent.height
        anchors.verticalCenter: parent.verticalCenter
        code: modelData['code']
        priceInfo: modelData['priceInfo']
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