import QtQuick 2.15
import QtQuick.Controls 2.15
import "./component"

ApplicationWindow {
    visible: true
    width: 800
    height: 480
    title: "pykiwoomtest condition"

    ConditionListView {
        width: 240
        height: parent.height
        model: conditionList
    }
}
