import os
import time
import win32file as pywin32
import shutil


def mk_dir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print("---  create new folder success...  ---")
    else:
        print ("---  There is this folder!  --")

def get_time():
    return time.strftime('%Y%m%d%H%M%S', time.localtime())

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

def get_src_log(rootDir,dstPath,app,mode):
	fileList=os.listdir(rootDir)
	flag=False
	if len(fileList)!=0:
		# 判断不含old字符的文件数量
		fileNew=list(filter(lambda x: 'old' not in x, fileList))
		print("fileNew,",fileNew)
		if len(fileNew)==0:
			flag=True
		elif len(fileNew)==1:
			keywords="TimeSpy,Heaven11,Furmark,FireStrike"
			if any([w in app and w for w in keywords.split(',')]): # 判断app是否包含这些关键字
				dstPath=os.path.join(dstPath,mode)
				# copy log到指定目录
				copyfile(fileNew[0],dstPath)
				if os.path.exists(os.path.join(dstPath,fileNew[0])) == False:
					raise Exception("File {fileNew[0]} copy Failed!")
				# 将文件重新命名
				oldFile=changeName(fileNew[0])
				if os.path.exists(oldFile) ==False:
					raise Exception("change file name failed!")
		elif len(fileNew)==2:
			if app.__contains__("Heaven11"):
				# TODO 判断文件是否符合要求需要在这里做吗
				for file in fileNew:
					dstPath = os.path.join(dstPath, mode)
					# copy log到指定目录
					copyfile(file, dstPath)
					if os.path.exists(os.path.join(dstPath, file)) == False:
						raise Exception(f"File {file} copy Failed!")
					# 将文件重新命名
					oldFile = changeName(file)
					if os.path.exists(oldFile) == False:
						raise Exception("change file name failed!")
		else:
			for file in fileNew:
				# 将文件重新命名
				oldFile = changeName(file)
				if os.path.exists(oldFile) == False:
					raise Exception("change file name failed!")
			flag=True
	else:
		flag=True

	if flag==True:
		print("Please Rerun Testcase !")
		return



def copyfile(srcfile,dstpath):
	if not os.path.isfile(srcfile):
		print ("%s not exist!"%(srcfile))
	else:
		fpath,fname=os.path.split(srcfile)
		if not os.path.exists(dstpath):
			os.makedirs(dstpath)
		shutil.copy(srcfile, dstpath + fname)
		print ("copy %s -> %s"%(srcfile, dstpath + fname))


def changeName(beforeFile):
	index = beforeFile.find('.')
	finalFile = beforeFile[:index] + '_old ' + beforeFile[index:]
	print(finalFile)
	os.rename(beforeFile,finalFile)
	return finalFile