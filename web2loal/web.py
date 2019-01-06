
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys,time
from web2loal.web2local import Html2Local
from PyQt5.QtCore import *
class Runthread(QtCore.QThread):
    # python3,pyqt5与之前的版本有些不一样
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(int)

    def __init__(self,domaim,path):
        super(Runthread, self).__init__()
        self.domaim=domaim;
        self.path=path;
        self.times=0;
    def __del__(self):
        self.wait()

    def run(self):
        msg=True
        try:
            html = Html2Local(self.domaim, self.path)
            html.html2local('/index.html')
        except Exception as e:
            msg=False
        time.sleep(3)
        print('=================end============')
        self._signal.emit(msg);


class Ui_MainWindow():
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(497, 279)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(180, 10, 151, 61))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setBaseSize(QtCore.QSize(20, 28))
        font = QtGui.QFont()
        font.setFamily("Adobe 宋体 Std L")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAcceptDrops(False)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setStyleSheet("")
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(30, 70, 461, 171))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit.setGeometry(QtCore.QRect(130, 30, 301, 31))
        self.textEdit.setObjectName("textEdit")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(40, 40, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.textEdit.setFont(font)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.textEdit_2 = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_2.setGeometry(QtCore.QRect(130, 80, 191, 31))
        self.textEdit_2.setAutoFillBackground(False)
        self.textEdit_2.setReadOnly(True)
        self.textEdit_2.setObjectName("textEdit_2")
        self.btn_select = QtWidgets.QPushButton(self.groupBox)
        self.btn_select.setGeometry(QtCore.QRect(340, 80, 91, 31))
        self.btn_select.setObjectName("btn_select")
        self.btn_select.clicked.connect(self.select_file)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(40, 90, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.start = QtWidgets.QPushButton(self.groupBox)
        self.start.setGeometry(QtCore.QRect(180, 130, 91, 31))
        self.start.setObjectName("start")
        self.start.clicked.connect(self.start_deal_with)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 497, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.label_finish = QtWidgets.QLabel(self.centralwidget)
        self.label_finish.setGeometry(QtCore.QRect(370, 240, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_finish.setFont(font)
        self.label_finish.setObjectName("label_finish")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def select_file(self):
        dialog = QtWidgets.QFileDialog()
        self.path=dialog.getExistingDirectory(caption='选取文件')
        print('-------------->>>path:'+self.path)
        self.textEdit_2.setText(self.path)

    def start_deal_with(self):
        print('finish.......')
        # self.label_finish.setText("操作中.....")
        domaim=self.textEdit.toPlainText()
        t = Runthread(domaim, self.path)
        t._signal.connect(self.callbacklog)
        t.start()

    def callbacklog(self,msg):
        print('finish.......')
        self.label_finish.setText("完成！")
    def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
            self.label.setText(_translate("MainWindow", "网页离线器"))
            self.label_2.setText(_translate("MainWindow", "输入网址："))
            self.btn_select.setText(_translate("MainWindow", "选择"))
            self.label_4.setText(_translate("MainWindow", "存储地址："))
            self.start.setText(_translate("MainWindow", "开始"))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = QtWidgets.QMainWindow()
    main=Ui_MainWindow()
    main.setupUi(ex)
    ex.show()
    sys.exit(app.exec_())