import os
import sys
import xlsxwriter
import re
import glob

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from PyQt5 import QtWidgets, QtCore, QtGui

HEADERS = ['Time','Outlet Temp', 'Boiler Temp', 'Warm Plate Temp', 'Max Temp', 'Calibrated Offset Temp', 'Pump PWM', 'Boiler On/Off', 'PTC On/Off',
           'Flow rate', 'Current Block Volume', 'Current Total Volume', 'Clean Count', 'Recipe Size', 'Recipe Brew',
           'Recipe Block', 'Recipe Total Volume', 'Recipe Time']
     
SUB_HEADERS = ['sec.','degC','degC','degC','degC','degC']

SUMMARY_HEADERS = ['Max. Outlet Temp', 'Max. Boiler Temp', 'Max. Warm Plate Temp',
                   'Max. Flowrate']

SUMMARY_SUB_HEADERS = ['degC','degC','degC','ml/sec.']

def closeworkbook(workbook):
    while True:
        try:
            workbook.close()
            
        except xlsxwriter.exceptions.FileCreateError as e:
            # For Python 3 use input() instead of raw_input().
            decision = input("Exception caught in workbook.close(): %s\n"
                                 "Please close the file if it is open in Excel.\n"
                                 "Try to write file again? [Y/n]: " % e)
            if decision != 'n':
                continue
        except:
            continue
        break

def parse(Myfiles):
    unformatted_files = set()
    for myfile in Myfiles:
        workbook = xlsxwriter.Workbook(os.path.splitext(myfile)[0]+'.xlsx',{'constant_memory': True})

        #RAW data
        worksheet = workbook.add_worksheet('Data')
        worksheet.freeze_panes(1, 0)
        worksheet.set_column('A:R', 8.8)

        #Summary data
    ##    summary_worksheet = workbook.add_worksheet('Summary')
    ##    summary_worksheet.freeze_panes(1, 0)
        
        f = open(myfile,encoding= 'utf-8',errors='ignore')
        try:
            data = f.read()
        except:
            continue

        entries = data.split('\n')
        entries = entries[2:-1]

        # Add formatting to highlight cells.
        header_format  = workbook.add_format()
        header_format.set_align('center')
        header_format.set_bold()
        header_format.set_text_wrap()
        header_format.set_align('vcenter')

        subheader_format  = workbook.add_format()
        subheader_format.set_align('center')
        subheader_format.set_bold()
        subheader_format.set_italic()
        subheader_format.set_text_wrap()
        subheader_format.set_align('vcenter')

        data_format  = workbook.add_format()
        data_format.set_align('vcenter')
        data_format.set_align('center')

        row_index = 0

        # Write headers
        for index, i in enumerate(HEADERS):
            worksheet.write(row_index, index, i, header_format)
        for index, i in enumerate(SUB_HEADERS):
            worksheet.write(row_index + 1, index, i, subheader_format)

    ##    for index, i in enumerate(SUMMARY_HEADERS):
    ##        summary_worksheet.write(row_index, index, i, header_format)
    ##    for index, i in enumerate(SUMMARY_SUB_HEADERS):
    ##        summary_worksheet.write(row_index + 1, index, i, subheader_format)
            
        row_index = 1

        try:
            for i in range(0, len(entries)):
                row_index += 1
                data = entries[i].split(' ')
                
                worksheet.write(row_index,0, i+1 ,data_format) 
                for k in range(0, len(data)):
                    try:
                        data[k] = float(data[k])
                        if k<=5:
                            data[k] = float(data[k])/10
                        
                        worksheet.write(row_index,k+1, data[k],data_format)
                    except:
                        txt = data[k]
                        x = re.search(r"(B)(.)", txt)
                        y = re.search(r"(P)(.)", txt)
                        try: 
                            if x:
                                data[k] = x.group(2)
                                data[k] = float(data[k])

                            if y:
                                data[k] = y.group(2)
                                data[k] = float(data[k])

                            if x or y:
                                worksheet.write(row_index, k+1, data[k],data_format)
                            else:
                                unformatted_files.add(myfile)
                        except:
                            pass

            worksheet = workbook.add_worksheet('Graph')
            finalRow = len(entries) - 1
            chart1, chart2, chart3, chart4 = excelGraph(workbook, finalRow)
            worksheet.insert_chart('A1', chart1)
            worksheet.insert_chart('A21', chart2)
            worksheet.insert_chart('N1', chart3)
            worksheet.insert_chart('N21', chart4)
            

            closeworkbook(workbook)
        
        except KeyboardInterrupt as e:
            closeworkbook(workbook)
            
        except:
            continue
    return unformatted_files

