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
from util.logger_util import log_info, log_error, log_critical


def _prepare_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a","--application",help="application_mode;The value must in ['TimeSpy','TimeSpy_FPS', 'Furmark', 'Heaven', 'FireStrike','3dmark11']")
    parser.add_argument("-m","--mode",required=True,help="config_mode;The value must in ['AC+HG', 'DC+HG', 'AC+NoHG', 'DC+NoHG']")
    parser.add_argument("-d","--destination_path",default=r"C:\Users\gvle\tmp")
    return parser.parse_args()

def collect_log(srcPath,workPath,app,mode):
    '''
    :param srcPath:
    :param app:
    :param mode:
    :return:
    '''

    log_info(f"++++++++++Begin collect {app} performance log++++++++++++++++")
    if not os.path.exists(srcPath):
        log_critical(f"{srcPath} is not exist, maybe you run a error env")

    if not os.path.exists(workPath):
        os.makedirs(workPath)

    resultXls = os.path.join(workPath, "result.xls")

    if app == "Heaven":
        workPath=get_Heaven_log(srcPath,workPath)
        if workPath:
            get_Heaven_score(workPath,resultXls,[mode,app])
        else:
            log_error(f"{app} log not found!")

    elif app == "FurMark":
        workPath=get_FurMark_log(srcPath,workPath)
        if workPath:
            get_FurMark_score(workPath,resultXls,[mode,app])
        else:
            log_error(f"{app} log not found!")

    elif app in ["TimeSpy","TimeSpy_FPS", "FireStrike"]:
        workPath=get_3dmark_log(srcPath,workPath,app)
        if workPath:
            get_3dmark_score(workPath,resultXls,[mode,app])
        else:
            log_error(f"{app} log not found!")


    log_info(f"+++++++++++++Begin collect {app} pm log++++++++++++++++++++")
    pmLogSrcPath = r"C:\Users\gvle\AppData\Local\Temp"
    collect_pm_log(pmLogSrcPath, dstPath, [app, mode])

if __name__ == '__main__':
    """
    :param
        1.log path
        2. destination excel file path
        3.data (data[0] must in ["AC+HG", "DC+HG", "AC+NoHG", "DC+NoHG"]
                data[1] must in [["TimeSpy", "FurMark", "Heaven", "FireStrike","3dmark11"]])
    """
    # src log path
    markPath=r"C:\Users\gvle\Documents\3DMark"
    logDirDict={"TimeSpy":markPath,"TimeSpy_FPS":markPath,"FurMark":r"C:\Program Files (x86)\Geeks3D\Benchmarks\FurMark","Heaven":r"C:\Users\gvle\Heaven","FireStrike":markPath}

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
        log_info("will collect all applications' logs!")
        for key in logDirDict.keys():
            collect_log(logDirDict[key],dstPath,key, mode)




