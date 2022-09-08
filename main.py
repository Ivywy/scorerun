import argparse
import os.path
import sys

from control.get_Furmark_score import get_txt_score
from control.get_heaven_score import get_html_score
from control.get_3dmark_score import get_3dmark_score
from control.get_3dmark_score import get_3dmark11_score
from control.get_pm_log import csv2excel
from util import common






def _prepare_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a","--application",help="application_mode;The value must in ['TimeSpy_Score','TimeSpy_FPS', 'Furmark', 'Heaven11', 'FireStrike','3dmark11']")
    parser.add_argument("-m","--mode",help="config_mode;he value must in ['AC + HG', 'DC + HG', 'AC + NoHG', 'DC + NoHG']")
    return parser.parse_args()

def get_score(src_log,pm_log):
    args_=_prepare_args()
    app= args_.application
    mode = args_.mode
    dst_file=""
    excel_path=""
    if app not in ["TimeSpy_Score","TimeSpy_FPS", "Furmark", "Heaven11", "FireStrike","3dmark11"]:
        raise Exception("parameter error!")
    if mode not in ["AC + HG", "DC + HG", "AC + NoHG", "DC + NoHG"]:
        raise Exception("parameter error!")

    if app == "Heaven11":
        get_html_score(src_log,dst_file,[mode,app])
        csv2excel(pm_log, excel_path, [app,mode])
    elif app == "Furmark":
        get_txt_score(src_log,dst_file,[mode,app])
    elif app in ["TimeSpy_Score","TimeSpy_FPS", "FireStrike"]:
        get_3dmark_score(src_log,dst_file,[mode,app])
    else:
        raise Exception("parameter error!")

if __name__ == '__main__':
    """
    :param
        1.log path
        2. destination excel file path
        3.data (data[0] must in ["AC + HG", "DC + HG", "AC + NoHG", "DC + NoHG"]
                data[1] must in [["TimeSpy_Score","TimeSpy_FPS", "Furmark", "Heaven11", "FireStrike","3dmark11"]])
    """
    # dstFile=os.path.join("data","result_{}.xls".format(common.get_time()))

    # # 读取heaven11的log
    # get_html_score(os.path.join("data","Heaven11"),dstFile,["AC + HG", "Heaven11"])
    #
    # 读取Furmark的log
    # get_txt_score(os.path.join("data","Furmark","FurMark-Scores.txt"),dstFile,["DC + HG", 'Furmark'])

    # # 读取TimeSpy(GT1+GT2)的log
    # get_3dmark_score(os.path.join("data","TimeSpy",),dstFile,["AC + HG", 'TimeSpy_Score'])
    # # 读取TimeSpy(GT1+GT2)的log
    # get_3dmark_score(os.path.join("data", "TimeSpy", ), dstFile, ["AC + HG", 'TimeSpy_FPS'])
    #
    # # 读取FireStrike的log
    # get_3dmark_score(os.path.join("data", "FireStrike", ), dstFile, ["AC + HG", 'FireStrike'])
    #
    # # TODO 读取3dmark11的数据
    # # get_3dmark11_score(os.path.join("data", "3dmark11", ), dstFile, ["AC + HG", '3dmark11'])
    #
    # # 读取pmlog
    # data_path=os.path.join("data","pmlog")
    # csv_path=os.path.join(data_path,"pm_log.csv")
    # excel_path=os.path.join(data_path,"pm_log.xls")
    # mode=["TimeSpy_Score","AC + HG"]
    # csv2excel(csv_path,excel_path,mode)
    # # csv_excel(csv_path,excel_path)

    # get_score()





