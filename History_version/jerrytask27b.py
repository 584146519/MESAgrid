import os
import math
import threading
from tomso import mesa
import math
from glob import glob
import multiprocessing
import psutil
import subprocess
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import mesa_reader as mr
'''
ctrol+k ctrl+0 折叠所有代码
'''
def initialize_variables():# 获取CPU的核心数量，定义基本的变量
    cores = multiprocessing.cpu_count()
    print("Number of CPU cores:", cores)
    filename = './mesabasic/inlist_basic'
    gridname = 'grid'
    grids = []
    return cores, filename, gridname, grids
cores, filename, gridname, grids = initialize_variables()# 初始化变量
def makemesadir(a,name='grid',start=0,step=1):#创建一维网格文件夹
    '传入网格数量,网格的名字'
    global gridname 
    global grids
    gridname=str(name)
    os.system('mkdir mesagrid\n')
    grids=[]
    for i in range(a):
        os.system('cp -r ./mesabasic ./mesagrid/'+gridname+str(start+step*i)+'\n')
        grids+=[gridname+str(start+step*i)]
def mkmesadir2D(a, b, name='grid', start1=0, step1=1, start2=0, step2=1):#创建二维网格文件夹
    '传入网格数量(行列),网格的名字'
    global gridname 
    global grids
    gridname = str(name).replace(' ', '_')  # 替换空格为下划线
    os.system('mkdir -p mesagrid')
    grids = []
    for i in range(a):
        for j in range(b):
            dirname = f'{gridname}{start1+step1*i}_{start2+step2*j}' 
            os.system(f'mkdir -p ./mesagrid')
            os.system(f'cp -r ./mesabasic ./mesagrid/{dirname}')
            grids.append(dirname)
def replaceline2D(a, b,content1,content2, start1=0, step1=1, start2=0, step2=1):#对二维网格进行修改
    '传入网格数量(行列),修改变量的名称,(初始值，布长)'
    for i in range(a):
        for j in range(b):
            filename = f'./mesagrid/{grids[i*b+j]}/inlist_basic'
            b1 = start1 + step1 * i
            b2 = start2 + step2 * j
            update_value_in_file(filename, content1, b1)
            update_value_in_file(filename, content2, b2)
def makegrids(a=10,name='grid',start=0,step=1):
    global grids
    grids=[]
    for i in range(a):
        grids+=[name+str(start+step*i)]
        print(grids)
def searchline(content):   #送入想要查找的内容，从mesabasic模板里寻找
    global filename
    content=str(content)
    contents=open(filename).readlines() #把文件每一行作为元素放入元祖contents
    contentline=[]  #把所有包含所查找内容的行写入元组contentline
    for i in range(len(contents)): #对所有的行遍历
        if content in contents[i]:  #如果该行有所查找的内容
            print(contents[i].rstrip()) #输出整行内容
            print('在',i+1,'行')    #输出行数
            contentline.append(i)   #把行数加入到contentline
def replaceline(content, initial=0.55874, step=0.00001):
    '传入网格数量(行列),修改变量的名称,(初始值，布长)'
    if grids==[]:
        for i,path in enumerate(glob('./mesagrid/*/')):
                filename = f'{path}/inlist_basic'
                b = initial + step * i
                try:
                    update_value_in_file(filename, content, b)
                except FileNotFoundError:
                    print(f'文件{filename}不存在')
    else:
        for i,path in enumerate(grids):
            filename = f'./mesagrid/{path}/inlist_basic'
            b = initial + step * i
            try:
                update_value_in_file(filename, content, b)
            except FileNotFoundError:
                print(f'文件{filename}不存在')
def replaceline2(a,linenum,content,initial=0.55874,step=0.00001):#
    '文件数量，所在行，修改的新固定内容,(初始值，布长)'
    for i,path in enumerate(glob('./mesagrid/*/')):
        filename = f'{path}/inlist_basic'
        contents=open(filename,'r+').readlines() #把文件每一行作为元素放入元祖contents
        b=initial+step*i
        contents[int(linenum)-1]=content +str(b)+'\n'
        open(filename,'w').writelines(contents)
