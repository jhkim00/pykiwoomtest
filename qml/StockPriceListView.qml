import QtQuick 2.15
import QtQuick.Controls 1.4
import QtQuick.Controls.Styles 1.4
import "./component"

ListView {
    id: root

    clip: true
    boundsBehavior: Flickable.StopAtBounds

    signal itemClicked(variant itemData)

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

    delegate: StockPriceDelegate {
        listView: root
        width: root.width
    }
}
