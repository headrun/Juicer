import xlwt

excel_file_name = 'mighty_fares.xlsx'
todays_excel_file = xlwt.Workbook(encoding="utf-8")

page = 1
counter =1
def parse_head():
    header = ['url','Title','Text','date','date in epoch','Author','Auth_url']

    for i, row in enumerate(header):
        todays_excel_sheet.write(0,i,row)


header = ['url','Title','Text','date','date in epoch','Author','Auth_url']
todays_excel_sheet = todays_excel_file.add_sheet('sheet1',cell_overwrite_ok=True)
parse_head()

for row in open('fares.txt', 'r').readlines():
    list_values = eval(row)
    
    for col_count,value in enumerate(list_values):
        todays_excel_sheet.write(counter, col_count, value)
    counter +=1

    if counter >5000:
        counter = 1
        page = page+1
        todays_excel_sheet = todays_excel_file.add_sheet("sheet%s" %page, cell_overwrite_ok=True)
        parse_head()


todays_excel_file.save(excel_file_name)




