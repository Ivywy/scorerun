import os
import time
import win32file as pywin32


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



