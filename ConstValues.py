# coding=utf-8
# 此文件负责定义一些常量
# 石油组学软件 petromics software


class ConstValues():
    def __init__(self):
        pass

    # 用于打开调试
    PsIsDebug = True
    # 用于是否可以单独运行
    PsIsSingleRun = False
    # 主窗口名称
    PsMainWindowTitle = "石油组学软件"
    # 主窗口宽度
    PsMainWindowWidth = 1200
    # 主窗口高度
    PsMainWindowHeight = 800
    # 窗口弹出的图片所在的位置
    PsMainWindowIcon = './images/Dragon.ico'
    # 主窗口底部状态栏显示的信息
    PsMainWindowStatusMessage = "欢迎使用！"
    # 主窗口风格  可选：["Windows", "Fusion", "Macintosh"]
    PsMainWindowStyle = "Macintosh"
    # 运行提示框弹出时间 1000 -> 1s
    PsBeforeRunningPromptBoxTime = 1000
    PsAfterRunningPromptBoxTime = 1000
    # 扣空白错误提示信息
    PsDeleteBlankErrorMessage = "请选择需要处理的样本文件、空白文件和总离子流图文件!"
    # 扣同位素错误提示信息
    PsDeleteIsotopeErrorMessage = "请先扣空白和生成数据库!"
    # 峰识别错误提示信息
    PsPeakDistinguishErrorMessage1 = "请选择需要处理的总离子流图文件!"
    PsPeakDistinguishErrorMessage2 = "请先扣同位素!"

    # 样本文件和空白文件header所在excel中的行数：PsHeaderLine = excel.header - 1
    PsHeaderLine = 7

    # 设置框字体以及大小
    PsSetupFontType = "Arial"
    PsSetupFontSize = 12

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
    PsGDBClass = ["N1", "N1O1", "N1S1", "CH"]  # 数据库生成(参数)：Class类型
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
    PsGDBM_ZRageLow = 50  # 数据库生成(参数)：m/z rage(质荷比范围)最小值(包含)
    PsGDBM_ZRageHigh = 1000  # 数据库生成(参数)：m/z rage(质荷比范围)最小值(包含)
    PsGDBM_ZRageMin = 50
    PsGDBM_ZRageMax = 5000
    # 离子类型
    PsGDB_MHPostive = True  # 数据库生成(参数)：正离子，是否选择[M+H]+，True为选中
    PsGDB_MPostive = False  # 数据库生成(参数)：正离子，是否选择M+，True为选中
    PsGDB_MHNegative = False  # 数据库生成(参数)：负离子，是否选择[M-H]-，True为选中
    PsGDB_MNegative = False  # 数据库生成(参数)：负离子，是否选择M-，True为选中

    # 扣同位素设置默认参数
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
    PsDelIsoIsotopeIntensityDeviation = 10  # 30%
    PsDelIsoIsotopeIntensityDeviationMin = 0
    PsDelIsoIsotopeIntensityDeviationMax = 100

    # 峰识别设置默认参数
    # 0~10000（整数）
    PsPeakDisContinuityNum = 30
    PsPeakDisContinuityNumMin = 0
    PsPeakDisContinuityNumMax = 10000
    # 0.00~100.00（浮点数）
    PsPeakDisMassDeviation = 2.0
    PsPeakDisMassDeviationMin = 0.0
    PsPeakDisMassDeviationMax = 100.0




