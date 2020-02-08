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
    PsDeleteIsotopeErrorMessage = "请先扣空白!"


    # 样本文件和空白文件header所在excel中的行数：PsHeaderLine = excel.header - 1
    PsHeaderLine = 7







