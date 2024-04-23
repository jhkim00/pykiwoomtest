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
            conditionController.currentCondition = condition
        }
    }

    Connections {
        target: conditionController
        function onCurrentConditionChanged() {
            console.log("conditionController onCurrentConditionChanged.")
            var cond = conditionController.currentCondition
            if (typeof(cond) !== 'undefined') {
                console.log("conditionController.currentCondtion name:%1, code:%2".arg(cond["name"]).arg(cond["code"]))
                conditionController.getCondition()
            }
            else {
                console.log("conditionController.currentCondtion is undefined....")
            }
        }
    }

    Component.onCompleted: {
        conditionController.getConditionList()
    }

    ConditionListView {
        width: 240
        height: parent.height
        model: conditionList

        onItemClicked: {
            console.log('onItemClicked ' + itemData['name'] + ', '+ itemData['code'])

            root.setCurrentCondition(itemData)
        }
    }
}