def excelGraph(workbook, finalRow):
    chart1 = workbook.add_chart({'type': 'line'})
    chart2 = workbook.add_chart({'type': 'line'})
    chart3 = workbook.add_chart({'type': 'line'})
    chart4 = workbook.add_chart({'type': 'line'})
    try:
        chart1.add_series({
        'name' : 'Outlet Temp',
        'categories': ['Data', 1, 0, finalRow, 0], 
        'values': ['Data', 1, 1, finalRow, 1], 
        })
        chart1.add_series({
        'name' : 'Boiler Temp' ,
        'categories': ['Data', 1, 0, finalRow, 0], 
        'values': ['Data', 1, 2, finalRow, 2], 
        })
        chart1.add_series({
        'name' : 'Warmplate Temp' ,
        'categories': ['Data', 1, 0, finalRow, 0], 
        'values': ['Data', 1, 3, finalRow, 3], 
        })

        chart2.add_series({
        'name' : 'Boiler ON',
        'categories': ['Data', 1, 0, finalRow, 0], 
        'values': ['Data', 1, 7, finalRow, 7], 
        })
        chart2.add_series({
        'name' : 'PTC ON' ,
        'categories': ['Data', 1, 0, finalRow, 0], 
        'values': ['Data', 1, 8, finalRow, 8], 
        })
        chart2.add_series({
        'name' : 'Recipe Block' ,
        'categories': ['Data', 1, 0, finalRow, 0], 
        'values': ['Data', 1, 15, finalRow, 15], 
        })

        chart3.add_series({
        'name' : 'Current Block Volume',
        'categories': ['Data', 1, 0, finalRow, 0], 
        'values': ['Data', 1, 10, finalRow, 10], 
        })
        chart3.add_series({
        'name' : 'Current Total Volume' ,
        'categories': ['Data', 1, 0, finalRow, 0], 
        'values': ['Data', 1, 11, finalRow, 11], 
        })
        chart3.add_series({
        'name' : 'Recipe Total Block' ,
        'categories': ['Data', 1, 0, finalRow, 0], 
        'values': ['Data', 1, 16, finalRow, 16], 
        })

        chart4.add_series({
        'name' : 'Pump PWM',
        'categories': ['Data', 1, 0, finalRow, 0], 
        'values': ['Data', 1, 6, finalRow, 6], 
        })
        chart4.add_series({
        'name' : 'Flow Rate' ,
        'categories': ['Data', 1, 0, finalRow, 0], 
        'values': ['Data', 1, 9, finalRow, 9], 
        })

    except:
        pass

    # Configure the chart axes.
    chart1.set_y_axis({'name' : 'Temperature (C)', 'interval_unit' : 50})
    chart1.set_x_axis({'name': 'Time (s)', 'interval_unit': 10000})
    chart1.set_size({'width': 750, 'height' : 400})

    chart2.set_y_axis({'name' : ' ', 'interval_unit' : 2})
    chart2.set_x_axis({'name': 'Time (s)', 'interval_unit': 10000})
    chart2.set_size({'width': 750, 'height' : 400})

    chart3.set_y_axis({'name' : 'Volume (mL)', 'interval_unit' : 500})
    chart3.set_x_axis({'name': 'Time (s)', 'interval_unit': 10000})
    chart3.set_size({'width': 750, 'height' : 400})

    chart4.set_y_axis({'name' : 'Pump Plates', 'interval_unit' : 200})
    chart4.set_x_axis({'name': 'Time (s)', 'interval_unit': 10000})
    chart4.set_size({'width': 750, 'height' : 400})
    return chart1, chart2, chart3, chart4

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MplCanvas, self).__init__(self.fig)

class GraphWindow(QtWidgets.QWidget):
    def __init__(self, data, path):
        super().__init__()
        self.resize(600,600)
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.setObjectName("GraphWindow")

        sc = self.graphCFP(data,path)
        layout = QtWidgets.QVBoxLayout()
        toolbar = NavigationToolbar(sc, self)
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        self.setLayout(layout)
        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("GraphWindow", "Graphs"))

    def graphCFP(self,data, path):
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        try:
            time = data['Time'][1:]
            outlet_temp = data['Outlet Temp'][1:]
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

            title = str(path).split('/')[-1]
            sc.fig.suptitle(title)
            plot1 = sc.fig.add_subplot(411, ylabel = 'Temperature (C)')
            line1, = plot1.plot(time, outlet_temp, label = 'Outlet Temp')
            line2, = plot1.plot(time, boiler_temp, label = 'Boiler Temp')
            line3, = plot1.plot(time, warm_plate_temp, label = 'Warmplate Temp')
            box = plot1.get_position()
            plot1.set_position([box.x0, box.y0, box.width * 0.8, box.height])
            plot1.legend(loc='center left', bbox_to_anchor=(1, 0.5))

            plot2 = sc.fig.add_subplot(412)
            line1, = plot2.plot(time, boiler_on, label = 'Boiler ON')
            line2, = plot2.plot(time, ptc_on, label = 'PTC ON')
            line3, = plot2.plot(time, recipe_block, label = 'Recipe Block')
            box = plot2.get_position()
            plot2.set_position([box.x0, box.y0, box.width * 0.8, box.height])
            plot2.legend(loc='center left', bbox_to_anchor=(1, 0.5))

            plot3 = sc.fig.add_subplot(413,  ylabel = 'Volume (mL)')
            line1, = plot3.plot(time, current_block_volume, label = 'Current Block Volume')
            line2, = plot3.plot(time, current_total_volume, label = 'Current Total Volume')
            line3, = plot3.plot(time, recipe_total_volume, label = 'Recipe Total Volume')
            box = plot3.get_position()
            plot3.set_position([box.x0, box.y0, box.width * 0.8, box.height])
            plot3.legend(loc='center left', bbox_to_anchor=(1, 0.5))

            plot4 = sc.fig.add_subplot(414, xlabel = 'Time (s)', ylabel = 'Pump Plates')
            line1, = plot4.plot(time, pump_pwm, label = 'Pump PWM')
            line2, = plot4.plot(time, flow_rate, label = 'Flow Rate')
            box = plot4.get_position()
            plot4.set_position([box.x0, box.y0, box.width * 0.8, box.height])
            plot4.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        
        except:
            pass

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        return sc
