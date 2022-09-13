import os
import re
from bs4 import BeautifulSoup
from util import common

from util.perf_to_excel import write2excel

# Get all files end with .html
def get_heaven_log(rootDir):
    # allFiles=[]
    fileList = os.listdir(rootDir)
    # print(fileList,"----------")
    for filename in fileList:
        pathTmp = os.path.join(rootDir, filename)
        if os.path.isdir(pathTmp):
            get_heaven_log(pathTmp)
        elif filename.endswith("html") and (filename.__contains__("heaven") or filename.__contains__("Heaven")):
            print("1111111",filename)
            # allFiles.append(pathTmp)
            return os.path.join(rootDir,filename)
    # return allFiles


# get score in html file
def get_html_score(rootDir,dstFile,data):
    heavenLog=get_heaven_log(rootDir)
    if heavenLog == None:
        print("there is not heavenlog")
        return
    score=common.read_heaven_log(heavenLog)
    if score:
        return write2excel(dstFile, "sheet1", [data[0], data[1], score])
    else:
        raise Exception("There file hasn't score {}".format(rootDir))
