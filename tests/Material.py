# -------关联C++库---------------
import ctypes
import platform
system = platform.system()
if system == "Windows":
    pre = "./"
    suff = ".dll"
else:
    pre = "../lib/lib"
    suff = ".so"

libfile = ctypes.cdll.LoadLibrary
filename = pre+"HPDI.OSIS.PREP.Material"+suff

ma = libfile(filename)

# ---------------------------------


def setMat(Id, svariable, type):
    variable = bytes(svariable, encoding='utf-8')
    ma.setMat(Id, variable, type)
    pass