def startall100():#开始的网格数量
    # 获取CPU的核心数量
    cores = multiprocessing.cpu_count()
    print("Number of CPU cores:", cores)
    # 获取 CPU 的总占用率，间隔为 1 秒
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"Total CPU usage: {cpu_usage}%")
    core=math.floor(cores*(1-cpu_usage/100)/len(os.listdir("./mesagrid")))
    print(f"free cores: {cores*(1-cpu_usage/100)}")
    print(f"cores per model: {core}")
    print(f'export OMP_NUM_THREADS={core}')
    # 直接在Python进程中设置环境变量
    os.environ['OMP_NUM_THREADS'] = f'{core}'
    print(os.system('echo $OMP_NUM_THREADS'))
    for i in glob('./mesagrid/*/'):
        try:
            os.system('cd '+i+'\nchmod 700 mk re rn star\n./mk\nnohup ./rn &\ncd ../..\n')
            os.system("echo $OMP_NUM_THREADS")
        except FileNotFoundError:
            print(f'文件{i}不存在')
def startall(cpu_percent=50,setcore=0):#开始的网格数量
    # 获取CPU的核心数量
    cores = multiprocessing.cpu_count()
    print("Number of CPU cores:", cores)
    # 获取 CPU 的总占用率，间隔为 1 秒
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"Total CPU usage: {cpu_usage}%")
    if cpu_usage<1-cpu_percent/100:
        core=math.floor((cores*cpu_percent/100)/len(os.listdir("./mesagrid")))
    else:
        core=math.floor(cores*(1-cpu_usage/100)/len(os.listdir("./mesagrid")))
    print(f"free cores: {cores*(1-cpu_usage/100)},i will use {core} cores")
    print(f"cores per model: {core}")
    print(f'export OMP_NUM_THREADS={core}')
    # 直接在Python进程中设置环境变量
    os.environ['OMP_NUM_THREADS'] = f'{core}'
    if setcore!=0:
        os.environ['OMP_NUM_THREADS'] = f'{setcore}'
    print(os.system('echo $OMP_NUM_THREADS'))
    for i in glob('./mesagrid/*/'):
        try:
            os.system('cd '+i+'\nchmod 700 mk re rn star\n./mk\nnohup ./rn &\ncd ../..\n')
            os.system("echo $OMP_NUM_THREADS")
        except FileNotFoundError:
            print(f'文件{i}不存在')
def stopall():
    os.system("ps -u Liuzy -o pid,comm | grep 'star' | awk '{print $1}' | xargs kill")
def startinturn(a):#为了防止占用太多cpu，一个一个来。
    # 直接在Python进程中设置环境变量
    os.environ['OMP_NUM_THREADS'] = f'{a}'
    if grids == []:
        for i in glob('./mesagrid/*/'):
            os.system('cd '+i+'\nchmod 700 mk re rn star\n./mk\nnohup ./rn &\ncd ../..\n')
            os.system("echo $OMP_NUM_THREADS")
    else:   
            for i in grids:
                os.system('cd ./mesagrid/'+str(i)+'\nchmod 700 mk re rn star\n./mk\nnohup ./rn \ncd ..\n')
def restartall(a=len(grids),step=''):#网格数，re 的步数位置
    if grids == []:
        def runmesa():
            os.system('cd ./mesagrid/grid' +str(i)+f'\n./mk\nnohup ./re {step} &\ncd ..\n')
        for i in range(a):
            t = threading.Thread(target=runmesa)
            t.start()
    else:
        def runmesa():
            os.system('cd ./mesagrid/' +str(i)+f'\n./mk\nnohup ./re {step} &\ncd ..\n')
        for i in grids:
            t = threading.Thread(target=runmesa)
            t.start()
def gyregrid(startstep,endstep):
    j=endstep-startstep+1
    os.system('mkdir gyregrid\n')
    filename='LOGS/history.data'
    h=mesa.load_history(filename)
    for i in range(startstep,endstep+1):
        os.system(f'mkdir ./gyregrid/profile{i}\ncp gyre.in ./gyregrid/profile{i}/\ncp ./LOGS/profile{i}.data.GYRE ./gyregrid/profile{i}/profile.data.GYRE\ncd ./gyregrid/profile{i}/\nnohup $GYRE_DIR/bin/gyre ./gyre.in')
        os.system('cd ../..')
def gyregridnum(startstep,endstep):
    j=endstep-startstep+1
    os.system('mkdir gyregrid\n')
    filename='LOGS/history.data'
    for i in range(j):
        os.system(f'mkdir ./gyregrid/profile{i+1}\ncp gyre.in ./gyregrid/profile{i+1}/\ncp ./LOGS/profile{i+1}.data.GYRE ./gyregrid/profile{i+1}/profile.data.GYRE\ncd ./gyregrid/profile{i+1}/\nnohup $GYRE_DIR/bin/gyre ./gyre.in')
        os.system('cd ../..')
