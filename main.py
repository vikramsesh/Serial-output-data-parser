#!/usr/bin/env python3

"""
BDP Parser Application

Vikram Seshadri
November 11, 2020

"""

from easygui import fileopenbox

# GUI
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import QMessageBox

# FILES
import Parser_UI
import CFP_P2_parse
import OL600_BDP_parse

displayname = ""


class WorkerSignals(QObject):
    result = pyqtSignal(object)


class Worker(QtCore.QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        result = self.fn(*self.args, **self.kwargs)
        self.signals.result.emit(result)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        self.threadpool = QtCore.QThreadPool()
        self.do_init = QtCore.QEvent.registerEventType()
        QtWidgets.QMainWindow.__init__(self)
        super(MainWindow, self).__init__()
        self.ui = Parser_UI.Ui_MainWindow().setupUi(self)

        # Quit button and shortcut
        quit_action = QtWidgets.QAction('Quit', self)
        quit_action.setShortcuts(['Ctrl+Q', 'Ctrl+W'])
        quit_action.triggered.connect(QtWidgets.qApp.closeAllWindows)
        self.addAction(quit_action)
        self.ui.PB_Quit.clicked.connect(QtWidgets.qApp.closeAllWindows)

        self.ui.PB_Clear.clicked.connect(self.clearText)
        self.ui.PB_File.clicked.connect(self.addFiles)
        self.ui.PB_Parse.clicked.connect(self.parse)

    def clearText(self):
        # self.ui.PB_Parse.setEnabled(True)
        # self.ui.PB_Parse.setStyleSheet("background-color: rgba(75, 178, 249, 64);\n"
        #                                "border-style:outset;\n"
        #                                "color: rgb(255, 255, 255);\n"
        #                                "border-radius:5px;\n"
        #                                "padding:10px;")

        self.ui.Text_drop.links = set()
        self.ui.Text_drop.clear()
        self.ui.Text_drop.addItem(QtWidgets.QListWidgetItem())
        self.ui.Text_drop.item(0).setText("Drop Files Here:")
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ui.Text_drop.item(0).setFont(font)

        self.ui.Text_status.clear()
        self.ui.Text_status.addItem(QtWidgets.QListWidgetItem())
        self.ui.Text_status.item(0).setText("Status:")
        self.ui.Text_status.item(0).setFont(font)
        self.ui.PB_Parse.setEnabled(True)
        self.ui.PB_Parse.setStyleSheet("background-color: #3700B3;"
                                    "border-style:outset;"
                                    "color: #FFFFFF;"
                                    "border-radius:5px;"
                                    "padding:10px;")

    def addFiles(self):
        files = fileopenbox(multiple=True)
        if files is not None:
            for file in files:
                self.ui.Text_drop.addItem(file)

    def notifications(self, unformatted_files):
        for file in self.ui.Text_drop.links:
            item = QtWidgets.QListWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(10)
            item.setFont(font)
            if unformatted_files != None:
                if file not in unformatted_files:
                    item.setText(str(file.split('/')[-1]) + ' - Complete')
                    item.setForeground(Qt.green)
                    self.ui.Text_status.addItem(item)
                else:
                    item.setText(str(file.split('/')[-1]) + ' - Error')
                    item.setForeground(Qt.red)
                    self.ui.Text_status.addItem(item)
    
    def noFilesAdded(self):
        error = QMessageBox()
        error.setText("Error! No files available to parse!")
        error.setIcon(QMessageBox.Critical)
        error.exec()

    def parse(self):
        selected_parser = self.ui.CB_SKUSelect.currentText()
        if self.ui.Text_drop.count() > 1:
            self.ui.PB_Parse.setEnabled(False)
            self.ui.CB_SKUSelect.setEnabled(False)
            self.ui.PB_Parse.setStyleSheet("background-color: rgba(55,0,179,128);"
                                    "border-style:outset;"
                                    "color: #FFFFFF;"
                                    "border-radius:5px;"
                                    "padding:10px;")
        else:
            self.noFilesAdded()


        if selected_parser == 'OLxxx':
            ol_worker = Worker(OL600_BDP_parse.parse, self.ui.Text_drop.links)
            ol_worker.signals.result.connect(self.notifications)
            self.threadpool.start(ol_worker)

        elif selected_parser == 'CFPxxx':
            cfp_worker = Worker(CFP_P2_parse.parse, self.ui.Text_drop.links)
            cfp_worker.signals.result.connect(self.notifications)
            self.threadpool.start(cfp_worker)


        else:
            pass


if __name__ == "__main__":
    import sys

    if sys.flags.interactive != 1:
        app = QtWidgets.QApplication(sys.argv)
        app.processEvents()
        program = MainWindow()
        program.show()
        app.exec_()
