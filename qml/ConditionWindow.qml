import QtQuick 2.15
import QtQuick.Controls 2.15
import "./component"

ApplicationWindow {
    id: root
    visible: true
    width: 800
    height: 480
    title: "pykiwoomtest condition"

    property var conditionStockListViewDict: {}
    property var currentStockListView: null

    Component.onCompleted: {
        conditionController.getConditionList()
    }

    function createConditionStockListView(name, index) {
        console.log('createConditionStockListView ' + name + ', '+ index)
        var conditionStockList = conditionController.getConditionStockList(index)
        var componentInstance = stockPriceListViewComponent.createObject(root, { "x": 240, "model": conditionStockList })
        return componentInstance
    }

    Connections {
        target: conditionController
        function onConditionStockChanged(conditionIndex) {
            console.log('onConditionStockChanged ' + conditionIndex)
            if (typeof(conditionStockListViewDict) !== 'undefined') {
                var view = conditionStockListViewDict[conditionIndex]
                if (typeof(view) !== 'undefined' && view === currentStockListView) {
                    view.model = conditionController.getConditionStockList(conditionIndex)
                }
            }
        }
    }

    ConditionListView {
        id: conditionListView
        width: 240
        height: parent.height
        model: conditionList

        onItemClicked: {
            console.log('conditionListView onItemClicked ' + itemData['name'] + ', '+ itemData['code'])
            var newStockListView = null
            if (conditionController.registerCondition(itemData['code'])) {
                newStockListView = createConditionStockListView(itemData['name'], itemData['code'])
                if (typeof(conditionStockListViewDict) === 'undefined') {
                    console.log('conditionStockListViewDict is undefined... ???')
                    conditionStockListViewDict = {}
                }
                conditionStockListViewDict[itemData['code']] = newStockListView
            } else {
                if (itemData['code'] in conditionStockListViewDict) {
                    newStockListView = conditionStockListViewDict[itemData['code']]
                }
            }
            if (newStockListView !== null) {
                if (currentStockListView != null) {
                    currentStockListView.visible = false
                }
                newStockListView.visible = true
                currentStockListView = newStockListView
            }
        }
    }

    Component {
        id: stockPriceListViewComponent
        StockPriceListView {
            width: parent.width - conditionListView.width
            height: conditionListView.height

            onItemClicked: {
                console.log('onItemClicked ' + itemData['name'] + ', '+ itemData['code'])
                conditionController.onCurrentStock(itemData['name'], itemData['code'])
            }
        }
    }
}
