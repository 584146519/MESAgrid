MESA Grid GUI Program

English instruction ：

The program files are named using a convention of numbers (major versions) + letters (minor versions). For example, version 36 is newer than version 35, and version 36c is newer than version 36b. You only need to download the latest version of a single .py file.

Version 40 allow command-line execution.
Version 43 allow crate grid in Scientific notation.(like 3d-5)

Preparation steps:

Step 0: Ensure that all imported packages are installed; all can be installed using pip.

Step 1: Place all the initial model files of the grid into the mesabasic folder (in other words, rename the mother-folder containing the initial model files to mesabasic).

Step 2: Run this program in the parent directory of the mesabasic folder.Enter the name of the inlist you want to change into the first function and click the run button

Steps for use:

One-dimensional Grid:
If only one parameter is adjusted, use grid1D to create the grid. The program will generate a mesagrid folder next to the mesabasic folder, which will contain the grid models. Afterward, use startall to start everything. Once started, the program can be closed.

Two-dimensional Grid:
Use grid2D to create the grid. For variables that exceed two but are related (essentially still a two-dimensional grid), use replaceline2D to modify the inlist.

To Start:
Afterward, use startall to start everything. Once started, the program can be closed.

You can use replaceline, replaceline2D, insert_line, and changevalue_all to change the values of all inlist.

The functions I find most commonly used are:
AAAAAAA_initialize_variables, makemesadir, mkmesadir2D, replaceline2D, startall, startnumber, stopall, and gethistorydata.

Finally:
It’s very simple for everyone to update the master code on their own. You only need to define a function directly, and the function’s area and execution button will be generated in the GUI or command line.

中文说明

MESA 网格可视化程序 
程序文件命名规则是数字（大版本）+字母（小版本），例如 36 比 35 版本新，36c 比 36b 版本新，只下载最新版单个 py 文件即可
40版本增加允许使用命令行来执行本程序
43版本创建网格可以用科学计数法（比如3d-5）

准备操作如下：

step0 确保安装所有的 import 的包,全部可以使用pip安装

step1 把网格初始的模型文件全部放进 mesabasic 的文件夹中（换句话说把初始模型的文件夹名称改为 mesabasic）

step2 在 mesabasic 的上级文件夹内运行该程序，把需要改的inlist的名字输入到第一个函数中并点击run按钮




正式使用步骤如下：

一维网格:
如果只调整一个参数，使用 grid1D 创建网格，程序会在 mesabaisc 文件夹旁边生成 mesagrid 文件夹里面放网格模型
，之后使用 startall 来全部开始，开始后本程序可以关闭

二维网格:
使用 grid2D 创建网格
对于需要改变的变量超过二个但是具有相关性的变量（本质还是二维网格），使用replaceline2D更改 inlist

开始：
之后使用 startall 来全部开始，开始后本程序可以关闭

可以使用replaceline、replaceline2D、insert_line 以及changevalue_all来改变全体 inlist 的值
我认为最常用的函数为：
AAAAAAA_initialize_variables、makemesadir、mkmesadir2D、replaceline2D、startall、startnumber、stopall、gethistorydata

<img width="344" alt="image" src="https://github.com/user-attachments/assets/ec1559df-24c4-488f-97fa-69bcea104f07" />

![image](https://github.com/user-attachments/assets/0ea34491-6f9e-43cf-81b8-b7a886b74af4)


![截屏2025-02-27 11 49 43](https://github.com/user-attachments/assets/0c8201ac-d63c-4a0c-a62e-74d4be062a53)

最后：
大家对 master 代码进行自己的更新是非常简单的，只需要直接定义函数就会有函数的区域和执行函数的按钮生成在 GUI 或者命令行中
