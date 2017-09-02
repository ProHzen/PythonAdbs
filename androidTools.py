import subprocess
import re
import os
import os.path


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
    result = sh('adb shell "dumpsys activity | grep mFocusedActivity"').decode("utf-8")
    regularly = r'[\s\/{1}\s]'
    result = re.split(regularly, result)
    packageName = result[6]
    className = result[7]
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

activity = getCurrrentActivity()
packageName = activity[0]
print(packageName)

path = sh('adb shell pm path '+ packageName).decode("utf-8")
s = r'\:'
path1 = re.split(s, path)


# result = sh(' adb pull ' + path1[1] + ' ~/apks')
ensure_dir(os.path.join(os.path.abspath('.'), 'apks'))
p = subprocess.Popen(' adb pull ' + path1[1] + ' ~/apks', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

# while(True):
#     line = p.stdout.readline().decode("utf-8")
#     if not line:
#         break
#     print(line)

print(path1[1])
# print(os.path.abspath('.'))
# print(result)