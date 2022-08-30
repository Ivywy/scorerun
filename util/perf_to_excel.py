import os
import xlrd
import xlwt
from xlutils.copy import copy


def write_excel_head(fileName,sheetName,row_head,column_head):
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet(sheetName,cell_overwrite_ok=True)

    # 设置字体加粗
    style = xlwt.easyxf('font: bold on')
    # 写入首行
    for index, title in enumerate(row_head):
        worksheet.write(0, index+1, title,style)
    # 写入首列
    for row in range(len(column_head)):
        worksheet.write(row + 1, 0, column_head[row],style)
    workbook.save(fileName)

def get_value_position(fileName,sheet_name,row_name,col_name):
    wb = xlrd.open_workbook(fileName,formatting_info=True)
    sheet=wb.sheet_by_name(sheet_name)
    row, col = 0, 0
    row_head=sheet.row_values(0)
    if row_name in row_head:
        col=row_head.index(row_name)
    else:
        raise Exception("%s not found in list"%row_name)
    coloumn_head=sheet.col_values(0)
    # print("column_head=",coloumn_head)
    if col_name in coloumn_head:
        row=coloumn_head.index(col_name)
    else:
        raise Exception("%s not found in list"%col_name)
    return row,col

def write2excel(fileName,sheetName,data):
    # 校验filename是否为xls后缀
    if not fileName.endswith(".xls"):
        raise Exception("destination file should end with xls")
    row_head = ["AC + HG", "DC + HG", "AC + NoHG", "DC + NoHG"]
    column_head = ["TimeSpy_Score","TimeSpy_FPS", "Furmark", "Heaven11", "FireStrike","3dmark11"]

    # 检查data[0]与data[1]是否在row_head与column_head中
    if data[0] not in row_head or data[1] not in column_head:
        raise Exception("data error! data[0] should in {} and data[1] should in {}".format(row_head,column_head))

    # 检查xls文件是否存在，如果不存在，就新建
    if not os.path.exists(fileName):
        write_excel_head(fileName,sheetName,row_head,column_head)

    # 检查传入的sheetName在表格中是否存在，如果不存在就新建一个工作表
    wb = xlrd.open_workbook(fileName,formatting_info=True)
    sheetnames = wb.sheet_names()
    if sheetName not in sheetnames:
        raise Exception("%s Not Found"%sheetName)

    # data[0]必须是列中元素 data[1]必须是行中元素 否则报错

    workbook = copy(wb=wb)
    worksheet = workbook.get_sheet(sheetnames.index(sheetName))

    # 检查data是不是一个列表
    if not isinstance(data,list):
        raise Exception("data is not a list")
    
    # 检查data[2]是否是int或float型
    if not isinstance(data[2],int) and not isinstance(data[2],float):
        raise Exception("the value must be int or float")

    pos=list(get_value_position(fileName,sheetName,data[0],data[1]))
    worksheet.write(pos[0],pos[1],data[2])
    workbook.save(fileName)

    # TODO 读取excel数据
    # if data[2]==read4excel(fileName,sheetName,pos[0],pos[1]):
    #     print("data write to excel success!!")
    # else:
    #     raise Exception("Write data failed!")

def read4excel(fileName,sheet,row,col):
    wb = xlrd.open_workbook(fileName, formatting_info=True)
    worksheet=wb.get_sheet(sheet)
    value=worksheet.cell(row,col)
    print(value)
    return value



def unit_test_filename():
    try:
        write2excel("text1.txt","sheet1",["AC + HG",'Heaven11',1999.99])
    except Exception:
        return

def unit_test_sheet():
    try:
        write2excel("text1.xls","sheet2",["AC + HG",'Heaven11',1999.99])
    except Exception:
        return

def unit_test_data(): 
    try:
        write2excel("text1.xls","sheet1",["AC + HG",'Heaven11',1999.99])
        write2excel("text1.xls","sheet1",["AC + HG1",'Heaven11',1999.99])
        write2excel("text1.xls","sheet1",["AC + HG",'Heaven111',"1999.99"])
    except Exception:
        return

# if __name__ == "__main__":
#
#     data_path="data"
#     write2excel("text.xls1", "sheet1", ["AC + NoHG", 'Furmark', 1200.19])








