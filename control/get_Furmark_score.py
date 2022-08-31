import re

from util.perf_to_excel import write2excel


def get_txt_score(inputpath,dstFile,data):
    li = list()
    with open(inputpath, "r") as f:
        line = f.readlines()
        for i in line:
            score=re.findall("Score=\d+", i)    # ['Score=505']
            for j in score:
                li.append(re.findall(r"\d+\.?\d*",j))   # [['505']]

    return write2excel(dstFile, "sheet1", [data[0], data[1], float(li[0][0])])
