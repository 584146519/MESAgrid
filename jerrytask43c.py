'''
ctro(keep)+k+0 折叠所有代码
'''
import os
import shlex, subprocess
from contextlib import redirect_stdout
import inspect
import sys
import math
# import threading
from tomso import mesa
import math
from glob import glob
import multiprocessing
import psutil
import subprocess
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor
import shutil
from decimal import Decimal
import inspect
import re

exclude_functions = ['update_value_in_file_raw','_strip_quotes','create_gui_for_function', 'find_value_line', 'timescale', 'replaceline2', 'getvalue', 'glob', 'update_value_in_file',
                     'count_decimal_places', '版本变化', 'process_HR', 'on_mouse_wheel', 'main', 'call_function_by_number', 'get_functions',
                     'display_functions', 'change_log', 'timescale', 'timescaleo', 'get_value', 'parse_scientific_str', 'safe_convert', 
                     'gui_format_value','format_fortran_exponent','simple_fortran_format','graphts','graphhe','graphts2D','replaceline']

print("select mode:")
print("1. GUI ")
print("2. Command Line")

choice = input("(1 or 2): ")

if choice == '1':
    try:
        import tkinter as tk
        from tkinter import messagebox

        def main():
            # 这里写入原来的带图形界面的主函数代码
            def on_mouse_wheel(event):
                # 针对不同操作系统，调整滚动事件的处理
                if event.delta:  # Windows 和 macOS 使用 event.delta
                    if event.delta < 0:
                        canvas.yview_scroll(1, "units")  # 向下滚动
                    else:
                        canvas.yview_scroll(-1, "units")  # 向上滚动
                elif event.num:  # Linux 使用 event.num
                    if event.num == 5:
                        canvas.yview_scroll(1, "units")  # 向下滚动
                    elif event.num == 4:
                        canvas.yview_scroll(-1, "units")  # 向上滚动
            root = tk.Tk()
            root.title("MESAgrid Function GUI")
            root.geometry("1200x800")  # 设置初始大小

            canvas = tk.Canvas(root)
            scrollbar = tk.Scrollbar(root, command=canvas.yview)
            scrollable_frame = tk.Frame(canvas)

            # # 排除列表

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
    except (ImportError, tk.TclError):
        print("GUI mode is not available. Use the command line mode.")
        def get_functions():
            # 获取当前模块中的所有函数，并过滤掉不需要显示的函数
            functions = {name: obj for name, obj in inspect.getmembers(__import__(__name__), inspect.isfunction) 
                            if name not in exclude_functions}
            return functions

        def display_functions(functions):
            # 显示函数列表
            print("Available Functions:")
            for i, (name, func) in enumerate(functions.items(), start=1):
                print(f"{i}. {name}")

        def call_function_by_number(functions, func_number=None):
            if func_number is not None:
                func_name = list(functions.keys())[func_number - 1]
                func = functions[func_name]
                print(f"Calling function: {func_name}")

                # 获取函数的参数信息
                sig = inspect.signature(func)
                params = sig.parameters
                
                args = []
                kwargs = {}
                # 提示用户输入参数值
                for name, param in params.items():
                    if param.default == inspect.Parameter.empty:  # 如果参数没有默认值
                        value = input(f"Please enter the value for parameter '{name}': ")
                        args.append(value)
                    else:
                        value = input(f"Please enter the value for '{name}' (or press Enter to use the default value: {param.default}): ")
                        if value:
                            kwargs[name] = value

                # 调用函数并传入参数
                result = func(*args, **kwargs)

            while True:
                display_functions(functions)
                try:
                    # 提示用户输入要调用的函数序号
                    func_number = int(input("Enter the function number to run: "))
                    if 1 <= func_number <= len(functions):
                        func_name = list(functions.keys())[func_number - 1]
                        func = functions[func_name]
                        print(f"Calling function: {func_name}")

                        # 获取函数的参数信息
                        sig = inspect.signature(func)
                        params = sig.parameters
                        
                        args = []
                        kwargs = {}
                        # 提示用户输入参数值
                        for name, param in params.items():
                            if param.default == inspect.Parameter.empty:  # 如果参数没有默认值
                                value = input(f"Please enter the value for parameter '{name}': ")
                                args.append(value)
                            else:
                                value = input(f"Please enter the value for '{name}' (or press Enter to use the default value {param.default}): ")
                                if value:
                                    kwargs[name] = value

                        # 调用函数并传入参数
                        result = func(*args, **kwargs)
                        
                        # 打印结果
                        if result is not None:
                            print(f"The result of the function '{func_name}' is: {result}")
                        break
                    else:
                        print("Invalid choice. Please enter a number corresponding to a function.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

        def main():
            functions = get_functions()
            call_function_by_number(functions, 1)
            while True:
                call_function_by_number(functions)
elif choice == '2':
    def get_functions():
        # 获取当前模块中的所有函数，并过滤掉不需要显示的函数
        functions = {name: obj for name, obj in inspect.getmembers(__import__(__name__), inspect.isfunction) 
                        if name not in exclude_functions}
        return functions

    def display_functions(functions):
        # 显示函数列表
        print("Available Functions:")
        for i, (name, func) in enumerate(functions.items(), start=1):
            print(f"{i}. {name}")

    def call_function_by_number(functions, func_number=None):
        if func_number is not None:
            func_name = list(functions.keys())[func_number - 1]
            func = functions[func_name]
            print(f"Calling function: {func_name}")

            # 获取函数的参数信息
            sig = inspect.signature(func)
            params = sig.parameters
            
            args = []
            kwargs = {}
            # 提示用户输入参数值
            for name, param in params.items():
                if param.default == inspect.Parameter.empty:  # 如果参数没有默认值
                    value = input(f"Please enter the value for parameter '{name}': ")
                    args.append(value)
                else:
                    value = input(f"Please enter the value for '{name}' (or press Enter to use the default value: {param.default}): ")
                    if value:
                        kwargs[name] = value

            # 调用函数并传入参数
            result = func(*args, **kwargs)

        while True:
            display_functions(functions)
            try:
                # 提示用户输入要调用的函数序号
                func_number = int(input("Enter the function number to run: "))
                if 1 <= func_number <= len(functions):
                    func_name = list(functions.keys())[func_number - 1]
                    func = functions[func_name]
                    print(f"Calling function: {func_name}")

                    # 获取函数的参数信息
                    sig = inspect.signature(func)
                    params = sig.parameters
                    
                    args = []
                    kwargs = {}
                    # 提示用户输入参数值
                    for name, param in params.items():
                        if param.default == inspect.Parameter.empty:  # 如果参数没有默认值
                            value = input(f"Please enter the value for parameter '{name}': ")
                            args.append(value)
                        else:
                            value = input(f"Please enter the value for '{name}' (or press Enter to use the default value {param.default}): ")
                            if value:
                                kwargs[name] = value

                    # 调用函数并传入参数
                    result = func(*args, **kwargs)
                    
                    # 打印结果
                    if result is not None:
                        print(f"The result of the function '{func_name}' is: {result}")
                    break
                else:
                    print("Invalid choice. Please enter a number corresponding to a function.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def main():
        functions = get_functions()
        call_function_by_number(functions, 1)
        while True:
            call_function_by_number(functions)
else:
    print("wrong choice, please run the program again and choose 1 or 2.")

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
33b 把初始化函数加上 AAAAA,使得最开始就可以设置 inlist 的名字,改了所有的 filename,stopall 可以加上 user 了 增加了使用教程  startall 增加了各种程序支持
33c 完善可执行性
34 确定功能可用，增加了使用教程
34b inlist_name声明为全局变量
34c 重要更新，脱离了 mesa_reader 包的使用，剩余包均可直接使用 pip安装,以及 startall 对 py 文件支持的 bug
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
40 big update,test the tkinter gui,if not,can use command line to run the program,and change function name and parameter name to make it more understandable
40a fix restartall,change name to resumall
41 add function start in group
42 simple change all value , add parse_scientific_str,get_value,change count_decimal_places,grid2D
43 delete startinturn and simple the GUI make it more simple to new user ,change1100*800 to1200*800
43a replace gethistorydata to gatherdata
43b change subprocess.Popen make sure process running when python is killed
43c add changevalue1D ,change changevalue2D grid2D, make it can change string varieble ,like '3M.mod', add gather_by_keyword, can gather different file with diff name
'''
使用教程='''
One-dimensional grid:
If you adjust just one parameter and use makemesadir to create the grid, the mesagrid folder will be generated next to the mesabaisc folder to put the grid model
Then use startall to startall, after starting the program can be closed

Two-dimensional grid:
Create the grid using mkmesadir2D
Use replaceline2D for more than two variables that need to be changed, but are related (essentially or two-dimensional grids)

Start:
Then use startall to startall, after starting the program can be closed

You can use replaceline, replaceline2D, insert_line, and changevalue_all to change the value of all Inlists
'''
def change_log():

    # 移除首尾的空白字符，并分割字符串成行
    版本更新记录列表 = 版本更新日志.strip().splitlines()
    # 输出最后一行
    print("welcome use jerrytask!\nversion:"+版本更新记录列表[-1])
    print(使用教程)

def format_fortran_exponent(sci_str):
    """
    给定类似 "1.0000000000d+02" 的字符串，转换为：
      "1.0000000000d2"（正指数去掉 "+" 和前导零）
      "3.1400000000d-03" -> "3.1400000000d-3"
    """
    def repl(match):
        sign = match.group(1)
        exp_num = match.group(2)
        exp_int = int(exp_num)  # 自动去除前导0
        if sign == '+':
            return f"d{exp_int}"
        else:
            return f"d-{exp_int}"
    return re.sub(r"d([+-])0*([0-9]+)", repl, sci_str)

def A_initialize_variables(input_inlist_name = 'inlist_basic'):# 获取CPU的核心数量，定义基本的变量
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
cores, basic_inlist, inlist_name,gridname, grids = A_initialize_variables()# 初始化变量

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

def parse_scientific_str(s, default_coeff=1.0):
    """
    解析形如 "1d-10" 或 "d0.5" 的字符串，返回 (系数, 指数)。
    如果系数部分为空，则默认使用 default_coeff；指数部分为空则默认 0.0。
    若不含 "d"，则直接转换为 float，并返回 (float(s), 0.0)。
    """
    if 'd' in s:
        parts = s.split('d')
        if len(parts) != 2:
            raise ValueError(f"格式错误: {s}")
        coeff_str, exp_str = parts
        coeff = float(coeff_str) if coeff_str else default_coeff
        exp = float(exp_str) if exp_str else 0.0
        return coeff, exp
    else:
        return float(s), 0.0

def simple_fortran_format(num):
    """
    将浮点数 num 转换为简化后的 Fortran 风格科学计数法字符串，
    保证：系数部分采用最小表示（不带多余小数位），指数为整数且不带正号或前导 0。
    例如：1e-2 -> "1d-2"，3.16227766e-10 -> "3.16228d-10"。
    """
    if num == 0:
        return "0d0"
    exp = int(math.floor(math.log10(abs(num))))
    coeff = num / (10 ** exp)
    # 使用 'g' 格式得到最简表示
    coeff_str = format(coeff, 'g')
    return f"{coeff_str}d{exp}"

def update_value_in_file(file_path, keyword, new_value, decimal=10, sci_format=False):
    """
    更新文件中特定变量的值。
    如果 sci_format 为 True，则调用 simple_fortran_format 将 new_value 转换为 Fortran 风格（例如 "1d-2"），
    否则使用普通的 f 格式，保留 decimal 指定的小数位数。
    """
    keyword = ' ' + str(keyword)
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        if keyword in line:
            if sci_format:
                formatted = simple_fortran_format(new_value)
            else:
                formatted = f"{new_value:.{decimal}f}"
            lines[i] = f"     {keyword} = {formatted}\n"
            break
    with open(file_path, 'w') as file:
        file.writelines(lines)

def update_value_in_file_raw(file_path, keyword, raw_value_str):
    """
    直接将原样字符串写入 inlist（例如：'1d-3.mod' 或 'abc'）。
    注意：调用者需自行决定是否加引号。
    """
    keyword = ' ' + str(keyword)
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if keyword in line:
            lines[i] = f"     {keyword} = {raw_value_str}\n"
            break
    with open(file_path, 'w') as f:
        f.writelines(lines)

def _strip_quotes(s):
    return s.strip().strip("'").strip('"')

def grid2D(number_of_2Dgrid_rows, number_of_2Dgrid_columns,
           parameter_name_1='grid1', parameter_name_2='grid2',
           start1=0, step1=1, start2=0, step2=1,
           suffix1='', suffix2=''):
    """
    创建二维网格，并把两个参数写入各自 inlist。
    - 数值部分仍由 start/step 控制，支持 'd' 科学计数法（如 '1d-2'）。
    - 若 suffixX 非空：写入形式为  '<引号>数值部分+后缀<引号>'  (例如 '1d-3.mod')
    - 若 suffixX 为空：写入为纯数值（不加引号），行为与原先完全一致。
    - 目录命名只使用数值部分（不含引号/后缀），保持兼容。
    """
    global gridname, grids
    a = int(number_of_2Dgrid_rows)
    b = int(number_of_2Dgrid_columns)

    sci_format1 = isinstance(start1, str) and ('d' in start1)
    sci_format2 = isinstance(start2, str) and ('d' in start2)

    # 计算用于数值显示的小数位数
    if sci_format1:
        decimal1 = count_decimal_places(start1)
    else:
        decimal1 = max(count_decimal_places(start1), count_decimal_places(step1))
    if sci_format2:
        decimal2 = count_decimal_places(start2)
    else:
        decimal2 = max(count_decimal_places(start2), count_decimal_places(step2))

    # 规范化后缀（去掉用户误加的引号）
    suffix1 = _strip_quotes(suffix1) if isinstance(suffix1, str) else ''
    suffix2 = _strip_quotes(suffix2) if isinstance(suffix2, str) else ''

    base_dir = 'mesagrid'
    os.makedirs(base_dir, exist_ok=True)
    grids = []

    # 先创建目录并复制模板
    for i in range(a):
        for j in range(b):
            v1 = get_value(start1, step1, i)
            v2 = get_value(start2, step2, j)
            # 目录里的“数值部分”字符串
            v1_str_for_dir = simple_fortran_format(v1) if sci_format1 else f"{v1:.{decimal1}f}"
            v2_str_for_dir = simple_fortran_format(v2) if sci_format2 else f"{v2:.{decimal2}f}"
            dirname = f'{parameter_name_1}_{v1_str_for_dir}_{parameter_name_2}_{v2_str_for_dir}'
            dir_path = os.path.join(base_dir, dirname)
            os.makedirs(dir_path, exist_ok=True)
            shutil.copytree('mesabasic', dir_path, dirs_exist_ok=True)
            grids.append(dir_path)

    # 再写 inlist 值（根据是否有后缀，决定是否加引号）
    for i in range(a):
        for j in range(b):
            filename = os.path.join(grids[i * b + j], inlist_name)
            v1 = get_value(start1, step1, i)
            v2 = get_value(start2, step2, j)

            # 数值部分的格式化（用于字符串或纯数值）
            num1 = simple_fortran_format(v1) if sci_format1 else f"{v1:.{decimal1}f}"
            num2 = simple_fortran_format(v2) if sci_format2 else f"{v2:.{decimal2}f}"

            # param 1
            if suffix1:  # 写入带引号的字符串
                raw1 = f"'{num1}{suffix1}'"
                update_value_in_file_raw(filename, parameter_name_1, raw1)
            else:        # 纯数值（原逻辑）
                update_value_in_file(filename, parameter_name_1, v1, decimal1, sci_format=sci_format1)

            # param 2
            if suffix2:
                raw2 = f"'{num2}{suffix2}'"
                update_value_in_file_raw(filename, parameter_name_2, raw2)
            else:
                update_value_in_file(filename, parameter_name_2, v2, decimal2, sci_format=sci_format2)

def grid1D(number_of_1Dgrid, parameter_name='grid', start=0, step=1):
    """
    创建一维网格文件夹。
    
    若 start 使用科学计数法（包含 "d"），则生成的文件夹名称将由计算得到的数值通过 simple_fortran_format 格式化，
    例如输入 "1d-02" 将生成 "1d-2"；否则使用普通十进制格式。
    同时更新 inlist 文件时也按相应格式写入。
    """
    global gridname, grids
    a = int(number_of_1Dgrid)
    
    sci_format = isinstance(start, str) and ('d' in start)
    
    if sci_format:
        decimal = count_decimal_places(start)
    else:
        decimal = max(count_decimal_places(start), count_decimal_places(step))
    
    gridname = str(parameter_name)
    base_dir = './mesagrid'
    os.makedirs(base_dir, exist_ok=True)
    grids = []
    
    for i in range(a):
        value = get_value(start, step, i)
        if sci_format:
            value_str = simple_fortran_format(value)
        else:
            value_str = f"{value:.{decimal}f}"
        dir_name = f"{gridname}_{value_str}"
        dst = os.path.join(base_dir, dir_name)
        shutil.copytree('./mesabasic', dst, dirs_exist_ok=True)
        grids.append(dst)
    
    for i, path in enumerate(grids):
        filename = os.path.join(path, inlist_name)
        value = get_value(start, step, i)
        update_value_in_file(filename, parameter_name, value, decimal, sci_format=sci_format)

def get_value(start, step, i):
    start_coeff, start_exp = parse_scientific_str(start, default_coeff=1.0)
    step_coeff, step_exp   = parse_scientific_str(step, default_coeff=0.0)
    # 然后每步计算
    new_coeff = start_coeff + i * step_coeff
    new_exp   = start_exp   + i * step_exp
    return new_coeff * (10 ** new_exp)


def changevalue1D(n=None,
                  parameter_name='grid',
                  start=0, step=1,
                  suffix=''):
    """
    一维批量改值：
    - 按目录顺序（优先用全局 grids，否则 sorted(glob('./mesagrid/*/'))）从 i=0..n-1 写入；
    - 数值部分由 start/step 控制（支持 'd' 科学计数法）；
    - 若 suffix 非空 -> 写成带引号的 '数值部分+后缀'；否则写纯数值。
    - n 为 None 时自动用目录总数。
    """
    # 决定写入目录列表
    pathlist = grids if (isinstance(glids := globals().get('grids', []), list) and len(grids) > 0) else sorted(glob('./mesagrid/*/'))
    if n is None:
        n = len(pathlist)
    n = int(n)
    if n > len(pathlist):
        print(f"[warn] 期望写 {n} 个，但实际只有 {len(pathlist)} 个目录；将仅写前 {len(pathlist)} 个。")
        n = len(pathlist)

    # 是否使用 'd' 科学计数法（与 grid1D / grid2D 保持一致：看 start）
    sci_format = isinstance(start, str) and ('d' in start)

    # 小数位数
    if sci_format:
        decimal = count_decimal_places(start)
    else:
        decimal = max(count_decimal_places(start), count_decimal_places(step))

    # 处理后缀
    suffix = _strip_quotes(suffix) if isinstance(suffix, str) else ''

    # 逐目录写值
    for i in range(n):
        dir_path = pathlist[i]
        filename = os.path.join(dir_path, inlist_name)

        v = get_value(start, step, i)
        num = simple_fortran_format(v) if sci_format else f"{v:.{decimal}f}"

        if suffix:
            raw = f"'{num}{suffix}'"
            update_value_in_file_raw(filename, parameter_name, raw)
        else:
            update_value_in_file(filename, parameter_name, v, decimal, sci_format=sci_format)

def changevalue2D(a, b,
                  parameter_name_1, parameter_name_2,
                  start1=0, step1=1, start2=0, step2=1,
                  suffix1='', suffix2=''):
    """
    按二维索引 (i, j) 为已有网格批量改值：
    - 数值部分仍由 start/step 控制（支持 'd' 科学计数法）。
    - 若 suffixX 非空 -> 写成带引号的 '数值部分+后缀'；否则写纯数值（不加引号）。
    - 目录顺序优先使用全局 grids（若存在且长度匹配 a*b），否则用 sorted(glob('./mesagrid/*/'))。
    """
    a, b = int(a), int(b)

    # 判断是否使用 d 科学计数法来格式化写入（与 grid2D 保持一致：看 startX）
    sci_format1 = isinstance(start1, str) and ('d' in start1)
    sci_format2 = isinstance(start2, str) and ('d' in start2)

    # 计算小数位数（与 grid2D 一致）
    if sci_format1:
        decimal1 = count_decimal_places(start1)
    else:
        decimal1 = max(count_decimal_places(start1), count_decimal_places(step1))
    if sci_format2:
        decimal2 = count_decimal_places(start2)
    else:
        decimal2 = max(count_decimal_places(start2), count_decimal_places(step2))

    # 规范化后缀（去除误加的引号）
    suffix1 = _strip_quotes(suffix1) if isinstance(suffix1, str) else ''
    suffix2 = _strip_quotes(suffix2) if isinstance(suffix2, str) else ''

    # 选择网格目录列表
    pathlist = grids if (isinstance(glids := globals().get('grids', []), list) and len(grids) >= a*b) else sorted(glob('./mesagrid/*/'))
    if len(pathlist) < a * b:
        print(f"[warn] 目录数 {len(pathlist)} < a*b={a*b}；仅对可用目录进行写入。")

    # 逐格写值
    for i in range(a):
        for j in range(b):
            idx = i * b + j
            if idx >= len(pathlist):
                break
            dir_path = pathlist[idx]
            filename = os.path.join(dir_path, inlist_name)

            v1 = get_value(start1, step1, i)
            v2 = get_value(start2, step2, j)

            num1 = simple_fortran_format(v1) if sci_format1 else f"{v1:.{decimal1}f}"
            num2 = simple_fortran_format(v2) if sci_format2 else f"{v2:.{decimal2}f}"

            # param 1
            if suffix1:
                raw1 = f"'{num1}{suffix1}'"
                update_value_in_file_raw(filename, parameter_name_1, raw1)
            else:
                update_value_in_file(filename, parameter_name_1, v1, decimal1, sci_format=sci_format1)

            # param 2
            if suffix2:
                raw2 = f"'{num2}{suffix2}'"
                update_value_in_file_raw(filename, parameter_name_2, raw2)
            else:
                update_value_in_file(filename, parameter_name_2, v2, decimal2, sci_format=sci_format2)

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
    """
    Executable_file 可以是:
      - 字符串: 例如 're 13000'、'rn'、'script.py 123'
      - 列表:   例如 ['re', '13000']、['script.py', '123']
    """
    setcore = int(setcore)
    if setcore != 0:
        os.environ['OMP_NUM_THREADS'] = str(setcore)

    # 统一把 Executable_file 解析为 [prog, arg1, arg2, ...]
    if isinstance(Executable_file, str):
        parts = shlex.split(Executable_file)
    else:
        parts = list(Executable_file)

    if not parts:
        raise ValueError("Executable_file 不能为空")

    prog = parts[0]          # 可执行文件名（或脚本名）
    args = parts[1:]         # 参数列表

    for i in glob('./mesagrid/*/'):
        try:
            # 只给真实的文件本体加执行权限（避免把参数当文件）
            chmod_targets = ['mk', 're', 'rn', 'star']
            if prog not in chmod_targets:
                chmod_targets.append(prog)
            subprocess.run(['chmod', '700', *chmod_targets], cwd=i, check=False)

            # 先跑构建脚本
            subprocess.run(['./mk'], cwd=i, check=False)

            # 组装 nohup 命令（注意程序与参数分开）
            if prog.endswith('.py'):
                cmd = ['nohup', 'python3', prog, *args]
            else:
                # 相对路径执行：在每个子目录内执行 ./prog
                prog_path = prog if (prog.startswith('./') or os.path.isabs(prog)) else f'./{prog}'
                cmd = ['nohup', prog_path, *args]

            # 建议把 stdin 也断开，防止占着终端
            with open(os.path.join(i, 'nohup.out'), 'a') as outfile:
                subprocess.Popen(
                    cmd,
                    cwd=i,
                    stdout=outfile,
                    stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL,
                    start_new_session=True,
                    close_fds=True
                )

        except FileNotFoundError:
            print(f'文件夹不存在或缺少必要文件：{i}')
        except subprocess.CalledProcessError as e:
            print(f"在 {i} 执行命令出错: {e}")

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

def startinturn(setcore=1):#为了防止占用太多cpu，一个一个来。
    a=int(setcore)
    # 直接在Python进程中设置环境变量
    os.environ['OMP_NUM_THREADS'] = f'{a}'
    if grids == []:
        for i in glob('./mesagrid/*/'):
            os.system('cd '+i+'\nchmod 700 mk re rn star\n./mk\nnohup ./rn &\ncd ../..\n')
            os.system("echo $OMP_NUM_THREADS")
    else:   
            for i in grids:
                os.system('cd ./mesagrid/'+str(i)+'\nchmod 700 mk re rn star\n./mk\nnohup ./rn \ncd ..\n')

def start_in_group(Executable_file='rn',setcore=1,groupnumber=50):#同时运行50个程序，每结束一个，再运行一个。
    a=int(setcore)
    second_script_code =f'''
import os
import subprocess
import time
from datetime import datetime
from glob import glob
# 直接在Python进程中设置环境变量
os.environ['OMP_NUM_THREADS'] = f'{a}'
running_processes = []
dir_list = glob('./mesagrid/*/')

for dir in dir_list:
    # 当正在运行的进程数量达到限制时，等待其中一个结束
    while len(running_processes) >= {groupnumber}:
        for p in running_processes:
            if p.poll() is not None:
                running_processes.remove(p)
                break
        else:
            time.sleep(1)

    # 设置工作目录
    cwd = os.path.abspath(dir)
    # 设置权限
    subprocess.run(['chmod', '700', 'mk', 're', 'rn', 'star'], cwd=cwd)
    # 运行 './mk'
    subprocess.run(['./mk'], cwd=cwd)
    # 动态生成执行命令
    if str('{Executable_file}').endswith(".py"):
        Executable_file='python {Executable_file}'
    else:
        Executable_file = './{Executable_file}' 
    exec_cmd = [Executable_file]

    # 创建输出文件，类似于 nohup.out
    nohup_out = os.path.join(cwd, "nohup.out")
    with open(nohup_out, "a") as outfile:
        # 写入开始时间
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        outfile.write(f"Script started at: start_time\\n")
        # 启动进程
        process = subprocess.Popen(exec_cmd, stdout=outfile, stderr=subprocess.STDOUT, cwd=cwd,start_new_session=True,close_fds=True,)
        running_processes.append(process)
    '''

    # second_script_code += '''
    # # 删除自身脚本（second_script.py）
    # os.remove(__file__)
    # '''

    # 将第二个脚本写入磁盘
    with open('second_script.py', 'w') as f:
        f.write(second_script_code)

    # 判断是否是 Python 文件，动态生成 exec_cmd
    Executable_file = 'second_script.py'
    exec_cmd = ['nohup', 'python3', Executable_file] if Executable_file.endswith(".py") else ['nohup', f'./{Executable_file}']

    # 创建输出文件（类似 nohup.out）
    with open("nohup.out", "a") as outfile:
        # 写入开始时间
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        outfile.write(f"Script started at: {start_time}\n")

        # 运行第二个脚本，将输出重定向到 nohup.out
        process = subprocess.Popen(exec_cmd, stdout=outfile,stderr=subprocess.STDOUT,start_new_session=True,  close_fds=True)

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

def gather_by_keyword(history_dirname='LOGS', keyword='history'):
    dest_dir = f'./mesagrid/{keyword}'
    os.makedirs(dest_dir, exist_ok=True)

    for model_dir in glob('./mesagrid/*/'):
        src_dir = os.path.join(model_dir, history_dirname)
        if not os.path.isdir(src_dir):
            continue
        for src in glob(os.path.join(src_dir, f"*{keyword}*")):
            if os.path.isfile(src):
                dst = os.path.join(dest_dir, os.path.basename(src))
                shutil.copy2(src, dst)  # 直接覆盖
                print(f"Copied: {src} -> {dst}")

def gatherdata_indir(history_dirname = 'LOGS',dataname='history.data',format='.data'):
    
    History_dir = f'./mesagrid/{dataname}'
    # 确保HISTORY目录存在
    os.makedirs(History_dir, exist_ok=True)
    
    for i in glob('mesagrid/*/'):
        # 获取文件夹的名称，去掉尾部的 '/'
        folder_name = os.path.basename(os.path.dirname(i))
        new_file_name = folder_name + format
        
        # 构造原始和目标文件的完整路径
        original_file = os.path.join(i, history_dirname, dataname)
        target_file = os.path.join(History_dir, new_file_name)
        
        # 拷贝和重命名文件
        try:
            # 使用 shutil 来拷贝和重命名文件
            shutil.copy2(original_file, target_file)
            print(f"Copied and renamed document  to {target_file}")
        except FileNotFoundError:
            print(f"document file not found in {i}")
        except Exception as e:
            print(f"An error occurred: {e}")

def changevalue_all(keyword, new_value):
    new_value_str = str(new_value).strip()
    try:
        # Try to convert new_value to float
        num_value = float(new_value_str)
        # Check if it's an integer
        if num_value == int(num_value):
            # Integer, format without decimal point
            new_value_formatted = str(int(num_value))
        else:
            # Float, count decimal places
            decimal_places = count_decimal_places(new_value_str)
            new_value_formatted = f"{num_value:.{decimal_places}f}"
    except ValueError:
        # new_value is a string, use as-is
        new_value_formatted = new_value_str
    for i in glob('mesagrid/*/'):
        filename = os.path.join(i, f'{inlist_name}')
        try:
            update_value_in_file(filename, keyword, new_value_formatted)
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

def safe_convert(value_str):
    """
    如果字符串包含 'd'，则用科学计数法格式解析成浮点数；
    否则直接转为 float。
    """
    if isinstance(value_str, str) and 'd' in value_str:
        coeff, exp = parse_scientific_str(value_str)
        return coeff * (10 ** exp)
    else:
        return float(value_str)

def gui_format_value(value_str):
    """
    如果输入值中包含 'd'（即科学计数法形式），则转换成普通十进制字符串用于 GUI 显示，
    否则原样返回。
    """
    try:
        # 如果含有 'd'，转换为 float，再以普通字符串形式返回
        if isinstance(value_str, str) and 'd' in value_str:
            num = safe_convert(value_str)
            # 此处可根据需要调整显示格式，比如保留合适的小数位
            return f"{num}"
    except Exception:
        pass
    return value_str

def create_gui_for_function(frame, func, column):
    subframe = tk.Frame(frame)
    # 使用 grid 管理 subframe 的布局
    grid_row = column // 4
    grid_col = column % 4
    subframe.grid(row=grid_row, column=grid_col, padx=10, pady=10, sticky='nw')

    tk.Label(subframe, text=f"Function: {func.__name__}").grid(sticky="w")

    params = inspect.signature(func).parameters
    entries = {}

    for index, param in enumerate(params.values()):
        row = tk.Frame(subframe)
        row.grid(row=index + 1, column=0, sticky="ew", padx=5, pady=5)
        tk.Label(row, text=param.name + ":").pack(side=tk.LEFT)
        entry = tk.Entry(row)
        entry.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        if param.default != param.empty:
            # 直接显示原始默认值（保持例如 "1d-10" 这样的格式）
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
    """
    统计小数位数。如果 number 为 'd' 形式，则只统计系数部分。
    """
    if isinstance(number, str) and 'd' in number:
        parts = number.split('d')
        coeff_str = parts[0] if parts[0] else "1.0"
        try:
            coeff = Decimal(coeff_str)  # 只解析系数部分
            num_str = format(coeff, 'f')
            return len(num_str.split('.')[1]) if '.' in num_str else 0
        except:
            raise ValueError(f"无法解析小数位数: {number}")
    else:
        try:
            d = Decimal(str(number))
            num_str = format(d, 'f')
            return len(num_str.split('.')[1]) if '.' in num_str else 0
        except:
            raise ValueError(f"无法解析小数位数: {number}")
    
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

def check_termination_codes():
    """
    Check all nohup.out files in ./mesagrid/*/ directories for 'termination code:' string.
    Prints directories where the string is not found.
    """
    missing_termination_dirs = []
    
    for dir_path in glob('./mesagrid/*/'):
        nohup_file = os.path.join(dir_path, 'nohup.out')
        
        if not os.path.exists(nohup_file):
            missing_termination_dirs.append((dir_path, "nohup.out file not found"))
            continue
            
        try:
            with open(nohup_file, 'r') as f:
                content = f.read()
                if "termination code:" not in content:
                    missing_termination_dirs.append((dir_path, "termination code not found"))
        except Exception as e:
            missing_termination_dirs.append((dir_path, f"error reading file: {str(e)}"))
    
    if missing_termination_dirs:
        print("Directories without 'termination code:' in nohup.out:")
        for dir_path, reason in missing_termination_dirs:
            print(f"- {dir_path} ({reason})")
    else:
        print("All directories contain 'termination code:' in their nohup.out files")
    
    return missing_termination_dirs

if __name__ == "__main__":
    main()