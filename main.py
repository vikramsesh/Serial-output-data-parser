#!/usr/bin/env python3

"""
BDP Parser Application

Vikram Seshadri
November 11, 2020

"""

import os
from easygui import fileopenbox

# PLOTTING
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import pandas as pd

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

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MplCanvas, self).__init__(self.fig)

class GraphWindow(QtWidgets.QWidget):
    def __init__(self, data, SKU):
        super().__init__()
        self.setFixedSize(600,600)
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setObjectName("GraphWindow")

        if SKU == "OLxxx":
            sc = self.graphOL(data)
        else:
            sc = self.graphCFP(data)
        
        layout = QtWidgets.QVBoxLayout()
        toolbar = NavigationToolbar(sc, self)

        layout.addWidget(toolbar)
        layout.addWidget(sc)
        self.setLayout(layout)
        
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("GraphWindow", "Graphs"))

    def graphOL(self,data):
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        time = data['Time (sec.)'][1:]
        heatsink = data['HeatSink'][1:]
        af_ntc = data['AF NTC'][1:]
        pc_ntc = data['PC NTC'][1:]
        probe1_ntc = data['Probe1 NTC'][1:]
        probe2_ntc = data['Probe2 NTC'][1:]
        high_pressure = data['High Pressure'][1:]
        low_pressure = data['Low Pressure'][1:]
        v = data['V'][1:]

        try:
            plot1 = sc.fig.add_subplot(111)
            plot1.plot(time, heatsink)
            plot1.plot(time, af_ntc)
            plot1.plot(time, pc_ntc)
            plot1.plot(time, probe1_ntc)
            plot1.plot(time, probe2_ntc)
            plot1.plot(time, high_pressure)
            plot1.plot(time, low_pressure)
            plot1.plot(time, v)
        
        except:
            pass

        return sc

    def graphCFP(self,data):
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        time = data['Time'][1:]
        outlet_temp = data['Outlet Temp'][1:]
        print(outlet_temp)
        boiler_temp = data['Boiler Temp'][1:]
        warm_plate_temp = data['Warm Plate Temp'][1:]
        pump_pwm = data['Pump PWM'][1:]
        recipe_block = data['Recipe Block'][1:]
        flow_rate = data['Flow rate'][1:]
        boiler_on = data['Boiler On/Off'][1:]
        ptc_on = data['PTC On/Off'][1:]
        current_block_volume = data['Current Block Volume'][1:]
        current_total_volume = data['Current Total Volume'][1:]
        recipe_total_volume = data['Recipe Total Volume'][1:]  

        try:
            plot1 = sc.fig.add_subplot(311)
            plot1.plot(time, outlet_temp)
            plot1.plot(time, boiler_temp)
            plot1.plot(time, warm_plate_temp)
            plot1.plot(time, pump_pwm)
            plot1.plot(time, recipe_block)
            plot1.plot(time, flow_rate)

            plot2 = sc.fig.add_subplot(312)
            plot2.plot(time, boiler_on)
            plot2.plot(time, ptc_on)
            plot2.plot(time, recipe_block)

            plot3 = sc.fig.add_subplot(313)
            plot3.plot(time, current_block_volume)
            plot3.plot(time, current_total_volume)
            plot3.plot(time, recipe_total_volume)
        
        except:
            pass

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        return sc
        

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
        parse_action.triggered.connect(self.parse)
        self.addAction(parse_action)
        self.ui.PB_Parse.clicked.connect(self.parse)

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
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ui.Text_drop.item(0).setFont(font)

        self.ui.Text_status.clear()
        self.ui.Text_status.addItem(QtWidgets.QListWidgetItem())
        self.ui.Text_status.item(0).setText("Status:")
        self.ui.Text_status.item(0).setFont(font)
        self.ui.PB_Parse.setEnabled(True)
        self.ui.PB_Parse.setStyleSheet("background-color: #673AB7;"
                                       "border-style:outset;"
                                       "color: #D9D9D9;"
                                       "border-radius:10px;"
                                       "height:30px;"
                                       "padding-top: 10px;"
                                       "padding-bottom: 10px;"
                                       "padding-left: 10px;"
                                       "padding-right: 10px;"
                                       )

    def addFiles(self):
        files = fileopenbox(multiple=True)
        if files is not None:
            for file in files:
                self.ui.Text_drop.addItem(file)
    
    def noFilesAdded(self):
        error = QMessageBox()
        error.setText("Error! No files available to parse!")
        error.setIcon(QMessageBox.Critical)
        error.exec()

    def notifications(self, unformatted_files):
        self.ui.CB_SKUSelect.setEnabled(True)
        self.fileStatus(unformatted_files)
        self.graphs()
    
    def graphs(self):
        for path in self.ui.Text_drop.links:
            path = os.path.splitext(path)[0]+'.xlsx'
            data = pd.read_excel(path)
            graphWindow = GraphWindow(data, self.ui.CB_SKUSelect.current)
            self.graphWindows.append(graphWindow)
            graphWindow.show()
            
    def fileStatus(self, unformatted_files):
        for file in self.ui.Text_drop.links:
            item = QtWidgets.QListWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(10)
            item.setFont(font)
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


if __name__ == "__main__":
    import sys

    if sys.flags.interactive != 1:
        app = QtWidgets.QApplication(sys.argv)
        app.processEvents()
        program = MainWindow()
        program.show()
        app.exec_()
