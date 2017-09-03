import subprocess
import re
import os
import os.path
import time
import tkinter as t

tup1 = ('获取当前包名和activity', '获取当前应用版本信息', '获取当前apk', '截取当前屏幕',
        '重启当前设备', '杀掉当前应用', '清除当前应用数据', '卸载当前应用')

# 执行shell脚本
def sh(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p.stdout.read()


# 创建文件夹
def ensure_dir(f):
    try:
        if not os.path.exists(f):
            os.makedirs(f)
    except IOError:
        print("apks文件夹创建异常")
        return False
    return True


# 获取当前activity 实际返回的是包含包名和类名的元组 0为包名 1为类名
def getCurrrentActivity():
    # 采用正则表达式截取
    result = sh('adb shell "dumpsys activity | grep mFocusedActivity"').decode("utf-8").lstrip()
    regularly = r'[\s\/{1}\s]'
    result = re.split(regularly, result)
    print(result)
    for index in range(len(result)):
        if (result[index].find('com') == 0):
            packageIndex = index
            break
    packageName = result[packageIndex]
    className = result[packageIndex + 1]
    print("packageName = " + packageName + " className = " + className)
    str = (packageName, className)
    # 不采用正则表达式截取
    # index = str1.find('com')
    # str2 = str1[index:].split('/')
    # str3 = str2[0]
    # str4 = str2[1]
    # str5 = str4[:str4.find(' ')]
    # print("packageName = " + str3 + " className = " + str5)
    textln('packageName = ' + packageName)
    textln('className = ' + className)
    return str

def getCurrentPackageName():
    return getCurrrentActivity()[0]

# 获取当前apk 存放到当前目录下的apks文件夹里面
def getCurrentApk():
    activity = getCurrrentActivity()
    packageName = activity[0]
    getApkByPackageName(packageName)
    return


# 根据包名获取apk 存放到当前目录下的apks文件夹里面
def getApkByPackageName(packageName):
    path = sh('adb shell pm path ' + packageName).decode("utf-8").rstrip()
    s = r'\:'
    path1 = re.split(s, path)
    # result = sh(' adb pull ' + path1[1] + ' ~/apks')
    ensure_dir(os.path.join(os.path.abspath('.'), 'apks'))
    p = subprocess.Popen(' adb pull ' + path1[1] + " " + os.path.join(os.path.abspath('.'), 'apks'), shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while (True):
        line = p.stdout.readline().decode("utf-8")
        if not line:
            break
        print(line)
        textln(line)
    textln("成功拉取apk")
    return


# 获取屏幕截图 存放到当前目录下的images文件夹里面
def getScreenShots():
    ensure_dir(os.path.join(os.path.abspath('.'), 'images'))
    timeName = time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.png';
    textln(timeName)
    textln('adb exec-out screencap -p > ' + " " + os.path.join(os.path.abspath('.'), 'images', timeName + '.png'))
    textln('adb exec-out screencap -p   /sdcard/' + timeName)
    textln('adb pull /sdcard/' + timeName + '  ' + os.path.join(os.path.abspath('.'), 'images'))
    p = subprocess.Popen('adb exec-out screencap -p /sdcard/' + timeName,
                         shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()
    sh('adb pull /sdcard/' + timeName + '  ' + os.path.join(os.path.abspath('.'), 'images'))
    sh('adb shell rm /sdcard/' + timeName)

    # while (True):
    #     line = p.stdout.readline().decode("utf-8")
    #     if not line:
    #         break
    #     print(line)
    return


# 重启
def reboot():
    sh('adb reboot')
    return


# 杀死当前运行的应用
def killCurrentApp():
    activity = getCurrrentActivity()
    packageName = activity[0]
    sh('adb shell am force-stop ' + packageName)
    return


# 清除当前运行应用的数据
def clearData():
    activity = getCurrrentActivity()
    packageName = activity[0]
    sh('adb shell pm clear ' + packageName)
    return


# 卸载应用
def uninstall():
    activity = getCurrrentActivity()
    packageName = activity[0]
    sh('adb uninstall ' + packageName)
    return


def handler(index1):
    try:
        print("processButton = " + str(index1))
        text.delete(0.0, t.END)
        switcher = {
            0: getCurrrentActivity,
            1: getCurrentAppVersionInfo,
            2: getCurrentApk,
            3: getScreenShots,
            4: reboot,
            5: killCurrentApp,
            6: clearData,
            7: uninstall
        }
        return switcher.get(index1)()
    except Exception:
        textln(Exception)

def get_screen_size(window):
    return window.winfo_screenwidth(), window.winfo_screenheight()


def get_window_size(window):
    return window.winfo_reqwidth(), window.winfo_reqheight()


def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)

# 换行的text
def textln(content):
    text.insert(t.END, content + '\n')

def initView():
    global text
    window = t.Tk()
    window.title("Android Tools Made By YangShangZhen")
    center_window(window, 800, 500)
    frame1 = t.Frame(window)
    frame1.pack()
    for index in range(8):
        if index <= 3:
            button1 = t.Button(frame1, padx=1, pady=1, height=1,
                               text=tup1[index], command=lambda index=index: handler(index))
            button1.grid(padx=10, pady=10, row=1, column=index)
        else:
            button2 = t.Button(frame1, padx=1, pady=1, height=1,
                               text=tup1[index], command=lambda index=index: handler(index))
            button2.grid(padx=10, pady=10, row=2, column=index - 4)
    text = t.Text(window, foreground='black', font=('宋体', 12), spacing1=10)
    text.pack(padx=0, pady=20)
    window.mainloop()

# 解析当前的版本号和版本名字
# 解析的格式根据 versionCode='694' versionName='11.5.2.942' 如果格式不对 可能会出现错误
def getCurrentAppVersionInfo():
    versionInfo = sh('adb shell dumpsys package ' + getCurrentPackageName()).decode("utf-8")
    vCodePattern = r'versionCode=.+?\s'
    vNamePattern = r'versionName=.+?\s'
    vCodeNumberPattern = r'\d+'
    vNameNumberPattern = r'\d.+\d'
    versionCodeInfo = re.findall(vCodePattern, versionInfo)
    print(versionCodeInfo)
    defaultVersionCode = ''
    defaultVersionName = ''
    for index in range(len(versionCodeInfo)):
        if index == 0:
            currentVersionCode = re.findall(vCodeNumberPattern, versionCodeInfo[0])
        if index == 1:
            defaultVersionCode = re.findall(vCodeNumberPattern, versionCodeInfo[1])
    versionCodeDict = {"currentVersionCode": currentVersionCode, "defaultVersionCode": defaultVersionCode}
    versionNameInfo = re.findall(vNamePattern, versionInfo)
    print(versionNameInfo)
    for index in range(len(versionNameInfo)):
        if index == 0:
            currentVersionName = re.findall(vNameNumberPattern, versionNameInfo[0])
        if index == 1:
            defaultVersionName = re.findall(vNameNumberPattern, versionNameInfo[1])
    versionNameDict = {"currentVersionName": currentVersionName, "defaultVersionName": defaultVersionName}
    textln(str(versionCodeDict))
    textln(str(versionNameDict))
    return

if __name__ == '__main__':
    initView()