import os
import shutil
import tkinter as t
import _thread

root = r'D:\Repos\com\sinyee\babybus'
reposRoot = r'Z:\dev-repos\com\sinyee\babybus'

localFileDict = dict()
reposFileDict = dict()

fileListLayer = os.listdir(root)
reposFileListLayer = os.listdir(reposRoot)


# 打印本地文件夹
def getLocalFile():
    for eachFileDirName in fileListLayer:
        if eachFileDirName.__contains__("DS"):
            continue
        source = os.path.join(root, eachFileDirName)
        fileListChildren = os.listdir(source)
        stringL = []
        for fileListName in fileListChildren:
            if 'DS' in fileListName:
                stringL.append(fileListName)
            if 'xml' in fileListName:
                stringL.append(fileListName)
        for index in stringL:
            fileListChildren.remove(index)
        localFileDict[eachFileDirName] = fileListChildren
    print(localFileDict)


# 打印远程文件夹
def getRemoteFile():
    for eachFileDirName in reposFileListLayer:
        if eachFileDirName.__contains__("DS"):
            continue
        source = os.path.join(reposRoot, eachFileDirName)
        fileListChildren = os.listdir(source)
        stringL = []
        for fileListName in fileListChildren:
            if 'DS' in fileListName:
                stringL.append(fileListName)
            if 'xml' in fileListName:
                stringL.append(fileListName)
        for index in stringL:
            fileListChildren.remove(index)
        reposFileDict[eachFileDirName] = fileListChildren
    print(reposFileDict)


# 对比两个目录，拷贝文件
def copyFile():
    for eachFileDirName in reposFileDict:
        if eachFileDirName.__contains__("DS"):
            continue
        if eachFileDirName not in localFileDict.keys():
            sourceSrc = os.path.join(reposRoot, eachFileDirName)
            dstSrc = os.path.join(root, eachFileDirName)
            print('拷贝代码文件夹' + eachFileDirName + '开始...')
            textln('拷贝代码文件夹' + eachFileDirName + '开始...')
            shutil.copytree(sourceSrc, dstSrc)
            print('拷贝代码文件夹' + eachFileDirName + '结束！')
            textln('拷贝代码文件夹' + eachFileDirName + '结束！')
        else:
            localFile = localFileDict[eachFileDirName]
            reposFile = reposFileDict[eachFileDirName]
            for fileName in reposFile:
                if fileName not in localFile:
                    sourceSrc = os.path.join(reposRoot, eachFileDirName + '/' + fileName)
                    dstSrc = os.path.join(root, eachFileDirName + '/' + fileName)
                    print('拷贝代码文件夹' + eachFileDirName + '/' + fileName + '开始...')
                    textln('拷贝代码文件夹' + eachFileDirName + '/' + fileName + '开始...')
                    shutil.copytree(sourceSrc, dstSrc)
                    print('拷贝代码文件夹' + eachFileDirName + '/' + fileName + '结束！')
                    textln('拷贝代码文件夹' + eachFileDirName + '/' + fileName + '结束！')

def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)

def rename():
    root = str(e_local.get()).replace('\\', '\\\\')
    reposRoot = str(e_remote.get()).replace('\\', '\\\\')
    print('root = ', root)
    print('reposRoot = ', reposRoot)
    getLocalFile()
    getRemoteFile()
    _thread.start_new_thread(copyFile, ())

    dict_name = {1: root, 2: reposRoot}
    f = open('path.txt', 'w')
    f.write(str(dict_name))
    f.close()

# 换行的text
def textln(content):
    text.insert(t.END, content + '\n')

if __name__ == '__main__':
    global text

    window = t.Tk()
    window.title("Android Tools Made By YangShangZhen")
    center_window(window, 800, 500)
    frame1 = t.Frame(window)
    frame1.pack()

    var = t.StringVar()
    var.set('本地文件夹')
    l = t.Label(window, textvariable=var, font=('Arial', 12), width=15, height=2)
    l.place(x=20, y=10, anchor='nw')

    e_local = t.Entry(window, width=50)
    e_local.place(x=150, y=20)

    var = t.StringVar()
    var.set('远程文件夹')
    l = t.Label(window, textvariable=var, font=('Arial', 12), width=15, height=2)
    l.place(x=20, y=70, anchor='nw')

    e_remote = t.Entry(window, width=50)
    e_remote.place(x=150, y=83)

    b = t.Button(window, text='确定', width=15, height=1, command=rename)
    b.place(x=650, y=40)

    text = t.Text(window, foreground='black', font=('宋体', 12), spacing1=10, height=13)
    text.place(x=50, y=130)

    if os.path.exists('path.txt'):
        f = open('path.txt', 'r')
        a = f.read()
        dict_name = eval(a)
        e_local.insert(0, str(dict_name[1]).replace('\\\\','\\'))
        e_remote.insert(0, str(dict_name[2]).replace('\\\\','\\'))
        f.close()

    window.mainloop()
