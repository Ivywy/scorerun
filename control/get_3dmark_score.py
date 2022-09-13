import os
from pickle import FALSE, TRUE
import sys
import tempfile
import zipfile
import shutil
from util import common
from xml.etree import ElementTree

from util.perf_to_excel import write2excel

def get_3dmark(rootDir):
    allFiles = []
    fileList = os.listdir(rootDir)
    for filename in fileList:
        pathTmp = os.path.join(rootDir, filename)
        if os.path.isdir(pathTmp):
            get_3dmark(pathTmp)
        elif filename.endswith("3dmark-result") and "-FAILED-" not in filename:
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


def get_3dmark_score(rootDir,dstFile,data):
    fileList=get_3dmark(rootDir)
    print(fileList)
    score, test1, test2=float(),float(),float()
    for file in fileList:
        if "TimeSpy" in file:
            timespy_log=extract_3dResult(file, os.path.join(rootDir,"3dmarkResult-{}.xml".format(common.get_time())))
            # if data[1]=="TimeSpy_Score" or data[1] == "TimeSpy_FPS":
            #     score=read_xml(timespy_log,"TimeSpyCustom3DMarkScore")
            #     test1=read_xml(timespy_log,"TimeSpyCustomGraphicsTest1")
            #     test2=read_xml(timespy_log,"TimeSpyCustomGraphicsTest2")
            #     print(score, test1, test2)
            #     if score != 0:
            #         print(f"TimeSpy_Score={score}")
            #     elif score == 0 & test1 == -1 & test2 !=0:
            #         print(f"TimeSpy_FPS={test2}")
            #     else:
            #         print("Neither TimeSpy_Score and not TimeSpy_FPS")
            if data[1] == "TimeSpy_Score":
                score = read_xml(timespy_log, "TimeSpyCustom3DMarkScore")
            elif data[1] == "TimeSpy_FPS":
                scoreAll=read_xml(timespy_log,"TimeSpyCustom3DMarkScore")
                test1=read_xml(timespy_log,"TimeSpyCustomGraphicsTest1")
                test2=read_xml(timespy_log,"TimeSpyCustomGraphicsTest2")
                # TODO 再验证test1=-1的情况
                # if scoreAll == 0 and test1 == -1 and test2 != 0:
                if scoreAll == 0 and test2 != 0:
                    score=test2
                    # print(f"TimeSpy_FPS={score}")
        elif "FireStrike" in file:
                if data[1] in file:
                    timespy_log=extract_3dResult(file, os.path.join(rootDir,"3dmarkResult-{}.xml".format(common.get_time())))
                    score=read_xml(timespy_log,"FireStrikeCustomGraphicsScore")
                    break
        else:
            raise Exception("Parameter error")

    return write2excel(dstFile, "sheet1", [data[0], data[1], float(score)])

def get_3dmark11(rootDir):
    allFiles = []
    fileList = os.listdir(rootDir)
    for filename in fileList:
        pathTmp = os.path.join(rootDir, filename)
        if os.path.isdir(pathTmp):
            get_3dmark(pathTmp)
        elif filename.endswith("3dmark-11-result"):
            allFiles.append(pathTmp)
    return allFiles

def get_3dmark11_score(rootDir,dstFile,data):
    fileList = get_3dmark11(rootDir)
    score = float()
    for file in fileList:
        log=extract_3dResult(file,os.path.join(rootDir,"3dmark11Result-{}.xml".format(common.get_time())))
        score = read_xml(log, "GraphicsScore")
