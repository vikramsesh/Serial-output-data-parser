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
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
import BDP_Parse

count = 0
displayname = ""

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
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

    def clearText(self):
        self.ui.Text_drop.clear()
        self.ui.Text_drop.addItem(QtWidgets.QListWidgetItem())
        self.ui.Text_drop.item(0).setText("Drop Files Here:")
        font = QtGui.QFont()
        font.setPointSize(16)
        self.ui.Text_drop.item(0).setFont(font)

        count = 0

    def addFiles(self):
        files = fileopenbox(multiple=True)

        for file in files:
            print(file)
        
    
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
