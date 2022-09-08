import os
import re
from bs4 import BeautifulSoup
from util import common

from util.perf_to_excel import write2excel

# Get all files end with .html
def get_html(rootDir):
    allFiles=[]
    fileList = os.listdir(rootDir)
    for filename in fileList:
        pathTmp = os.path.join(rootDir, filename)
        if os.path.isdir(pathTmp):
            get_html(pathTmp)
        elif filename[-5:].lower() == '.html':
            allFiles.append(pathTmp)
    return allFiles



# get score in html file
def get_html_score(rootDir,dstFile,data):
    html_list=get_html(rootDir)
    score = float
    if len(html_list):

        for file in html_list:
            score=common.read_html(file)
            if score:
                break
        if data==None:
            print("There are no target values in file {}".format(html_list))
    else:
        print("There are no html files in path {}".format(rootDir))

    return write2excel(dstFile, "sheet1", [data[0], data[1], score])