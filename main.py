import argparse
import os.path
from pdb import runcall
import sys

from control.get_Furmark_score import get_txt_score
from control.get_heaven_score import get_html_score
from control.get_3dmark_score import get_3dmark_score
from control.get_3dmark_score import get_3dmark11_score
from control.get_pm_log import csv2excel
from util import common

def _prepare_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a","--application",help="application_mode;The value must in ['TimeSpy_Score','TimeSpy_FPS', 'Furmark', 'Heaven', 'FireStrike','3dmark11']")
    parser.add_argument("-m","--mode",required=True,help="config_mode;he value must in ['AC + HG', 'DC + HG', 'AC + NoHG', 'DC + NoHG']")
    parser.add_argument("-fps",action='store_true',help="run TimeSpy_FPS but not TimeSpy")
    parser.add_argument("-pm","--pm_log",help="path of pm_log.csv")
    parser.add_argument("-d","--destination_path",default=r"C:\Users\gvle\tmp")
    return parser.parse_args()

def collect_log(srcPath,workPath,app,mode):
    '''
    :param srcPath:
    :param app:
    :param mode:
    :return:
    '''
    print(f"!!!Begin collect {app} log")
    common.get_src_log(srcPath,workPath,app)
    if workPath:
        resultXls = os.path.join(workPath, "result.xls")
    else:
        # TODO when one app dosn't match the condition,The script should exit or skip the app?
        print(f"There are not correct log in  {srcPath} .please run your app!")
        return
    if app == "Heaven":
        get_html_score(workPath,resultXls,[mode,app])
        # csv2excel(pm_log, "", [app,mode])
        print("数据生成在", resultXls)
    elif app == "FurMark":
        get_txt_score(workPath,resultXls,[mode,app])
        print("数据生成在", resultXls)
    elif app in ["TimeSpy","TimeSpy_FPS", "FireStrike"]:
        get_3dmark_score(workPath,resultXls,[mode,app])
        print("数据生成在", resultXls)

if __name__ == '__main__':
    """
    :param
        1.log path
        2. destination excel file path
        3.data (data[0] must in ["AC + HG", "DC + HG", "AC + NoHG", "DC + NoHG"]
                data[1] must in [["TimeSpy", "FurMark", "Heaven", "FireStrike","3dmark11"]])
    """
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
    # if not os.path.exists(dstPath):
    #     os.mkdir(dstPath)
    #
    # if mode not in modeAll:
    #     raise Exception(f"parameter error!The mode should in {modeAll}")
    #
    # if app:
    #     appLis = app.split(",")
    #     if not set(appLis).issubset(set(appAll)) :
    #         raise Exception(f"parameter error! The app should in {appAll}")
    #     else:
    #         for a in appLis:
    #             if a in logDirDict:
    #                 collect_log(logDirDict[a],dstPath, a, mode)
    # # default:all application log will be collected.
    # else:
    #     print("run all app!")
    #     if (args_.fps):
    #         for key in logDirDictFps.keys():
    #             collect_log(logDirDictFps[key],dstPath,key, mode)
    #     else:
    #         for key in logDirDict.keys():
    #             collect_log(logDirDict[key],dstPath,key, mode)

    # 读取pmlog
    srcPmLog=args_.pm_log
    csv_path=common.seek_file(srcPmLog,dstPath,"pm_log.csv")
    excel_path=os.path.join(dstPath,"pm_log.xls")
    data=["TimeSpy_Score","AC + HG"]
    csv2excel(csv_path,excel_path,mode)
    # # csv_excel(csv_path,excel_path)






