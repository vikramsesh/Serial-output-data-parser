import xlsxwriter
import pandas as pd
import re
import os
import sys
import openpyxl
import matplotlib.pyplot as plt

HEADERS = ['Time (sec.)','HeatSink','AF NTC','PC NTC','Probe1 NTC',
           'Probe2 NTC', 'High Pressure','Low Pressure','SW version (Release.Version.Revision)','Build date']

path = "C:\\Users\\vseshadri\\Desktop\\Chili testing_SW1.33\\"
filename = "Chilli3_126V_Serial.txt"
file = path + filename

f = open(file)
data = f.read()

pattern = r'(\?KN1\n)'
pattern1 = r'(\n\?KN2\n)'
pattern2 = r'(\n\?KN3\n)'
pattern3 = r'(\n\?KN4\n)'
pattern4 = r'(\n\?KN5\n)'
pattern5 = r'(\n\?SW2\n)'
pattern6 = r'(\n\?SW1\n)'
pattern7 = r'(\n\?WZ\n)'

try:
    data = re.sub(pattern, '', data)
    data = re.sub(pattern1, ',', data)
    data = re.sub(pattern2, ',', data)
    data = re.sub(pattern3, ',', data)
    data = re.sub(pattern4, ',', data)
    data = re.sub(pattern5, ',', data)
    data = re.sub(pattern6, ',', data)
    data = re.sub(pattern7, ',', data)
except:
    pass

data = data.split('\n')
data.remove(data[0])
data.remove(data[len(data)-1])
data.remove(data[len(data)-1])

workbook = xlsxwriter.Workbook("Chilli3_126V_Serial.xlsx")
worksheet1 = workbook.add_worksheet('Data')
##worksheet2 = workbook.add_worksheet('RAW')

header_format = workbook.add_format()
header_format.set_align('center')
header_format.set_bold()
header_format.set_text_wrap()
header_format.set_align('vcenter')

cell_format = workbook.add_format()
cell_format.set_align('center')
##cell_format.set_text_wrap()

for index, i in enumerate(HEADERS):
    worksheet1.write(0, index, i,header_format)
                 
for row in range (0,len(data)):
    
    cell = data[row].split(',')
    for col in range (0,len(cell)):
        worksheet1.write(row+1, col+len(HEADERS)+1, cell[col],cell_format)
        if col<5:
            convert_cell = int(cell[col][5:],16)/10
        elif col>=5 and col<7:
            convert_cell = int(cell[col][4:])
        x = re.match(r'(\$WZ)(..)(..)(..)(\w+........)',cell[col])
        if x:
            convert_cell = x.group(2)+'.'+ x.group(3)+'.'+x.group(4)
            worksheet1.write(row+1, col+2, x.group(5),cell_format)
        else:
            pass
        worksheet1.write(row+1, 0, row+1,cell_format)
        worksheet1.write(row+1, col+1, convert_cell,cell_format)
 
workbook.close()
