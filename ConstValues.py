# coding=utf-8
# 此文件负责定义一些常量
# 石油组学软件 petromics software


class ConstValues():
    def __init__(self):
        pass

    # 用于打开调试
    PsIsDebug = True
    # 主窗口名称
    PsMainWindowTitle = "石油组学软件"
    # 主窗口宽度
    PsMainWindowWidth = 1200
    # 主窗口高度
    PsMainWindowHeight = 800
    # 主窗口底部状态栏显示的信息
    PsMainWindowStatusMessage = "欢迎使用！"
    # 主窗口风格  可选：["Windows", "Fusion", "Macintosh"]
    PsMainWindowStyle = "Macintosh"
    # 扣空白错误提示信息
    PsDeleteBlankErrorMessage = "请选择需要处理的样本文件和空白文件!"
    # 扣同位素错误提示信息
    PsDeleteIsotopeErrorMessage = "请先扣空白和生成数据库!"

    # 样本文件和空白文件header所在excel中的行数：PsHeaderLine = excel.header - 1
    PsHeaderLine = 7

    # 设置框字体以及大小
    PsSetupFontType = "Arial"
    PsSetupFontSize = 12

    # 扣空白设置默认参数
    PsDeleteBlankIntensity = 1000
    PsDeleteBlankPPM = 1.0
    PsDeleteBlankPercentage = 50

    # 数据库生成设置默认参数
    PsGDBClass = ["N1", "N1O1", "N1S1", "CH"]  # 数据库生成(参数)：Class类型
    # 1~100（整数）
    PsGDBCarbonRangeLow = 10  # 数据库生成(参数)：carbon rage(碳数范围)最小值(包含)
    PsGDBCarbonRangeHigh = 14  # 数据库生成(参数)：carbon rage(碳数范围)最大值(包含)
    # 1~30（整数）
    PsGDBDBERageLow = 1  # 数据库生成(参数)：DBE rage(不饱和度范围)最小值(包含)
    PsGDBDBERageHigh = 3  # 数据库生成(参数)：DBE rage(不饱和度范围)最大值(包含)
    # 50~1500(整数)
    PsGDBM_ZRageLow = 50  # 数据库生成(参数)：m/z rage(质荷比范围)最小值(包含)
    PsGDBM_ZRageHigh = 1000  # 数据库生成(参数)：m/z rage(质荷比范围)最小值(包含)
    # 离子类型
    PsGDB_MHPostive = True  # 数据库生成(参数)：正离子，是否选择[M+H]+，True为选中
    PsGDB_MPostive = True  # 数据库生成(参数)：正离子，是否选择M+，True为选中
    PsGDB_MHNegative = False  # 数据库生成(参数)：负离子，是否选择[M-H]-，True为选中
    PsGDB_MNegative = False  # 数据库生成(参数)：负离子，是否选择M-，True为选中


        





