import xlsxwriter
import re
import os
import sys
import glob

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from PyQt5 import QtWidgets, QtCore, QtGui

class OL():
    def __init__(self):
        self.HEADERS = ['Time (sec.)','HeatSink','AF NTC','PC NTC','Probe1 NTC', 'Probe2 NTC', 'High Pressure',
                        'Low Pressure','V','SW version (Release.Version.Revision)','Build date']

    def parse(self, Myfiles, checkboxes):
        unformatted_files = set()

        for myfile in Myfiles:
            filename = os.path.splitext(myfile)[0]+'.xlsx'
            workbook = xlsxwriter.Workbook(filename)
            worksheet = workbook.add_worksheet('Data')
            worksheet.freeze_panes(1, 0)

            f = open(myfile, encoding="utf8", errors="ignore")
            data = f.read()
            
            pattern = r'(\?KN1\n)'
            pattern1 = r'(\n\[[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]) (2[0-3]|[01][0-9]):[0-5][0-9]:[0-5][0-9].[0-9]{3}\] )'
            pattern2 = r'(\n\?KN2\n)'
            pattern3 = r'(\n\?KN3\n)'
            pattern4 = r'(\n\?KN4\n)'
            pattern5 = r'(\n\?KN5\n)'
            pattern6 = r'(\n\?SW2\n)'
            pattern7 = r'(\n\?SW1\n)'
            pattern8 = r'(\n\?WZ\n)'

            try:
                data = re.sub(pattern, '', data)
                data = re.sub(pattern1, '\n', data)
                data = re.sub(pattern2, ',', data)
                data = re.sub(pattern3, ',', data)
                data = re.sub(pattern4, ',', data)
                data = re.sub(pattern5, ',', data)
                data = re.sub(pattern6, ',', data)
                data = re.sub(pattern7, ',', data)
                data = re.sub(pattern8, ',', data)   
            except:
                pass
            
            data = data.split('\n')
            data.remove(data[0])
            data.remove(data[0])
            data.remove(data[len(data)-1])
            data.remove(data[len(data)-1])
            data.remove(data[len(data)-1])
            
            # Rearrange if there's a timestamp
            pattern = r'(\[[0-9]{4}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1]) (2[0-3]|[01][0-9]):[0-5][0-9]:[0-5][0-9].[0-9]{3}\])'
            match = re.search(pattern,data[0])
            
            if match:
                for row in range(len(data)):
                    r = data[row].split(' ')
                    
                    if len(r) == 6:
                        r = r[2] + ' ' + r[3] + ' ' + r[4] + ',' + r[0] + ' ' + r[1]
                        data[row] = r

            # Header format
            header_format = workbook.add_format()
            header_format.set_align('center')
            header_format.set_bold()
            header_format.set_text_wrap()
            header_format.set_align('vcenter')

            # Cell format
            cell_format = workbook.add_format()
            cell_format.set_align('center')

            for index, i in enumerate(self.HEADERS):
                worksheet.write(0, index, i,header_format)

            # Convert serial data
            for row in range (0,len(data)):
                cell = data[row].split(',')

                for col in range (0,len(cell)):

                    try:
                        worksheet.write(row+1, col+len(self.HEADERS)+1, cell[col],cell_format)
                        if col<5:
                            convert_cell = int(cell[col][5:],16)/10
                        elif col>=5 and col<7:
                            convert_cell = int(cell[col][4:])
                        elif col == 7:
                            convert_cell = ''

                        #match SW version BDP                        
                        x = re.match(r'(\$WZ)(..)(..)(..)(\w+........)',cell[col])

                        if x:
                            SW_version = x.group(2)+'.'+ x.group(3)+'.'+x.group(4)
                            worksheet.write(row+1, col+2, SW_version,cell_format)
                            worksheet.write(row+1, col+3, x.group(5),cell_format)   
                        else:
                            pass
                        
                        #time
                        worksheet.write(row+1, 0, row+1,cell_format)
                        #Columns
                        if col < 8:
                            worksheet.write(row+1, col+1, convert_cell,cell_format)

                    except:
                        unformatted_files.add(myfile)
                        continue
            
            # Graphs
            worksheet = workbook.add_worksheet('Graph')
            finalRow = len(data) - 1
            chart = self.excelGraph(workbook, finalRow, checkboxes)

            while True:
                try:
                    worksheet.insert_chart('A1', chart)
                    workbook.close()
                except xlsxwriter.exceptions.FileCreateError as e:
                    # For Python 2 use raw_input() instead of input().
                    decision = input("Exception caught in workbook.close(): %s\n"
                                        "Please close the file if it is open in Excel.\n"
                                        "Try to write file again? [Y/n]: " % e)
                    if decision != 'n':
                        continue
                break
            
        return unformatted_files

    def excelGraph(self, workbook, finalRow, checkboxes):
        
        try:
            chart = workbook.add_chart({'type': 'line'})
            if 'Heatsink (KN1)' in checkboxes:
                chart.add_series({
                'name' : 'HeatSink',
                'categories': ['Data', 1, 0, finalRow, 0], 
                'values': ['Data', 1, 1, finalRow, 1], 
                })
            if 'AF NTC (KN2)' in checkboxes:
                chart.add_series({
                'name' : 'AF NTC' ,
                'categories': ['Data', 1, 0, finalRow, 0], 
                'values': ['Data', 1, 2, finalRow, 2], 
                })
            if 'PC NTC (KN3)' in checkboxes:    
                chart.add_series({
                'name' : 'PC NTC',
                'categories': ['Data', 1, 0, finalRow, 0], 
                'values': ['Data', 1, 3, finalRow, 3], 
                })
            if 'Probe1 NTC (KN4)' in checkboxes: 
                chart.add_series({
                'name' : 'Probe1 NTC',
                'categories': ['Data', 1, 0, finalRow, 0], 
                'values': ['Data', 1, 4, finalRow, 4], 
                })
            if 'Probe2 NTC (KN5)' in checkboxes: 
                chart.add_series({
                'name' : 'Probe2 NTC',
                'categories': ['Data', 1, 0, finalRow, 0], 
                'values': ['Data', 1, 5, finalRow, 5], 
                })
                
            if 'Low Pressure Switch (SW1)' in checkboxes or 'High Pressure Switch (SW2)' in checkboxes:
                chart.set_y2_axis({'name' : ' ', 'interval_unit' : 0.2})

            if 'Low Pressure Switch (SW1)' in checkboxes:
                chart.add_series({
                'name' : 'High Prs Switch',
                'categories': ['Data', 1, 0, finalRow, 0], 
                'values': ['Data', 1, 6, finalRow, 6], 
                'y2_axis' : 1,
                })
                
            if 'High Pressure Switch (SW2)' in checkboxes:
                chart.add_series({
                'name' : 'Low Prs Switch',
                'categories': ['Data', 1, 0, finalRow, 0], 
                'values': ['Data', 1, 7, finalRow, 7], 
                'y2_axis' : 1,
                })
            
        except:
            pass

        # Configure the chart axes.
        chart.set_y_axis({'name' : 'Temperature (C)', 'interval_unit' : 50})
        chart.set_x_axis({'name': 'Time (s)', 'interval_unit': 1000})
        chart.set_size({'width': 750, 'height' : 500})

        return chart

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MplCanvas, self).__init__(self.fig)

