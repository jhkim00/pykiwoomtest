import QtQuick 2.15
import QtQuick.Controls 2.15
import "./component"

ApplicationWindow {
    id: root
    visible: true
    width: 800
    height: 480
    title: "pykiwoomtest condition"

    Component.onCompleted: {
        conditionController.getConditionList()
    }

    ConditionListView {
        width: 240
        height: parent.height
        model: conditionList

        onItemClicked: {
            console.log('onItemClicked ' + itemData['name'] + ', '+ itemData['code'])
            conditionController.getCondition(itemData['code'])
        }
    }
}
