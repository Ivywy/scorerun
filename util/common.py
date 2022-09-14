import os
import sys
import time
import win32file as pywin32
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
def read_heaven_log(file_path):
    print(file_path)
    doc = open(file_path, 'r', encoding='utf-8').read()
    soup = BeautifulSoup(doc, "html.parser")
    total=soup.findAll(text=re.compile('.*?Total.*?'))
    if len(total):
        s = ""
        # dic = {}
        for str in total:
            if str.find("Total scores") != -1:
                s = str.split("Total scores: ")[1]
                break

        return float(s)
    else:
        print("There are no keyword 'total' in file {}".format(file_path))
        return None


def get_key(app):
	if "TimeSpy" in app:
		return "TimeSpy"
	elif "Heaven" in app:
		return "heaven"
	else:
		return app

def get_src_log(rootDir,dstPath,app):
	if app == "TimeSpy" or "TimeSpyFPS" or "FireStrike":
		get_3dmark_log(rootDir,dstPath, app)
	elif app == "Heaven":
		get_heaven_log(rootDir,dstPath)
	elif app == "FurMark":
		get_furmark_log(rootDir,dstPath)
	else:
		# TODO
		# 还有3dmark11的日志
		pass

def get_3dmark_log(rootDir,dstPath, app):
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
		fileList=[f for f in os.listdir(rootDir) if os.path.isfile(os.path.join(rootDir,f)) and f.endswith('.3dmark-result') and f.__contains__("TimeSpy")]
	elif app == "TimeSpy_FPS":
		fileList=[f for f in os.listdir(rootDir) if os.path.isfile(os.path.join(rootDir,f)) and f.endswith('.3dmark-result') and f.__contains__("TimeSpyFPS")]
	elif app == "FireStrike":
		fileList=[f for f in os.listdir(rootDir) if os.path.isfile(os.path.join(rootDir,f)) and f.endswith('.3dmark-result') and f.__contains__("FireStrike")]

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
				copyfile(os.path.join(rootDir, file), dstPath)
				continue_ = True
				changeName(os.path.join(rootDir, file))
				break
	else:
		# 将文件重新命名
		for file in seletedFiles:
			changeName(os.path.join(rootDir, file))

	if continue_==False:
		print("\033[0;31;40m", "No matched logs were found of {app},please press enter to continue or esc to exit", "\033[0m")

def get_heaven_log(rootDir,dstPath):
	'''
	:param rootDir: Log path where generated directory
	:param dstPath: The destination path from the rootDir copy
	:return:
	'''
	continue_=False
	# 找出所有含有heaven的html文件
	fileList=[f for f in os.listdir(rootDir) if os.path.isfile(os.path.join(rootDir,f)) and f.endswith('.html') and f.__contains__("heaven")]

	# 去掉含old字符的文件
	seletedFiles=list(filter(lambda x: 'old' not in x, fileList))

	logs = list()
	for log in seletedFiles:
		logs.append(int(re.compile(r'2022\d+').findall(log)[0]))

	dic = dict(zip(logs, seletedFiles))

	if len(logs) != 0:
		# it means have more than one log file,so compare to get the newest log file
		loglist = heapq.nlargest(len(logs), logs)
		for fileNum in loglist:
			heavenlog = os.path.join(rootDir, dic[fileNum])
			if read_heaven_log(heavenlog) != None:
				# copy log到指定目录
				copyfile(heavenlog, dstPath)
				if os.path.exists(heavenlog) == False:
					raise Exception(f"File {heavenlog} copy Failed!")
				continue_ = True
				break
	
		for file in seletedFiles:
			changeName(os.path.join(rootDir, file))
	else:
		# 将文件重新命名
		for file in seletedFiles:
			changeName(os.path.join(rootDir, file))

	if continue_==False:
		print("\033[0;31;40m", "No matched logs were found of {app},please press enter to continue or esc to exit", "\033[0m")

def get_furmark_log(rootDir,dstPath):
	'''
	:param rootDir: Log path where generated directory
	:param dstPath: The destination path from the rootDir copy
	:return:
	'''
	continue_=False

	# 找出所有含有furmark的txt文件
	fileList=[f for f in os.listdir(rootDir) if os.path.isfile(os.path.join(rootDir,f)) and f.endswith('.txt') and f.__contains__("FurMark-Scores")]

	# 去掉含old字符的文件
	seletedFiles=list(filter(lambda x: 'old' not in x, fileList))

	# furmark的文件只能有一个
	if len(seletedFiles) == 1:
		copyfile(os.path.join(rootDir, seletedFiles[0]), dstPath)
		continue_ = True
		changeName(os.path.join(rootDir, seletedFiles[0]))
	else:
		# 将文件重新命名
		for file in seletedFiles:
			changeName(os.path.join(rootDir, file))

	if continue_==False:
		print("\033[0;31;40m", "No matched logs were found of {app},please press enter to continue or esc to exit", "\033[0m")



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

