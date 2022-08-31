import os
import sys
import tempfile
import zipfile
import shutil
from util import common
from xml.etree import ElementTree

from util.perf_to_excel import write2excel


def get_3dmark(rootDir):
    allFiles = []
    fileList = os.listdir(rootDir)  # 列出文件夹下所有的目录与文件
    for filename in fileList:
        pathTmp = os.path.join(rootDir, filename)  # 获取path与filename组合后的路径
        if os.path.isdir(pathTmp):  # 如果是目录
            get_3dmark(pathTmp)  # 则递归查找
        elif filename.endswith("3dmark-result") and "-0-" in filename:  # 如果不是目录，则比较后缀名
            allFiles.append(pathTmp)
    return allFiles

def extract_3dResult(filename,dst_name):
    if os.path.isfile(filename):
        tmp = tempfile.mkdtemp()
        zipfile.ZipFile(filename).extractall(tmp)
        shutil.copyfile(os.path.join(tmp,"Result.xml"), dst_name)
        shutil.rmtree(tmp)
        if os.path.exists(dst_name):
            return dst_name
        else:
            print("The 3dMark result generate failed!")
    else:
        print(filename, "{} is not a file".format(filename))
        sys.exit(0)

def read_xml(file_path,item):
    data=float()
    dom = ElementTree.parse(file_path)
    root = dom.getroot()
    result = root.findall(".//result/")
    for element in result:
        if element.tag == item:
            data= element.text
            break

    return data


def get_3dmark_score(rootDir,dstFile,data):
    fileList=get_3dmark(rootDir)
    score=float()
    if data[1]=="TimeSpy_Score":
        for file in fileList:
            if "TimeSpy" in file:
                timespy_log=extract_3dResult(file, os.path.join(rootDir,"3dmarkResult-{}.xml".format(common.get_time())))
                score=read_xml(timespy_log,"TimeSpyExtremeCustomGraphicsScore")
                break
    elif data[1] == "TimeSpy_FPS":
        for file in fileList:
            if "TimeSpy" in file:
                timespy_log = extract_3dResult(file, os.path.join(rootDir,
                                                                  "3dmarkResult-{}.xml".format(common.get_time())))
                score = read_xml(timespy_log, "TimeSpyExtremeCustomGraphicsScore1")
                # TODO 再增加判断
                if score == 0:
                    score=read_xml(timespy_log,"TimeSpyCustomGraphicsTest2")
                    break

    elif data[1]=="FireStrike":
        for file in fileList:
            if data[1] in file:
                timespy_log=extract_3dResult(file, os.path.join(rootDir,"3dmarkResult-{}.xml".format(common.get_time())))
                score=read_xml(timespy_log,"FireStrikeCustomGraphicsScore")
                break
    else:
        raise Exception("Parameter error")
    return write2excel(dstFile, "sheet1", [data[0], data[1], float(score)])

def get_3dmark11(rootDir):
    allFiles = []
    fileList = os.listdir(rootDir)  # 列出文件夹下所有的目录与文件
    for filename in fileList:
        pathTmp = os.path.join(rootDir, filename)  # 获取path与filename组合后的路径
        if os.path.isdir(pathTmp):  # 如果是目录
            get_3dmark(pathTmp)  # 则递归查找
        elif filename.endswith("3dmark-11-result"):  # 如果不是目录，则比较后缀名
            allFiles.append(pathTmp)
    return allFiles

def get_3dmark11_score(rootDir,dstFile,data):
    fileList = get_3dmark11(rootDir)
    score = float()
    for file in fileList:
        log=extract_3dResult(file,os.path.join(rootDir,"3dmark11Result-{}.xml".format(common.get_time())))
        score = read_xml(log, "GraphicsScore")
