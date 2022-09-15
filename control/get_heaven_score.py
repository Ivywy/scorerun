import os
import re
from bs4 import BeautifulSoup
from util import common
import heapq
from util.perf_to_excel import write2excel

def read_Heaven_log(file_path):
    doc = open(file_path, 'r', encoding='utf-8').read()
    soup = BeautifulSoup(doc, "html.parser")
    total=soup.findAll(text=re.compile('.*?Total.*?'))
    if len(total):
        s = ""
        # dic = {}
        for str in total:
            if str.find("Total scores") != -1:
                s = str.split("Total scores: ")[1]
                break

        return float(s)
    else:
        print("There are no keyword 'total' in file {}".format(file_path))
        return None
def get_Heaven_log(rootDir, dstPath):
    '''
    :param rootDir: Log path where generated directory
    :param dstPath: The destination path from the rootDir copy
    :return:
    '''
    continue_ = False
    # 找出所有含有heaven的html文件
    seletedFiles = [f for f in os.listdir(rootDir) if
                os.path.isfile(os.path.join(rootDir, f)) and f.endswith('.html') and f.__contains__("heaven") and not f.__contains__("old")]

    if not seletedFiles:
        print("\033[0;31;40m", f"No matched logs were found of heaven in {rootDir}","\033[0m")
        return

    fileNumList = list()
    for log in seletedFiles:
        fileNumList.append(int(re.compile(r'2022\d+').findall(log)[0]))
    if not fileNumList:
        print("\033[0;31;40m", f" {rootDir} log should contain timestamp ", "\033[0m")
        return

    dic = dict()
    for file in seletedFiles:
        for fileNum in fileNumList:
            if file.__contains__(str(fileNum)):
                dic[fileNum]=file

    if len(fileNumList) != 0:
        # it means have more than one log file,so compare to get the newest log file
        loglist = heapq.nlargest(len(fileNumList), fileNumList)
        for fileNum in loglist:
            heavenlog = os.path.join(rootDir, dic[fileNum])
            if read_Heaven_log(heavenlog) != None:
                # copy log到指定目录
                dstPath=common.copyfile(heavenlog, dstPath)
                if os.path.exists(heavenlog) == False:
                    raise Exception(f"File {heavenlog} copy Failed!")
                continue_ = True
                break

        for file in seletedFiles:
            common.changeName(os.path.join(rootDir, file))
    else:
        print("Heaven no log generated!!!!")

    if continue_ == False:
        print("\033[0;31;40m", f"No matched logs were found of heaven,please press enter to continue or esc to exit","\033[0m")

    return dstPath

# get score in html file
def get_Heaven_score(srcPath,dstFile,data):
    score=read_Heaven_log(srcPath)
    if score:
        return write2excel(dstFile, "sheet1", [data[0], data[1], score])
    else:
        raise Exception("There file hasn't score {}".format(srcPath))
