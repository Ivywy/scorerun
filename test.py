import os
import re

# def get_3dmark_log(rootDir ,dstPath, app):
#     '''
#     :param rootDir: Log path where generated directory
#     :param dstPath: The destination path from the rootDir copy
#     :param app:application
#     :return:
#     '''
#     continue_=False
#     # 找到.3dmark-result结尾并包含TimeSpy的日志
#     fileList = list()
#     if app == "TimeSpy":
#         fileList =[f for f in os.listdir(rootDir) if os.path.isfile(os.path.join(rootDir ,f)) and f.endswith('.3dmark-result') and f.__contains__
#                         ("TimeSpyExtremeCustom") and not f.__contains__("FAILED")]
#     elif app == "TimeSpy_FPS":
#         fileList =[f for f in os.listdir(rootDir) if os.path.isfile(os.path.join(rootDir ,f)) and f.endswith('.3dmark-result') and f.__contains__
#                         ("TimeSpyExtremeCustom") and not f.__contains__("FAILED")]
#     elif app == "FireStrike":
#         fileList =[f for f in os.listdir(rootDir) if os.path.isfile(os.path.join(rootDir ,f)) and f.endswith('.3dmark-result') and f.__contains__
#                         ("FireStrikeCustom") and not f.__contains__("FAILED")]
#
#     # 去掉含old字符的文件
#     seletedFiles = list(filter(lambda x: 'old' not in x, fileList))
#
#     # 正则取出日志名字的时间戳
#     logs = list()
#     for log in seletedFiles:
#         logs.append(int(re.compile(r'2022\d+').findall(log)[0]))
#
#     if len(logs) != 0:
#         # it means have more than one log file,so compare to get the newest log file
#         lastlog = heapq.nlargest(1, logs)
#         for file in seletedFiles:
#             if file.__contains__(str(lastlog[0])):
#                 dstPath =common.copyfile(os.path.join(rootDir, file), dstPath)
#                 continue_ = True
#                 common.changeName(os.path.join(rootDir, file))
#                 break
#     else:
#         print("{app} no log generated!!!!")
#
#
#     if continue_==False:
#         print("\033[0;31;40m", "No matched logs were found of {app},please press enter to continue or esc to exit", "\033[0m")
#
#     return dstPath

# workPath=r"C:\Users\gvle\tmp"
#
#
# resultXls = os.path.join(workPath, "result111.xls")

# rootDir=r"C:\Users\gvle\AppData\Local\Temp"
# fileList=[f for f in os.listdir(rootDir) if f.endswith("heaven4_1080p") and not f.__contains__("old")]
# print(fileList)

# def get_pm_key(app):
#     print("app1",app)
#     if app == "TimeSpy" or app == "TimeSpy_FPS":
#         return "timespy_extreme_ppa"
#     elif app == "FireStrike":
#         return "firestrike_ppa"
#     elif app == "Heaven":
#         return "heaven4_1080p"
#     elif app == "FurMark":
#         return "furmark_benchmark_4k"
#     else:
#         print(f'appname error,{app} should in ["TimeSpy", "TimeSpy_FPS","FurMark", "Heaven", "FireStrike","3dmark11"]')
#         return
#
# app="Heaven"
# print(get_pm_key(app))

# regex = re.compile(r'\d+.*-\d')
# file="Results_2022-09-14-05-11-59_heaven4_1080p"
# print("reg=",regex.findall(file))
# # file_num = int(regex.findall(file)[0].replace("-",""))
a=1
b=3
print(f"\033[0;32;40m{a}'s pmlog has been collected in {b} successfully!\033[0m")
print(f"\033[0;34;40m######Begin collect {a} log######\033[0m")