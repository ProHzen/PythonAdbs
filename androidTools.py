import subprocess
import re
import os
import os.path
import time

def sh(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p.stdout.read()


def ensure_dir(f):
    try:
        if not os.path.exists(f):
            os.makedirs(f)
    except IOError:
        print("apks文件夹创建异常")
        return False
    return True


def getCurrrentActivity():
    # 采用正则表达式截取
    result = sh('adb shell "dumpsys activity | grep mFocusedActivity"').decode("utf-8").lstrip()
    regularly = r'[\s\/{1}\s]'
    print(result)
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

    return str


def getCurrentApk():
    activity = getCurrrentActivity()
    packageName = activity[0]
    print(packageName)
    getApkByPackageName(packageName)


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


def getScreenShots():
    ensure_dir(os.path.join(os.path.abspath('.'), 'images'))
    timeName = time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.png';
    print(timeName)
    print('adb exec-out screencap -p > ' + " " + os.path.join(os.path.abspath('.'), 'images', timeName + '.png'))
    print('adb exec-out screencap -p   /sdcard/' + timeName)
    print('adb pull /sdcard/' + timeName + '  ' + os.path.join(os.path.abspath('.'), 'images'))
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


def reboot():
    sh('adb reboot')


def killCurrentApp():
    activity = getCurrrentActivity()
    packageName = activity[0]
    sh('adb shell am force-stop ' + packageName)


def clearData():
    activity = getCurrrentActivity()
    packageName = activity[0]
    sh('adb shell pm clear ' + packageName)

def uninstall():
    activity = getCurrrentActivity()
    packageName = activity[0]
    sh('adb uninstall ' + packageName)

uninstall()