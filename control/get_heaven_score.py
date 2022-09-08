import os
import re
from bs4 import BeautifulSoup
from util import common

from util.perf_to_excel import write2excel

# Get all files end with .html
def get_heaven_log(rootDir):
    # allFiles=[]
    fileList = os.listdir(rootDir)
    for filename in fileList:
        pathTmp = os.path.join(rootDir, filename)
        if os.path.isdir(pathTmp):
            get_heaven_log(pathTmp)
        elif filename.endswith("html") & filename.__contains__("Heaven11"):
            # allFiles.append(pathTmp)
            return filename
    # return allFiles


# get score in html file
def get_html_score(rootDir,dstFile,data):
    heavenLog=get_heaven_log(rootDir)
    score=common.read_html(heavenLog)
    if not score:
        return score
    else:
        print("There file hasn't score {}".format(rootDir))

    return write2excel(dstFile, "sheet1", [data[0], data[1], score])