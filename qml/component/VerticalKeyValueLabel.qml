import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    id: root
    width: 80
    height: 50

    property string keyText
    property string valueText

    Item {
        x: 10
        width: parent.width - x
        height: 14
        Text {
            anchors.verticalCenter: parent.verticalCenter
            text: keyText
            font.pixelSize: 12
            color: 'white'
        }
    }
    Item {
        x: 10
        y: 20
        width: parent.width - x
        height: 18
        Text {
            anchors.verticalCenter: parent.verticalCenter
            text: valueText
            font.pixelSize: 14
            font.bold: true
            color: 'white'
        }
    }
}