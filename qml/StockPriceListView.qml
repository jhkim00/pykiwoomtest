import QtQuick 2.15
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import "./component"

ListView {
    id: root

    clip: true
    boundsBehavior: Flickable.StopAtBounds

    signal itemClicked(variant itemData)

    delegate: StockPriceDelegate {
        listView: root
        width: root.width
    }
}