def gethistorydata(): #网格数，把history.data改名为
    os.system('mkdir -p ./mesagrid/HISTORY')
    for i in glob('mesagrid/*/'):
        new = i.split('/')[-2] + '.data'
        os.system(f'cp ./{i}/LOGS/history.data ./mesagrid/HISTORY/\nmv ./mesagrid/HISTORY/history.data ./mesagrid/HISTORY/{new}\n')
def update_value_in_file(file_path, keyword, new_value):# 更新文件中特定变量的值
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        if keyword in  line:
            lines[i] = f"      {keyword}={new_value}\n"
            break
    with open(file_path, 'w') as file:
        file.writelines(lines)
def changevalue_all(keyword, new_value):
    for i in glob('mesagrid/*/'):
        filename = i + 'inlist_basic'
        try:
            update_value_in_file(filename, keyword, new_value)
        except FileNotFoundError:
            print(f'文件{filename}不存在')
def nethr():
    def calculate_angle(p1, p2, p3):
        """
        Calculate the angle formed by three points p1, p2, and p3.
        p1, p2, and p3 are coordinates in the form (x, y).
        Returns the angle in degrees.
        """
        # Calculate vectors for the triangle sides
        vec_ab = np.array(p1) - np.array(p2) 
        vec_bc = np.array(p3) - np.array(p2)

        # Calculate the angles using the dot product
        # angle_a = np.arccos(np.dot(vec_ab, -vec_ca) / (np.linalg.norm(vec_ab) * np.linalg.norm(vec_ca)))
        angle_b = np.arccos(np.dot(vec_bc, -vec_ab) / (np.linalg.norm(vec_bc) * np.linalg.norm(vec_ab)))
        # angle_c = np.arccos(np.dot(vec_ca, -vec_bc) / (np.linalg.norm(vec_ca) * np.linalg.norm(vec_bc)))

        return np.degrees(angle_b)
    def delnoise(list1,list2,j=80):
        i=1
        while i <len(list1)-3 :
            angle=calculate_angle([list1[i-1],list2[i-1]],[list1[i],list2[i]],[list1[i+1],list2[i+1]])
            if angle > j:
                # list1[i]=0.1*list1[i-2] + 0.2*list1[i-1] + 0.4*list1[i] + 0.2*list1[i+1] + 0.1*list1[i+2]
                del list1[i]
                # list2[i]=0.1*list2[i-2] + 0.2*list2[i-1] + 0.4*list2[i] + 0.2*list2[i+1] + 0.1*list2[i+2]
                del list2[i]
                i=i-1
            i=i+1
        return list1,list2
    def repeat_delnoise(list1,list2,j=80):
        for i in range(100):
            print(len(list1))
            list1,list2=delnoise(list1,list2,j)
        return list1,list2
    paths=sorted([i for i in (Path('./mesagrid/HISTORY/').rglob('*.data'))])
    os.system('mkdir ./mesagrid/HR\n')
    for i in paths:
        plt.figure()
        h = mr.MesaData(f'{i}')
        teff,Lum=h.log_Teff,h.log_L
        teff,Lum=repeat_delnoise(h.log_Teff.tolist(), h.log_L.tolist(),90)
        plt.plot(teff,Lum)
        # try :
        #     He=h.surface_he4[5000]
        # except IndexError:
        #     He=h.surface_he4[-1]
        if max(h.surface_he4)>h.surface_he4[1]:
            He=max(h.surface_he4)
        else:
            He=h.surface_he4[1]
        plt.xlabel('log Teff')
        plt.ylabel('log L/Lsun')
        plt.gca().invert_xaxis()
        j=str(i).split("/")[-1]
        plt.savefig(f'./mesagrid/HR/He={He:.3f}'+str(j)[:-5]+'.png')
        plt.close()
