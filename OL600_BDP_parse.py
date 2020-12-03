import xlsxwriter
import re
import os
import sys
import glob

HEADERS = ['Time (sec.)','HeatSink','AF NTC','PC NTC','Probe1 NTC',
           'Probe2 NTC', 'High Pressure','Low Pressure','V','SW version (Release.Version.Revision)','Build date']

def parse(Myfiles):
    unformatted_files = set()
    for myfile in Myfiles:

        workbook = xlsxwriter.Workbook(os.path.splitext(myfile)[0]+'.xlsx')
        worksheet = workbook.add_worksheet('Data')
        worksheet.freeze_panes(1, 0)

        # Create a chart object.
        chart = workbook.add_chart({'type': 'line'})

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
    

        #print("Step2")
        #worksheet2 = workbook.add_worksheet('RAW')

        header_format = workbook.add_format()
        header_format.set_align('center')
        header_format.set_bold()
        header_format.set_text_wrap()
        header_format.set_align('vcenter')

        cell_format = workbook.add_format()
        cell_format.set_align('center')
        ##cell_format.set_text_wrap()

        for index, i in enumerate(HEADERS):
            worksheet.write(0, index, i,header_format)

        #print("Step3")
        
        for row in range (0,len(data)):
            cell = data[row].split(',')

            #print("Step4")
            for col in range (0,len(cell)):
                try:
                    worksheet.write(row+1, col+len(HEADERS)+1, cell[col],cell_format)
                    if col<5:
                        convert_cell = int(cell[col][5:],16)/10
                    #print("Step5")
                    elif col>=5 and col<7:
                        convert_cell = int(cell[col][4:])
                    elif col == 7:
                        convert_cell = ''

                    #match SW version BDP                        
                    x = re.match(r'(\$WZ)(..)(..)(..)(\w+........)',cell[col])
                    #print("Step6")
                    if x:
                        SW_version = x.group(2)+'.'+ x.group(3)+'.'+x.group(4)
                        worksheet.write(row+1, col+2, SW_version,cell_format)
                        worksheet.write(row+1, col+3, x.group(5),cell_format)   
                    #print("Step7")
                    else:
                        pass
                    
                     #time
                    worksheet.write(row+1, 0, row+1,cell_format)
                     #Columns
                    if col < 8:
                        worksheet.write(row+1, col+1, convert_cell,cell_format)

                #print("Step8")
                except:
                    unformatted_files.add(myfile)
                    continue


        #Chart
        chart.add_series({
            'name': ['Data',0,1],
            'values':     '=Data!$B2:$B3159',
        })

        # Configure the chart axes.
        chart.set_y_axis({'major_gridlines': {'visible': True}})
        chart.set_x_axis({'name': 'Time (sec.)'})

        # Turn off chart legend. It is on by default in Excel.
        chart.set_legend({'position': 'none'})

        while True:
            try:
                worksheet.insert_chart('L2', chart)
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
