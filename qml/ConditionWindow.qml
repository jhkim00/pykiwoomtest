import QtQuick 2.15
import QtQuick.Controls 2.15
import "./component"

ApplicationWindow {
    id: root
    visible: true
    width: 800
    height: 480
    title: "pykiwoomtest condition"

    function setCurrentCondition(condition) {
        console.log("setCurrentCondition")
        if (typeof(condition) !== 'undefined') {
            conditionController.currentCondtion = condition

            console.log("setCurrentCondition name:%1, code:%2".arg(condition["name"]).arg(condition["code"]))
        }
    }

    ConditionListView {
        width: 240
        height: parent.height
        model: conditionList

        onItemClicked: {
            console.log('onItemClicked' + itemData)
            console.log('onItemClicked ' + itemData['name'] + ', '+ itemData['code'])

            root.setCurrentCondition(itemData)
        }
    }
}
