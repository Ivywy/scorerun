import os
import sys
import time
import win32file as pywin32
import shutil
import re
from pathlib import Path
from bs4 import BeautifulSoup
import keyboard


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
	'''
	:param rootDir: Log path where generated directory
	:param dstPath: The destination path from the rootDir copy
	:param app:application
	:return:
	'''
	continue_=False
	# 找到不含old关键字的文件
	fileList=[f for f in os.listdir(rootDir) if os.path.isfile(os.path.join(rootDir,f)) and f.endswith(('.3dmark-result','.html','.txt'))]

	# 获取每个app生成的log中含有的可唯一识别该app的关键字
	keyword=get_key(app)

	if len(fileList)!=0:
		# 判断不含old字符的文件数量
		seletedFiles=list(filter(lambda x: 'old' not in x, fileList))
		# 当有不含old字的文件存在且只含有1个或2个时，进入判断：
		if len(seletedFiles) == 1 or len(seletedFiles) == 2:
			generateFiles = []
			for file in seletedFiles:
				if file.__contains__(keyword):
					generateFiles.append(file)

			# 与app相匹配的log只有一个时，符合提取要求
			if len(generateFiles)==1:
				# copy log到指定目录
				copyfile(os.path.join(rootDir, generateFiles[0]), dstPath)
				if os.path.exists(os.path.join(dstPath, generateFiles[0])) == False:
					raise Exception(f"File {generateFiles[0]} copy Failed!")
				continue_ = True
				changeName(os.path.join(rootDir, generateFiles[0]))

			# 当 app为Heaven11时，有可能会生成两个log，只取内容含有total score的那个log即可
			elif len(generateFiles)==2:
				if keyword == "Heaven":
						# 判断文件是否包含total关键字
						for file in generateFiles:
							if read_heaven_log(os.path.join(rootDir, file)) != None:
								# copy log到指定目录
								copyfile(os.path.join(rootDir, file), dstPath)
								if os.path.exists(os.path.join(dstPath, file)) == False:
									raise Exception(f"File {file} copy Failed!")
								continue_ = True
								break
						for file in generateFiles:
							changeName(os.path.join(rootDir, file))

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

