import os
import re
from bs4 import BeautifulSoup

from util.perf_to_excel import write2excel


def get_html(rootDir):
    allFiles=[]
    fileList = os.listdir(rootDir)  # 列出文件夹下所有的目录与文件
    for filename in fileList:
        pathTmp = os.path.join(rootDir, filename)  # 获取path与filename组合后的路径
        if os.path.isdir(pathTmp):  # 如果是目录
            get_html(pathTmp)  # 则递归查找
        elif filename[-5:].lower() == '.html':  # 如果不是目录，则比较后缀名
            allFiles.append(pathTmp)
    return allFiles

# 读取log内容
def read_html(file_path,app):
    doc = open(file_path, 'r', encoding='utf-8').read()
    soup = BeautifulSoup(doc, "html.parser")
    total=soup.findAll(text=re.compile('.*?Total.*?'))
    if len(total):
        s = ""
        dic = {}
        for str in total:
            if str.find("Total scores") != -1:
                s = str.split("Total scores: ")[1]
                break
        dic[app]=float(s)
        return dic
    else:
        print("There are no keyword 'total' in file {}".format(file_path))
        return

def get_html_score(rootDir,dstFile):
    html_list=get_html(rootDir)
    data = dict
    if len(html_list):

        for file in html_list:
            data=read_html(file,"Heaven11")
            if data:
                break
        if data==None:
            print("There are no target values in file {}".format(html_list))
    else:
        print("There are no html files in path {}".format(rootDir))

    return write2excel(dstFile, "sheet1", ["AC + NoHG", 'Furmark', data["Heaven11"]])