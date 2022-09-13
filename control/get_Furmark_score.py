import os
import re

from util.perf_to_excel import write2excel

def get_furmark_log(rootDir):
    fileList = os.listdir(rootDir)
    for filename in fileList:
        pathTmp = os.path.join(rootDir, filename)
        if os.path.isdir(pathTmp):
            get_furmark_log(pathTmp)
        elif filename.endswith("txt") & filename.__contains__("FurMark"):
            return filename
    # return allFiles
def get_txt_score(rootDir,dstFile,data):
    # TODO posite FurMark log
    li = list()

    fmLogFile = get_furmark_log(rootDir)
    if fmLogFile == None:
        print("no furmark log file")
        return

    furmarkLog=os.path.join(rootDir, fmLogFile)

    if not os.path.isfile(furmarkLog):
        print("input file is not exists")
        return

    with open(furmarkLog, "r") as f:
        line = f.readlines()
        for i in line:
            score=re.findall("Score=\d+", i)
            for j in score:
                li.append(re.findall(r"\d+\.?\d*",j))

    return write2excel(dstFile, "sheet1", [data[0], data[1], float(li[-1][0])])
