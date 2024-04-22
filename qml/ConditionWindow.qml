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
            conditionController.currentCondtion = condition // 이 코드가 안먹혀서 할 수 없이 아래 코드 추가함....
            conditionController.setCurrentCondition(condition)

            var cond = conditionController.currentCondtion
            if (typeof(cond) !== 'undefined') {
                console.log("conditionController.currentCondtion name:%1, code:%2".arg(cond["name"]).arg(cond["code"]))
            }
            else {
                console.log("conditionController.currentCondtion is undefined....")
            }
            conditionController.getCondition()
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
