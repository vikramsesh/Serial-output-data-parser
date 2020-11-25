#!/usr/bin/env python3

"""
BDP Parser Application

Vikram Seshadri
November 11, 2020

"""

import sys
import os
import logging
import re
from easygui import fileopenbox
import xlsxwriter

# GUI
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt, QObject, QRunnable, pyqtSignal
from PyQt5.QtWidgets import QMessageBox

# FILES
import BDP_Parse
import CFP_P2_parse

count = 0
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
        result = self.fn(*self.args,**self.kwargs)
        self.signals.result.emit(result)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        self.threadpool = QtCore.QThreadPool()
        self.do_init = QtCore.QEvent.registerEventType()
        QtWidgets.QMainWindow.__init__(self)
        super(MainWindow, self).__init__()
        self.ui = BDP_Parse.Ui_MainWindow().setupUi(self)

        # Quit button and shortcut
        quit_action = QtWidgets.QAction('Quit', self)
        quit_action.setShortcuts(['Ctrl+Q', 'Ctrl+W'])
        quit_action.triggered.connect(QtWidgets.qApp.closeAllWindows)
        self.addAction(quit_action)
        self.ui.PB_Quit.clicked.connect(QtWidgets.qApp.closeAllWindows)
        
        self.ui.PB_Clear.clicked.connect(self.clearText)
##      self.PB_Start.clicked.connect(self.printText())
        self.ui.PB_File.clicked.connect(self.addFiles)
        self.ui.PB_Start.clicked.connect(self.parse)

    def clearText(self):
        self.ui.PB_Start.setEnabled(True)
        self.ui.PB_Start.setStyleSheet("background-color: rgba(75, 178, 249, 64);\n"
        "border-style:outset;\n"
        "color: rgb(255, 255, 255);\n"
        "border-radius:10px;\n"
        "padding:10px;")
        self.ui.Text_drop.links = []
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


    def addFiles(self):
        files = fileopenbox(multiple=True)
        if files != None:
            for file in files:
                self.ui.Text_drop.addItem(file)
    
    def notifications(self,unformatted_files):
        for file in self.ui.Text_drop.links:
            item = QtWidgets.QListWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(10)
            item.setFont(font)
            if file not in unformatted_files:
                item.setText(str(file.split('/')[-1]) + (' - Complete'))
                item.setForeground(Qt.green)
                self.ui.Text_status.addItem(item)
            else:
                item.setText(str(file.split('/')[-1]) + (' - Error'))
                item.setForeground(Qt.red)
                self.ui.Text_status.addItem(item)
                


    def parse(self):
        selected_parser = self.ui.CB_SKUSelect.currentText()
        if self.ui.Text_drop.count() > 1:
            self.ui.PB_Start.setEnabled(False)
            self.ui.PB_Start.setStyleSheet("background-color: rgba(75, 178, 249, 32);\n"
            "border-style:outset;\n"
            "color: rgb(255, 255, 255);\n"
            "border-radius:10px;\n"
            "padding:10px;")
        
        if selected_parser == 'OLxxx':
            pass

        elif selected_parser == 'CFPxxx':
            cfp_worker = Worker(CFP_P2_parse.parse, self.ui.Text_drop.links)
            cfp_worker.signals.result.connect(self.notifications)
            self.threadpool.start(cfp_worker)
           
        else:
            pass


        
    
if __name__ == "__main__":
    import sys
    if (sys.flags.interactive != 1):
##        log_dir = os.path.abspath(os.curdir) + "/Logs"
##        if not os.path.exists(log_dir):
##            os.makedirs(log_dir)
##
##        log_file = log_dir + "/program.log"
##        i = 0
##        while os.path.exists(log_file):
##            i += 1
##            log_file = log_dir + "/program" + str(i) + ".log"
##        print("Log File:" + log_file)
##        logging.basicConfig(
##            filename=log_file,
##            format='%(asctime)s %(message)s',
##            level=logging.DEBUG)

        app = QtWidgets.QApplication(sys.argv)
        app.processEvents()
        program = MainWindow()
        program.show()
        app.exec_()
