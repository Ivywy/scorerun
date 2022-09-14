import os


def get_3dmark_log(rootDir ,dstPath, app):
    '''
    :param rootDir: Log path where generated directory
    :param dstPath: The destination path from the rootDir copy
    :param app:application
    :return:
    '''
    continue_=False
    # 找到.3dmark-result结尾并包含TimeSpy的日志
    fileList = list()
    if app == "TimeSpy":
        fileList =[f for f in os.listdir(rootDir) if os.path.isfile(os.path.join(rootDir ,f)) and f.endswith('.3dmark-result') and f.__contains__
                        ("TimeSpyExtremeCustom") and not f.__contains__("FAILED")]
    elif app == "TimeSpy_FPS":
        fileList =[f for f in os.listdir(rootDir) if os.path.isfile(os.path.join(rootDir ,f)) and f.endswith('.3dmark-result') and f.__contains__
                        ("TimeSpyExtremeCustom") and not f.__contains__("FAILED")]
    elif app == "FireStrike":
        fileList =[f for f in os.listdir(rootDir) if os.path.isfile(os.path.join(rootDir ,f)) and f.endswith('.3dmark-result') and f.__contains__
                        ("FireStrikeCustom") and not f.__contains__("FAILED")]

    # 去掉含old字符的文件
    seletedFiles = list(filter(lambda x: 'old' not in x, fileList))

    # 正则取出日志名字的时间戳
    logs = list()
    for log in seletedFiles:
        logs.append(int(re.compile(r'2022\d+').findall(log)[0]))

    if len(logs) != 0:
        # it means have more than one log file,so compare to get the newest log file
        lastlog = heapq.nlargest(1, logs)
        for file in seletedFiles:
            if file.__contains__(str(lastlog[0])):
                dstPath =common.copyfile(os.path.join(rootDir, file), dstPath)
                continue_ = True
                common.changeName(os.path.join(rootDir, file))
                break
    else:
        print("{app} no log generated!!!!")


    if continue_==False:
        print("\033[0;31;40m", "No matched logs were found of {app},please press enter to continue or esc to exit", "\033[0m")

    return dstPath