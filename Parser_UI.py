# -*- coding: utf-8 -*-

# GUI for parser application

from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Styling
section_style = (
    "background-color: #28293D;"  # Style 1
    # "background-color: #555770;"  # Style 2
    # "background-color: #8F90A6;"  # Style 3
    "selection-background-color: #03DAC6;"
    "border-style:outset;"
    "border-radius:10px;"
    "border: 1px solid;"
    "border-color: #3568D4;"
    "color: #d9d9d9;"
    "padding:10px;"
)

scrollbar_horizontal = (
    "QScrollBar:horizontal"
    "{"
    "height:10px;"
    "padding:0px;"
    "border:solid;"
    "border-radius: 5px;"
    "background-color: solid;"
    "border-radius:5px;"
    "}"
    "QScrollBar::handle:horizontal"
    "{"
    "background-color:#3568D4;"
    "border-radius:0px;"
    "height:15px"
    "}"
)

scrollbar_vertical = (
    "QScrollBar:vertical"
    "{"
    "width:10px;"
    "padding:0px;"
    "background-color: solid;"
    "border-radius:5px;"
    "}"
    "QScrollBar::handle:vertical"
    "{"
    "background-color:#3568D4;"
    "border-radius:0px;"
    "width:15px"
    "}"
)

# Fonts
minifont = QFont("Calibri", 9, QFont.Normal)
textfont = QFont("Calibri", 11, QFont.Normal)
headerfont = QFont("Calibri", 12, QFont.Medium)
buttonfont = QFont("Calibri", 12, QFont.Black)


class ComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.previous = ""
        self.current = "OLxxx"


class ListBoxWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.links = set()
        self.setAcceptDrops(True)

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
            for url in event.mimeData().urls():
                item = QtWidgets.QListWidgetItem()
                font = QtGui.QFont()
                font.setPointSize(10)
                item.setFont(font)
                if (url.isLocalFile()) and (str(url.toLocalFile()) not in self.links):
                    self.links.add(str(url.toLocalFile()))
                    item.setText(str(url.toLocalFile()))
                    self.addItem(item)
        else:
            event.ignore()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(700, 800)
        MainWindow.setMinimumSize(600, 700)
        MainWindow.setAcceptDrops(True)
        MainWindow.setStyleSheet(
            "background-color: #1C1C28;"  # style 1
            # "background-color: #28293D;"  # style 2
        )
        MainWindow.setWindowIcon(QtGui.QIcon("icon/binary-file.png"))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setVerticalSpacing(10)

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setStyleSheet(section_style)

        item = QtWidgets.QListWidgetItem()
        item.setFont(textfont)
        self.listWidget.addItem(item)
        self.listWidget.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.listWidget.itemPressed["QListWidgetItem*"].connect(
            lambda item: item.setCheckState(
                Qt.Checked
                if item.checkState() == Qt.Unchecked
                else Qt.Unchecked
            )
        )
        self.listWidget.setSpacing(8)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        item.setFont(textfont)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        item.setFont(textfont)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        item.setFont(textfont)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        item.setFont(textfont)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        item.setFont(textfont)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        item.setFont(textfont)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        item.setFont(textfont)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        item.setFont(textfont)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        item.setFont(textfont)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        item.setFont(textfont)
        self.listWidget.addItem(item)

        self.listWidget.horizontalScrollBar().setStyleSheet(scrollbar_horizontal)
        self.listWidget.verticalScrollBar().setStyleSheet(scrollbar_vertical)

        self.listWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.listWidget.setObjectName("listwidget")

        self.gridLayout.addWidget(self.listWidget, 2, 4, 4, 3)

        # Drop down combo button
        self.drop_down = QtWidgets.QListView(self.centralwidget)
        self.drop_down.setStyleSheet(section_style)
        self.CB_SKUSelect = ComboBox(self.centralwidget)
        self.CB_SKUSelect.setView(self.drop_down)

        self.CB_SKUSelect.setFont(headerfont)
        self.drop_down.setFont(headerfont)
        self.CB_SKUSelect.setStyleSheet("QComboBox"
                                        "{"
                                        "color: #D9D9D9;"
                                        "border-radius:5px;"
                                        "border: 1px solid;"
                                        "border-color: #3568D4;"
                                        "padding-left:10px;"
                                        "background-color: #28293D;"
                                        "}"
                                        "QComboBox::drop-down"
                                        "{"
                                        "border-width:10px;"
                                        "}"
                                        "QComboBox::focus"
                                        "{"
                                        "}"
                                        "QComboBox::down-arrow"
                                        "{"
                                        "image: url(icon/drop-down.png);"
                                        "border : 0px solid;"
                                        "border-radius:0px;"
                                        "border-color: #1E1E1E;"
                                        "width:20px;"
                                        "height:25px;"
                                        "}"
                                        )
        self.CB_SKUSelect.setObjectName("CB_SKUSelect")
        self.CB_SKUSelect.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.CB_SKUSelect.addItem("")
        self.CB_SKUSelect.addItem("")
        self.CB_SKUSelect.addItem("")
        self.CB_SKUSelect.setFixedHeight(60)
        self.gridLayout.addWidget(self.CB_SKUSelect, 1, 1, 1, 3)

        # Push Button
        self.PB_File = QtWidgets.QPushButton(self.centralwidget)
        self.PB_File.setToolTip('Add files')
        QToolTip.setFont(headerfont)

        self.PB_File.setStyleSheet(
            # "background-color: #673AB7;"  # style 1
            "background-color: #3568D4;"  # style 2
            "border-style:outset;"
            "color: #D9D9D9;"
            "height:40px;"
            "padding-top: 10px;"
            "padding-bottom: 10px;"
            "padding-left: 10px;"
            "padding-right: 10px;"
            "border-radius:10px;")
        self.PB_File.setObjectName("PB_File")
        self.PB_File.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.PB_File.setIcon(QIcon("icon/file.png"))
        self.PB_File.setIconSize(QSize(50, 35))

        self.gridLayout.addWidget(self.PB_File, 7, 1, 1, 1)

        self.PB_Parse = QtWidgets.QPushButton(self.centralwidget)
        self.PB_Parse.setStyleSheet(
            # "background-color: #673AB7;"  # style 1
            "background-color: #3568D4;"  # style 2
            "border-style:outset;"
            "color: #D9D9D9;"
            "border-radius:10px;"
            "height:40px;"
            "padding-top: 10px;"
            "padding-bottom: 10px;"
            "padding-left: 10px;"
            "padding-right: 10px;"
        )

        self.PB_Parse.setIcon(QIcon("icon/parse.png"))
        self.PB_Parse.setIconSize(QSize(50, 35))
        self.PB_Parse.setToolTip('Parse')
        QToolTip.setFont(headerfont)

        self.PB_Parse.setObjectName("PB_Parse")
        self.PB_Parse.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.gridLayout.addWidget(self.PB_Parse, 7, 2, 1, 2)

        self.PB_Clear = QtWidgets.QPushButton(self.centralwidget)
        self.PB_Clear.setStyleSheet(
            # "background-color: #673AB7;"  # style 1
            "background-color: #3568D4;"  # style 2
            "border-style:outset;"
            "color: #D9D9D9;"
            "border-radius:10px;"
            "height:40px;"
            "padding-top: 10px;"
            "padding-bottom: 10px;"
            "padding-left: 10px;"
            "padding-right: 10px;"
        )

        self.PB_Clear.setIcon(QIcon("icon/clear.png"))
        self.PB_Clear.setIconSize(QSize(50, 40))
        self.PB_Clear.setToolTip('Clear')
        QToolTip.setFont(headerfont)

        self.PB_Clear.setObjectName("PB_Clear")
        self.PB_Clear.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.gridLayout.addWidget(self.PB_Clear, 7, 4, 1, 2)

        self.PB_Quit = QtWidgets.QPushButton(self.centralwidget)
        self.PB_Quit.setStyleSheet(
            # "background-color: #D0112B;"  # style1
            "background-color: #FF3B3B;"  # style2
            "border-style:outset;"
            "color: #D9D9D9;"
            "height:40px;"
            "padding-top: 10px;"
            "padding-bottom: 10px;"
            "padding-left: 10px;"
            "padding-right: 10px;"
            "border-radius:10px;"
        )
        self.PB_Quit.setIcon(QIcon("icon/quit.png"))
        self.PB_Quit.setIconSize(QSize(50, 25))
        self.PB_Quit.setToolTip('Quit')
        QToolTip.setFont(headerfont)

        self.PB_Quit.setObjectName("PB_Quit")
        self.PB_Quit.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.gridLayout.addWidget(self.PB_Quit, 7, 6, 1, 1)

        self.Text_drop = ListBoxWidget(self.centralwidget)
        self.Text_drop.setStyleSheet(section_style)

        self.Text_drop.setObjectName("Text_drop")
        self.Text_drop.horizontalScrollBar().setStyleSheet(scrollbar_horizontal)
        self.Text_drop.verticalScrollBar().setStyleSheet(scrollbar_vertical)

        item = QtWidgets.QListWidgetItem()
        self.Text_drop.addItem(item)
        self.gridLayout.addWidget(self.Text_drop, 2, 1, 2, 3)

        self.Text_status = QtWidgets.QListWidget(self.centralwidget)
        self.Text_status.setStyleSheet(section_style)
        self.Text_status.setObjectName("Text_status")
        item = QtWidgets.QListWidgetItem()
        self.Text_status.addItem(item)
        self.gridLayout.addWidget(self.Text_status, 4, 1, 2, 3)
        self.Text_status.horizontalScrollBar().setStyleSheet(scrollbar_horizontal)
        self.Text_status.verticalScrollBar().setStyleSheet(scrollbar_vertical)

        self.info_label = QtWidgets.QLabel(self.centralwidget)
        self.info_label.setText("© Ninja Testing")
        self.info_label.setFont(minifont)
        self.info_label.setAlignment(QtCore.Qt.AlignRight)
        self.info_label.setStyleSheet("color: #d9d9d9;")
        self.gridLayout.addWidget(self.info_label, 1, 4, 1, 3)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        return self

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Data Parser"))

        item = self.listWidget.item(0)
        item.setFont(headerfont)
        item.setText("Parameters: ")
        item.setFlags(Qt.NoItemFlags)
        item = self.listWidget.item(1)
        item.setText("Power Software version (WZ)")
        item.setFlags(Qt.NoItemFlags)
        item = self.listWidget.item(2)
        item.setText("UI Software version (WU)")
        item.setFlags(Qt.NoItemFlags)
        item = self.listWidget.item(3)
        item.setText("Product Current (KH1)")
        item = self.listWidget.item(4)
        item.setText("AF NTC (KN1)")
        item = self.listWidget.item(5)
        item.setText("PC NTC (KN2)")
        item = self.listWidget.item(6)
        item.setText("Probe1 NTC (KN3)")
        item = self.listWidget.item(7)
        item.setText("Probe2 NTC (KN4)")
        item = self.listWidget.item(8)
        item.setText("Low Pressure Switch (SW1)")
        item = self.listWidget.item(9)
        item.setText("High Pressure Switch (SW2)")
        item = self.listWidget.item(10)
        item.setText("Solenoid Status (KV)")

        self.PB_File.setText(_translate("MainWindow", ""))
        self.PB_File.setFont(buttonfont)
        self.PB_Quit.setText(_translate("MainWindow", ""))
        self.PB_Quit.setFont(buttonfont)
        self.PB_Clear.setText(_translate("MainWindow", "Clear"))
        self.PB_Clear.setFont(buttonfont)
        self.PB_Parse.setText(_translate("MainWindow", " Parse"))
        self.PB_Parse.setFont(buttonfont)
        self.CB_SKUSelect.setItemText(0, _translate("MainWindow", "OLxxx"))
        self.CB_SKUSelect.setItemText(1, _translate("MainWindow", "CFPxxx"))
        self.CB_SKUSelect.setItemText(2, _translate("MainWindow", "CP300"))
        __sortingEnabled = self.Text_drop.isSortingEnabled()
        self.Text_drop.setSortingEnabled(False)

        item = self.Text_drop.item(0)
        item.setFont(headerfont)
        item.setText(_translate("MainWindow", "Drop Files Here:"))
        self.Text_drop.setSortingEnabled(__sortingEnabled)

        self.Text_status.setSortingEnabled(False)
        item = self.Text_status.item(0)
        item.setFont(headerfont)
        item.setText(_translate("MainWindow", "Status:"))
        self.Text_status.setSortingEnabled(__sortingEnabled)
