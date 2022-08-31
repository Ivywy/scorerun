import os
import re
from bs4 import BeautifulSoup

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

# read file content
def read_html(file_path):
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
        return

# get score in html file
def get_html_score(rootDir,dstFile,data):
    html_list=get_html(rootDir)
    score = float
    if len(html_list):

        for file in html_list:
            score=read_html(file)
            if score:
                break
        if data==None:
            print("There are no target values in file {}".format(html_list))
    else:
        print("There are no html files in path {}".format(rootDir))

    return write2excel(dstFile, "sheet1", [data[0], data[1], score])