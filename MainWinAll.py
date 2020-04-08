# coding=utf-8
import os
import sys
import time
import math
import random
import pandas as pd
import numpy as np
import qtawesome
import qdarkstyle
import traceback
import xlsxwriter
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


# 工具函数
# 将excel文件读入到list中
def ReadExcelToList(filepath="", hasNan=True):
    if not hasNan:
        result = []
        result += pd.read_excel(io=filepath, header=None).values.tolist()
    else:  # 每一行的数据长度不一致，且nan在正常数据最后
        dataFrame = pd.read_excel(io=filepath, header=None)
        result = [dataFrame.values[0].tolist()]  # 处理表头
        data = dataFrame.values[1:]
        for item in data:
            # 全部是nan
            if isinstance(item[0], float) and math.isnan(item[0]):
                result.append([])
                continue
            # 后面一部分是nan
            flag = False
            for i in range(len(item)):
                if isinstance(item[i], str):
                    continue
                if math.isnan(item[i]):
                    result.append(item[:i].tolist())
                    flag = True
                    break
            # 全部不是nan
            if not flag:
                result.append(item.tolist())

    return result
# 负责将数据写入xlsx文件
def WriteDataToExcel(data, filename):
    """
    :param data: 每一行是一组数据，第一行是表头
    :return:
    """
    # 新建excel表
    workbook = xlsxwriter.Workbook(filename)
    # 创建sheet，默认名称sheet1
    worksheet = workbook.add_worksheet()
    # 数据写入excel
    for i in range(len(data)):
        worksheet.write_row("A{}".format(i + 1), data[i])
    # 将excel文件保存关闭，如果没有这一行运行代码会报错
    workbook.close()
# 负责创建文件夹，要求此文件必须和其他的py文件目录同级
def CreateDirectory(outputFilesPath="", directoryPath="", subDirectory=""):
    if outputFilesPath == "" and directoryPath == "":
        return

    # 默认的文件输出路径
    if outputFilesPath == "":
        if not os.path.exists(directoryPath + subDirectory):
            os.makedirs(directoryPath + subDirectory)
            if ConstValues.PsIsDebug:
                print("文件夹 " + directoryPath + subDirectory + " 不存在，创建成功......")
        return directoryPath + subDirectory
    else:  # 用户选择的文件输出路径
        if not os.path.exists(outputFilesPath + subDirectory):
            os.makedirs(outputFilesPath + subDirectory)
            if ConstValues.PsIsDebug:
                print("文件夹 " + outputFilesPath + subDirectory + "不存在，创建成功......")
        return outputFilesPath + subDirectory

# 一些常量
class ConstValues:
    def __init__(self):
        pass

    # 用于打开调试
    PsIsDebug = False
    # 用于是否可以单独运行
    PsIsSingleRun = False
    # 主窗口名称
    PsMainWindowTitle = "石油组学软件"
    # 主窗口单位长度
    PsMainWindowLength = 100
    # 主窗口宽度
    PsMainWindowWidth = PsMainWindowLength * 12
    # 主窗口高度
    PsMainWindowHeight = PsMainWindowLength * 8
    # 主窗口底部状态栏显示的信息
    PsMainWindowStatusMessage = "欢迎使用！"
    # 主窗口风格  可选：["Windows", "Fusion", "Macintosh", "Qdarkstyle"]
    PsMainWindowStyle = "Qdarkstyle"
    # 主窗口背景样式（背景颜色RGB）
    PsMainBackgroundStyle = "#MainWindow{background-color: #F5F5F5;}"  # 白烟色
    # PsMainBackgroundStyle = "#MainWindow{border-image:url(./images/test.jpg);}}"  # 背景图片
    # 状态栏背景样式（颜色RGB）
    PsStatusStyle = "background-color: #DCDCDC;"
    # 主界面显示的字体及大小
    PsMainFontType = "Arial"
    PsMainFontSize = 12
    # 下拉菜单显示的字体及大小
    PsMenuFontType = "Arial"
    PsMenuFontSize = 10.5
    # 工具栏显示的字体及大小
    PsToolbarFontType = "Arial"
    PsToolbarFontSize = 10
    # 状态栏显示的字体及大小
    PsStatusFontType = "Arial"
    PsStatusFontSize = 11
    # 主界面树控件显示的字体及大小
    PsTreeFontType = "Arial"
    PsTreeFontSize = 11
    # 运行提示框弹出时间 1 -> 1s
    PsPromptBoxTime = 2
    # 图标系统  1:从图片读取  2:来自 qtawesome
    PsIconType = 2
    PsIconLoading = './__system/images/basic/ajax-loading.gif'  # 正在运行gif
    # 从图片读取
    PsWindowIcon = './__system/images/basic/Dragon.ico'  # 窗口弹出的图标所在的位置
    PsIconOpenFile = './__system/images/basic/open.png'  # 打开文件图标
    PsIconExit = './__system/images/basic/close.ico'  # 退出软件图标
    PsIconDeleteBlank = './__system/images/work/j1.png'  # 删空白图标
    PsIconGDB = './__system/images/work/j2.png'  # 数据库生成图标
    PsIcondelIso = './__system/images/work/j3.png'  # 去同位素图标
    PsIconpeakDis = './__system/images/work/j4.png'  # 峰识别图标
    PsIconRemoveFP = './__system/images/work/j5.png'  # 去假阳性图标
    PsIconpeakDiv = './__system/images/work/j6.png'  # 峰检测图标
    PsIconPlot = './__system/images/work/j7.png'  # 绘图图标
    PsIconHelpEdit = "./__system/images/basic/Sorceress.ico"  # 帮助图标：编辑
    PsIconHelpOther = "./__system/images/basic/Logo.ico"  # 帮助图标：其他帮助
    PsIconHelpAbout = "./__system/images/basic/help.png"  # 帮助图标：about
    PsIconAllStart = './__system/images/work/j21.png'  # 全部开始图标
    PsIconAllReset = './__system/images/work/j12.png'  # 重置软件图标
    PsIconBack = "./__system/images/basic/back.png"
    # 来自 qtawesome 网址：https://fontawesome.dashgame.com/
    PsqtaColor = "black"
    PsqtaWindowIconColor = "red"
    PsqtaIconFolderColor = "black"
    PsqtaWindowIcon = 'fa.fire'  # 窗口弹出的图标
    PsqtaIconOpenFileExcel = 'fa.file-excel-o'  # 打开Excel文件图标
    PsqtaIconOpenFileTxt = 'fa.file-text-o'  # 打开Txt文件图标
    PsqtaIconOpenFileOut = 'fa.folder-open-o'  # 输出到文件夹图标
    PsqtaIconExit = 'fa.window-close-o'  # 退出软件图标
    PsqtaIconDeleteBlank = 'fa.trash-o'  # 删空白图标
    PsqtaIconGDB = 'fa.database'  # 数据库生成图标
    PsqtaIcondelIso = 'fa.search'  # 去同位素图标
    PsqtaIconpeakDis = 'fa.wheelchair'  # 峰识别图标
    PsqtaIconRemoveFP = 'fa.trash-o'  # 去假阳性图标
    PsqtaIconpeakDiv = 'fa.search'  # 峰检测图标
    PsqtaIconPlot = 'fa.bar-chart-o'  # 绘图图标
    PsqtathemeMacintosh = "fa.plane"  # 主题图标
    PsqtathemeQdarkstyle = "fa.rocket"
    PsqtathemeWindows = "fa.ship"
    PsqtathemeFusion = "fa.train"
    PsqtaIconHelpWindows = "fa.windows"  # 帮助图标：界面介绍
    PsqtaIconHelpEdit = "fa.edit"  # 帮助图标：编辑
    PsqtaIconHelpOther = "fa.star-o"  # 帮助图标：其他帮助
    PsqtaIconHelpAbout = "fa.heart-o"  # 帮助图标：功能介绍
    PsqtaIconAllStart = 'fa.play-circle-o'  # 全部开始图标
    PsqtaIconAllReset = 'fa.refresh'  # 重置软件图标
    PsqtaIconBack = "fa.arrow-left"  # 返回上一级图标
    PsqtaIconTreeFolder = "fa.folder-o"  # 树控件文件夹
    PsqtaIconTreeImage = "fa.file-image-o"  # 树控件文件夹

    # 左侧树结构二级目录名称
    PsTreeProject = "石油组学数据"
    PsTreeInputFiles = "输入文件"
    PsTreeDeleteBlank = "去空白结果"
    PsTreeGDB = "数据库生成结果"
    PsTreeDelIso = "搜同位素结果"
    PsTreePeakDis = "峰提取结果"
    PsTreeRemoveFP = "去假阳性结果"
    PsTreePeakDiv = "峰检测结果"
    PsTreePlot = "绘图结果"
    PsTreePlotInit = "initShow"
    # 生成的文件名称
    PsNameDeleteBlank = "__DeleteBlank.xlsx"
    PsNameGDB = "__GDB.xlsx"
    PsNameDeleteIsotope = "__FindIsotope.xlsx"
    PsNamePeakDistinguish = "__PeakDistinguish.xlsx"  # 原始名称 PeakDisPart1.xlsx
    PsNameRemoveFPFrom_DelIsoResult = "__RemoveFPFrom_DelIsoResult.xlsx"
    PsNameRemoveFPFrom_PeakDisResult = "__RemoveFPFrom_PeakDisResult.xlsx"
    PsNamePeakDivision = "__PeakDivision.xlsx"

    # 运行模式
    # 1：去空白 --> 数据库生成 --> 搜同位素 --> 去假阳性
    # 2：去空白 --> 数据库生成 --> 搜同位素 --> 峰提取 --> 去假阳性
    # 3：去空白 --> 数据库生成 --> 搜同位素 --> 峰提取 --> 去假阳性 --> 峰检测
    # 4：数据库生成 --> 搜同位素 --> 去假阳性
    # 5：数据库生成 --> 搜同位素 --> 峰提取 --> 去假阳性
    # 6：数据库生成 --> 搜同位素 --> 峰提取 --> 去假阳性 --> 峰检测
    PsStartMode = 1

    # 处理过程中是否显示弹框
    PsIsShowGif = True

    # 扣空白错误提示信息
    PsDeleteBlankErrorMessage = "请选择需要处理的样本文件、空白文件和总离子流图文件!"
    # 去同位素错误提示信息
    PsDeleteIsotopeErrorMessage = "请先扣空白和生成数据库!"
    # 峰识别错误提示信息
    PsPeakDistinguishErrorMessage1 = "请选择需要处理的总离子流图文件!"
    PsPeakDistinguishErrorMessage2 = "请先去同位素!"
    # 去假阳性提示信息
    PsRemoveFPErrorMessage1 = "请先去同位素!"
    PsRemoveFPErrorMessage2 = "请先峰识别!"
    # 峰检测提示信息
    PsPeakDivErrorMessage = "请先去假阳性!"
    # 画图提示信息
    PsPlotErrorMessage = "请先去假阳性!"

    # 样本文件和空白文件header所在excel中的行数：PsHeaderLine = excel.header - 1
    PsHeaderLine = 7
    # 主页面最多显示的表格行数
    PsMainMaxRowNum = 10000
    # 读入文件默认目录
    PsReadFileDefaultDirectoy = "./inputData/test"

    # 设置框字体以及大小
    PsSetupFontType = "Arial"
    PsSetupFontSize = 12
    PsSetupStyleEnabled = True  # 默认颜色是否使能
    PsSetupStyle = "background-color: #F0F0F0;"  # 默认颜色
    # PsSetupStyle = "background-color: #F5F5F5;"

    # 扣空白设置默认参数
    # 1~9999（整数）
    PsDeleteBlankIntensity = 1000
    PsDeleteBlankIntensityMin = 0
    PsDeleteBlankIntensityMax = 10000
    # 0.0~100.0（浮点数）
    PsDeleteBlankPPM = 1.0  # 单位ppm
    PsDeleteBlankPPMMin = 0.0
    PsDeleteBlankPPMMax = 100.0
    # 0~100（整数）
    PsDeleteBlankPercentage = 50  # 50%
    PsDeleteBlankPercentageMin = 0
    PsDeleteBlankPercentageMax = 100

    # 数据库生成设置默认参数
    # PsGDBClass = ["N1", "N1O1", "N1S1", "CH"]  # 数据库生成(参数)：Class类型
    PsGDBClass = ["N1", "N1O1", "CH", "N2", "N1S1", "N1O2", "O1S1", "O1", "O2", "O3"]  # 四组需要测试的数据
    # 1~100（整数）
    PsGDBCarbonRangeLow = 1  # 数据库生成(参数)：carbon rage(碳数范围)最小值(包含)
    PsGDBCarbonRangeHigh = 100  # 数据库生成(参数)：carbon rage(碳数范围)最大值(包含)
    PsGDBCarbonRangeMin = 1
    PsGDBCarbonRangeMax = 1000
    # 1~30（整数）
    PsGDBDBERageLow = 1  # 数据库生成(参数)：DBE rage(不饱和度范围)最小值(包含)
    PsGDBDBERageHigh = 30  # 数据库生成(参数)：DBE rage(不饱和度范围)最大值(包含)
    PsGDBDBERageMin = 0
    PsGDBDBERageMax = 50
    # 50~1500(整数)
    PsGDBM_ZRageLow = 150  # 数据库生成(参数)：m/z rage(质荷比范围)最小值(包含)
    PsGDBM_ZRageHigh = 2000  # 数据库生成(参数)：m/z rage(质荷比范围)最大值(包含)
    PsGDBM_ZRageMin = 50
    PsGDBM_ZRageMax = 5000
    # 离子类型
    PsGDB_MHPostive = True  # 数据库生成(参数)：正离子，是否选择[M+H]+，True为选中
    PsGDB_MPostive = False  # 数据库生成(参数)：正离子，是否选择M+，True为选中
    PsGDB_MHNegative = False  # 数据库生成(参数)：负离子，是否选择[M-H]-，True为选中
    PsGDB_MNegative = False  # 数据库生成(参数)：负离子，是否选择M-，True为选中

    # 去同位素设置默认参数
    # 0~正无穷（整数）
    PsDelIsoIntensityX = 100000
    PsDelIsoIntensityXMin = 0
    PsDelIsoIntensityXMax = 200000000
    PsDelIsoIntensityXMaxStr = "2e8"  # 方便设置界面显示
    # 0~100（整数）
    PsDelIso_13C2RelativeIntensity = 20  # 20%
    PsDelIso_13C2RelativeIntensityMin = 0
    PsDelIso_13C2RelativeIntensityMax = 100
    # 0.00~20.00（浮点数）
    PsDelIsoMassDeviation = 2.0  # 单位ppm
    PsDelIsoMassDeviationMin = 0.0  # 单位ppm
    PsDelIsoMassDeviationMax = 20.0  # 单位ppm
    # 0.00~20.00（浮点数）
    PsDelIsoIsotopeMassDeviation = 2.0  # 单位ppm
    PsDelIsoIsotopeMassDeviationMin = 0.0
    PsDelIsoIsotopeMassDeviationMax = 20.0
    # 0~100（整数）
    PsDelIsoIsotopeIntensityDeviation = 30  # 30%
    PsDelIsoIsotopeIntensityDeviationMin = 0
    PsDelIsoIsotopeIntensityDeviationMax = 100

    # 峰识别设置默认参数
    # 0~10000（整数）
    PsPeakDisContinuityNum = 60  # 第一部分参数
    PsPeakDisContinuityNumMin = 0
    PsPeakDisContinuityNumMax = 10000
    # 0.00~100.00（浮点数）
    PsPeakDisMassDeviation = 2.0
    PsPeakDisMassDeviationMin = 0.0
    PsPeakDisMassDeviationMax = 100.0
    # 0~30(整数)
    PsPeakDisDiscontinuityPointNum = 5
    PsPeakDisDiscontinuityPointNumMin = 0
    PsPeakDisDiscontinuityPointNumMax = 30
    # 输入字符串
    PsPeakDisClassIsNeed = True  # 第二部分，是否需要峰检测与分割，即将多个峰分开输出
    # PsPeakDisClass = ["N1"]  # PsPeakDisClassIsNeed为False是此字段不起作用
    PsPeakDisClass = ["N1", "N1O1"]  # PsPeakDisClassIsNeed为False是此字段不起作用

    # 去假阳性设置默认参数
    PsRemoveFPId = 2  # 默认处理的内容
    # 1~100（整数）
    PsRemoveFPContinue_CNum = 3
    PsRemoveFPContinue_CNumMin = 1
    PsRemoveFPContinue_CNumMax = 100
    # 1~100（整数）
    PsRemoveFPContinue_DBENum = 2
    PsRemoveFPContinue_DBENumMin = 1
    PsRemoveFPContinue_DBENumMax = 100

    # 峰检测全过程所需要的数据，必须 PsPeakDisClassIsNeed=True，峰检测过程才有效
    # 0~1000000(整数)
    PsPeakDivNoiseThreshold = 15000  # 噪音阈值
    PsPeakDivNoiseThresholdMin = 0
    PsPeakDivNoiseThresholdMax = 1000000
    PsPeakDivNoiseThresholdMaxStr = "1e6"  # 方便设置界面显示
    # 0.0~100.0(浮点数)
    PsPeakDivRelIntensity = 2.0  # 相对强度阈值，去每张图中，相对强度小于最高峰的0.1%的那些信号
    PsPeakDivRelIntensityMin = 0.0
    PsPeakDivRelIntensityMax = 100.0
    # 该参数决定是否需要将溶剂效应的第一个峰融合到第二个峰
    PsPeakDivNeedMerge = True
    # 该参数决定是否生成图片信息
    PsPeakDivNeedGenImage = True

    # 峰检测全过程所需要的数据
    PsPlotTitleName = "plot"  # 标题名称
    PsPlotTitleColor = (255, 0, 0, 255)  # 标题颜色，(R, G, B, Alpha)
    PsPlotXAxisName = "x"  # x轴名称
    PsPlotXAxisColor = (0, 0, 255, 255)  # x轴颜色，(R, G, B, Alpha)
    PsPlotYAxisName = "y"  # y轴名称
    PsPlotYAxisColor = (0, 0, 255, 255)  # y轴颜色，(R, G, B, Alpha)
    PsPlotHasEnter = False  # 记录是否进入过PlotSetup()函数，并且确认
    PsPlotType = 1  # 1~6(整数)
    PsPlotClassList = []  # 需要绘制的类型，多选
    PsPlotClassItem = []  # 需要绘制的类型，单选
    PsPlotDBENum = -1
    PsPlotConfirm = False  # 用户是否确认要画图

    # 初始化显示图片列表，必须在./__system/images/show文件夹中
    PstitleList = [
            "sky.png",
            "people.png",
            "dandelion.png",
            "lake.png",
            "botchi.png",
            "castle.png",
            "flower.png",
            "sea.png",
            "road.png",
            "hand.png",
            "book.png",
            "notebook.png",
        ]
    # 初始化是否是只显示指定数目图片，大于图片总数目则全部显示
    PsShowImageNum = 2

    # 软件版本
    """
    v1.2相对于v1.1更改3处错误：
        （1）MultiThread之前需要更新列表数据
        （2）ClassPeakDivision中if len(ContinueItem) == 1:之后不应改变area
        （3）ClassDeleteIsotope更改第三个判断条件
    """
    PsSoftwareEdition = "v1.2"

# 弹出对话框
class PromptBox:
    def __init__(self):
        pass

    """
    1.关于对话框
    2.错误对话框
    3.警告对话框
    4.提问对话框
    5.消息对话框
    """
    # 1.关于对话框
    def aboutMessage(self, message):
        # 创建对话框
        dialog = QDialog()
        QMessageBox.about(dialog, '关于', message)

    # 2.错误对话框
    def errorMessage(self, message):
        # 创建对话框
        dialog = QDialog()
        reply = QMessageBox.critical(dialog, '错误', message, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        # reply = QMessageBox.critical(dialog, '警告', message, QMessageBox.Yes)
        return reply == QMessageBox.Yes

    # 3.警告对话框
    def warningMessage(self, message):
        # 创建对话框
        dialog = QDialog()
        reply = QMessageBox.warning(dialog, '警告', message, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        # reply = QMessageBox.warning(dialog, '警告', message, QMessageBox.Yes)
        return reply == QMessageBox.Yes

    # 4.提问对话框
    def questionMessage(self, message):
        # 创建对话框
        dialog = QDialog()
        reply = QMessageBox.question(dialog, '疑问', message, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        # reply = QMessageBox.question(dialog, '警告', message, QMessageBox.Yes)
        return reply == QMessageBox.Yes

    # 5.消息对话框
    def informationMessage(self, message):
        # 创建对话框
        dialog = QDialog()
        reply = QMessageBox.information(dialog, '消息', message, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        return reply == QMessageBox.Yes

    # 一定时间后自动关闭消息对话框
    def informationMessageAutoClose(self, message, second):
        """
        :param message: 显示的信息
        :param second: 秒数
        :return:
        """
        infoBox = QMessageBox()  # Message Box that doesn't run
        infoBox.setIcon(QMessageBox.Information)
        infoBox.setText(message)
        infoBox.setWindowTitle("Information")
        infoBox.setStandardButtons(QMessageBox.Ok)
        infoBox.button(QMessageBox.Ok).animateClick(second * 1000)  # second秒自动关闭
        infoBox.exec_()

    # 显示图片
    def showImage(self, title, filename):
        """
        :param title: 窗口名称
        :param filename: 图片路径
        :return:
        """
        # 创建对话框
        self.imageDialog = QDialog()
        # 设置对话框名称
        self.imageDialog.setWindowTitle(title)
        # 设置对话框图标
        if ConstValues.PsIconType == 1:
            self.imageDialog.setWindowIcon(QIcon(ConstValues.PsWindowIcon))
        elif ConstValues.PsIconType == 2:
            self.imageDialog.setWindowIcon(qtawesome.icon(ConstValues.PsqtaWindowIcon, color=ConstValues.PsqtaWindowIconColor))
        # 设置对话框弹出后后面的界面不可用
        self.imageDialog.setWindowModality(Qt.ApplicationModal)
        # 创建image标签
        imageLabel = QLabel()
        imageLabel.setPixmap(QPixmap(filename))
        # 将image标签放到layout中
        layout = QVBoxLayout()
        layout.addWidget(imageLabel)
        # 将layout标签放到dialog中
        self.imageDialog.setLayout(layout)
        # 保证提示框一直出现
        self.imageDialog.exec()

    # 显示gif
    def showGif(self, title, filename):
        """
        :param title: 窗口名称
        :param filename: gif路径
        :return:
        """
        # 创建对话框
        self.gifDialog = QDialog()
        # 设置对话框图标
        if ConstValues.PsIconType == 1:
            self.gifDialog.setWindowIcon(QIcon(ConstValues.PsWindowIcon))
        elif ConstValues.PsIconType == 2:
            self.gifDialog.setWindowIcon(qtawesome.icon(ConstValues.PsqtaWindowIcon, color=ConstValues.PsqtaWindowIconColor))
        # 设置窗口状态
        # self.gifDialog.setWindowFlags(Qt.WindowCloseButtonHint)  # 只显示叉号
        self.gifDialog.setWindowFlags(Qt.WindowMaximizeButtonHint| Qt.MSWindowsFixedSizeDialogHint)  # 禁止使用叉号
        # 设置对话框名称
        self.gifDialog.setWindowTitle(title)
        # 设置对话框弹出后后面的界面不可用
        self.gifDialog.setWindowModality(Qt.ApplicationModal)
        # gif标签
        gifLabel = QLabel()
        self.gifQMovie = QMovie(filename)
        gifLabel.setMovie(self.gifQMovie)
        self.gifQMovie.start()
        # 将gif标签放到layout中
        layout = QVBoxLayout()
        layout.addWidget(gifLabel)
        # 将layout标签放到dialog中
        self.gifDialog.setLayout(layout)
        # 保证提示框一直出现
        self.gifDialog.exec()

    # 关闭gif
    def closeGif(self):
        self.gifDialog.close()

# 主界面
class MainWin(QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()
        self.initUI()

    # 初始化主窗口
    def initUI(self):
        # 全局数据初始化
        self.dataInit()
        # 主窗口初始设置
        self.mainWinInit()
        # 使主窗口居中
        self.center()
        # 创建主窗口菜单栏（下拉菜单栏）
        self.menu()
        # 设置工具栏
        self.toolbar()
        # 设置主窗口底部状态栏
        self.status()

    # 主窗口初始设置
    def mainWinInit(self):
        # 设置主窗口的标题
        self.setWindowTitle(ConstValues.PsMainWindowTitle)
        # 设置主窗口的尺寸
        self.setFixedSize(ConstValues.PsMainWindowWidth, ConstValues.PsMainWindowHeight)
        # 设置主窗口风格
        app = QApplication.instance()
        self.MainWindowsStyle = ConstValues.PsMainWindowStyle
        styleList = ["Windows", "Fusion", "Macintosh", "Qdarkstyle"]
        try:
            with open("./__system/config.txt", "r") as f:
                style = f.read()
            if style in styleList:
                self.MainWindowsStyle = style
        except Exception as e:
            if ConstValues.PsIsDebug:
                print("Error_ReadConfig : ", e)
                # PromptBox().errorMessage("出现错误！错误标识：Error_ReadConfig")
                traceback.print_exc()

        if self.MainWindowsStyle == "Qdarkstyle":
            app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        else:
            app.setStyle(self.MainWindowsStyle)
        # 设置窗口样式
        self.setWindowFlags(Qt.WindowMinimizeButtonHint  # 最小化
                            | Qt.WindowCloseButtonHint  # 关闭
                            )
        # 创建主窗口应用的图标
        if ConstValues.PsIconType == 1:
            self.setWindowIcon(QIcon(ConstValues.PsWindowIcon))
        elif ConstValues.PsIconType == 2:
            self.setWindowIcon(qtawesome.icon(ConstValues.PsqtaWindowIcon, color=ConstValues.PsqtaWindowIconColor))
        # 设置背景颜色
        self.setObjectName("MainWindow")
        if self.MainWindowsStyle != "Qdarkstyle":
            self.setStyleSheet(ConstValues.PsMainBackgroundStyle)
        # 设置透明度
        self.setWindowOpacity(0.98)
        # 设置窗口显示内容
        self.initShow()
        # 显示主窗口
        self.show()

    # -------------------------------------- 设置窗口显示内容
    def initShow(self):
        # initShow 初始化数据
        self.initShowDataInit()

        # 主界面添加 QWidget，QWidget 中添加 Layout
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.Layout = QGridLayout(self.centralwidget)

        # self.Layout 添加控件
        self.MainLayoutAddWidget()

    # initShow 初始化数据
    def initShowDataInit(self):
        # 样本文件名称，长度恒为一，空白文件和TIC同理
        self.sampleNameList = [None]
        self.blankNameList = [None]
        self.TICNameList = [None]
        # 主界面读取文件名称列表，读入相同名称的文件时，需要确认是否覆盖
        self.mainDataNameSet = set()  # 当前显示表格名称集合，里面全是字符串，可增可减，因为用户可能点击叉号
        self.mainDataNameSetAll = set()  # 所有可能需要显示的表格名称集合，里面全是字符串，只增不减
        self.mainNeedCover = False
        # 主界面生成图形后的图形名称列表，读入相同名称的图片名称时，需要确认是否覆盖
        self.mainPlotNameSetAll = set()  # 所有可能需要显示的图片名称集合，里面全是字符串，只增不减
        self.mainPlotNeedCover = False

    # self.Layout 添加控件
    def MainLayoutAddWidget(self):
        # 创建左右两边Widget框
        self.mainTreeWidget = QTreeWidget()  # 树控件，左边
        self.mainTreeWidget.setColumnCount(1)
        self.mainTreeWidget.setHeaderLabel("Project")
        self.mainTreeWidget.header().setMinimumSectionSize(500)  # 杜文文件名太长，设置这一句有水平滚动条
        self.mainTreeWidget.setFont(QFont(ConstValues.PsTreeFontType, ConstValues.PsTreeFontSize))  # 设置字体和大小
        self.mainTreeWidget.setContextMenuPolicy(Qt.CustomContextMenu)  # 开放右键策略
        self.mainTreeWidget.customContextMenuRequested.connect(self.rightTreeShow)
        self.plotStack = QStackedWidget()  # 堆栈窗口控件，右边
        # 主窗口放置左右两大控件
        self.Layout.addWidget(self.mainTreeWidget, 0, 0, 1, 2)
        self.Layout.addWidget(self.plotStack, 0, 2, 1, 8)

        # 树控件设置根节点
        self.mainTreeRoot = QTreeWidgetItem(self.mainTreeWidget)
        self.mainTreeRoot.setText(0, ConstValues.PsTreeProject)
        self.mainTreeRoot.setIcon(0,
                                  qtawesome.icon(ConstValues.PsqtaWindowIcon, color=ConstValues.PsqtaWindowIconColor))
        # 树控件创建子节点
        self.mainTreeChild1 = QTreeWidgetItem(self.mainTreeRoot)
        self.mainTreeChild2 = QTreeWidgetItem(self.mainTreeRoot)
        self.mainTreeChild3 = QTreeWidgetItem(self.mainTreeRoot)
        self.mainTreeChild4 = QTreeWidgetItem(self.mainTreeRoot)
        self.mainTreeChild5 = QTreeWidgetItem(self.mainTreeRoot)
        self.mainTreeChild6 = QTreeWidgetItem(self.mainTreeRoot)
        self.mainTreeChild7 = QTreeWidgetItem(self.mainTreeRoot)
        self.mainTreeChild8 = QTreeWidgetItem(self.mainTreeRoot)

        # 设置显示的文字，设置图标
        treeChildList = [
            self.mainTreeChild1, self.mainTreeChild2, self.mainTreeChild3, self.mainTreeChild4,
            self.mainTreeChild5, self.mainTreeChild6, self.mainTreeChild7, self.mainTreeChild8,
        ]
        treeNameList = [
            ConstValues.PsTreeInputFiles, ConstValues.PsTreeDeleteBlank, ConstValues.PsTreeGDB,
            ConstValues.PsTreeDelIso,
            ConstValues.PsTreePeakDis, ConstValues.PsTreeRemoveFP, ConstValues.PsTreePeakDiv, ConstValues.PsTreePlot
        ]
        color = ConstValues.PsqtaIconFolderColor
        if self.MainWindowsStyle == "Qdarkstyle":
            color = "white"
        for i in range(len(treeChildList)):
            treeChildList[i].setText(0, treeNameList[i])
            treeChildList[i].setIcon(0, qtawesome.icon(ConstValues.PsqtaIconTreeFolder, color=color))

        # 展开所有树控件
        self.mainTreeWidget.expandAll()
        # 树控件关联槽函数，显示内容包括excel
        self.mainTreeWidget.clicked.connect(self.onTreeClicked)

        # 创建一个QTabWidget，专门用于存放用于显示的数据(包括excel,txt以及中间生成的数据)
        self.tabWidgetShowData = QTabWidget()
        self.tabWidgetShowData.setFont(QFont(ConstValues.PsMainFontType, ConstValues.PsMainFontSize))
        self.tabWidgetShowData.setFixedWidth(ConstValues.PsMainWindowWidth * 8 / 10)
        style = "QTabBar::tab{background-color: #DCDCDC;}" + \
                "QTabBar::tab:selected{background-color:rbg(255, 255, 255, 0);} "
        if self.MainWindowsStyle != "Qdarkstyle":
            self.tabWidgetShowData.setStyleSheet(style)
        self.tabWidgetShowData.setTabsClosable(True)  # 可以关闭
        self.tabWidgetShowData.tabCloseRequested.connect(self.TabWidgetCloseTab)  # 点击叉号后关闭
        self.plotStack.addWidget(self.tabWidgetShowData)  # 添加 QTabWidget，0

        titleList = ConstValues.PstitleList
        imagePathList = [
            "./__system/images/show/sky.png",
            "./__system/images/show/people.png",
            "./__system/images/show/dandelion.png",
            "./__system/images/show/lake.png",
            "./__system/images/show/botchi.png",
            "./__system/images/show/castle.png",
            "./__system/images/show/flower.png",
            "./__system/images/show/sea.png",
            "./__system/images/show/road.png",
        ]
        globals()["Plot_" + ConstValues.PsTreePlotInit] = self.CreateQTabWidgetImages(titleList)  # 创建 QTabWidget
        self.plotStack.addWidget(globals()["Plot_" + ConstValues.PsTreePlotInit])  # 添加 QTabWidget，1
        self.mainTreeChild8_1 = QTreeWidgetItem(self.mainTreeChild8)
        self.mainTreeChild8_1.setText(0, ConstValues.PsTreePlotInit)
        self.mainTreeChild8_1.setIcon(0, qtawesome.icon(ConstValues.PsqtaIconTreeImage,
                                                        color=color))
        self.mainTreeChild8_1.setSelected(True)
        self.plotStack.setCurrentWidget(globals()["Plot_" + ConstValues.PsTreePlotInit])

        # 树控件设置字体大小
        item = QTreeWidgetItemIterator(self.mainTreeWidget)
        while item.value():
            treeWidgetItem = item.value()
            treeWidgetItem.setFont(0, QFont(ConstValues.PsTreeFontType, ConstValues.PsTreeFontSize))
            # 到下一个节点
            item += 1

    # 左侧树控件点击后反应
    def onTreeClicked(self, index):
        item = self.mainTreeWidget.currentItem()  # 获取当前树控件，item.text(0)是树控件的名称
        if item == self.mainTreeRoot:
            if ConstValues.PsIsDebug:
                print(
                    "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                    sys._getframe().f_code.co_name, "\" method***：",
                    "i am root"
                )
            return
        treeWidgetName = item.parent().text(0)
        indexRow = index.row()
        myName = item.text(0)
        if treeWidgetName == ConstValues.PsTreeInputFiles \
                or treeWidgetName == ConstValues.PsTreeDeleteBlank \
                or treeWidgetName == ConstValues.PsTreeGDB \
                or treeWidgetName == ConstValues.PsTreeDelIso \
                or treeWidgetName == ConstValues.PsTreePeakDis \
                or treeWidgetName == ConstValues.PsTreeRemoveFP \
                or treeWidgetName == ConstValues.PsTreePeakDiv:

            if myName not in self.mainDataNameSet:  # 如果当前tab没显示在主界面上，添加到主界面
                self.tabWidgetShowData.addTab(globals()["tableWidget_" + myName], myName)
                self.mainDataNameSet.add(myName)
            self.tabWidgetShowData.setCurrentWidget(globals()["tableWidget_" + myName])  # 切换到当前tab
            self.plotStack.setCurrentIndex(0)
        elif treeWidgetName == ConstValues.PsTreePlot:  # 画图结果
            self.plotStack.setCurrentWidget(globals()["Plot_" + myName])

        if ConstValues.PsIsDebug:
            print(
                "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                sys._getframe().f_code.co_name, "\" method***：",
                "key:", treeWidgetName, "; indexRow", indexRow
            )

    # 创建图像选项卡控件（初始化显示）
    def CreateQTabWidgetImages(self, titleList):
        tabWidget = QTabWidget()
        tabWidget.setFont(QFont(ConstValues.PsMainFontType, ConstValues.PsMainFontSize))
        style = "QTabBar::tab{background-color: #DCDCDC;}" + \
                "QTabBar::tab:selected{background-color:rbg(255, 255, 255, 0);} "
        if self.MainWindowsStyle != "Qdarkstyle":
            tabWidget.setStyleSheet(style)
        # 固定 QTabWidget 大小
        tabWidget.setFixedWidth(ConstValues.PsMainWindowWidth * 8 / 10)
        # 为了随机显示图片，打乱顺序
        shuffleList = [i for i in range(len(titleList))]
        random.shuffle(shuffleList)
        imageNum = 0
        width = ConstValues.PsMainWindowWidth * 95 / 120
        if self.MainWindowsStyle == "Qdarkstyle":
            width = ConstValues.PsMainWindowWidth * 90 / 120
        for i in shuffleList:
            title = titleList[i]
            imagePath = "./__system/images/show/" + title

            tb = QScrollArea()
            tb.setAlignment(Qt.AlignCenter)
            if self.MainWindowsStyle != "Qdarkstyle":
                tb.setStyleSheet("background-color: #FFFFFF;")
            label = QLabel()  # 创建Label
            pixmap = QPixmap(imagePath)
            pixmap = pixmap.scaled(width, 4000, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # 限制一个即可
            label.setPixmap(pixmap)
            tb.setWidget(label)

            tabWidget.addTab(tb, title)

            imageNum += 1
            if imageNum == ConstValues.PsShowImageNum:
                break

        return tabWidget

    # 创建选项卡控件
    def CreateQTabWidget(self, imagePath, rawData=None):
        tabWidget = QTabWidget()
        tabWidget.setFont(QFont(ConstValues.PsMainFontType, ConstValues.PsMainFontSize))
        style = "QTabBar::tab{background-color: #DCDCDC;}" + \
                "QTabBar::tab:selected{background-color:rbg(255, 255, 255, 0);} "
        if self.MainWindowsStyle != "Qdarkstyle":
            tabWidget.setStyleSheet(style)
        # 固定 QTabWidget 大小
        tabWidget.setFixedWidth(ConstValues.PsMainWindowWidth * 8 / 10)

        # tb1相关内容
        tb1 = QScrollArea()
        tb1.setAlignment(Qt.AlignCenter)
        if self.MainWindowsStyle != "Qdarkstyle":
            tb1.setStyleSheet("background-color: #FFFFFF;")
        label = QLabel()  # 创建Label
        pixmap = QPixmap(imagePath)
        pixmap = pixmap.scaled(ConstValues.PsMainWindowWidth * 90 / 120, 4000, Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)  # 限制一个即可
        label.setPixmap(pixmap)
        tb1.setWidget(label)

        # tb2相关内容
        tb2 = self.CreateQTableWidget(rawData)

        tabWidget.addTab(tb1, "图形")
        if tb2 is not None:
            tabWidget.addTab(tb2, "原始数据")

        return tabWidget, tb2, label

    # 关闭 self.tabWidgetShowData 中的一个tab
    def TabWidgetCloseTab(self, index):
        sender = self.sender()
        name = self.tabWidgetShowData.tabText(index)  # 当前tab的名称
        if ConstValues.PsIsDebug:
            print(
                "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                sys._getframe().f_code.co_name, "\" method***：",
                "sender:", sender, "; name", name
            )
        if name in self.mainDataNameSet:
            self.mainDataNameSet.remove(name)
        sender.removeTab(index)

    # 创建表格控件
    def CreateQTableWidget(self, data):
        """
        :param data: 二维列表，有表头的数据，第一行是表头
        :return:
        """
        tableWidget = QTableWidget()
        tableWidget.setFont(QFont(ConstValues.PsMainFontType, ConstValues.PsMainFontSize))

        # 合法性检查,同时获取行数、列数
        if data is None:
            return None
        rowNum = len(data)
        if rowNum == 0:
            return None
        columnNum = len(data[0])
        if columnNum == 0:
            return None
        # 行数过多时，不全部显示
        rowNum = min(rowNum, ConstValues.PsMainMaxRowNum)

        # 设置行列数
        tableWidget.setRowCount(rowNum)
        tableWidget.setColumnCount(columnNum)

        # 添加数据
        for i in range(rowNum):
            for j in range(len(data[i])):
                item = data[i][j]
                if isinstance(item, float) and math.isnan(item):
                    continue
                item = str(item)
                nameItem = QTableWidgetItem(item)
                tableWidget.setItem(i, j, nameItem)
        # 调整列和行
        tableWidget.resizeColumnsToContents()
        tableWidget.resizeRowsToContents()
        # 禁止编辑
        tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        return tableWidget

    # 读入    文件    后树控件添加一项，并切换到当前数据显示，在 HandleData 调用
    def AddTreeItemShowData(self, parent, name, data, promptBox, icon, functionStr=""):
        # 判断是否需要覆盖原本文件，并进行相应的操作
        if self.mainNeedCover:
            self.tabWidgetShowData.removeTab(self.tabWidgetShowData.indexOf(globals()["tableWidget_" + name]))
        # 记录导入文件的信息
        self.mainDataNameSet.add(name)
        self.mainDataNameSetAll.add(name)
        # 树控件创建对应项
        if not self.mainNeedCover:
            mainTreeChild_ = QTreeWidgetItem(parent)
            mainTreeChild_.setText(0, name)
            color = ConstValues.PsqtaColor
            if self.MainWindowsStyle == "Qdarkstyle":
                color = "white"
            mainTreeChild_.setIcon(0, qtawesome.icon(icon, color=color))
            # 遍历所有节点，如果选择，则取消选择，因为只可能有一个选择了，所以碰到第一个选择的之后就可以退出
            item = QTreeWidgetItemIterator(self.mainTreeWidget)
            while item.value():
                treeWidgetItem = item.value()
                # if ConstValues.PsIsDebug:
                #     # print(treeWidgetItem)
                #     print(treeWidgetItem.text(0))
                if treeWidgetItem.isSelected():
                    treeWidgetItem.setSelected(False)
                treeWidgetItem.setFont(0, QFont(ConstValues.PsTreeFontType, ConstValues.PsTreeFontSize))  # 树控件设置字体大小
                # 到下一个节点
                item += 1
            # 光标选择到当前导入的文件
            mainTreeChild_.setSelected(True)
        # 创建 QTableWidget
        globals()["tableWidget_" + name] = self.CreateQTableWidget(data)
        # self.tabWidgetShowData 添加该项内容
        if globals()["tableWidget_" + name] is not None:  # 添加 QTableWidget
            self.tabWidgetShowData.addTab(globals()["tableWidget_" + name], name)
            self.tabWidgetShowData.setCurrentWidget(globals()["tableWidget_" + name])  # 切换到当前tab
        self.plotStack.setCurrentIndex(0)  # 显示导入的数据
        self.mainNeedCover = False  # 下次导入文件默认不需要覆盖，经过检查确定是否需要覆盖
        # 更新状态栏消息
        self.statusSetup(ConstValues.PsMainWindowStatusMessage, functionStr)
        if (promptBox is not None) and ConstValues.PsIsShowGif:
            promptBox.closeGif()
        # 如果行数过多，不全部显示，提醒用户
        if len(data) > ConstValues.PsMainMaxRowNum:
            message = "文件" + name + "行数多于" + str(ConstValues.PsMainMaxRowNum) + "行, 未完全显示."
            PromptBox().informationMessageAutoClose(message, ConstValues.PsPromptBoxTime)

    # 生成    图形    后树控件添加一项，并切换到当前数据显示，在 HandleData 调用
    def AddTreeItemPlot(self, plotImagePath, rawData, functionStr=""):
        # 提取名称
        treeItemName = plotImagePath.split("/")[-1]
        # 判断是否需要覆盖原本图片，并进行相应的操作
        if self.mainPlotNeedCover:
            self.plotStack.removeWidget(globals()["Plot_" + treeItemName])
        # 记录导入图片的名称
        self.mainPlotNameSetAll.add(treeItemName[:-4])  # 后缀为.png，需要去掉
        # 树控件创建对应项
        if not self.mainPlotNeedCover:
            mainTreeChild8_ = QTreeWidgetItem(self.mainTreeChild8)
            mainTreeChild8_.setText(0, treeItemName)
            mainTreeChild8_.setIcon(0, qtawesome.icon(ConstValues.PsqtaIconTreeImage,
                                                      color=ConstValues.PsqtaIconFolderColor))
            # 遍历所有节点，如果选择，则取消选择，因为只可能有一个选择了，所以碰到第一个选择的之后就可以退出
            item = QTreeWidgetItemIterator(self.mainTreeWidget)
            while item.value():
                treeWidgetItem = item.value()
                # if ConstValues.PsIsDebug:
                #     print(treeWidgetItem)
                #     print(treeWidgetItem.text(0))
                if treeWidgetItem.isSelected():
                    treeWidgetItem.setSelected(False)
                treeWidgetItem.setFont(0, QFont(ConstValues.PsTreeFontType, ConstValues.PsTreeFontSize))  # 树控件设置字体大小
                # 到下一个节点
                item += 1
            # 光标选择到当前导入的文件
            mainTreeChild8_.setSelected(True)
        # 创建 QTabWidget
        globals()["Plot_" + treeItemName], globals()["PlotTB_" + treeItemName], globals()[
            "PlotLabel_" + treeItemName] = self.CreateQTabWidget(plotImagePath, rawData)
        # self.plotStack 添加并显示该项内容
        self.plotStack.addWidget(globals()["Plot_" + treeItemName])
        self.plotStack.setCurrentWidget(globals()["Plot_" + treeItemName])
        self.mainPlotNeedCover = False  # 下次导入文件默认不需要覆盖，经过检查确定是否需要覆盖
        # 右键处理
        globals()["PlotLabel_" + treeItemName].setContextMenuPolicy(Qt.CustomContextMenu)
        globals()["PlotLabel_" + treeItemName].customContextMenuRequested.connect(
            lambda: self.rightMenuShow(1))  # 开放右键策略
        globals()["PlotTB_" + treeItemName].setContextMenuPolicy(Qt.CustomContextMenu)
        globals()["PlotTB_" + treeItemName].customContextMenuRequested.connect(lambda: self.rightMenuShow(2))  # 开放右键策略
        # 更新状态栏消息
        self.statusSetup(ConstValues.PsMainWindowStatusMessage, functionStr)

    # 右击选项菜单（Plot / Raw Plot Data）
    def rightMenuShow(self, Type):
        try:
            sender = self.sender()
            self.currentFunction = Type

            self.currentPixmapName = "plot.png"
            # 获取当前图片名称
            item = QTreeWidgetItemIterator(self.mainTreeWidget)
            while item.value():
                treeWidgetItem = item.value()
                if treeWidgetItem.isSelected():
                    self.currentPixmapName = treeWidgetItem.text(0)
                    break
                item += 1  # 到下一个节点

            if Type == 1:
                # 获取当前图片
                self.currentPixmap = sender.pixmap()
            elif Type == 2:
                # 从QTableWigget获取数据
                rowNum = sender.rowCount()  # 获取行数
                columnNum = sender.columnCount()  # 获取列数
                self.currentPixmapData = []
                for i in range(rowNum):
                    tempList = []
                    for j in range(columnNum):
                        text = sender.item(i, j).text()
                        try:
                            textFloat = float(sender.item(i, j).text())
                            tempList.append(textFloat)
                        except ValueError:
                            tempList.append(text)

                    self.currentPixmapData.append(tempList)
            menu = QMenu()
            menu.addAction(QAction("导出到", menu))
            menu.triggered.connect(self.MenuSlot)
            menu.exec_(QCursor.pos())
        except Exception as e:
            if ConstValues.PsIsDebug:
                print("Error_rightMenuShow : ", e)
                traceback.print_exc()
            PromptBox().errorMessage("右键导出出现错误1!")

    # 右击后处理函数（Plot / Raw Plot Data）
    def MenuSlot(self, act):
        try:
            if act.text() == "导出到":
                outputImagePath = QFileDialog.getExistingDirectory(self, '选择导出到的文件夹', './')
                if ConstValues.PsIsDebug:
                    print(
                        "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                        sys._getframe().f_code.co_name, "\" method***：",
                        "outputImagePath:", outputImagePath
                    )
                if self.currentFunction == 1:
                    if outputImagePath != "":
                        self.currentPixmap.save(outputImagePath + "/" + self.currentPixmapName)
                elif self.currentFunction == 2:
                    WriteDataToExcel(self.currentPixmapData,
                                     outputImagePath + "/" + self.currentPixmapName[:-4] + ".xlsx")
        except Exception as e:
            if ConstValues.PsIsDebug:
                print("Error_MenuSlot : ", e)
                traceback.print_exc()
            PromptBox().errorMessage("右键导出出现错误2!")

    # 右击选项菜单（树控件），就是为了删除导入的数据
    def rightTreeShow(self):
        try:
            # 遍历所有节点，如果选择，记录下来，根据后续逻辑决定是否需要删除
            item = QTreeWidgetItemIterator(self.mainTreeWidget)
            treeItemSelected = None
            while item.value():
                treeWidgetItem = item.value()
                if treeWidgetItem.isSelected():
                    treeItemSelected = treeWidgetItem
                    break
                # 到下一个节点
                item += 1
            returnList = [
                ConstValues.PsTreeProject, ConstValues.PsTreeInputFiles, ConstValues.PsTreeDeleteBlank,
                ConstValues.PsTreeGDB, ConstValues.PsTreeDelIso,
                ConstValues.PsTreePeakDis, ConstValues.PsTreeRemoveFP, ConstValues.PsTreePeakDiv,
                ConstValues.PsTreePlot, ConstValues.PsTreePlotInit,
            ]
            if treeItemSelected is None:  # 为空返回
                return
            treeItemName = treeItemSelected.text(0)
            if treeItemName in returnList:  # 不是需要删除的内容返回
                return

            if ConstValues.PsIsDebug:  # 调试输出名称
                print(
                    "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                    sys._getframe().f_code.co_name, "\" method***：",
                    "treeItemName:", treeItemName
                )
            menu = QMenu()
            menu.addAction(QAction("删除", menu))
            menu.triggered.connect(lambda: self.TreeSlot(treeItemName))
            menu.exec_(QCursor.pos())
        except Exception as e:
            if ConstValues.PsIsDebug:
                print("Error_MenuSlot : ", e)
                traceback.print_exc()
            PromptBox().errorMessage("右键删除出现错误1!")

    # 右击后处理函数（树控件），就是删除功能
    def TreeSlot(self, name):
        try:
            if name in self.mainDataNameSetAll:  # 说明是数据
                for item in self.mainTreeWidget.selectedItems():
                    item.parent().removeChild(item)
                    self.tabWidgetShowData.removeTab(self.tabWidgetShowData.indexOf(globals()["tableWidget_" + name]))
                    if name in self.mainDataNameSet:
                        self.mainDataNameSet.remove(name)
                    self.mainDataNameSetAll.remove(name)
                # 判断是否为样本文件，或者空白文件，或者TIC
                if name in self.sampleNameList:
                    self.sampleFilePath = ""  # 重置
                    self.sampleData = []
                    self.sampleNameList = [None]
                elif name in self.blankNameList:
                    self.blankFilePath = ""
                    self.blankData = []
                    self.blankNameList = [None]
                elif name in self.TICNameList:
                    self.TICFilePath = ""  # 总离子流图路径，第一部分
                    self.TICData = None
                    self.TICDataDictionary = None
                    self.TICNameList = [None]
            else:  # 一定是图形
                pass
        except Exception as e:
            if ConstValues.PsIsDebug:
                print("Error_MenuSlot : ", e)
                traceback.print_exc()
            PromptBox().errorMessage("右键删除出现错误2!")

    # -------------------------------------- 全局数据初始化
    def dataInit(self):
        # 专门用来弹出gif
        self.promptGif = PromptBox()
        self.whetherShowGif = False
        # 文件路径
        self.sampleFilePath = ""  # 样本文件路径
        self.sampleData = []
        self.blankFilePath = ""  # 空白文件路径
        self.blankData = []
        self.outputFilesPath = ""  # 输出文件路径
        if ConstValues.PsIsSingleRun:
            self.sampleFilePath = "./inputData/350/60%ACN-phenyl-kbd350-3.xlsx"
            self.blankFilePath = "./inputData/350/blank-54.xlsx"

        # 扣空白全过程需要的数据  0~10000（整数）
        self.deleteBlankIntensity = ConstValues.PsDeleteBlankIntensity  # 去空白(参数)：删除Intensity小于deleteBlankIntensity的行
        # 0.00~100.00（浮点数）
        self.deleteBlankPPM = ConstValues.PsDeleteBlankPPM  # 去空白(参数)：删去样本和空白中相同的mass且intensity相近的mass中的指标
        # 0~100（整数）
        self.deleteBlankPercentage = ConstValues.PsDeleteBlankPercentage  # 去空白(参数)：删去样本和空白中相同的mass且intensity相近的mass中的指标
        self.deleteBlankList = [
            self.sampleFilePath,  # 格式：字符串
            self.blankFilePath,  # 格式：字符串
            self.deleteBlankIntensity,  # 格式：整数
            self.deleteBlankPPM,  # 格式：浮点数
            self.deleteBlankPercentage  # 格式：整数
        ]
        self.deleteBlankResult = None  # 去空白：最终返回的结果（格式：list二维数组，有表头）
        self.deleteBlankIsFinished = False  # 去空白：记录扣空白过程是否完成

        # 数据库生成全过程需要的数据
        self.GDBClass = ConstValues.PsGDBClass  # 数据库生成(参数)：Class类型
        # 1~100（整数）
        self.GDBCarbonRangeLow = ConstValues.PsGDBCarbonRangeLow  # 数据库生成(参数)：carbon rage(碳数范围)最小值(包含)
        self.GDBCarbonRangeHigh = ConstValues.PsGDBCarbonRangeHigh  # 数据库生成(参数)：carbon rage(碳数范围)最大值(包含)
        # 1~30（整数）
        self.GDBDBERageLow = ConstValues.PsGDBDBERageLow  # 数据库生成(参数)：DBE rage(不饱和度范围)最小值(包含)
        self.GDBDBERageHigh = ConstValues.PsGDBDBERageHigh  # 数据库生成(参数)：DBE rage(不饱和度范围)最大值(包含)
        # 50~1500(整数)
        self.GDBM_ZRageLow = ConstValues.PsGDBM_ZRageLow  # 数据库生成(参数)：m/z rage(质荷比范围)最小值(包含)
        self.GDBM_ZRageHigh = ConstValues.PsGDBM_ZRageHigh  # 数据库生成(参数)：m/z rage(质荷比范围)最小值(包含)
        # 离子类型
        self.GDB_MHPostive = ConstValues.PsGDB_MHPostive  # 数据库生成(参数)：正离子，是否选择[M+H]+，True为选中
        self.GDB_MPostive = ConstValues.PsGDB_MPostive  # 数据库生成(参数)：正离子，是否选择M+，True为选中
        self.GDB_MHNegative = ConstValues.PsGDB_MHNegative  # 数据库生成(参数)：负离子，是否选择[M-H]-，True为选中
        self.GDB_MNegative = ConstValues.PsGDB_MNegative  # 数据库生成(参数)：负离子，是否选择M-，True为选中
        self.GDBList = [
            self.GDBClass,  # 格式：列表，列表中均为字符串
            self.GDBCarbonRangeLow,  # 格式：整数
            self.GDBCarbonRangeHigh,  # 格式：整数
            self.GDBDBERageLow,  # 格式：整数
            self.GDBDBERageHigh,  # 格式：整数
            self.GDBM_ZRageLow,  # 格式：整数
            self.GDBM_ZRageHigh,  # 格式：整数
            self.GDB_MHPostive,  # 格式：bool
            self.GDB_MPostive,  # 格式：bool
            self.GDB_MHNegative,  # 格式：bool
            self.GDB_MNegative  # 格式：bool
        ]
        self.GDBResult = None  # 数据库生成：最终返回的结果（格式：list二维数组，有表头）
        self.GDBIsFinished = False  # 数据库生成：记录数据库生成过程是否完成

        # 去同位素全过程需要的数据，另外还需要 扣空白的self.deleteBlankResult 和 数据库生成self.GDBResult
        self.DelIsoIntensityX = ConstValues.PsDelIsoIntensityX  # 0~正无穷（整数）
        # 0~100（整数）
        self.DelIso_13C2RelativeIntensity = ConstValues.PsDelIso_13C2RelativeIntensity
        # 0.00~20.00（浮点数）
        self.DelIsoMassDeviation = ConstValues.PsDelIsoMassDeviation
        # 0.00~20.00（浮点数）
        self.DelIsoIsotopeMassDeviation = ConstValues.PsDelIsoIsotopeMassDeviation
        # 1~100（整数）
        self.DelIsoIsotopeIntensityDeviation = ConstValues.PsDelIsoIsotopeIntensityDeviation
        self.DelIsoList = [
            self.deleteBlankResult,  # 删空白的结果（格式：list二维数组，有表头）
            self.GDBResult,  # 数据库生成的结果（格式：list二维数组，有表头）
            self.deleteBlankIntensity,
            self.DelIsoIntensityX,  # 格式：整数
            self.DelIso_13C2RelativeIntensity,  # 格式：整数
            self.DelIsoMassDeviation,  # 格式：浮点数
            self.DelIsoIsotopeMassDeviation,  # 格式：浮点数
            self.DelIsoIsotopeIntensityDeviation  # 格式：整数
        ]
        self.DelIsoResult = None  # 搜同位素：最终返回的结果（格式：list二维数组，有表头）
        self.DelIsoIsFinished = False  # 搜同位素：记录去同位素过程是否完成

        # 峰识别全过程所需要的数据
        self.TICFilePath = ""  # 总离子流图路径，第一部分
        # self.TICFilePath 直接读入后的数据
        self.TICData = None
        # self.TICFilePath 读入后并处理后的数据,为字典：{key:value}，value为二维列表[[Mass, Intensity],...,[Mass, Intensity]]
        self.TICDataDictionary = None
        # if ConstValues.PsIsSingleRun:
        #     self.TICFilePath = "./inputData/350/60%ACN-phenyl-kbd350-3.txt"
        # 0~10000（整数）
        self.PeakDisContinuityNum = ConstValues.PsPeakDisContinuityNum
        # 0.00~100.00（浮点数）
        self.PeakDisMassDeviation = ConstValues.PsPeakDisMassDeviation
        # 0~30(整数)
        self.PeakDisDiscontinuityPointNum = ConstValues.PsPeakDisDiscontinuityPointNum
        # 第二部分，峰检测
        self.PeakDisClassIsNeed = ConstValues.PsPeakDisClassIsNeed
        self.PeakDisClass = ConstValues.PsPeakDisClass
        self.PeakDisList = [
            self.TICDataDictionary,
            self.DelIsoResult,
            self.PeakDisContinuityNum,
            self.PeakDisMassDeviation,
            self.PeakDisDiscontinuityPointNum,
            self.PeakDisClassIsNeed,  # 第二部分
            self.PeakDisClass
        ]
        # 结果是一个列表，有三个元素，
        # 第一个是峰识别的结果（格式：list二维数组，有表头）
        # 第二个是需要需要峰检测（第二部分）的详细数据，二维列表，无表头
        # 第三个是txt文件中RT值(从小到大排序)
        self.PeakDisResult = [[], [], []]
        self.PeakDisIsFinished = False  # 峰识别：记录峰识别过程是否完成

        # 去假阳性全过程所需要的数据
        self.RemoveFPId = ConstValues.PsRemoveFPId  # 1：去同位素之后的内容，2：峰识别之后的内容
        # 0~100（整数）
        self.RemoveFPContinue_CNum = ConstValues.PsRemoveFPContinue_CNum  # 连续碳数
        # 0~100（整数）
        self.RemoveFPContinue_DBENum = ConstValues.PsRemoveFPContinue_DBENum  # 连续DBE数
        self.RemoveFPList = [
            self.DelIsoResult,
            self.PeakDisResult,
            self.RemoveFPId,  # 决定选择哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
            self.RemoveFPContinue_CNum,
            self.RemoveFPContinue_DBENum
        ]
        # 结果是一个列表，有两个元素
        # 第一个所有类别去假阳性的结果，二维列表，或者1：去同位素之后的内容，或者2：峰识别之后的内容 都有表头
        # 第二个是去假阳性后需要峰检测（第二部分）的数据，二维列表，无表头，即self.PeakDisResult[1]去假阳性后的数据
        self.RemoveFPResult = [[], []]
        self.RemoveFPIsFinished = False

        # 峰检测全过程所需要的数据  0~1000000(整数)
        self.PeakDivNoiseThreshold = ConstValues.PsPeakDivNoiseThreshold  # 噪音阈值
        # 0.0~100.0(浮点数)
        self.PeakDivRelIntensity = ConstValues.PsPeakDivRelIntensity  # # 相对强度阈值
        # 该参数决定是否需要将溶剂效应的第一个峰融合到第二个峰
        self.PeakDivNeedMerge = ConstValues.PsPeakDivNeedMerge
        # 该参数决定是否生成图片信息
        self.PeakDivNeedGenImage = ConstValues.PsPeakDivNeedGenImage
        self.PeakDivList = [
            self.RemoveFPId,  # 判断选择了哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
            self.RemoveFPResult[1],  # 去假阳性后的需要峰识别（第二部分）结果，二维列表，无表头
            self.PeakDisResult[2],  # 第三个是txt文件中RT值(从小到大排序)
            self.PeakDivNoiseThreshold,
            self.PeakDivRelIntensity,
            self.PeakDivNeedMerge,  # 该参数决定是否需要将溶剂效应的第一个峰融合到第二个峰
            self.PeakDivNeedGenImage  # 该参数决定是否生成图片信息
        ]
        self.PeakDivResult = None
        self.PeakDivIsFinished = False

        # 绘图全过程所需要的数据
        self.PlotTitleName = ConstValues.PsPlotTitleName  # 标题名称
        self.PlotTitleColor = ConstValues.PsPlotTitleColor  # 标题颜色
        self.PlotXAxisName = ConstValues.PsPlotXAxisName  # x轴名称
        self.PlotXAxisColor = ConstValues.PsPlotXAxisColor  # x轴颜色
        self.PlotYAxisName = ConstValues.PsPlotYAxisName  # y轴名称
        self.PlotYAxisColor = ConstValues.PsPlotYAxisColor  # y轴颜色
        # 记录是否进入过PlotSetup()函数
        self.PlotHasEnter = ConstValues.PsPlotHasEnter
        # 1~6(整数)
        self.PlotType = ConstValues.PsPlotType  # 绘图类型
        self.PlotClassList = ConstValues.PsPlotClassList  # 列表，需要绘制的类型，例子：["CH", "N1"]，对应多选按钮
        self.PlotClassItem = ConstValues.PsPlotClassItem  # 列表，需要绘制的类型，例子：["CH"]，对应单选钮，长度必须为1
        self.PlotDBENum = ConstValues.PsPlotDBENum  # 整数，记录用户选择的DBE数目
        # 用户是否确认要画图
        self.PlotConfirm = ConstValues.PsPlotConfirm
        # 输出文件路径
        self.PlotImagePath = ""
        # 画图原始数据
        self.PlotRawData = []

        self.PlotList = [
            self.RemoveFPId,  # 判断选择了哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
            self.RemoveFPResult[0],  # 所有类别去假阳性的结果，二维列表，有表头
            self.PlotTitleName,
            self.PlotTitleColor,
            self.PlotXAxisName,
            self.PlotXAxisColor,
            self.PlotYAxisName,
            self.PlotYAxisColor,
            self.PlotHasEnter,  # 记录是否进入过PlotSetup()函数
            self.PlotType,  # 绘图类型
            self.PlotClassList,  # 列表，需要绘制的类型，例子：["CH", "N1"]
            self.PlotClassItem,  # 列表，需要绘制的类型，例子：["CH"]，对应单选钮，长度必须为1
            self.PlotDBENum,  # 整数，记录用户选择的DBE数目
            self.PlotConfirm
        ]

        # 运行模式
        # 1：去空白 --> 数据库生成 --> 搜同位素 --> 去假阳性
        # 2：去空白 --> 数据库生成 --> 搜同位素 --> 峰提取 --> 去假阳性
        # 3：去空白 --> 数据库生成 --> 搜同位素 --> 峰提取 --> 去假阳性 --> 峰检测
        # 4：数据库生成 --> 搜同位素 --> 去假阳性
        # 5：数据库生成 --> 搜同位素 --> 峰提取 --> 去假阳性
        # 6：数据库生成 --> 搜同位素 --> 峰提取 --> 去假阳性 --> 峰检测
        self.startMode = ConstValues.PsStartMode
        # 确定开始运行
        self.startModeConfirm = False

        self.startModeList = [
            self.startMode,
            self.startModeConfirm
        ]

    # 使窗口居中
    def center(self):
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = (screen.width() - size.width()) / 2
        newTop = (screen.height() - size.height()) / 2
        self.move(newLeft, newTop)

    # 创建主窗口菜单栏（下拉菜单栏）
    def menu(self):
        # 获取菜单栏
        bar = self.menuBar()
        # 创建第一个主菜单
        file = bar.addMenu("文件")
        importSampleFile = QAction("样本", self)  # 添加二级菜单
        file.addAction(importSampleFile)
        importSampleFile.triggered.connect(self.ImportSampleFile)

        importBlankFile = QAction("空白", self)  # 添加二级菜单
        file.addAction(importBlankFile)
        importBlankFile.triggered.connect(self.ImportBlankFile)

        TICFile = QAction("样本TIC", self)  # 添加二级菜单
        file.addAction(TICFile)
        TICFile.triggered.connect(self.ImportTICFile)

        intermediateFiles = QAction("导入", self)  # 添加二级菜单
        file.addAction(intermediateFiles)
        intermediateFiles.triggered.connect(self.importIntermediateFiles)

        OutFilesPath = QAction("输出", self)  # 添加二级菜单
        file.addAction(OutFilesPath)
        OutFilesPath.triggered.connect(self.GetOutputFilesPath)

        exitProgram = QAction("退出", self)  # 添加二级菜单
        file.addAction(exitProgram)
        exitProgram.triggered.connect(self.QuitApplication)

        # 创建第二个主菜单
        set = bar.addMenu("编辑")
        deleteBlank = QAction("去空白", self)  # 添加二级菜单
        set.addAction(deleteBlank)
        deleteBlank.triggered.connect(self.DeleteBlankSetup)

        DBSearch = QAction("数据库生成", self)  # 添加二级菜单
        set.addAction(DBSearch)
        DBSearch.triggered.connect(self.GenerateDataBaseSetup)

        deleteIsotope = QAction("搜同位素", self)  # 添加二级菜单
        set.addAction(deleteIsotope)
        deleteIsotope.triggered.connect(self.DeleteIsotopeSetup)

        peakDistinguish = QAction("峰提取", self)  # 添加二级菜单
        set.addAction(peakDistinguish)
        peakDistinguish.triggered.connect(self.PeakDistinguishSetup)

        RemoveFP = QAction("去假阳性", self)  # 添加二级菜单
        set.addAction(RemoveFP)
        RemoveFP.triggered.connect(self.RemoveFalsePositiveSetup)

        peakDivision = QAction("峰检测", self)  # 添加二级菜单
        set.addAction(peakDivision)
        peakDivision.triggered.connect(self.PeakDivisionSetup)

        # 创建第三个主菜单
        plot = bar.addMenu("绘图")
        addPlot = QAction("添加", self)  # 添加二级菜单
        plot.addAction(addPlot)
        addPlot.triggered.connect(self.SetupAndPlot)

        # 创建第四个主菜单
        theme = bar.addMenu("主题")
        themeMacintosh = QAction("Macintosh", self)  # 添加二级菜单
        theme.addAction(themeMacintosh)
        themeMacintosh.triggered.connect(lambda: self.ThemeSelect("Macintosh"))

        themeQdarkstyle = QAction("Qdarkstyle", self)  # 添加二级菜单
        theme.addAction(themeQdarkstyle)
        themeQdarkstyle.triggered.connect(lambda: self.ThemeSelect("Qdarkstyle"))

        themeWindows = QAction("Windows", self)  # 添加二级菜单
        theme.addAction(themeWindows)
        themeWindows.triggered.connect(lambda: self.ThemeSelect("Windows"))

        themeFusion = QAction("Fusion", self)  # 添加二级菜单
        theme.addAction(themeFusion)
        themeFusion.triggered.connect(lambda: self.ThemeSelect("Fusion"))

        # 创建第五个主菜单
        help = bar.addMenu("帮助")
        uiHelp = QAction("界面介绍", self)  # 添加二级菜单
        help.addAction(uiHelp)
        uiHelp.triggered.connect(lambda: self.Help("UIHelp"))

        fileHelp = QAction("文件帮助", self)  # 添加二级菜单
        help.addAction(fileHelp)
        fileHelp.triggered.connect(lambda: self.Help("FileHelp"))

        editHelp = QMenu("编辑帮助", self)  # 添加二级菜单
        help.addMenu(editHelp)
        editHelpDeleteBlank = QAction("去空白", self)  # 添加三级菜单
        editHelp.addAction(editHelpDeleteBlank)
        editHelpDeleteBlank.triggered.connect(lambda: self.Help("EditHelpDeleteBlank"))
        editHelpGDB = QAction("数据库生成", self)
        editHelp.addAction(editHelpGDB)
        editHelpGDB.triggered.connect(lambda: self.Help("EditHelpGDB"))
        editHelpDeleteIso = QAction("搜同位素", self)
        editHelp.addAction(editHelpDeleteIso)
        editHelpDeleteIso.triggered.connect(lambda: self.Help("EditHelpDeleteIso"))
        editHelpPeakDis = QAction("峰提取", self)
        editHelp.addAction(editHelpPeakDis)
        editHelpPeakDis.triggered.connect(lambda: self.Help("EditHelpPeakDis"))
        editHelpRFP = QAction("去假阳性", self)
        editHelp.addAction(editHelpRFP)
        editHelpRFP.triggered.connect(lambda: self.Help("EditHelpRFP"))
        editHelpPeakDiv = QAction("峰检测", self)
        editHelp.addAction(editHelpPeakDiv)
        editHelpPeakDiv.triggered.connect(lambda: self.Help("EditHelpPeakDiv"))

        plotHelp = QAction("绘图帮助", self)  # 添加二级菜单
        help.addAction(plotHelp)
        plotHelp.triggered.connect(lambda: self.Help("PlotHelp"))

        modeHelp = QAction("模式帮助", self)  # 添加二级菜单
        help.addAction(modeHelp)
        modeHelp.triggered.connect(lambda: self.Help("ModeHelp"))

        otherHelp = QAction("其他帮助", self)  # 添加二级菜单
        help.addAction(otherHelp)
        otherHelp.triggered.connect(lambda: self.Help("OtherHelp"))

        about = QAction("关于", self)  # 添加二级菜单
        help.addAction(about)
        about.triggered.connect(lambda: self.Help("About"))

        # 设置字体，图标等
        elementList = [
            importSampleFile, importBlankFile, TICFile, intermediateFiles, OutFilesPath, exitProgram,
            deleteBlank, DBSearch, deleteIsotope, peakDistinguish, RemoveFP,
            peakDivision, addPlot,
            themeMacintosh, themeQdarkstyle, themeWindows, themeFusion,
            uiHelp, fileHelp, editHelp, editHelpDeleteBlank, editHelpGDB,
            editHelpDeleteIso, editHelpPeakDis, editHelpRFP, editHelpPeakDiv,
            plotHelp, modeHelp, otherHelp, about
        ]
        IconFromImage = [
            ConstValues.PsIconOpenFile, ConstValues.PsIconOpenFile, ConstValues.PsIconOpenFile,
            ConstValues.PsIconOpenFile, ConstValues.PsIconOpenFile, ConstValues.PsIconExit,
            ConstValues.PsIconDeleteBlank, ConstValues.PsIconGDB, ConstValues.PsIcondelIso, ConstValues.PsIconpeakDis,
            ConstValues.PsIconRemoveFP,
            ConstValues.PsIconpeakDiv, ConstValues.PsIconPlot,
            None, None, None, None,
            ConstValues.PsIconOpenFile, ConstValues.PsIconOpenFile, ConstValues.PsIconHelpEdit,
            ConstValues.PsIconDeleteBlank, ConstValues.PsIconGDB,
            ConstValues.PsIcondelIso, ConstValues.PsIconpeakDis, ConstValues.PsIconRemoveFP, ConstValues.PsIconpeakDiv,
            ConstValues.PsIconPlot, ConstValues.PsIconAllStart, ConstValues.PsIconHelpOther, ConstValues.PsIconHelpAbout
        ]
        IconFromQta = [
            ConstValues.PsqtaIconOpenFileExcel, ConstValues.PsqtaIconOpenFileExcel, ConstValues.PsqtaIconOpenFileTxt,
            ConstValues.PsqtaIconOpenFileOut, ConstValues.PsqtaIconOpenFileOut, ConstValues.PsqtaIconExit,
            ConstValues.PsqtaIconDeleteBlank, ConstValues.PsqtaIconGDB, ConstValues.PsqtaIcondelIso,
            ConstValues.PsqtaIconpeakDis, ConstValues.PsqtaIconRemoveFP,
            ConstValues.PsqtaIconpeakDiv, ConstValues.PsqtaIconPlot,
            ConstValues.PsqtathemeMacintosh, ConstValues.PsqtathemeQdarkstyle, ConstValues.PsqtathemeWindows,
            ConstValues.PsqtathemeFusion,
            ConstValues.PsqtaIconHelpWindows, ConstValues.PsqtaIconOpenFileOut, ConstValues.PsqtaIconHelpEdit,
            ConstValues.PsqtaIconDeleteBlank, ConstValues.PsqtaIconGDB,
            ConstValues.PsqtaIcondelIso, ConstValues.PsqtaIconpeakDis, ConstValues.PsqtaIconRemoveFP,
            ConstValues.PsqtaIconpeakDiv,
            ConstValues.PsqtaIconPlot, ConstValues.PsqtaIconAllStart, ConstValues.PsqtaIconHelpOther,
            ConstValues.PsqtaIconHelpAbout
        ]
        color = ConstValues.PsqtaColor
        if self.MainWindowsStyle == "Qdarkstyle":
            color = "white"
        bar.setFont(QFont(ConstValues.PsMenuFontType, ConstValues.PsMenuFontSize))
        for i in range(len(elementList)):
            # 设置字体大小
            elementList[i].setFont(QFont(ConstValues.PsMenuFontType, ConstValues.PsMenuFontSize))
            # 设置图标
            if ConstValues.PsIconType == 1:  # 从图片读取
                if IconFromImage[i] == None:
                    continue
                elementList[i].setIcon(QIcon(IconFromImage[i]))
            elif ConstValues.PsIconType == 2:  # 来自 qtawesome
                elementList[i].setIcon(qtawesome.icon(IconFromQta[i], color=color))

    # 设置工具栏
    def toolbar(self):
        # 添加第一个工具栏
        tb1 = self.addToolBar("文件")
        tb1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # 设置图标下显示功能
        # 为第一个工具栏添加按钮
        importSampleFile = QAction("样本", self)
        importSampleFile.setToolTip("选择需要导入的样本文件")  # 鼠标停放时显示的信息
        tb1.addAction(importSampleFile)
        importSampleFile.triggered.connect(self.ImportSampleFile)

        importBlankFile = QAction("空白", self)
        importBlankFile.setToolTip("选择需要导入的空白文件")
        tb1.addAction(importBlankFile)
        importBlankFile.triggered.connect(self.ImportBlankFile)

        TICFile = QAction("样本TIC", self)
        TICFile.setToolTip("选择需要导入的总离子图文件")
        tb1.addAction(TICFile)
        TICFile.triggered.connect(self.ImportTICFile)

        intermediateFiles = QAction("导入", self)
        intermediateFiles.setToolTip("从生成的结果文件夹中导入数据")
        tb1.addAction(intermediateFiles)
        intermediateFiles.triggered.connect(self.importIntermediateFiles)

        OutFilesPath = QAction("输出", self)
        OutFilesPath.setToolTip("选择生成文件位置")
        tb1.addAction(OutFilesPath)
        OutFilesPath.triggered.connect(self.GetOutputFilesPath)

        exitProgram = QAction("退出", self)
        exitProgram.setToolTip("退出程序")
        tb1.addAction(exitProgram)
        exitProgram.triggered.connect(self.QuitApplication)
        exitProgram.setShortcut("Esc")

        # 添加第二个工具栏
        tb2 = self.addToolBar("单项处理开始按钮")
        # tb2.setToolButtonStyle(Qt.ToolButtonTextOnly)  # 设置只显示文本
        tb2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # 设置图标下显示功能
        # 为第二个工具栏添加按钮
        deleteBlank = QAction("去空白", self)
        tb2.addAction(deleteBlank)
        deleteBlank.triggered.connect(self.DeleteBlank)

        DBSearch = QAction("数据库生成", self)
        tb2.addAction(DBSearch)
        DBSearch.triggered.connect(self.GenerateDataBase)

        deleteIsotope = QAction("搜同位素", self)
        tb2.addAction(deleteIsotope)
        deleteIsotope.triggered.connect(self.DeleteIsotope)

        peakDistinguish = QAction("峰提取", self)
        tb2.addAction(peakDistinguish)
        peakDistinguish.triggered.connect(self.PeakDistinguish)

        RemoveFP = QAction("去假阳性", self)
        tb2.addAction(RemoveFP)
        RemoveFP.triggered.connect(self.RemoveFalsePositive)

        self.TBpeakDivision = QAction("峰检测", self)  # 因为需要控制是否使能，所以为全局变量
        tb2.addAction(self.TBpeakDivision)
        self.TBpeakDivision.triggered.connect(self.PeakDivision)
        self.TBpeakDivision.setEnabled(self.PeakDisClassIsNeed)

        plot = QAction("绘图", self)
        tb2.addAction(plot)
        plot.triggered.connect(self.SetupAndPlot)

        # 添加第三个工具栏
        tb4 = self.addToolBar("模式选择重置软件")
        tb4.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # 设置图标下显示功能
        # 为第三个工具栏添加按钮
        allStart = QAction("模式选择", self)
        tb4.addAction(allStart)
        allStart.triggered.connect(self.SetupAndStartMode)

        allReset = QAction("重置软件", self)
        allReset.setToolTip("重置所有参数为默认参数")
        tb4.addAction(allReset)
        allReset.triggered.connect(self.ResetProgram)

        # 设置字体，图标等
        elementList = [
            importSampleFile, importBlankFile, TICFile, intermediateFiles, OutFilesPath, exitProgram,
            deleteBlank, DBSearch, deleteIsotope, peakDistinguish, RemoveFP,
            self.TBpeakDivision, plot, allStart, allReset
        ]
        IconFromImage = [
            ConstValues.PsIconOpenFile, ConstValues.PsIconOpenFile, ConstValues.PsIconOpenFile,
            ConstValues.PsIconOpenFile, ConstValues.PsIconOpenFile, ConstValues.PsIconExit,
            ConstValues.PsIconDeleteBlank, ConstValues.PsIconGDB, ConstValues.PsIcondelIso, ConstValues.PsIconpeakDis,
            ConstValues.PsIconRemoveFP,
            ConstValues.PsIconpeakDiv, ConstValues.PsIconPlot, ConstValues.PsIconAllStart, ConstValues.PsIconAllReset
        ]
        IconFromQta = [
            ConstValues.PsqtaIconOpenFileExcel, ConstValues.PsqtaIconOpenFileExcel, ConstValues.PsqtaIconOpenFileTxt,
            ConstValues.PsqtaIconOpenFileOut, ConstValues.PsqtaIconOpenFileOut, ConstValues.PsqtaIconExit,
            ConstValues.PsqtaIconDeleteBlank, ConstValues.PsqtaIconGDB, ConstValues.PsqtaIcondelIso,
            ConstValues.PsqtaIconpeakDis, ConstValues.PsqtaIconRemoveFP,
            ConstValues.PsqtaIconpeakDiv, ConstValues.PsqtaIconPlot, ConstValues.PsqtaIconAllStart,
            ConstValues.PsqtaIconAllReset
        ]
        color = ConstValues.PsqtaColor
        if self.MainWindowsStyle == "Qdarkstyle":
            color = "white"
        for i in range(len(elementList)):
            # 设置字体大小
            elementList[i].setFont(QFont(ConstValues.PsToolbarFontType, ConstValues.PsToolbarFontSize))
            # 设置图标
            if ConstValues.PsIconType == 1:  # 从图片读取
                elementList[i].setIcon(QIcon(IconFromImage[i]))
            elif ConstValues.PsIconType == 2:  # 来自 qtawesome
                elementList[i].setIcon(qtawesome.icon(IconFromQta[i], color=color))

    # 设置主窗口底部状态栏
    def status(self):
        self.statusBar = self.statusBar()
        # 设置状态栏背景颜色
        if self.MainWindowsStyle != "Qdarkstyle":
            self.statusBar.setStyleSheet(ConstValues.PsStatusStyle)
        # 设置字体显示样式
        style = "color:rgb(0,0,0,250); font-family: Microsoft YaHei;"
        # 第一条显示的信息
        nowDate = str(QDate.currentDate().toString("yyyy.MM.dd"))
        self.statusContext1 = QLabel(ConstValues.PsMainWindowStatusMessage + "|   日期：" + nowDate)
        self.statusContext1.setFont(QFont(ConstValues.PsStatusFontType, ConstValues.PsStatusFontSize))
        if self.MainWindowsStyle != "Qdarkstyle":
            self.statusContext1.setStyleSheet(style)
        # 第二条显示的信息
        self.statusContext2 = QLabel("当前处于空闲状态.")
        self.statusContext2.setFont(QFont(ConstValues.PsStatusFontType, ConstValues.PsStatusFontSize))
        if self.MainWindowsStyle != "Qdarkstyle":
            self.statusContext2.setStyleSheet(style)
        # 状态栏添加显示的信息
        self.statusBar.addPermanentWidget(self.statusContext1, stretch=2)
        self.statusBar.addPermanentWidget(self.statusContext2, stretch=1)

    # 设置主窗口底部状态栏显示文字
    def statusSetup(self, text1, text2):
        # 设置第一条显示的信息
        nowDate = str(QDate.currentDate().toString("yyyy.MM.dd"))
        self.statusContext1.setText(text1 + "|   日期：" + nowDate)
        # 设置第二条显示的信息
        self.statusContext2.setText(text2)

    # -------------------------------------- 导入样本文件，文件路径存在sampleFileName中
    def ImportSampleFile(self):
        # 程序运行前准备工作
        if not self.BeforeRunning("ImportSampleFile"):
            return
        # 处理扣空白，另起一个线程运行扣空白代码，主界面可以操作
        self.StartRunning("ImportSampleFile")
        # 程序开始运行后收尾工作
        self.AfterRunning("ImportSampleFile")

    # 导入空白文件，文件路径存在blankFileName中
    def ImportBlankFile(self):
        # 程序运行前准备工作
        if not self.BeforeRunning("ImportBlankFile"):
            return
        # 处理扣空白，另起一个线程运行扣空白代码，主界面可以操作
        self.StartRunning("ImportBlankFile")
        # 程序开始运行后收尾工作
        self.AfterRunning("ImportBlankFile")

    # 导入总离子流图文件，文件路径存在TICFilePath中
    def ImportTICFile(self):

        # 程序运行前准备工作
        if not self.BeforeRunning("ImportTICFile"):
            return
        # 处理扣空白，另起一个线程运行扣空白代码，主界面可以操作
        self.StartRunning("ImportTICFile")
        # 程序开始运行后收尾工作
        self.AfterRunning("ImportTICFile")

    # 导入中间生成的文件，直接选择中间文件所在的总文件夹，如果默认是 intermediateFiles
    def importIntermediateFiles(self):
        # 导入文件，并得到文件名称
        self.intermediateFilesPath = QFileDialog.getExistingDirectory(self, '选择生成的文件所在的总文件夹', './')
        if ConstValues.PsIsDebug:
            print(
                "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                sys._getframe().f_code.co_name, "\" method***：",
                "self.intermediateFilesPath:", self.intermediateFilesPath
            )
        # 如果为空，直接返回
        if self.intermediateFilesPath == "":
            return
        # 用户选择导入哪个假阳性文件
        RFPPath = ""
        RFPName = None
        RFPPath1 = self.intermediateFilesPath + "/_5_removeFalsePositive/" + ConstValues.PsNameRemoveFPFrom_DelIsoResult
        RFPPath2 = self.intermediateFilesPath + "/_5_removeFalsePositive/" + ConstValues.PsNameRemoveFPFrom_PeakDisResult
        if os.path.exists(RFPPath1) and (not os.path.exists(RFPPath2)):
            RFPPath = RFPPath1
            RFPName = ConstValues.PsNameRemoveFPFrom_DelIsoResult
            self.RemoveFPId = 1
        elif os.path.exists(RFPPath2) and (not os.path.exists(RFPPath1)):
            RFPPath = RFPPath2
            RFPName = ConstValues.PsNameRemoveFPFrom_PeakDisResult
            self.RemoveFPId = 2
        elif os.path.exists(RFPPath1) and os.path.exists(RFPPath2):
            chooseRFPPath1 = PromptBox().informationMessage(
                "去假阳性可以有两种方式生成:\n1.选择搜同位素后去假阳性文件点击：Yes\n2.选择峰提取后去假阳性文件点击：No")
            if chooseRFPPath1:
                RFPPath = RFPPath1
                RFPName = ConstValues.PsNameRemoveFPFrom_DelIsoResult
                self.RemoveFPId = 1
            else:
                RFPPath = RFPPath2
                RFPName = ConstValues.PsNameRemoveFPFrom_PeakDisResult
                self.RemoveFPId = 2

        # if ConstValues.PsIsShowGif:
        #     self.promptGif.showGif("正在导入数据，请稍后...", ConstValues.PsIconLoading)

        if os.path.exists(RFPPath):
            self.statusSetup(ConstValues.PsMainWindowStatusMessage, "开始导入数据.")
            # 是否存在去假阳性后的文件，如果存在，读取并显示
            parent = self.mainTreeChild6
            name = RFPName
            data = ReadExcelToList(RFPPath, hasNan=True)
            icon = ConstValues.PsqtaIconOpenFileExcel
            functionStr = "峰提取数据导入完毕！"
            # self.AddTreeItemShowData(parent, name, data, self.promptGif, icon, functionStr)
            self.AddTreeItemShowData(parent, name, data, None, icon, functionStr)

            self.RemoveFPResult = [data, []]
            self.RemoveFPIsFinished = True
            # 更新状态栏消息
            self.statusSetup(ConstValues.PsMainWindowStatusMessage, "数据导入完毕.")
        else:
            PromptBox().informationMessageAutoClose("没有内容可以导入!", ConstValues.PsPromptBoxTime)

    # 选择输入的文件存放的文件夹
    def GetOutputFilesPath(self):
        # 导入文件，并得到文件名称
        self.outputFilesPath = QFileDialog.getExistingDirectory(self, '选择文件生成到的文件夹', './')
        if ConstValues.PsIsDebug:
            print(
                "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                sys._getframe().f_code.co_name, "\" method***：",
                "self.outputFilesPath:", self.outputFilesPath
            )

    # -------------------------------------- 重置软件，参数重置
    def ResetProgram(self):
        if PromptBox().informationMessage("是否重置?"):
            self.dataInit()
            self.ResetAssembly()
            PromptBox().informationMessageAutoClose("已重置.", ConstValues.PsPromptBoxTime / 2)

    # 复位主窗口中的一些组件（如：标签）
    def ResetAssembly(self):
        self.plotStack.removeWidget(globals()["Plot_" + ConstValues.PsTreePlotInit])
        self.Layout.removeWidget(self.mainTreeWidget)
        self.Layout.removeWidget(self.plotStack)
        # initShow 初始化数据
        self.initShowDataInit()
        # self.Layout 添加控件
        self.MainLayoutAddWidget()
        # 更新状态栏
        self.TBpeakDivision.setEnabled(self.PeakDisClassIsNeed)

    # 退出程序
    @staticmethod
    def QuitApplication(self):
        if not PromptBox().questionMessage("是否要退出程序？"):
            return

        app = QApplication.instance()
        # 退出应用程序
        app.quit()

    # 扣空白参数设置  #######################################
    def DeleteBlankSetup(self):
        try:
            # 重新设置参数
            newParameters = SetupInterface(self.MainWindowsStyle).DeleteBlankSetup(self.deleteBlankList[2:])
            # 更新数据
            self.UpdateData("DeleteBlankSetup", newParameters)
        except Exception as e:
            if ConstValues.PsIsDebug:
                print("Error_DeleteBlankSetup_MainWin : ", e)
                traceback.print_exc()
            PromptBox().errorMessage("删空白设置出现错误!")

    # 数据库生成参数设置
    def GenerateDataBaseSetup(self):
        try:
            newParameters = SetupInterface(self.MainWindowsStyle).GenerateDataBaseSetup(self.GDBList)
            self.UpdateData("GenerateDataBaseSetup", newParameters)
        except Exception as e:
            if ConstValues.PsIsDebug:
                print("Error_GenerateDataBaseSetup_MainWin : ", e)
                traceback.print_exc()
            PromptBox().errorMessage("数据库生成设置出现错误!")

    # 搜同位素参数设置
    def DeleteIsotopeSetup(self):
        try:
            newParameters = SetupInterface(self.MainWindowsStyle).DeleteIsotopeSetup(self.DelIsoList[3:])
            self.UpdateData("DeleteIsotopeSetup", newParameters)
        except Exception as e:
            if ConstValues.PsIsDebug:
                print("Error_DeleteIsotopeSetup_MainWin : ", e)
                traceback.print_exc()
            PromptBox().errorMessage("搜同位素设置出现错误!")

    # 峰提取参数设置
    def PeakDistinguishSetup(self):
        try:
            newParameters = SetupInterface(self.MainWindowsStyle).PeakDistinguishSetup(self.PeakDisList[2:])
            self.UpdateData("PeakDistinguishSetup", newParameters)
        except Exception as e:
            if ConstValues.PsIsDebug:
                print("Error_PeakDistinguishSetup_MainWin : ", e)
                traceback.print_exc()
            PromptBox().errorMessage("峰提取设置出现错误!")

    # 去假阳性参数设置
    def RemoveFalsePositiveSetup(self):
        try:
            newParameters = SetupInterface(self.MainWindowsStyle).RemoveFalsePositiveSetup(self.RemoveFPList[2:])
            self.UpdateData("RemoveFalsePositiveSetup", newParameters)
        except Exception as e:
            if ConstValues.PsIsDebug:
                print("Error_RemoveFalsePositiveSetup_MainWin : ", e)
                traceback.print_exc()
            PromptBox().errorMessage("去假阳性设置出现错误!")

    # 峰检测参数设置
    def PeakDivisionSetup(self):
        try:
            newParameters = SetupInterface(self.MainWindowsStyle).PeakDivisionSetup(self.PeakDivList[3:])
            self.UpdateData("PeakDivisionSetup", newParameters)
        except Exception as e:
            if ConstValues.PsIsDebug:
                print("Error_PeakDivisionSetup_MainWin : ", e)
                traceback.print_exc()
            PromptBox().errorMessage("峰检测设置出现错误!")

    # 绘图设置
    def PlotSetup(self):
        if ConstValues.PsIsSingleRun:  # 读取文件需要花费一些时间，所以界面会延迟一下
            self.RemoveFPIsFinished = True
            filePath = "./intermediateFiles/_5_removeFalsePositive/" + ConstValues.PsNameRemoveFPFrom_DelIsoResult
            if self.RemoveFPId == 2:
                filePath = "./intermediateFiles/_5_removeFalsePositive/" + ConstValues.PsNameRemoveFPFrom_PeakDisResult
            self.RemoveFPResult[0] = ReadExcelToList(filepath=filePath, hasNan=True)
        # 画图前前需要先读入数据
        if not self.RemoveFPIsFinished:
            PromptBox().warningMessage(ConstValues.PsPlotErrorMessage)  # 弹出错误提示
            return False
        # 更新数据
        self.PlotConfirm = False  # 每次绘图前需要重置
        self.PlotList = [
            self.RemoveFPId,  # 判断选择了哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
            self.RemoveFPResult[0],  # 所有类别去假阳性的结果，二维列表，有表头
            self.PlotTitleName,
            self.PlotTitleColor,
            self.PlotXAxisName,
            self.PlotXAxisColor,
            self.PlotYAxisName,
            self.PlotYAxisColor,
            self.PlotHasEnter,  # 记录是否进入过PlotSetup()函数
            self.PlotType,  # 绘图类型
            self.PlotClassList,  # 列表，需要绘制的类型，例子：["CH", "N1"]
            self.PlotClassItem,  # 列表，需要绘制的类型，例子：["CH"]，对应单选钮，长度必须为1
            self.PlotDBENum,  # 整数，记录用户选择的DBE数目
            self.PlotConfirm
        ]

        try:
            newParameters = SetupInterface(self.MainWindowsStyle).PlotSetup(self.PlotList)
            self.UpdateData("PlotSetup", newParameters)
        except Exception as e:
            if ConstValues.PsIsDebug:
                print("Error_PlotSetup_MainWin : ", e)
                traceback.print_exc()
            PromptBox().errorMessage("绘图设置出现错误!")

        # 判断是否要绘图
        return self.PlotConfirm

    # 模式选择设置
    def StartModeSetup(self):

        self.startModeConfirm = False  # 每次运行前需要重置
        self.startModeList = [
            self.startMode,
            self.startModeConfirm
        ]

        try:
            newParameters = SetupInterface(self.MainWindowsStyle).StartModeSetup(self.startModeList)
            self.UpdateData("StartModeSetup", newParameters)
        except Exception as e:
            if ConstValues.PsIsDebug:
                print("Error_StartModeSetup_MainWin : ", e)
                traceback.print_exc()
            PromptBox().errorMessage("模式选择设置出现错误!")

        return self.startModeConfirm

    # 去空白 #######################################
    def DeleteBlank(self):
        # 程序运行前准备工作
        if not self.BeforeRunning("DeleteBlank"):
            return
        # 处理扣空白，另起一个线程运行扣空白代码，主界面可以操作
        self.StartRunning("DeleteBlank")
        # 程序开始运行后收尾工作
        self.AfterRunning("DeleteBlank")

    # 数据库生成
    def GenerateDataBase(self):
        if not self.BeforeRunning("GenerateDataBase"):
            return
        self.StartRunning("GenerateDataBase")
        self.AfterRunning("GenerateDataBase")

    # 搜同位素
    def DeleteIsotope(self):
        if not self.BeforeRunning("DeleteIsotope"):
            return
        self.StartRunning("DeleteIsotope")
        self.AfterRunning("DeleteIsotope")

    # 峰识别
    def PeakDistinguish(self):
        if not self.BeforeRunning("PeakDistinguish"):
            return
        self.StartRunning("PeakDistinguish")
        self.AfterRunning("PeakDistinguish")

    # 去假阳性
    def RemoveFalsePositive(self):
        if not self.BeforeRunning("RemoveFalsePositive"):
            return
        self.StartRunning("RemoveFalsePositive")
        self.AfterRunning("RemoveFalsePositive")

    # 峰检测
    def PeakDivision(self):
        if not self.BeforeRunning("PeakDivision"):
            return
        self.StartRunning("PeakDivision")
        self.AfterRunning("PeakDivision")

    # 画图
    def Plot(self):
        if not self.BeforeRunning("Plot"):
            return
        self.StartRunning("Plot")
        self.AfterRunning("Plot")  # 暂时不需要使用

    # 全部开始
    def StartMode(self):
        if not self.BeforeRunning("StartMode"):
            return
        self.StartRunning("StartMode")
        self.AfterRunning("StartMode")

    # 辅助函数 ####################################### 多进程数据返回接收
    def HandleData(self, retList):
        try:
            if retList[0] == "ClassDeleteBlank":
                self.deleteBlankResult = retList[1]
                self.deleteBlankIsFinished = retList[2]
                # 数据显示到界面
                parent = self.mainTreeChild2
                name = ConstValues.PsNameDeleteBlank
                data = self.deleteBlankResult
                icon = ConstValues.PsqtaIconOpenFileExcel
                functionStr = "去空白处理完毕！"
                self.AddTreeItemShowData(parent, name, data, self.promptGif, icon, functionStr)
            elif retList[0] == "ClassGenerateDataBase":
                self.GDBResult = retList[1]
                self.GDBIsFinished = retList[2]
                # 数据显示到界面
                parent = self.mainTreeChild3
                name = ConstValues.PsNameGDB
                data = self.GDBResult
                icon = ConstValues.PsqtaIconOpenFileExcel
                functionStr = "数据库生成处理完毕！"
                self.AddTreeItemShowData(parent, name, data, self.promptGif, icon, functionStr)
            elif retList[0] == "ClassDeleteIsotope":
                self.DelIsoResult = retList[1]
                self.DelIsoIsFinished = retList[2]
                # 数据显示到界面
                parent = self.mainTreeChild4
                name = ConstValues.PsNameDeleteIsotope
                data = self.DelIsoResult
                icon = ConstValues.PsqtaIconOpenFileExcel
                functionStr = "搜同位素处理完毕！"
                self.AddTreeItemShowData(parent, name, data, self.promptGif, icon, functionStr)
            elif retList[0] == "ClassPeakDistinguish":
                self.PeakDisResult = retList[1]  # 列表，有三个数据
                self.PeakDisIsFinished = retList[2]
                # 数据显示到界面
                parent = self.mainTreeChild5
                name = ConstValues.PsNamePeakDistinguish
                data = self.PeakDisResult[0]
                icon = ConstValues.PsqtaIconOpenFileExcel
                functionStr = "峰识别处理完毕！"
                self.AddTreeItemShowData(parent, name, data, self.promptGif, icon, functionStr)
            elif retList[0] == "ClassRemoveFalsePositive":
                self.RemoveFPResult = retList[1]  # 列表，有两个数据
                self.RemoveFPIsFinished = retList[2]
                # 数据显示到界面
                parent = self.mainTreeChild6
                name = "RemoveFPResult.xlsx"
                if self.RemoveFPId == 1:  # self.RemoveFPId取值只可能为1或者2
                    name = ConstValues.PsNameRemoveFPFrom_DelIsoResult
                elif self.RemoveFPId == 2:
                    name = ConstValues.PsNameRemoveFPFrom_PeakDisResult
                data = self.RemoveFPResult[0]
                icon = ConstValues.PsqtaIconOpenFileExcel
                functionStr = "去假阳性处理完毕！"
                self.AddTreeItemShowData(parent, name, data, self.promptGif, icon, functionStr)
            elif retList[0] == "ClassPeakDivision":
                self.PeakDivResult = retList[1]
                self.PeakDivIsFinished = retList[2]
                # 数据显示到界面
                parent = self.mainTreeChild7
                name = ConstValues.PsNamePeakDivision
                data = self.PeakDivResult
                icon = ConstValues.PsqtaIconOpenFileExcel
                functionStr = "峰检测处理完毕！"
                self.AddTreeItemShowData(parent, name, data, self.promptGif, icon, functionStr)
            elif retList[0] == "ClassPlot":
                # 输出文件路径
                self.PlotImagePath = retList[1]
                # 画图原始数据
                self.PlotRawData = retList[2]  # 必须为二维列表，并且第二个维度必须相同
                if ConstValues.PsIsDebug:
                    print(
                        "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                        sys._getframe().f_code.co_name, "\" method***：",
                        "self.PlotImagePath：", self.PlotImagePath
                    )
                    print(
                        "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                        sys._getframe().f_code.co_name, "\" method***：",
                        "self.PlotRawData：", self.PlotRawData
                    )
                # 检查数据合法性
                if self.PlotImagePath is None:
                    return
                # 将数据展示到界面上
                self.AddTreeItemPlot(self.PlotImagePath, list(zip(*self.PlotRawData)), "图形绘制成功!")
            elif retList[0] == "ImportSampleFile":
                # 读入数据，并显示到主界面
                self.sampleData = retList[1]
                if ConstValues.PsIsDebug:
                    print(
                        "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                        sys._getframe().f_code.co_name, "\" method***：",
                        "self.sampleData：", self.sampleData
                    )
                # 处理过程
                parent = self.mainTreeChild1
                name = self.sampleFilePath.split("/")[-1]
                self.sampleNameList[0] = name
                data = self.sampleData
                icon = ConstValues.PsqtaIconOpenFileExcel
                functionStr = "样本导入完成!"
                self.AddTreeItemShowData(parent, name, data, self.promptGif, icon, functionStr)
            elif retList[0] == "ImportBlankFile":
                # 读入数据，并显示到主界面
                self.blankData = retList[1]
                if ConstValues.PsIsDebug:
                    print(
                        "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                        sys._getframe().f_code.co_name, "\" method***：",
                        "self.blankData：", self.blankData
                    )
                # 处理过程
                parent = self.mainTreeChild1
                name = self.blankFilePath.split("/")[-1]
                self.blankNameList[0] = name
                data = self.blankData
                icon = ConstValues.PsqtaIconOpenFileExcel
                functionStr = "空白导入完成!"
                self.AddTreeItemShowData(parent, name, data, self.promptGif, icon, functionStr)
            elif retList[0] == "ImportTICFile":
                # 读入数据，并显示到主界面
                self.TICData = retList[1]
                self.TICDataDictionary = retList[2]
                # if ConstValues.PsIsDebug:
                #     print(self.TICData)
                # 处理过程
                parent = self.mainTreeChild1
                name = self.TICFilePath.split("/")[-1]
                self.TICNameList[0] = name
                data = self.TICData
                icon = ConstValues.PsqtaIconOpenFileTxt
                functionStr = "总离子流图导入完成!"
                self.AddTreeItemShowData(parent, name, data, self.promptGif, icon, functionStr)
            elif retList[0] == "StartMode":
                # 更新状态
                if ConstValues.PsIsShowGif:
                    self.promptGif.closeGif()
            elif retList[0] == "deleteBlankFinished":
                self.deleteBlankResult = retList[1]
                self.deleteBlankIsFinished = retList[2]
                functionStr = retList[3]
                # 数据显示到界面
                parent = self.mainTreeChild2
                name = ConstValues.PsNameDeleteBlank
                data = self.deleteBlankResult
                icon = ConstValues.PsqtaIconOpenFileExcel
                self.AddTreeItemShowData(parent, name, data, None, icon, functionStr)
            elif retList[0] == "GDBFinished":
                self.GDBResult = retList[1]
                self.GDBIsFinished = retList[2]
                functionStr = retList[3]
                # 数据显示到界面
                parent = self.mainTreeChild3
                name = ConstValues.PsNameGDB
                data = self.GDBResult
                icon = ConstValues.PsqtaIconOpenFileExcel
                self.AddTreeItemShowData(parent, name, data, None, icon, functionStr)
            elif retList[0] == "DelIsoFinished":
                self.DelIsoResult = retList[1]
                self.DelIsoIsFinished = retList[2]
                functionStr = retList[3]
                # 数据显示到界面
                parent = self.mainTreeChild4
                name = ConstValues.PsNameDeleteIsotope
                data = self.DelIsoResult
                icon = ConstValues.PsqtaIconOpenFileExcel
                self.AddTreeItemShowData(parent, name, data, None, icon, functionStr)
            elif retList[0] == "PeakDisFinished":
                self.PeakDisResult = retList[1]  # 列表，有三个数据
                self.PeakDisIsFinished = retList[2]
                functionStr = retList[3]
                # 数据显示到界面
                parent = self.mainTreeChild5
                name = ConstValues.PsNamePeakDistinguish
                data = self.PeakDisResult[0]
                icon = ConstValues.PsqtaIconOpenFileExcel
                self.AddTreeItemShowData(parent, name, data, None, icon, functionStr)
            elif retList[0] == "RemoveFPFinished":
                self.RemoveFPResult = retList[1]  # 列表，有两个数据
                self.RemoveFPIsFinished = retList[2]
                functionStr = retList[3]
                # 数据显示到界面
                parent = self.mainTreeChild6
                name = "RemoveFPResult.xlsx"
                if self.RemoveFPId == 1:  # self.RemoveFPId取值只可能为1或者2
                    name = ConstValues.PsNameRemoveFPFrom_DelIsoResult
                elif self.RemoveFPId == 2:
                    name = ConstValues.PsNameRemoveFPFrom_PeakDisResult
                data = self.RemoveFPResult[0]
                icon = ConstValues.PsqtaIconOpenFileExcel
                self.AddTreeItemShowData(parent, name, data, None, icon, functionStr)
            elif retList[0] == "PeakDivFinished":
                self.PeakDivResult = retList[1]
                self.PeakDivIsFinished = retList[2]
                functionStr = retList[3]
                # 数据显示到界面
                parent = self.mainTreeChild7
                name = ConstValues.PsNamePeakDivision
                data = self.PeakDivResult
                icon = ConstValues.PsqtaIconOpenFileExcel
                self.AddTreeItemShowData(parent, name, data, None, icon, functionStr)
            elif retList[0] == "Error_CDB_MultiThread":
                if ConstValues.PsIsShowGif:
                    self.promptGif.closeGif()
                PromptBox().errorMessage("去空白出现错误!")
            elif retList[0] == "Error_CGDB_MultiThread":
                if ConstValues.PsIsShowGif:
                    self.promptGif.closeGif()
                PromptBox().errorMessage("数据库生成出现错误!")
            elif retList[0] == "Error_CDI_MultiThread":
                if ConstValues.PsIsShowGif:
                    self.promptGif.closeGif()
                PromptBox().errorMessage("去同位素出现错误!")
            elif retList[0] == "Error_CPD1_MultiThread":
                if ConstValues.PsIsShowGif:
                    self.promptGif.closeGif()
                PromptBox().errorMessage("峰识别出现错误!")
            elif retList[0] == "Error_CRFP_MultiThread":
                if ConstValues.PsIsShowGif:
                    self.promptGif.closeGif()
                PromptBox().errorMessage("去假阳性出现错误!")
            elif retList[0] == "Error_CPD2_MultiThread":
                if ConstValues.PsIsShowGif:
                    self.promptGif.closeGif()
                PromptBox().errorMessage("峰检测出现错误!")
            elif retList[0] == "Error_CPlot_MultiThread":
                if ConstValues.PsIsShowGif:
                    self.promptGif.closeGif()
                PromptBox().errorMessage("绘图出现错误!")
            elif retList[0] == "Error_ImSample_MultiThread":
                if ConstValues.PsIsShowGif:
                    self.promptGif.closeGif()
                PromptBox().errorMessage("导入样本文件出现错误!")
            elif retList[0] == "Error_ImBlank_MultiThread":
                if ConstValues.PsIsShowGif:
                    self.promptGif.closeGif()
                PromptBox().errorMessage("导入空白文件出现错误!")
            elif retList[0] == "Error_ImTIC_MultiThread":
                if ConstValues.PsIsShowGif:
                    self.promptGif.closeGif()
                PromptBox().errorMessage("导入样本总离子图文件出现错误!")
            elif retList[0] == "Error_StartMode_MultiThread":
                # 关闭弹出的程序运行指示对话框
                self.promptGif.closeGif()
                PromptBox().errorMessage("程序运行出现错误!")
        except Exception as e:
            if ConstValues.PsIsDebug:
                print("Error_HandleData : ", e)
                if ConstValues.PsIsShowGif and self.whetherShowGif:
                    self.promptGif.closeGif()
                PromptBox().errorMessage("出现错误！错误标识：Error_HandleData")
                traceback.print_exc()

    # 设置：数据更新
    def UpdateData(self, Type, newParameters):
        if Type == "DeleteBlankSetup":
            self.deleteBlankIntensity = newParameters[0]
            self.deleteBlankPPM = newParameters[1]
            self.deleteBlankPercentage = newParameters[2]
            self.deleteBlankList = [
                self.sampleFilePath,  # 格式：字符串
                self.blankFilePath,  # 格式：字符串
                self.deleteBlankIntensity,  # 格式：整数
                self.deleteBlankPPM,  # 格式：浮点数
                self.deleteBlankPercentage  # 格式：整数
            ]
            if ConstValues.PsIsDebug:
                print(self.deleteBlankList[2:])
        elif Type == "GenerateDataBaseSetup":
            self.GDBClass = newParameters[0]
            self.GDBCarbonRangeLow = newParameters[1]
            self.GDBCarbonRangeHigh = newParameters[2]
            self.GDBDBERageLow = newParameters[3]
            self.GDBDBERageHigh = newParameters[4]
            self.GDBM_ZRageLow = newParameters[5]
            self.GDBM_ZRageHigh = newParameters[6]
            self.GDB_MHPostive = newParameters[7]
            self.GDB_MPostive = newParameters[8]
            self.GDB_MHNegative = newParameters[9]
            self.GDB_MNegative = newParameters[10]
            self.GDBList = [
                self.GDBClass,  # 格式：列表，列表中均为字符串
                self.GDBCarbonRangeLow,  # 格式：整数
                self.GDBCarbonRangeHigh,  # 格式：整数
                self.GDBDBERageLow,  # 格式：整数
                self.GDBDBERageHigh,  # 格式：整数
                self.GDBM_ZRageLow,  # 格式：整数
                self.GDBM_ZRageHigh,  # 格式：整数
                self.GDB_MHPostive,  # 格式：bool
                self.GDB_MPostive,  # 格式：bool
                self.GDB_MHNegative,  # 格式：bool
                self.GDB_MNegative  # 格式：bool
            ]

            if ConstValues.PsIsDebug:
                print(self.GDBList)
        elif Type == "DeleteIsotopeSetup":
            self.DelIsoIntensityX = newParameters[0]
            self.DelIso_13C2RelativeIntensity = newParameters[1]
            self.DelIsoMassDeviation = newParameters[2]
            self.DelIsoIsotopeMassDeviation = newParameters[3]
            self.DelIsoIsotopeIntensityDeviation = newParameters[4]
            self.DelIsoList = [
                self.deleteBlankResult,  # 删空白的结果（格式：list二维数组，有表头）
                self.GDBResult,  # 数据库生成的结果（格式：list二维数组，有表头）
                self.deleteBlankIntensity,
                self.DelIsoIntensityX,  # 格式：整数
                self.DelIso_13C2RelativeIntensity,  # 格式：整数
                self.DelIsoMassDeviation,  # 格式：浮点数
                self.DelIsoIsotopeMassDeviation,  # 格式：浮点数
                self.DelIsoIsotopeIntensityDeviation  # 格式：整数
            ]

            if ConstValues.PsIsDebug:
                print(self.DelIsoList[3:])
        elif Type == "PeakDistinguishSetup":
            self.PeakDisContinuityNum = newParameters[0]
            self.PeakDisMassDeviation = newParameters[1]
            self.PeakDisDiscontinuityPointNum = newParameters[2]
            self.PeakDisClassIsNeed = newParameters[3]
            self.PeakDisClass = newParameters[4]
            self.PeakDisList = [
                self.TICDataDictionary,
                self.DelIsoResult,
                self.PeakDisContinuityNum,
                self.PeakDisMassDeviation,
                self.PeakDisDiscontinuityPointNum,
                self.PeakDisClassIsNeed,  # 第二部分
                self.PeakDisClass,
            ]

            # 更新状态栏
            self.TBpeakDivision.setEnabled(self.PeakDisClassIsNeed)
            if ConstValues.PsIsDebug:
                print(self.PeakDisList[2:])
        elif Type == "RemoveFalsePositiveSetup":
            self.RemoveFPId = newParameters[0]
            self.RemoveFPContinue_CNum = newParameters[1]
            self.RemoveFPContinue_DBENum = newParameters[2]
            self.RemoveFPList = [
                self.DelIsoResult,
                self.PeakDisResult,
                self.RemoveFPId,  # 决定选择哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
                self.RemoveFPContinue_CNum,
                self.RemoveFPContinue_DBENum
            ]

            if ConstValues.PsIsDebug:
                print(self.RemoveFPList[2:])
        elif Type == "PeakDivisionSetup":
            self.PeakDivNoiseThreshold = newParameters[0]
            self.PeakDivRelIntensity = newParameters[1]
            self.PeakDivNeedMerge = newParameters[2]
            self.PeakDivNeedGenImage = newParameters[3]
            self.PeakDivList = [
                self.RemoveFPId,  # 判断选择了哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
                self.RemoveFPResult[1],  # 去假阳性后的需要峰识别（第二部分）结果，二维列表，无表头
                self.PeakDisResult[2],  # 第三个是txt文件中RT值(从小到大排序)
                self.PeakDivNoiseThreshold,
                self.PeakDivRelIntensity,
                self.PeakDivNeedMerge,  # 该参数决定是否需要将溶剂效应的第一个峰融合到第二个峰
                self.PeakDivNeedGenImage  # 该参数决定是否生成图片信息
            ]

            if ConstValues.PsIsDebug:
                print(self.PeakDivList[3:])
        elif Type == "PlotSetup":
            self.PlotTitleName = newParameters[0]  # 标题名称
            self.PlotTitleColor = newParameters[1]  # 标题颜色
            self.PlotXAxisName = newParameters[2]  # x轴名称
            self.PlotXAxisColor = newParameters[3]  # x轴颜色
            self.PlotYAxisName = newParameters[4]  # y轴名称
            self.PlotYAxisColor = newParameters[5]  # y轴颜色
            self.PlotHasEnter = newParameters[6]  # 记录是否进入过PlotSetup()函数
            self.PlotType = newParameters[7]  # 绘图类型
            self.PlotClassList = newParameters[8]  # 列表，需要绘制的类型，例子：["CH", "N1"]
            self.PlotClassItem = newParameters[9]  # 列表，需要绘制的类型，例子：["CH"]，对应单选钮，长度必须为1
            self.PlotDBENum = newParameters[10]  # 整数，记录用户选择的DBE数目
            self.PlotConfirm = newParameters[11]
            self.PlotList = [
                self.RemoveFPId,  # 判断选择了哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
                self.RemoveFPResult[0],  # 所有类别去假阳性的结果，二维列表，有表头
                self.PlotTitleName,
                self.PlotTitleColor,
                self.PlotXAxisName,
                self.PlotXAxisColor,
                self.PlotYAxisName,
                self.PlotYAxisColor,
                self.PlotHasEnter,  # 记录是否进入过PlotSetup()函数
                self.PlotType,  # 绘图类型
                self.PlotClassList,  # 列表，需要绘制的类型，例子：["CH", "N1"]
                self.PlotClassItem,  # 列表，需要绘制的类型，例子：["CH"]，对应单选钮，长度必须为1
                self.PlotDBENum,  # 整数，记录用户选择的DBE数目
                self.PlotConfirm
            ]

            if ConstValues.PsIsDebug:
                print(self.PlotList[2:])
        elif Type == "StartModeSetup":
            # 运行模式
            self.startMode = newParameters[0]
            # 确定开始运行
            self.startModeConfirm = newParameters[1]
            self.startModeList = [
                self.startMode,
                self.startModeConfirm
            ]

            if ConstValues.PsIsDebug:
                print(
                    "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                    sys._getframe().f_code.co_name, "\" method***：",
                    "self.startModeList：", self.startModeList
                )

    # 程序运行前准备工作
    def BeforeRunning(self, Type):
        if Type == "DeleteBlank":
            # 扣空白前需要先读入数据
            if self.sampleFilePath == "" or self.blankFilePath == "":
                PromptBox().warningMessage(ConstValues.PsDeleteBlankErrorMessage)  # 弹出错误提示
                return False
            # 因为有self.sampleFilePath，self.blankFilePath，所以需要更新self.sampleFilePath,self.blankFilePath（最开始前两项为空字符串）
            self.deleteBlankList = [
                self.sampleFilePath,  # 格式：字符串
                self.blankFilePath,  # 格式：字符串
                self.deleteBlankIntensity,  # 格式：整数
                self.deleteBlankPPM,  # 格式：浮点数
                self.deleteBlankPercentage  # 格式：整数
            ]
            if ConstValues.PsNameDeleteBlank in self.mainDataNameSetAll:
                self.mainNeedCover = PromptBox().warningMessage("是否确定覆盖当前文件?")
                return self.mainNeedCover
        elif Type == "GenerateDataBase":
            if not (self.GDB_MHPostive or self.GDB_MPostive or self.GDB_MHNegative or self.GDB_MNegative):
                PromptBox().warningMessage("生成数据库需要至少一种离子模式!")
                return False
            if ConstValues.PsNameGDB in self.mainDataNameSetAll:
                self.mainNeedCover = PromptBox().warningMessage("是否确定覆盖当前文件?")
                return self.mainNeedCover
        elif Type == "DeleteIsotope":
            # 单独运行，调试使用
            if ConstValues.PsIsSingleRun:
                self.deleteBlankIsFinished = True
                filePath = "./intermediateFiles/_1_deleteBlank/" + ConstValues.PsNameDeleteBlank
                self.deleteBlankResult = ReadExcelToList(filepath=filePath, hasNan=False)
                self.GDBIsFinished = True
                filePath = "./intermediateFiles/_2_generateDataBase/" + ConstValues.PsNameGDB
                self.GDBResult = ReadExcelToList(filepath=filePath, hasNan=False)
                if ConstValues.PsNameGDB in self.mainDataNameSetAll:
                    self.mainNeedCover = PromptBox().warningMessage("是否确定覆盖当前文件?")
                    return self.mainNeedCover
            # 去同位素前需要扣空白，数据库生成
            if (not self.deleteBlankIsFinished) or (not self.GDBIsFinished):
                PromptBox().warningMessage(ConstValues.PsDeleteIsotopeErrorMessage)
                return False
            # 因为有self.deleteBlankResult和self.GDBResult，所以需要更新self.DelIsoList（最开始前两项为空）
            self.DelIsoList = [
                self.deleteBlankResult,  # 删空白的结果（格式：list二维数组，有表头）
                self.GDBResult,  # 数据库生成的结果（格式：list二维数组，有表头）
                self.deleteBlankIntensity,
                self.DelIsoIntensityX,  # 格式：整数
                self.DelIso_13C2RelativeIntensity,  # 格式：整数
                self.DelIsoMassDeviation,  # 格式：浮点数
                self.DelIsoIsotopeMassDeviation,  # 格式：浮点数
                self.DelIsoIsotopeIntensityDeviation  # 格式：整数
            ]
            if ConstValues.PsNameDeleteIsotope in self.mainDataNameSetAll:
                self.mainNeedCover = PromptBox().warningMessage("是否确定覆盖当前文件?")
                return self.mainNeedCover
        elif Type == "PeakDistinguish":
            # 扣空白前需要先读入数据
            if self.TICFilePath == "":
                PromptBox().warningMessage(ConstValues.PsPeakDistinguishErrorMessage1)  # 弹出错误提示
                return False
            # 单独运行，调试使用
            if ConstValues.PsIsSingleRun:
                self.DelIsoIsFinished = True
                filePath = "./intermediateFiles/_3_deleteIsotope/" + ConstValues.PsNameDeleteIsotope
                self.DelIsoResult = ReadExcelToList(filepath=filePath, hasNan=True)
            # 峰识别前需要去同位素
            if not self.DelIsoIsFinished:
                PromptBox().warningMessage(ConstValues.PsPeakDistinguishErrorMessage2)
                return False
            # 因为有self.TICFilePath，self.DelIsoResult，所以需要更新self.TICFilePath，self.PeakDisList（最开始第一项为空字符串，第二项为空）
            self.PeakDisList = [
                self.TICDataDictionary,
                self.DelIsoResult,
                self.PeakDisContinuityNum,
                self.PeakDisMassDeviation,
                self.PeakDisDiscontinuityPointNum,
                self.PeakDisClassIsNeed,  # 第二部分
                self.PeakDisClass,
            ]
            if ConstValues.PsNamePeakDistinguish in self.mainDataNameSetAll:
                self.mainNeedCover = PromptBox().warningMessage("是否确定覆盖当前文件?")
                return self.mainNeedCover
        elif Type == "RemoveFalsePositive":
            # 单独运行，调试使用
            if ConstValues.PsIsSingleRun:
                if self.RemoveFPId == 1:
                    self.DelIsoIsFinished = True
                    filePath = "./intermediateFiles/_3_deleteIsotope/" + ConstValues.PsNameDeleteIsotope
                    self.DelIsoResult = ReadExcelToList(filepath=filePath, hasNan=True)
                elif self.RemoveFPId == 2:
                    self.PeakDisIsFinished = True
                    self.PeakDisResult = [[], [], []]
            # 去假阳性前需要去同位素 或者 峰识别第一阶段
            if self.RemoveFPId == 1:
                if not self.DelIsoIsFinished:
                    PromptBox().warningMessage(ConstValues.PsRemoveFPErrorMessage1)
                    return False
            elif self.RemoveFPId == 2:
                if not self.PeakDisIsFinished:
                    PromptBox().warningMessage(ConstValues.PsRemoveFPErrorMessage2)
                    return False
            # 更新数据
            self.RemoveFPList = [
                self.DelIsoResult,
                self.PeakDisResult,  # 列表，有三个数据
                self.RemoveFPId,  # 决定选择哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
                self.RemoveFPContinue_CNum,
                self.RemoveFPContinue_DBENum
            ]
            if (ConstValues.PsNameRemoveFPFrom_DelIsoResult in self.mainDataNameSetAll) or \
                    (ConstValues.PsNameRemoveFPFrom_PeakDisResult in self.mainDataNameSetAll):
                self.mainNeedCover = PromptBox().warningMessage("是否确定覆盖当前文件?")
                return self.mainNeedCover
        elif Type == "PeakDivision":
            if self.RemoveFPId == 1:
                return False
            # 单独运行，调试使用
            if ConstValues.PsIsSingleRun:
                self.RemoveFPIsFinished = True
            # 峰检测之前需要 去假阳性
            if not self.RemoveFPIsFinished:
                PromptBox().warningMessage(ConstValues.PsPeakDivErrorMessage)
                return False
            # 更新数据
            self.PeakDivList = [
                self.RemoveFPId,  # 判断选择了哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
                self.RemoveFPResult[1],  # 去假阳性后的需要峰识别（第二部分）结果，二维列表，无表头，第5步
                self.PeakDisResult[2],  # 第三个是txt文件中RT值(从小到大排序)，第4步
                self.PeakDivNoiseThreshold,
                self.PeakDivRelIntensity,
                self.PeakDivNeedMerge,  # 该参数决定是否需要将溶剂效应的第一个峰融合到第二个峰
                self.PeakDivNeedGenImage  # 该参数决定是否生成图片信息
            ]
            if ConstValues.PsNamePeakDivision in self.mainDataNameSetAll:
                self.mainNeedCover = PromptBox().warningMessage("是否确定覆盖当前文件?")
                return self.mainNeedCover
        elif Type == "Plot":
            # 更新数据
            self.PlotList = [
                self.RemoveFPId,  # 判断选择了哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
                self.RemoveFPResult[0],  # 所有类别去假阳性的结果，二维列表，有表头
                self.PlotTitleName,
                self.PlotTitleColor,
                self.PlotXAxisName,
                self.PlotXAxisColor,
                self.PlotYAxisName,
                self.PlotYAxisColor,
                self.PlotHasEnter,  # 记录是否进入过PlotSetup()函数
                self.PlotType,  # 绘图类型
                self.PlotClassList,  # 列表，需要绘制的类型，例子：["CH", "N1"]
                self.PlotClassItem,  # 列表，需要绘制的类型，例子：["CH"]，对应单选钮，长度必须为1
                self.PlotDBENum,  # 整数，记录用户选择的DBE数目
                self.PlotConfirm
            ]
            # 更新过参数后，检查是否重名
            if self.PlotTitleName in self.mainPlotNameSetAll:
                self.mainPlotNeedCover = PromptBox().warningMessage("是否确定覆盖当前文件?")
                return self.mainPlotNeedCover
        elif Type == "StartMode":
            if self.startMode == 1:
                if self.sampleFilePath == "" or self.blankFilePath == "":
                    PromptBox().warningMessage("请选择需要处理的样本文件、空白文件!")  # 弹出错误提示
                    return False
            elif (self.startMode == 2) or (self.startMode == 3):
                if self.sampleFilePath == "" or self.blankFilePath == "" or self.TICFilePath == "":
                    PromptBox().warningMessage("请选择需要处理的样本文件、空白文件和总离子流图文件!")  # 弹出错误提示
                    return False
            elif self.startMode == 4:
                if self.sampleFilePath == "":
                    PromptBox().warningMessage("请选择需要处理的样本文件!")  # 弹出错误提示
                    return False
            elif (self.startMode == 5) or (self.startMode == 6):
                if self.sampleFilePath == "" or self.TICFilePath == "":
                    PromptBox().warningMessage("请选择需要处理的样本文件和总离子流图文件!")  # 弹出错误提示
                    return False

            if ConstValues.PsNameGDB in self.mainDataNameSetAll:
                self.mainNeedCover = PromptBox().warningMessage("是否确定覆盖当前文件?")
                return self.mainNeedCover
        elif Type == "ImportSampleFile":
            # 导入文件，并得到文件名称
            openfile_name = QFileDialog.getOpenFileName(self, '选择样本文件', ConstValues.PsReadFileDefaultDirectoy,
                                                        'Excel files(*.xlsx , *.xls)')
            self.sampleFilePath = openfile_name[0]
            if ConstValues.PsIsDebug:
                print(
                    "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                    sys._getframe().f_code.co_name, "\" method***：",
                    "self.sampleFilePath：", self.sampleFilePath
                )
            if self.sampleFilePath == "":
                return False
            # 检查是否重名
            name = self.sampleFilePath.split("/")[-1]
            if (name in self.blankNameList) or (name in self.TICNameList):
                PromptBox().informationMessageAutoClose("和其他文件重名，导入失败！", ConstValues.PsPromptBoxTime)
                return False
            # 如果已经存在样本文件，则需要确定是否替换
            if self.sampleNameList[0] is not None:
                if PromptBox().questionMessage("已经导入过样本文件，是否替换？"):
                    # 遍历所有节点，删除对应样本文件
                    oldNmae = self.sampleNameList[0]
                    item = QTreeWidgetItemIterator(self.mainTreeWidget)
                    while item.value():
                        treeWidgetItem = item.value()
                        if treeWidgetItem.text(0) == oldNmae:
                            treeWidgetItem.parent().removeChild(treeWidgetItem)
                            self.tabWidgetShowData.removeTab(
                                self.tabWidgetShowData.indexOf(globals()["tableWidget_" + oldNmae]))
                            self.mainDataNameSetAll.remove(oldNmae)
                            self.mainNeedCover = False
                            break
                        # 到下一个节点
                        item += 1
                else:
                    return False
            else:
                return PromptBox().questionMessage(name + "是否为样本文件？")
            # 更新数据
            self.deleteBlankList = [
                self.sampleFilePath,  # 格式：字符串
                self.blankFilePath,  # 格式：字符串
                self.deleteBlankIntensity,  # 格式：整数
                self.deleteBlankPPM,  # 格式：浮点数
                self.deleteBlankPercentage  # 格式：整数
            ]
        elif Type == "ImportBlankFile":
            # 导入文件，并得到文件名称
            openfile_name = QFileDialog.getOpenFileName(self, '选择空白文件', ConstValues.PsReadFileDefaultDirectoy,
                                                        'Excel files(*.xlsx , *.xls)')
            self.blankFilePath = openfile_name[0]
            if ConstValues.PsIsDebug:
                print(
                    "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                    sys._getframe().f_code.co_name, "\" method***：",
                    "self.blankFilePath：", self.blankFilePath
                )
            if self.blankFilePath == "":
                return False
            name = self.blankFilePath.split("/")[-1]
            if (name in self.sampleNameList) or (name in self.TICNameList):
                PromptBox().informationMessageAutoClose("和其他文件重名，导入失败！", ConstValues.PsPromptBoxTime)
                return False
            # 如果已经存在样本文件，则需要确定是否替换
            if self.blankNameList[0] is not None:
                if PromptBox().questionMessage("已经导入过空白文件，是否替换？"):
                    # 遍历所有节点，删除对应样本文件
                    oldNmae = self.blankNameList[0]
                    item = QTreeWidgetItemIterator(self.mainTreeWidget)
                    while item.value():
                        treeWidgetItem = item.value()
                        if treeWidgetItem.text(0) == oldNmae:
                            treeWidgetItem.parent().removeChild(treeWidgetItem)
                            self.tabWidgetShowData.removeTab(
                                self.tabWidgetShowData.indexOf(globals()["tableWidget_" + oldNmae]))
                            self.mainDataNameSetAll.remove(oldNmae)
                            self.mainNeedCover = False
                            break
                        # 到下一个节点
                        item += 1
                else:
                    return False
            else:
                return PromptBox().questionMessage(name + "是否为空白文件？")
            # 更新数据
            self.deleteBlankList = [
                self.sampleFilePath,  # 格式：字符串
                self.blankFilePath,  # 格式：字符串
                self.deleteBlankIntensity,  # 格式：整数
                self.deleteBlankPPM,  # 格式：浮点数
                self.deleteBlankPercentage  # 格式：整数
            ]
        elif Type == "ImportTICFile":
            # 导入文件，并得到文件名称
            openfile_name = QFileDialog.getOpenFileName(self, '选择总离子流图文件', ConstValues.PsReadFileDefaultDirectoy,
                                                        'Txt files(*.txt)')
            self.TICFilePath = openfile_name[0]
            if ConstValues.PsIsDebug:
                print(
                    "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                    sys._getframe().f_code.co_name, "\" method***：",
                    "self.TICFilePath：", self.TICFilePath
                )
            if self.TICFilePath == "":
                return False
            name = self.TICFilePath.split("/")[-1]
            if (name in self.sampleNameList) or (name in self.blankNameList):
                PromptBox().informationMessageAutoClose("和其他文件重名，导入失败！", ConstValues.PsPromptBoxTime)
                return False
            # 如果已经存在样本文件，则需要确定是否替换
            if self.TICNameList[0] is not None:
                if PromptBox().questionMessage("已经导入过TIC文件，是否替换？"):
                    # 遍历所有节点，删除对应样本文件
                    oldNmae = self.TICNameList[0]
                    item = QTreeWidgetItemIterator(self.mainTreeWidget)
                    while item.value():
                        treeWidgetItem = item.value()
                        if treeWidgetItem.text(0) == oldNmae:
                            treeWidgetItem.parent().removeChild(treeWidgetItem)
                            self.tabWidgetShowData.removeTab(
                                self.tabWidgetShowData.indexOf(globals()["tableWidget_" + oldNmae]))
                            self.mainDataNameSetAll.remove(oldNmae)
                            self.mainNeedCover = False
                            break
                        # 到下一个节点
                        item += 1
                else:
                    return False
            else:
                return PromptBox().questionMessage(name + "是否为TIC文件？")

        return True

    # 开启新进程，运行
    def StartRunning(self, Type):
        if Type == "DeleteBlank":
            self.deleteBlankMt = MultiThread("ClassDeleteBlank", self.deleteBlankList, self.outputFilesPath)
            self.deleteBlankMt.signal.connect(self.HandleData)
            self.deleteBlankMt.start()
        elif Type == "GenerateDataBase":
            self.GDBMt = MultiThread("ClassGenerateDataBase", self.GDBList, self.outputFilesPath)
            self.GDBMt.signal.connect(self.HandleData)
            self.GDBMt.start()
        elif Type == "DeleteIsotope":
            self.DelIsoMt = MultiThread("ClassDeleteIsotope", self.DelIsoList, self.outputFilesPath)
            self.DelIsoMt.signal.connect(self.HandleData)
            self.DelIsoMt.start()
        elif Type == "PeakDistinguish":
            self.PeakDisMt = MultiThread("ClassPeakDistinguish", self.PeakDisList, self.outputFilesPath)
            self.PeakDisMt.signal.connect(self.HandleData)
            self.PeakDisMt.start()
        elif Type == "RemoveFalsePositive":
            self.RemoveFPMt = MultiThread("ClassRemoveFalsePositive", self.RemoveFPList, self.outputFilesPath)
            self.RemoveFPMt.signal.connect(self.HandleData)
            self.RemoveFPMt.start()
        elif Type == "PeakDivision":
            self.PeakDivMt = MultiThread("ClassPeakDivision", self.PeakDivList, self.outputFilesPath)
            self.PeakDivMt.signal.connect(self.HandleData)
            self.PeakDivMt.start()
        elif Type == "Plot":
            self.PlotMt = MultiThread("ClassPlot", self.PlotList, self.outputFilesPath)
            self.PlotMt.signal.connect(self.HandleData)
            self.PlotMt.start()
        elif Type == "StartMode":
            startModeData = []
            if self.startMode == 1:
                # 1：去空白 --> 数据库生成 --> 搜同位素 --> 去假阳性
                self.RemoveFPId = 1  # 设置为去假阳性
                # 更新数据
                self.UpdateList()
                # 需要传入另一个线程的数据
                startModeData = [
                    self.deleteBlankList,
                    self.GDBList,
                    self.DelIsoList,
                    self.RemoveFPList
                ]
            elif self.startMode == 2:
                # 2：去空白 --> 数据库生成 --> 搜同位素 --> 峰提取 --> 去假阳性
                self.RemoveFPId = 2  # 设置为 峰提取
                # 更新数据
                self.UpdateList()
                # 需要传入另一个线程的数据
                startModeData = [
                    self.deleteBlankList,
                    self.GDBList,
                    self.DelIsoList,
                    self.PeakDisList,
                    self.RemoveFPList
                ]
            elif self.startMode == 3:
                # 3：去空白 --> 数据库生成 --> 搜同位素 --> 峰提取 --> 去假阳性 --> 峰检测
                self.RemoveFPId = 2  # 设置为 峰提取
                # 更新数据
                self.UpdateList()
                # 需要传入另一个线程的数据
                startModeData = [
                    self.deleteBlankList,
                    self.GDBList,
                    self.DelIsoList,
                    self.PeakDisList,
                    self.RemoveFPList,
                    self.PeakDivList
                ]
            elif self.startMode == 4:
                # 4：数据库生成 --> 搜同位素 --> 去假阳性
                self.RemoveFPId = 1  # 设置为去假阳性
                self.deleteBlankResult = self.sampleData[ConstValues.PsHeaderLine:]
                # 更新数据
                self.UpdateList()
                # 需要传入另一个线程的数据
                startModeData = [
                    self.GDBList,
                    self.DelIsoList,
                    self.RemoveFPList
                ]
            elif self.startMode == 5:
                # 5：数据库生成 --> 搜同位素 --> 峰提取 --> 去假阳性
                self.RemoveFPId = 2  # 设置为 峰提取
                self.deleteBlankResult = self.sampleData[ConstValues.PsHeaderLine:]
                # 更新数据
                self.UpdateList()
                # 需要传入另一个线程的数据
                startModeData = [
                    self.GDBList,
                    self.DelIsoList,
                    self.PeakDisList,
                    self.RemoveFPList
                ]
            elif self.startMode == 6:
                # 6：数据库生成 --> 搜同位素 --> 峰提取 --> 去假阳性 --> 峰检测
                self.RemoveFPId = 2  # 设置为 峰提取
                self.deleteBlankResult = self.sampleData[ConstValues.PsHeaderLine:]
                # 更新数据
                self.UpdateList()
                # 需要传入另一个线程的数据
                startModeData = [
                    self.GDBList,
                    self.DelIsoList,
                    self.PeakDisList,
                    self.RemoveFPList,
                    self.PeakDivList
                ]
            # 启动线程，开始处理
            startMode = "StartMode" + str(self.startMode)
            self.StartModeMt = MultiThread(startMode, startModeData, self.outputFilesPath)
            self.StartModeMt.signal.connect(self.HandleData)
            self.StartModeMt.start()
        elif Type == "ImportSampleFile":
            self.ImportSampleFileMt = MultiThread("ImportSampleFile", [self.sampleFilePath], self.outputFilesPath)
            self.ImportSampleFileMt.signal.connect(self.HandleData)
            self.ImportSampleFileMt.start()
        elif Type == "ImportBlankFile":
            self.ImportBlankFileMt = MultiThread("ImportBlankFile", [self.blankFilePath], self.outputFilesPath)
            self.ImportBlankFileMt.signal.connect(self.HandleData)
            self.ImportBlankFileMt.start()
        elif Type == "ImportTICFile":
            self.ImportTICFileeMt = MultiThread("ImportTICFile", [self.TICFilePath], self.outputFilesPath)
            self.ImportTICFileeMt.signal.connect(self.HandleData)
            self.ImportTICFileeMt.start()

    # 程序开始运行后收尾工作
    def AfterRunning(self, Type):
        self.whetherShowGif = True
        if Type == "DeleteBlank":
            # 更新状态栏消息
            self.statusSetup(ConstValues.PsMainWindowStatusMessage, "正在处理扣空白，请稍后...")
            # 弹出提示框
            if ConstValues.PsIsShowGif:
                self.promptGif.showGif("正在处理扣空白，请稍后...", ConstValues.PsIconLoading)
        elif Type == "GenerateDataBase":
            # 更新状态栏消息
            self.statusSetup(ConstValues.PsMainWindowStatusMessage, "正在生成数据库，请稍后...")
            # 弹出提示框
            if ConstValues.PsIsShowGif:
                self.promptGif.showGif("正在生成数据库，请稍后...", ConstValues.PsIconLoading)
        elif Type == "DeleteIsotope":
            # 更新状态栏消息
            self.statusSetup(ConstValues.PsMainWindowStatusMessage, "正在处理去同位素，请稍后...")
            # 弹出提示框
            if ConstValues.PsIsShowGif:
                self.promptGif.showGif("正在处理去同位素，请稍后...", ConstValues.PsIconLoading)
        elif Type == "PeakDistinguish":
            # 更新状态栏消息
            self.statusSetup(ConstValues.PsMainWindowStatusMessage, "正在处理去峰识别，请稍后...")
            # 弹出提示框
            if ConstValues.PsIsShowGif:
                self.promptGif.showGif("正在处理峰识别，请稍后...", ConstValues.PsIconLoading)
        elif Type == "RemoveFalsePositive":
            # 更新状态栏消息
            self.statusSetup(ConstValues.PsMainWindowStatusMessage, "正在处理去假阳性，请稍后...")
            # 弹出提示框
            if ConstValues.PsIsShowGif:
                self.promptGif.showGif("正在处理去假阳性，请稍后...", ConstValues.PsIconLoading)
        elif Type == "PeakDivision":
            # 更新状态栏消息
            self.statusSetup(ConstValues.PsMainWindowStatusMessage, "正在处理峰检测，请稍后...")
            # 弹出提示框
            if ConstValues.PsIsShowGif:
                self.promptGif.showGif("正在处理峰检测，请稍后...", ConstValues.PsIconLoading)
        elif Type == "StartMode":
            # 更新状态栏消息
            self.statusSetup(ConstValues.PsMainWindowStatusMessage, "正在处理中，请稍后...")
            # 弹出提示框
            if ConstValues.PsIsShowGif:
                self.promptGif.showGif("正在处理中，请稍后...", ConstValues.PsIconLoading)
        elif Type == "ImportSampleFile":
            # 更新状态栏消息
            self.statusSetup(ConstValues.PsMainWindowStatusMessage, "正在导入样本文件，请稍后...")
            # 弹出提示框
            if ConstValues.PsIsShowGif:
                self.promptGif.showGif("正在导入样本文件，请稍后...", ConstValues.PsIconLoading)
        elif Type == "ImportBlankFile":
            # 更新状态栏消息
            self.statusSetup(ConstValues.PsMainWindowStatusMessage, "正在导入空白文件，请稍后...")
            # 弹出提示框
            if ConstValues.PsIsShowGif:
                self.promptGif.showGif("正在导入空白文件，请稍后...", ConstValues.PsIconLoading)
        elif Type == "ImportTICFile":
            # 更新状态栏消息
            self.statusSetup(ConstValues.PsMainWindowStatusMessage, "正在导入总离子图文件，请稍后...")
            # 弹出提示框
            if ConstValues.PsIsShowGif:
                self.promptGif.showGif("正在导入总离子图文件，请稍后...", ConstValues.PsIconLoading)
        else:
            self.whetherShowGif = False

    # 画图
    def SetupAndPlot(self):
        # 参数设置
        if self.PlotSetup():
            # 绘图
            self.Plot()

    # 模式选择
    def SetupAndStartMode(self):
        # 参数设置
        if self.StartModeSetup():
            # 绘图
            self.StartMode()

    # 主题选择
    def ThemeSelect(self, theme):
        PromptBox().informationMessageAutoClose(theme + "主题选择成功，下次重启生效。", 2)
        try:
            with open("./__system/config.txt", "w") as f:
                f.write(theme)
        except Exception as e:
            if ConstValues.PsIsDebug:
                print("Error_WriteConfig : ", e)
                PromptBox().errorMessage("出现错误！错误标识：Error_WriteConfig")
                traceback.print_exc()

    # 帮助界面
    def Help(self, functionStr):
        if ConstValues.PsIsDebug:
            print(
                "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                sys._getframe().f_code.co_name, "\" method***：",
                "functionStr:", functionStr
            )
        # 创建对话框
        ClassHelp(functionStr, self.MainWindowsStyle).Help()

    # 更新数据
    def UpdateList(self):
        self.deleteBlankList = [
            self.sampleFilePath,  # 格式：字符串
            self.blankFilePath,  # 格式：字符串
            self.deleteBlankIntensity,  # 格式：整数
            self.deleteBlankPPM,  # 格式：浮点数
            self.deleteBlankPercentage  # 格式：整数
        ]
        self.GDBList = [
            self.GDBClass,  # 格式：列表，列表中均为字符串
            self.GDBCarbonRangeLow,  # 格式：整数
            self.GDBCarbonRangeHigh,  # 格式：整数
            self.GDBDBERageLow,  # 格式：整数
            self.GDBDBERageHigh,  # 格式：整数
            self.GDBM_ZRageLow,  # 格式：整数
            self.GDBM_ZRageHigh,  # 格式：整数
            self.GDB_MHPostive,  # 格式：bool
            self.GDB_MPostive,  # 格式：bool
            self.GDB_MHNegative,  # 格式：bool
            self.GDB_MNegative  # 格式：bool
        ]
        self.DelIsoList = [
            self.deleteBlankResult,  # 删空白的结果（格式：list二维数组，有表头）
            self.GDBResult,  # 数据库生成的结果（格式：list二维数组，有表头）
            self.deleteBlankIntensity,
            self.DelIsoIntensityX,  # 格式：整数
            self.DelIso_13C2RelativeIntensity,  # 格式：整数
            self.DelIsoMassDeviation,  # 格式：浮点数
            self.DelIsoIsotopeMassDeviation,  # 格式：浮点数
            self.DelIsoIsotopeIntensityDeviation  # 格式：整数
        ]
        self.PeakDisList = [
            self.TICDataDictionary,
            self.DelIsoResult,
            self.PeakDisContinuityNum,
            self.PeakDisMassDeviation,
            self.PeakDisDiscontinuityPointNum,
            self.PeakDisClassIsNeed,  # 第二部分
            self.PeakDisClass
        ]
        self.RemoveFPList = [
            self.DelIsoResult,
            self.PeakDisResult,
            self.RemoveFPId,  # 决定选择哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
            self.RemoveFPContinue_CNum,
            self.RemoveFPContinue_DBENum
        ]
        self.PeakDivList = [
            self.RemoveFPId,  # 判断选择了哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
            self.RemoveFPResult[1],  # 去假阳性后的需要峰识别（第二部分）结果，二维列表，无表头
            self.PeakDisResult[2],  # 第三个是txt文件中RT值(从小到大排序)
            self.PeakDivNoiseThreshold,
            self.PeakDivRelIntensity,
            self.PeakDivNeedMerge,  # 该参数决定是否需要将溶剂效应的第一个峰融合到第二个峰
            self.PeakDivNeedGenImage  # 该参数决定是否生成图片信息
        ]
        self.PlotList = [
            self.RemoveFPId,  # 判断选择了哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
            self.RemoveFPResult[0],  # 所有类别去假阳性的结果，二维列表，有表头
            self.PlotTitleName,
            self.PlotTitleColor,
            self.PlotXAxisName,
            self.PlotXAxisColor,
            self.PlotYAxisName,
            self.PlotYAxisColor,
            self.PlotHasEnter,  # 记录是否进入过PlotSetup()函数
            self.PlotType,  # 绘图类型
            self.PlotClassList,  # 列表，需要绘制的类型，例子：["CH", "N1"]
            self.PlotClassItem,  # 列表，需要绘制的类型，例子：["CH"]，对应单选钮，长度必须为1
            self.PlotDBENum,  # 整数，记录用户选择的DBE数目
            self.PlotConfirm
        ]
        self.startModeList = [
            self.startMode,
            self.startModeConfirm
        ]

# 删空白
class ClassDeleteBlank:
    def __init__(self, parameterList, outputFilesPath):
        """
        :param parameterList: 程序运行所需要的参数列表
        """
        assert len(parameterList) == 5, "ClassDeleteBlank参数不对"
        # 样本文件路径
        self.samplePath = parameterList[0]
        # 空白文件路径
        self.blankPath = parameterList[1]
        # 1~9999（整数）
        self.deleteBlankIntensity = parameterList[2]
        # 0.01~99.99（浮点数）
        self.deleteBlankPPM = parameterList[3]
        # 1~100（整数）
        self.deleteBlankPercentage = parameterList[4]
        # 数据预处理
        self.sampleData = pd.read_excel(io=self.samplePath, header=ConstValues.PsHeaderLine)
        self.sampleData.columns = ["Mass", "Intensity"]  # 强制改变列名，方便后面使用
        self.blankData = pd.read_excel(io=self.blankPath, header=ConstValues.PsHeaderLine)
        self.blankData.columns = ["Mass", "Intensity"]  # 强制改变列名，方便后面使用
        # 用户选择的文件的生成位置
        self.outputFilesPath = outputFilesPath

    # 负责扣空白
    def DeleteBlank(self):
        self.DeleteSmallIntensity()
        return self.DeleteSimilarToBlank()

    # 删除Intensity小于self.deleteBlankIntensity的行
    def DeleteSmallIntensity(self):
        # 只保留大于intensity的行
        self.sampleData = self.sampleData[self.sampleData.Intensity > self.deleteBlankIntensity]
        self.blankData = self.blankData[self.blankData.Intensity > self.deleteBlankIntensity]
        if ConstValues.PsIsDebug:
            # 180-onescan-external.xlsx处理后：5888
            # blank-3.xlsx处理后：3778
            print(
                "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                sys._getframe().f_code.co_name, "\" method***：",
                "self.sampleData.shape[0]:", self.sampleData.shape[0], "self.blankData.shape[0]:", self.blankData.shape[0]
            )

    # 删去样本和空白中相同的mass且intensity相近的mass，必须调过DeleteSmallIntensity函数调用此函数才有意义
    def DeleteSimilarToBlank(self):
        """
                    m1:样本中的mass
                    m2:空白中的mass
                    in1:样本中的intensity
                    in2:空白中的intensity
        :param ppm: abs((m1 - m2) * 1000000.0 / m1) < ppm，则认为mass相同，这个ppm需要可以设置，条件1
        :param percentage: 0 < abs((in1 - in2)  * 100.0 / in1) < percentage%，则认为intensity相近，这个percentage也需要可以设置，条件2
        :return: 处理后的数据(格式：list二维数组)
        """
        header = [["Mass", "Intensity"]]
        m1 = self.sampleData["Mass"].values            # 样本中的mass，类型为numpy中的ndarray
        in1 = self.sampleData["Intensity"].values     # 样本中的intensity
        m2 = self.blankData["Mass"].values             # 空白中的mass
        in2 = self.blankData["Intensity"].values      # 空白中的intensity
        result = np.hstack([m1.reshape(-1, 1), in1.reshape(-1, 1)])  # 两个一维数组拼接为二维数组
        if ConstValues.PsIsDebug:
            print(
                "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                sys._getframe().f_code.co_name, "\" method***：",
                "type(result):", type(result), "result[:6, :]:", result[:6, :]
            )

        # 核心处理逻辑
        deleteList = []  # 记录需要删除的索引
        # 要求m1和m2为升序
        i = 0
        j = 0
        while i < m2.size:
            breakFlag = False
            j = 0
            while j < m1.size:
                if abs((m1[j] - m2[i]) * 1000000.0 / m1[j]) < self.deleteBlankPPM:
                    if abs((in1[j] - in2[i]) * 100.0 / in1[j]) < self.deleteBlankPercentage:
                        deleteList.append(j)
                        breakFlag = True
                elif breakFlag or m1[j] > m2[i]:
                    break
                j += 1
            i += 1

        # # 不要求要求m1和m2为有序
        # for i in range(m2.size):
        #     for j in range(m1.size):
        #         if abs((m1[j] - m2[i]) * 1000000.0 / m1[j]) < ppm:
        #             if abs((in1[j] - in2[i]) * 100.0 / in1[j]) * 100 < percentage:
        #                 deleteList.append(j)

        result = np.delete(result, deleteList, axis=0)  # 删除索引在deleteList中的向量
        result = result.tolist()
        result = header + result

        if ConstValues.PsIsDebug:
            print(
                "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                sys._getframe().f_code.co_name, "\" method***：",
                "len(deleteList):", len(deleteList), "len(result):", len(result), "result[:6]:", result[:6]
            )

        # 数据写入excel文件中
        newDirectory = CreateDirectory(self.outputFilesPath, "./intermediateFiles", "/_1_deleteBlank")
        WriteDataToExcel(result, newDirectory + "/" + ConstValues.PsNameDeleteBlank)

        return result, True

# 生成数据库
class ClassGenerateDataBase:
    def __init__(self, parameterList, outputFilesPath):
        assert len(parameterList) == 11, "ClassGenerateDataBase参数不对"
        self.GDBClass = parameterList[0]  # 数据库生成(参数)：Class类型
        # 1~100（整数）
        self.GDBCarbonRangeLow = parameterList[1]  # 数据库生成(参数)：carbon rage(碳数范围)最小值(包含)
        self.GDBCarbonRangeHigh = parameterList[2]  # 数据库生成(参数)：carbon rage(碳数范围)最大值(包含)
        # 1~30（整数）
        self.GDBDBERageLow = parameterList[3]  # 数据库生成(参数)：DBE rage(不饱和度范围)最小值(包含)
        self.GDBDBERageHigh = parameterList[4]  # 数据库生成(参数)：DBE rage(不饱和度范围)最大值(包含)
        # 50~1500(整数)
        self.GDBM_ZRageLow = parameterList[5]  # 数据库生成(参数)：m/z rage(质荷比范围)最小值(包含)
        self.GDBM_ZRageHigh = parameterList[6]  # 数据库生成(参数)：m/z rage(质荷比范围)最大值(包含)
        # 离子类型
        self.GDB_MHPostive = parameterList[7]  # 数据库生成(参数)：正离子，是否选择[M+H]+，True为选中
        self.GDB_MPostive = parameterList[8]  # 数据库生成(参数)：正离子，是否选择M+，True为选中
        self.GDB_MHNegative = parameterList[9]  # 数据库生成(参数)：负离子，是否选择[M-H]-，True为选中
        self.GDB_MNegative = parameterList[10]  # 数据库生成(参数)：负离子，是否选择M-，True为选中
        # 用户选择的文件的生成位置
        self.outputFilesPath = outputFilesPath

    # 负责生成数据库
    def GenerateData(self):
        # excel表头
        header = ["Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]

        # 判断最后一列（ion）应该填入什么
        isPositive = self.GDB_MHPostive or self.GDB_MPostive  # 是否为正离子
        # isChoiceTwo = 0  # 是否勾选了两项
        if isPositive:
            isChoiceTwo = self.GDB_MHPostive + self.GDB_MPostive
        else:
            isChoiceTwo = self.GDB_MHNegative + self.GDB_MNegative

        # 生成数据主逻辑
        if isPositive:
            if isChoiceTwo == 2:  # 说明选择的是两个正离子
                data = self._GenerateData([1, 2])
            elif self.GDB_MHPostive:  # 说明选择的是一个正离子[M＋H]+
                data = self._GenerateData([1])
            else:  # 说明选择的是一个正离子M+
                data = self._GenerateData([2])
        else:
            if isChoiceTwo == 2:  # 说明选择的是两个负离子
                data = self._GenerateData([3, 4])
            elif self.GDB_MHNegative == True:  # 说明选择的是一个负离子[M-H]-
                data = self._GenerateData([3])
            else:  # 说明选择的是一个负离子M-
                data = self._GenerateData([4])

        result = [header]  # 根据m/z筛选符合条件的item
        # result.append(header)
        for item in data:
            if self.GDBM_ZRageLow <= item[3] <= self.GDBM_ZRageHigh:
                result.append(item)

        # 数据写入excel文件中
        newDirectory = CreateDirectory(self.outputFilesPath, "./intermediateFiles", "/_2_generateDataBase")
        WriteDataToExcel(result, newDirectory + "/" + ConstValues.PsNameGDB)

        return result, True

    # 根据类型生成数据
    def _GenerateData(self, typeList):
        data = []
        for Class in self.GDBClass:  # 对每个Class会生成多条NeutralDBE
            # 计算N的数目，为后面排除不符合要求数据使用
            NNumber = 0
            for i in range(len(Class)):
                if Class[i] == "N":
                    NNumber = int(Class[i + 1])
                    break
            for NeutralDBE in range(self.GDBDBERageLow, self.GDBDBERageHigh + 1):  # 对每个NeutralDBE会根据C数不同生成不同的分子式
                for CNumber in range(self.GDBCarbonRangeLow, self.GDBCarbonRangeHigh + 1):  # 每个C数生成一个分子式（可能对应两项数据）
                    if CNumber >= NeutralDBE / 0.9 - NNumber:  # 排除一些不法分子式
                        for i in typeList:
                            item = self.GenerateItem(Class, NeutralDBE, CNumber, i)
                            if item is not None:
                                data.append(item)
        return data

    # 负责生成excel某一行（项）
    def GenerateItem(self, Class, NeutralDBE, CNumber, IonType):
        """
        :param Class: 物质类型，字符串类型，（N1，N1O1，N1S1，O1S1，N2，N1O2，O1，O2，S1，CH），必须保证1个原子也要写上1，除了CH
        :param NeutralDBE: DBE(不饱和度)，整数类型1~30
        :param CNumber: carbon number(碳数目)，整数类型1~100
        :param IonType: (离子类型选项)：包括[M＋H]+和M+和[M-H]-和M-(可选择一个也可以选择两个，只能选相同电荷的)
                        1：代表[M＋H]+
                        2：代表M+
                        3：代表[M-H]-
                        4：代表M-
        :return:
        """
        # 计算各元素的数目
        # O的数目，N的数目，S的数目
        ONumber = 0
        NNumber = 0
        SNumber = 0
        for i in range(len(Class)):
            if Class[i] == "O":
                ONumber = int(Class[i + 1])
            elif Class[i] == "N":
                NNumber = int(Class[i + 1])
            elif Class[i] == "S":
                SNumber = int(Class[i + 1])
        # H的数目，class为Nz（这里z表示氮的个数）DBE为x，碳数为y,则formula为Cy H 2y+z-2x+2 Nz
        HNumber = 2 * CNumber + NNumber - 2 * NeutralDBE + 2

        # H数少于0，可以直接排除
        if HNumber <= 0:
            return None

        # 生成分子式
        formula = "C" + str(CNumber)
        formula = formula + "H" + str(HNumber)
        if Class != "CH":
            formula += Class

        # 根据用户选择计算cal m/z，ion
        calMZ = 0.0
        ion = None
        if IonType == 1:  # 代表[M＋H]+
            calMZ = CNumber * 12.0 + HNumber * 1.007825 \
                    + ONumber * 15.994915 + NNumber * 14.003074 + SNumber * 31.972071 + 1.007277
            ion = "H"
        elif IonType == 2:  # 代表M+
            calMZ = CNumber * 12.0 + HNumber * 1.007825 + \
                    ONumber * 15.994915 + NNumber * 14.003074 + SNumber * 31.972071 + 0.000549
        elif IonType == 3:  # 代表[M-H]-
            calMZ = CNumber * 12.0 + HNumber * 1.007825 + \
                    ONumber * 15.994915 + NNumber * 14.003074 + SNumber * 31.972071 - 1.007276
            ion = "H"
        elif IonType == 4:  # 代表M-
            calMZ = CNumber * 12.0 + HNumber * 1.007825 + \
                    ONumber * 15.994915 + NNumber * 14.003074 + SNumber * 31.972071 - 0.000548
        item = []
        item.append(Class)  # 字符串
        item.append(NeutralDBE)  # 整数
        item.append(formula)  # 字符串
        item.append(calMZ)  # 浮点数
        item.append(CNumber)  # 整数
        if ion != None:
            item.append(ion)  # 字符串

        return item

# 搜同位素
class ClassDeleteIsotope:
    def __init__(self, parameterList, outputFilesPath):
        assert len(parameterList) == 8, "ClassDeleteIsotope参数个数不对"
        self.deleteBlankResult = parameterList[0]  # 删空白的结果（格式：list二维数组，有表头）
        self.GDBResult = parameterList[1]  # 数据库生成的结果（格式：list二维数组，有表头）
        self.deleteBlankIntensity = parameterList[2]  # 格式：整数
        self.DelIsoIntensityX = parameterList[3]  # 格式：整数
        self.DelIso_13C2RelativeIntensity = parameterList[4]  # 格式：整数
        self.DelIsoMassDeviation = parameterList[5]  # 格式：浮点数
        self.DelIsoIsotopeMassDeviation = parameterList[6]  # 格式：浮点数
        self.DelIsoIsotopeIntensityDeviation = parameterList[7]  # 格式：整数
        # 去掉表头
        self.deleteBlankResult = self.deleteBlankResult[1:]
        self.GDBResult = self.GDBResult[1:]
        # 用户选择的文件的生成位置
        self.outputFilesPath = outputFilesPath

    # 负责去同位素
    def DeleteIsotope(self):
        result = []
        header = ["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
        result.append(header)

        for sampleItem in self.deleteBlankResult:
            # sampleItem均为列表，列表：[Mass, Intensity]，都是浮点数
            ret = self.DelIsoHandleItem(sampleItem)
            for item in ret:
                result.append(item)

        # 去同位素按照Formula（主键），C（次主键）从小到大顺序排序
        result = self.DelIsoSort(result)

        # 数据写入excel文件中
        newDirectory = CreateDirectory(self.outputFilesPath, "./intermediateFiles", "/_3_deleteIsotope")
        WriteDataToExcel(result, newDirectory + "/" + ConstValues.PsNameDeleteIsotope)

        return result, True

    # 负责判断某个删空白样本是否能匹配成功 数据库
    def DelIsoHandleItem(self, sampleItem):
        """
        :param sampleItem: 样本(self.deleteBlankResult)中某个样本，是列表：[Mass, Intensity]，都是浮点数
        :return: list二维列表，长度可能为2或3或4，最后一个元素均为[]，目的显示写入文件后容易区分
        """
        sampleItemMass = sampleItem[0]
        sampleItemIntensity = sampleItem[1]
        # 返回结果：list二维数组，数组的长度可能为1或2或3
        ret = []
        for DBItem in self.GDBResult:
            # DatabaseItem均为列表，列表：["Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
            # [str, int, str, float, int, str]
            # DBItemClass = DBItem[0]  # 类型
            # DBItemNDBE = DBItem[1]  # 不饱和度
            # DBItemFormula = DBItem[2]  # 分子式
            DBItemM_Z = DBItem[3]  # 质荷比
            DBItemCNumber = DBItem[4]  # 碳数目

            # 1.sampleItem中Mass与database一个class中的cal m/z是否相同
            if abs((sampleItemMass - DBItemM_Z) * 1000000.0 / DBItemM_Z) > self.DelIsoMassDeviation:
                continue

            # 2.根据cal m/z 对应的碳数，计算“13C1”及其intensity1，计算“13C2”及其intensity2
            DBItem_13C1 = DBItemM_Z + 1.00335
            DBItem_13C1Intensity = 1.081572829 * DBItemCNumber
            DBItem_13C2 = DBItemM_Z + 1.00335 * 2
            DBItem_13C2Intensity = (1.081572829 * DBItemCNumber) ** 2 / 200

            if sampleItemIntensity * DBItem_13C1Intensity / 100.0 < self.deleteBlankIntensity:
                ret.append(sampleItem + DBItem)
                break
            else:
                # 3.sampleItemIntensity>self.DelIsoIntensityX 且 DBItem_13C2Intensity>self.DelIso_13C2RelativeIntensity
                # if (sampleItemIntensity > self.DelIsoIntensityX) and (DBItem_13C2Intensity > self.DelIso_13C2RelativeIntensity):
                # 3.sampleItemIntensity * DBItem_13C2Intensity > self.deleteBlankIntensity
                if sampleItemIntensity * DBItem_13C2Intensity > self.deleteBlankIntensity:
                    # 4.样本(self.deleteBlankResult)中所有mass是否有对应的“13C1”和“13C2”及intensity相近
                    parameterList = [DBItem_13C1, DBItem_13C1Intensity, DBItem_13C2, DBItem_13C2Intensity, sampleItemIntensity]
                    retValue = self.DelIsoHasCorrespondInSample(parameterList)
                    if retValue[0]:
                        ret.append(sampleItem + DBItem)
                        ret.append(retValue[1] + ["iostope"])
                        if len(ret) == 3:
                            ret.append(retValue[2] + ["iostope"])
                        break
                else:
                    # 5.样本中是否有对应的“13C1”及intensity1相近
                    parameterList = [DBItem_13C1, DBItem_13C1Intensity, sampleItemIntensity]
                    retValue = self.DelIsoHasCorrespondInSample(parameterList)
                    if retValue[0]:
                        ret.append(sampleItem + DBItem)
                        ret.append(retValue[1] + ["iostope"])
                        break

        if len(ret) == 0:
            ret.append(sampleItem)
        ret.append([])

        return ret

    # 4.样本(self.deleteBlankResult)中所有mass是否有对应的“13C1”和“13C2”及intensity相近。5.样本中是否有对应的“13C1”及intensity1相近
    def DelIsoHasCorrespondInSample(self, parameterList):
        if len(parameterList) == 5:  # 4.样本(self.deleteBlankResult)中所有mass是否有对应的“13C1”和“13C2”及intensity相近
            # 返回值可能为：[False]，[True, []]，[True, [], []]
            DBItem_13C1 = parameterList[0]
            DBItem_13C1Intensity = parameterList[1]
            DBItem_13C2 = parameterList[2]
            DBItem_13C2Intensity = parameterList[3]
            sampleItemIntensity = parameterList[4]
            ret = []
            for item in self.deleteBlankResult:
                Mass = item[0]
                Intensity = item[1]
                # if (abs((Mass - DBItem_13C1) * 1000000.0 / DBItem_13C1)) <= self.DelIsoIsotopeMassDeviation and \
                #         (abs((Intensity * 100.0 / sampleItemIntensity - DBItem_13C1Intensity) * 100.0 / DBItem_13C1Intensity) < self.DelIsoIsotopeIntensityDeviation):
                if (abs((Mass - DBItem_13C1) * 1000000.0 / DBItem_13C1)) <= self.DelIsoIsotopeMassDeviation and \
                        (abs((Intensity * 100.0 / sampleItemIntensity - DBItem_13C1Intensity)) < self.DelIsoIsotopeIntensityDeviation):
                    ret.append(True)
                    ret.append(item)
                    break
            for item in self.deleteBlankResult:
                Mass = item[0]
                Intensity = item[1]
                # if (abs((Mass - DBItem_13C2) * 1000000.0 / DBItem_13C2)) <= self.DelIsoIsotopeMassDeviation and \
                #         (abs((Intensity * 100.0 / sampleItemIntensity - DBItem_13C2Intensity) * 100.0 / DBItem_13C2Intensity) < self.DelIsoIsotopeIntensityDeviation):
                if (abs((Mass - DBItem_13C2) * 1000000.0 / DBItem_13C2)) <= self.DelIsoIsotopeMassDeviation and \
                        (abs((Intensity * 100.0 / sampleItemIntensity - DBItem_13C2Intensity)) < self.DelIsoIsotopeIntensityDeviation):
                    if len(ret) == 0:
                        ret.append(True)
                    ret.append(item)
                    break
            if len(ret) == 0:
                ret.append(False)
            return ret
        elif len(parameterList) == 3:  # 5.样本中是否有对应的“13C1”及intensity1相近
            # 返回值可能为：[False]，[True, []]
            DBItem_13C1 = parameterList[0]
            DBItem_13C1Intensity = parameterList[1]
            sampleItemIntensity = parameterList[2]
            ret = []
            for item in self.deleteBlankResult:
                Mass = item[0]
                Intensity = item[1]
                # if (abs((Mass - DBItem_13C1) * 1000000.0 / DBItem_13C1)) <= self.DelIsoIsotopeMassDeviation and \
                #         (abs((Intensity * 100.0 / sampleItemIntensity - DBItem_13C1Intensity) * 100.0 / DBItem_13C1Intensity) < self.DelIsoIsotopeIntensityDeviation):
                if (abs((Mass - DBItem_13C1) * 1000000.0 / DBItem_13C1)) <= self.DelIsoIsotopeMassDeviation and \
                        (abs((Intensity * 100.0 / sampleItemIntensity - DBItem_13C1Intensity)) < self.DelIsoIsotopeIntensityDeviation):
                    ret.append(True)
                    ret.append(item)
                    break
            if len(ret) == 0:
                ret.append(False)
            return ret

        # 传入的参数个数错误
        if ConstValues.PsIsDebug:
            print(
                "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                sys._getframe().f_code.co_name, "\" method***：",
                "parameterList参数错误！"
            )

        return False

    # 峰识别按照Formula（主键），C（次主键）从小到大顺序排序
    def DelIsoSort(self, result):
        # self.DelIsoResult种每个元素均为列表，有多种类型：
        # 类型一：["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
        # 类型二：["SampleMass", "SampleIntensity"]
        # 类型三：[DBItem_13C1, DBItem_13C1Intensity, "iostope"] 或者 [DBItem_13C2, DBItem_13C2Intensity, "iostope"]
        # 类型四：[]

        # {key:[ [[...], ..., [...]] , ..., [...]], ..., key:[...]}，[[...], ..., [...]]对应某个分子式，长度为1,2或3
        dataDirectory = {}  # 记录所有符合要求的数据
        # {key:[ [...] , ..., [...] ], ..., key:[ [...] , ..., [...] ]}，[...]对应某个分子式，长度为8
        dataOneDirectory = {}  # 某个分子式对应多条记录，只记录第一条，长度为3，最后一个数据记录其位置

        # 以类别为键，将数据整理为字典
        i = 1  # 跳过表头
        length = len(result)
        while i < length:
            firstItem = result[i]
            if len(firstItem) != 8:
                i += 1
                continue
            # 此时找到第一个符合条件的记录，查找其紧随的下面是否有 类型三
            item = [firstItem]  # 是一个二维列表，对应一种物质
            i += 1
            nextItem = result[i]
            while len(nextItem) != 0:
                item.append(nextItem)
                i += 1
                nextItem = result[i]

            key = firstItem[2]  # "Class"作为键
            if key in dataDirectory.keys():
                dataDirectory[key].append(item)
                dataOneDirectory[key].append([firstItem[3]] + [firstItem[6]] + [len(dataOneDirectory[key])])
            else:
                dataDirectory[key] = [item]
                dataOneDirectory[key] = [[firstItem[3]] + [firstItem[6]] + [0]]
            # 查看下一条数据
            i += 1

        # 对dataOneDirectory中的各项进行排序
        for key in dataOneDirectory.keys():
            dataOneDirectory[key] = sorted(dataOneDirectory[key], key=(lambda x: [x[0], x[1]]), reverse=False)

        # 重新整理结果
        ret = [["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]]
        for key in dataOneDirectory.keys():
            data = dataOneDirectory[key]
            for item1 in data:
                for item2 in dataDirectory[key][item1[2]]:
                    ret.append(item2)
                ret.append([])

        return ret

# 峰识别
class ClassPeakDistinguish:
    def __init__(self, parameterList, outputFilesPath):
        assert len(parameterList) == 7, "ClassPeakDistinguish参数个数不对!"
        # self.TICData是读入后并处理后的数据, 为字典：{key: value}，value为二维列表[[Mass, Intensity], ..., [Mass, Intensity]]
        self.TICData = parameterList[0]  # 总离子流图路径（第一阶段）
        self.DelIsoResult = parameterList[1]  # 扣同位素后生成的文件，两项记录之间通过空列表分割（格式：list二维数组，有表头）
        self.PeakDisContinuityNum = parameterList[2]  # 连续出现的扫描点个数，格式：整数
        self.PeakDisMassDeviation = parameterList[3]  # 质量偏差，格式：浮点数
        self.PeakDisDiscontinuityPointNum = parameterList[4]
        self.PeakDisClassIsNeed = parameterList[5]  # 第二部分，峰检测分割
        self.PeakDisClass = parameterList[6]
        # 第一部分结果
        self.resultPart1 = None
        self.resultPart1Detail = None
        # 用户选择的文件的生成位置
        self.outputFilesPath = outputFilesPath

    # 负责峰识别
    def PeakDistinguish(self):
        # 获取排序后的RT，后面峰检测需要使用
        sortedRTValue = sorted([float(num) for num in list(self.TICData)])
        newDirectory = CreateDirectory(self.outputFilesPath, "./intermediateFiles", "/_4_peakDistinguish")
        WriteDataToExcel([sortedRTValue], newDirectory + "/sortedRTValue.xlsx")  # 只有一行，没有表头，峰检测（第二部分）需要
        # 去掉表头
        self.DelIsoResult = self.DelIsoResult[1:]
        # 说明读取的文件存在问题
        if self.TICData is None:
            return [], False
        self.resultPart1 = []  # 第一部分，识别连续的扫描点
        headerPart1 = ["SampleMass", "Area", "startRT", "startRTValue", "endRT", "endRTValue", "TICMassMedian", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
        self.resultPart1.append(headerPart1)
        # 存储第一阶段的详细信息，为第二阶段做准备，三维列表[[a, ..., b], ...]
        # self.resultPart1Detail[0]代表某个去同位素后的样本在TIC中的所有数据（如果连续或没匹配上为0）。
        # self.resultPart1Detail[0]前面部分为该样本的信息，字段和  类型一 一样
        # self.resultPart1Detail中所有的数据都是是用户输入的需要进行峰检测（第二部分）的类别
        self.resultPart1Detail = []
        flag = 1

        for sampleItem in self.DelIsoResult:
            # sampleItem均为列表，有多种类型：
            # 类型一：["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
            # 类型二：["SampleMass", "SampleIntensity"]
            # 类型三：[DBItem_13C1, DBItem_13C1Intensity, "iostope"]或者[DBItem_13C2, DBItem_13C2Intensity, "iostope"]
            # 类型四：[]
            if len(sampleItem) == 8:
                ret, retDetail = self.PeakDisHandleItem(sampleItem)
                for item in ret:
                    self.resultPart1.append(item)
                if len(retDetail) != 0:
                    if flag == 1 and ConstValues.PsIsDebug:
                        print(
                            "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                            sys._getframe().f_code.co_name, "\" method***：",
                            "len(retDetail):", len(retDetail)
                        )
                        flag = 0
                    self.resultPart1Detail.append(sampleItem + [":"] + retDetail)

        # 峰识别按照Formula（主键），C（次主键）从小到大顺序排序
        self.resultPart1 = self.PeakDisSort()
        self.resultPart1Detail = self.PeakDisSortDetail()

        # 数据写入excel文件中
        WriteDataToExcel(self.resultPart1, newDirectory + "/" + ConstValues.PsNamePeakDistinguish)
        WriteDataToExcel(self.resultPart1Detail, newDirectory + "/PeakDisPart1DetailPlot.xlsx")

        # # 为了录屏演示用，直接从文件读取
        # self.resultPart1 = ReadExcelToList("./intermediateFiles/_4_peakDistinguish/" + ConstValues.PsNamePeakDistinguish)
        # self.resultPart1Detail = ReadExcelToList("./intermediateFiles/_4_peakDistinguish/PeakDisPart1DetailPlot.xlsx", hasNan=False)
        # sortedRTValue = ReadExcelToList("./intermediateFiles/_4_peakDistinguish/sortedRTValue.xlsx", hasNan=False)[0]

        return [self.resultPart1, self.resultPart1Detail, sortedRTValue], True

    # 负责判断某个扣同位素后的样本是否能成功在总离子流图文件(txt)查到符合条件的记录集合
    def PeakDisHandleItem(self, sampleItem):
        # 获取样本中的Mass（Mass0）
        sampleMass = sampleItem[0]
        # # 获取样本的类型，判断是否需要进行第二部分
        needDetectPeak = False
        if (sampleItem[2] in self.PeakDisClass) and self.PeakDisClassIsNeed:
            needDetectPeak = True
        # 获取字典的长度
        scanNum = len(self.TICData)
        # 将字典的键转化为列表
        keysList = list(self.TICData)
        ret = []
        retDetail = []  # 第二部分信息

        k = 0
        while k < scanNum:
            firstRT = None
            continuityItems = []  # 存储连续的符合要求的记录，为二维列表[[Mass, Intensity],...,[Mass, Intensity]]
            continuityItems2 = []
            while k < scanNum and firstRT is None:
                firstRT = self.PeakDisHasCorrespondInTIC(keysList, sampleMass, k)
                if needDetectPeak:
                    if (firstRT is None) or (k == scanNum - 1):
                        retDetail.append(0)
                    else:
                        retDetail.append(firstRT[1])
                k += 1
            if k >= scanNum:
                break
            # 此时保证在self.TICData找到第一个符合要求的记录
            startRT = k - 1
            continuityItems.append(firstRT)  # 不严格连续，同时不连续的条目记为[0,0]
            continuityItems2.append(firstRT)  # 不严格连续，不记录不连续的条目，为了计算中位数
            # 寻找连续的符合要求的记录
            DiscontinuityPointNum = 0
            nextRT = self.PeakDisHasCorrespondInTIC(keysList, sampleMass, k)
            if nextRT is None:
                DiscontinuityPointNum += 1
            while k < scanNum and ((nextRT is not None) or DiscontinuityPointNum < self.PeakDisDiscontinuityPointNum):
                if nextRT is None:
                    DiscontinuityPointNum += 1
                    continuityItems.append([0, 0])
                    if needDetectPeak:
                        retDetail.append(0)
                else:
                    DiscontinuityPointNum = 0
                    continuityItems.append(nextRT)
                    continuityItems2.append(nextRT)
                    if needDetectPeak:
                        retDetail.append(nextRT[1])
                k += 1
                if k >= scanNum:
                    break
                nextRT = self.PeakDisHasCorrespondInTIC(keysList, sampleMass, k)
            if needDetectPeak and k < scanNum:  # 因为跳出上面的循环说明此时nextRT不符合要求
                retDetail.append(0)
            # 到这里连续的记录已经结束
            if len(continuityItems) >= self.PeakDisContinuityNum:  # 说明连续的扫描点数目符合要求
                continuityItems = np.array(continuityItems)
                continuityItems2 = np.array(continuityItems2)
                continuityMasses2 = continuityItems2[:, 0]
                continuityIntensities = continuityItems[:, 1]

                Area = np.sum(continuityIntensities)  # 求面积
                startRTValue = keysList[startRT]  # 开始的扫描点的值
                endRT = startRT + len(continuityItems) - 1  # 结束的扫描点在TIC中属于第几个扫描点
                endRTValue = keysList[endRT]  # 结束的扫描点的值

                # 计算中位数：应该是先计算最大值，然后各个intensity／最大值，选取大于60的 m/z，取中位数
                thresholdValue = np.max(continuityMasses2) * 0.6
                greaterThanThresholdList = []
                for value in continuityMasses2:
                    if value > thresholdValue:
                        greaterThanThresholdList.append(value)
                MassMedian = -1  # 代表不存在这样的中位数，理论上一定存在
                if len(greaterThanThresholdList) > 0:
                    MassMedian = np.median(np.array(greaterThanThresholdList))  # TIC中所有符合条件的连续的记录的

                ret.append([sampleMass, Area, startRT, startRTValue, endRT, endRTValue, MassMedian] + sampleItem[2:])
            elif needDetectPeak:  # 需要将连续的但扫描点数目不符合要求的数据值清零
                length1 = len(retDetail)
                length2 = len(continuityItems)
                if k < scanNum:  # 说明还没到最后，但是连续的扫描点数目不符合要求
                    for i in range(length1 - length2 - 1, length1 - 1):
                        retDetail[i] = 0
                else:  # 说明最后的数据都符合要求，但是连续的扫描点数目不符合要求
                    for i in range(length1 - length2, length1):
                        retDetail[i] = 0
            # 本次连续的考察完毕，进行之后没有考虑的扫描点考察
            k += 1
        if len(ret) != 0:
            ret.append([])
        return ret, retDetail

    # 搜索RTk中是否存在和sampleMass相近的记录
    def PeakDisHasCorrespondInTIC(self, keysList, sampleMass, k):
        value = self.TICData[keysList[k]]  # value为二维列表[[Mass, Intensity],...,[Mass, Intensity]]
        for item in value:
            TICMass = item[0]
            # TICIntensity = item[1]
            if abs((TICMass - sampleMass) * 1000000.0 / sampleMass) < self.PeakDisMassDeviation:
                return item
        return None

    # 峰识别按照Formula（主键），C（次主键）从小到大顺序排序
    def PeakDisSort(self):
        # self.PeakDisResult
        # ["SampleMass", "Area", "startRT", "startRTValue", "endRT", "endRTValue", "TICMassMedian", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
        # {key:[ [...], ..., [...]] , ..., [[...], ..., [...]]], ..., key:[...]}，[[...], ..., [...]]对应某个分子式，[...]长度为13
        dataDirectory = {}  # 记录所有符合要求的数据
        # {key:[ [...] , ..., [...] ], ..., key:[ [...] , ..., [...] ]}，[...]对应某个分子式，长度为8
        dataOneDirectory = {}  # 某个分子式对应多条记录，只记录第一条，长度为3，最后一个数据记录其位置

        # 以类别为键，将数据整理为字典
        i = 1  # 跳过表头
        length = len(self.resultPart1)
        while i < length:
            firstItem = self.resultPart1[i]
            item = [firstItem]  # 是一个二维列表，对应一种物质
            i += 1
            if i < length:
                nextItem = self.resultPart1[i]
                while len(nextItem) != 0:
                    item.append(nextItem)
                    i += 1
                    if i >= length:
                        break
                    nextItem = self.resultPart1[i]

            key = firstItem[7]  # "Class"作为键
            if key in dataDirectory.keys():
                dataDirectory[key].append(item)
                dataOneDirectory[key].append([firstItem[8]] + [firstItem[11]] + [len(dataOneDirectory[key])])
            else:
                dataDirectory[key] = [item]
                dataOneDirectory[key] = [[firstItem[8]] + [firstItem[11]] + [0]]
            # 查看下一条数据
            i += 1

        # 对dataOneDirectory中的各项进行排序
        for key in dataOneDirectory.keys():
            dataOneDirectory[key] = sorted(dataOneDirectory[key], key=(lambda x: [x[0], x[1]]), reverse=False)

        # 重新整理结果
        ret = [["SampleMass", "Area", "startRT", "startRTValue", "endRT", "endRTValue", "TICMassMedian", "Class",
                "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]]
        for key in dataOneDirectory.keys():
            data = dataOneDirectory[key]
            for item1 in data:
                for item2 in dataDirectory[key][item1[2]]:
                    ret.append(item2)
                ret.append([])
        return ret

    # 峰识别按照Formula（主键），C（次主键）从小到大顺序排序
    def PeakDisSortDetail(self):
        # self.PeakDisResult
        # ["SampleMass", "Area", "startRT", "startRTValue", "endRT", "endRTValue", "TICMassMedian", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
        # {key:[ [...], ..., [...]] , ..., [[...], ..., [...]]], ..., key:[...]}，[[...], ..., [...]]对应某个分子式，[...]长度为13
        dataDirectory = {}  # 记录所有符合要求的数据
        # {key:[ [...] , ..., [...] ], ..., key:[ [...] , ..., [...] ]}，[...]对应某个分子式，长度为8
        dataOneDirectory = {}  # 某个分子式对应多条记录，只记录第一条，长度为3，最后一个数据记录其位置

        # 以类别为键，将数据整理为字典
        i = 1  # 跳过表头
        length = len(self.resultPart1Detail)
        while i < length:
            firstItem = self.resultPart1Detail[i]
            item = [firstItem]  # 是一个二维列表，对应一种物质
            i += 1
            if i < length:
                nextItem = self.resultPart1Detail[i]
                while len(nextItem) != 0:
                    item.append(nextItem)
                    i += 1
                    if i >= length:
                        break
                    nextItem = self.resultPart1Detail[i]

            key = firstItem[7]  # "Class"作为键
            if key in dataDirectory.keys():
                dataDirectory[key].append(item)
                dataOneDirectory[key].append([firstItem[3]] + [firstItem[6]] + [len(dataOneDirectory[key])])
            else:
                dataDirectory[key] = [item]
                dataOneDirectory[key] = [[firstItem[3]] + [firstItem[6]] + [0]]
            # 查看下一条数据
            i += 1

        # 对dataOneDirectory中的各项进行排序
        for key in dataOneDirectory.keys():
            dataOneDirectory[key] = sorted(dataOneDirectory[key], key=(lambda x: [x[0], x[1]]), reverse=False)

        # 重新整理结果
        ret = []
        # ret = [["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]]
        for key in dataOneDirectory.keys():
            data = dataOneDirectory[key]
            for item1 in data:
                for item2 in dataDirectory[key][item1[2]]:
                    ret.append(item2)
        return ret

# 去假阳性
class ClassRemoveFalsePositive:
    def __init__(self, parameterList, outputFilesPath):
        assert len(parameterList) == 5, "ClassRemoveFalsePositive参数个数不对!"
        self.DelIsoResult = parameterList[0]  # 扣同位素后生成的文件，两项记录之间通过空列表分割（格式：list二维数组，有表头）

        peakDisResult = parameterList[1]
        # 结果是一个列表，有三个元素，
        # 第一个是峰识别的结果（格式：list二维数组，有表头）
        # 第二个是需要需要峰检测（第二部分）的详细数据，二维列表，无表头
        # 第三个是txt文件中RT值(从小到大排序)
        self.PeakDisResult = peakDisResult[0]  # 峰识别第一阶段后生成的文件，两项记录之间通过空列表分割（格式：list二维数组，有表头）
        self.PeakDisResultDetail = peakDisResult[1]

        self.RemoveFPId = parameterList[2]  # 1：去同位素之后的内容self.DelIsoResult 2：峰识别之后的内容self.DelIsoResult
        self.RemoveFPContinue_CNum = parameterList[3]
        self.RemoveFPContinue_DBENum = parameterList[4]
        # 用户选择的文件的生成位置
        self.outputFilesPath = outputFilesPath

        if ConstValues.PsIsSingleRun:
            filePath = "./intermediateFiles/_4_peakDistinguish/" + ConstValues.PsNamePeakDistinguish
            self.PeakDisResult = ReadExcelToList(filepath=filePath, hasNan=True)
            filePath = "./intermediateFiles/_4_peakDistinguish/PeakDisPart1DetailPlot.xlsx"
            self.PeakDisResultDetail = ReadExcelToList(filepath=filePath, hasNan=False)

    def RemoveFalsePositive(self):
        result = []
        # 创建文件夹
        newDirectory = CreateDirectory(self.outputFilesPath, "./intermediateFiles", "/_5_removeFalsePositive")
        # 运行主逻辑
        if self.RemoveFPId == 1:
            result = self.RemoveFPFromDelIso()
            WriteDataToExcel(result, newDirectory + "/" + ConstValues.PsNameRemoveFPFrom_DelIsoResult)
        elif self.RemoveFPId == 2:
            result = self.RemoveFPFromPeakDis()
            WriteDataToExcel(result, newDirectory + "/" + ConstValues.PsNameRemoveFPFrom_PeakDisResult)

        # 去假阳性后峰识别的峰
        newData = []
        if self.RemoveFPId == 2:
            newData = self.RemoveFPFromPeakDisPlot(result)  # 从读取PeakDisPart1DetailPlot.xlsx去假阳性后生成newData
            WriteDataToExcel(newData, newDirectory + "/PeakDisPart1DetailPlotAfterRFP.xlsx")
            # self.PlotAfterRemoveFP(newData)

        return [result, newData], True

    # 从去同位素后的文件里去假阳性
    def RemoveFPFromDelIso(self):
        # self.DelIsoResult种每个元素均为列表，有多种类型：
        # 类型一：["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
        # 类型二：["SampleMass", "SampleIntensity"]
        # 类型三：[DBItem_13C1, DBItem_13C1Intensity, "iostope"] 或者 [DBItem_13C2, DBItem_13C2Intensity, "iostope"]
        # 类型四：[]

        # {key:[ [[...], ..., [...]] , ..., [...]], ..., key:[...]}，[[...], ..., [...]]对应某个分子式，长度为1,2或3
        dataDirectory = {}  # 记录所有符合要求的数据
        # {key:[ [...] , ..., [...] ], ..., key:[ [...] , ..., [...] ]}，[...]对应某个分子式，长度为8
        dataOneDirectory = {}  # 某个分子式对应多条记录，只记录第一条，长度为3，最后一个数据记录其位置

        # 以类别为键，将数据整理为字典
        i = 1  # 跳过表头
        length = len(self.DelIsoResult)
        while i < length:
            firstItem = self.DelIsoResult[i]
            if len(firstItem) != 8:
                i += 1
                continue
            # 此时找到第一个符合条件的记录，查找其紧随的下面是否有 类型三
            item = [firstItem]  # 是一个二维列表，对应一种物质
            i += 1
            if i < length:
                nextItem = self.DelIsoResult[i]
                while len(nextItem) != 0:
                    item.append(nextItem)
                    i += 1
                    if i >= length:
                        break
                    nextItem = self.DelIsoResult[i]

            key = firstItem[2]  # "Class"作为键
            if key in dataDirectory.keys():
                dataDirectory[key].append(item)
                dataOneDirectory[key].append([firstItem[3]] + [firstItem[6]] + [len(dataOneDirectory[key])])
            else:
                dataDirectory[key] = [item]
                dataOneDirectory[key] = [[firstItem[3]] + [firstItem[6]] + [0]]
            # 查看下一条数据
            i += 1

        # # 对dataOneDirectory中的各项进行排序，因为修改去同位素的生成文件的顺序，所以这里不需要再次排序
        # for key in dataOneDirectory.keys():
        #     dataOneDirectory[key] = sorted(dataOneDirectory[key], key=(lambda x: [x[0], x[1]]), reverse=False)

        # 删除不符合的数据
        afterDel_DBEDirectory = self.RemoveFPHandleContinue(dataOneDirectory)

        # 重新整理结果
        ret = [["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]]
        for key in afterDel_DBEDirectory.keys():
            data = afterDel_DBEDirectory[key]
            for item1 in data:
                for item2 in dataDirectory[key][item1[2]]:
                    ret.append(item2)
                ret.append([])

        return ret

    # 从峰识别第一阶段后的文件里去假阳性
    def RemoveFPFromPeakDis(self):
        # self.PeakDisResult
        # ["SampleMass", "Area", "startRT", "startRTValue", "endRT", "endRTValue", "TICMassMedian", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
        # {key:[ [...], ..., [...]] , ..., [[...], ..., [...]]], ..., key:[...]}，[[...], ..., [...]]对应某个分子式，[...]长度为13
        dataDirectory = {}  # 记录所有符合要求的数据
        # {key:[ [...] , ..., [...] ], ..., key:[ [...] , ..., [...] ]}，[...]对应某个分子式，长度为8
        dataOneDirectory = {}  # 某个分子式对应多条记录，只记录第一条，长度为3，最后一个数据记录其位置

        # 以类别为键，将数据整理为字典
        i = 1  # 跳过表头
        length = len(self.PeakDisResult)
        while i < length:
            firstItem = self.PeakDisResult[i]
            item = [firstItem]  # 是一个二维列表，对应一种物质
            i += 1
            if i < length:
                nextItem = self.PeakDisResult[i]
                while len(nextItem) != 0:
                    item.append(nextItem)
                    i += 1
                    if i >= length:
                        break
                    nextItem = self.PeakDisResult[i]

            key = firstItem[7]  # "Class"作为键
            if key in dataDirectory.keys():
                dataDirectory[key].append(item)
                dataOneDirectory[key].append([firstItem[8]] + [firstItem[11]] + [len(dataOneDirectory[key])])
            else:
                dataDirectory[key] = [item]
                dataOneDirectory[key] = [[firstItem[8]] + [firstItem[11]] + [0]]
            # 查看下一条数据
            i += 1

        # 对dataOneDirectory中的各项进行排序
        for key in dataOneDirectory.keys():
            dataOneDirectory[key] = sorted(dataOneDirectory[key], key=(lambda x: [x[0], x[1]]), reverse=False)

        # 删除不符合的数据
        afterDel_DBEDirectory = self.RemoveFPHandleContinue(dataOneDirectory)

        # 重新整理结果
        ret = [["SampleMass", "Area", "startRT", "startRTValue", "endRT", "endRTValue", "TICMassMedian", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]]
        for key in afterDel_DBEDirectory.keys():
            data = afterDel_DBEDirectory[key]
            for item1 in data:
                for item2 in dataDirectory[key][item1[2]]:
                    ret.append(item2)
                ret.append([])

        return ret

    # 过滤不符合条件的条目的主逻辑
    def RemoveFPHandleContinue(self, dataOneDirectory):
        """
        :param dataOneDirectory: 是一个字典，类型是键，值是二维列表[[...], ... , [...]]，[...]只有三个数据：DBE,C,在dataDirectory中的index
        :return: 过滤掉不符合条件后的dataOneDirectory，格式一样
        """
        # 记录需要删除的数据，首先删除C数不符合要求的
        afterDel_CDirectory = {}  # 记录C数目>=self.RemoveFPContinue_CNum的数据
        for key in dataOneDirectory.keys():  # 针对每一个类别进行下面的过程
            data = dataOneDirectory[key]  # 获取二维有序列表,data[0]是Neutral DBE，data[1]是C数
            i = 0
            dataLength = len(data)
            while i < dataLength - 1:
                firstDBE = data[i]
                everyDBEList = [firstDBE]  # 每个类别有多个不同的DBE，记录某一个DBE所对应的记录
                i += 1
                while data[i][0] == firstDBE[0]:  # Neutral DBE相同
                    everyDBEList.append(data[i])
                    i += 1
                    if i >= dataLength:
                        break
                # 或取到某一个DBE所对应的记录
                everyDBEListLength = len(everyDBEList)
                if everyDBEListLength < self.RemoveFPContinue_CNum:  # 长度不足，直接舍去
                    continue
                # 此时长度符合要求，考察是否连续
                j = 0
                while j < everyDBEListLength - 1:  # 考虑一个DBE
                    nowDBE = everyDBEList[j]
                    continueDBEList = [nowDBE]  # 二维列表
                    nextDBE = everyDBEList[j + 1]
                    j += 1
                    while nowDBE[1] + 1 == nextDBE[1]:  # 考虑连续的DBE，一个DBE可能有多个连续的
                        continueDBEList.append(nextDBE)
                        nowDBE = nextDBE  # 更新当前DBE
                        j += 1
                        if j >= len(everyDBEList):
                            break
                        nextDBE = everyDBEList[j]  # 获取下一个DBE
                    if len(continueDBEList) >= self.RemoveFPContinue_CNum:  # 找到符合要求的数据
                        if key in afterDel_CDirectory.keys():
                            for k in range(len(continueDBEList)):
                                afterDel_CDirectory[key].append(continueDBEList[k])
                        else:
                            afterDel_CDirectory[key] = continueDBEList

        # 记录需要删除的数据，之后删除DBE数不符合要求的
        afterDel_DBEDirectory = {}  # 记录DBE数目>=self.RemoveFPContinue_DBENum的数据
        for key in afterDel_CDirectory.keys():  # 针对每一个类别进行下面的过程
            data = afterDel_CDirectory[key]  # 获取二维有序列表,data[0]是Neutral DBE，data[1]是C数
            i = 0
            dataLength = len(data)
            while i < dataLength - 1:
                first = data[i]
                continueList = [first]
                continueNum = 1
                next = data[i + 1]
                i += 1
                # 寻找相等的条目
                while first[0] == next[0]:
                    continueList.append(next)
                    i += 1
                    if i >= dataLength:
                        break
                    first = next
                    next = data[i]
                # 寻找连续的条目
                if i < dataLength:
                    while (first[0] + 1 == next[0]) or (first[0] == next[0]):
                        continueList.append(next)
                        i += 1
                        if i >= dataLength:
                            break
                        if first[0] + 1 == next[0]:
                            continueNum += 1
                        first = next
                        next = data[i]
                if continueNum >= self.RemoveFPContinue_DBENum:
                    if key in afterDel_DBEDirectory.keys():
                        for k in range(len(continueList)):
                            afterDel_DBEDirectory[key].append(continueList[k])
                    else:
                        afterDel_DBEDirectory[key] = continueList

        return afterDel_DBEDirectory

    # 读取PeakDisPart1DetailPlot.xlsx文件的内容，并进行去假阳性
    def RemoveFPFromPeakDisPlot(self, result):
        # ["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
        if ConstValues.PsIsSingleRun:
            self.PeakDisResultDetail = ReadExcelToList(filepath="./intermediateFiles/_4_peakDistinguish/PeakDisPart1DetailPlot.xlsx", hasNan=False)
        massSet = set()
        newData = []  # 存储需要画出图形的经过去假阳性后的数据
        for item in result:
            if len(item) != 0:
                massSet.add(item[0])
        for item in self.PeakDisResultDetail:
            if item[0] in massSet:
                newData.append(item)
        return newData

    # 过滤峰识别第一阶段生成的PeakDistinguishPart1Detail.xlsx文件，并绘制图形
    def PlotAfterRemoveFP(self, data):
        lengthList = [i for i in range(len(data[0][9:]))]
        # 创建对应的文件夹
        CreateDirectory(self.outputFilesPath, "./intermediateFiles", "/_5_removeFalsePositive/peakImagesAfterRemoveFP")
        for i in range(len(data)):
            item = data[i]
            Class = item[2]  # 化合物类型
            DBE = item[3]  # 不饱和度数目
            plt.xlabel('RT', fontproperties='SimHei', fontsize=15, color='blue')
            plt.ylabel('Intensity', fontproperties='SimHei', fontsize=15, color='blue')
            plt.title("Mass:" + str(item[0]) + "  DBE:" + str(DBE) + "  formula:" + item[4], fontproperties='SimHei', fontsize=12, color='red')
            plt.vlines(x=lengthList, ymin=0, ymax=item[9:])
            newDirectory = CreateDirectory(self.outputFilesPath,
                                           "./intermediateFiles",
                                           "/_5_removeFalsePositive/peakImagesAfterRemoveFP/"+Class+"_DBE"+str(DBE)
                                           )
            plt.savefig(fname=newDirectory+"/"+Class+"_DBE"+str(DBE)+"_C"+str(item[6]), dpi=300)
            plt.close()

# 峰检测
class ClassPeakDivision:
    def __init__(self, parameterList, outputFilesPath):
        assert len(parameterList) == 7, "ClassPeakDivision参数个数不对!"
        self.RemoveFPId = parameterList[0]  # 判断选择了哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
        self.RemoveFPPlotResult = parameterList[1]  # 去假阳性后的需要峰识别（第二部分）结果，二维列表，无表头
        self.sortedRTValue = parameterList[2]  # 第三个是txt文件中RT值(从小到大排序)

        self.PeakDivNoiseThreshold = parameterList[3]
        self.PeakDivRelIntensity = parameterList[4]
        self.PeakDivNeedMerge = parameterList[5]  # 该参数决定是否需要将溶剂效应的第一个峰融合到第二个峰
        self.PeakDivNeedGenImage = parameterList[6]  # 该参数决定是否生成图片信息
        # 用户选择的文件的生成位置
        self.outputFilesPath = outputFilesPath
        if ConstValues.PsIsSingleRun:
            filePath = "./intermediateFiles/_5_removeFalsePositive/PeakDisPart1DetailPlotAfterRFP.xlsx"
            self.RemoveFPPlotResult = ReadExcelToList(filepath=filePath, hasNan=False)
            filePath = "./intermediateFiles/_4_peakDistinguish/sortedRTValue.xlsx"
            self.sortedRTValue = ReadExcelToList(filepath=filePath, hasNan=False)[0]

    # 第二部分，峰检测分割  ######################################################################
    def PeakDivision(self):
        resultPart2 = []  # 第二部分，峰检测与分割，即将多个峰分开输出
        headerPart2 = ["SampleMass", "Area", "PeakRTIndex", "PeakRT", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion", "orderOfMagnitude"]
        resultPart2.append(headerPart2)
        # 峰检测预处理
        ret1DetailPreprocessing = self.PeakDivPreprocessing()
        # 统计连续区间的个数
        ret1DetailContinueList = self.PeakDivSeekContinue(ret1DetailPreprocessing)
        # 为生成图片准备数据
        parametersList = self.PeakDivPrepareParams(ret1DetailPreprocessing, ret1DetailContinueList)
        # 生成图片，同时生成结果
        for parameters in parametersList:
            ret = self.PlotAfterRemoveFP(parameters)  # 返回结果为二维列表
            for item in ret:
                resultPart2.append(item)
        # 数据写入文件
        newDirectory = CreateDirectory(self.outputFilesPath, "./intermediateFiles", "/_6_peakDivision")
        WriteDataToExcel(ret1DetailPreprocessing, newDirectory + "/ret1DetailPreprocessing.xlsx")
        WriteDataToExcel(resultPart2, newDirectory + "/" + ConstValues.PsNamePeakDivision)

        return resultPart2, True

    # 峰检测预处理
    def PeakDivPreprocessing(self):
        # 返回结果：二维列表，和self.RemoveFPPlotResult格式完全一致

        # 预处理，删除一些干扰值，具体包括：
        # 1.设置噪音阈值: 500000，小于这个强度的都删除，这样应该删除一部分强度低，峰形不好的图像
        # 2.设置一个相对强度阈值：0.1%，这个和你之前的想法一样，就是删去每张图中，相对强度小于最高峰的0.1%的那些信号
        # TODO: 3.设置一个最小峰宽? 至少现在没有这一步

        # 二维列表，物质相关信息，后续拼接使用
        rawInformation = [[num for num in self.RemoveFPPlotResult[i][:9]] for i in range(len(self.RemoveFPPlotResult))]
        # 二维列表，峰识别第一阶段生成的需要进行第二阶段的数据，无表头，非数据项全部移除
        rawData = np.array([[num for num in self.RemoveFPPlotResult[i][9:]] for i in range(len(self.RemoveFPPlotResult))])
        rawData[rawData < self.PeakDivNoiseThreshold] = 0  # 第1步
        for i in range(len(rawData)):
            RelativeThreshold = np.max(rawData[i]) * self.PeakDivRelIntensity / 100.0  # 第2步
            rawData[i][rawData[i] < RelativeThreshold] = 0

        rawData = rawData.tolist()
        # 二维列表，最终结果
        ret1DetailPreprocessing = [rawInformation[i] + rawData[i] for i in range(len(rawInformation))]

        return ret1DetailPreprocessing

    # dataProcessing中所有行查到符合条件的记录集合
    def PeakDivSeekContinue(self, dataProcessing):
        """
        :param dataProcessing: 格式二维列表，
                    每一行["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion",....]
        :return: 三维列表，[[[...], ..., [..]], ..., [[...], ..., [..]]]
                    [[...], ..., [..]]代表dataProcessing每一行处理的结果
        """
        ret = []
        for item in dataProcessing:
            ret.append(self.PeakDivSeekContinueItem(item))
        return ret

    # dataProcessing中某一行查到符合连续条件（这里的连续是中间没有超过5个为0的点）的记录集合
    def PeakDivSeekContinueItem(self, item):
        # 返回内容格式：
        # 三维列表，[[[...], ..., [..]], ..., [[...], ..., [..]]]
        # [[...], ..., [..]]代表dataProcessing每一行处理的结果
        # 获取需要处理的数据
        itemData = item[9:]
        # 获取扫描点数目
        scanNum = len(itemData)
        # TODO:参数
        PeakDisDiscontinuityPointNum = 5

        ret = [item[:9]]  # ContinueList
        k = 0
        while k < scanNum:
            firstRT = 0
            continuityIntensities = []  # 存储连续的符合要求的记录，为列表[Intensity, ..., Intensity]
            while k < scanNum and firstRT == 0:
                firstRT = itemData[k]
                k += 1
            if k >= scanNum:
                break
            # 此时保证在itemData找到第一个不为0记录
            startRT = k - 1
            continuityIntensities.append(firstRT)  # 不严格连续

            # 寻找连续的符合要求的记录
            DiscontinuityPointNum = 0
            nextRT = itemData[k]
            if nextRT == 0:
                DiscontinuityPointNum += 1
            while k < scanNum and ((nextRT != 0) or DiscontinuityPointNum < PeakDisDiscontinuityPointNum):
                continuityIntensities.append(nextRT)
                if nextRT == 0:
                    DiscontinuityPointNum += 1
                else:
                    DiscontinuityPointNum = 0
                k += 1
                if k >= scanNum:
                    break
            # 到这里连续的记录已经结束
            continuityIntensities = np.array(continuityIntensities)
            Area = np.sum(continuityIntensities)  # 求面积
            endRT = startRT + len(continuityIntensities) - 1  # 结束的扫描点在TIC中属于第几个扫描点
            ret.append([startRT, endRT, Area])  # ContinueList

            # 本次连续的考察完毕，进行之后没有考虑的扫描点考察
            k += 1
        return ret

    # 为绘制峰准备数据
    def PeakDivPrepareParams(self, dataProcessing, ContinueList):
        """
        :param dataProcessing: 峰检测预处理后的数据
                每一行["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion",....]
        :param ContinueList: 数据的连续信息，[[[...], ..., [..]], ..., [[...], ..., [..]]]
                [[...], ..., [..]]代表dataProcessing每一行处理的结果
        :return: 返回一个二维列表[[..], ... , [...]]，[..]对应每个图片的参数信息
        """
        assert len(dataProcessing) == len(ContinueList), "Error1 in PeakDivPrepareParams!"
        assert len(dataProcessing[0][9:]) == len(self.sortedRTValue), "Error2 in PeakDivPrepareParams!"
        rawData = np.array([[num for num in dataProcessing[i][9:]] for i in range(len(self.RemoveFPPlotResult))])
        # 存储每行的最大值
        maxValueList = [np.max(item) for item in rawData]
        # 存储每个数据的数量级（数字），例如：10000
        orderValueList = [10 ** int(math.log10(maxValue+1)) for maxValue in maxValueList]  # +1是为了防止maxValue=0
        # 存储每个数据的数量级（字符串），例如：1e4
        orderStrList = ["1e" + str(int(math.log10(maxValue+1))) for maxValue in maxValueList]

        # 拟合数据
        smoothData = []  # 平滑后的数据，每一项均为numpy类型数据
        for item in dataProcessing:
            # # 拟合滤波算法
            # smoothData.append(self.FilterPoly(item[9:]))

            # 普通滤波算法
            smoothData.append(self.Filter(item[9:], "mean"))

        # 主逻辑
        ret = []
        length = len(rawData[0])  # 获取数据个数（扫描点个数）
        for i in range(len(ContinueList)):
            ContinueItem = ContinueList[i]  # 是个二维列表，最前面一项是个列表，表示该物质信息
            ret.append([dataProcessing[i], smoothData[i]])
            redList = []  # 一维列表
            areas = []  # 一维列表
            peakInfo = []  # 记录峰顶信息：二维列表，因为可能有多个峰[[index, RT, Intensity], ..., [...]]
            if len(ContinueItem) == 1:  # 说明该图为空图
                pass
            elif (len(ContinueItem) == 2) and \
                    ((ContinueItem[1][1]-ContinueItem[1][0]) <= int(length/10)):  # 说明只有一项连续的数据，并且很窄
                redList = ContinueItem[1][:2]
                areas = [format(ContinueItem[1][2]/orderValueList[i], '.2f')]
                # 计算峰顶信息，smoothData[a:b]最大值对应的索引对应的实际值
                peakMaxIndex = np.argmax(smoothData[i][ContinueItem[1][0]:ContinueItem[1][1]]) + ContinueItem[1][0]
                peakMaxIntensity = format(rawData[i][peakMaxIndex]/orderValueList[i], '.3f')
                peakInfo.append([peakMaxIndex, self.sortedRTValue[peakMaxIndex], peakMaxIntensity])
            else:  # 说明有一项既以上的连续数据，此时需要峰分割，只有一项连续的数据，不窄，重点逻辑
                redList, areas, peakInfo = self.PeakDivSplit(rawData[i], smoothData[i], orderValueList[i])
            parameters = [redList, areas, peakInfo, orderStrList[i], maxValueList[i]]
            ret[i].append(parameters)

        return ret

    # 滤波算法
    def Filter(self, data, filterType="median", filterSize=10):
        rawDataLength = len(data)
        if rawDataLength <= filterSize:
            return data

        newData = []
        halfFilterSize = int(filterSize / 2)  # 开始滤波的位置
        endEdge = rawDataLength - halfFilterSize  # 滤波结束位置
        # 前面halfFilterSize个数据
        for i in range(halfFilterSize):
            newData.append(data[i])
        # 滤波
        if filterType == "median":  # 中位值滤波法
            for i in range(halfFilterSize, endEdge):
                newData.append(np.median(np.array(data[i - halfFilterSize:i + halfFilterSize])))
        elif filterType == "mean":  # 滑动平均数滤波
            for i in range(halfFilterSize, endEdge):
                newData.append(np.mean(np.array(data[i - halfFilterSize:i + halfFilterSize])))
        # 后面halfFilterSize个数据
        for i in range(endEdge, rawDataLength):
            newData.append(data[i])

        return np.array(newData)

    # 拟合滤波算法
    def FilterPoly(self, data):
        # 获取数据个数（扫描点个数）
        length = len(data)
        # 将数据进行平滑处理，分为两段平滑：[0...shortEdge]，[longEdge...length-1]
        shortWinLength = 101  # 平滑数据窗口大小
        longWinLength = 201
        shortEdge = int(length / 6)  # 500
        bufferLength = int(length / 20)  # 150
        longEdge = shortEdge - 2 * bufferLength

        y1 = savgol_filter(data[:shortEdge], window_length=shortWinLength, polyorder=2)
        y2 = savgol_filter(data[longEdge:], window_length=longWinLength, polyorder=2)
        # 合并平滑后的数据：[0...shortEdge-bufferLength]，[bufferLength...length-1]
        y = np.hstack([y1[: shortEdge - bufferLength], y2[bufferLength:]])

        return y

    # 重点逻辑，峰分割
    def PeakDivSplit(self, rawdata, smoothdata, ordervalue):
        """
        :param rawdata: 原始数据，一维numpy格式
        :param smoothdata: 平滑处理后的数据，一维numpy格式
        :param ordervalue: rawdata中最大值
        :return:
        """
        # 返回内容
        ret = []
        areas = []
        # 定义峰谷，峰顶左右比较数据的偏移量
        # 若：smoothdata[i] < smoothdata[i-deviation]，smoothdata[i] < smoothdata[i+deviation]，smoothdata[i]是峰底
        # 若：smoothdata[i] > smoothdata[i-deviation]，smoothdata[i] > smoothdata[i+deviation]，smoothdata[i]是峰顶
        deviation = int(len(rawdata) / 75)
        # 平滑后的数据的最大值
        smoothMax = np.max(smoothdata)
        i = deviation
        while i < len(smoothdata) - deviation:
            # 寻找峰谷
            while (i < len(smoothdata) - deviation) and \
                    not ((smoothdata[i] < smoothdata[i-deviation]) and (smoothdata[i] < smoothdata[i+deviation])):
                i += 1
            left = i
            # 寻找峰顶
            while (i < len(smoothdata) - deviation) and \
                    not ((smoothdata[i] > smoothdata[i-deviation]) and (smoothdata[i] > smoothdata[i+deviation])):
                i += 1
            top = i
            # 寻找峰谷
            while (i < len(smoothdata) - deviation) and \
                    not ((smoothdata[i] < smoothdata[i - deviation]) and (smoothdata[i] < smoothdata[i + deviation])):
                i += 1
            right = i
            # 判断峰是否足够高
            while (i < len(smoothdata) - deviation) and (smoothdata[top] - smoothdata[right] < smoothMax / 100):
                # 寻找峰顶
                while (i < len(smoothdata) - deviation) and \
                        not ((smoothdata[i] > smoothdata[i - deviation]) and (smoothdata[i] > smoothdata[i + deviation])):
                    i += 1
                top = i
                # 寻找峰谷
                while (i < len(smoothdata) - deviation) and \
                        not ((smoothdata[i] < smoothdata[i - deviation]) and (smoothdata[i] < smoothdata[i + deviation])):
                    i += 1
                right = i
            if i < len(smoothdata) - deviation:
                ret.append(left)
                ret.append(right)
                # 计算面积
                areas.append(format(np.sum(rawdata[left:right])/ordervalue, '.2f'))
        # 面积小于0.05的峰，删除
        areaThreshold = 0.05
        redList = []
        areasList = []
        k = 0
        while k < len(areas):
            if float(areas[k]) >= areaThreshold:
                redList.append(ret[2*k])
                redList.append(ret[2*k+1])
                areasList.append(areas[k])
            k += 1
        # 计算峰顶相关信息，smoothData[a:b]最大值对应的索引对应的实际值
        peakInfo = []
        for i in range(len(areasList)):
            peakLeft = redList[2*i]
            peakRight = redList[2*i+1]
            peakMaxIndex = np.argmax(smoothdata[peakLeft:peakRight]) + peakLeft
            peakMaxIntensity = rawdata[peakMaxIndex] / ordervalue  # 可能为0，因为存在不连续的点

            tempIndex = peakMaxIndex
            tempIntensity = peakMaxIntensity
            while tempIntensity == 0.0:  # 寻找邻近的不为0的点
                tempIndex += 1  # peakMaxIndex此时不一定是最大值对应的索引
                if tempIndex >= len(rawdata):
                    break
                tempIntensity = rawdata[tempIndex] / ordervalue
            if tempIndex >= len(rawdata):
                peakMaxIntensity = format(peakMaxIntensity, '.3f')  # str格式
            else:
                peakMaxIndex = tempIndex
                peakMaxIntensity = format(tempIntensity, '.3f')  # str格式

            peakInfo.append([peakMaxIndex, self.sortedRTValue[peakMaxIndex], peakMaxIntensity])  # 和areasList长度一致

        if self.PeakDivNeedMerge:  # 根据参数决定最前面的尖峰是否合并到后面
            lengthThreshold = int(len(smoothdata) / 15)  # 200左右
            leftThreshold = int(len(smoothdata) / 6)  # 500左右
            if len(areas) >= 3:  # 只有峰数大于等于三个才可能合并
                if redList[1] <= leftThreshold \
                        and (redList[1] - redList[0]) <= lengthThreshold \
                        and redList[1] == redList[2]:
                    sumArea = format(float(areasList[0]) + float(areasList[1]), '.2f')
                    del redList[2]
                    del redList[1]
                    del areasList[1]
                    del areasList[0]
                    del peakInfo[0]
                    areasList.insert(0, sumArea)

        return redList, areasList, peakInfo

    # 根据某个峰的数据，画出相应的图形
    def PlotAfterRemoveFP(self, parameters):
        """
        :param parameters: 生成该图片需要的所有数据
            item: 格式：["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion",....]
            smoothItem: 该组数据平滑后的结果，只有item中的数据平滑后的结果
            parameters:
                redList: 列表，对应的位置红线,位置从小到大,不包含0 和 len(data)-1
                        [50, 100, 100, 425, 500, 700]代表[50...100]，[100...425]，[500...700]三个峰
                areas: 列表，各个峰的面积
                        [2.104, 3.105, 5.211]代表[50...100]，[100...425]，[500...700]三个峰的面积分别为2.104, 3.105, 5.211
                orderOfMagnitude: 面积的数量级，字符串格式，比如：1e8
                max: 该组数据的最大值（item的最大值），数字格式
        :return:
        """
        # 运行该函数一次生成一张图片
        item = parameters[0]
        smoothItem = parameters[1]
        parameter = parameters[2]
        # 二级参数
        redList = parameter[0]  # 列表
        areas = parameter[1]  # 列表，里面的数据是str
        peakInfo = parameter[2]  # 记录峰顶信息：二维列表，因为可能有多个峰[[index, RT, Intensity], ..., [...]]
        orderOfMagnitude = parameter[3]  # 字符串
        max = parameter[4]  # 浮点数

        # 将item分切为两部分，信息 和 数据
        information = item[:9]
        data = item[9:]
        # 横坐标
        x = [i for i in range(len(data))]
        # 文件输出需要的信息
        SampleMass = information[0]
        Class = information[2]  # 化合物类型
        DBENum = information[3]  # 不饱和度数目
        formula = information[4]
        CNum = information[6]
        # 返回值
        ret = []
        for i in range(len(areas)):
            # print(len(areas), len(peakInfo))
            ret.append([SampleMass, float(areas[i]), peakInfo[i][0], peakInfo[i][1]] + information[2:8] + [orderOfMagnitude])
        if len(ret) != 0:
            ret.append([])
        if self.PeakDivNeedGenImage:  # 根据参数决定是否生成图片
            # 创建对应的文件夹
            newDirectory = CreateDirectory(self.outputFilesPath, "./intermediateFiles", "/_6_peakDivision/peakImages/" + Class + "_DBE" + str(DBENum))
            # 画图
            step = 0.05
            # 改变y坐标的范围
            bottomNum = 2 if len(peakInfo) <= 2 else len(peakInfo)
            plt.ylim(-(step * (bottomNum + 1) * max), (1+step*6) * max)
            # 添加坐标提示，标题
            plt.xlabel('RT', fontproperties='SimHei', fontsize=15, color='k')
            plt.ylabel('Intensity', fontproperties='SimHei', fontsize=15, color='k')
            title = "Mass:" + str(SampleMass) + "  DBE:" + str(DBENum) + "  formula:" + formula
            plt.title(title, fontproperties='SimHei', fontsize=12, color='red')
            # 画出线图，原始数据
            plt.vlines(x=x, ymin=0, ymax=data, colors="b", linewidth=1)
            # 画出峰之间以及两侧的分割线，+15为了修正画出来的偏移
            for splitIndex in redList:
                plt.vlines(x=splitIndex+15, ymin=-int((step*2) * max), ymax=int((1+step*4) * max), colors="g", linewidth=0.5)
            # 添加峰面积信息
            for k in range(len(areas)):
                start = redList[k*2]
                end = redList[k*2+1]
                middle = int((start + end) / 2 - 50)
                plt.text(middle, int((1+step*(k % 2+1))*(max+1)), areas[k], fontproperties='SimHei', fontsize=5, color="k")
            # 添加数量级标识
            plt.text(int(4 * len(data) / 5), int((1+step*4.4) * (max + 1)), "数量级:" + orderOfMagnitude, fontproperties='SimHei', fontsize=8, color="k")
            # 添加三元组含义提示
            plt.text(int(len(data) / 50), int((1+step*4.6) * (max + 1)), "三元组含义:(Index, RT, Intensity)", fontproperties='SimHei', fontsize=6, color="k")
            # 画出平滑后的曲线
            plt.plot(x, smoothItem, color="r", linewidth=0.6)
            # 添加峰顶标记信息
            for i in range(len(peakInfo)):
                peak = peakInfo[i]
                index = peak[0]  # int
                RT = peak[1]  # float
                Intensity = peak[2]  # str
                plt.vlines(x=x[index], ymin=-int(step * max), ymax=int((1+step*2) * max), colors="r", linewidth=0.5, linestyle="--")
                text = "(" + str(index) + ", " + str(RT) + ", " + Intensity + ")"
                plt.text(index-200, -int(step * (i % 4 + 1) * (max + 1)), text, fontproperties='SimHei', fontsize=5, color="k")
            # 保存图像
            plt.savefig(fname=newDirectory + "/" + Class + "_DBE" + str(DBENum) + "_C" + str(CNum), dpi=200)
            # 关闭当前图像
            plt.close()

        return ret

# 多线程
class MultiThread(QThread):
    signal = pyqtSignal(list)

    def __init__(self, function=None, parameters=None, outputFilesPath=""):
        super(MultiThread, self).__init__()
        self.__function = function  # 指定运行的功能
        self.__parameters = parameters  # 运行需要的参数
        self.outputFilesPath = outputFilesPath  # 文件输出的路径

    def run(self):
        startTime = time.time()

        if self.__function == "ClassDeleteBlank":
            try:
                cdb = ClassDeleteBlank(self.__parameters, self.outputFilesPath)
                deleteBlankResult, deleteBlankIsFinished = cdb.DeleteBlank()
                self.signal.emit(["ClassDeleteBlank", deleteBlankResult, deleteBlankIsFinished])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_CDB_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_CDB_MultiThread"])
        elif self.__function == "ClassGenerateDataBase":
            try:
                cgdb = ClassGenerateDataBase(self.__parameters, self.outputFilesPath)
                GDBResult, GDBIsFinished = cgdb.GenerateData()
                self.signal.emit(["ClassGenerateDataBase", GDBResult, GDBIsFinished])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_CGDB_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_CGDB_MultiThread"])
        elif self.__function == "ClassDeleteIsotope":
            try:
                cdi = ClassDeleteIsotope(self.__parameters, self.outputFilesPath)
                DelIsoResult, DelIsoIsFinished = cdi.DeleteIsotope()
                self.signal.emit(["ClassDeleteIsotope", DelIsoResult, DelIsoIsFinished])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_CDI_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_CDI_MultiThread"])
        elif self.__function == "ClassPeakDistinguish":
            try:
                cpd = ClassPeakDistinguish(self.__parameters, self.outputFilesPath)
                PeakDisResult, PeakDisIsFinished = cpd.PeakDistinguish()
                self.signal.emit(["ClassPeakDistinguish", PeakDisResult, PeakDisIsFinished])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_CPD1_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_CPD1_MultiThread"])
        elif self.__function == "ClassRemoveFalsePositive":
            try:
                crfp = ClassRemoveFalsePositive(self.__parameters, self.outputFilesPath)
                RemoveFPResult, RemoveFPIsFinished = crfp.RemoveFalsePositive()
                self.signal.emit(["ClassRemoveFalsePositive", RemoveFPResult, RemoveFPIsFinished])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_CRFP_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_CRFP_MultiThread"])
        elif self.__function == "ClassPeakDivision":
            try:
                cpd = ClassPeakDivision(self.__parameters, self.outputFilesPath)
                PeakDivResult, PeakDivIsFinished = cpd.PeakDivision()
                self.signal.emit(["ClassPeakDivision", PeakDivResult, PeakDivIsFinished])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_CPD2_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_CPD2_MultiThread"])
        elif self.__function == "ClassPlot":
            try:
                cp = ClassPlot(self.__parameters, self.outputFilesPath)
                PlotImagePath, PlotRawData = cp.Plot()
                self.signal.emit(["ClassPlot", PlotImagePath, PlotRawData])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_CPlot_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_CPlot_MultiThread"])
        elif self.__function == "ImportSampleFile":  # 读入数据显示，后台处理
            try:
                sampleFilePath = self.__parameters[0]  # 提取参数
                sampleData = np.array(pd.read_excel(sampleFilePath, header=None)).tolist()  # 弹出提示框
                self.signal.emit(["ImportSampleFile", sampleData])  # 返回结果
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_ImSample_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_ImSample_MultiThread"])
        elif self.__function == "ImportBlankFile":  # 读入数据显示，后台处理
            try:
                blankFilePath = self.__parameters[0]  # 提取参数
                blankData = np.array(pd.read_excel(blankFilePath, header=None)).tolist()  # 弹出提示框
                self.signal.emit(["ImportBlankFile", blankData])  # 返回结果
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_ImBlank_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_ImBlank_MultiThread"])
        elif self.__function == "ImportTICFile":  # 读入数据显示，后台处理
            try:
                TICFilePath = self.__parameters[0]  # 提取参数
                TICData, TICDataDictionary = self.ReadTIC(TICFilePath)  # 弹出提示框
                self.signal.emit(["ImportTICFile", TICData, TICDataDictionary])  # 返回结果
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_ImTIC_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_ImTIC_MultiThread"])
        elif self.__function == "StartMode1":
            try:
                # 提取参数
                DeleteBlankParameterList = self.__parameters[0]  # 去空白
                GDBParameterList = self.__parameters[1]  # 数据库生成
                DelIsoParameterList = self.__parameters[2]  # 搜同位素
                RemoveFPParameterList = self.__parameters[3]  # 去假阳性
                # 去空白
                cdb = ClassDeleteBlank(DeleteBlankParameterList, self.outputFilesPath)
                deleteBlankResult, deleteBlankIsFinished = cdb.DeleteBlank()
                functionStr = "去空白处理完毕！正在处理：数据库生成..."
                self.signal.emit(["deleteBlankFinished", deleteBlankResult, deleteBlankIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("扣空白完成！")
                # 数据库生成
                cgdb = ClassGenerateDataBase(GDBParameterList, self.outputFilesPath)
                GDBResult, GDBIsFinished = cgdb.GenerateData()
                functionStr = "数据库生成完毕！正在处理：搜同位素..."
                self.signal.emit(["GDBFinished", GDBResult, GDBIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("数据库生成完成！")
                # 搜同位素
                DelIsoParameterList[0] = deleteBlankResult  # 更新数据，此处注意
                DelIsoParameterList[1] = GDBResult
                cdi = ClassDeleteIsotope(DelIsoParameterList, self.outputFilesPath)
                DelIsoResult, DelIsoIsFinished = cdi.DeleteIsotope()
                functionStr = "搜同位素处理完毕！正在处理：去假阳性..."
                self.signal.emit(["DelIsoFinished", DelIsoResult, DelIsoIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("搜同位素完成！")
                # 去假阳性
                RemoveFPParameterList[0] = DelIsoResult  # 更新数据，此处注意
                # RemoveFPParameterList[1] = PeakDisResult
                crfp = ClassRemoveFalsePositive(RemoveFPParameterList, self.outputFilesPath)
                RemoveFPResult, RemoveFPIsFinished = crfp.RemoveFalsePositive()
                functionStr = "全部处理完毕！"
                self.signal.emit(["RemoveFPFinished", RemoveFPResult, RemoveFPIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("去假阳性完成！")
                # 返回结果
                self.signal.emit(["StartMode"])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_StartMode1_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_StartMode_MultiThread"])
        elif self.__function == "StartMode2":
            try:
                # 提取参数
                DeleteBlankParameterList = self.__parameters[0]  # 去空白
                GDBParameterList = self.__parameters[1]  # 数据库生成
                DelIsoParameterList = self.__parameters[2]  # 搜同位素
                PeakDisParameterList = self.__parameters[3]  # 峰提取
                RemoveFPParameterList = self.__parameters[4]  # 去假阳性
                # 去空白
                cdb = ClassDeleteBlank(DeleteBlankParameterList, self.outputFilesPath)
                deleteBlankResult, deleteBlankIsFinished = cdb.DeleteBlank()
                functionStr = "去空白处理完毕！正在处理：数据库生成..."
                self.signal.emit(["deleteBlankFinished", deleteBlankResult, deleteBlankIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("扣空白完成！")
                # 数据库生成
                cgdb = ClassGenerateDataBase(GDBParameterList, self.outputFilesPath)
                GDBResult, GDBIsFinished = cgdb.GenerateData()
                functionStr = "数据库生成完毕！正在处理：搜同位素..."
                self.signal.emit(["GDBFinished", GDBResult, GDBIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("数据库生成完成！")
                # 搜同位素
                DelIsoParameterList[0] = deleteBlankResult  # 更新数据，此处注意
                DelIsoParameterList[1] = GDBResult
                cdi = ClassDeleteIsotope(DelIsoParameterList, self.outputFilesPath)
                DelIsoResult, DelIsoIsFinished = cdi.DeleteIsotope()
                functionStr = "搜同位素处理完毕！正在处理：峰提取..."
                self.signal.emit(["DelIsoFinished", DelIsoResult, DelIsoIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("搜同位素完成！")
                # 峰提取
                PeakDisParameterList[1] = DelIsoResult  # 更新数据，此处注意
                cpd = ClassPeakDistinguish(PeakDisParameterList, self.outputFilesPath)
                PeakDisResult, PeakDisIsFinished = cpd.PeakDistinguish()
                functionStr = "峰提取处理完毕！正在处理：去假阳性..."
                self.signal.emit(["PeakDisFinished", PeakDisResult, PeakDisIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("峰提取完成！")
                # 去假阳性
                RemoveFPParameterList[0] = DelIsoResult  # 更新数据，此处注意
                RemoveFPParameterList[1] = PeakDisResult
                crfp = ClassRemoveFalsePositive(RemoveFPParameterList, self.outputFilesPath)
                RemoveFPResult, RemoveFPIsFinished = crfp.RemoveFalsePositive()
                functionStr = "全部处理完毕！"
                self.signal.emit(["RemoveFPFinished", RemoveFPResult, RemoveFPIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("去假阳性完成！")
                # 返回结果
                self.signal.emit(["StartMode"])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_StartMode2_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_StartMode_MultiThread"])
        elif self.__function == "StartMode3":
            try:
                # 提取参数
                DeleteBlankParameterList = self.__parameters[0]  # 去空白
                GDBParameterList = self.__parameters[1]  # 数据库生成
                DelIsoParameterList = self.__parameters[2]  # 搜同位素
                PeakDisParameterList = self.__parameters[3]  # 峰提取
                RemoveFPParameterList = self.__parameters[4]  # 去假阳性
                PeakDivParameterList = self.__parameters[5]  # 峰检测
                # 去空白
                cdb = ClassDeleteBlank(DeleteBlankParameterList, self.outputFilesPath)
                deleteBlankResult, deleteBlankIsFinished = cdb.DeleteBlank()
                functionStr = "去空白处理完毕！正在处理：数据库生成..."
                self.signal.emit(["deleteBlankFinished", deleteBlankResult, deleteBlankIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("扣空白完成！")
                # 数据库生成
                cgdb = ClassGenerateDataBase(GDBParameterList, self.outputFilesPath)
                GDBResult, GDBIsFinished = cgdb.GenerateData()
                functionStr = "数据库生成完毕！正在处理：搜同位素..."
                self.signal.emit(["GDBFinished", GDBResult, GDBIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("数据库生成完成！")
                # 搜同位素
                DelIsoParameterList[0] = deleteBlankResult  # 更新数据，此处注意
                DelIsoParameterList[1] = GDBResult
                cdi = ClassDeleteIsotope(DelIsoParameterList, self.outputFilesPath)
                DelIsoResult, DelIsoIsFinished = cdi.DeleteIsotope()
                functionStr = "搜同位素处理完毕！正在处理：峰提取..."
                self.signal.emit(["DelIsoFinished", DelIsoResult, DelIsoIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("搜同位素完成！")
                # 峰提取
                PeakDisParameterList[1] = DelIsoResult  # 更新数据，此处注意
                cpd = ClassPeakDistinguish(PeakDisParameterList, self.outputFilesPath)
                PeakDisResult, PeakDisIsFinished = cpd.PeakDistinguish()
                functionStr = "峰提取处理完毕！正在处理：去假阳性..."
                self.signal.emit(["PeakDisFinished", PeakDisResult, PeakDisIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("峰提取完成！")
                # 去假阳性
                RemoveFPParameterList[0] = DelIsoResult  # 更新数据，此处注意
                RemoveFPParameterList[1] = PeakDisResult
                crfp = ClassRemoveFalsePositive(RemoveFPParameterList, self.outputFilesPath)
                RemoveFPResult, RemoveFPIsFinished = crfp.RemoveFalsePositive()
                functionStr = "去假阳性处理完毕！正在处理：峰检测..."
                self.signal.emit(["RemoveFPFinished", RemoveFPResult, RemoveFPIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("去假阳性完成！")
                # 峰检测
                # PeakDisClassIsNeed = PeakDisParameterList[5]
                # if PeakDisClassIsNeed:  # 需要判断是否需要运行，此时设置的参数不起作用
                PeakDivParameterList[1] = RemoveFPResult[1]  # 更新数据，此处注意
                PeakDivParameterList[2] = PeakDisResult[2]
                cpd = ClassPeakDivision(PeakDivParameterList, self.outputFilesPath)
                PeakDivResult, PeakDivIsFinished = cpd.PeakDivision()
                functionStr = "全部处理完毕！"
                self.signal.emit(["PeakDivFinished", PeakDivResult, PeakDivIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("峰检测完成！")
                # 返回结果
                self.signal.emit(["StartMode"])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_StartMode3_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_StartMode_MultiThread"])
        elif self.__function == "StartMode4":
            try:
                # 提取参数
                GDBParameterList = self.__parameters[0]  # 数据库生成
                DelIsoParameterList = self.__parameters[1]  # 搜同位素
                RemoveFPParameterList = self.__parameters[2]  # 去假阳性
                # 数据库生成
                cgdb = ClassGenerateDataBase(GDBParameterList, self.outputFilesPath)
                GDBResult, GDBIsFinished = cgdb.GenerateData()
                functionStr = "数据库生成完毕！正在处理：搜同位素..."
                self.signal.emit(["GDBFinished", GDBResult, GDBIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("数据库生成完成！")
                # 搜同位素
                # DelIsoParameterList[0] = deleteBlankResult  # 更新数据，此处注意
                DelIsoParameterList[1] = GDBResult  # 更新数据，此处注意
                cdi = ClassDeleteIsotope(DelIsoParameterList, self.outputFilesPath)
                DelIsoResult, DelIsoIsFinished = cdi.DeleteIsotope()
                functionStr = "搜同位素处理完毕！正在处理：去假阳性..."
                self.signal.emit(["DelIsoFinished", DelIsoResult, DelIsoIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("搜同位素完成！")
                # 去假阳性
                RemoveFPParameterList[0] = DelIsoResult  # 更新数据，此处注意
                # RemoveFPParameterList[1] = PeakDisResult
                crfp = ClassRemoveFalsePositive(RemoveFPParameterList, self.outputFilesPath)
                RemoveFPResult, RemoveFPIsFinished = crfp.RemoveFalsePositive()
                functionStr = "全部处理完毕！"
                self.signal.emit(["RemoveFPFinished", RemoveFPResult, RemoveFPIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("去假阳性完成！")
                # 返回结果
                self.signal.emit(["StartMode"])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_StartMode4_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_StartMode_MultiThread"])
        elif self.__function == "StartMode5":
            try:
                # 提取参数
                GDBParameterList = self.__parameters[0]  # 数据库生成
                DelIsoParameterList = self.__parameters[1]  # 搜同位素
                PeakDisParameterList = self.__parameters[2]  # 峰提取
                RemoveFPParameterList = self.__parameters[3]  # 去假阳性
                # 数据库生成
                cgdb = ClassGenerateDataBase(GDBParameterList, self.outputFilesPath)
                GDBResult, GDBIsFinished = cgdb.GenerateData()
                functionStr = "数据库生成完毕！正在处理：搜同位素..."
                self.signal.emit(["GDBFinished", GDBResult, GDBIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("数据库生成完成！")
                # 搜同位素
                DelIsoParameterList[1] = GDBResult  # 更新数据，此处注意
                cdi = ClassDeleteIsotope(DelIsoParameterList, self.outputFilesPath)
                DelIsoResult, DelIsoIsFinished = cdi.DeleteIsotope()
                functionStr = "搜同位素处理完毕！正在处理：峰提取..."
                self.signal.emit(["DelIsoFinished", DelIsoResult, DelIsoIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("搜同位素完成！")
                # 峰提取
                PeakDisParameterList[1] = DelIsoResult  # 更新数据，此处注意
                cpd = ClassPeakDistinguish(PeakDisParameterList, self.outputFilesPath)
                PeakDisResult, PeakDisIsFinished = cpd.PeakDistinguish()
                functionStr = "峰提取处理完毕！正在处理：去假阳性..."
                self.signal.emit(["PeakDisFinished", PeakDisResult, PeakDisIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("峰提取完成！")
                # 去假阳性
                RemoveFPParameterList[0] = DelIsoResult  # 更新数据，此处注意
                RemoveFPParameterList[1] = PeakDisResult
                crfp = ClassRemoveFalsePositive(RemoveFPParameterList, self.outputFilesPath)
                RemoveFPResult, RemoveFPIsFinished = crfp.RemoveFalsePositive()
                functionStr = "全部处理完毕！"
                self.signal.emit(["RemoveFPFinished", RemoveFPResult, RemoveFPIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("去假阳性完成！")
                # 返回结果
                self.signal.emit(["StartMode"])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_StartMode5_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_StartMode_MultiThread"])
        elif self.__function == "StartMode6":
            try:
                # 提取参数
                GDBParameterList = self.__parameters[0]  # 数据库生成
                DelIsoParameterList = self.__parameters[1]  # 搜同位素
                PeakDisParameterList = self.__parameters[2]  # 峰提取
                RemoveFPParameterList = self.__parameters[3]  # 去假阳性
                PeakDivParameterList = self.__parameters[4]  # 峰检测
                # 数据库生成
                cgdb = ClassGenerateDataBase(GDBParameterList, self.outputFilesPath)
                GDBResult, GDBIsFinished = cgdb.GenerateData()
                functionStr = "数据库生成完毕！正在处理：搜同位素..."
                self.signal.emit(["GDBFinished", GDBResult, GDBIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("数据库生成完成！")
                # 搜同位素
                DelIsoParameterList[1] = GDBResult  # 更新数据，此处注意
                cdi = ClassDeleteIsotope(DelIsoParameterList, self.outputFilesPath)
                DelIsoResult, DelIsoIsFinished = cdi.DeleteIsotope()
                functionStr = "搜同位素处理完毕！正在处理：峰提取..."
                self.signal.emit(["DelIsoFinished", DelIsoResult, DelIsoIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("搜同位素完成！")
                # 峰提取
                PeakDisParameterList[1] = DelIsoResult  # 更新数据，此处注意
                cpd = ClassPeakDistinguish(PeakDisParameterList, self.outputFilesPath)
                PeakDisResult, PeakDisIsFinished = cpd.PeakDistinguish()
                functionStr = "峰提取处理完毕！正在处理：去假阳性..."
                self.signal.emit(["PeakDisFinished", PeakDisResult, PeakDisIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("峰提取完成！")
                # 去假阳性
                RemoveFPParameterList[0] = DelIsoResult  # 更新数据，此处注意
                RemoveFPParameterList[1] = PeakDisResult
                crfp = ClassRemoveFalsePositive(RemoveFPParameterList, self.outputFilesPath)
                RemoveFPResult, RemoveFPIsFinished = crfp.RemoveFalsePositive()
                functionStr = "去假阳性处理完毕！正在处理：峰检测..."
                self.signal.emit(["RemoveFPFinished", RemoveFPResult, RemoveFPIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("去假阳性完成！")
                # 峰检测
                # PeakDisClassIsNeed = PeakDisParameterList[5]
                # if PeakDisClassIsNeed:  # 需要判断是否需要运行，此时设置的参数不起作用
                PeakDivParameterList[1] = RemoveFPResult[1]  # 更新数据，此处注意
                PeakDivParameterList[2] = PeakDisResult[2]
                cpd = ClassPeakDivision(PeakDivParameterList, self.outputFilesPath)
                PeakDivResult, PeakDivIsFinished = cpd.PeakDivision()
                functionStr = "全部处理完毕！"
                self.signal.emit(["PeakDivFinished", PeakDivResult, PeakDivIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("峰检测完成！")
                # 返回结果
                self.signal.emit(["StartMode"])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_StartMode6_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_StartMode_MultiThread"])
        endTime = time.time()
        if ConstValues.PsIsDebug:
            if endTime - startTime > 60:
                print("程序运行总用时：", (endTime - startTime) / 60, " min.")
            else:
                print("程序运行总用时：", endTime - startTime, " s.")

    # 负责读取总离子流图文件(txt)
    def ReadTIC(self, TICFilePath):
        """
        文件格式必须为：每行三个数据，一个表头，数据之间用制表符(\t)分割，无其他无关字符
        :return:返回结果为字典：{key:value,...,key:value}，value为二维列表[[Mass, Intensity],...,[Mass, Intensity]]
        """
        startTime = time.time()
        # 读取数据，数据分割
        f = open(TICFilePath, "r")
        content = f.read().strip().replace("\n", "\t").replace(" ", "").split("\t")
        # 去除表头
        header = content[:3]
        content = content[3:]
        if len(content) / 3 != int(len(content) / 3):
            # raise Exception("Error in ClassPeakDistinguish ReadTIC.")
            PromptBox().warningMessage("总离子流图文件(txt)存在问题，请重新选择！")
            return None, None
        # str全部转为float
        content = [float(item) for item in content]
        # 返回结果，二维字典
        resList = [header]
        # 返回结果为字典：{key:value}，value为二维列表[[Mass, Intensity],...,[Mass, Intensity]]
        resDictionary = {}

        key = content[0]
        value = []
        for i in range(int(len(content) / 3)):
            resList.append(content[(i * 3): (i * 3 + 3)])
            if content[i * 3] != key:
                resDictionary[key] = value  # 字典中添加元素（二维列表）
                key = content[i * 3]
                value = []
            value.append([content[i * 3 + 1], content[i * 3 + 2]])

        if ConstValues.PsIsDebug:
            print(
                "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                sys._getframe().f_code.co_name, "\" method***：",
                "扫描点的个数 len(resDictionary):", len(resDictionary)
            )
        endTime = time.time()
        if ConstValues.PsIsDebug:
            print(
                "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                sys._getframe().f_code.co_name, "\" method***：",
                "读入和处理文件费时: ", endTime - startTime, " s"
            )
        return resList, resDictionary

# 绘图
class ClassPlot:
    def __init__(self, parameterList, outputFilesPath):
        assert len(parameterList) == 14, "ClassPlot参数个数不对!"
        self.RemoveFPId = parameterList[0]  # 判断选择了哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
        self.RemoveFPResult = parameterList[1]  # 所有类别去假阳性的结果，二维列表，有表头
        self.PlotTitleName = parameterList[2]  # 标题名称
        self.PlotTitleColor = parameterList[3]  # 标题颜色，(R, G, B, Alpha)，针对plt，值为0~255，需要转为0~1
        self.PlotXAxisName = parameterList[4]  # x轴名称
        self.PlotXAxisColor = parameterList[5]  # x轴颜色，(R, G, B, Alpha)，针对plt，值为0~255，需要转为0~1
        self.PlotYAxisName = parameterList[6]  # y轴名称
        self.PlotYAxisColor = parameterList[7]  # y轴颜色，(R, G, B, Alpha)，针对plt，值为0~255，需要转为0~1
        self.PlotHasEnter = parameterList[8]  # 记录是否进入过PlotSetup()函数
        self.PlotType = parameterList[9]  # 绘图类型
        self.PlotClassList = parameterList[10]  # 列表，需要绘制的类型，例子：["CH", "N1"]
        self.PlotClassItem = parameterList[11]  # 列表，需要绘制的类型，例子：["CH"]，对应单选钮，长度必须为1
        self.PlotDBENum = parameterList[12]  # 整数，记录用户选择的DBE数目
        self.PlotConfirm = parameterList[13]  # 是否需要绘图

        # 用户选择的文件的生成位置
        self.outputFilesPath = outputFilesPath

        # 去掉表头
        self.RemoveFPResult = self.RemoveFPResult[1:]

    # 主逻辑，画图
    def Plot(self):
        # 添加坐标名称，标题
        plt.xlabel(self.PlotXAxisName, fontproperties='SimHei', fontsize=12, color=[num / 255 for num in self.PlotXAxisColor])
        plt.ylabel(self.PlotYAxisName, fontproperties='SimHei', fontsize=12, color=[num / 255 for num in self.PlotYAxisColor])

        # 创建对应文件夹
        newDirectory = CreateDirectory(self.outputFilesPath, "./intermediateFiles", "/_7_plot")

        # 3.搜同位素 去假阳性后的数据
        # ["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
        ClassIndex = 2  # 类别对应的Index
        DBEIndex = 3  # 不饱和度对应的Index
        CIndex = 6  # C数对应的Index
        if self.RemoveFPId == 2:  # 4.峰识别 去假阳性后的数据，需要加和的为area
            # ["SampleMass", "Area", "startRT", "startRTValue", "endRT", "endRTValue", "TICMassMedian",
            # "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
            ClassIndex = 7
            DBEIndex = 8
            CIndex = 11
        sumIndex = 1  # 需要加和的为SampleIntensity，或者Area

        # 根据图的类型不同，绘制图形
        if self.PlotType == 1:  # Class distribution
            if len(self.PlotClassList) == 0:  # 不存在要绘制的类别，绘制失败
                plt.close()
                return None, []

            # 计算所需要的数据
            sumList = [0.0 for _ in range(len(self.PlotClassList))]
            # 转为字典，方便后面查找指定类型对应索引
            PlotClassDictionary = dict(zip(self.PlotClassList, [i for i in range(len(self.PlotClassList))]))
            for item in self.RemoveFPResult:
                if len(item) != 0:
                    if len(item) == 3:  # 搜同位素后去假阳性文件，还要跳过同位素
                        continue
                    itemClass = item[ClassIndex]
                    if itemClass in self.PlotClassList:
                        itemIndex = PlotClassDictionary[itemClass]  # 查询对应类别的下标
                        sumList[itemIndex] += item[sumIndex]
            sum = 0  # 计算总和
            for num in sumList:
                sum += num
            # 计算比例
            sumList = [num*100/sum for num in sumList]

            # 添加标题
            plt.title(self.PlotTitleName, fontproperties='SimHei', fontsize=12, color=[num / 255 for num in self.PlotTitleColor])
            # 可以绘制图形，横坐标：self.PlotClassList，纵坐标：sumList
            plt.bar(self.PlotClassList, sumList)
            imagePath = newDirectory + "/" + self.PlotTitleName
            plt.savefig(fname=imagePath, dpi=150)
            # 关闭绘图
            plt.close()
            # 返回图片路径
            return imagePath + ".png", [[self.PlotXAxisName]+self.PlotClassList, [self.PlotYAxisName]+[num/100 for num in sumList]]
        elif self.PlotType == 2:  # DBE distribution by class
            if len(self.PlotClassItem) == 0:  # 不存在要绘制的类别，绘制失败
                plt.close()
                return None, []

            # 计算所需要的数据
            DBEDictionary = {}  # key : DBE ,   value : 总量

            for item in self.RemoveFPResult:
                if len(item) != 0:
                    if len(item) == 3:  # 搜同位素后去假阳性文件，还要跳过同位素
                        continue
                    itemClass = item[ClassIndex]  # 获取类别
                    itemDBE = item[DBEIndex]  # DBE数目
                    if itemClass in self.PlotClassItem:
                        if itemDBE not in DBEDictionary:
                            DBEDictionary[itemDBE] = item[sumIndex]
                        else:
                            DBEDictionary[itemDBE] += item[sumIndex]

            # 提取出横纵坐标
            xList = []
            yList = []
            for key in sorted(DBEDictionary):
                value = DBEDictionary[key]
                xList.append(key)
                yList.append(value)

            sum = 0  # 计算总和
            for num in yList:
                sum += num
            yList = [num * 100 / sum for num in yList]  # 计算比例

            # 添加标题
            title = self.PlotTitleName + "_(" + str(self.PlotClassItem[0]) + ")"
            plt.title(title, fontproperties='SimHei', fontsize=12, color=[num / 255 for num in self.PlotTitleColor])
            # 可以绘制图形，横坐标：xList，纵坐标：yList
            plt.bar(xList, yList)
            imagePath = newDirectory + "/" + title
            plt.savefig(fname=imagePath, dpi=150)
            # 关闭绘图
            plt.close()
            # 返回图片路径
            return imagePath + ".png", [[self.PlotXAxisName]+xList, [self.PlotYAxisName]+[num / 100 for num in yList]]
        elif self.PlotType == 3:  # Carbon number distribution by class and DBE
            if (len(self.PlotClassItem) == 0) or (self.PlotDBENum == ConstValues.PsPlotDBENum):  # 不存在要绘制的类别，绘制失败
                plt.close()
                return None, []

            # 计算所需要的数据
            CDictionary = {}  # key : C ,   value : 总量

            for item in self.RemoveFPResult:
                if len(item) != 0:
                    if len(item) == 3:  # 搜同位素后去假阳性文件，还要跳过同位素
                        continue
                    itemClass = item[ClassIndex]  # 获取类别
                    itemDBE = item[DBEIndex]  # DBE数目
                    itemCNum = item[CIndex]
                    if (itemClass in self.PlotClassItem) and (self.PlotDBENum == itemDBE):
                        if itemDBE not in CDictionary:
                            CDictionary[itemCNum] = item[sumIndex]
                        else:
                            CDictionary[itemCNum] += item[sumIndex]

            # 提取出横纵坐标
            xList = []
            yList = []
            for key in sorted(CDictionary):
                value = CDictionary[key]
                xList.append(key)
                yList.append(value)

            sum = 0  # 计算总和
            for num in yList:
                sum += num
            yList = [num * 100 / sum for num in yList]  # 计算比例

            # 添加标题
            title = self.PlotTitleName + "_(" + str(self.PlotClassItem[0]) + "_DBE_" + str(self.PlotDBENum) + ")"
            plt.title(title, fontproperties='SimHei', fontsize=12, color=[num / 255 for num in self.PlotTitleColor])
            # 可以绘制图形，横坐标：xList，纵坐标：yList
            plt.bar(xList, yList)
            imagePath = newDirectory + "/" + title
            plt.savefig(fname=imagePath, dpi=150)
            # 关闭绘图
            plt.close()
            # 返回图片路径
            return imagePath + ".png", [[self.PlotXAxisName]+xList, [self.PlotYAxisName]+[num / 100 for num in yList]]
        elif self.PlotType == 4:  # DBE vs carbon number by class
            if len(self.PlotClassItem) == 0:  # 不存在要绘制的类别，绘制失败
                plt.close()
                return None, []

            # 计算所需要的数据
            DBECDictionary = {}  # key : (DBE, CNum),   value : 总量

            for item in self.RemoveFPResult:
                if len(item) != 0:
                    if len(item) == 3:  # 搜同位素后去假阳性文件，还要跳过同位素
                        continue
                    itemClass = item[ClassIndex]  # 获取类别
                    itemDBE = item[DBEIndex]  # DBE数目
                    itemCNum = item[CIndex]
                    if itemClass in self.PlotClassItem:  # 是需要绘制的类别
                        if (itemDBE, itemCNum) not in DBECDictionary:
                            DBECDictionary[(itemDBE, itemCNum)] = item[sumIndex]
                        else:
                            DBECDictionary[(itemDBE, itemCNum)] += item[sumIndex]

            # 提取出横纵坐标，气泡图的大小
            xList = []
            yList = []
            sizeList = []
            for key in sorted(DBECDictionary):
                value = DBECDictionary[key]
                xList.append(key[1])  # CNum
                yList.append(key[0])  # DBE
                sizeList.append(value)

            sum = 0  # 计算总和
            for num in sizeList:
                sum += num
            scaledSizeList = [num * 10000 / sum for num in sizeList]  # 计算比例

            # 添加标题
            title = self.PlotTitleName + "_(" + str(self.PlotClassItem[0]) + ")"
            plt.title(title, fontproperties='SimHei', fontsize=12, color=[num / 255 for num in self.PlotTitleColor])
            # 可以绘制图形，横坐标：xList，纵坐标：yList
            plt.scatter(xList, yList, s=scaledSizeList, c="red", alpha=0.6)
            imagePath = newDirectory + "/" + title
            plt.savefig(fname=imagePath, dpi=150)
            # 关闭绘图
            plt.close()
            # 返回图片路径
            return imagePath + ".png", [[self.PlotXAxisName]+xList, [self.PlotYAxisName]+yList, ["Size"]+sizeList]
        elif self.PlotType == 5:  # Kendrick mass defect （KMD）
            def round_up(num):
                # 默认num大于0，用round函数会造成数据错误，如：round(2.5) --> 2
                integer = int(num)
                decimalNum = num - integer
                if decimalNum >= 0.5:
                    return integer + 1
                else:
                    return integer

            sampleMassIndex = 0
            sampleMassSet = set()  # 记录不同的 sampleMass
            xList = []  # KM
            yList = []  # KMD
            for item in self.RemoveFPResult:
                if len(item) != 0:
                    if len(item) == 3:  # 搜同位素后去假阳性文件，还要跳过同位素
                        continue
                    # 获取sampleMass
                    sampleMass = item[sampleMassIndex]
                    # 记录数据
                    if sampleMass not in sampleMassSet:
                        KM = (sampleMass * 14.0) / 14.01565
                        NKM = round_up(KM)
                        KMD = NKM - KM
                        xList.append(NKM)
                        yList.append(KMD)
                    # 集合中添加元素
                    sampleMassSet.add(sampleMass)

            # 添加标题
            plt.title(self.PlotTitleName, fontproperties='SimHei', fontsize=12, color=[num / 255 for num in self.PlotTitleColor])
            # 可以绘制图形，横坐标：xList，纵坐标：yList
            plt.scatter(xList, yList, s=20, c="blue", alpha=0.8)
            imagePath = newDirectory + "/" + self.PlotTitleName
            plt.savefig(fname=imagePath, dpi=150)
            # 关闭绘图
            plt.close()
            # 返回图片路径
            return imagePath + ".png", [[self.PlotXAxisName] + xList, [self.PlotYAxisName] + yList]
        elif self.PlotType == 6:  # Retention time vs carbon number
            if (len(self.PlotClassItem) == 0) or (self.PlotDBENum == ConstValues.PsPlotDBENum) or (self.RemoveFPId == 1):  # 不存在要绘制的类别，绘制失败
                plt.close()
                return None, []

            # startRTValue 位置
            startRTValueIndex = 3
            # 计算所需要的数据
            xList = []  # CNum
            yList = []  # startRTValue

            for item in self.RemoveFPResult:
                if len(item) != 0:
                    if len(item) == 3:  # 搜同位素后去假阳性文件，还要跳过同位素
                        continue
                    itemClass = item[ClassIndex]  # 获取类别
                    itemDBE = item[DBEIndex]  # DBE数目
                    itemCNum = item[CIndex]  # C的数目
                    itemStartRTValue = item[startRTValueIndex]
                    if (itemClass in self.PlotClassItem) and (self.PlotDBENum == itemDBE):
                        xList.append(itemCNum)
                        yList.append(itemStartRTValue)

            # 添加标题
            title = self.PlotTitleName + "_(" + str(self.PlotClassItem[0]) + "_DBE_" + str(self.PlotDBENum) + ")"
            plt.title(title, fontproperties='SimHei', fontsize=12, color=[num / 255 for num in self.PlotTitleColor])
            # 可以绘制图形，横坐标：xList，纵坐标：yList
            plt.scatter(xList, yList, s=20, c="blue", alpha=0.8)
            imagePath = newDirectory + "/" + title
            plt.savefig(fname=imagePath, dpi=150)
            # 关闭绘图
            plt.close()
            # 返回图片路径
            return imagePath + ".png", [[self.PlotXAxisName]+xList, [self.PlotYAxisName]+yList]

# 帮助
class ClassHelp:

    def __init__(self, function, theme=""):
        self.__function = function
        self.MainWindowsStyle = theme

    # 设置QLabel
    def GetQLabel(self, text, style="", alignment=""):
        label = QLabel()
        label.setText(text)
        label.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        label.setStyleSheet(style)
        if alignment == "AlignCenter":
            label.setAlignment(Qt.AlignCenter)
        elif alignment == "AlignLeft":
            label.setAlignment(Qt.AlignLeft)
        elif alignment == "AlignRight":
            label.setAlignment(Qt.AlignRight)
        return label

    # 创建Dialog
    def CreateDialog(self, title, xNum, yNum):
        # 创建QDialog
        dialog = QDialog()
        dialog.setWindowTitle(title)
        dialog.setFixedSize(ConstValues.PsSetupFontSize * xNum, ConstValues.PsSetupFontSize * yNum)  # 固定窗口大小
        if ConstValues.PsIconType == 1:
            dialog.setWindowIcon(QIcon(ConstValues.PsWindowIcon))
        elif ConstValues.PsIconType == 2:
            dialog.setWindowIcon(
                qtawesome.icon(ConstValues.PsqtaWindowIcon, color=ConstValues.PsqtaWindowIconColor))
        return dialog

    def Help(self):
        if self.__function == "UIHelp":
            dialog = self.CreateDialog("界面介绍", 60, 40)
            dialog.setWindowOpacity(0.94)  # 设置透明度

            label = QLabel()
            imagePath = "./__system/images/help/uiExplain1.png"
            if self.MainWindowsStyle == "Qdarkstyle":
                imagePath = "./__system/images/help/uiExplainDark1.png"
            pixmap = QPixmap(imagePath)
            pixmap = pixmap.scaled(ConstValues.PsSetupFontSize * 55, 4000, Qt.KeepAspectRatio, Qt.SmoothTransformation) # 限制一个即可
            label.setPixmap(pixmap)  # 设置图片
            label.setAlignment(Qt.AlignCenter)  # 居中对齐

            layout = QVBoxLayout(dialog)  # 创建栅格布局
            # 栅格布局添加控件
            layout.addWidget(label)

            dialog.exec()  # 运行
        elif self.__function == "FileHelp":
            dialog = self.CreateDialog("文件帮助", 60, 40)
            dialog.setWindowOpacity(0.94)  # 设置透明度

            label = self.GetQLabel("菜单栏 “文件” 下各项功能解释：", "color:red; font-size:15pt")
            textEdit = QTextEdit()
            textEdit.setFocusPolicy(Qt.NoFocus)  # 禁止编辑
            textEdit.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
            # 显示内容编辑
            sampleExplain = "样本：该文件应该为excel文件，前" + str(ConstValues.PsHeaderLine) + "行为仪器输出信息概况，" \
                            "第" + str(ConstValues.PsHeaderLine+1) + "行为表头:(Mass, Intensity)，之后为两列数据。这个" \
                            "文件生成过程：添加石油的样本经过仪器处理后生成总离子图文件(TIC)，对于每个扫描点的所有Mass" \
                             "和Intensity求平均后得到的结果。"
            blankExplain = "空白：格式同“样本”。这个文件的生成过程：未添加石油的样本经过仪器处理后生成总离子图文件(" \
                           "TIC)，对于每个扫描点的所有Mass和Intensity求平均后得到的结果。"
            TICExplain = "样本TIC：该文件应该为txt文件，第一行是表头(labels, masses, intensity)，之后为数据。这个文件" \
                         "的生成过程：从仪器生成的.raw或者.mzXML文件经处理得到的结果。"
            importExplain = "导入：导入上次运行生成的文件夹中的文件，从而方便绘制图形。如果“输出”未选择的话，应该选择" \
                            "默认生成的intermediateFiles导入，否则应该选择你所选择“输出”文件夹。"
            outputExplain = "输出：选择软件运行过程中文件输出到的文件夹，如果不选择的话，中间文件会生成在intermediateFiles" \
                            "文件夹中。"
            ExitExplain = "退出：退出整个程序。"
            taskbarExplain = "工具栏和菜单栏对应功能一致。"
            showStr = sampleExplain + "\n\n" + blankExplain + "\n\n" + TICExplain + "\n\n" + importExplain + "\n\n" + outputExplain + "\n\n" + ExitExplain + "\n\n\n" + taskbarExplain
            textEdit.setPlainText(showStr)

            layout = QGridLayout(dialog)  # 创建栅格布局
            # 栅格布局添加控件
            layout.addWidget(label, 0, 0, 1, 1)
            layout.addWidget(textEdit, 1, 0, 1, 1)
            dialog.exec()  # 运行
        elif self.__function == "EditHelpDeleteBlank":
            explain = "这是一个参数设置界面，如果没有导入“空白”，虽然能设置数据，但不能运行这一步。" \
                      "这一步的目的：去除样品中无关物质以及仪器产生的影响，使得分析结果更加准确。"
            self.EditShow("去空白", explain)
        elif self.__function == "EditHelpGDB":
            explain = "这是一个参数设置界面，这一步不需要任何输入文件即可运行，根据用户输出参数自动生成信息，" \
                      "信息格式为：（Class, Neutral, Formula, Calc m/z, C, ion），即（类别，不饱和度，分子式，质荷比，" \
                      "碳的数目，仪器离子模式），生成的数据最终存储在excel中。这一步的目的：为后续分子式匹配做准备。"
            self.EditShow("数据库生成", explain)
        elif self.__function == "EditHelpDeleteIso":
            explain = "这是一个参数设置界面，这一步需要“（去空白后的）样本文件”（记为file_A）和生成的数据库文件，我们根据file_A里的内" \
                      "容根据Mass去匹配数据库，如果未匹配到，当前Mass结束，不记录任何信息，继续file_A中下一条记录的匹配；如果匹配到，则计算匹" \
                      "配到的分子式分子量为12的C元素替换为分子量为13的C元素，分别替换一个和两个，根据替换后分子量在file_A中搜" \
                      "索是否有对应的记录，并记录下来；信息格式为（SampleMass，SampleIntensity，Class, Neutral, Formula," \
                      " Calc m/z, C, ion），即（file_A中的Mass，file_A中的Intensity，类别，不饱和度，分子式，质荷比，碳的数目，仪器" \
                      "离子模式）；如果搜到同位素，则记下来，格式为（Mass，Intensity，iostope）。这个步骤最终生成一个excel文件，excel中" \
                      "的内容都是匹配到分子的记录。"
            self.EditShow("搜同位素", explain)
        elif self.__function == "EditHelpPeakDis":
            explain = "这是一个参数设置界面，这一步需要“搜同位素后的结果”（记为file_B）和总离子流图文件（TIC），我们根据file_B中的" \
                      "SampleMass去TIC中搜索是否有基本连续的Mass，并记录TIC中连续的Mass，信息格式为：（SampleMass，Area，startRT，" \
                      "startRTValue，endRT，endRTValue，TICMassMedian，Class，Neutral DBE，Formula，Calc m/z，C，ion），即（file_B" \
                      "中的Mass，TIC中区间[startRT,endRT]对应的Intensity之和，TIC中连续Mass开始的索引（从0开始，到扫描点个数-1结束），" \
                      "开始索引对应的保留时间（RT）的值，TIC中连续Mass结束的索引，结束索引对应的保留时间（RT）的值，TIC中区间[startRT," \
                      "endRT]对应的Mass大于该区间中最大Mass的60%的数据集合的中位数，类别，不饱和度，分子式，质荷比，碳的数目，仪器离子" \
                      "模式）。这个步骤最终生成一个excel文件。"
            self.EditShow("峰匹配", explain)
        elif self.__function == "EditHelpRFP":
            explain = "这是一个参数设置界面，这一步需要“搜同位素后的结果”（记为file_B）或者“峰匹配后的结果”（记为file_C），根据不饱" \
                      "和度（Neutral DBE）以及碳数（C）的连续性，判断是否需要去除，不满足连续条件的会被删除。这个步骤最终生成一个excel文" \
                      "件，格式和file_B或者file_C的格式一致。"
            self.EditShow("去假阳性", explain)
        elif self.__function == "EditHelpPeakDiv":
            explain = "这是一个参数设置界面，这一步需要“去假阳性后的结果（并且去假阳性需要选择的是“峰匹配后的结果”）”（记为file_D），" \
                      "我们已经进行了峰匹配，根据峰匹配的功能解释，我们相当于总离子流图（TIC）提取出一个个提取离子流图（EIC），这一步的" \
                      "目的就是：提取出每一个m/z的色峰谱，并计算峰面积。"
            self.EditShow("峰识别", explain)
        elif self.__function == "PlotHelp":
            dialog = self.CreateDialog("绘图帮助", 60, 40)
            dialog.setWindowOpacity(0.94)  # 设置透明度

            label = self.GetQLabel("菜单栏 “绘图->添加” 下解释：", "color:red; font-size:15pt")
            textEdit = QTextEdit()
            textEdit.setFocusPolicy(Qt.NoFocus)  # 禁止编辑
            textEdit.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
            # 显示内容编辑
            showStr = "需要去假阳性后生成的文件，去假阳性选择了哪个文件，就选择该文件去假阳性之后" \
                      "的文件进行可视化。"
            plot1Explain = "Class distribution：比较不同种类杂原子化合物（class）的相对含量差异。"
            plot2Explain = "DBE distribution by class：比较具有相同class的化合物，DBE的分布情况。"
            plot3Explain = "Carbon number distribution by class and DBEn：比较相同相同class且相" \
                           "同DBE的化合物碳数分布情况（根据这个情况，可以推测一定化合物结构信息）。"
            plot4Explain = "DBE vs carbon number by class：比较相同class化合物的DBE和碳数分布情况。"
            plot5Explain = "Kendrick mass defect （KMD）：KMD图（辅助判断排除假阳性的充分性）。"
            plot6Explain = "Retention time vs carbon number：同系物之间保留时间和碳数的关系（" \
                           "体现液相色谱方法的优越性）。"
            taskbarExplain = "工具栏和菜单栏对应功能一致。"
            showStr = showStr + "\n\n" + plot1Explain + "\n\n" + plot2Explain + "\n\n" + plot3Explain + \
                      "\n\n" + plot4Explain + "\n\n" + plot5Explain + "\n\n" + plot6Explain + "\n\n" + taskbarExplain
            textEdit.setPlainText(showStr)

            layout = QGridLayout(dialog)  # 创建栅格布局
            # 栅格布局添加控件
            layout.addWidget(label, 0, 0, 1, 1)
            layout.addWidget(textEdit, 1, 0, 1, 1)
            dialog.exec()  # 运行
        elif self.__function == "ModeHelp":
            dialog = self.CreateDialog("模式选择帮助", 60, 40)
            dialog.setWindowOpacity(0.94)  # 设置透明度

            label = self.GetQLabel("工具栏 “模式选择” 解释：", "color:red; font-size:15pt")
            textEdit = QTextEdit()
            textEdit.setFocusPolicy(Qt.NoFocus)  # 禁止编辑
            textEdit.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
            # 显示内容编辑
            showStr = "模式选择：此软件一共有6个主要的步骤（除了绘图之外），有些功能可以不必运行，但某些" \
                      "功能运行前必须运行某些功能，用户可以根据需要选择需要运行哪些内容。"
            textEdit.setPlainText(showStr)

            layout = QGridLayout(dialog)  # 创建栅格布局
            # 栅格布局添加控件
            layout.addWidget(label, 0, 0, 1, 1)
            layout.addWidget(textEdit, 1, 0, 1, 1)
            dialog.exec()  # 运行
        elif self.__function == "OtherHelp":
            dialog = self.CreateDialog("其他帮助", 60, 40)
            dialog.setWindowOpacity(0.94)  # 设置透明度

            label = self.GetQLabel("其他帮助：", "color:red; font-size:15pt")
            textEdit = QTextEdit()
            textEdit.setFocusPolicy(Qt.NoFocus)  # 禁止编辑
            textEdit.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
            # 显示内容编辑
            showStr = "用户点击重置软件后，所有参数会重置为默认参数，并且需要重新读入各个文件才能运行"
            textEdit.setPlainText(showStr)

            layout = QGridLayout(dialog)  # 创建栅格布局
            # 栅格布局添加控件
            layout.addWidget(label, 0, 0, 1, 1)
            layout.addWidget(textEdit, 1, 0, 1, 1)
            dialog.exec()  # 运行
        elif self.__function == "About":
            dialog = self.CreateDialog("关于", 20, 10)
            label = self.GetQLabel("石油组学软件：" + ConstValues.PsSoftwareEdition, alignment="AlignCenter")  # 创建label
            layout = QVBoxLayout(dialog)  # 创建垂直布局
            layout.addWidget(label)
            dialog.exec()

    def EditShow(self, name, explain):
        dialog = self.CreateDialog("编辑->" + name, 60, 40)
        dialog.setWindowOpacity(0.94)  # 设置透明度

        label = self.GetQLabel("菜单栏 “编辑->" + name + "” 下功能解释：", "color:red; font-size:15pt")
        textEdit = QTextEdit()
        textEdit.setFocusPolicy(Qt.NoFocus)  # 禁止编辑
        textEdit.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        # 显示内容编辑
        explain = name + ":" + explain
        taskbarExplain = "工具栏对应的“" + name + "”是运行按钮，菜单栏对应的“" + name + "”是参数设置。"
        showStr = explain + "\n\n\n" + taskbarExplain
        textEdit.setPlainText(showStr)

        layout = QGridLayout(dialog)  # 创建栅格布局
        # 栅格布局添加控件
        layout.addWidget(label, 0, 0, 1, 1)
        layout.addWidget(textEdit, 1, 0, 1, 1)
        dialog.exec()  # 运行

# 设置界面
class SetupInterface:
    def __init__(self, theme=""):
        # 全局变量初始化
        self.dataInit(theme)

    def dataInit(self, theme):
        self.MainWindowsStyle = theme
        # 扣空白所需要返回的数据，数据初值无所谓
        # 0~10000（整数）
        self.deleteBlankIntensity = None
        # 0.00~100.00（浮点数）
        self.deleteBlankPPM = None
        # 0~100（整数）
        self.deleteBlankPercentage = None

        # 生成数据库所需要返回的数据，数据初值无所谓
        self.GDBClass = None  # 数据库生成(参数)：Class类型
        # 1~100（整数）
        self.GDBCarbonRangeLow = None  # 数据库生成(参数)：carbon rage(碳数范围)最小值(包含)
        self.GDBCarbonRangeHigh = None  # 数据库生成(参数)：carbon rage(碳数范围)最大值(包含)
        # 1~30（整数）
        self.GDBDBERageLow = None  # 数据库生成(参数)：DBE rage(不饱和度范围)最小值(包含)
        self.GDBDBERageHigh = None  # 数据库生成(参数)：DBE rage(不饱和度范围)最大值(包含)
        # 50~1500(整数)
        self.GDBM_ZRageLow = None  # 数据库生成(参数)：m/z rage(质荷比范围)最小值(包含)
        self.GDBM_ZRageHigh = None  # 数据库生成(参数)：m/z rage(质荷比范围)最小值(包含)
        # 离子类型
        self.GDB_MHPostive = None  # 数据库生成(参数)：正离子，是否选择[M+H]+，True为选中
        self.GDB_MPostive = None  # 数据库生成(参数)：正离子，是否选择M+，True为选中
        self.GDB_MHNegative = None  # 数据库生成(参数)：负离子，是否选择[M-H]-，True为选中
        self.GDB_MNegative = None  # 数据库生成(参数)：负离子，是否选择M-，True为选中

        # 去同位素所需要返回的数据，数据初值无所谓
        # 0~正无穷（整数）
        self.DelIsoIntensityX = None
        # 0~100（整数）
        self.DelIso_13C2RelativeIntensity = None
        # 0.00~20.00（浮点数）
        self.DelIsoMassDeviation = None
        # 0.00~20.00（浮点数）
        self.DelIsoIsotopeMassDeviation = None
        # 1~100（整数）
        self.DelIsoIsotopeIntensityDeviation = None

        # 去同位素所需要返回的数据，数据初值无所谓
        # 0~10000（整数）
        self.PeakDisContinuityNum = None  # 第一部分
        # 0.00~100.00（浮点数）
        self.PeakDisMassDeviation = None
        # 0~30(整数)
        self.PeakDisDiscontinuityPointNum = None
        # str类型
        self.PeakDisClassIsNeed = None  # 第二部分，峰检测
        self.PeakDisClass = None

        # 去同位素所需要返回的数据，数据初值无所谓
        self.RemoveFPId = None  # 1：去同位素之后的内容，2：峰提取之后的内容
        # 0~100（整数）
        self.RemoveFPContinue_CNum = None  # 连续碳数
        # 0~100（整数）
        self.RemoveFPContinue_DBENum = None

        # 峰检测全过程所需要的数据  0~1000000(整数)
        self.PeakDivNoiseThreshold = None  # 噪音阈值
        # 0.0~100.0(浮点数)
        self.PeakDivRelIntensity = None  # # 相对强度阈值
        # 该参数决定是否需要将溶剂效应的第一个峰融合到第二个峰
        self.PeakDivNeedMerge = None
        # 该参数决定是否生成图片信息
        self.PeakDivNeedGenImage = None

        # 绘图全过程所需要的数据  1~6(整数)
        self.PlotTitleName = None  # 标题名称
        self.PlotTitleColor = None  # 标题颜色
        self.PlotXAxisName = None  # x轴名称
        self.PlotXAxisColor = None  # x轴颜色
        self.PlotYAxisName = None  # y轴名称
        self.PlotYAxisColor = None  # y轴颜色
        self.PlotHasEnter = None  # 记录是否进入过PlotSetup()函数
        self.PlotType = None  # 绘图类型
        self.PlotClassList = None  # 列表，需要绘制的类型，例子：["CH", "N1"]
        self.PlotClassItem = None  # 列表，需要绘制的类型，例子：["CH"]，对应单选钮，长度必须为1
        self.PlotDBENum = None  # 整数，记录用户选择的DBE数目
        self.PlotConfirm = None  # 用户是否确认要画图

        # 绘图模式选择设置
        # 运行模式
        # 1：去空白 --> 数据库生成 --> 搜同位素 --> 去假阳性
        # 2：去空白 --> 数据库生成 --> 搜同位素 --> 峰提取 --> 去假阳性
        # 3：去空白 --> 数据库生成 --> 搜同位素 --> 峰提取 --> 去假阳性 --> 峰检测
        # 4：数据库生成 --> 搜同位素 --> 去假阳性
        # 5：数据库生成 --> 搜同位素 --> 峰提取 --> 去假阳性
        # 6：数据库生成 --> 搜同位素 --> 峰提取 --> 去假阳性 --> 峰检测
        self.startMode = ConstValues.PsStartMode
        # 确定开始运行
        self.startModeConfirm = False

    # 设置有int校验器的QLineEdit
    def IntQLineEdit(self, low, high, text):
        # 设置校验器
        intValidator = QIntValidator()
        intValidator.setRange(low, high)
        # 创建QLineEdit
        lineEdit = QLineEdit()
        lineEdit.setValidator(intValidator)  # 设置校验器
        lineEdit.setPlaceholderText(text)  # 默认显示内容
        lineEdit.setAlignment(Qt.AlignRight)  # 对齐方式
        lineEdit.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))  # 设置字体
        return lineEdit

    # 设置有double校验器的QLineEdit
    def DoubleQLineEdit(self, low, high, decimals, text):
        # 设置校验器
        doubleValidator = QDoubleValidator()
        doubleValidator.setRange(low, high, decimals)
        doubleValidator.setNotation(QDoubleValidator.StandardNotation)  # 必须有这一句校验器设置的范围才有效
        # 创建QLineEdit
        lineEdit = QLineEdit()
        lineEdit.setValidator(doubleValidator)  # 设置校验器
        lineEdit.setPlaceholderText(text)  # 默认显示内容
        lineEdit.setAlignment(Qt.AlignRight)  # 对齐方式
        lineEdit.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))  # 设置字体
        return lineEdit

    # 设置正则表示式校验器QLineEdit
    def RegExpQLineEdit(self, reg="", text=""):
        # 设置校验器
        regExpValidator = QRegExpValidator()
        regExpValidator.setRegExp(QRegExp(reg))
        # 创建QLineEdit
        lineEdit = QLineEdit()
        if reg != "":
            lineEdit.setValidator(regExpValidator)  # 设置校验器
        if text != "":
            lineEdit.setPlaceholderText(text)  # 默认显示内容
        lineEdit.setAlignment(Qt.AlignLeft)  # 对齐方式
        lineEdit.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))  # 设置字体
        return lineEdit

    # 设置QLabel
    def GetQLabel(self, text, style="", alignment=""):
        label = QLabel()
        label.setText(text)
        label.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        if self.MainWindowsStyle != "Qdarkstyle":
            label.setStyleSheet(style)
        if alignment == "AlignCenter":
            label.setAlignment(Qt.AlignCenter)
        elif alignment == "AlignLeft":
            label.setAlignment(Qt.AlignLeft)
        elif alignment == "AlignRight":
            label.setAlignment(Qt.AlignRight)
        return label

    # 创建Dialog
    def CreateDialog(self, title, xNum, yNum):
        # 创建QDialog
        dialog = QDialog()
        dialog.setWindowTitle(title)
        dialog.setFixedSize(ConstValues.PsSetupFontSize * xNum, ConstValues.PsSetupFontSize * yNum)  # 固定窗口大小
        if ConstValues.PsIconType == 1:
            dialog.setWindowIcon(QIcon(ConstValues.PsWindowIcon))
        elif ConstValues.PsIconType == 2:
            dialog.setWindowIcon(qtawesome.icon(ConstValues.PsqtaWindowIcon, color=ConstValues.PsqtaWindowIconColor))
        # if ConstValues.PsSetupStyleEnabled:
        #     dialog.setStyleSheet(ConstValues.PsSetupStyle)
        return dialog

    #################################################################################################################
    def DeleteBlankSetup(self, parameters):
        # 扣空白设置对话框
        # 设置默认参数
        self.DeleteBlankSetDefaultParameters(parameters)

        # 创建QDialog
        self.deleteBlankDialog = self.CreateDialog("扣空白参数设置", 30, 16)

        # Intensity对话框
        deleteBlankEdit1 = self.IntQLineEdit(ConstValues.PsDeleteBlankIntensityMin, ConstValues.PsDeleteBlankIntensityMax, str(self.deleteBlankIntensity))
        deleteBlankEdit1.textChanged.connect(lambda: self.HandleTextChangedDeleteBlank("Intensity", deleteBlankEdit1))
        # PPM对话框
        deleteBlankEdit2 = self.DoubleQLineEdit(int(ConstValues.PsDeleteBlankPPMMin), int(ConstValues.PsDeleteBlankPPMMax), 2, str(self.deleteBlankPPM))
        deleteBlankEdit2.textChanged.connect(lambda: self.HandleTextChangedDeleteBlank("PPM", deleteBlankEdit2))
        # Percentage对话框
        deleteBlankEdit3 = self.IntQLineEdit(ConstValues.PsDeleteBlankPercentageMin, ConstValues.PsDeleteBlankPercentageMax, str(self.deleteBlankPercentage))
        deleteBlankEdit3.textChanged.connect(lambda: self.HandleTextChangedDeleteBlank("Percentage", deleteBlankEdit3))
        # 创建按钮
        deleteBlankButton1 = QPushButton("确定")
        deleteBlankButton1.setFixedSize(ConstValues.PsSetupFontSize * 5, ConstValues.PsSetupFontSize * 3)
        deleteBlankButton1.clicked.connect(lambda: self.HBCDeleteBlank(parameters, True))
        deleteBlankButton2 = QPushButton("退出")
        deleteBlankButton2.setFixedSize(ConstValues.PsSetupFontSize * 5, ConstValues.PsSetupFontSize * 3)
        deleteBlankButton2.clicked.connect(lambda: self.HBCDeleteBlank(parameters, False))

        # 创建栅格布局
        layout = QGridLayout(self.deleteBlankDialog)
        # 第一行内容，intensity
        layout.addWidget(self.GetQLabel("intensity(" + str(ConstValues.PsDeleteBlankIntensityMin) + "~" + str(ConstValues.PsDeleteBlankIntensityMax) + "):"), 0, 0, 1, 2)
        layout.addWidget(deleteBlankEdit1, 0, 2, 1, 2)
        # 第二行内容，ppm
        layout.addWidget(self.GetQLabel("ppm(" + str(ConstValues.PsDeleteBlankPPMMin) + "~" + str(ConstValues.PsDeleteBlankPPMMax) + "):"), 1, 0, 1, 2)
        layout.addWidget(deleteBlankEdit2, 1, 2, 1, 2)
        # 第三行内容，percentage
        layout.addWidget(self.GetQLabel("percentage(" + str(ConstValues.PsDeleteBlankPercentageMin) + "~" + str(ConstValues.PsDeleteBlankPercentageMax) + "):"), 2, 0, 1, 2)
        layout.addWidget(deleteBlankEdit3, 2, 2, 1, 2)
        # 最后一行内容，按钮行
        layout.addWidget(deleteBlankButton1, 3, 2)
        layout.addWidget(deleteBlankButton2, 3, 3)

        self.deleteBlankDialog.exec()
        # 返回值类型：list
        retList = [self.deleteBlankIntensity,
                   self.deleteBlankPPM,
                   self.deleteBlankPercentage]
        return retList

    # 设置参数为用户上次输入的值
    def DeleteBlankSetDefaultParameters(self, parameters):
        self.deleteBlankIntensity = parameters[0]
        self.deleteBlankPPM = parameters[1]
        self.deleteBlankPercentage = parameters[2]

    # 用户输入文本后，会进入这个函数处理
    def HandleTextChangedDeleteBlank(self, DBType, edit):
        if edit.text() != "":
            if DBType == "Intensity":
                self.deleteBlankIntensity = int(edit.text())
            elif DBType == "PPM":
                self.deleteBlankPPM = float(edit.text())
            elif DBType == "Percentage":
                self.deleteBlankPercentage = int(edit.text())

    # HBC：HandleButtonClicked 用户点击确认/取消后，会进入这个函数处理
    def HBCDeleteBlank(self, parameters, isOK):
        if not isOK:  # 点击取消按钮
            self.DeleteBlankSetDefaultParameters(parameters)
            self.deleteBlankDialog.close()
        else:  # 点击确认按钮
            inputState = self.DeleteBlankIsParameterValidate()
            if inputState == 1:
                self.deleteBlankDialog.close()
            elif inputState == 2:
                PromptBox().warningMessage("intensity输入不合法！")
            elif inputState == 3:
                PromptBox().warningMessage("ppm输入不合法！")
            elif inputState == 4:
                PromptBox().warningMessage("percentage输入不合法！")

    # 参数合法性检查
    def DeleteBlankIsParameterValidate(self):
        # 合法返回1，不合法返回对应的代码
        # 判断self.deleteBlankIntensity是否合法，对应代码2
        if not (ConstValues.PsDeleteBlankIntensityMin <= self.deleteBlankIntensity <= ConstValues.PsDeleteBlankIntensityMax):
            return 2
        # 判断self.deleteBlankPPM是否合法，对应代码3
        if not (ConstValues.PsDeleteBlankPPMMin <= self.deleteBlankPPM <= ConstValues.PsDeleteBlankPPMMax):
            return 3
        # 判断self.deleteBlankPercentage是否合法，对应代码4
        if not (ConstValues.PsDeleteBlankPercentageMin <= self.deleteBlankPercentage <= ConstValues.PsDeleteBlankPercentageMax):
            return 4
        # 合法
        return 1

    #################################################################################################################
    def GenerateDataBaseSetup(self, parameters):
        # 数据库生成设置对话框
        # 设置参数（上一次更改后的参数）
        self.GDBSetDefaultParameters(parameters)

        # 创建QDialog
        self.GDBDialog = self.CreateDialog("数据库生成参数设置", 52, 35)

        # Class
        GDBEdit1 = self.RegExpQLineEdit("([A-Z0-9]|,)+$", ",".join(self.GDBClass))  # 注意：list需要转为str
        GDBEdit1.textChanged.connect(lambda: self.HandleTextChangedGDB("Class", GDBEdit1))
        # carbon rage(碳数范围)：1~100（整数）
        GDBEdit2 = self.IntQLineEdit(ConstValues.PsGDBCarbonRangeMin, ConstValues.PsGDBCarbonRangeMax, str(self.GDBCarbonRangeLow))
        GDBEdit3 = self.IntQLineEdit(ConstValues.PsGDBCarbonRangeMin, ConstValues.PsGDBCarbonRangeMax, str(self.GDBCarbonRangeHigh))
        GDBEdit2.textChanged.connect(lambda: self.HandleTextChangedGDB("carbon rage low", GDBEdit2))
        GDBEdit3.textChanged.connect(lambda: self.HandleTextChangedGDB("carbon rage high", GDBEdit3))
        # DBE rage(不饱和度范围)：1~30（整数）
        GDBEdit4 = self.IntQLineEdit(ConstValues.PsGDBDBERageMin, ConstValues.PsGDBDBERageMax, str(self.GDBDBERageLow))
        GDBEdit5 = self.IntQLineEdit(ConstValues.PsGDBDBERageMin, ConstValues.PsGDBDBERageMax, str(self.GDBDBERageHigh))
        GDBEdit4.textChanged.connect(lambda: self.HandleTextChangedGDB("DBE rage low", GDBEdit4))
        GDBEdit5.textChanged.connect(lambda: self.HandleTextChangedGDB("DBE rage high", GDBEdit5))
        # m/z rage(质荷比范围)：50~1500(整数)
        GDBEdit6 = self.IntQLineEdit(ConstValues.PsGDBM_ZRageMin, ConstValues.PsGDBM_ZRageMax, str(self.GDBM_ZRageLow))
        GDBEdit7 = self.IntQLineEdit(ConstValues.PsGDBM_ZRageMin, ConstValues.PsGDBM_ZRageMax, str(self.GDBM_ZRageHigh))
        GDBEdit6.textChanged.connect(lambda: self.HandleTextChangedGDB("m/z rage low", GDBEdit6))
        GDBEdit7.textChanged.connect(lambda: self.HandleTextChangedGDB("m/z rage high", GDBEdit7))
        # 离子类型（复选按钮）
        GDBCheckBox1 = QCheckBox("[M+H]+")  # 四个复选框
        GDBCheckBox2 = QCheckBox("M+")
        self.GDBFlag12 = False
        GDBCheckBox3 = QCheckBox("[M-H]-")
        GDBCheckBox4 = QCheckBox("M-")
        self.GDBFlag34 = False
        GDBCheckBox1.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))  # 设置字体
        GDBCheckBox2.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        GDBCheckBox3.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        GDBCheckBox4.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        GDBCheckBox1.setChecked(self.GDB_MHPostive)  # 设置初始勾选
        GDBCheckBox2.setChecked(self.GDB_MPostive)
        GDBCheckBox3.setChecked(self.GDB_MHNegative)
        GDBCheckBox4.setChecked(self.GDB_MNegative)
        GDBCheckBox1.stateChanged.connect(lambda: self.GDBCheckboxState12(GDBCheckBox1, GDBCheckBox2, GDBCheckBox3, GDBCheckBox4))  # 绑定槽函数
        GDBCheckBox2.stateChanged.connect(lambda: self.GDBCheckboxState12(GDBCheckBox1, GDBCheckBox2, GDBCheckBox3, GDBCheckBox4))
        GDBCheckBox3.stateChanged.connect(lambda: self.GDBCheckboxState34(GDBCheckBox1, GDBCheckBox2, GDBCheckBox3, GDBCheckBox4))
        GDBCheckBox4.stateChanged.connect(lambda: self.GDBCheckboxState34(GDBCheckBox1, GDBCheckBox2, GDBCheckBox3, GDBCheckBox4))

        # 创建按钮
        GDBButton1 = QPushButton("确定")
        GDBButton1.setFixedSize(ConstValues.PsSetupFontSize * 5, ConstValues.PsSetupFontSize * 3)
        GDBButton1.clicked.connect(lambda : self.HBCGDB(parameters, True))
        GDBButton2 = QPushButton("退出")
        GDBButton2.setFixedSize(ConstValues.PsSetupFontSize * 5, ConstValues.PsSetupFontSize * 3)
        GDBButton2.clicked.connect(lambda : self.HBCGDB(parameters, False))

        # 创建栅格布局
        layout = QGridLayout(self.GDBDialog)
        # layout.setSpacing(10)
        # 第一行内容，Class
        layout.addWidget(self.GetQLabel("class："), 0, 0)
        layout.addWidget(GDBEdit1, 0, 1, 1, 6)  # 第0行第1列，占1行3列
        # 第二行内容，carbon rage
        layout.addWidget(self.GetQLabel("carbon rage(min)" + str(ConstValues.PsGDBCarbonRangeMin) + "~" + str(ConstValues.PsGDBCarbonRangeMax) + ":"), 1, 0, 1, 2)
        layout.addWidget(GDBEdit2, 1, 2)
        layout.addWidget(self.GetQLabel("carbon rage(max)" + str(ConstValues.PsGDBCarbonRangeMin) + "~" + str(ConstValues.PsGDBCarbonRangeMax) + ":"), 1, 4, 1, 2)
        layout.addWidget(GDBEdit3, 1, 6)
        # 第三行内容，DBE rage
        layout.addWidget(self.GetQLabel("DBE rage(min)" + str(ConstValues.PsGDBDBERageMin) + "~" + str(ConstValues.PsGDBDBERageMax) + ":"), 2, 0, 1, 2)
        layout.addWidget(GDBEdit4, 2, 2)
        layout.addWidget(self.GetQLabel("DBE rage(max)" + str(ConstValues.PsGDBDBERageMin) + "~" + str(ConstValues.PsGDBDBERageMax) + ":"), 2, 4, 1, 2)
        layout.addWidget(GDBEdit5, 2, 6)
        # 第四行内容，m/z rage
        layout.addWidget(self.GetQLabel("m/z rage(min)" + str(ConstValues.PsGDBM_ZRageMin) + "~" + str(ConstValues.PsGDBM_ZRageMax) + ":"), 3, 0, 1, 2)
        layout.addWidget(GDBEdit6, 3, 2)
        layout.addWidget(self.GetQLabel("m/z rage(max)" + str(ConstValues.PsGDBM_ZRageMin) + "~" + str(ConstValues.PsGDBM_ZRageMax) + ":"), 3, 4, 1, 2)
        layout.addWidget(GDBEdit7, 3, 6)
        # 第五行内容，离子类型
        layout.addWidget(self.GetQLabel("选择离子类型："), 4, 0)
        layout.addWidget(GDBCheckBox1, 4, 2)
        layout.addWidget(GDBCheckBox2, 4, 3)
        layout.addWidget(GDBCheckBox3, 4, 5)
        layout.addWidget(GDBCheckBox4, 4, 6)
        # 最后一行内容，按钮行
        layout.addWidget(GDBButton1, 6, 5)
        layout.addWidget(GDBButton2, 6, 6)

        self.GDBDialog.exec()
        # 返回值类型：list
        retList = [self.GDBClass,
                   self.GDBCarbonRangeLow,
                   self.GDBCarbonRangeHigh,
                   self.GDBDBERageLow,
                   self.GDBDBERageHigh,
                   self.GDBM_ZRageLow,
                   self.GDBM_ZRageHigh,
                   self.GDB_MHPostive,
                   self.GDB_MPostive,
                   self.GDB_MHNegative,
                   self.GDB_MNegative]
        return retList

    # 设置参数为用户上次输入的值
    def GDBSetDefaultParameters(self, parameters):
        # 设置参数
        self.GDBClass = parameters[0]  # 数据库生成(参数)：Class类型
        # 1~100（整数）
        self.GDBCarbonRangeLow = parameters[1]  # 数据库生成(参数)：carbon rage(碳数范围)最小值(包含)
        self.GDBCarbonRangeHigh = parameters[2]  # 数据库生成(参数)：carbon rage(碳数范围)最大值(包含)
        # 1~30（整数）
        self.GDBDBERageLow = parameters[3]  # 数据库生成(参数)：DBE rage(不饱和度范围)最小值(包含)
        self.GDBDBERageHigh = parameters[4]  # 数据库生成(参数)：DBE rage(不饱和度范围)最大值(包含)
        # 50~1500(整数)
        self.GDBM_ZRageLow = parameters[5]  # 数据库生成(参数)：m/z rage(质荷比范围)最小值(包含)
        self.GDBM_ZRageHigh = parameters[6]  # 数据库生成(参数)：m/z rage(质荷比范围)最小值(包含)
        # 离子类型
        self.GDB_MHPostive = parameters[7]  # 数据库生成(参数)：正离子，是否选择[M+H]+，True为选中
        self.GDB_MPostive = parameters[8]  # 数据库生成(参数)：正离子，是否选择M+，True为选中
        self.GDB_MHNegative = parameters[9]  # 数据库生成(参数)：负离子，是否选择[M-H]-，True为选中
        self.GDB_MNegative = parameters[10]  # 数据库生成(参数)：负离子，是否选择M-，True为选中

    # GDBEdit1~GDBEdit7文字改变会进入该函数
    def HandleTextChangedGDB(self, GDBType, edit):
        if edit.text() != "":
            if GDBType == "Class":
                self.GDBClass = edit.text().split(",")  # 转为list
            elif GDBType == "carbon rage low":
                self.GDBCarbonRangeLow = int(edit.text())
            elif GDBType == "carbon rage high":
                self.GDBCarbonRangeHigh = int(edit.text())
            elif GDBType == "DBE rage low":
                self.GDBDBERageLow = int(edit.text())
            elif GDBType == "DBE rage high":
                self.GDBDBERageHigh = int(edit.text())
            elif GDBType == "m/z rage low":
                self.GDBM_ZRageLow = int(edit.text())
            elif GDBType == "m/z rage high":
                self.GDBM_ZRageHigh = int(edit.text())

    # 当GDBCheckBox1，GDBCheckBox2状态改变会进入该函数
    def GDBCheckboxState12(self, cb1, cb2, cb3, cb4):
        """
        :param cb1: 第一个复选框
        :param cb2: 第二个复选框
        :return:
        """
        # 3种状态：未选中：0，半选中：1， 选中：2
        # 避免GDBCheckboxState34在调用 setChecked 进入该函数
        if self.GDBFlag34:
            return
        self.GDBFlag12 = True
        # 合法性检查
        if cb3.isChecked() or cb4.isChecked():
            cb3.setChecked(False)
            cb4.setChecked(False)
        # 更新变量的值
        self.GDB_MHPostive = cb1.isChecked()  # 数据库生成(参数)：正离子，是否选择[M+H]+，True为选中
        self.GDB_MPostive = cb2.isChecked()  # 数据库生成(参数)：正离子，是否选择M+，True为选中
        self.GDB_MHNegative = cb3.isChecked()  # 数据库生成(参数)：负离子，是否选择[M-H]-，True为选中
        self.GDB_MNegative = cb4.isChecked()  # 数据库生成(参数)：负离子，是否选择M-，True为选中
        self.GDBFlag12 = False

    # 当GDBCheckBox3，GDBCheckBox4状态改变会进入该函数
    def GDBCheckboxState34(self, cb1, cb2, cb3, cb4):
        """
        :param cb3: 第三个复选框
        :param cb4: 第四个复选框
        :return:
        """
        # 3种状态：未选中：0，半选中：1， 选中：2
        # 避免GDBCheckboxState12在调用 setChecked 进入该函数
        if self.GDBFlag12:
            return
        self.GDBFlag34 = True
        # 合法性检查
        if cb1.isChecked() or cb2.isChecked():
            cb1.setChecked(False)
            cb2.setChecked(False)
        # 更新变量的值
        self.GDB_MHPostive = cb1.isChecked()  # 数据库生成(参数)：正离子，是否选择[M+H]+，True为选中
        self.GDB_MPostive = cb2.isChecked()  # 数据库生成(参数)：正离子，是否选择M+，True为选中
        self.GDB_MHNegative = cb3.isChecked()  # 数据库生成(参数)：负离子，是否选择[M-H]-，True为选中
        self.GDB_MNegative = cb4.isChecked()  # 数据库生成(参数)：负离子，是否选择M-，True为选中
        self.GDBFlag34 = False

    # HBC：HandleButtonClicked 用户点击确认/取消后，会进入这个函数处理
    def HBCGDB(self, parameters, isOK):
        if not isOK:  # 点击取消按钮
            self.GDBSetDefaultParameters(parameters)
            self.GDBDialog.close()
        else:  # 点击确认按钮
            inputState = self.GDBIsParameterValidate()
            if inputState == 1:
                self.GDBDialog.close()
            elif inputState == 2:
                PromptBox().warningMessage("Class输入不合法！")
            elif inputState == 3:
                PromptBox().warningMessage("carbon rage输入不合法！")
            elif inputState == 4:
                PromptBox().warningMessage("DBE rage输入不合法！")
            elif inputState == 5:
                PromptBox().warningMessage("m/z rage输入不合法！")

    # 参数合法性检查
    def GDBIsParameterValidate(self):
        # 合法返回1，不合法返回对应的代码

        # 判断self.GDBClass是否合法，对应代码2
        for item in self.GDBClass:
            if item == "CH":
                continue
            for i in range(len(item)):
                if i % 2 == 0:  # 应该是字母
                    if not ("A" <= item[i] <= "Z"):
                        return 2
                else:  # 应该是数字字符
                    if not ("0" <= item[i] <= "9"):
                        return 2
        # 判断self.GDBCarbonRangeLow，self.GDBCarbonRangeHigh是否合法，对应代码3
        if (self.GDBCarbonRangeLow > self.GDBCarbonRangeHigh) or \
                (not (ConstValues.PsGDBCarbonRangeMin <= self.GDBCarbonRangeLow <= ConstValues.PsGDBCarbonRangeMax)) or \
                (not (ConstValues.PsGDBCarbonRangeMin <= self.GDBCarbonRangeHigh <= ConstValues.PsGDBCarbonRangeMax)):
            return 3
        # 判断self.GDBDBERageLow，self.GDBDBERageHigh是否合法，对应代码4
        if self.GDBDBERageLow > self.GDBDBERageHigh or \
                (not (ConstValues.PsGDBDBERageMin <= self.GDBDBERageLow <= ConstValues.PsGDBDBERageMax)) or \
                (not (ConstValues.PsGDBDBERageMin <= self.GDBDBERageHigh <= ConstValues.PsGDBDBERageMax)):
            return 4
        # 判断self.GDBM_ZRageLow，self.GDBM_ZRageHigh是否合法，对应代码5
        if self.GDBM_ZRageLow > self.GDBM_ZRageHigh or \
                (not (ConstValues.PsGDBM_ZRageMin <= self.GDBM_ZRageLow <= ConstValues.PsGDBM_ZRageMax)) or \
                (not (ConstValues.PsGDBM_ZRageMin <= self.GDBM_ZRageHigh <= ConstValues.PsGDBM_ZRageMax)):
            return 5
        # 合法
        return 1

    #################################################################################################################
    def DeleteIsotopeSetup(self, parameters):
        # 去同位素设置对话框
        # 设置默认参数
        self.DeleteIsotopeSetDefaultParameters(parameters)

        # 创建QDialog
        self.deleteIsotopeDialog = self.CreateDialog("去同位素参数设置", 40, 25)

        # IntensityX对话框
        deleteIsotopeEdit1 = self.IntQLineEdit(ConstValues.PsDelIsoIntensityXMin, ConstValues.PsDelIsoIntensityXMax, str(self.DelIsoIntensityX))
        deleteIsotopeEdit1.textChanged.connect(lambda: self.HandleTextChangedDeleteIsotope("IntensityX", deleteIsotopeEdit1))
        # 13C2RelativeIntensity对话框
        deleteIsotopeEdit2 = self.IntQLineEdit(ConstValues.PsDelIso_13C2RelativeIntensityMin, ConstValues.PsDelIso_13C2RelativeIntensityMax, str(self.DelIso_13C2RelativeIntensity))
        deleteIsotopeEdit2.textChanged.connect(lambda: self.HandleTextChangedDeleteIsotope("13C2RelativeIntensity", deleteIsotopeEdit2))
        # Mass Deviation对话框
        deleteIsotopeEdit3 = self.DoubleQLineEdit(int(ConstValues.PsDelIsoMassDeviationMin), int(ConstValues.PsDelIsoMassDeviationMax), 2, str(self.DelIsoMassDeviation))
        deleteIsotopeEdit3.textChanged.connect(lambda: self.HandleTextChangedDeleteIsotope("Mass Deviation", deleteIsotopeEdit3))
        # Isotope Mass Deviation对话框
        deleteIsotopeEdit4 = self.DoubleQLineEdit(int(ConstValues.PsDelIsoIsotopeMassDeviationMin), int(ConstValues.PsDelIsoIsotopeMassDeviationMax), 2, str(self.DelIsoIsotopeMassDeviation))
        deleteIsotopeEdit4.textChanged.connect(lambda: self.HandleTextChangedDeleteIsotope("Isotope Mass Deviation", deleteIsotopeEdit4))
        # Isotope Intensity Deviation对话框
        deleteIsotopeEdit5 = self.IntQLineEdit(ConstValues.PsDelIsoIsotopeIntensityDeviationMin, ConstValues.PsDelIsoIsotopeIntensityDeviationMax, str(self.DelIsoIsotopeIntensityDeviation))
        deleteIsotopeEdit5.textChanged.connect(lambda: self.HandleTextChangedDeleteIsotope("Isotope Intensity Deviation", deleteIsotopeEdit5))

        # 创建按钮
        deleteIsotopeButton1 = QPushButton("确定")
        deleteIsotopeButton1.setFixedSize(ConstValues.PsSetupFontSize * 5, ConstValues.PsSetupFontSize * 3)
        deleteIsotopeButton1.clicked.connect(lambda: self.HBCDeleteIsotope(parameters, True))
        deleteIsotopeButton2 = QPushButton("退出")
        deleteIsotopeButton2.setFixedSize(ConstValues.PsSetupFontSize * 5, ConstValues.PsSetupFontSize * 3)
        deleteIsotopeButton2.clicked.connect(lambda: self.HBCDeleteIsotope(parameters, False))

        # 创建栅格布局
        layout = QGridLayout(self.deleteIsotopeDialog)
        # # 第一行内容，IntensityX
        # layout.addWidget(self.GetQLabel("IntensityX(" + str(ConstValues.PsDelIsoIntensityXMin) + "~" + ConstValues.PsDelIsoIntensityXMaxStr + ") :"), 0, 0, 1, 4)
        # layout.addWidget(deleteIsotopeEdit1, 0, 4, 1, 2)
        # # 第二行内容，13C2RelativeIntensity
        # layout.addWidget(self.GetQLabel("13C2RelativeIntensity(" + str(ConstValues.PsDelIso_13C2RelativeIntensityMin) + "~" + str(ConstValues.PsDelIso_13C2RelativeIntensityMax) + "):"), 1, 0, 1, 4)
        # layout.addWidget(deleteIsotopeEdit2, 1, 4, 1, 2)
        # 第三行内容，Mass Deviation
        layout.addWidget(self.GetQLabel("Mass Deviation(" + str(ConstValues.PsDelIsoMassDeviationMin) + "~" + str(ConstValues.PsDelIsoMassDeviationMax) + ") :"), 2, 0, 1, 4)
        layout.addWidget(deleteIsotopeEdit3, 2, 4, 1, 2)
        # 第三行内容，Isotope Mass Deviation
        layout.addWidget(self.GetQLabel("Isotope Mass Deviation(" + str(ConstValues.PsDelIsoIsotopeMassDeviationMin) + "~" + str(ConstValues.PsDelIsoIsotopeMassDeviationMax) + ") :"), 3, 0, 1, 4)
        layout.addWidget(deleteIsotopeEdit4, 3, 4, 1, 2)
        # 第三行内容，Isotope Intensity Deviation
        layout.addWidget(self.GetQLabel("Isotope Intensity Deviation(" + str(ConstValues.PsDelIsoIsotopeIntensityDeviationMin) + "~" + str(ConstValues.PsDelIsoIsotopeIntensityDeviationMax) + ") :"), 4, 0, 1, 4)
        layout.addWidget(deleteIsotopeEdit5, 4, 4, 1, 2)
        # 最后一行内容，按钮行
        layout.addWidget(deleteIsotopeButton1, 5, 4)
        layout.addWidget(deleteIsotopeButton2, 5, 5)

        self.deleteIsotopeDialog.exec()
        # 返回值类型：list
        retList = [self.DelIsoIntensityX,  # 格式：整数
                   self.DelIso_13C2RelativeIntensity,  # 格式：整数
                   self.DelIsoMassDeviation,  # 格式：浮点数
                   self.DelIsoIsotopeMassDeviation,  # 格式：浮点数
                   self.DelIsoIsotopeIntensityDeviation  # 格式：整数
                  ]
        return retList

    # 设置参数为用户上次输入的值
    def DeleteIsotopeSetDefaultParameters(self, parameters):
        # 设置参数
        # 0~正无穷（整数）
        self.DelIsoIntensityX = parameters[0]
        # 0~100（整数）
        self.DelIso_13C2RelativeIntensity = parameters[1]
        # 0.00~20.00（浮点数）
        self.DelIsoMassDeviation = parameters[2]
        # 0.00~20.00（浮点数）
        self.DelIsoIsotopeMassDeviation = parameters[3]
        # 0~100（整数）
        self.DelIsoIsotopeIntensityDeviation = parameters[4]

    # 用户输入文本后，会进入这个函数处理
    def HandleTextChangedDeleteIsotope(self, DBType, edit):
        if edit.text() != "":
            if DBType == "IntensityX":
                self.DelIsoIntensityX = int(edit.text())
            elif DBType == "13C2RelativeIntensity":
                self.DelIso_13C2RelativeIntensity = int(edit.text())
            elif DBType == "Mass Deviation":
                self.DelIsoMassDeviation = float(edit.text())
            elif DBType == "Isotope Mass Deviation":
                self.DelIsoIsotopeMassDeviation = float(edit.text())
            elif DBType == "Isotope Intensity Deviation":
                self.DelIsoIsotopeIntensityDeviation = int(edit.text())

    # HBC：HandleButtonClicked 用户点击确认/取消后，会进入这个函数处理
    def HBCDeleteIsotope(self, parameters, isOK):
        if not isOK:  # 点击取消按钮
            self.DeleteIsotopeSetDefaultParameters(parameters)
            self.deleteIsotopeDialog.close()
        else:  # 点击确认按钮
            inputState = self.DeleteIsotopeIsParameterValidate()
            if inputState == 1:
                self.deleteIsotopeDialog.close()
            elif inputState == 2:
                PromptBox().warningMessage("IntensityX输入不合法！")
            elif inputState == 3:
                PromptBox().warningMessage("13C2RelativeIntensity输入不合法！")
            elif inputState == 4:
                PromptBox().warningMessage("Mass Deviation输入不合法！")
            elif inputState == 5:
                PromptBox().warningMessage("Isotope Mass Deviation输入不合法！")
            elif inputState == 6:
                PromptBox().warningMessage("Isotope Intensity Deviation输入不合法！")

    # 参数合法性检查
    def DeleteIsotopeIsParameterValidate(self):
        # 合法返回1，不合法返回对应的代码
        # 判断self.DelIsoIntensityX是否合法，对应代码2
        if not (ConstValues.PsDelIsoIntensityXMin <= self.DelIsoIntensityX <= ConstValues.PsDelIsoIntensityXMax):
            return 2
        # 判断self.DelIso_13C2RelativeIntensity是否合法，对应代码3
        if not (ConstValues.PsDelIso_13C2RelativeIntensityMin <= self.DelIso_13C2RelativeIntensity <= ConstValues.PsDelIso_13C2RelativeIntensityMax):
            return 3
        # 判断self.DelIsoMassDeviation是否合法，对应代码4
        if not (ConstValues.PsDelIsoMassDeviationMin <= self.DelIsoMassDeviation <= ConstValues.PsDelIsoMassDeviationMax):
            return 4
        # 判断self.DelIsoIsotopeMassDeviation是否合法，对应代码5
        if not (ConstValues.PsDelIsoIsotopeMassDeviationMin <= self.DelIsoIsotopeMassDeviation <= ConstValues.PsDelIsoIsotopeMassDeviationMax):
            return 5
        # 判断self.DelIsoIsotopeIntensityDeviation是否合法，对应代码6
        if not (ConstValues.PsDelIsoIsotopeIntensityDeviationMin <= self.DelIsoIsotopeIntensityDeviation <= ConstValues.PsDelIsoIsotopeIntensityDeviationMax):
            return 6
        # 合法
        return 1

    #################################################################################################################
    def PeakDistinguishSetup(self, parameters):
        # 峰提取设置对话框
        # 设置默认参数
        self.PeakDistinguishDefaultParameters(parameters)

        # 创建QDialog
        self.peakDistinguishDialog = self.CreateDialog("峰提取参数设置", 40, 25)

        # PeakDisContinuityNum对话框
        peakDistinguishEdit1 = self.IntQLineEdit(ConstValues.PsPeakDisContinuityNumMin, ConstValues.PsPeakDisContinuityNumMax, str(self.PeakDisContinuityNum))
        peakDistinguishEdit1.textChanged.connect(lambda: self.HandleTextChangedPeakDistinguish("Continuity Num", peakDistinguishEdit1))
        # Mass Deviation对话框
        peakDistinguishEdit2 = self.DoubleQLineEdit(int(ConstValues.PsPeakDisMassDeviationMin), int(ConstValues.PsPeakDisMassDeviationMax), 2, str(self.PeakDisMassDeviation))
        peakDistinguishEdit2.textChanged.connect(lambda: self.HandleTextChangedPeakDistinguish("Mass Deviation", peakDistinguishEdit2))
        # PeakDisDiscontinuityPointNum对话框
        peakDistinguishEdit3 = self.IntQLineEdit(ConstValues.PsPeakDisDiscontinuityPointNumMin, ConstValues.PsPeakDisDiscontinuityPointNumMax, str(self.PeakDisDiscontinuityPointNum))
        peakDistinguishEdit3.textChanged.connect(lambda: self.HandleTextChangedPeakDistinguish("Discontinuity Num", peakDistinguishEdit3))
        # 创建单选按钮，以确定第二部分是否运行，即下面两个按钮是否有效
        peakDistinguishQRadioButton = QRadioButton("使能")
        peakDistinguishQRadioButton.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        if self.PeakDisClassIsNeed:
            peakDistinguishQRadioButton.setChecked(True)
        else:
            peakDistinguishQRadioButton.setChecked(False)
        peakDistinguishQRadioButton.toggled.connect(lambda: self.peakDistinguishQRadioButton(peakDistinguishQRadioButton))
        # Class
        self.peakDistinguishEdit4 = self.RegExpQLineEdit("([A-Z0-9]|,)+$", ",".join(self.PeakDisClass))  # 注意：list需要转为str
        self.peakDistinguishEdit4.textChanged.connect(lambda: self.HandleTextChangedPeakDistinguish("Class", self.peakDistinguishEdit4))

        # 创建按钮
        peakDistinguishButton1 = QPushButton("确定")
        peakDistinguishButton1.setFixedSize(ConstValues.PsSetupFontSize * 5, ConstValues.PsSetupFontSize * 3)
        peakDistinguishButton1.clicked.connect(lambda: self.HBCPeakDistinguish(parameters, True))
        peakDistinguishButton2 = QPushButton("退出")
        peakDistinguishButton2.setFixedSize(ConstValues.PsSetupFontSize * 5, ConstValues.PsSetupFontSize * 3)
        peakDistinguishButton2.clicked.connect(lambda: self.HBCPeakDistinguish(parameters, False))

        # 创建栅格布局
        layout = QGridLayout(self.peakDistinguishDialog)
        layout.setContentsMargins(10, 10, 10, 10)
        # 第一行内容，Continuity Num
        layout.addWidget(self.GetQLabel("Continuity Num(" + str(ConstValues.PsPeakDisContinuityNumMin) + "~" + str(ConstValues.PsPeakDisContinuityNumMax) + ") :"), 0, 0, 1, 3)
        layout.addWidget(peakDistinguishEdit1, 0, 3, 1, 3)
        # 第二行内容，Mass Deviation
        layout.addWidget(self.GetQLabel("Mass Deviation(" + str(ConstValues.PsPeakDisMassDeviationMin) + "~" + str(ConstValues.PsPeakDisMassDeviationMax) + "):"), 1, 0, 1, 3)
        layout.addWidget(peakDistinguishEdit2, 1, 3, 1, 3)
        # 第三行内容，Discontinuity Num
        layout.addWidget(self.GetQLabel("Discontinuity Num(" + str(ConstValues.PsPeakDisDiscontinuityPointNumMin) + "~" + str(ConstValues.PsPeakDisDiscontinuityPointNumMax) + ") :"), 2, 0, 1, 3)
        layout.addWidget(peakDistinguishEdit3, 2, 3, 1, 3)
        # 第四行内容，单选按钮
        layout.addWidget(self.GetQLabel("峰检测 ： "), 3, 0, 1, 3)
        layout.addWidget(peakDistinguishQRadioButton, 3, 3, 1, 3)
        # 第五行内容，Class
        layout.addWidget(self.GetQLabel("Class(需要峰检测的类型) : "), 4, 0, 1, 2)
        layout.addWidget(self.peakDistinguishEdit4, 4, 2, 1, 4)
        if not self.PeakDisClassIsNeed:
            self.peakDistinguishEdit4.setEnabled(False)

        # 最后一行内容，按钮行
        layout.addWidget(peakDistinguishButton1, 6, 4)
        layout.addWidget(peakDistinguishButton2, 6, 5)

        self.peakDistinguishDialog.exec()
        # 返回值类型：list
        retList = [self.PeakDisContinuityNum,  # 格式：整数
                   self.PeakDisMassDeviation,  # 格式：浮点数
                   self.PeakDisDiscontinuityPointNum,
                   self.PeakDisClassIsNeed,  # 第二部分
                   self.PeakDisClass,
                  ]
        return retList

    # 设置参数为用户上次输入的值
    def PeakDistinguishDefaultParameters(self, parameters):
        # 设置参数
        # 0~10000（整数）
        self.PeakDisContinuityNum = parameters[0]
        # 0.00~100.00（浮点数）
        self.PeakDisMassDeviation = parameters[1]
        # 0~30(整数)
        self.PeakDisDiscontinuityPointNum = parameters[2]
        # str类型
        self.PeakDisClassIsNeed = parameters[3]  # 第二部分，峰检测
        self.PeakDisClass = parameters[4]

    # 用户输入文本后，会进入这个函数处理
    def HandleTextChangedPeakDistinguish(self, DBType, edit):
        if edit.text() != "":
            if DBType == "Continuity Num":
                self.PeakDisContinuityNum = int(edit.text())
            elif DBType == "Mass Deviation":
                self.PeakDisMassDeviation = float(edit.text())
            elif DBType == "Discontinuity Num":
                self.PeakDisDiscontinuityPointNum = int(edit.text())
            elif DBType == "Class":
                self.PeakDisClass = edit.text().split(",")  # 转为list

    # HBC：HandleButtonClicked 用户点击确认/取消后，会进入这个函数处理
    def HBCPeakDistinguish(self, parameters, isOK):
        if not isOK:  # 点击取消按钮
            self.PeakDistinguishDefaultParameters(parameters)
            self.peakDistinguishDialog.close()
        else:  # 点击确认按钮
            inputState = self.PeakDistinguishIsParameterValidate()
            if inputState == 1:
                self.peakDistinguishDialog.close()
            elif inputState == 2:
                PromptBox().warningMessage("Continuity Num输入不合法！")
            elif inputState == 3:
                PromptBox().warningMessage("Mass Deviation输入不合法！")
            elif inputState == 4:
                PromptBox().warningMessage("Discontinuity Num输入不合法！")
            elif inputState == 5:
                PromptBox().warningMessage("Class输入不合法！")
            elif inputState == 6:
                PromptBox().warningMessage("ScanPoints输入不合法！")

    # 单选按钮
    def peakDistinguishQRadioButton(self, radioButton):
        if radioButton.isChecked():
            self.PeakDisClassIsNeed = True
            self.peakDistinguishEdit4.setEnabled(True)
        else:
            self.PeakDisClassIsNeed = False
            self.peakDistinguishEdit4.setEnabled(False)

    # 参数合法性检查
    def PeakDistinguishIsParameterValidate(self):
        # 合法返回1，不合法返回对应的代码
        # 判断self.PeakDisContinuityNum是否合法，对应代码2
        if not (ConstValues.PsPeakDisContinuityNumMin <= self.PeakDisContinuityNum <= ConstValues.PsPeakDisContinuityNumMax):
            return 2
        # 判断self.PeakDisMassDeviation是否合法，对应代码3
        if not (ConstValues.PsPeakDisMassDeviationMin <= self.PeakDisMassDeviation <= ConstValues.PsPeakDisMassDeviationMax):
            return 3
        # 判断self.PeakDisDiscontinuityPointNum是否合法，对应代码4
        if not (ConstValues.PsPeakDisDiscontinuityPointNumMin <= self.PeakDisDiscontinuityPointNum <= ConstValues.PsPeakDisDiscontinuityPointNumMax):
            return 4
        # 判断self.PeakDisClass是否合法，对应代码5
        for item in self.PeakDisClass:
            if item == "CH":
                continue
            for i in range(len(item)):
                if i % 2 == 0:  # 应该是字母
                    if not ("A" <= item[i] <= "Z"):
                        return 5
                else:  # 应该是数字字符
                    if not ("0" <= item[i] <= "9"):
                        return 5
        # 合法
        return 1

    #################################################################################################################
    def RemoveFalsePositiveSetup(self, parameters):
        # 去假阳性设置对话框
        # 设置默认参数
        self.RemoveFalsePositiveDefaultParameters(parameters)

        # 创建QDialog
        self.RemoveFPDialog = self.CreateDialog("去假阳性参数设置", 45, 20)

        # PsRemoveFPId二选一按钮
        RemoveFPQRadioButton1 = QRadioButton("去同位素后的文件")
        RemoveFPQRadioButton1.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        RemoveFPQRadioButton1.toggled.connect(lambda: self.RemoveFalsePositiveQRadioButton(RemoveFPQRadioButton1))
        RemoveFPQRadioButton2 = QRadioButton("峰提取后的文件")
        RemoveFPQRadioButton2.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        RemoveFPQRadioButton2.toggled.connect(lambda: self.RemoveFalsePositiveQRadioButton(RemoveFPQRadioButton2))
        if self.RemoveFPId == 1:
            RemoveFPQRadioButton1.setChecked(True)
            RemoveFPQRadioButton2.setChecked(False)
        elif self.RemoveFPId == 2:
            RemoveFPQRadioButton1.setChecked(False)
            RemoveFPQRadioButton2.setChecked(True)
        # RemoveFPContinue_CNum对话框
        RemoveFPEdit1 = self.IntQLineEdit(ConstValues.PsRemoveFPContinue_CNumMin, ConstValues.PsRemoveFPContinue_CNumMax, str(self.RemoveFPContinue_CNum))
        RemoveFPEdit1.textChanged.connect(lambda: self.HandleTextChangedRemoveFalsePositive("Continuity C Num", RemoveFPEdit1))
        # RemoveFPContinue_DBENum对话框
        RemoveFPEdit2 = self.IntQLineEdit(ConstValues.PsRemoveFPContinue_DBENumMin, ConstValues.PsRemoveFPContinue_DBENumMax, str(self.RemoveFPContinue_DBENum))
        RemoveFPEdit2.textChanged.connect(lambda: self.HandleTextChangedRemoveFalsePositive("Continuity DBE Num", RemoveFPEdit2))

        # 创建按钮
        peakDistinguishButton1 = QPushButton("确定")
        peakDistinguishButton1.setFixedSize(ConstValues.PsSetupFontSize * 5, ConstValues.PsSetupFontSize * 3)
        peakDistinguishButton1.clicked.connect(lambda: self.HBCRemoveFalsePositive(parameters, True))
        peakDistinguishButton2 = QPushButton("退出")
        peakDistinguishButton2.setFixedSize(ConstValues.PsSetupFontSize * 5, ConstValues.PsSetupFontSize * 3)
        peakDistinguishButton2.clicked.connect(lambda: self.HBCRemoveFalsePositive(parameters, False))

        # 创建栅格布局
        layout = QGridLayout(self.RemoveFPDialog)
        # 第一行内容，PsRemoveFPId二选一按钮
        layout.addWidget(self.GetQLabel("去假阳性文件 ： "), 0, 0, 1, 2)
        layout.addWidget(RemoveFPQRadioButton1, 0, 2, 1, 2)
        layout.addWidget(RemoveFPQRadioButton2, 0, 4, 1, 2)
        # 第二行内容，Continuity C Num
        layout.addWidget(self.GetQLabel("Continuity C Num(" + str(ConstValues.PsRemoveFPContinue_CNumMin) + "~" + str(ConstValues.PsRemoveFPContinue_CNumMax) + "):"), 1, 0, 1, 3)
        layout.addWidget(RemoveFPEdit1, 1, 3, 1, 3)
        # 第三行内容，Continuity DBE Num
        layout.addWidget(self.GetQLabel("Continuity DBE Num(" + str(ConstValues.PsRemoveFPContinue_DBENumMin) + "~" + str(ConstValues.PsRemoveFPContinue_DBENumMax) + ") :"), 2, 0, 1, 3)
        layout.addWidget(RemoveFPEdit2, 2, 3, 1, 3)
        # 最后一行内容，按钮行
        layout.addWidget(peakDistinguishButton1, 3, 4)
        layout.addWidget(peakDistinguishButton2, 3, 5)

        self.RemoveFPDialog.exec()
        # 返回值类型：list
        retList = [self.RemoveFPId,  # 决定选择哪一个文件 1：self.DelIsoResult 或者 2：self.PeakDisResult
                   self.RemoveFPContinue_CNum,
                   self.RemoveFPContinue_DBENum
                  ]
        return retList

    # 设置参数为用户上次输入的值
    def RemoveFalsePositiveDefaultParameters(self, parameters):
        # 设置参数
        # [1,2]
        self.RemoveFPId = parameters[0]
        # 1~100(整数)
        self.RemoveFPContinue_CNum = parameters[1]
        # 1~100(整数)
        self.RemoveFPContinue_DBENum = parameters[2]

    # 用户输入文本后，会进入这个函数处理
    def HandleTextChangedRemoveFalsePositive(self, DBType, edit):
        if edit.text() != "":
            if DBType == "Continuity C Num":
                self.RemoveFPContinue_CNum = int(edit.text())
            elif DBType == "Continuity DBE Num":
                self.RemoveFPContinue_DBENum = int(edit.text())

    # HBC：HandleButtonClicked 用户点击确认/取消后，会进入这个函数处理
    def HBCRemoveFalsePositive(self, parameters, isOK):
        if not isOK:  # 点击取消按钮
            self.RemoveFalsePositiveDefaultParameters(parameters)
            self.RemoveFPDialog.close()
        else:  # 点击确认按钮
            inputState = self.RemoveFalsePositiveIsParameterValidate()
            if inputState == 1:
                self.RemoveFPDialog.close()
            elif inputState == 2:
                PromptBox().warningMessage("Continuity C Num输入不合法！")
            elif inputState == 3:
                PromptBox().warningMessage("Continuity DBE Num输入不合法！")

    # 单选按钮
    def RemoveFalsePositiveQRadioButton(self, radioButton):
        if radioButton.text() == "去同位素后的文件":
            if radioButton.isChecked():
                self.RemoveFPId = 1
            else:
                self.RemoveFPId = 2
        else:
            if radioButton.isChecked():
                self.RemoveFPId = 2
            else:
                self.RemoveFPId = 1

    # 参数合法性检查
    def RemoveFalsePositiveIsParameterValidate(self):
        # 合法返回1，不合法返回对应的代码
        # 判断self.RemoveFPContinue_CNum 是否合法，对应代码2
        if not (ConstValues.PsRemoveFPContinue_CNumMin <= self.RemoveFPContinue_CNum <= ConstValues.PsRemoveFPContinue_CNumMax):
            return 2
        # 判断self.RemoveFPContinue_DBENum 是否合法，对应代码3
        if not (ConstValues.PsRemoveFPContinue_DBENumMin <= self.RemoveFPContinue_DBENum <= ConstValues.PsRemoveFPContinue_DBENumMax):
            return 3
        # 合法
        return 1

    #################################################################################################################
    def PeakDivisionSetup(self, parameters):
        # 峰检测设置对话框，设置默认参数
        self.PeakDivisionDefaultParameters(parameters)

        # 创建QDialog
        self.PeakDivDialog = self.CreateDialog("峰检测参数设置", 35, 20)

        # PeakDivNoiseThreshold 对话框
        PeakDivEdit1 = self.IntQLineEdit(ConstValues.PsPeakDivNoiseThresholdMin, ConstValues.PsPeakDivNoiseThresholdMax, str(self.PeakDivNoiseThreshold))
        PeakDivEdit1.textChanged.connect(lambda: self.HandleTextChangedPeakDivision("Noise Threshold", PeakDivEdit1))
        # PeakDivRelIntensity 对话框
        PeakDivEdit2 = self.DoubleQLineEdit(int(ConstValues.PsPeakDivRelIntensityMin), int(ConstValues.PsPeakDivRelIntensityMax), 2, str(self.PeakDivRelIntensity))
        PeakDivEdit2.textChanged.connect( lambda: self.HandleTextChangedPeakDivision("Relative Noise Threshold", PeakDivEdit2))
        # 多选框，两个选择框
        PeakDivBox1 = QCheckBox("Enable")  # self.PeakDivNeedMerge
        PeakDivBox2 = QCheckBox("Enable")  # self.PeakDivNeedGenImage
        PeakDivBox1.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))  # 设置字体
        PeakDivBox2.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        PeakDivBox1.setChecked(self.PeakDivNeedMerge)  # 设置初始勾选
        PeakDivBox2.setChecked(self.PeakDivNeedGenImage)
        PeakDivBox1.stateChanged.connect(lambda: self.PeakDivCheckboxState(PeakDivBox1, PeakDivBox2))  # 绑定槽函数
        PeakDivBox2.stateChanged.connect(lambda: self.PeakDivCheckboxState(PeakDivBox1, PeakDivBox2))

        # 创建按钮
        PeakDivisionButton1 = QPushButton("确定")
        PeakDivisionButton1.setFixedSize(ConstValues.PsSetupFontSize * 5, ConstValues.PsSetupFontSize * 3)
        PeakDivisionButton1.clicked.connect(lambda: self.HBCPeakDivision(parameters, True))
        PeakDivisionButton2 = QPushButton("退出")
        PeakDivisionButton2.setFixedSize(ConstValues.PsSetupFontSize * 5, ConstValues.PsSetupFontSize * 3)
        PeakDivisionButton2.clicked.connect(lambda: self.HBCPeakDivision(parameters, False))

        # 创建栅格布局
        layout = QGridLayout(self.PeakDivDialog)
        # 第一行内容，PeakDivNoiseThreshold 对话框
        layout.addWidget(self.GetQLabel("Noise Threshold(" + str(ConstValues.PsPeakDivNoiseThresholdMin) + "~" + ConstValues.PsPeakDivNoiseThresholdMaxStr + "):"), 0, 0, 1, 2)
        layout.addWidget(PeakDivEdit1, 0, 2, 1, 2)
        # 第二行内容，PeakDivRelIntensity 对话框
        layout.addWidget(self.GetQLabel("Relative Noise Threshold(" + str(ConstValues.PsPeakDivRelIntensityMin) + "~" + str(ConstValues.PsPeakDivRelIntensityMax) + "):"), 1, 0, 1, 2)
        layout.addWidget(PeakDivEdit2, 1, 2, 1, 2)
        # 第三行内容，self.PeakDivNeedMerge
        layout.addWidget(self.GetQLabel("Merge First Pike : "), 2, 0, 1, 2)
        layout.addWidget(PeakDivBox1, 2, 2, 1, 2)
        # 第四行内容，self.PeakDivNeedGenImage
        layout.addWidget(self.GetQLabel("Generate Images : "), 3, 0, 1, 2)
        layout.addWidget(PeakDivBox2, 3, 2, 1, 2)
        # 最后一行内容，按钮行
        layout.addWidget(PeakDivisionButton1, 4, 2)
        layout.addWidget(PeakDivisionButton2, 4, 3)

        self.PeakDivDialog.exec()
        # 返回值类型：list
        retList = [
                    self.PeakDivNoiseThreshold,
                    self.PeakDivRelIntensity,
                    self.PeakDivNeedMerge,  # 该参数决定是否需要将溶剂效应的第一个峰融合到第二个峰
                    self.PeakDivNeedGenImage  # 该参数决定是否生成图片信息
                  ]
        return retList

    # 设置参数为用户上次输入的值
    def PeakDivisionDefaultParameters(self, parameters):
        # 设置参数，0~1000000(整数)
        self.PeakDivNoiseThreshold = parameters[0]
        # 0.0~100.0(浮点数)
        self.PeakDivRelIntensity = parameters[1]
        # bool，该参数决定是否需要将溶剂效应的第一个峰融合到第二个峰
        self.PeakDivNeedMerge = parameters[2]
        # bool，该参数决定是否生成图片信息
        self.PeakDivNeedGenImage = parameters[3]

    # 用户输入文本后，会进入这个函数处理
    def HandleTextChangedPeakDivision(self, DBType, edit):
        if edit.text() != "":
            if DBType == "Noise Threshold":
                self.PeakDivNoiseThreshold = int(edit.text())
            elif DBType == "Relative Noise Threshold":
                self.PeakDivRelIntensity = float(edit.text())

    # 当 PeakDivBox1,PeakDivBox2 状态改变会进入该函数
    def PeakDivCheckboxState(self, cb1, cb2):
        self.PeakDivNeedMerge = cb1.isChecked()
        self.PeakDivNeedGenImage = cb2.isChecked()

    # HBC：HandleButtonClicked 用户点击确认/取消后，会进入这个函数处理
    def HBCPeakDivision(self, parameters, isOK):
        if not isOK:  # 点击取消按钮
            self.PeakDivisionDefaultParameters(parameters)
            self.PeakDivDialog.close()
        else:  # 点击确认按钮
            inputState = self.PeakDivisionIsParameterValidate()
            if inputState == 1:
                self.PeakDivDialog.close()
            elif inputState == 2:
                PromptBox().warningMessage("Noise Threshold输入不合法！")
            elif inputState == 3:
                PromptBox().warningMessage("Relative Noise Threshold输入不合法！")

    # 参数合法性检查
    def PeakDivisionIsParameterValidate(self):
        # 合法返回1，不合法返回对应的代码
        # 判断self.PeakDivNoiseThreshold 是否合法，对应代码2
        if not (ConstValues.PsPeakDivNoiseThresholdMin <= self.PeakDivNoiseThreshold <= ConstValues.PsPeakDivNoiseThresholdMax):
            return 2
        # 判断self.PeakDivRelIntensity 是否合法，对应代码3
        if not (ConstValues.PsPeakDivRelIntensityMin <= self.PeakDivRelIntensity <= ConstValues.PsPeakDivRelIntensityMax):
            return 3
        # 合法
        return 1

    #################################################################################################################
    def PlotSetup(self, parameters):
        # 画图需要清楚数据来源，因为设置界面需要 3.搜同位素 或者 4.峰提取 去假阳性后的数据，因此设置中需要将去假阳性后的数据传进来
        self.RemoveFPId = parameters[0]  # 判断选择了哪一个文件：self.DelIsoResult(1) 或者 self.PeakDisResult(2)
        self.RemoveFPResult = parameters[1]  # 所有类别去假阳性的结果，二维列表，有表头
        self.RemoveFPResult = self.RemoveFPResult[1:]  # 去掉表头

        # 图形生成参数设置对话框，设置默认参数，这是第一个主窗口
        self.PlotNewParameters = parameters[2:]
        self.PlotDefaultParameters(self.PlotNewParameters)

        # 获取需要绘图的类别
        self.PlotClass = set()
        self.PlotDictionary = {}  # 格式：{key:value, ...}, key : 类别, value : []列表中为DBE的数目
        ClassIndex = 2  # ["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
        DBEIndex = 3
        if self.RemoveFPId == 2:  # 4.峰提取 去假阳性后的数据
            # ["SampleMass", "Area", "startRT", "startRTValue", "endRT", "endRTValue", "TICMassMedian",
            # "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
            ClassIndex = 7
            DBEIndex = 8
        for item in self.RemoveFPResult:
            if len(item) != 0:
                if len(item) == 3:  # 搜同位素后去假阳性文件，还要跳过同位素
                    continue
                itemClass = item[ClassIndex]  # 获取类别
                itemDBE = item[DBEIndex]  # DBE数目
                # 更新集合
                self.PlotClass.add(itemClass)
                # 更新字典
                if itemClass not in self.PlotDictionary:
                    self.PlotDictionary[itemClass] = [itemDBE]
                else:
                    if itemDBE not in self.PlotDictionary[itemClass]:
                        self.PlotDictionary[itemClass].append(itemDBE)
        # 字典中DBE排序
        for key in self.PlotDictionary:
            self.PlotDictionary[key] = sorted(self.PlotDictionary[key])

        self.PlotClass = sorted(list(self.PlotClass))  # 转为list并排序
        self.PlotClassFlag = [0 for _ in range(len(self.PlotClass))]  # 对应标志位，根据此判断是否需要处理这个类别，0不需要，1需要
        for item in self.PlotClass:
            globals()["checkBox_1" + item] = None
            globals()["radioBox_2" + item] = None
            globals()["radioBox_3_1" + item] = None
            globals()["radioBox_4" + item] = None
            globals()["radioBox_6_1" + item] = None
        for key in self.PlotDictionary:  # 用户带勾选DBE初始化
            for num in self.PlotDictionary[key]:
                globals()["radioBox_3_2" + str(key) + str(num)] = None
                globals()["radioBox_6_2" + str(key) + str(num)] = None
        if not self.PlotHasEnter:  # 第一次进入，需要更新self.PlotClassList，在函数HBCPlot()中该值被置为True
            self.PlotClassList = self.PlotClass
        # 单选按钮
        if (not self.PlotHasEnter) and (len(self.PlotClass) != 0):
            self.PlotClassItem = [self.PlotClass[0]]

        # 创建标志位，负责进程互斥
        self.PlotSubUI_1_1AllNoneFlag = False

        # 创建QDialog
        self.PlotDialog = self.CreateDialog("图形生成参数设置", 67, 40)

        # 创建栅格布局
        self.PlotLayout = QGridLayout(self.PlotDialog)

        # 创建控件
        self.PlotMainUIList = self.PlotMainUICreateWidget()  # 主界面控件
        self.PlotSubUI_1List = self.PlotSubUI_1CreateWidget()  # SubUI_1控件
        self.PlotSubUI_2List = self.PlotSubUI_2CreateWidget()  # SubUI_2控件
        self.PlotSubUI_3List = self.PlotSubUI_3CreateWidget()  # SubUI_3控件
        self.PlotSubUI_4List = self.PlotSubUI_4CreateWidget()  # SubUI_4控件
        self.PlotSubUI_5List = self.PlotSubUI_5CreateWidget()  # SubUI_5控件
        self.PlotSubUI_6List = self.PlotSubUI_6CreateWidget()  # SubUI_6控件

        self.PlotSubUINameList = self.PlotSubUINameCreateWidget()  # 命名控件

        # 主界面添加控件
        self.PlotMainUIAddWidget()

        # # 绘制 Retention time vs carbon number 图，探究如何去除假阳性
        # for key in self.PlotDictionary:  # 用户带勾选DBE初始化
        #     for num in self.PlotDictionary[key]:
        #         params = [
        #             2,
        #             self.RemoveFPResult,
        #             self.PlotTitleName,  # 标题名称
        #             self.PlotTitleColor,  # 标题颜色
        #             self.PlotXAxisName,  # x轴名称
        #             self.PlotXAxisColor,  # x轴颜色
        #             self.PlotYAxisName,  # y轴名称
        #             self.PlotYAxisColor,  # y轴颜色
        #             self.PlotHasEnter,  # 记录是否进入过PlotSetup()函数
        #             6,  # 绘图类型
        #             self.PlotClassList,  # 列表，需要绘制的类型，例子：["CH", "N1"]
        #             [key],  # 列表，需要绘制的类型，例子：["CH"]，对应单选钮，长度必须为1
        #             num,  # 整数，记录用户选择的DBE数目
        #             self.PlotConfirm  # 是否确认要画图
        #         ]
        #         ClassPlot(params, "").Plot()

        # 运行
        self.PlotDialog.exec()

        return [
                    self.PlotTitleName,  # 标题名称
                    self.PlotTitleColor,  # 标题颜色
                    self.PlotXAxisName,  # x轴名称
                    self.PlotXAxisColor,  # x轴颜色
                    self.PlotYAxisName,  # y轴名称
                    self.PlotYAxisColor,  # y轴颜色
                    self.PlotHasEnter,  # 记录是否进入过PlotSetup()函数
                    self.PlotType,  # 绘图类型
                    self.PlotClassList,  # 列表，需要绘制的类型，例子：["CH", "N1"]
                    self.PlotClassItem,  # 列表，需要绘制的类型，例子：["CH"]，对应单选钮，长度必须为1
                    self.PlotDBENum,  # 整数，记录用户选择的DBE数目
                    self.PlotConfirm  # 是否确认要画图
                ]

    # -------------------------------------- 删除控件
    def PlotRemoveWidget(self, IdStr):
        destoryList = []
        if IdStr == "MainUI":
            destoryList = self.PlotMainUIList
        elif IdStr == "SubUI_1":
            destoryList = self.PlotSubUI_1List
        elif IdStr == "SubUI_2":
            destoryList = self.PlotSubUI_2List
        elif IdStr == "SubUI_3":
            destoryList = self.PlotSubUI_3List
        elif IdStr == "SubUI_4":
            destoryList = self.PlotSubUI_4List
        elif IdStr == "SubUI_5":
            destoryList = self.PlotSubUI_5List
        elif IdStr == "SubUI_6":
            destoryList = self.PlotSubUI_6List
        elif IdStr == "SubUIName":
            destoryList = self.PlotSubUINameList
        for item in destoryList:
            item.setParent(None)

    # 添加控件
    def PlotAddWidget(self, IdStr):
        if IdStr == "MainUI":
            self.PlotMainUIAddWidget()
        elif IdStr == "SubUI_1":
            self.PlotSubUI_1AddWidget()
        elif IdStr == "SubUI_2":
            self.PlotSubUI_2AddWidget()
        elif IdStr == "SubUI_3":
            self.PlotSubUI_3AddWidget()
        elif IdStr == "SubUI_4":
            self.PlotSubUI_4AddWidget()
        elif IdStr == "SubUI_5":
            self.PlotSubUI_5AddWidget()
        elif IdStr == "SubUI_6":
            self.PlotSubUI_6AddWidget()
        elif IdStr == "SubUIName":
            self.PlotSubUINameAddWidget()

    # 删除控件后再添加控件
    def PlotRemoveAddWidget(self, RemoveIdStr, AddIdStr):
        # 删除控件
        self.PlotRemoveWidget(RemoveIdStr)
        # 添加控件
        self.PlotAddWidget(AddIdStr)

    # -------------------------------------- 创建主界面控件
    def PlotMainUICreateWidget(self):
        # 单选按钮
        self.PlotMainUIRadioButton1 = QRadioButton("Class distribution")
        self.PlotMainUIRadioButton2 = QRadioButton("DBE distribution by class")
        self.PlotMainUIRadioButton3 = QRadioButton("Carbon number distribution by class and DBE")
        self.PlotMainUIRadioButton4 = QRadioButton("DBE vs carbon number by class")
        self.PlotMainUIRadioButton5 = QRadioButton("Kendrick mass defect （KMD）")
        self.PlotMainUIRadioButton6 = QRadioButton("Retention time vs carbon number")
        if self.RemoveFPId == 1:
            self.PlotMainUIRadioButton6.setEnabled(False)
        PlotMainUIRadioButtonList = [
            self.PlotMainUIRadioButton1, self.PlotMainUIRadioButton2, self.PlotMainUIRadioButton3,
            self.PlotMainUIRadioButton4, self.PlotMainUIRadioButton5, self.PlotMainUIRadioButton6,
        ]
        flag = False
        for i in range(6):
            PlotMainUIRadioButtonList[i].setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
            if (self.PlotType == i+1) and (not flag):
                PlotMainUIRadioButtonList[i].setChecked(True)
                flag = True
        # Next/Cancel
        self.PlotMainUIButton1 = QPushButton("Next")
        self.PlotMainUIButton1.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)
        self.PlotMainUIButton2 = QPushButton("Cancel")
        self.PlotMainUIButton2.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)

        # 创建Label
        self.PlotMainUILabel1 = self.GetQLabel("Select Plot Type", "font:15pt '楷体'; color:blue;")
        content = " This Plot Setup Wizard guide you through the steps required to add a new plot and to specify the " + \
                  "plot content\n and properties.\n First,select the type of plot to add:"
        style = "font:10pt '楷体'; border-width:1px; border-style:solid; border-color:rgb(255, 255, 255);"
        self.PlotMainUILabel2 = self.GetQLabel(content, style)
        self.PlotMainUILabel3 = self.GetQLabel("Bar Charts(Histograms)", "color:red")
        self.PlotMainUILabel4 = self.GetQLabel("Dot Plots", "color:red")
        self.PlotMainUILabel5 = self.GetQLabel("")
        self.PlotMainUILabel6 = self.GetQLabel("")

        # 绑定槽函数
        self.PlotMainUIRadioButton1.toggled.connect(lambda: self.PlotMainUIRadioButtonState(self.PlotMainUIRadioButton1, 1))
        self.PlotMainUIRadioButton2.toggled.connect(lambda: self.PlotMainUIRadioButtonState(self.PlotMainUIRadioButton2, 2))
        self.PlotMainUIRadioButton3.toggled.connect(lambda: self.PlotMainUIRadioButtonState(self.PlotMainUIRadioButton3, 3))
        self.PlotMainUIRadioButton4.toggled.connect(lambda: self.PlotMainUIRadioButtonState(self.PlotMainUIRadioButton4, 4))
        self.PlotMainUIRadioButton5.toggled.connect(lambda: self.PlotMainUIRadioButtonState(self.PlotMainUIRadioButton5, 5))
        self.PlotMainUIRadioButton6.toggled.connect(lambda: self.PlotMainUIRadioButtonState(self.PlotMainUIRadioButton6, 6))

        self.PlotMainUIButton1.clicked.connect(self.PlotMainToSubUI)
        self.PlotMainUIButton2.clicked.connect(lambda: self.HBCPlot(False))

        return [
            self.PlotMainUIRadioButton1,
            self.PlotMainUIRadioButton2,
            self.PlotMainUIRadioButton3,
            self.PlotMainUIRadioButton4,
            self.PlotMainUIRadioButton5,
            self.PlotMainUIRadioButton6,
            self.PlotMainUILabel1,
            self.PlotMainUILabel2,
            self.PlotMainUILabel3,
            self.PlotMainUILabel4,
            self.PlotMainUILabel5,
            self.PlotMainUILabel6,
            self.PlotMainUIButton1,
            self.PlotMainUIButton2
        ]

    # 添加主界面控件
    def PlotMainUIAddWidget(self):
        self.PlotLayout.setVerticalSpacing(20)
        # 向 self.PlotLayout 添加控件， 第一个文本
        self.PlotLayout.addWidget(self.PlotMainUILabel1, 0, 0, 1, 5)
        # 第二个文本
        self.PlotLayout.addWidget(self.PlotMainUILabel2, 1, 0, 1, 5)
        # 第三个文本
        self.PlotLayout.addWidget(self.PlotMainUILabel3, 2, 0, 1, 2)
        self.PlotLayout.addWidget(self.PlotMainUILabel4, 2, 2, 1, 2)
        # 第四个：单选按钮
        self.PlotLayout.addWidget(self.PlotMainUIRadioButton1, 3, 0, 1, 2)
        self.PlotLayout.addWidget(self.PlotMainUIRadioButton4, 3, 2, 1, 2)
        self.PlotLayout.addWidget(self.PlotMainUIRadioButton2, 4, 0, 1, 2)
        self.PlotLayout.addWidget(self.PlotMainUIRadioButton5, 4, 2, 1, 2)
        self.PlotLayout.addWidget(self.PlotMainUIRadioButton3, 5, 0, 1, 2)
        self.PlotLayout.addWidget(self.PlotMainUIRadioButton6, 5, 2, 1, 2)
        # 空行
        self.PlotLayout.addWidget(self.PlotMainUILabel5, 6, 0, 1, 5)
        self.PlotLayout.addWidget(self.PlotMainUILabel6, 7, 0, 1, 5)
        # 最后一行
        self.PlotLayout.addWidget(self.PlotMainUIButton1, 8, 3, 1, 1)
        self.PlotLayout.addWidget(self.PlotMainUIButton2, 8, 4, 1, 1)

    # 当单选按钮状态改变会进入该函数
    def PlotMainUIRadioButtonState(self, radioButton, Id):  # 用一个整数代表选中了哪个单选按钮
        if radioButton.isChecked():
            self.PlotType = Id
            if ConstValues.PsIsDebug:
                print(
                    "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                    sys._getframe().f_code.co_name, "\" method***：",
                    "self.PlotType:", self.PlotType
                )

    # -------------------------------------- 一级子界面
    def PlotMainToSubUI(self):
        # 根据选择绘制一级子界面
        subUI = "SubUI_" + str(self.PlotType)
        self.PlotRemoveAddWidget("MainUI", subUI)

    # -------------------------------------- 一级界面下右六个不同的设置界面，第一个：Class distribution，创建控件
    def PlotSubUI_1CreateWidget(self):
        # 返回上一个界面按钮
        self.PlotSubUI_1ButtonPrev = QPushButton("back")
        self.PlotSubUI_1ButtonPrev.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)
        if ConstValues.PsIconType == 1:
            self.PlotSubUI_1ButtonPrev.setIcon(QIcon(QPixmap(ConstValues.PsIconBack)))
        elif ConstValues.PsIconType == 2:
            self.PlotSubUI_1ButtonPrev.setIcon(qtawesome.icon(ConstValues.PsqtaIconBack))
        self.PlotSubUI_1LabelPrev = self.GetQLabel("")  # 标签
        # 复选按钮
        self.PlotSubUI_1CheckBoxAll = QCheckBox("All")
        self.PlotSubUI_1CheckBoxAll.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        # 全选按钮更新值
        if len(self.PlotClassList) == len(self.PlotClass):
            self.PlotSubUI_1CheckBoxAll.setChecked(True)
        self.PlotSubUI_1CheckBoxNone = QCheckBox("None")
        self.PlotSubUI_1CheckBoxNone.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        # 复选按钮，根据类别数目（self.PlotClass：一个列表，里面是种类str）生成复选框
        self.PlotSubUI_1ListWidget = QListWidget()  # 列表控件
        if self.MainWindowsStyle != "Qdarkstyle":
            self.PlotSubUI_1ListWidget.setStyleSheet("background-color: white;")
        for item in self.PlotClass:
            if globals()["checkBox_1" + item] is None:
                globals()["checkBox_1" + item] = QCheckBox(item)
            listWidgetItem = QListWidgetItem()
            self.PlotSubUI_1ListWidget.addItem(listWidgetItem)
            self.PlotSubUI_1ListWidget.setItemWidget(listWidgetItem, globals()["checkBox_1" + item])
            if item in self.PlotClassList:
                globals()["checkBox_1" + item].setChecked(True)
        # Next/Cancel
        self.PlotSubUI_1Button1 = QPushButton("Next")
        self.PlotSubUI_1Button1.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)
        self.PlotSubUI_1Button2 = QPushButton("Cancel")
        self.PlotSubUI_1Button2.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)

        # 绑定槽函数
        self.PlotSubUI_1ButtonPrev.clicked.connect(lambda: self.PlotRemoveAddWidget("SubUI_1", "MainUI"))  # 返回按钮
        self.PlotSubUI_1CheckBoxAll.clicked.connect(lambda: self.PlotSubUI_1CheckBox(1))  # 全选按钮
        self.PlotSubUI_1CheckBoxNone.clicked.connect(lambda: self.PlotSubUI_1CheckBox(2))  # 全不选按钮
        k = 3
        for item in self.PlotClass:
            globals()["checkBox_1" + item].clicked.connect(lambda: self.PlotSubUI_1CheckBox(k))
            k += 1
        self.PlotSubUI_1Button1.clicked.connect(lambda: self.PlotRemoveAddWidget("SubUI_1", "SubUIName"))  # next按钮
        self.PlotSubUI_1Button2.clicked.connect(lambda: self.HBCPlot(False))  # 取消按钮

        return [
            self.PlotSubUI_1ButtonPrev,
            self.PlotSubUI_1LabelPrev,
            self.PlotSubUI_1CheckBoxAll,
            self.PlotSubUI_1CheckBoxNone,
            self.PlotSubUI_1ListWidget,
            self.PlotSubUI_1Button1,
            self.PlotSubUI_1Button2,
        ]

    # 添加控件
    def PlotSubUI_1AddWidget(self):
        self.PlotLayout.setVerticalSpacing(20)
        # 向 self.PlotDialog 添加控件， 第一个文本
        self.PlotLayout.addWidget(self.PlotSubUI_1ButtonPrev, 0, 0, 1, 1)
        self.PlotLayout.addWidget(self.PlotSubUI_1LabelPrev, 0, 1, 1, 4)
        # 第二行
        self.PlotLayout.addWidget(self.PlotSubUI_1CheckBoxAll, 1, 0, 1, 1)
        self.PlotLayout.addWidget(self.PlotSubUI_1CheckBoxNone, 1, 1, 1, 1)
        # 第三行
        self.PlotLayout.addWidget(self.PlotSubUI_1ListWidget, 2, 0, 1, 5)
        # 最后一行
        self.PlotLayout.addWidget(self.PlotSubUI_1Button1, 8, 3, 1, 1)
        self.PlotLayout.addWidget(self.PlotSubUI_1Button2, 8, 4, 1, 1)

    # 一级子界面第一个界面 全选/全不选
    def PlotSubUI_1CheckBox(self, DType):
        if self.PlotSubUI_1_1AllNoneFlag:
            return
        self.PlotSubUI_1_1AllNoneFlag = True

        if DType == 1 and self.PlotSubUI_1CheckBoxAll.isChecked():  # 全选按钮
            self.PlotSubUI_1CheckBoxNone.setChecked(False)
            for item in self.PlotClass:
                globals()["checkBox_1" + item].setChecked(True)
        elif DType == 2 and self.PlotSubUI_1CheckBoxNone.isChecked():  # 全部取消按钮
            self.PlotSubUI_1CheckBoxAll.setChecked(False)
            for item in self.PlotClass:
                globals()["checkBox_1" + item].setChecked(False)
        # 更新数据
        ClassList = []
        for item in self.PlotClass:
            if globals()["checkBox_1" + item].isChecked():
                ClassList.append(item)
        self.PlotClassList = ClassList

        self.PlotSubUI_1_1AllNoneFlag = False

    # -------------------------------------- 第二个：DBE distribution by class，创建控件
    def PlotSubUI_2CreateWidget(self):
        # 返回上一个界面按钮
        self.PlotSubUI_2ButtonPrev = QPushButton("back")
        self.PlotSubUI_2ButtonPrev.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)
        if ConstValues.PsIconType == 1:
            self.PlotSubUI_2ButtonPrev.setIcon(QIcon(QPixmap(ConstValues.PsIconBack)))
        elif ConstValues.PsIconType == 2:
            self.PlotSubUI_2ButtonPrev.setIcon(qtawesome.icon(ConstValues.PsqtaIconBack))
        self.PlotSubUI_2LabelPrev = self.GetQLabel("")  # 标签
        # 单选按钮
        self.PlotSubUI_2ListWidget = QListWidget()  # 列表控件
        if self.MainWindowsStyle != "Qdarkstyle":
            self.PlotSubUI_2ListWidget.setStyleSheet("background-color: white;")
        for item in self.PlotClass:
            if globals()["radioBox_2" + item] is None:
                globals()["radioBox_2" + item] = QRadioButton(item)
            listWidgetItem = QListWidgetItem()
            self.PlotSubUI_2ListWidget.addItem(listWidgetItem)
            self.PlotSubUI_2ListWidget.setItemWidget(listWidgetItem, globals()["radioBox_2" + item])
        if len(self.PlotClassItem) != 0:
            item = self.PlotClassItem[0]
            globals()["radioBox_2" + item].setChecked(True)
        # Next/Cancel
        self.PlotSubUI_2Button1 = QPushButton("Next")
        self.PlotSubUI_2Button1.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)
        self.PlotSubUI_2Button2 = QPushButton("Cancel")
        self.PlotSubUI_2Button2.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)

        # 绑定槽函数
        self.PlotSubUI_2ButtonPrev.clicked.connect(lambda: self.PlotRemoveAddWidget("SubUI_2", "MainUI"))  # 返回按钮
        self.PlotSubUI_2Button1.clicked.connect(lambda: self.PlotRemoveAddWidget("SubUI_2", "SubUIName"))  # next按钮
        self.PlotSubUI_2Button2.clicked.connect(lambda: self.HBCPlot(False))  # 取消按钮

        for item in self.PlotClass:
            globals()["radioBox_2" + item].clicked.connect(self.PlotSubUI_2RadioButton)

        return [
            self.PlotSubUI_2ButtonPrev,
            self.PlotSubUI_2LabelPrev,
            self.PlotSubUI_2ListWidget,
            self.PlotSubUI_2Button1,
            self.PlotSubUI_2Button2,
        ]

    # 添加控件
    def PlotSubUI_2AddWidget(self):
        self.PlotLayout.setVerticalSpacing(20)
        # 向 self.PlotDialog 添加控件， 第一个文本
        self.PlotLayout.addWidget(self.PlotSubUI_2ButtonPrev, 0, 0, 1, 1)
        self.PlotLayout.addWidget(self.PlotSubUI_2LabelPrev, 0, 1, 1, 4)
        # 第二行
        self.PlotLayout.addWidget(self.PlotSubUI_2ListWidget, 1, 0, 1, 5)
        # 最后一行
        self.PlotLayout.addWidget(self.PlotSubUI_2Button1, 8, 3, 1, 1)
        self.PlotLayout.addWidget(self.PlotSubUI_2Button2, 8, 4, 1, 1)

    # 一级子界面第二个界面 选择需要绘制的Class
    def PlotSubUI_2RadioButton(self):
        for item in self.PlotClass:
            if globals()["radioBox_2" + item].isChecked():
                self.PlotClassItem[0] = globals()["radioBox_2" + item].text()
                if ConstValues.PsIsDebug:
                    print(
                        "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                        sys._getframe().f_code.co_name, "\" method***：",
                        "self.PlotClassItem[0]:", self.PlotClassItem[0]
                    )
                break

    # -------------------------------------- 第三个：Carbon number distribution by class and DBE，创建控件
    def PlotSubUI_3CreateWidget(self):
        # 返回上一个界面按钮
        self.PlotSubUI_3ButtonPrev = QPushButton("back")
        self.PlotSubUI_3ButtonPrev.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)
        if ConstValues.PsIconType == 1:
            self.PlotSubUI_3ButtonPrev.setIcon(QIcon(QPixmap(ConstValues.PsIconBack)))
        elif ConstValues.PsIconType == 2:
            self.PlotSubUI_3ButtonPrev.setIcon(qtawesome.icon(ConstValues.PsqtaIconBack))
        self.PlotSubUI_3LabelPrev = self.GetQLabel("")  # 标签
        # 单选按钮
        self.PlotSubUI_3ListWidget1 = QListWidget()  # 列表控件1
        if self.MainWindowsStyle != "Qdarkstyle":
            self.PlotSubUI_3ListWidget1.setStyleSheet("background-color: white;")
        for item in self.PlotClass:
            if globals()["radioBox_3_1" + item] is None:
                globals()["radioBox_3_1" + item] = QRadioButton(item)
            listWidgetItem = QListWidgetItem()
            self.PlotSubUI_3ListWidget1.addItem(listWidgetItem)
            self.PlotSubUI_3ListWidget1.setItemWidget(listWidgetItem, globals()["radioBox_3_1" + item])
        if len(self.PlotClass) != 0:
            item = self.PlotClass[0]
            globals()["radioBox_3_1" + item].setChecked(True)

        # 单选按钮
        self.PlotSubUI_3ListWidget2 = QListWidget()  # 列表控件1
        if self.MainWindowsStyle != "Qdarkstyle":
            self.PlotSubUI_3ListWidget2.setStyleSheet("background-color: white;")
        key = self.PlotClass[0]
        for num in self.PlotDictionary[key]:
            if globals()["radioBox_3_2" + str(key) + str(num)] is None:
                globals()["radioBox_3_2" + str(key) + str(num)] = QRadioButton(str(num))
            listWidgetItem = QListWidgetItem()
            self.PlotSubUI_3ListWidget2.addItem(listWidgetItem)
            self.PlotSubUI_3ListWidget2.setItemWidget(listWidgetItem, globals()["radioBox_3_2" + str(key) + str(num)])
            # 关联槽函数
            globals()["radioBox_3_2" + str(key) + str(num)].clicked.connect(lambda: self.PlotSubUI_3RadioButtonDBE(key))
        # 默认勾选C数赋初值
        self.PlotDBENum = self.PlotDictionary[key][0]
        # 默认勾选第一个
        globals()["radioBox_3_2" + str(key) + str(self.PlotDBENum)].setChecked(True)
        # Next/Cancel
        self.PlotSubUI_3Button1 = QPushButton("Next")
        self.PlotSubUI_3Button1.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)
        self.PlotSubUI_3Button2 = QPushButton("Cancel")
        self.PlotSubUI_3Button2.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)

        # 绑定槽函数
        self.PlotSubUI_3ButtonPrev.clicked.connect(lambda: self.PlotRemoveAddWidget("SubUI_3", "MainUI"))  # 返回按钮
        self.PlotSubUI_3Button1.clicked.connect(lambda: self.PlotRemoveAddWidget("SubUI_3", "SubUIName"))  # next按钮
        self.PlotSubUI_3Button2.clicked.connect(lambda: self.HBCPlot(False))  # 取消按钮

        for item in self.PlotClass:
            globals()["radioBox_3_1" + item].clicked.connect(self.PlotSubUI_3RadioButtonClass)

        return [
            self.PlotSubUI_3ButtonPrev,
            self.PlotSubUI_3LabelPrev,
            self.PlotSubUI_3ListWidget1,
            self.PlotSubUI_3ListWidget2,
            self.PlotSubUI_3Button1,
            self.PlotSubUI_3Button2,
        ]

    # 添加控件
    def PlotSubUI_3AddWidget(self):
        self.PlotLayout.setVerticalSpacing(20)
        # 向 self.PlotDialog 添加控件， 第一个文本
        self.PlotLayout.addWidget(self.PlotSubUI_3ButtonPrev, 0, 0, 1, 1)
        self.PlotLayout.addWidget(self.PlotSubUI_2LabelPrev, 0, 1, 1, 4)
        # 第二行
        self.PlotLayout.addWidget(self.PlotSubUI_3ListWidget1, 1, 0, 1, 2)
        self.PlotLayout.addWidget(self.PlotSubUI_3ListWidget2, 1, 2, 1, 2)
        # 最后一行
        self.PlotLayout.addWidget(self.PlotSubUI_3Button1, 8, 3, 1, 1)
        self.PlotLayout.addWidget(self.PlotSubUI_3Button2, 8, 4, 1, 1)

    # 一级子界面第三个界面 选择需要绘制的Class
    def PlotSubUI_3RadioButtonClass(self):
        # 清除 DBE 显示
        self.PlotSubUI_3ListWidget2.clear()  # 会导致C++回收QRadioButton，因此下面必须创建新globals变量
        # 寻找需要显示的 DBE
        for item in self.PlotClass:
            if globals()["radioBox_3_1" + item].isChecked():
                key = item
                for num in self.PlotDictionary[key]:
                    # print(globals()["radioBox_3_2" + str(key) + str(num)])
                    # if globals()["radioBox_3_2" + str(key) + str(num)] is None:
                    globals()["radioBox_3_2" + str(key) + str(num)] = QRadioButton(str(num))
                    listWidgetItem = QListWidgetItem()
                    self.PlotSubUI_3ListWidget2.addItem(listWidgetItem)
                    self.PlotSubUI_3ListWidget2.setItemWidget(listWidgetItem, globals()["radioBox_3_2" + str(key) + str(num)])
                    # 关联槽函数
                    globals()["radioBox_3_2" + str(key) + str(num)].clicked.connect(lambda: self.PlotSubUI_3RadioButtonDBE(key))
                # C数更新值
                self.PlotDBENum = self.PlotDictionary[key][0]
                # 默认勾选第一个
                globals()["radioBox_3_2" + str(key) + str(self.PlotDBENum)].setChecked(True)
                if ConstValues.PsIsDebug:
                    print(
                        "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                        sys._getframe().f_code.co_name, "\" method***：",
                        "key（self.PlotClassItem[0]）:", key, "self.PlotDBENum:", self.PlotDBENum
                    )
                break

    # 一级子界面第三个界面 选择需要绘制的DBE
    def PlotSubUI_3RadioButtonDBE(self, Class):
        for num in self.PlotDictionary[Class]:
            if globals()["radioBox_3_2" + str(Class) + str(num)].isChecked():
                self.PlotClassItem[0] = Class
                self.PlotDBENum = num
                if ConstValues.PsIsDebug:
                    print(
                        "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                        sys._getframe().f_code.co_name, "\" method***：",
                        "self.PlotClassItem[0]:", self.PlotClassItem[0], "; self.PlotDBENum:", self.PlotDBENum
                    )
                break

    # -------------------------------------- 第四个：DBE vs carbon number by class，创建控件
    def PlotSubUI_4CreateWidget(self):
        # 返回上一个界面按钮
        self.PlotSubUI_4ButtonPrev = QPushButton("back")
        self.PlotSubUI_4ButtonPrev.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)
        if ConstValues.PsIconType == 1:
            self.PlotSubUI_4ButtonPrev.setIcon(QIcon(QPixmap(ConstValues.PsIconBack)))
        elif ConstValues.PsIconType == 2:
            self.PlotSubUI_4ButtonPrev.setIcon(qtawesome.icon(ConstValues.PsqtaIconBack))
        self.PlotSubUI_4LabelPrev = self.GetQLabel("")  # 标签
        # 单选按钮
        self.PlotSubUI_4ListWidget = QListWidget()  # 列表控件
        if self.MainWindowsStyle != "Qdarkstyle":
            self.PlotSubUI_4ListWidget.setStyleSheet("background-color: white;")
        for item in self.PlotClass:
            if globals()["radioBox_4" + item] is None:
                globals()["radioBox_4" + item] = QRadioButton(item)
            listWidgetItem = QListWidgetItem()
            self.PlotSubUI_4ListWidget.addItem(listWidgetItem)
            self.PlotSubUI_4ListWidget.setItemWidget(listWidgetItem, globals()["radioBox_4" + item])
        if len(self.PlotClassItem) != 0:
            item = self.PlotClassItem[0]
            globals()["radioBox_4" + item].setChecked(True)
        # Next/Cancel
        self.PlotSubUI_4Button1 = QPushButton("Next")
        self.PlotSubUI_4Button1.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)
        self.PlotSubUI_4Button2 = QPushButton("Cancel")
        self.PlotSubUI_4Button2.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)

        # 绑定槽函数
        self.PlotSubUI_4ButtonPrev.clicked.connect(lambda: self.PlotRemoveAddWidget("SubUI_4", "MainUI"))  # 返回按钮
        self.PlotSubUI_4Button1.clicked.connect(lambda: self.PlotRemoveAddWidget("SubUI_4", "SubUIName"))  # next按钮
        self.PlotSubUI_4Button2.clicked.connect(lambda: self.HBCPlot(False))  # 取消按钮

        for item in self.PlotClass:
            globals()["radioBox_4" + item].clicked.connect(self.PlotSubUI_4RadioButton)

        return [
            self.PlotSubUI_4ButtonPrev,
            self.PlotSubUI_4LabelPrev,
            self.PlotSubUI_4ListWidget,
            self.PlotSubUI_4Button1,
            self.PlotSubUI_4Button2,
        ]

    # 添加控件
    def PlotSubUI_4AddWidget(self):
        self.PlotLayout.setVerticalSpacing(20)
        # 向 self.PlotDialog 添加控件， 第一个文本
        self.PlotLayout.addWidget(self.PlotSubUI_4ButtonPrev, 0, 0, 1, 1)
        self.PlotLayout.addWidget(self.PlotSubUI_4LabelPrev, 0, 1, 1, 4)
        # 第二行
        self.PlotLayout.addWidget(self.PlotSubUI_4ListWidget, 1, 0, 1, 5)
        # 最后一行
        self.PlotLayout.addWidget(self.PlotSubUI_4Button1, 8, 3, 1, 1)
        self.PlotLayout.addWidget(self.PlotSubUI_4Button2, 8, 4, 1, 1)

    # 一级子界面第四个界面 选择需要绘制的Class
    def PlotSubUI_4RadioButton(self):
        for item in self.PlotClass:
            if globals()["radioBox_4" + item].isChecked():
                self.PlotClassItem[0] = globals()["radioBox_4" + item].text()
                if ConstValues.PsIsDebug:
                    print(
                        "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                        sys._getframe().f_code.co_name, "\" method***：",
                        "self.PlotClassItem[0]:", self.PlotClassItem[0]
                    )
                break

    # -------------------------------------- 第五个：Kendrick mass defect （KMD），创建控件
    def PlotSubUI_5CreateWidget(self):
        # 返回上一个界面按钮
        self.PlotSubUI_5ButtonPrev = QPushButton("back")
        self.PlotSubUI_5ButtonPrev.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)
        if ConstValues.PsIconType == 1:
            self.PlotSubUI_5ButtonPrev.setIcon(QIcon(QPixmap(ConstValues.PsIconBack)))
        elif ConstValues.PsIconType == 2:
            self.PlotSubUI_5ButtonPrev.setIcon(qtawesome.icon(ConstValues.PsqtaIconBack))
        self.PlotSubUI_5LabelPrev = self.GetQLabel("")  # 标签
        # 单选按钮
        self.PlotSubUI_5ListWidget = QListWidget()  # 列表控件
        if self.MainWindowsStyle != "Qdarkstyle":
            self.PlotSubUI_5ListWidget.setStyleSheet("background-color: white;")
        listWidgetItem = QListWidgetItem()
        self.PlotSubUI_5ListWidget.addItem(listWidgetItem)
        self.PlotSubUI_5ListWidget.setItemWidget(listWidgetItem, self.GetQLabel("请直接下一步"))
        # Next/Cancel
        self.PlotSubUI_5Button1 = QPushButton("Next")
        self.PlotSubUI_5Button1.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)
        self.PlotSubUI_5Button2 = QPushButton("Cancel")
        self.PlotSubUI_5Button2.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)

        # 绑定槽函数
        self.PlotSubUI_5ButtonPrev.clicked.connect(lambda: self.PlotRemoveAddWidget("SubUI_5", "MainUI"))  # 返回按钮
        self.PlotSubUI_5Button1.clicked.connect(lambda: self.PlotRemoveAddWidget("SubUI_5", "SubUIName"))  # next按钮
        self.PlotSubUI_5Button2.clicked.connect(lambda: self.HBCPlot(False))  # 取消按钮


        return [
            self.PlotSubUI_5ButtonPrev,
            self.PlotSubUI_5LabelPrev,
            self.PlotSubUI_5ListWidget,
            self.PlotSubUI_5Button1,
            self.PlotSubUI_5Button2,
        ]

    # 添加控件
    def PlotSubUI_5AddWidget(self):
        self.PlotLayout.setVerticalSpacing(20)
        # 向 self.PlotDialog 添加控件， 第一个文本
        self.PlotLayout.addWidget(self.PlotSubUI_5ButtonPrev, 0, 0, 1, 1)
        self.PlotLayout.addWidget(self.PlotSubUI_5LabelPrev, 0, 1, 1, 4)
        # 第二行
        self.PlotLayout.addWidget(self.PlotSubUI_5ListWidget, 1, 0, 1, 5)
        # 最后一行
        self.PlotLayout.addWidget(self.PlotSubUI_5Button1, 8, 3, 1, 1)
        self.PlotLayout.addWidget(self.PlotSubUI_5Button2, 8, 4, 1, 1)

    # -------------------------------------- 第六个：Retention time vs carbon number，创建控件
    def PlotSubUI_6CreateWidget(self):
        # 返回上一个界面按钮
        self.PlotSubUI_6ButtonPrev = QPushButton("back")
        self.PlotSubUI_6ButtonPrev.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)
        if ConstValues.PsIconType == 1:
            self.PlotSubUI_6ButtonPrev.setIcon(QIcon(QPixmap(ConstValues.PsIconBack)))
        elif ConstValues.PsIconType == 2:
            self.PlotSubUI_6ButtonPrev.setIcon(qtawesome.icon(ConstValues.PsqtaIconBack))
        self.PlotSubUI_6LabelPrev = self.GetQLabel("")  # 标签
        # 单选按钮
        self.PlotSubUI_6ListWidget1 = QListWidget()  # 列表控件1
        if self.MainWindowsStyle != "Qdarkstyle":
            self.PlotSubUI_6ListWidget1.setStyleSheet("background-color: white;")
        for item in self.PlotClass:
            if globals()["radioBox_6_1" + item] is None:
                globals()["radioBox_6_1" + item] = QRadioButton(item)
            listWidgetItem = QListWidgetItem()
            self.PlotSubUI_6ListWidget1.addItem(listWidgetItem)
            self.PlotSubUI_6ListWidget1.setItemWidget(listWidgetItem, globals()["radioBox_6_1" + item])
        if len(self.PlotClass) != 0:
            item = self.PlotClass[0]
            globals()["radioBox_6_1" + item].setChecked(True)

        # 单选按钮
        self.PlotSubUI_6ListWidget2 = QListWidget()  # 列表控件1
        if self.MainWindowsStyle != "Qdarkstyle":
            self.PlotSubUI_6ListWidget2.setStyleSheet("background-color: white;")
        key = self.PlotClass[0]
        for num in self.PlotDictionary[key]:
            if globals()["radioBox_6_2" + str(key) + str(num)] is None:
                globals()["radioBox_6_2" + str(key) + str(num)] = QRadioButton(str(num))
            listWidgetItem = QListWidgetItem()
            self.PlotSubUI_6ListWidget2.addItem(listWidgetItem)
            self.PlotSubUI_6ListWidget2.setItemWidget(listWidgetItem,
                                                      globals()["radioBox_6_2" + str(key) + str(num)])
            # 关联槽函数
            globals()["radioBox_6_2" + str(key) + str(num)].clicked.connect(
                lambda: self.PlotSubUI_3RadioButtonDBE(key))
        # 默认勾选C数赋初值
        self.PlotDBENum = self.PlotDictionary[key][0]
        # 默认勾选第一个
        globals()["radioBox_6_2" + str(key) + str(self.PlotDBENum)].setChecked(True)
        # Next/Cancel
        self.PlotSubUI_6Button1 = QPushButton("Next")
        self.PlotSubUI_6Button1.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)
        self.PlotSubUI_6Button2 = QPushButton("Cancel")
        self.PlotSubUI_6Button2.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)

        # 绑定槽函数
        self.PlotSubUI_6ButtonPrev.clicked.connect(lambda: self.PlotRemoveAddWidget("SubUI_6", "MainUI"))  # 返回按钮
        self.PlotSubUI_6Button1.clicked.connect(lambda: self.PlotRemoveAddWidget("SubUI_6", "SubUIName"))  # next按钮
        self.PlotSubUI_6Button2.clicked.connect(lambda: self.HBCPlot(False))  # 取消按钮

        for item in self.PlotClass:
            globals()["radioBox_6_1" + item].clicked.connect(self.PlotSubUI_6RadioButtonClass)

        return [
            self.PlotSubUI_6ButtonPrev,
            self.PlotSubUI_6LabelPrev,
            self.PlotSubUI_6ListWidget1,
            self.PlotSubUI_6ListWidget2,
            self.PlotSubUI_6Button1,
            self.PlotSubUI_6Button2,
        ]

    # 添加控件
    def PlotSubUI_6AddWidget(self):
        self.PlotLayout.setVerticalSpacing(20)
        # 向 self.PlotDialog 添加控件， 第一个文本
        self.PlotLayout.addWidget(self.PlotSubUI_6ButtonPrev, 0, 0, 1, 1)
        self.PlotLayout.addWidget(self.PlotSubUI_2LabelPrev, 0, 1, 1, 4)
        # 第二行
        self.PlotLayout.addWidget(self.PlotSubUI_6ListWidget1, 1, 0, 1, 2)
        self.PlotLayout.addWidget(self.PlotSubUI_6ListWidget2, 1, 2, 1, 2)
        # 最后一行
        self.PlotLayout.addWidget(self.PlotSubUI_6Button1, 8, 3, 1, 1)
        self.PlotLayout.addWidget(self.PlotSubUI_6Button2, 8, 4, 1, 1)

    # 一级子界面第三个界面 选择需要绘制的Class
    def PlotSubUI_6RadioButtonClass(self):
        # 清除 DBE 显示
        self.PlotSubUI_6ListWidget2.clear()  # 会导致C++回收QRadioButton，因此下面必须创建新globals变量
        # 寻找需要显示的 DBE
        for item in self.PlotClass:
            if globals()["radioBox_6_1" + item].isChecked():
                key = item
                for num in self.PlotDictionary[key]:
                    # print(globals()["radioBox_6_2" + str(key) + str(num)])
                    # if globals()["radioBox_6_2" + str(key) + str(num)] is None:
                    globals()["radioBox_6_2" + str(key) + str(num)] = QRadioButton(str(num))
                    listWidgetItem = QListWidgetItem()
                    self.PlotSubUI_6ListWidget2.addItem(listWidgetItem)
                    self.PlotSubUI_6ListWidget2.setItemWidget(listWidgetItem, globals()["radioBox_6_2" + str(key) + str(num)])
                    # 关联槽函数
                    globals()["radioBox_6_2" + str(key) + str(num)].clicked.connect(lambda: self.PlotSubUI_6RadioButtonDBE(key))
                # C数更新值
                self.PlotDBENum = self.PlotDictionary[key][0]
                # 默认勾选第一个
                globals()["radioBox_6_2" + str(key) + str(self.PlotDBENum)].setChecked(True)
                if ConstValues.PsIsDebug:
                    print(
                        "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                        sys._getframe().f_code.co_name, "\" method***：",
                        "key（self.PlotClassItem[0]）:", key, "self.PlotDBENum:", self.PlotDBENum
                    )
                break

    # 一级子界面第三个界面 选择需要绘制的DBE
    def PlotSubUI_6RadioButtonDBE(self, Class):
        for num in self.PlotDictionary[Class]:
            if globals()["radioBox_6_2" + str(Class) + str(num)].isChecked():
                self.PlotClassItem[0] = Class
                self.PlotDBENum = num
                if ConstValues.PsIsDebug:
                    print(
                        "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                        sys._getframe().f_code.co_name, "\" method***：",
                        "self.PlotClassItem[0]:", self.PlotClassItem[0], "; self.PlotDBENum:", self.PlotDBENum
                    )
                break

    # -------------------------------------- 一级子界面对应的二级子界面，命名功能等
    def PlotSubUINameCreateWidget(self):
        # 返回上一个界面按钮
        self.PlotSubUINamePrev = QPushButton("back")
        self.PlotSubUINamePrev.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)
        if ConstValues.PsIconType == 1:
            self.PlotSubUINamePrev.setIcon(QIcon(QPixmap(ConstValues.PsIconBack)))
        elif ConstValues.PsIconType == 2:
            self.PlotSubUINamePrev.setIcon(qtawesome.icon(ConstValues.PsqtaIconBack))
        self.PlotSubUINameLabelPrev = self.GetQLabel("")

        style = "background-color:white;border-width:1px; border-style:solid; border-color:rgb(211, 211, 211);"
        pa = QPalette()
        # 第一行输入内容
        self.PlotSubUINameLabel1 = self.GetQLabel("标题")
        self.PlotSubUINameEdit1 = self.RegExpQLineEdit(text=self.PlotTitleName)
        if self.MainWindowsStyle != "Qdarkstyle":
            self.PlotSubUINameEdit1.setStyleSheet("background-color: white;")
        self.PlotSubUINameLabel1_ = self.GetQLabel(text="标题", style=style, alignment="AlignCenter")
        self.PlotSubUINameLabel1_.setFixedSize(ConstValues.PsSetupFontSize * 5, ConstValues.PsSetupFontSize * 3)
        self.PlotSubUINameButton1 = QPushButton("color")
        pa.setColor(QPalette.WindowText, QColor(*self.PlotTitleColor))
        self.PlotSubUINameLabel1_.setPalette(pa)
        # 第二行输入内容
        self.PlotSubUINameLabel2 = self.GetQLabel("x轴名称")
        self.PlotSubUINameEdit2 = self.RegExpQLineEdit(text=self.PlotXAxisName)
        if self.MainWindowsStyle != "Qdarkstyle":
            self.PlotSubUINameEdit2.setStyleSheet("background-color: white;")
        self.PlotSubUINameLabel2_ = self.GetQLabel(text="x轴", style=style, alignment="AlignCenter")
        self.PlotSubUINameLabel2_.setFixedSize(ConstValues.PsSetupFontSize * 5, ConstValues.PsSetupFontSize * 3)
        self.PlotSubUINameButton2 = QPushButton("color")
        pa.setColor(QPalette.WindowText, QColor(*self.PlotXAxisColor))
        self.PlotSubUINameLabel2_.setPalette(pa)
        # 第三行输入内容
        self.PlotSubUINameLabel3 = self.GetQLabel("y轴名称")
        self.PlotSubUINameEdit3 = self.RegExpQLineEdit(text=self.PlotYAxisName)
        if self.MainWindowsStyle != "Qdarkstyle":
            self.PlotSubUINameEdit3.setStyleSheet("background-color: white;")
        self.PlotSubUINameLabel3_ = self.GetQLabel(text="y轴", style=style, alignment="AlignCenter")
        self.PlotSubUINameLabel3_.setFixedSize(ConstValues.PsSetupFontSize * 5, ConstValues.PsSetupFontSize * 3)
        self.PlotSubUINameButton3 = QPushButton("color")
        pa.setColor(QPalette.WindowText, QColor(*self.PlotYAxisColor))
        self.PlotSubUINameLabel3_.setPalette(pa)

        # Next/Cancel
        self.PlotSubUINameButtonFinish = QPushButton("Finish")
        self.PlotSubUINameButtonFinish.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)

        # 绑定槽函数
        self.PlotSubUINameEdit1.textChanged.connect(lambda: self.HandleTextChangedPlot(1, self.PlotSubUINameEdit1))
        self.PlotSubUINameEdit2.textChanged.connect(lambda: self.HandleTextChangedPlot(2, self.PlotSubUINameEdit2))
        self.PlotSubUINameEdit3.textChanged.connect(lambda: self.HandleTextChangedPlot(3, self.PlotSubUINameEdit3))
        self.PlotSubUINameButton1.clicked.connect(lambda: self.PlotSubUINameSetColor(1))  # 标题颜色
        self.PlotSubUINameButton2.clicked.connect(lambda: self.PlotSubUINameSetColor(2))  # x轴颜色
        self.PlotSubUINameButton3.clicked.connect(lambda: self.PlotSubUINameSetColor(3))  # y轴颜色
        self.PlotSubUINameButtonFinish.clicked.connect(lambda: self.HBCPlot(True))  # 取消按钮

        return [
            self.PlotSubUINamePrev,
            self.PlotSubUINameLabelPrev,
            self.PlotSubUINameLabel1,
            self.PlotSubUINameEdit1,
            self.PlotSubUINameLabel1_,
            self.PlotSubUINameButton1,
            self.PlotSubUINameLabel2,
            self.PlotSubUINameEdit2,
            self.PlotSubUINameLabel2_,
            self.PlotSubUINameButton2,
            self.PlotSubUINameLabel3,
            self.PlotSubUINameEdit3,
            self.PlotSubUINameLabel3_,
            self.PlotSubUINameButton3,
            self.PlotSubUINameButtonFinish
        ]

    # 添加 Class distribution 1_1 控件
    def PlotSubUINameAddWidget(self):
        self.PlotLayout.setVerticalSpacing(40)
        # 向 self.PlotDialog 添加控件， 第一个文本
        self.PlotLayout.addWidget(self.PlotSubUINamePrev, 0, 0, 1, 1)
        self.PlotLayout.addWidget(self.PlotSubUINameLabelPrev, 0, 1, 1, 5)
        # 第二行
        self.PlotLayout.addWidget(QLabel(), 1, 0, 1, 1)
        line = 2
        self.PlotLayout.addWidget(self.PlotSubUINameLabel1, line, 0, 1, 1)
        self.PlotLayout.addWidget(self.PlotSubUINameEdit1, line, 1, 1, 3)
        self.PlotLayout.addWidget(self.PlotSubUINameLabel1_, line, 4, 1, 1)
        self.PlotLayout.addWidget(self.PlotSubUINameButton1, line, 5, 1, 1)
        # 第三行
        line = 3
        self.PlotLayout.addWidget(self.PlotSubUINameLabel2, line, 0, 1, 1)
        self.PlotLayout.addWidget(self.PlotSubUINameEdit2, line, 1, 1, 3)
        self.PlotLayout.addWidget(self.PlotSubUINameLabel2_, line, 4, 1, 1)
        self.PlotLayout.addWidget(self.PlotSubUINameButton2, line, 5, 1, 1)
        # 第四行
        line = 4
        self.PlotLayout.addWidget(self.PlotSubUINameLabel3, line, 0, 1, 1)
        self.PlotLayout.addWidget(self.PlotSubUINameEdit3, line, 1, 1, 3)
        self.PlotLayout.addWidget(self.PlotSubUINameLabel3_, line, 4, 1, 1)
        self.PlotLayout.addWidget(self.PlotSubUINameButton3, line, 5, 1, 1)
        # 填充行
        self.PlotLayout.addWidget(QLabel(), 5, 0, 1, 1)
        # 最后一行
        self.PlotLayout.addWidget(self.PlotSubUINameButtonFinish, 8, 5, 1, 1)

        # 根据图的类型不同，绑定返回不同的界面
        backUI = "SubUI_" + str(self.PlotType)
        self.PlotSubUINamePrev.clicked.connect(lambda: self.PlotRemoveAddWidget("SubUIName", backUI))  # 返回按钮

        # 根据图的类型不同，绘制图形
        if self.PlotType == 1:  # Class distribution
            self.PlotTitleName = "Class_distribution"  # 标题名称
            self.PlotXAxisName = "Class"  # x轴名称
            self.PlotYAxisName = "Relative abundance(%)"  # y轴名称
        elif self.PlotType == 2:  # DBE distribution by class
            self.PlotTitleName = "DBE_distribution_by_class"  # 标题名称
            self.PlotXAxisName = "DBE"  # x轴名称
            self.PlotYAxisName = "Relative abundance(%)"  # y轴名称
        elif self.PlotType == 3:  # Carbon number distribution by class and DBE
            self.PlotTitleName = "Carbon_number_distribution_by_class_and_DBE"  # 标题名称
            self.PlotXAxisName = "Carbon number"  # x轴名称
            self.PlotYAxisName = "Relative abundance(%)"  # y轴名称
        elif self.PlotType == 4:  # DBE vs carbon number by class
            self.PlotTitleName = "DBE_vs_carbon_number_by_class"  # 标题名称
            self.PlotXAxisName = "Carbon number"  # x轴名称
            self.PlotYAxisName = "DBE"  # y轴名称
        elif self.PlotType == 5:  # Kendrick mass defect （KMD）
            self.PlotTitleName = "Kendrick_mass_defect"  # 标题名称
            self.PlotXAxisName = "NKM"  # x轴名称
            self.PlotYAxisName = "KMD"  # y轴名称
        elif self.PlotType == 6:  # retention time vs carbon number
            self.PlotTitleName = "Retention_time_vs_carbon_number"  # 标题名称
            self.PlotXAxisName = "Carbon number"  # x轴名称
            self.PlotYAxisName = "startRTValue"  # y轴名称

        self.PlotSubUINameEdit1.setPlaceholderText(self.PlotTitleName)
        self.PlotSubUINameEdit2.setPlaceholderText(self.PlotXAxisName)
        self.PlotSubUINameEdit3.setPlaceholderText(self.PlotYAxisName)

    # 设置颜色对话框
    def PlotSubUINameSetColor(self, DType):
        color = QColorDialog.getColor()
        if ConstValues.PsIsDebug:
            print(
                "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                sys._getframe().f_code.co_name, "\" method***：",
                "color.getRgb():", color.getRgb()
            )
        p = QPalette()
        p.setColor(QPalette.WindowText, color)
        if DType == 1:  # 标题颜色
            self.PlotSubUINameLabel1_.setPalette(p)
            self.PlotTitleColor = color.getRgb()
            pass
        elif DType == 2:  # x轴颜色
            self.PlotSubUINameLabel2_.setPalette(p)
            self.PlotXAxisColor = color.getRgb()
        elif DType == 3:  # y轴颜色
            self.PlotSubUINameLabel3_.setPalette(p)
            self.PlotYAxisColor = color.getRgb()

    # 用户输入文本后，会进入这个函数处理
    def HandleTextChangedPlot(self, DType, edit):
        if edit.text() != "":
            if DType == 1:  # 标题名称
                self.PlotTitleName = edit.text()
            elif DType == 2:  # x轴名称
                self.PlotXAxisName = edit.text()
            elif DType == 3:  # y轴名称
                self.PlotYAxisName = edit.text()

    # -------------------------------------- 设置参数为用户上次输入的值
    def PlotDefaultParameters(self, newParameters):
        self.PlotTitleName = newParameters[0]  # 标题名称
        self.PlotTitleColor = newParameters[1]  # 标题颜色
        self.PlotXAxisName = newParameters[2]  # x轴名称
        self.PlotXAxisColor = newParameters[3]  # x轴颜色
        self.PlotYAxisName = newParameters[4]  # y轴名称
        self.PlotYAxisColor = newParameters[5]  # y轴颜色
        self.PlotHasEnter = newParameters[6]  # 记录是否进入过PlotSetup()函数
        self.PlotType = newParameters[7]  # 整数（1~6），绘图类型
        self.PlotClassList = newParameters[8]  # 列表，需要绘制的类型，例子：["CH", "N1"]
        self.PlotClassItem = newParameters[9]  # 列表，需要绘制的类型，例子：["CH"]，对应单选钮，长度必须为1
        self.PlotDBENum = newParameters[10]  # 整数，记录用户选择的DBE数目
        self.PlotConfirm = newParameters[11]  # 用户是否确认要画图

    # HBC：HandleButtonClicked 用户点击 Finished/Cancel后，会进入这个函数处理
    def HBCPlot(self, isOK):
        if not isOK:  # 点击取消按钮
            self.PlotDefaultParameters(self.PlotNewParameters)
            self.PlotConfirm = False
            self.PlotDialog.close()
        else:  # 点击确认按钮
            self.PlotHasEnter = True
            self.PlotConfirm = True
            inputState = self.PlotIsParameterValidate()
            if inputState == 1:
                self.PlotDialog.close()

    # 参数合法性检查
    def PlotIsParameterValidate(self):

        # 一定合法
        return 1

    #################################################################################################################
    def StartModeSetup(self, parameters):
        # 峰检测设置对话框，设置默认参数
        self.StartModeDefaultParameters(parameters)

        # 创建QDialog
        self.StartModeDialog = QDialog()
        self.StartModeDialog.setWindowTitle("模式选择")
        self.StartModeDialog.setFixedSize(ConstValues.PsSetupFontSize * 67, ConstValues.PsSetupFontSize * 40)  # 固定窗口大小
        if ConstValues.PsIconType == 1:
            self.StartModeDialog.setWindowIcon(QIcon(ConstValues.PsWindowIcon))
        elif ConstValues.PsIconType == 2:
            self.StartModeDialog.setWindowIcon(qtawesome.icon(ConstValues.PsqtaWindowIcon, color=ConstValues.PsqtaWindowIconColor))
        if ConstValues.PsSetupStyleEnabled and (self.MainWindowsStyle != "Qdarkstyle"):
            self.StartModeDialog.setStyleSheet(ConstValues.PsSetupStyle)

        # 创建控件
        StartModeLabel = self.GetQLabel("Select Run Mode", "font:15pt '楷体'; color:blue;")
        # 单选按钮
        StartModeListWidget = QListWidget()  # 列表控件
        if self.MainWindowsStyle != "Qdarkstyle":
            StartModeListWidget.setStyleSheet("background-color: white;")
        self.modeList = [
                        "1：去空白 --> 数据库生成 --> 搜同位素 --> 去假阳性",
                        "2：去空白 --> 数据库生成 --> 搜同位素 --> 峰提取 --> 去假阳性",
                        "3：去空白 --> 数据库生成 --> 搜同位素 --> 峰提取 --> 去假阳性 --> 峰检测",
                        "4：数据库生成 --> 搜同位素 --> 去假阳性",
                        "5：数据库生成 --> 搜同位素 --> 峰提取 --> 去假阳性",
                        "6：数据库生成 --> 搜同位素 --> 峰提取 --> 去假阳性 --> 峰检测"
                    ]
        for i in range(len(self.modeList)):
            mode = self.modeList[i]
            globals()["mode" + str(i)] = QRadioButton(mode)
            globals()["mode" + str(i)].setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
            listWidgetItem = QListWidgetItem()
            StartModeListWidget.addItem(listWidgetItem)
            StartModeListWidget.setItemWidget(listWidgetItem, globals()["mode" + str(i)])
            # 关联槽函数
            globals()["mode" + str(i)].clicked.connect(lambda: self.StartModeRadioButtonState())
        globals()["mode" + str(self.startMode-1)].setChecked(True)

        # 创建按钮
        StartModeButton1 = QPushButton("确定")
        StartModeButton1.setFixedSize(ConstValues.PsSetupFontSize * 5, ConstValues.PsSetupFontSize * 3)
        StartModeButton1.clicked.connect(lambda: self.HBCStartMode(parameters, True))
        StartModeButton2 = QPushButton("退出")
        StartModeButton2.setFixedSize(ConstValues.PsSetupFontSize * 5, ConstValues.PsSetupFontSize * 3)
        StartModeButton2.clicked.connect(lambda: self.HBCStartMode(parameters, False))

        # 创建栅格布局
        layout = QGridLayout(self.StartModeDialog)
        layout.setVerticalSpacing(20)
        # 向 self.PlotDialog 添加控件， 第一个文本
        layout.addWidget(StartModeLabel, 0, 0, 1, 5)
        # 第二行
        layout.addWidget(StartModeListWidget, 1, 0, 1, 5)
        # 最后一行
        layout.addWidget(StartModeButton1, 8, 3, 1, 1)
        layout.addWidget(StartModeButton2, 8, 4, 1, 1)

        self.StartModeDialog.exec()
        # 返回值类型：list
        retList = [
                    self.startMode,
                    self.startModeConfirm
                  ]
        return retList

    # 设置参数为用户上次输入的值
    def StartModeDefaultParameters(self, parameters):
        # 运行模式
        self.startMode = parameters[0]
        # 确定开始运行
        self.startModeConfirm = parameters[1]

    # HBC：HandleButtonClicked 用户点击确认/取消后，会进入这个函数处理
    def HBCStartMode(self, parameters, isOK):
        if not isOK:  # 点击取消按钮
            self.StartModeDefaultParameters(parameters)
            self.startModeConfirm = False
        else:  # 点击确认按钮
            self.startModeConfirm = True
        self.StartModeDialog.close()

    def StartModeRadioButtonState(self):
        for i in range(len(self.modeList)):
            if globals()["mode" + str(i)].isChecked():  # 确定是哪个按钮被选中
                self.startMode = i + 1
                if ConstValues.PsIsDebug:
                    print(
                        "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                        sys._getframe().f_code.co_name, "\" method***：",
                        "self.startMode:", self.startMode
                    )
                break


if __name__ == '__main__':
    # 创建QApplication类的实例
    app = QApplication(sys.argv)
    # 创建一个窗口
    main = MainWin()
    # 进入程序的主循环、并通过exit_()函数确保主循环安全结束
    sys.exit(app.exec_())

