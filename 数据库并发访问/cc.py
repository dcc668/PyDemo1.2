# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cc.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from pymysql import Connection, cursors
import time
from threading import Thread
from 数据库并发访问.user_eo import UserEO
from 数据库并发访问.utils.db_utils import DBUtils
from 数据库并发访问.utils.dict2obj_utils import Dict2Obj

from PyQt5.QtCore import *

class BaseDao:
    def findById(self,id):
        #return dict
        conn = DBUtils.getConn();#有问题待解决
        # 关闭自动commit
        conn.autocommit(False)
        try:
            cursor = conn.cursor(cursor=cursors.DictCursor)
            sql = "select a.* from users a where a.id="+str(id)
            cursor.execute(sql)
            rs = cursor.fetchone()
            # print('------findById------>>>>retudict '+str(rs));
            user=Dict2Obj(rs);
        except Exception as e:
            print('error where execute update.......')
        finally:
            # conn.commit()
            # conn.close()
            pass
        return user;

    def updateUserNoLock(self, user):
        start = time.time()
        try:
            conn = DBUtils.getConn();  # 有问题待解决
            cursor = conn.cursor(cursor=cursors.DictCursor)
            sql = "select status from users where id = %d;" \
                  "update users set status = %d" \
                  ",userName = %s" \
                  ",password = %s" \
                  ",email = %s,money=%d;" \
                  % (user.id, user.status, user.userName, user.password, user.email, user.money)

            print('....execute...sql.....' + sql)
            cursor.execute(sql)
            print('....execute...sql.....')
        except Exception as e:
            conn.rollback();
            print('error where execute update.......')
            raise;
        finally:
            # conn.commit()
            # conn.close()
            pass
        print('....execute...sql...end..')
        end = time.time()
        print(str(end - start))
        return str(end - start)

    def updateUser(self, user):
        start = time.time()
        try:
            conn = DBUtils.getConn();  # 有问题待解决
            cursor = conn.cursor(cursor=cursors.DictCursor)
            sql = "select status from users where id = %d for update;" \
                      "update users set status = %d" \
                      ",userName = %s" \
                      ",password = %s" \
                      ",email = %s,money=%d;" \
                      % (user.id, user.status, user.userName, user.password, user.email, user.money)

            print('....execute...sql.....'+sql)
            cursor.execute(sql)
        except Exception as e:
            conn.rollback();
            print('error where execute update.......')
            raise;
        finally:
            # conn.commit()
            # conn.close()
            pass
        print('....execute...sql...end..')
        end = time.time()
        print(str(end-start))
        return str(end-start)
class Runthread(QtCore.QThread):
    # python3,pyqt5与之前的版本有些不一样
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(str)

    def __init__(self,base,sym):
        super(Runthread, self).__init__()
        self.base=base;
        self.sym=sym;
        self.times=0;
    def __del__(self):
        self.wait()

    def run(self):
        user = self.base.findById(1);
        user.money = user.money - 1
        if (self.sym):
             self.times=self.base.updateUser(user)
        else:
            self.times =self.base.updateUserNoLock(user)
        self._signal.emit(str(self.times));


MEMO=''
CISHU=0
import json
class Ui_MainWindow(object):
    def __init__(self):
        self.base = BaseDao();
        self.textB = QtWidgets.QTextBrowser()

    def modifyCiShu(self):
        global CISHU
        CISHU += 1
    def modifyMEMO(self,content):
        global MEMO
        MEMO +=(content+'\n')
        return
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(696, 438)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 681, 51))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.verticalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 150, 681, 191))
        self.groupBox.setObjectName("groupBox")
        self.scrollArea = QtWidgets.QScrollArea(self.groupBox)
        self.scrollArea.setGeometry(QtCore.QRect(20, 20, 651, 151))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 649, 149))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 60, 681, 71))
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_2)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(410, 10, 79, 56))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.textEdit = QtWidgets.QTextEdit(self.groupBox_2)
        self.textEdit.setGeometry(QtCore.QRect(50, 20, 104, 31))
        self.textEdit.setObjectName("textEdit")
        user = self.base.findById(1);
        self.textEdit.setText(str(user.money))
        con='从数据库中获取到当前金额:' + str(user.money)
        self.modifyMEMO(con)
        self.textB.setText(MEMO)
        self.scrollArea.setWidget(self.textB)
        self.radioButton = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton.setGeometry(QtCore.QRect(260, 40, 89, 16))
        self.radioButton.setChecked(False)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox_2)
        self.radioButton_2.setGeometry(QtCore.QRect(260, 20, 89, 16))
        self.radioButton_2.setChecked(True)
        self.radioButton_2.setObjectName("radioButton_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 696, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(self.buy_goods)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "消费记录"))
        self.groupBox_2.setTitle(_translate("MainWindow", "金额"))
        self.pushButton.setText(_translate("MainWindow", "消费1元"))
        self.radioButton.setText(_translate("MainWindow", "悲观锁"))
        self.radioButton_2.setText(_translate("MainWindow", "乐观锁"))
        self.menu.setTitle(_translate("MainWindow", "设置"))
        self.menu_2.setTitle(_translate("MainWindow", "关于"))

    def buy_goods(self):
        sym=self.radioButton.isChecked()
        t = Runthread(self.base,sym)
        t._signal.connect(self.callbacklog)
        t.start()

    def callbacklog(self,times):
        print('-------->>>111');
        self.modifyCiShu()
        con='第'+str(CISHU)+'次消费，耗时：'+str(times)
        self.modifyMEMO(con)
        self.textB.setText(MEMO)
        print(MEMO)
        self.scrollArea.setWidget(self.textB)
        user = self.base.findById(1);
        self.textEdit.setText(str(user.money))

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = QtWidgets.QMainWindow()
    main=Ui_MainWindow()
    main.setupUi(ex)
    ex.show()
    sys.exit(app.exec_())