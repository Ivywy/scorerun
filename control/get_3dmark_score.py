import os
from pickle import FALSE, TRUE
import sys
import tempfile
import zipfile
import shutil
from util import common
from xml.etree import ElementTree
import heapq
import re

from util.logger_util import log_error
from util.perf_to_excel import write2excel

# 从src目录中找到log文件，并移动到指定文件夹
def get_3dmark_log(rootDir, dstPath, app):
    '''
    :param rootDir: Log path where generated directory
    :param dstPath: The destination path from the rootDir copy
    :param app:application
    :return:
    '''
    continue_ = False
    # 找到.3dmark-result结尾并包含TimeSpy的日志
    fileList = [f for f in os.listdir(rootDir) if
                    os.path.isfile(os.path.join(rootDir, f)) and not f.__contains__('old') and f.endswith('.3dmark-result')]

    if app == "TimeSpy":
        fileList = [f for f in fileList if f.__contains__("TimeSpyExtreme") and not f.__contains__("FAILED") and not f.__contains__("-0-")]
    elif app == "TimeSpy_FPS":
        fileList = [f for f in fileList if f.__contains__("TimeSpyExtreme") and not f.__contains__("FAILED") and f.__contains__("-0-")]

    elif app == "FireStrike":
        fileList = [f for f in fileList if f.__contains__("FireStrikeCustom") and not f.__contains__("FAILED")]

    # 去掉含old字符的文件
    seletedFiles = list(filter(lambda x: 'old' not in x, fileList))

    # 正则取出日志名字的时间戳
    logs = list()
    for log in seletedFiles:
        logs.append(int(re.compile(r'2022\d+').findall(log)[0]))
    # 根据时间戳找出最新生成的log，并复制到工作目录
    if len(logs) != 0:
        # it means have more than one log file,so compare to get the newest log file
        maxLogList = heapq.nlargest(1, logs)
        for file in seletedFiles:
            if file.__contains__(str(maxLogList[0])):
                dstPath = common.copyfile(os.path.join(rootDir, file), dstPath)
                continue_ = True
                break

        for file in seletedFiles:
            common.changeName(os.path.join(rootDir, file))
    else:
        log_error(f"{app} no log generated!!!!")

    if continue_ == False:
        log_error(f"No matched logs were found of {app},please ensure log has been generated in {rootDir}")
        return

    return dstPath

def extract_3dResult(filename,dst_name):
    if os.path.isfile(filename):
        tmp = tempfile.mkdtemp()
        zipfile.ZipFile(filename).extractall(tmp)
        shutil.copyfile(os.path.join(tmp,"Result.xml"), dst_name)
        shutil.rmtree(tmp)
        if os.path.exists(dst_name):
            return dst_name
        else:
            log_error("The 3dMark result generate failed!")
    else:
        log_error("{} is not a file".format(filename))
        sys.exit(0)

def is_exist(srcPath,app,item):
    rootDir = os.path.dirname(srcPath)
    xml_log = extract_3dResult(srcPath, os.path.join(rootDir, f"3dmarkResult-{app}-{common.get_time()}.xml"))
    data = read_xml(xml_log, item)
    if data!=-1:
        return True
    else:
        return False
def read_xml(file_path,item):
    data=float()
    find_it=bool()
    find_it= False
    dom = ElementTree.parse(file_path)
    root = dom.getroot()
    result = root.findall(".//result/")
    for element in result:
        if element.tag == item:
            data= float(element.text)
            find_it = True
            break

    if find_it == False:
        return -1 # -1 means not found 
    return data

# 读取score
def get_3dmark_score(srcPath,dstFile,data):
    rootDir = os.path.dirname(srcPath)
    xml_log = extract_3dResult(srcPath, os.path.join(rootDir, f"3dmarkResult-{data[1]}-{common.get_time()}.xml"))
    score=float()
    if data[1]=="TimeSpy":
        score = read_xml(xml_log, "TimeSpyExtremeGraphicsScore")
    elif data[1]=="TimeSpy_FPS":
        scoreAll=read_xml(xml_log,"TimeSpyExtremeGraphicsScore")
        test1=read_xml(xml_log,"TimeSpyExtremeGraphicsTest1")
        test2=read_xml(xml_log,"TimeSpyExtremeGraphicsTest2")
        # TODO 再验证test1=-1的情况
        # if scoreAll == 0 and test1 == -1 and test2 != 0:
        if scoreAll == 0 and test2 != 0:
            score=test2
    elif data[1]=="FireStrike":
        score = read_xml(xml_log, "FireStrikeCustomGraphicsScore")
    else:
        raise Exception("Parameter error")

    return write2excel(dstFile, "sheet1", [data[0], data[1], float(score)])
    # fileList=get_3dmark(rootDir)
    # print(fileList)
    # score, test1, test2=float(),float(),float()
    # for file in fileList:
    #     if "TimeSpy" in file:
    #         timespy_log=extract_3dResult(file, os.path.join(rootDir,"3dmarkResult-{}.xml".format(common.get_time())))
    #         if data[1] == "TimeSpy_Score":
    #             score = read_xml(timespy_log, "TimeSpyExtremeCustomGraphicsScore")
    #         elif data[1] == "TimeSpy_FPS":
    #             scoreAll=read_xml(timespy_log,"TimeSpyExtremeCustomGraphicsScore")
    #             test1=read_xml(timespy_log,"TimeSpyCustomGraphicsTest1")
    #             test2=read_xml(timespy_log,"TimeSpyCustomGraphicsTest2")
    #             # TODO 再验证test1=-1的情况
    #             # if scoreAll == 0 and test1 == -1 and test2 != 0:
    #             if scoreAll == 0 and test2 != 0:
    #                 score=test2
    #     elif "FireStrike" in file:
    #             if data[1] in file:
    #                 timespy_log=extract_3dResult(file, os.path.join(rootDir,"3dmarkResult-{}.xml".format(common.get_time())))
    #                 score=read_xml(timespy_log,"FireStrikeCustomGraphicsScore")
    #                 break
    #     else:
    #         raise Exception("Parameter error")
    #
    # return write2excel(dstFile, "sheet1", [data[0], data[1], float(score)])


def get_3dmark11(rootDir):
    allFiles = []
    fileList = os.listdir(rootDir)
    for filename in fileList:
        pathTmp = os.path.join(rootDir, filename)
        if os.path.isdir(pathTmp):
            get_3dmark11(pathTmp)
        elif filename.endswith("3dmark-11-result"):
            allFiles.append(pathTmp)
    return allFiles

def get_3dmark11_score(rootDir,dstFile,data):
    fileList = get_3dmark11(rootDir)
    score = float()
    for file in fileList:
        log=extract_3dResult(file,os.path.join(rootDir,"3dmark11Result-{}.xml".format(common.get_time())))
        score = read_xml(log, "GraphicsScore")
