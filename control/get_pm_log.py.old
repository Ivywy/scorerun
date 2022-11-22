import heapq
import os
import re

import pandas as pd
import xlwt
import xlrd
from xlutils.copy import copy

from util import common
from util.common import mk_dir
from util.logger_util import log_error, log_info, log_debug


# Write the data of the specified column to excel
def csv_excel(csv_path,excel_path):
    file = pd.read_csv(csv_path,dtype={"user_id": int, "username": object})
    row_head = ['GPU0 Power Socket Power', 'GPU0 Frequencies Target Frequency GFXCLK',
                'GPU0 Frequencies Actual Frequency GFXCLK', 'GPU0 Power TGP Power', 'GPU0 Temperature Hotspot',
                'GPU0 Temperature MEM', 'GPU0 Fan PWM']
    datas = file[row_head]
    write_excel_head(excel_path,"sheet_1",row_head)
    datas.to_excel(excel_path,index=False)

# Write maximum and average value of column to excel
def csv2excel(csv_path,excel_path,mode):
    if not excel_path.endswith(".xls"):
        raise Exception(IOError)

    # if mode[0] not in ["TimeSpy","TimeSpy_FPS","Furmark","Heaven11","FireStrike","3dmark11"]:
    #     raise Exception('arg error!! mode[0] must in ["TimeSpy","TimeSpy_FPS","Furmark","Heaven11","FireStrike","3dmark11"] ')
    # if mode[1] not in ["AC + HG","DC + HG","AC + NoHG","DC + NoHG"]:
    #     raise Exception('arg error!! mode[1] must in ["AC + HG","DC + HG","AC + NoHG","DC + NoHG"]')

    row_head = ['GPU0 Power Socket Power', 'GPU0 Frequencies Target Frequency GFXCLK',
                'GPU0 Frequencies Actual Frequency GFXCLK', 'GPU0 Power TGP Power', 'GPU0 Temperature Hotspot',
                'GPU0 Temperature MEM', 'GPU0 Fan PWM']

    # row_head = ['GPU0 Power Socket Power', 'GPU0 GDFLL Frequencies DFLL0 Targe',
    #             'GPU0 GDFLL Frequencies DFLL0 Pre-DS', 'GPU0 Power TGP Power', 'GPU0 Temperature Hotspot',
    #             'GPU0 Temperature MEM', 'GPU0 Fan PWM']
    _,file_name=os.path.split(excel_path)
    if not os.path.exists(excel_path):
        write_excel_head(excel_path, mode[0], row_head)

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

    file = pd.read_csv(csv_path)

    # Construct the first column data
    max_0="{}_max".format(mode[1])
    aver_0="{}_average".format(mode[1])
    max_lis,aver_lis=list(),list()
    max_lis.append(max_0)
    aver_lis.append(aver_0)

    # get max & mean value and write to excel
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
    workbook.save(path)

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

def seek_latest_log(rootDir,app,dstPath):
    # 获取该app的所有log文件
    log_debug(f"app={app}")
    tailKey=common.get_pm_key(app)
    # print("tailKey=",tailKey)
    fileList=[f for f in os.listdir(rootDir) if f.endswith(tailKey) and not f.__contains__("old")]
    # print("fileList=",fileList)

    # 提取出上面列表的时间戳列表，并构造成字典
    fileNumList=[]
    regex = re.compile(r'\d+.*-\d')
    if fileList:
        for file in fileList:
            file_num = int(regex.findall(file)[0].replace("-",""))
            fileNumList.append(file_num)
        dic=dict(zip(fileNumList,fileList))

        # 获取时间戳最大的文件，即为该app最新的log目录
        maxNum=heapq.nlargest(1, fileNumList)[0]
        latest_path=os.path.join(rootDir,dic[maxNum])
        log_debug(f"latest_path={latest_path}")

        # 进入该文件找到pm_log.csv，并移动到工作目录
        dstPath=os.path.join(dstPath,app)
        if not os.path.exists(dstPath):
            os.makedirs(dstPath)
        finalPath=common.seek_file(latest_path, dstPath)
        if not finalPath:
            log_error(f"There are not pm_log.csv in {latest_path},please check!",)
            return
        log_debug(f"finalPath={finalPath}")

        #修改latest_path名字，方便下次寻找时过滤
        for file in fileList:
            common.changeName(os.path.join(rootDir,file))

        return finalPath
    else:
        log_error(f"No matched pmlogs were found of {app},please ensure log has been generated in {rootDir}")
        return

def collect_pm_log(srcPath,dstPath,data):
    workPath=seek_latest_log(srcPath,data[0],dstPath)
    if workPath:
        excel_path = os.path.join(dstPath, "pm_log.xls")
        csv2excel(workPath,excel_path,data)
        log_info(f"{data[0]}'s pmlog has been collected in {excel_path} successfully!")
    else:
        log_error("No matched pmlogs")
        return






