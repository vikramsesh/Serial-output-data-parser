import os
import sys
import xlsxwriter
import re
import glob

pathname = r"C:\Users\vseshadri\Downloads\Test"
os.chdir(pathname)

Myfiles = [i for i in glob.glob('*')]

HEADERS = ['Time','Outlet Temp', 'Boiler Temp', 'Warm Plate Temp', 'Max Temp', 'Calibrated Offset Temp', 'Pump PWM', 'Boiler On/Off', 'PTC On/Off',
           'Flow rate', 'Current Block Volume', 'Current Total Volume', 'Clean Count', 'Recipe Size', 'Recipe Brew',
           'Recipe Block', 'Recipe Total Volume', 'Recipe Time']
     
SUB_HEADERS = ['sec.','degC','degC','degC','degC','degC']

SUMMARY_HEADERS = ['Max. Outlet Temp', 'Max. Boiler Temp', 'Max. Warm Plate Temp',
                   'Max. Flowrate']

SUMMARY_SUB_HEADERS = ['degC','degC','degC','ml/sec.']

def closeworkbook():
    while True:
        try:
            print("Complete")
            workbook.close()
            
        except xlsxwriter.exceptions.FileCreateError as e:
            # For Python 3 use input() instead of raw_input().
            decision = raw_input("Exception caught in workbook.close(): %s\n"
                                 "Please close the file if it is open in Excel.\n"
                                 "Try to write file again? [Y/n]: " % e)
            if decision != 'n':

                continue
        except:
            continue
        break

for i in Myfiles:
    workbook = xlsxwriter.Workbook(os.path.splitext(i)[0]+'.xlsx',{'constant_memory': True})
    print(i)
    #RAW data
    worksheet = workbook.add_worksheet('Data')
    worksheet.freeze_panes(1, 0)
    worksheet.set_column('A:R', 8.8)

    #Summary data
##    summary_worksheet = workbook.add_worksheet('Summary')
##    summary_worksheet.freeze_panes(1, 0)
    
    f = open(i,encoding= 'utf-8',errors='ignore')
    try:
        data = f.read()
    except:
        continue

    entries = data.split('\n')
    entries.remove(entries[0])
    entries.remove(entries[1])

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
                    if x:
                        data[k] = x.group(2)
                        data[k] = float(data[k])

                    if y:
                        data[k] = y.group(2)
                        data[k] = float(data[k])
                        
                    worksheet.write(row_index, k+1, data[k],data_format)
                    pass
            print(data)
            
        closeworkbook()
    
    except KeyboardInterrupt as e:
        closeworkbook()
        
    except:
        continue
