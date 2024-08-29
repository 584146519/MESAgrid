import os
from contextlib import redirect_stdout
import inspect
import sys
import tkinter as tk
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
from datetime import datetime
from multiprocessing import Pool
from tkinter import messagebox
from concurrent.futures import ProcessPoolExecutor
import shutil
from decimal import Decimal
'''
ctrol+k ctrl+0 折叠所有代码
'''
    
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
2.8b 增加了timescale函数，可以计算表面温度大于a小于b的时间
2.8c 修改了timescale函数，增加了返回值,加入了netHR中
2.8 测试完毕， netHR 和 timescale可以用了
2.9c timescale 增加了更改 ab 参数的变量，使 nethr 显示不同范围的时标
2.9b ts函数增加了 valueerror
2.9 增加了 graphts，getvalue
3.0b 修改了 graphts，多进程并行计算 
3.0c nethr 增加except (IndexError, TypeError) as e:
3.0d nethr增加j，可以运行时调整
31 对照startall，调整了restartall
31b graphhe不会生成 HR 文件夹了
31c 终于把 graphts 和 nethr以及 graphtso 以及timescaleo 都写完了
32 每个函数都增加了类型转换，确保GUI能正常运行
32b 把 makemesadir 中直接加入了 replaceline
32c 解决 nethr 图片无名称的问题
33 把python加法出现 99999 问题进行优化
33b 把初始化函数加上 AAAAA，使得最开始就可以设置 inlist 的名字,改了所有的 filename，stopall 可以加上 user 了 增加了使用教程  startall 增加了各种程序支持
33c 完善可执行性
34 确定功能可用，增加了使用教程
34b inlist_name声明为全局变量
34c 重要更新，脱离了 mesa_reader 包的使用，剩余包均可直接使用 pip安装，以及 startall 对 py 文件支持的 bug
35 重要更新，完全脱离了 mesa_reader 包的使用，测试没有问题，
35b 尺寸也更加合适
35c nethr改为多线程
36a nethr's He is redefined
36b add start number ,fix bug in mkdir2D
37 fix bug,use shutil.copytree instead of os.system to creat dir to avoid "()" in dir name
37a fix bug if step is too small, use decimal to avoid float precision error
37b rewrited startall ,restartall to avoid "()" in dir name
37c this version can use mouse to scroll the window,and remove the chinese in function name
38a deleted timescaleo, timescale,use find_value_line
38b fix bug
38c fix bug in changevalue_all
39 make 2D dir can change inlist in sametime, and delete on_mousewheel buttun,and make timescale(o) back to laet HR run, and fix bug in upvalue_in_file
'''
使用教程='''
这是一个可以设定运行 mesa 网格的程序包，准备操作如下
0 安装所有的 import 的包
1把网格初始的模型文件全部放进 mesabasic 的文件夹中（换句话说把初始模型的文件夹名称改为 mesabasic）
2 在 mesabasic 的上级文件夹内运行该程序




正式使用步骤如下：
如果只调整一个参数即一维网格，使用 makemesadir 创建网格，会在 mesabaisc 文件夹旁边生成 mesagrid 里面放网格模型
，之后使用 startall 来全部开始，开始后本程序可以关闭

制作二维网格使用 mkmesadir2D 创建网格
使用replaceline2D来改变变量，对于需要改变的变量超过二个但是具有相关性的变量（本质还是二维网格），多次使用replaceline2D即可
之后使用 startall 来全部开始，开始后本程序可以关闭

