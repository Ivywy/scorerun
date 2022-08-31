import os
import pandas as pd
import xlwt
import xlrd
from xlutils.copy import copy
from util.common import mk_dir

# 将指定列的数据写入excel
def csv_excel(csv_path,excel_path):
    file = pd.read_csv(csv_path)
    print("++++++++++++++")
    row_head = ['GPU0 Power Socket Power', 'GPU0 Frequencies Target Frequency GFXCLK',
                'GPU0 Frequencies Actual Frequency GFXCLK', 'GPU0 Power TGP Power', 'GPU0 Temperature Hotspot',
                'GPU0 Temperature MEM', 'GPU0 Fan PWM']
    datas = file[row_head]
    write_excel_head(excel_path,"sheet_1",row_head)
    datas.to_excel(excel_path,index=False)

# 将指定列的最大值和平均值写入excel
def csv2excel(csv_path,excel_path,mode):
    # 校验filename是否为xls后缀
    if not excel_path.endswith(".xls"):
        raise Exception(IOError)

    # 检查 mode是否正确
    if mode[0] not in ["TimeSpy_Score","TimeSpy_FPS","Furmark","Heaven11","FireStrike","3dmark11"]:
        raise Exception('arg error!! mode[0] must in ["TimeSpy_Score","TimeSpy_FPS","Furmark","Heaven11","FireStrike","3dmark11"] ')
    if mode[1] not in ["AC + HG","DC + HG","AC + NoHG","DC + NoHG"]:
        raise Exception('arg error!! mode[1] must in ["AC + HG","DC + HG","AC + NoHG","DC + NoHG"]')
    # 检查xls文件是否存在，如果不存在，就新建
    row_head = ['GPU0 Power Socket Power', 'GPU0 Frequencies Target Frequency GFXCLK',
                'GPU0 Frequencies Actual Frequency GFXCLK', 'GPU0 Power TGP Power', 'GPU0 Temperature Hotspot',
                'GPU0 Temperature MEM', 'GPU0 Fan PWM']
    # _,file_name=os.path.split(excel_path)
    if not os.path.exists(excel_path):
        write_excel_head(excel_path, mode[0], row_head)
    # 检查sheet是否存在，如果不存在，则新建
    rb = xlrd.open_workbook(excel_path,formatting_info=True)
    sheetnames = rb.sheet_names()
    if mode[0] not in sheetnames:
        wb = copy(wb=rb)
        sheet=wb.add_sheet(mode[0])
        # write_excel_head(excel_path, mode[0], row_head)
        style = xlwt.easyxf('font: bold on')
        for index, title in enumerate(row_head):
            sheet.write(0, index + 1, title, style)
        wb.save(excel_path)
        # raise Exception("{} not Found in {}".format(mode[0],excel_path))
    # 读取csv文件内容
    file = pd.read_csv(csv_path)

    # 构造第一列数据
    max_0="{}_max".format(mode[1])
    aver_0="{}_average".format(mode[1])
    max_lis,aver_lis=list(),list()
    max_lis.append(max_0)
    aver_lis.append(aver_0)

    # 求最大值和平均值并写入excel
    value_lis = list()
    for i in row_head:
        max_value=file[i].max()
        max_lis.append(max_value)
        aver_value=file[i].mean()
        aver_lis.append(aver_value)

    value_lis.append(max_lis)
    value_lis.append(aver_lis)
    write_excel_xls_append(excel_path,mode[0],value_lis)

def write_excel_head(path, sheet_name, row_head):
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet(sheet_name)
    style = xlwt.easyxf('font: bold on')
    for index, title in enumerate(row_head):
        worksheet.write(0, index+1, title,style)
    workbook.save(path)  # 保存工作簿

def write_excel_xls_append(path, sheet_name,value):
    index = len(value)
    workbook = xlrd.open_workbook(path,formatting_info=True)
    sheets = workbook.sheet_names()
    worksheet = workbook.sheet_by_name(sheet_name)
    rows_old = worksheet.nrows
    new_workbook = copy(workbook)
    new_worksheet = new_workbook.get_sheet(sheets.index(sheet_name))
    for i in range(0, index):
        for j in range(0, len(value[i])):
            if j==0:
                style=xlwt.easyxf('font: bold on')
                new_worksheet.write(i + rows_old, j, value[i][j],style)
            else:
                new_worksheet.write(i + rows_old, j, value[i][j])
    new_workbook.save(path) 




