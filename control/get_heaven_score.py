import os
import re
from bs4 import BeautifulSoup
from util import common
import heapq

from util.logger_util import  log_info,log_error
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
        log_error("There are no keyword 'total' in file {}".format(file_path))
        return None
def get_Heaven_log(rootDir, dstPath):
    '''
    :param rootDir: Log path where generated directory
    :param dstPath: The destination path from the rootDir copy
    :return:
    '''
    continue_ = False
    # find the specific logs
    seletedFiles = [f for f in os.listdir(rootDir) if
                os.path.isfile(os.path.join(rootDir, f)) and f.endswith('.html') and f.__contains__("heaven") and not f.__contains__("old")]

    if not seletedFiles:
        log_error(f"No matched logs were found of heaven in {rootDir}")
        return

    fileNumList = list()
    for log in seletedFiles:
        fileNumList.append(int(re.compile(r'2022\d+').findall(log)[0]))
    if not fileNumList:
        log_error( f" {rootDir} log should contain timestamp ")
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
                # copy to work path
                dstPath=common.copyfile(heavenlog, dstPath)
                if os.path.exists(heavenlog) == False:
                    raise Exception(f"File {heavenlog} copy Failed!")
                continue_ = True
                break

        for file in seletedFiles:
            common.changeName(os.path.join(rootDir, file))
    else:
        log_error("Heaven no log generated!!!!")

    if continue_ == False:
        log_error("No matched logs were found of heaven,please press enter to continue or esc to exit")

    return dstPath

# get score in html file
def get_Heaven_score(srcPath,dstFile,data):
    score=read_Heaven_log(srcPath)
    if score:
        return write2excel(dstFile, "sheet1", [data[0], data[1], score])
    else:
        log_error("There file hasn't score {}".format(srcPath))
