import os
import re
from util import common
from util.perf_to_excel import write2excel

def get_FurMark_log(rootDir,dstPath):
    '''
    :param rootDir: Log path where generated directory
    :param dstPath: The destination path from the rootDir copy
    :return:
    '''
    selectFile=""
    if os.listdir(rootDir):
        for file in os.listdir(rootDir):
            if file=="FurMark-Scores.txt":
                selectFile=file
                break
        dstPath = common.copyfile(os.path.join(rootDir, selectFile), dstPath)
        return dstPath

    else:
        print("\033[0;31;40m", f"No matched logs were found of furMark in {rootDir},Please check!","\033[0m")
        return

    # # 找出所有含有furmark的txt文件
    # fileList=[f for f in os.listdir(rootDir) if os.path.isfile(os.path.join(rootDir,f)) and f.endswith('.txt') and f.__contains__("FurMark-Scores")]
    #
    # # 去掉含old字符的文件
    # seletedFiles=list(filter(lambda x: 'old' not in x, fileList))
    #
    # # furmark的文件只能有一个
    # if len(seletedFiles) == 1:
    #     dstPath=common.copyfile(os.path.join(rootDir, seletedFiles[0]), dstPath)
    #     continue_ = True
    #     common.changeName(os.path.join(rootDir, seletedFiles[0]))
    # else:
    #     # 将文件重新命名
    #     for file in seletedFiles:
    #         common.changeName(os.path.join(rootDir, file))
    #     print("FurMark no log generated!!!!")
    #
    # if continue_==False:
    #     print("\033[0;31;40m", "No matched logs were found of {app},please press enter to continue or esc to exit", "\033[0m")
    #
    # return dstPath

def get_FurMark_score(srcPath,dstFile,data):
    # TODO posite FurMark log
    li = list()

    if not os.path.isfile(srcPath):
        print("input file is not exists")
        return

    with open(srcPath, "r") as f:
        line = f.readlines()
        for i in line:
            score=re.findall("Score=\d+", i)
            for j in score:
                li.append(re.findall(r"\d+\.?\d*",j))

    return write2excel(dstFile, "sheet1", [data[0], data[1], float(li[-1][0])])
