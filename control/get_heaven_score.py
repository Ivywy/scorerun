import os
import re
from bs4 import BeautifulSoup
from util import common
import heapq
from util.perf_to_excel import write2excel

def read_Heaven_log(file_path):
    print(file_path)
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
    fileList = [f for f in os.listdir(rootDir) if
                os.path.isfile(os.path.join(rootDir, f)) and f.endswith('.html') and f.__contains__("heaven")]

    # 去掉含old字符的文件
    seletedFiles = list(filter(lambda x: 'old' not in x, fileList))

    fileNumList = list()
    for log in seletedFiles:
        fileNumList.append(int(re.compile(r'2022\d+').findall(log)[0]))

    dic = dict(zip(fileNumList, seletedFiles))

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
        print("\033[0;31;40m", "No matched logs were found of {app},please press enter to continue or esc to exit","\033[0m")

    return dstPath

# Get all files end with .html
# def get_heaven_log(rootDir):
#     # allFiles=[]
#     fileList = os.listdir(rootDir)
#     # print(fileList,"----------")
#     for filename in fileList:
#         pathTmp = os.path.join(rootDir, filename)
#         if os.path.isdir(pathTmp):
#             get_heaven_log(pathTmp)
#         elif filename.endswith("html") and filename.__contains__("heaven"):
#             print("1111111",filename)
#             # allFiles.append(pathTmp)
#             return os.path.join(rootDir,filename)
    # return allFiles


# get score in html file
def get_Heaven_score(srcPath,dstFile,data):
    score=read_Heaven_log(srcPath)
    if score:
        return write2excel(dstFile, "sheet1", [data[0], data[1], score])
    else:
        raise Exception("There file hasn't score {}".format(srcPath))
