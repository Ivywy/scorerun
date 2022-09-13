import os
import time
import win32file as pywin32
import shutil
import re
from pathlib import Path
from bs4 import BeautifulSoup


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

def is_used(file_name):
	try:
		vHandle = pywin32.CreateFile(file_name, pywin32.GENERIC_READ, 0, None, pywin32.OPEN_EXISTING, pywin32.FILE_ATTRIBUTE_NORMAL, None)
		return int(vHandle) == pywin32.INVALID_HANDLE_VALUE
	except:
		return True
	finally:
		try:
			pywin32.CloseHandle(vHandle)
		except:
			pass

'''
	rootDir:APP跑的日志存放路径
	dstPath:收集日志路径
	app:运行的APP名字
	mode:测试的不同模式
'''
def get_src_log(rootDir,dstPath,app):
	'''
	:param rootDir: Log path where generated directory
	:param dstPath: The destination path from the rootDir copy
	:param app:application
	:return:
	'''
	continue_=False
	# if not os.path.exists(dstPath):
	# 	os.makedirs(dstPath)
	# print("make new dir:",dstPath)
	fileList=[f for f in os.listdir(rootDir) if os.path.isfile(os.path.join(rootDir,f)) and f.endswith(('.3dmark-result','.html','.txt'))]
	# print(fileList)
	if len(fileList)!=0:
		# 判断不含old字符的文件数量
		seletedFiles=list(filter(lambda x: 'old' not in x, fileList))
		#print(f"{seletedFiles} not contained the 'old' ")
		if len(seletedFiles)==0:
			pass
		elif len(seletedFiles)==1:
			keywords="TimeSpy,Heaven11,Furmark,FireStrike"
			if any([w in app and w for w in keywords.split(',')]): # 判断app是否包含这些关键字
				# dstPath=os.path.join(dstPath,mode+'-'+get_time())
				# copy log到指定目录
				print("+++",os.path.join(rootDir,seletedFiles[0]))
				print("++++++++",dstPath)
				copyfile(os.path.join(rootDir,seletedFiles[0]),dstPath)
				if os.path.exists(os.path.join(dstPath,seletedFiles[0])) == False:
					raise Exception(f"File {seletedFiles[0]} copy Failed!")
				continue_=True
				# 将文件重新命名
				oldFile=changeName(os.path.join(rootDir,seletedFiles[0]))
				if os.path.exists(oldFile) == False:
					raise Exception("change file name failed!")
		elif len(seletedFiles)==2:
			if app.__contains__("Heaven11"):
				# 判断文件是否包含total关键字
				# dstPath = os.path.join(dstPath, mode+'-'+get_time())
				for file in seletedFiles:
					if read_heaven_log(os.path.join(rootDir, file)) != None:
						# copy log到指定目录
						copyfile(os.path.join(rootDir,file), dstPath)
						if os.path.exists(os.path.join(dstPath, file)) == False:
							raise Exception(f"File {file} copy Failed!")
						continue_=True
						break

				for file in seletedFiles:
					# 将文件重新命名
					oldFile = changeName(os.path.join(rootDir,file))
					if os.path.exists(oldFile) == False:
						raise Exception("change file name failed!")

		else:
			for file in seletedFiles:
				# 将文件重新命名
				oldFile = changeName(os.path.join(rootDir,file))
				if os.path.exists(oldFile) == False:
					raise Exception("change file name failed!")

	if continue_==False:
		#print("Please Rerun Testcase !")
		return None
	else:
		return dstPath
		



def copyfile(srcfile,dstpath):
	if not os.path.isfile(srcfile):
		print ("%s not exist!"%(srcfile))
	else:
		fpath,fname=os.path.split(srcfile)
		if not os.path.exists(dstpath):
			os.makedirs(dstpath)
		shutil.copy(srcfile, dstpath)
		print ("copy %s -> %s"%(srcfile, os.path.join(dstpath,srcfile)))


def changeName(beforeFile):
	index = beforeFile.find('.')
	finalFile = beforeFile[:index] + '_old' + beforeFile[index:]
	print(finalFile)
	os.rename(beforeFile,finalFile)
	return finalFile