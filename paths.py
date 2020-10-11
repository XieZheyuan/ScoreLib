import ctypes
from ctypes.wintypes import MAX_PATH
from os.path import abspath


def getDocuments():
    dll = ctypes.windll.shell32
    buf = ctypes.create_unicode_buffer(MAX_PATH + 1)
    if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
        return buf.value
    else:
        return abspath(".")