def graph():
    paths = sorted([i for i in (Path('./mesagrid/HISTORY/').rglob('*.data'))])
    x = []
    y = []
    z = []
    a = []
    x2= []
    y2= []
    os.system('mkdir HR\n')
    for i in paths:
        h = mr.MesaData(f'{i}')
        # try :
        #     He=max(h.surface_he4)  
        # except IndexError:
        #     He=h.surface_he4[-1]
        if max(h.surface_he4)>h.surface_he4[1]+0.001:
            He=max(h.surface_he4)
            z.append(He)
            parts = str(i).rsplit('_', 1)
            x.append(float(parts[0].rsplit('_', 1)[-1]))
            y.append(float(parts[1].rsplit('.', 1)[0]))

        else:
            He=h.surface_he4[1]
            a.append(He)
            parts = str(i).rsplit('_', 1)
            x2.append(float(parts[0].rsplit('_', 1)[-1]))
            y2.append(float(parts[1].rsplit('.', 1)[0]))

    # 确保保存图片的路径存在
    path = './mesagrid/HR/'
    os.makedirs(path, exist_ok=True)

    # 创建包含失败点的散点图
    fig, ax = plt.subplots()
    scatter1 = ax.scatter(x, y, c=z, cmap='viridis')
    scatter2 = ax.scatter(x2, y2, c="r", marker="x", cmap='viridis')
    ax.set_xlabel('mass')
    ax.set_ylabel('f0')
    ax.set_title('2D Scatter Plot with Colorbar')
    colorbar = plt.colorbar(scatter1)  # 使用第一组数据的颜色条
    colorbar.set_label('He surface')
    plt.savefig(os.path.join(path, 'He.png'), dpi=300)

    # 创建没有失败点的散点图
    fig, ax = plt.subplots()
    scatter = ax.scatter(x, y, c=z, cmap='viridis')
    ax.set_xlabel('mass')
    ax.set_ylabel('f0')
    ax.set_title('2D Scatter Plot with Colorbar')
    colorbar = plt.colorbar(scatter)
    colorbar.set_label('He surface')
    plt.savefig(os.path.join(path, 'He2.png'), dpi=300)
    plt.show()
def 版本变化():
    版本更新日志 = '''
版本变化：
1.1 增加了对网格文件夹的创建，以及对网格文件夹的修改
1.5 增加了对23.05.1的inlist_to_flash的函数，并且对startinturn进行完善
1.6beta 增加了全局变量的使用
1.6 完善了makegrids
1.7beta 增加了gyrenum，从1开始
1.8beta 增加了运行之前给予权限的一步,以及二维网格文件夹创立，并且把网格数量默认值取为len(grids),找到了“re”的bug，没有标准化f。
1.8 还优化了gethistorydata的文件名称。还优化了并行计算和单独计算的核心数量
1.9beta 删除了不用的函数，并增加了改变量的函数，使用该函数改变mesa参数。
1.9 更改gethistorydata的文件名称，为所在文件夹名称
2.0beta, 增加对文件夹所有网格某一参数的修改,增加一键启动的权限添加，以及核数限制
2.0 完善了startall和changeall，增加了try，except函数，防止出错，且运行时输出并行核心数
2.1beta 增加了stopall函数，可以停止所有的mesa运行,statall会输出动态调整的并行核心数
2.1 完美解决了stopall的问题，只会结束Liuzy的star进程，不会结束其他人的star进程，且startall会输出动态调整的并行核心数
2.2 更改了startall，运行之后最多占用50%的cpu，且输出动态调整的并行核心数，相较于2.2beta取消使用Decimal
2.3b, 修复gethistorydata的bug，.data .data，并按照折叠后更美观的格式优化了一下代码风格，例如把版本更新记录的字符串放到了函数里面
2.3a, 增加了startall100，可以使用100%的cpu,增加了nethr，可以画出hr图，增加了paragraph，可以输出参数空间图
2.3,对startall进行集成，增加了两个参数，一个指定可以使用的cpu百分比，一个可以指定使用的核心数量
2.31 对netHR保存路径进行优化
2.32 再优化net HR、graph路径，选步骤中最大的He到名字里
2.4Beta 重写graph，名字改成graph，取最大值He，如果表面He没有改变则画叉
2.5Beta 修改startinturn，可以指定核心数量
2.6b 修改replaceline和replaceline2，循环变量为mesagrid目录下所有文件夹
2.6 修改replaceline,删掉了不用的变量a，增加了try，except函数，防止出错
2.7b 修改replaceline,让其跟着grids顺序修改
'''
    # 移除首尾的空白字符，并分割字符串成行
    版本更新记录列表 = 版本更新日志.strip().splitlines()
    # 输出最后一行
    print(版本更新记录列表[-1])
版本变化()
