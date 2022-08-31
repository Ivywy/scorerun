import os.path

from control.get_Furmark_score import get_txt_score
from control.get_heaven_score import get_html_score
from control.get_3dmark_score import get_3dmark_score
from control.get_3dmark_score import get_3dmark11_score
from control.get_pm_log import csv2excel
from util import common

if __name__ == '__main__':
    """
    :param
        1.log path
        2. destination excel file path
        3.data (data[0] must in ["AC + HG", "DC + HG", "AC + NoHG", "DC + NoHG"]
                data[1] must in [["TimeSpy_Score","TimeSpy_FPS", "Furmark", "Heaven11", "FireStrike","3dmark11"]])
    """
    dstFile=os.path.join("data","result_{}.xls".format(common.get_time()))

    # 读取heaven11的log
    get_html_score(os.path.join("data","Heaven11"),dstFile,["AC + HG", "Heaven11"])

    # 读取Furmark的log
    get_txt_score(os.path.join("data","Furmark","FurMark-Scores.txt"),dstFile,["DC + HG", 'Furmark'])

    # 读取TimeSpy(GT1+GT2)的log
    get_3dmark_score(os.path.join("data","TimeSpy",),dstFile,["AC + HG", 'TimeSpy_Score'])
    # 读取TimeSpy(GT1+GT2)的log
    get_3dmark_score(os.path.join("data", "TimeSpy", ), dstFile, ["AC + HG", 'TimeSpy_FPS'])

    # 读取FireStrike的log
    get_3dmark_score(os.path.join("data", "FireStrike", ), dstFile, ["AC + HG", 'FireStrike'])

    # TODO 读取3dmark11的数据
    # get_3dmark11_score(os.path.join("data", "3dmark11", ), dstFile, ["AC + HG", '3dmark11'])

    # 读取pmlog
    data_path=os.path.join("data","pmlog")
    csv_path=os.path.join(data_path,"pm_log.csv")
    excel_path=os.path.join(data_path,"pm_log.xls")
    mode=["TimeSpy_Score","AC + HG"]
    csv2excel(csv_path,excel_path,mode)
    # csv_excel(csv_path,excel_path)




