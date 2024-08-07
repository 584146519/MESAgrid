文件命名规则是数字（大版本）+字母（小版本），例如 36 比 35 版本新，36c 比 36b 版本新，只下载最新版单个 py 文件即可

这是一个可以设定运行 mesa 网格的程序包，准备操作如下

0 安装所有的 import 的包,全部可以使用pip安装

1把网格初始的模型文件全部放进 mesabasic 的文件夹中（换句话说把初始模型的文件夹名称改为 mesabasic）

2 在 mesabasic 的上级文件夹内运行该程序




正式使用步骤如下：

如果只调整一个参数即一维网格，使用 makemesadir 创建网格，会在 mesabaisc 文件夹旁边生成 mesagrid 文件夹里面放网格模型
，之后使用 startall 来全部开始，开始后本程序可以关闭

制作二维网格使用 mkmesadir2D 创建网格

使用replaceline2D来改变变量，对于需要改变的变量超过二个但是具有相关性的变量（本质还是二维网格），多次使用replaceline2D即可
之后使用 startall 来全部开始，开始后本程序可以关闭

可以使用replaceline、replaceline2D、insert_line 以及changevalue_all来改变全体 inlist 的值

我认为最常用的函数为：
AAAAAAA_initialize_variables、makemesadir、mkmesadir2D、replaceline2D、startall、startnumber、stopall、gethistorydata



最后：
大家对 master 代码进行自己的更新是非常简单的，只需要直接定义函数就会有函数的区域和执行函数的按钮生成在 GUI 界面中

