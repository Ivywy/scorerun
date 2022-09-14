import os
import sys
import time
import shutil
import re
from pathlib import Path
from bs4 import BeautifulSoup
import keyboard
import heapq


def mk_dir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print("---  create new folder success...  ---")
    else:
        print ("---  There is this folder!  --")

def get_time():
    return time.strftime('%Y%m%d%H%M%S', time.localtime())

# read file content



def get_key(app):
	if "TimeSpy" in app:
		return "TimeSpy"
	elif "Heaven" in app:
		return "heaven"
	else:
		return app

# def get_src_log(rootDir,dstPath,app):
# 	if app == "TimeSpy" or "TimeSpy_FPS" or "FireStrike":
# 		get_3dmark_log(rootDir,dstPath, app)
# 	elif app == "Heaven":
# 		get_heaven_log(rootDir,dstPath)
# 	elif app == "FurMark":
# 		get_furmark_log(rootDir,dstPath)
# 	else:
# 		# TODO
# 		# 还有3dmark11的日志
# 		pass


def copyfile(srcfile,dstpath):
	if not os.path.isfile(srcfile):
		print ("%s not exist!"%(srcfile))
	else:
		fpath,fname=os.path.split(srcfile)
		if not os.path.exists(dstpath):
			os.makedirs(dstpath)
		shutil.copy(srcfile, dstpath)
		print ("copy %s -> %s"%(srcfile, os.path.join(dstpath,fname)))
		return os.path.join(dstpath,fname)

def changeName(beforeFile):
	finalFile=""
	if beforeFile.__contains__("."):
		index = beforeFile.find('.')
		finalFile = beforeFile[:index] + '_old' + beforeFile[index:]
	else:
		finalFile=beforeFile+'_old'
	if os.path.isfile(finalFile):
		os.remove(finalFile)
	os.rename(beforeFile,finalFile)
	if os.path.exists(finalFile) == False:
		raise Exception("change file name failed!")

def seek_file(rootDir,dstPath):
	file="pm_log.csv"
	if rootDir == None:
		return
	for root, dirs, files in os.walk(rootDir):
		if file in files:
			filePath='{0}/{1}'.format(root, file)
			finalPath=copyfile(filePath,dstPath)
			changeName(filePath)
			return finalPath

def get_pm_key(app):
	if app=="TimeSpy" or "TimeSpy_FPS":
		return "timespy_extreme_ppa"
	elif app=="FireStrike":
		return "firestrike_ppa"
	elif app=="Heaven":
		return "heaven4_1080p"
	elif app=="FurMark":
		return "furmark_benchmark_4k"

