# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BDP_Parse.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt, QUrl

class ListBoxWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setGeometry(QtCore.QRect(200, 200, 200, 200))
 
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()
 
    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
 
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
 
            links = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))
            self.addItems(links)
        else:
            event.ignore()
            
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(709, 666)
        MainWindow.setAcceptDrops(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.PB_Quit = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.PB_Quit.setFont(font)
        self.PB_Quit.setObjectName("PB_Quit")
        self.gridLayout.addWidget(self.PB_Quit, 7, 5, 1, 1)
        self.PB_File = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.PB_File.setFont(font)
        self.PB_File.setObjectName("PB_File")
        self.gridLayout.addWidget(self.PB_File, 7, 1, 1, 1)
        self.PB_Clear = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.PB_Clear.setFont(font)
        self.PB_Clear.setObjectName("PB_Clear")
        self.gridLayout.addWidget(self.PB_Clear, 7, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 2, 3, 1)
        self.CB_SKUSelect = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_SKUSelect.setFont(font)
        self.CB_SKUSelect.setObjectName("CB_SKUSelect")
        self.CB_SKUSelect.addItem("")
        self.CB_SKUSelect.addItem("")
        self.CB_SKUSelect.addItem("")
        self.gridLayout.addWidget(self.CB_SKUSelect, 1, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 1, 1, 1)
        self.Text_drop = ListBoxWidget(self.centralwidget)
        self.Text_drop.setObjectName("Text_drop")
        self.Text_drop.addItem(QtWidgets.QListWidgetItem())
        self.Text_drop.item(0).setText("Drop Files Here:")
        self.gridLayout.addWidget(self.Text_drop, 3, 1, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setMinimumSize(QtCore.QSize(218, 459))
        self.scrollArea.setMaximumSize(QtCore.QSize(218, 459))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 216, 569))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.CB_SWversion = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_SWversion.setEnabled(False)
        self.CB_SWversion.setGeometry(QtCore.QRect(10, 250, 196, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_SWversion.setFont(font)
        self.CB_SWversion.setChecked(True)
        self.CB_SWversion.setObjectName("CB_SWversion")
        self.verticalLayout_3.addWidget(self.CB_SWversion)
        self.CB_1 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_1.setEnabled(True)
        self.CB_1.setGeometry(QtCore.QRect(10, 10, 138, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_1.setFont(font)
        self.CB_1.setChecked(True)
        self.CB_1.setObjectName("CB_1")
        self.verticalLayout_3.addWidget(self.CB_1)
        self.CB_6 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_6.setGeometry(QtCore.QRect(10, 184, 234, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_6.setFont(font)
        self.CB_6.setChecked(True)
        self.CB_6.setObjectName("CB_6")
        self.verticalLayout_3.addWidget(self.CB_6)
        self.CB_2 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_2.setGeometry(QtCore.QRect(10, 44, 138, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_2.setFont(font)
        self.CB_2.setChecked(True)
        self.CB_2.setObjectName("CB_2")
        self.verticalLayout_3.addWidget(self.CB_2)
        self.CB_7 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_7.setGeometry(QtCore.QRect(10, 217, 237, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_7.setFont(font)
        self.CB_7.setChecked(True)
        self.CB_7.setObjectName("CB_7")
        self.verticalLayout_3.addWidget(self.CB_7)
        self.CB_4 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_4.setGeometry(QtCore.QRect(10, 110, 295, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_4.setFont(font)
        self.CB_4.setChecked(True)
        self.CB_4.setObjectName("CB_4")
        self.verticalLayout_3.addWidget(self.CB_4)
        self.CB_5 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_5.setGeometry(QtCore.QRect(10, 150, 162, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_5.setFont(font)
        self.CB_5.setChecked(True)
        self.CB_5.setObjectName("CB_5")
        self.verticalLayout_3.addWidget(self.CB_5)
        self.CB_3 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_3.setGeometry(QtCore.QRect(10, 77, 295, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_3.setFont(font)
        self.CB_3.setChecked(True)
        self.CB_3.setObjectName("CB_3")
        self.verticalLayout_3.addWidget(self.CB_3)
        self.CB_31 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_31.setGeometry(QtCore.QRect(10, 77, 295, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_31.setFont(font)
        self.CB_31.setChecked(True)
        self.CB_31.setObjectName("CB_31")
        self.verticalLayout_3.addWidget(self.CB_31)
        self.CB_32 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_32.setGeometry(QtCore.QRect(10, 77, 295, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_32.setFont(font)
        self.CB_32.setChecked(True)
        self.CB_32.setObjectName("CB_32")
        self.verticalLayout_3.addWidget(self.CB_32)
        self.CB_33 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_33.setGeometry(QtCore.QRect(10, 77, 295, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_33.setFont(font)
        self.CB_33.setChecked(True)
        self.CB_33.setObjectName("CB_33")
        self.verticalLayout_3.addWidget(self.CB_33)
        self.CB_34 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_34.setGeometry(QtCore.QRect(10, 77, 295, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_34.setFont(font)
        self.CB_34.setChecked(True)
        self.CB_34.setObjectName("CB_34")
        self.verticalLayout_3.addWidget(self.CB_34)
        self.CB_35 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_35.setGeometry(QtCore.QRect(10, 77, 295, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_35.setFont(font)
        self.CB_35.setChecked(True)
        self.CB_35.setObjectName("CB_35")
        self.verticalLayout_3.addWidget(self.CB_35)
        self.CB_36 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_36.setGeometry(QtCore.QRect(10, 77, 295, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_36.setFont(font)
        self.CB_36.setChecked(True)
        self.CB_36.setObjectName("CB_36")
        self.verticalLayout_3.addWidget(self.CB_36)
        self.CB_37 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_37.setGeometry(QtCore.QRect(10, 77, 295, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_37.setFont(font)
        self.CB_37.setChecked(True)
        self.CB_37.setObjectName("CB_37")
        self.verticalLayout_3.addWidget(self.CB_37)
        self.CB_38 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_38.setGeometry(QtCore.QRect(10, 77, 295, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_38.setFont(font)
        self.CB_38.setChecked(True)
        self.CB_38.setObjectName("CB_38")
        self.verticalLayout_3.addWidget(self.CB_38)
        self.CB_39 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_39.setGeometry(QtCore.QRect(10, 77, 295, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_39.setFont(font)
        self.CB_39.setChecked(True)
        self.CB_39.setObjectName("CB_39")
        self.verticalLayout_3.addWidget(self.CB_39)
        self.CB_310 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_310.setGeometry(QtCore.QRect(10, 77, 295, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_310.setFont(font)
        self.CB_310.setChecked(True)
        self.CB_310.setObjectName("CB_310")
        self.verticalLayout_3.addWidget(self.CB_310)
        self.CB_311 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_311.setGeometry(QtCore.QRect(10, 77, 295, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_311.setFont(font)
        self.CB_311.setChecked(True)
        self.CB_311.setObjectName("CB_311")
        self.verticalLayout_3.addWidget(self.CB_311)
        self.CB_312 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_312.setGeometry(QtCore.QRect(10, 77, 295, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_312.setFont(font)
        self.CB_312.setChecked(True)
        self.CB_312.setObjectName("CB_312")
        self.verticalLayout_3.addWidget(self.CB_312)
        self.CB_313 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_313.setGeometry(QtCore.QRect(10, 77, 295, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_313.setFont(font)
        self.CB_313.setChecked(True)
        self.CB_313.setObjectName("CB_313")
        self.verticalLayout_3.addWidget(self.CB_313)
        self.CB_314 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_314.setGeometry(QtCore.QRect(10, 77, 295, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_314.setFont(font)
        self.CB_314.setChecked(True)
        self.CB_314.setObjectName("CB_314")
        self.verticalLayout_3.addWidget(self.CB_314)
        self.CB_315 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_315.setGeometry(QtCore.QRect(10, 77, 295, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_315.setFont(font)
        self.CB_315.setChecked(True)
        self.CB_315.setObjectName("CB_315")
        self.verticalLayout_3.addWidget(self.CB_315)
        self.CB_316 = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        self.CB_316.setGeometry(QtCore.QRect(10, 77, 295, 27))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.CB_316.setFont(font)
        self.CB_316.setChecked(True)
        self.CB_316.setObjectName("CB_316")
        self.verticalLayout_3.addWidget(self.CB_316)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 3, 3, 3, 3)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 3, 6, 3, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 1, 0, 5, 1)
        self.Text_status = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.Text_status.setObjectName("Text_status")
        self.gridLayout.addWidget(self.Text_status, 5, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 6, 1, 1, 5)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 0, 1, 1, 1)
        self.PB_Start = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        self.PB_Start.setFont(font)
        self.PB_Start.setObjectName("PB_Start")
        self.gridLayout.addWidget(self.PB_Start, 7, 3, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem6, 4, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        return self

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.PB_Quit.setText(_translate("MainWindow", "Quit"))
        self.PB_File.setText(_translate("MainWindow", "Add File"))
        self.PB_Clear.setText(_translate("MainWindow", "Clear"))
        self.CB_SKUSelect.setItemText(0, _translate("MainWindow", "OLxxx"))
        self.CB_SKUSelect.setItemText(1, _translate("MainWindow", "CM400"))
        self.CB_SKUSelect.setItemText(2, _translate("MainWindow", "CFPxxx"))
        self.CB_SWversion.setText(_translate("MainWindow", "Software version (WZ)"))
        self.CB_1.setText(_translate("MainWindow", "Heatsink (KN1)"))
        self.CB_6.setText(_translate("MainWindow", "Low Pressure Switch (SW1)"))
        self.CB_2.setText(_translate("MainWindow", "AF NTC (KN2)"))
        self.CB_7.setText(_translate("MainWindow", "High Pressure Switch (SW2)"))
        self.CB_4.setText(_translate("MainWindow", "Probe1 NTC (KN4)"))
        self.CB_5.setText(_translate("MainWindow", "Probe2 NTC (KN5)"))
        self.CB_3.setText(_translate("MainWindow", "PC NTC (KN3)"))
        self.CB_31.setText(_translate("MainWindow", "Placeholder 1"))
        self.CB_32.setText(_translate("MainWindow", "Placeholder 2"))
        self.CB_33.setText(_translate("MainWindow", "Placeholder 3"))
        self.CB_34.setText(_translate("MainWindow", "Placeholder 4"))
        self.CB_35.setText(_translate("MainWindow", "Placeholder 5"))
        self.CB_36.setText(_translate("MainWindow", "Placeholder 6"))
        self.CB_37.setText(_translate("MainWindow", "Placeholder 7"))
        self.CB_38.setText(_translate("MainWindow", "Placeholder 8"))
        self.CB_39.setText(_translate("MainWindow", "Placeholder 9"))
        self.CB_310.setText(_translate("MainWindow", "Placeholder 10"))
        self.CB_311.setText(_translate("MainWindow", "Placeholder 11"))
        self.CB_312.setText(_translate("MainWindow", "Placeholder 12"))
        self.CB_313.setText(_translate("MainWindow", "Placeholder 13"))
        self.CB_314.setText(_translate("MainWindow", "Placeholder 14"))
        self.CB_315.setText(_translate("MainWindow", "Placeholder 15"))
        self.CB_316.setText(_translate("MainWindow", "Horizontal Scroll Bar Placeholder"))
        self.PB_Start.setText(_translate("MainWindow", "Parse"))
