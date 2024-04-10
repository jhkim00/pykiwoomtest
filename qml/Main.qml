import QtQuick 2.15
import QtQuick.Controls 2.15
import "./component"

ApplicationWindow {
    visible: true
    width: 200
    height: 100
    title: "My Application"

    Rectangle {
        width: parent.width
        height: parent.height
        color: "lightblue"
    }

    TextButton {
        anchors.fill: parent
        text: "Log In"
        textSize: 40
        textColor: "black"
//        normalColor: 'blue'

        onBtnClicked: {
            console.log('Log In btn clicked.')
            console.log(mainController)
            if (mainController && mainController !== undefined) {
                console.log('mainControllerr.test')
                console.log(mainController.test)
                mainController.login()
            }
        }
    }
}
