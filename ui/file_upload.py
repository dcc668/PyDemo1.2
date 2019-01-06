#!  /usr/bin/env python
#ecoding=utf-8
from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QFileDialog,QMainWindow,QMenuBar,QStatusBar, QWidget, QPushButton,QScrollArea,QHBoxLayout,QProgressBar
import sys

class MyWindow(QtWidgets.QWidget):
    def __init__(self,MainWindow):
        super(MyWindow, self).__init__()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(696, 438)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 120, 211, 221))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(0, 350, 691, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.scrollArea = QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(210, 120, 461, 221))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 459, 219))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 20, 75, 23))
        self.pushButton.setBaseSize(QtCore.QSize(100, 200))
        self.pushButton.setAutoDefault(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.buttonClicked)
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 671, 121))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.horizontalLayout_2 = QHBoxLayout(self.verticalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 696, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "上传关键字"))
    def buttonClicked(self):
        directory1 = QFileDialog.getExistingDirectory(self,
                                                      "选取文件夹",
                                                      "C:/")  # 起始路径
        print(directory1)

        fileName1, filetype = QFileDialog.getOpenFileName(self,
                                                          "选取文件",
                                                          "C:/",
                                                          "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,注意用双分号间隔
        print(fileName1, filetype)

        files, ok1 = QFileDialog.getOpenFileNames(self,
                                                  "多文件选择",
                                                  "C:/",
                                                  "All Files (*);;Text Files (*.txt)")
        print(files, ok1)

        fileName2, ok2 = QFileDialog.getSaveFileName(self,
                                                     "文件保存",
                                                     "C:/",
                                                     "All Files (*);;Text Files (*.txt)")
class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 status bar example - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.statusBar().showMessage('Message in statusbar.')
        self.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main=App()
    myshow = MyWindow(main)
    myshow.show()
    sys.exit(app.exec_())