import os
import xlrd
import xlwt
from xlutils.copy import copy

from util.logger_util import log_info, log_error, log_debug, log_critical


# Write the first column and first row of data to the table
def write_excel_head(fileName,sheetName,row_head,column_head):
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet(sheetName,cell_overwrite_ok=True)

    style = xlwt.easyxf('font: bold on')
    # write first row
    for index, title in enumerate(row_head):
        worksheet.write(0, index+1, title,style)
    # write first column
    for row in range(len(column_head)):
        worksheet.write(row + 1, 0, column_head[row],style)
    workbook.save(fileName)

def get_value_position(fileName,sheet_name,row_name,col_name):
    wb = xlrd.open_workbook(fileName,formatting_info=True)
    sheet=wb.sheet_by_name(sheet_name)
    row, col = 0, 0
    row_head=sheet.row_values(0)
    log_debug(f"row_name={row_name},col_name={col_name}")
    if row_name in row_head:
        col=row_head.index(row_name)
    else:
        log_error( f"{row_name} not found in list")
        return
    coloumn_head=sheet.col_values(0)
    if col_name in coloumn_head:
        row=coloumn_head.index(col_name)
    else:
        log_error(f"{col_name} not found in list")
        return
    return row,col

def write2excel(fileName,sheetName,data):
    """

    :param fileName:
    :param sheetName:
    :param data: data[0] is mode; data[1] is app; data[2] is score
    :return:
    """
    # Check if the file name is the xls suffix
    if not fileName.endswith(".xls"):
        log_critical("destination file should end with xls")
    row_head = ["AC+HG", "DC+HG", "AC+NoHG", "DC+NoHG"]
    column_head = ["TimeSpy","TimeSpy_FPS", "FurMark", "Heaven", "FireStrike","3dmark11"]

    # Check whether data[0] and data[1] are in row_head and column_head
    # if data[0] not in row_head or data[1] not in column_head:
    #     raise Exception(f"data error! {data[0]} should in {row_head} and {data[1]} should in {column_head}")

    # Check if the xls file exists, if not, create a new one
    if not os.path.exists(fileName):
        write_excel_head(fileName,sheetName,row_head,column_head)

    # check whether the fileName exists in excel
    wb = xlrd.open_workbook(fileName,formatting_info=True)
    sheetnames = wb.sheet_names()
    if sheetName not in sheetnames:
        log_critical("%s Not Found"%sheetName)

    workbook = copy(wb=wb)
    worksheet = workbook.get_sheet(sheetnames.index(sheetName))

    if not isinstance(data,list):
        log_critical("data is not a list")

    if not isinstance(data[2],int) and not isinstance(data[2],float):
        log_critical("the value must be int or float")

    pos=list(get_value_position(fileName,sheetName,data[0],data[1]))
    worksheet.write(pos[0],pos[1],data[2])
    workbook.save(fileName)
    log_info(f"{data[1]}'s score={data[2]} has been collected in {fileName} successfully!")

def read4excel(fileName,sheet,row,col):
    wb = xlrd.open_workbook(fileName, formatting_info=True)
    worksheet=wb.get_sheet(sheet)
    value=worksheet.cell(row,col)
    return value







