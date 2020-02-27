# coding=utf-8
# 此文件负责定义一些常量
# 石油组学软件 petromics software


class ConstValues():
    def __init__(self):
        pass

    # 用于打开调试
    PsIsDebug = True
    # 用于是否可以单独运行
    PsIsSingleRun = True
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
    # 运行提示框弹出时间 1 -> 1s
    PsBeforeRunningPromptBoxTime = 1
    PsAfterRunningPromptBoxTime = 1
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
    PsPeakDisClass = ["N1"]  # PsPeakDisClassIsNeed为False是此字段不起作用
    # 3~10（整数）
    PsPeakDisScanPoints = 5
    PsPeakDisScanPointsMin = 3
    PsPeakDisScanPointsMax = 10

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

    # 峰检测全过程所需要的数据
    # 0~1000000(整数)
    PsPeakDivNoiseThreshold = 15000  # 噪音阈值
    PsPeakDivNoiseThresholdMin = 0
    PsPeakDivNoiseThresholdMax = 1000000
    PsPeakDivNoiseThresholdMaxStr = "1e6"  # 方便设置界面显示
    # 0.0~100.0(浮点数)
    PsPeakDivRelIntensity = 2  # 相对强度阈值，去每张图中，相对强度小于最高峰的0.1%的那些信号
    PsPeakDivRelIntensityMin = 0.0
    PsPeakDivRelIntensityMax = 100.0
    # TODO:未定参数
    PsPeakDivMinimalPeakWidth = 10

