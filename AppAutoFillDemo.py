#!/usr/bin/env python3

import time,re,ctypes
import os,sys,subprocess,win32gui,win32con,win32api,win32process
import glob,time

#启进程函数
def createProcess(cmd, wait = False):
    if wait:
        proc = tryExcept(subprocess.Popen, cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    else:
        proc = tryExcept(subprocess.Popen, cmd)
    if isExcept(proc):
        return
    if not wait:
        return proc.pid
    proc.communicate()


def tryExcept(func, *params, **paramMap):
    try:
        return func(*params, **paramMap)
    except Exception as e:
        return e

def isExcept(e, eType = Exception):
    return isinstance(e, eType)

#获得窗口尺寸
def getWindowRect(hwnd):
    rect = tryExcept(win32gui.GetWindowRect, hwnd)
    if not isExcept(rect):
        return rect


##获取窗口文字
def getWindowText(hwnd, buf = ctypes.c_buffer(1024)):
    return win32gui.GetWindowText(hwnd)

#获取窗口类名
def getWindowClass(hwnd):
    return win32gui.GetClassName(hwnd)

def getWindowProcessId(hwnd):
    tid, pid = win32process.GetWindowThreadProcessId(hwnd)
    return pid

def findWindowsByPid(pid):
    wndList = enumWindows()
    hwndList = []
    for hwnd, wpid, wtitle in wndList:
        if wpid == pid:
            clazz = getWindowClass(hwnd)
            hwndList.append((hwnd, clazz, wtitle))
    return hwndList

def enumWindows(all = False):
    def __enumWindowHandler__(hwnd, wndList):
        if all or (win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd)):
            pid = getWindowProcessId(hwnd)
            wtitle = getWindowText(hwnd)
            wndList.append((hwnd, pid, wtitle))
                #return True
        return True
    wndList = []
    win32gui.EnumWindows(__enumWindowHandler__, wndList)
    return wndList

def findWindowsByTitle(title):
    wndList = enumWindows()
    for hwnd, pid, wtitle in wndList:
        if wtitle.startswith(title):
            return (hwnd, pid, wtitle)
    return None

def findChildHwnd(hwnd, type  = None):
    def __enumWindowHandler__(hwnd, wndList):
        text = getWindowText(hwnd)
        clazz = getWindowClass(hwnd).strip()
        ctrlId = win32gui.GetDlgCtrlID(hwnd)
        wndList[hwnd] = (hwnd, text, clazz, ctrlId)
        return True
    wndList = {}
    try:
        win32gui.EnumChildWindows(hwnd, __enumWindowHandler__, wndList)
    except Exception as e:
        pass
    return wndList


def clickMouse(x, y, byDrv = False, button = "LEFT"):
    moveMouse(x, y, byDrv)
    downMsg, upMsg = win32con.MOUSEEVENTF_LEFTDOWN, win32con.MOUSEEVENTF_LEFTUP
    if button == "RIGHT":
        downMsg, upMsg = win32con.MOUSEEVENTF_RIGHTDOWN, win32con.MOUSEEVENTF_RIGHTUP
    win32api.mouse_event(downMsg, 0, 0, 0, 0)
    win32api.mouse_event(upMsg, 0, 0, 0, 0)
    if button == "DOUBLE_CLICK":
        win32api.mouse_event(downMsg, 0, 0, 0, 0)
        win32api.mouse_event(upMsg, 0, 0, 0, 0)

#移动鼠标
def moveMouse(x, y, byDrv = False):
    point = (x, y)
    win32api.SetCursorPos(point)

hwndInfo = findWindowsByTitle("Navicat")
if hwndInfo:
    hwnd, pid, title = hwndInfo
else:
    command=sys.argv[1] if len(sys.argv) >=2 else 'C:\\Program Files (x86)\\PremiumSoft\\Navicat for MySQL\\navicat.exe'
    pid = createProcess(command)
    #pid = createProcess("C:\\Program Files (x86)\\Cloudbility\\XingYunGuanJiaPlugin\\cloudNativeTool.exe")

    while True:
        hwndInfo = findWindowsByPid(pid)
        if hwndInfo:
            hwnd, clazz, title = hwndInfo[0]
            if title.startswith("Navicat"):
                hwndList = findChildHwnd(hwnd)
                if hwndList:
                    break
        time.sleep(1)
    print(enumWindows())



win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
win32gui.SetForegroundWindow(hwnd)
hwndList = findChildHwnd(hwnd)

print("Child of windows %d:%s"%(hwnd, str(hwndList)))
#print(hwndList)

menuHwnd = None
for _, info in hwndList.items():
    childHwnd, text, clazz, ctrlId = info
    if clazz == "TActionMainMenuBar":
        menuHwnd = childHwnd
        break;
print(menuHwnd)
rect = win32gui.GetWindowRect(menuHwnd)
print(rect)

#点击第一级菜单
x,y =  (rect[0]+19, rect[1]+10)
print("Click at (%d,%d)"%(x, y))
clickMouse(x, y)
time.sleep(0.5)
hwnds = findWindowsByPid(pid)
print("find pid %d: %s"%(pid, str(hwnds)))
secMenuHwndInfo = [x for x in hwnds if x[1] == "TThemedPopupMenu"]
print("Second menu hwnd info %s"%(str(secMenuHwndInfo)))
secMenuHwnd = secMenuHwndInfo[0][0]
print("second menu childs: %s"%(str(findChildHwnd(secMenuHwnd))))
print("second menu rect: %s"%(str(win32gui.GetWindowRect(secMenuHwnd))))

#点击第二级菜单
x += 18
y += 36
print("Click at (%d,%d)"%(x, y))
clickMouse(x, y)
time.sleep(2)
hwnds = findWindowsByPid(pid)
print("find pid %d: %s"%(pid, str(hwnds)))
secMenuHwndInfo = [x for x in hwnds if x[1] == "TThemedPopupMenu"]
print("Second menu hwnd info %s"%(str(secMenuHwndInfo)))
# secMenuHwnd = secMenuHwndInfo[0][0]
# print("second menu childs: %s"%(str(findChildHwnd(secMenuHwnd))))
# print("second menu rect: %s"%(str(win32gui.GetWindowRect(secMenuHwnd))))

#点击第三级菜单
x += 160
print("Click at (%d,%d)"%(x, y))
clickMouse(x, y)

time.sleep(0.5)

print(enumWindows())
hwnd, clazz, title = findWindowsByPid(pid)[0]
print((hwnd, clazz, title))
childs = findChildHwnd(hwnd)
print(childs)
time.sleep(2)
for childHwnd, child in childs.items():
    if child[1] == '取消':
        rect = win32gui.GetWindowRect(childHwnd)
        print("Click cancel button at %s "%(str(rect)))
        clickMouse(int((rect[0] + rect[2])/2), int((rect[1]+rect[3])/2))

#
# win32gui.SendMessage(hwndList[2][0], win32con.WM_SETTEXT, None, user)
# win32gui.SendMessage(hwndList[3][0], win32con.WM_SETTEXT, None, password)
# time.sleep(2)
# win32gui.SendMessage(hwndList[0][0], win32con.BM_CLICK, 0, 0)
#

