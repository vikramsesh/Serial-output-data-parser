import os
import sys
import xlsxwriter
import re

filepath = "C:\\Users\\vseshadri\\Desktop\\Pasta_126V_Serial.txt"

(head, tail) = os.path.split( filepath )

workbook = xlsxwriter.Workbook(os.path.splitext(filepath)[0]+'.xlsx')
worksheet = workbook.add_worksheet('Data')

worksheet.freeze_panes(1, 0)

f = open(filename,"r")
data = f.read()

entries = data.split('\n')
entries.remove(entries[0])

HEADERS = ['Time','Outlet Temp', 'Boiler Temp', 'Warm Plate Temp', 'Max Temp', 'Calibrated Offset Temp', 'Pump PWM', 'Boiler On/Off', 'PTC On/Off',
           'Flow rate', 'Current Block Volume', 'Current Total Volume', 'Clean Count', 'Recipe Size', 'Recipe Brew',
           'Recipe Block', 'Recipe Total Volume', 'Recipe Time']
     
SUB_HEADERS = ['sec.','degC','degC','degC','degC','degC']


##worksheet2 = workbook.add_worksheet()

# Add a bold format to use to highlight cells.
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
                if x:
                    data[k] = x.group(2)
                    data[k] = float(data[k])

                if y:
                    data[k] = y.group(2)
                    data[k] = float(data[k])
                    
                worksheet.write(row_index, k+1, data[k],data_format)
                pass
        print(data)
except:
    pass
    
while True:
    try:
        workbook.close()
    except xlsxwriter.exceptions.FileCreateError as e:
        # For Python 3 use input() instead of raw_input().
        decision = raw_input("Exception caught in workbook.close(): %s\n"
                             "Please close the file if it is open in Excel.\n"
                             "Try to write file again? [Y/n]: " % e)
        if decision != 'n':
            continue

    break
