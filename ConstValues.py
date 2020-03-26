# coding=utf-8
# 此文件负责定义一些常量
# 石油组学软件 petromics software


class ConstValues:
    def __init__(self):
        pass

    # 用于打开调试
    PsIsDebug = True
    # 用于是否可以单独运行
    PsIsSingleRun = True
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
    # 主窗口风格  可选：["Windows", "Fusion", "Macintosh"]
    PsMainWindowStyle = "Macintosh"
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
    PsMenuFontSize = 10
    # 工具栏显示的字体及大小
    PsToolbarFontType = "Arial"
    PsToolbarFontSize = 10
    # 主界面树控件显示的字体及大小
    PsTreeFontType = "Arial"
    PsTreeFontSize = 11
    # 运行提示框弹出时间 1 -> 1s
    PsBeforeRunningPromptBoxTime = 1
    PsAfterRunningPromptBoxTime = 1
    # 图标系统  1:从图片读取  2:来自 qtawesome
    PsIconType = 2
    PsIconLoading = './images/ajax-loading.gif'  # 正在运行gif
    # 从图片读取
    PsWindowIcon = './images/Dragon.ico'  # 窗口弹出的图标所在的位置
    PsIconOpenFile = './images/open.png'  # 打开文件图标
    PsIconExit = './images/close.ico'  # 退出软件图标
    PsIconDeleteBlank = './images/work/j1.png'  # 删空白图标
    PsIconGDB = './images/work/j2.png'  # 数据库生成图标
    PsIcondelIso = './images/work/j3.png'  # 去同位素图标
    PsIconpeakDis = './images/work/j4.png'  # 峰识别图标
    PsIconRemoveFP = './images/work/j5.png'  # 去假阳性图标
    PsIconpeakDiv = './images/work/j6.png'  # 峰检测图标
    PsIconPlot = './images/work/j7.png'  # 画图图标
    PsIconAllStart = './images/work/j21.png'  # 全部开始图标
    PsIconAllReset = './images/work/j12.png'  # 重置软件图标
    PsIconBack = "./images/back.png"
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
    PsqtaIconPlot = 'fa.bar-chart-o'  # 峰检测图标
    PsqtaIconAllStart = 'fa.play-circle-o'  # 全部开始图标
    PsqtaIconAllReset = 'fa.refresh'  # 重置软件图标
    PsqtaIconBack = "fa.arrow-left"  # 返回上一级图标
    PsqtaIconTreeFolder = "fa.folder-o"  # 树控件文件夹
    PsqtaIconTreeImage = "fa.file-image-o"  # 树控件文件夹

    # 左侧树结构二级目录名称
    PsTreeInputFiles = "输入文件"
    PsTreeDeleteBlank = "去空白结果"
    PsTreeGDB = "数据库生成结果"
    PsTreeDelIso = "搜同位素结果"
    PsTreePeakDis = "峰提取结果"
    PsTreeRemoveFP = "去假阳性结果"
    PsTreePeakDiv = "峰检测结果"
    PsTreePlot = "绘图结果"
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
    PsIsShowGif = False

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
    PsReadFileDefaultDirectoy = "./inputdata/350"

    # 设置框字体以及大小
    PsSetupFontType = "Arial"
    PsSetupFontSize = 12
    PsSetupStyleEnabled = False  # 默认颜色是否使能
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


