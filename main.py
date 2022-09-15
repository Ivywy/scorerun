import argparse
import datetime
import os.path
import re
from pdb import runcall
import sys

from control.get_Furmark_score import get_FurMark_score, get_FurMark_log
from control.get_heaven_score import get_Heaven_score, get_Heaven_log
from control.get_3dmark_score import get_3dmark_score, get_3dmark_log
from control.get_3dmark_score import get_3dmark11_score
from control.get_pm_log import csv2excel, seek_latest_log, collect_pm_log
from util import common

def _prepare_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a","--application",help="application_mode;The value must in ['TimeSpy_Score','TimeSpy_FPS', 'Furmark', 'Heaven', 'FireStrike','3dmark11']")
    parser.add_argument("-m","--mode",required=True,help="config_mode;The value must in ['AC + HG', 'DC + HG', 'AC + NoHG', 'DC + NoHG']")
    parser.add_argument("-fps",action='store_true',help="run TimeSpy_FPS but not TimeSpy")
    parser.add_argument("-d","--destination_path",default=r"C:\Users\gvle\tmp")
    return parser.parse_args()

def collect_log(srcPath,workPath,app,mode):
    '''
    :param srcPath:
    :param app:
    :param mode:
    :return:
    '''

    print(f"\033[0;34;40m######Begin collect {app} performance log######\033[0m")
    if not os.path.exists(srcPath):
        raise Exception(f"{srcPath} is not exist, maybe you run a error env")

    if not os.path.exists(workPath):
        os.makedirs(workPath)

    resultXls = os.path.join(workPath, "result.xls")

    if app == "Heaven":
        workPath=get_Heaven_log(srcPath,workPath)
        if workPath:
            get_Heaven_score(workPath,resultXls,[mode,app])
        else:
            print(f"{app} log not found!")
            return
            # csv2excel(pm_log, "", [app,mode])
        print("Date has been saved in ", resultXls)
    elif app == "FurMark":
        workPath=get_FurMark_log(srcPath,workPath)
        if workPath:
            get_FurMark_score(workPath,resultXls,[mode,app])
        else:
            print(f"{app} log not found!")
            return
        print("Date has been saved in", resultXls)
    elif app in ["TimeSpy","TimeSpy_FPS", "FireStrike"]:
        workPath=get_3dmark_log(srcPath,workPath,app)
        if workPath:
            get_3dmark_score(workPath,resultXls,[mode,app])
        else:
            print(f"{app} log not found!")
            return
        print("Date has been saved in", resultXls)

    print(f"\033[0;34;40m######Begin collect {app} pm log######\033[0m")
    pmLogSrcPath = r"C:\Users\gvle\AppData\Local\Temp"
    collect_pm_log(pmLogSrcPath, dstPath, [app, mode])

if __name__ == '__main__':
    """
    :param
        1.log path
        2. destination excel file path
        3.data (data[0] must in ["AC + HG", "DC + HG", "AC + NoHG", "DC + NoHG"]
                data[1] must in [["TimeSpy", "FurMark", "Heaven", "FireStrike","3dmark11"]])
    """
    # src log path
    markPath=r"C:\Users\gvle\Documents\3DMark"
    logDirDict={"TimeSpy":markPath,"FurMark":r"C:\Program Files (x86)\Geeks3D\Benchmarks\FurMark","Heaven":r"C:\Users\gvle\Heaven","FireStrike":markPath}
    logDirDictFps={"TimeSpy_FPS":markPath,"FurMark":r"C:\Program Files (x86)\Geeks3D\Benchmarks\FurMark","Heaven":r"C:\Users\gvle\Heaven","FireStrike":markPath}

    args_=_prepare_args()
    dstPath=args_.destination_path
    mode = args_.mode
    app = args_.application
    appAll=["TimeSpy", "FurMark", "Heaven", "FireStrike","3dmark11"]
    modeAll=["AC+HG", "DC+HG", "AC+NoHG", "DC+NoHG"]
    # dstPath = os.path.join(os.path.abspath(os.path.join(os.getcwd(), "..")), "tmp", mode + '-' + common.get_time())
    if not os.path.exists(dstPath):
        os.makedirs(dstPath)
    
    if mode not in modeAll:
        raise Exception(f"parameter error!The mode should in {modeAll}")
    
    if app:
        appLis = app.split(",")
        if not set(appLis).issubset(set(appAll)) :
            raise Exception(f"parameter error! The app should in {appAll}")
        else:
            for a in appLis:
                if a in logDirDict:
                    collect_log(logDirDict[a],dstPath, a, mode)
    # default:all application log will be collected.
    else:
        print("will collect all applications' logs!")
        # if fps==True,run TimeSpy_FPS,else run TimeSpy
        if (args_.fps):
            for key in logDirDictFps.keys():
                collect_log(logDirDictFps[key],dstPath,key, mode)
        else:
            for key in logDirDict.keys():
                collect_log(logDirDict[key],dstPath,key, mode)




