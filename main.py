import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PyQt5.QtCore import QUrl
from flask import Flask


app = Flask(__name__)
class WebPage(QWebEnginePage):
    def __init__(self, parent=None):
        super(WebPage, self).__init__(parent)

    def createWindow(self, _type):
        if _type == QWebEnginePage.WebBrowserTab:
            new_tab = QWebEngineView()
            new_tab.urlChanged.connect(self.onNewTabUrlChanged)
            return new_tab
        return super(WebPage, self).createWindow(_type)

    def onNewTabUrlChanged(self, q):
        new_tab = self.sender()
        self.view().setTabUrl(new_tab, new_tab.url())

# Define the UI class
class Ui_BladeGuardBrowser(object):
    def setupUi(self, BladeGuardBrowser):
        BladeGuardBrowser.setObjectName("BladeGuardBrowser")
        BladeGuardBrowser.resize(1337, 768)
        BladeGuardBrowser.setAutoFillBackground(False)

        self.tabs = []
        self.amount_of_tabs = 1

        self.centralwidget = QtWidgets.QWidget(BladeGuardBrowser)
        self.centralwidget.setObjectName("centralwidget")

        self.add_tab_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_tab_button.setGeometry(QtCore.QRect(2, 0, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(20)
        font.setBold(True)
        self.add_tab_button.setFont(font)
        self.add_tab_button.setFlat(False)
        self.add_tab_button.setObjectName("add_tab_button")
        self.add_tab_button.clicked.connect(self.make_tab)

        self.Tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.Tabs.setGeometry(QtCore.QRect(0, 32, 1337, 736))
        self.Tabs.setObjectName("Tabs")

        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        self.url_input = QtWidgets.QLineEdit(self.centralwidget)
        self.url_input.setGeometry(QtCore.QRect(70, 0, 1267, 31))
        self.url_input.setObjectName("url_input")
        self.url_input.setPlaceholderText("Search...")
        self.url_input.returnPressed.connect(self.load_url)

        self.remove_tab_button = QtWidgets.QPushButton(self.centralwidget)
        self.remove_tab_button.setGeometry(QtCore.QRect(36, 0, 31, 31))
        font = QtGui.QFont()
        font.setFamily("Yu Gothic UI Semilight")
        font.setPointSize(20)
        font.setBold(True)
        self.remove_tab_button.setFont(font)
        self.remove_tab_button.setFlat(False)
        self.remove_tab_button.setObjectName("remove_tab_button")
        self.remove_tab_button.clicked.connect(self.remove_tab)

        BladeGuardBrowser.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(BladeGuardBrowser)
        self.statusbar.setObjectName("statusbar")
        BladeGuardBrowser.setStatusBar(self.statusbar)

        self.retranslateUi(BladeGuardBrowser)
        self.Tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(BladeGuardBrowser)

    def retranslateUi(self, BladeGuardBrowser):
        _translate = QtCore.QCoreApplication.translate
        BladeGuardBrowser.setWindowTitle(_translate("BladeGuardBrowser", "BladeGuardBrowser"))
        self.add_tab_button.setText(_translate("BladeGuardBrowser", "+"))
        self.remove_tab_button.setText(_translate("BladeGuardBrowser", "-"))

    def make_tab(self):
        tab = QWebEngineView(self.centralwidget)
        tab.load(QUrl("https://www.google.com"))
        tab.urlChanged.connect(self.update_url_entry)

        # Handle the createWindow signal with a custom lambda function
        tab.page().createWindow = lambda _type: self.create_new_tab(_type)

        index = self.Tabs.addTab(tab, "Tab " + str(self.amount_of_tabs))
        self.tabs.append(tab)
        self.amount_of_tabs += 1
        self.Tabs.setCurrentIndex(index)

    def create_new_tab(self, _type):
        if _type == QWebEnginePage.WebBrowserTab:
            self.make_tab()
    def remove_tab(self):
        if self.amount_of_tabs > 1:
            current_tab_index = self.Tabs.currentIndex()
            current_tab = self.tabs[current_tab_index]

            # Find the corresponding index in the list
            tab_index = None
            for i, tab in enumerate(self.tabs):
                if tab is current_tab:
                    tab_index = i
                    break

            if tab_index is not None:
                self.Tabs.removeTab(current_tab_index)
                current_tab.deleteLater()
                del self.tabs[tab_index]
                self.amount_of_tabs -= 1

    def update_url_entry(self, q):
        current_tab = self.Tabs.currentWidget()
        if current_tab is not None and isinstance(current_tab, QWebEngineView):
            self.url_input.setText(current_tab.url().toString())

    def load_url(self):
        current_tab = self.Tabs.currentWidget()
        if current_tab is not None:
            url = self.url_input.text()
            current_tab.load(QUrl(url))


class BladeGuardBrowserApp(QtWidgets.QMainWindow, Ui_BladeGuardBrowser):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = BladeGuardBrowserApp()
    window.show()
    sys.exit(app.exec_())