class GraphWindow(QtWidgets.QWidget):
    def __init__(self, data, path, checkboxes):
        super().__init__()
        self.resize(750,500)
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setObjectName("GraphWindow")

        sc = self.graphOL(data,path, checkboxes)
        layout = QtWidgets.QVBoxLayout()
        toolbar = NavigationToolbar(sc, self)
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        self.setLayout(layout)
        self.retranslateUi()

    def graphOL(self,data,path, checkboxes):
        sc = MplCanvas(self, width=5, height=4, dpi=100)

        try:
            time = data['Time (sec.)'][1:]
            heatsink = data['HeatSink'][1:]
            af_ntc = data['AF NTC'][1:]
            pc_ntc = data['PC NTC'][1:]
            probe1_ntc = data['Probe1 NTC'][1:]
            probe2_ntc = data['Probe2 NTC'][1:]
            high_pressure = data['High Pressure'][1:]
            low_pressure = data['Low Pressure'][1:]
            SW_verision = data['SW version (Release.Version.Revision)'][1]
            title = str(path).split('/')[-1] + ' - SWV: ' + str(SW_verision)
            
            sc.fig.suptitle(title)
            plot1 = sc.fig.add_subplot(111, xlabel = 'Time (s)', ylabel = 'Temperature (C)')
            plot1, lines = self.graphOLHelper(checkboxes, plot1, time, heatsink, af_ntc, pc_ntc, probe1_ntc, probe2_ntc, high_pressure, low_pressure)
            labels = [l.get_label() for l in lines]
            box = plot1.get_position()
            plot1.set_position([box.x0, box.y0, box.width * 0.8, box.height])
            plot1.legend(lines, labels, loc='center left', bbox_to_anchor=(1.05, 0.5))
            
        except:
            pass

        return sc
    
    def graphOLHelper(self,checkboxes, plot1, time, heatsink, af_ntc, pc_ntc, probe1_ntc, probe2_ntc, high_pressure, low_pressure):
        lines = []

        if 'Heatsink (KN1)' in checkboxes:
            line1, = plot1.plot(time, heatsink, label = 'HeatSink')
            lines.append(line1)
        if 'AF NTC (KN2)' in checkboxes:
            line2, = plot1.plot(time, af_ntc, label = 'AF NTC')
            lines.append(line2)
        if 'PC NTC (KN3)' in checkboxes:    
            line3, = plot1.plot(time, pc_ntc, label = 'PC NTC')
            lines.append(line3)
        if 'Probe1 NTC (KN4)' in checkboxes: 
            line4, = plot1.plot(time, probe1_ntc, label = 'Probe1 NTC')
            lines.append(line4)
        if 'Probe2 NTC (KN5)' in checkboxes: 
            line5, = plot1.plot(time, probe2_ntc, label = 'Probe2 NTC')
            lines.append(line5)
            
        if 'Low Pressure Switch (SW1)' in checkboxes or 'High Pressure Switch (SW2)' in checkboxes:
            secax = plot1.twinx()

        if 'Low Pressure Switch (SW1)' in checkboxes:
            line7, = secax.plot(time, low_pressure, label = 'Low Prs Switch')
            lines.append(line7)
            
        if 'High Pressure Switch (SW2)' in checkboxes:
            line6, = secax.plot(time, high_pressure, label = 'High Prs Switch')
            lines.append(line6)
            
        return plot1, lines

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("GraphWindow", "Graphs"))

    