可以使用replaceline、replaceline2D、insert_line 以及changevalue_all来改变全体 inlist 的值
'''
def change_log():

    # 移除首尾的空白字符，并分割字符串成行
    版本更新记录列表 = 版本更新日志.strip().splitlines()
    # 输出最后一行
    print("welcome use jerrytask!\nversion:"+版本更新记录列表[-1])
    print(使用教程)

def AAAAAAA_initialize_variables(input_inlist_name = 'inlist_basic'):# 获取CPU的核心数量，定义基本的变量
    cores = multiprocessing.cpu_count()
    print("Number of CPU cores:", cores)
    gridname = 'grid'
    global basic_inlist
    global inlist_name
    inlist_name=input_inlist_name
    basic_inlist='./mesabasic/'+inlist_name
    grids = []
    change_log()
    return cores, basic_inlist, inlist_name,gridname, grids
cores, basic_inlist, inlist_name,gridname, grids = AAAAAAA_initialize_variables()# 初始化变量

def makemesadir(a, content='grid', start=0, step=1):
    a = int(a)
    start, step = float(start), float(step)
    decimal = max(count_decimal_places(step), count_decimal_places(start))
    
    global gridname 
    global grids
    
    gridname = str(content)
    base_dir = './mesagrid'
    os.makedirs(base_dir, exist_ok=True)  # 使用 makedirs 而不是 os.system
    grids = []
    
    for i in range(a):
        dir_name = f"{gridname}_{start+step*i:.{decimal}f}"
        src = './mesabasic'
        dst = os.path.join(base_dir, dir_name)
        shutil.copytree(src, dst)  # 使用 shutil.copytree 而不是 os.system
        grids.append(dst)
    replaceline(content,start,step)

def insert_line(line_number,text):
    '传入行号和要插入的文本'
    line_number = int(line_number)
    if grids==[]:
        for i,path in enumerate(glob('./mesagrid/*/')):
            filepath = f'{path}/{inlist_name}'
            try:
                with open(filepath, 'r') as file:
                    lines = file.readlines()
                # 确保行号在文件的行数范围内
                if 0 <= line_number <= len(lines):
                    lines.insert(line_number, text + '\n')
                else:
                    print("Line number is out of range.")
                    return
                with open(filepath, 'w') as file:
                    file.writelines(lines)
            except FileNotFoundError:
                print(f'文件{filepath}不存在')

def mkmesadir2D(a, b,content1,content2, start1=0, step1=1, start2=0, step2=1):
    """创建二维网格文件夹"""
    global gridname 
    global grids
    a, b = int(a), int(b)
    start1, step1 = float(start1), float(step1)
    decimal1 = max(count_decimal_places(step1), count_decimal_places(start1))
    start2, step2 = float(start2), float(step2)
    decimal2 = max(count_decimal_places(step2), count_decimal_places(start2))
    base_dir = 'mesagrid'
    os.makedirs(base_dir, exist_ok=True)
    grids = []
    
    for i in range(a):
        for j in range(b):
            dirname = f'{content1}_{start1+step1*i:.{decimal1}f}_{content2}_{start2+step2*j:.{decimal2}f}'
            dir_path = os.path.join(base_dir, dirname)
            os.makedirs(dir_path, exist_ok=True)  # 创建目录，如果目录存在则忽略
            shutil.copytree('mesabasic', dir_path, dirs_exist_ok=True)  # 复制文件夹
            grids.append(dir_path)
    
    for i in range(a):
        for j in range(b):
            filename = f'./{grids[i*b+j]}/{inlist_name}'
            b1 = start1 + step1 * i
            b2 = start2 + step2 * j
            update_value_in_file(filename, content1, b1,decimal1)
            update_value_in_file(filename, content2, b2,decimal2)

def replaceline2D(a, b,content1,content2, start1=0, step1=1, start2=0, step2=1):#对二维网格进行修改
    '传入网格数量(行列),修改变量的名称,(初始值，布长)'
    a, b = int(a), int(b)
    start1, step1 = float(start1), float(step1)
    decimal1=max(count_decimal_places(step1),count_decimal_places(start1))
    start2, step2 = float(start2), float(step2)
    decimal2=max(count_decimal_places(step2),count_decimal_places(start2))
    for i in range(a):
        for j in range(b):
            filename = f'./mesagrid/{grids[i*b+j]}/{inlist_name}'
            b1 = start1 + step1 * i
            b2 = start2 + step2 * j
            update_value_in_file(filename, content1, b1,decimal1)
            update_value_in_file(filename, content2, b2,decimal2)

def makegrids(a=10,name='grid',start=0,step=1):
    global grids
    a=int(a)
    start,step=float(start),float(step) 
    grids=[]
    for i in range(a):
        grids+=[name+str(start+step*i)]
        print(grids)

def searchline(content):   #送入想要查找的内容，从mesabasic模板里寻找
    content=str(content)
    contents=open(basic_inlist).readlines() #把文件每一行作为元素放入元祖contents
    contentline=[]  #把所有包含所查找内容的行写入元组contentline
    for i in range(len(contents)): #对所有的行遍历
        if content in contents[i]:  #如果该行有所查找的内容
            print(contents[i].rstrip()) #输出整行内容
            print('在',i+1,'行')    #输出行数
            contentline.append(i)   #把行数加入到contentline

def replaceline(content, initial=0.55874, step=0.00001):
    '传入网格数量(行列),修改变量的名称,(初始值，布长)'
    global grids
    initial, step = float(initial), float(step)
    decimal=max(count_decimal_places(step),count_decimal_places(initial))
    if grids==[]:
        for i,path in enumerate(glob('./mesagrid/*/')):
                filename = f'{path}/{inlist_name}'
                b = initial + step * i
                try:
                    update_value_in_file(filename, content, b)
                except FileNotFoundError:
                    print(f'文件{filename}不存在')
    else:
        for i,path in enumerate(grids):
            filename = f'{path}/{inlist_name}'
            b = initial + step * i
            try:
                update_value_in_file(filename, content, b,decimal)
            except FileNotFoundError:
                print(f'文件{filename}不存在')

def replaceline2(a,linenum,content,initial=0.55874,step=0.00001):#
    '文件数量，所在行，修改的新固定内容,(初始值，布长)'
    global grids
    initial, step = float(initial), float(step)
    decimal=max(count_decimal_places(step),count_decimal_places(initial))
    a=int(a)
    for i,path in enumerate(glob('./mesagrid/*/')):
        filename = f'{path}/{inlist_name}'
        contents=open(filename,'r+').readlines() #把文件每一行作为元素放入元祖contents
        b=initial+step*i
        contents[int(linenum)-1]=content +f'{b:.{decimal}f}'+'\n'
        open(filename,'w').writelines(contents)

def startall(setcore=1, Executable_file='rn'):
    setcore = int(setcore)
    if setcore != 0:
        os.environ['OMP_NUM_THREADS'] = str(setcore)

    for i in glob('./mesagrid/*/'):
        try:
            # 给予文件执行权限
            subprocess.run(['chmod', '700', 'mk', Executable_file, 're', 'rn', 'star'], cwd=i)

            # 构造执行 mk 的命令
            subprocess.run(['./mk'], cwd=i)

            # 构造并执行主程序的命令
            exec_cmd = ['nohup', 'python3', Executable_file] if Executable_file.endswith(".py") else ['nohup', f'./{Executable_file}']
            with open(os.path.join(i, "nohup.out"), "a") as outfile:
                subprocess.Popen(exec_cmd, cwd=i, stdout=outfile, stderr=subprocess.STDOUT)

        except FileNotFoundError:
            print(f'文件{i}不存在')
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while executing in {i}: {e}")

def startnumber(startfrom=1,to=50,setcore=1,Executable_file='rn'):#开始的网格数量
    startfrom=int(startfrom)
    to=int(to)
    setcore=int(setcore)
    # 获取CPU的核心数量
    cores = multiprocessing.cpu_count()
    print("Number of CPU cores:", cores)
    # 获取 CPU 的总占用率，间隔为 1 秒
    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"Total CPU usage: {cpu_usage}%")
    # if cpu_usage<1-cpu_percent/100:
    #     core=math.floor((cores*cpu_percent/100)/len(os.listdir("./mesagrid")))
    # else:
    #     core=math.floor(cores*(1-cpu_usage/100)/len(os.listdir("./mesagrid")))
    # print(f"free cores: {cores*(1-cpu_usage/100)},i will use {core} cores")
    # print(f"cores per model: {core}")
    # print(f'export OMP_NUM_THREADS={core}')
    # # 直接在Python进程中设置环境变量
    # os.environ['OMP_NUM_THREADS'] = f'{core}'
    if setcore!=0:
        os.environ['OMP_NUM_THREADS'] = f'{setcore}'
    if Executable_file.endswith(".py"):
        for i in glob('./mesagrid/*/'):
            os.system('cd '+i+f'\nchmod 700 mk {Executable_file} re rn star\n./mk\nnohup python3 {Executable_file} &\ncd ../..\n')
            print("已执行Python文件。")
    else: 
        print(os.system('echo $OMP_NUM_THREADS'))
        for i in glob('./mesagrid/*/')[startfrom-1:to-1]:
            try:
                os.system('cd '+i+f'\nchmod 700 mk {Executable_file} re rn star\n./mk\nnohup ./{Executable_file} &\ncd ../..\n')
                os.system("echo $OMP_NUM_THREADS")
            except FileNotFoundError:
                print(f'文件{i}不存在')

def stopall(user="Liuzy"):
    os.system(f"ps -u {user} -o pid,comm "+"| grep 'star' | awk '{print $1}' | xargs kill")

def startinturn(a):#为了防止占用太多cpu，一个一个来。
    a=int(a)
    # 直接在Python进程中设置环境变量
    os.environ['OMP_NUM_THREADS'] = f'{a}'
    if grids == []:
        for i in glob('./mesagrid/*/'):
            os.system('cd '+i+'\nchmod 700 mk re rn star\n./mk\nnohup ./rn &\ncd ../..\n')
            os.system("echo $OMP_NUM_THREADS")
    else:   
            for i in grids:
                os.system('cd ./mesagrid/'+str(i)+'\nchmod 700 mk re rn star\n./mk\nnohup ./rn \ncd ..\n')

def restartall(setcore=0):#网格数，re 的步数位置
    setcore = int(setcore)
    Executable_file='re'
    if setcore != 0:
        os.environ['OMP_NUM_THREADS'] = str(setcore)

    for i in glob('./mesagrid/*/'):
        try:
            # 给予文件执行权限
            subprocess.run(['chmod', '700', 'mk', Executable_file, 're', 'rn', 'star'], cwd=i)

            # 构造执行 mk 的命令
            subprocess.run(['./mk'], cwd=i)

            # 构造并执行主程序的命令
            exec_cmd = ['nohup', f'./{Executable_file} ']
            with open(os.path.join(i, "nohup.out"), "a") as outfile:
                subprocess.Popen(exec_cmd, cwd=i, stdout=outfile, stderr=subprocess.STDOUT)

        except FileNotFoundError:
            print(f'文件{i}不存在')
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while executing in {i}: {e}")

def gyregrid(startstep,endstep):
    startstep=int(startstep)
    endstep=int(endstep)
    j=endstep-startstep+1
    os.system('mkdir gyregrid\n')
    filename='LOGS/history.data'
    h=mesa.load_history(filename)
    for i in range(startstep,endstep+1):
        os.system(f'mkdir ./gyregrid/profile{i}\ncp gyre.in ./gyregrid/profile{i}/\ncp ./LOGS/profile{i}.data.GYRE ./gyregrid/profile{i}/profile.data.GYRE\ncd ./gyregrid/profile{i}/\nnohup $GYRE_DIR/bin/gyre ./gyre.in')
        os.system('cd ../..')

def gyregridnum(startstep,endstep):
    startstep=int(startstep)
    endstep=int(endstep)
    j=endstep-startstep+1
    os.system('mkdir gyregrid\n')
    filename='LOGS/history.data'
    for i in range(j):
        os.system(f'mkdir ./gyregrid/profile{i+1}\ncp gyre.in ./gyregrid/profile{i+1}/\ncp ./LOGS/profile{i+1}.data.GYRE ./gyregrid/profile{i+1}/profile.data.GYRE\ncd ./gyregrid/profile{i+1}/\nnohup $GYRE_DIR/bin/gyre ./gyre.in')
        os.system('cd ../..')

def gethistorydata():
    # 确保HISTORY目录存在
    history_dir = './mesagrid/HISTORY'
    os.makedirs(history_dir, exist_ok=True)
    
    for i in glob('mesagrid/*/'):
        # 获取文件夹的名称，去掉尾部的 '/'
        folder_name = os.path.basename(os.path.dirname(i))
        new_file_name = folder_name + '.data'
        
        # 构造原始和目标文件的完整路径
        original_file = os.path.join(i, 'LOGS', 'history.data')
        target_file = os.path.join(history_dir, new_file_name)
        
        # 拷贝和重命名文件
        try:
            # 使用 shutil 来拷贝和重命名文件
            shutil.copy2(original_file, target_file)
            print(f"Copied and renamed history data to {target_file}")
        except FileNotFoundError:
            print(f"History data file not found in {i}")
        except Exception as e:
            print(f"An error occurred: {e}")

def update_value_in_file(file_path, keyword, new_value,decimal=10):# 更新文件中特定变量的值
    keyword=' '+str(keyword)
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        if keyword in  line:
            lines[i] = f"     {keyword} = {new_value:.{decimal}f}\n"
            break
    with open(file_path, 'w') as file:
        file.writelines(lines)

def changevalue_all(keyword, new_value):
    new_value=float(new_value)
    decimal=count_decimal_places(new_value)
    for i in glob('mesagrid/*/'):
        filename = i + f'{inlist_name}'
        try:
            update_value_in_file(filename, keyword, new_value,decimal)
        except FileNotFoundError:
            print(f'文件{filename}不存在')

def timescale(filenam,a=4.274158,b=4.3874):
    a,b=float(a),float(b)
    h=mesa.load_history(f'{filenam}')
    age=h['star_age']
    
    teff=h['log_Teff']
    logg=h['log_g']
    bas,ket=[],[]
    # for i,t in enumerate(teff):
    #     if (t>a and teff[i-1]<a) or (t<a and teff[i-1]>a):
    #         bas.append(i)
    # for j,t in enumerate(teff):
    #     if (t>b and teff[j-1]<b) or (t<b and teff[j-1]>b):
    #         ket.append(j)
    for i,t in enumerate(teff):
        if t>a and teff[i-1]<a :
            bas.append(i)

    for j,t in enumerate(teff):
        if t>b and teff[j-1]<b :
            ket.append(j)
    try:
        print(len(bas),len(ket))
        bas=min(bas, key=lambda x: logg[x])
        ket=min(ket, key=lambda x: logg[x])
        # bas=max(bas)
        # ket=max(ket)
    except ValueError:
        pass
    return bas,ket,age[ket]-age[bas]

def timescaleo(order,filename,a=4.274158,b=4.3874):
    a,b=float(a),float(b)
    h=mesa.load_history(f'{filename}')
    age=h['star_age']
    teff,Lum=h['log_Teff'],h['log_L']
    logg=h['log_g']
    bas,ket=[],[]

    for j,t in enumerate(order[:-1]):  # 仅遍历到列表的倒数第二个元素
        if teff[order[j]]<a and teff[order[j+1]]>a :
            bas.append(order[j])

    for j,t in enumerate(order[:-1]):  # 同上
        if teff[order[j]]<b and teff[order[j+1]]>b :
            ket.append(order[j+1])

    try:
        print(len(bas),len(ket))
        bas=max(bas)
        ket=max(ket)
    except ValueError:
        pass
    try:
        return bas,ket,age[ket]-age[bas]
    except ValueError:
        pass

def process_HR(args):
    ii, delangle = args  # 从传入的元组中解包 ii 和 delangle
    def calculate_angle(p1, p2, p3):
        """
        Calculate the angle formed by three points p1, p2, and p3.
        p1, p2, and p3 are coordinates in the form (x, y).
        Returns the angle in degrees.
        """
        # Calculate vectors for the triangle sides
        vec_ab = np.array(p1) - np.array(p2) 
        vec_bc = np.array(p3) - np.array(p2)
        angle_b = np.arccos(np.dot(vec_bc, -vec_ab) / (np.linalg.norm(vec_bc) * np.linalg.norm(vec_ab)))
        # angle_c = np.arccos(np.dot(vec_ca, -vec_bc) / (np.linalg.norm(vec_ca) * np.linalg.norm(vec_bc)))

        return np.degrees(angle_b)
    def delnoise(list1, list2):
        i = 1
        while i < len(list1) - 3:
            # 使用带索引的元组来计算角度
            angle = calculate_angle([list1[i - 1][1], list2[i - 1][1]], [list1[i][1], list2[i][1]], [list1[i + 1][1], list2[i + 1][1]])
            if angle > delangle:
                # 删除元素时，直接删除对应的元组
                del list1[i]
                del list2[i]
                i = i - 1
            i = i + 1
        return list1, list2
    def repeat_delnoise(list1,list2):
        for _ in range(20):
            print(len(list1))
            list1,list2=delnoise(list1,list2)
        return list1,list2
    plt.figure()
    h=mesa.load_history(f'{ii}')

    teff,Lum=h['log_Teff'],h['log_L']


    # teff,Lum=repeat_delnoise(h.log_Teff.tolist(), h.log_L.tolist())
    teff,Lum=repeat_delnoise(list(enumerate(teff)), list(enumerate(Lum)))  
    order=[]
    for j in range(len(teff)):
        order.append(teff[j][0])
    try:
        a,b,ts=timescaleo(order,ii,4.2,4.8)
    except TypeError:
        pass
    teff,Lum=h['log_Teff'],h['log_L']
    print('hello,world')

    teff,Lum=[teff[k] for k in order],[Lum[k] for k in order]
    try:
        bas,ket,time_scale=timescaleo(order,ii)
        u,p,o=timescale(ii)
    except (TypeError,ValueError):
        pass
    plt.plot(teff,Lum)

    try:
        # dycen范围
        plt.scatter(h['log_Teff'][bas], h['log_L'][bas], c='r', marker='x', s=200)
        plt.scatter(h['log_Teff'][ket], h['log_L'][ket], c='r', s=100, marker='x')
        plt.text(h['log_Teff'][bas], h['log_L'][bas], f'{time_scale:.2f}yr', fontsize=10)
        # 更大的范围
        plt.scatter(h['log_Teff'][a], h['log_L'][a], c='b', marker='x')
        plt.scatter(h['log_Teff'][b], h['log_L'][b], c='b', marker='x')
        plt.text(h['log_Teff'][b], h['log_L'][b], f'{ts:.2f}yr', fontsize=10)
        # dycen的更大周期
        plt.scatter(h['log_Teff'][u], h['log_L'][u], c='g', marker='x')
        plt.scatter(h['log_Teff'][p], h['log_L'][p], c='g', marker='x')
        plt.text(h['log_Teff'][p], h['log_L'][p], f'{o:.2f}yr', fontsize=10)
    except (IndexError, TypeError,ValueError) as e:
        pass

    if max(h['surface_he4'])>h['surface_he4'][1]:
        He=max(h['surface_he4'])
    else:
        He=h['surface_he4'][1]
    for i in range(len(h['star_age'])):
        if h['star_age'][i]-h['star_age'][0]>2000:
            He=h['surface_he4'][i]



    plt.xlabel('log Teff')
    plt.ylabel('log L/Lsun')
    plt.gca().invert_xaxis()
    # k=str(ii).split("_")[-1]
    k=os.path.basename(ii)[:-5]
    # print(f"He={He:.3f}, {k}")
    # print(f"Saving file to ./mesagrid/HR/He={He:.3f}_{k}.png")
    plt.savefig(f'./mesagrid/HR/He={He:.3f}_{k}.png')
    # plt.savefig(f'./mesagrid/HR/{k}.png')

    # plt.show()
    plt.close()

def gridHR(delangle=80,OMP=4):
    delangle=float(delangle)
    OMP=int(OMP)
    paths = sorted([i for i in Path('./mesagrid/HISTORY/').rglob('*.data')])
    os.system('mkdir -p ./mesagrid/HR')

    with ProcessPoolExecutor(max_workers=OMP) as executor:
        # 将 paths 和相同长度的 delangle 值打包成元组
        args = ((ii, delangle) for ii in paths)
        executor.map(process_HR, args)

def graphhe():
    paths = sorted([i for i in (Path('./mesagrid/HISTORY/').rglob('*.data'))])
    x = []
    y = []
    z = []
    x2= []
    y2= []
    os.system('mkdir ./mesagrid/HR\n')
    for i in paths:
        h=mesa.load_history(f'{i}')
        filename = os.path.basename(i)[:-5]
        parts = str(filename).rsplit('_', 4)
        y.append(float(parts[4]))
        x.append(float(parts[3]))
        ylabel = parts[2]
        xlabel = parts[1]


        # try :
        #     He=max(h.surface_he4)  
        # except IndexError:
        #     He=h.surface_he4[-1]
        if max(h['surface_he4'])>h['surface_he4'][1]+0.001:
            He=max(h['surface_he4'])
            z.append(He)

        else:
            He=h['surface_he4'][1]
            z.append(He)

    # 确保保存图片的路径存在
    path = './mesagrid/HR/'
    os.makedirs(path, exist_ok=True)

    # # 创建包含失败点的散点图
    # fig, ax = plt.subplots()
    # scatter1 = ax.scatter(x, y, c=z, cmap='viridis')
    # scatter2 = ax.scatter(x2, y2, c="r", marker="x", cmap='viridis')
    # ax.set_xlabel(f'{xlabel}')
    # ax.set_ylabel(f'{ylabel}')
    # # ax.set_title('2D Scatter Plot with Colorbar')
    # colorbar = plt.colorbar(scatter1)  # 使用第一组数据的颜色条
    # colorbar.set_label('He surface')
    # plt.savefig(os.path.join(path, 'He.png'), dpi=300)

    # 创建没有失败点的散点图
    fig, ax = plt.subplots()
    scatter = ax.scatter(x, y, c=z, cmap='viridis')
    ax.set_xlabel(f'{xlabel}')
    ax.set_ylabel(f'{ylabel}')
    ax.set_title('2D Scatter Plot with Colorbar')
    colorbar = plt.colorbar(scatter)
    colorbar.set_label('He surface')
    plt.savefig(os.path.join(path, 'He2.png'), dpi=300)
    plt.show()

def graphts2D():
    paths = sorted([i for i in (Path('./mesagrid/HISTORY/').rglob('*.data'))])
    x = []
    y = []
    ts=[]
    # 获取当前日期和时间

    os.system('mkdir ./mesagrid/HR\n')
    for i in paths:
        h=mesa.load_history(f'{i}')
        parts = str(i).rsplit('_', 1)
        x.append(float(parts[0].rsplit('_', 1)[-1]))
        y.append(float(parts[1].rsplit('.', 1)[0]))
        first=find_value_line('log_Teff', 4.274158)
        last=find_value_line('log_Teff', 4.3874)
        print(first, last)
        ts.append(h['star_age'][last]-h['star_age'][first])


    ts_clean = [x if isinstance(x, float) else 0 for x in ts]  # 用0替换非浮点数值，或者选择其他合适的默认值

    # 确保保存图片的路径存在
    path = './mesagrid/HR/'
    os.makedirs(path, exist_ok=True)


    # 创建没有失败点的散点图
    fig, ax = plt.subplots()
    # scatter = ax.scatter(x, y, c=ts, cmap='viridis')
    scatter = ax.scatter(x, y, c=ts_clean, cmap='viridis')

    ax.set_xlabel('mass')
    ax.set_ylabel('f0')
    # ax.set_title('wha')
    colorbar = plt.colorbar(scatter)
    colorbar.set_label('time scale')
    plt.savefig(os.path.join(path, 'timescale.png'), dpi=300)
    plt.show()

def graphts():
    paths = sorted([i for i in (Path('./mesagrid/HISTORY/').rglob('*.data'))])
    ts=[]
    f0=[]
    for path in paths:
        print(path)
        h=mesa.load_history(f'{path}')
        first=find_value_line('log_Teff', 4.274158)
        last=find_value_line('log_Teff', 4.3874)
        print(first, last)
        ts.append(h['star_age'][last]-h['star_age'][first])
        parts = str(path).rsplit('_', 1)
        f0.append(float(parts[1][:-5]))
        print(f0)
        print(f0[-1], ts[-1])





    fig, ax = plt.subplots()
    plt.plot( f0,ts, 'o')
    ax.set_xlabel('f0')
    ax.set_ylabel('timescale')

    plt.savefig('timescale.png', dpi=300)
    plt.show()

def getvalue():
    # 获取所有.data文件的路径，并排序
    paths = sorted([i for i in Path('./mesagrid/HISTORY/').rglob('*.data')])
    # 初始化一个空字典来存储列表
    variables = {}
    # 第一个循环，初始化字典中的键和空列表
    for filename in paths:
        parts = str(filename).split('_')  # 将Path对象转换为字符串
        for part in parts:
            if '=' in part:
                key, _ = part.split('=')  # 分割每个部分以获取键
                if key not in variables:  # 检查键是否已经在字典中
                    variables[key] = []  # 初始化键对应的列表
 
    # 第二个循环，填充数据
    for filename in paths:
        parts = str(filename).split('_')  # 将Path对象转换为字符串
        for part in parts:
            if '=' in part:
                key, value = part.split('=')  # 分割每个部分以获取键和值
                if key in variables:  # 确保键存在于字典中
                    variables[key].append(value)  # 将值添加到相应的列表

    return variables

def create_gui_for_function(frame, func, column):
    subframe = tk.Frame(frame)
    # 使用 grid 管理 subframe 的布局
    grid_row = column // 4
    grid_col = column % 4
    subframe.grid(row=grid_row, column=grid_col, padx=10, pady=10, sticky='nw')

    tk.Label(subframe, text=f"Function: {func.__name__}").grid(sticky="w")

    params = inspect.signature(func).parameters
    entries = {}

    # 对于每个参数，创建一个子框架，并使用 grid 管理布局
    for index, param in enumerate(params.values()):
        row = tk.Frame(subframe)
        row.grid(row=index + 1, column=0, sticky="ew", padx=5, pady=5)

        tk.Label(row, text=param.name + ":").pack(side=tk.LEFT)
        entry = tk.Entry(row)
        entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        if param.default != param.empty:
            entry.insert(0, str(param.default))
        entries[param.name] = entry

    def invoke():
        args = {name: entry.get() for name, entry in entries.items()}
        try:
            func(**args)
            messagebox.showinfo("Success", f"{func.__name__} executed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    run_button = tk.Button(subframe, text="Run", command=invoke)
    run_button.grid(row=len(params) + 2, column=0, sticky="e")

def count_decimal_places(number):
    # 使用Decimal来确保数值准确
    number = Decimal(str(number))
    # 转换为字符串
    num_str = format(number, 'f')
    # 检查是否有小数点
    if '.' in num_str:
        return len(num_str.split('.')[1])
    else:
        return 0
    
def on_mouse_wheel(event):
    # 针对不同操作系统，调整滚动事件的处理
    if event.num == 5 or event.delta == -120:
        canvas.yview_scroll(1, "units")
    elif event.num == 4 or event.delta == 120:
        canvas.yview_scroll(-1, "units")

def find_value_line(path,parameter, value):
    h=mesa.load_history(f'{path}')
    data=h[str(parameter)]
    for i in range(len(data)-1):
        if data[i]<=value and data[i+1]>=value:
            if h['log_L'][i]>3:
                if h['model_number'][i]>300:
                    num=i
                    break

    return  num

if __name__ == "__main__":
    root = tk.Tk()
    root.title("MESAgrid Function GUI")
    root.geometry("1100x800")  # 设置初始大小

    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    # # 排除列表
    exclude_functions = ['create_gui_for_function','find_value_line','timescale','replaceline2','getvalue','glob','update_value_in_file','count_decimal_places','版本变化','process_HR','on_mouse_wheel']

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    root.bind_all("<MouseWheel>", on_mouse_wheel)  # 适用于Windows和Mac
    root.bind_all("<Button-4>", on_mouse_wheel)   # 适用于Linux
    root.bind_all("<Button-5>", on_mouse_wheel)   # 适用于Linux

    # 确保所有内容使用 grid 布局
    scrollable_frame.grid(row=0, column=0, sticky="nsew")

    # # 为每个函数创建GUI，跳过排除列表中的函数
    # 创建 GUI 元素
    functions = [obj for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isfunction) if name not in exclude_functions]
    for ii, func in enumerate(functions):
        create_gui_for_function(scrollable_frame, func, ii)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    scrollable_frame.grid(row=0, column=0, sticky="nsew")
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    root.mainloop()
