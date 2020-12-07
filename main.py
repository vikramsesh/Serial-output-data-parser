#!/usr/bin/env python3

"""
BDP Parser Application

Vikram Seshadri
November 11, 2020

"""

import os
from easygui import fileopenbox
import re
import pandas as pd

# GUI
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import *

# FILES
import Parser_UI
import CFP_P2_parse
import OL600_BDP_parse

# Fonts
minifont = QFont("Calibri", 9, QFont.Normal)
textfont = QFont("Calibri", 11, QFont.Normal)
headerfont = QFont("Calibri", 12, QFont.Medium)
buttonfont = QFont("Calibri", 12, QFont.Black)


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

        # Parse button and shortcut
        parse_action = QtWidgets.QAction('Parse', self)
        parse_action.setShortcuts(['Return'])
        parse_action.triggered.connect(self.parsefn)
        self.addAction(parse_action)
        self.ui.PB_Parse.clicked.connect(self.parsefn)

        self.ui.PB_Clear.clicked.connect(self.clearText)
        self.ui.PB_File.clicked.connect(self.addFiles)

        # Combo box
        self.ui.CB_SKUSelect.currentTextChanged.connect(self.comboboxChanged)

        self.graphWindows = []

    def clearText(self):

        self.ui.Text_drop.links = set()
        self.ui.Text_drop.clear()
        self.ui.Text_drop.addItem(QtWidgets.QListWidgetItem())
        self.ui.Text_drop.item(0).setText("Drop Files Here:")
        self.ui.Text_drop.item(0).setFont(headerfont)

        self.ui.Text_status.clear()
        self.ui.Text_status.addItem(QtWidgets.QListWidgetItem())
        self.ui.Text_status.item(0).setText("Status:")
        self.ui.Text_status.item(0).setFont(headerfont)
        self.ui.PB_Parse.setEnabled(True)

    def noFilesAdded(self):
        error = QMessageBox()
        error.setText("Error! No files available to parse!")
        error.setIcon(QMessageBox.Critical)
        error.exec()
    
    def addFiles(self):
        files = fileopenbox(multiple=True)
        if files is not None:
            for file in files:
                pattern = r'(\\)'
                file = re.sub(pattern, '/', file)

                self.ui.Text_drop.addItem(file)
                self.ui.Text_drop.links.add(str(file))
                self.ui.Text_drop.setFont(textfont)

    def notifications(self, unformatted_files):
        self.ui.CB_SKUSelect.setEnabled(True)
        self.ui.PB_Parse.setEnabled(True)
        self.graphs()
        self.fileStatus(unformatted_files)
        
    def checkboxes(self):
        checkboxes = set()
        for i in range(self.ui.listWidget.count()):
            if self.ui.listWidget.item(i).checkState():
                checkboxes.add(self.ui.listWidget.item(i).text())
        return checkboxes

    def graphs(self):
        for path in self.ui.Text_drop.links:
            path = os.path.splitext(path)[0] + '.xlsx'
            data = pd.read_excel(path)
            if self.ui.CB_SKUSelect.current == "OLxxx":
                checkboxes = self.checkboxes()
                graphWindow = OL600_BDP_parse.GraphWindow(data, path, checkboxes)
            else:
                graphWindow = CFP_P2_parse.GraphWindow(data, path)

            self.graphWindows.append(graphWindow)
            graphWindow.show()

    def fileStatus(self, unformatted_files):
        for file in self.ui.Text_drop.links:
            item = QtWidgets.QListWidgetItem()
            item.setFont(textfont)
            if file not in unformatted_files:
                item.setText(str(file.split('/')[-1]) + ' - Complete')
                item.setForeground(Qt.green)
                self.ui.Text_status.addItem(item)
            else:
                item.setText(str(file.split('/')[-1]) + ' - Error')
                item.setForeground(Qt.red)
                self.ui.Text_status.addItem(item)

    def comboboxChanged(self, value):
        self.ui.CB_SKUSelect.previous = self.ui.CB_SKUSelect.current
        self.ui.CB_SKUSelect.current = value
        if (self.ui.CB_SKUSelect.previous == "OLxxx") and (
                self.ui.CB_SKUSelect.current == "CFPxxx"):
            for i in range(1, self.ui.listWidget.count()):
                self.ui.listWidget.item(i).setHidden(True)
        else:
            for i in range(1, self.ui.listWidget.count()):
                self.ui.listWidget.item(i).setHidden(False)

    def parsefn(self):
        selected_parser = self.ui.CB_SKUSelect.currentText()
        if self.ui.Text_drop.count() > 1:
            self.ui.PB_Parse.setEnabled(False)
            self.ui.CB_SKUSelect.setEnabled(False)

        else:
            QMessageBox.critical(
                None,
                "Error",
                "Error! No files available to parse!")

        if selected_parser == 'OLxxx':
            checkboxes = self.checkboxes()
            OL = OL600_BDP_parse.OL()
            OL_worker = Worker(OL.parse, self.ui.Text_drop.links, checkboxes)
            OL_worker.signals.result.connect(self.notifications)
            self.threadpool.start(OL_worker)

        elif selected_parser == 'CFPxxx':
            CFP = CFP_P2_parse.CFP()
            CFP_worker = Worker(CFP.parse, self.ui.Text_drop.links)
            CFP_worker.signals.result.connect(self.notifications)
            self.threadpool.start(CFP_worker)


if __name__ == "__main__":
    import sys

    if sys.flags.interactive != 1:
        app = QtWidgets.QApplication(sys.argv)
        app.processEvents()
        program = MainWindow()
        program.show()
        app.exec_()
