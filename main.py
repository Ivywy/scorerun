import os.path

from control.get_Furmark_score import get_txt_score
from control.get_heaven_score import get_html_score
from control.get_3dmark_score import get_3dmark_score

if __name__ == '__main__':
    dstFile=os.path.join("data","result.xls")
    # 读取heaven11的log
    get_html_score(os.path.join("data","Heaven11"),os.path.join("data","result.xls"))

    # 读取Furmark的log
    get_txt_score(os.path.join("data","Furmark","FurMark-Scores.txt"),dstFile,["AC + HG", 'Furmark'])

    # 读取TimeSpy的log
    get_3dmark_score(os.path.join("data","TimeSpy",),dstFile,["AC + HG", 'TimeSpy'])

    # 读取FireStrike的log
    get_3dmark_score(os.path.join("data", "FireStrike", ), dstFile, ["AC + HG", 'FireStrike'])

    # 读取3dmark11的数据




