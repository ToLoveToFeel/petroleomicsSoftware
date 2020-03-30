# coding=utf-8
# 此文件负责定义：各个设置参数界面
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ConstValues import ConstValues
from PromptBox import PromptBox
import qtawesome


class SetupInterface:
    def __init__(self):
        # 全局变量初始化
        self.dataInit()

    def dataInit(self):
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
        if ConstValues.PsMainWindowStyle != "Qdarkstyle":
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
        self.deleteBlankDialog = self.CreateDialog("扣空白参数设置", 25, 16)

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
        self.deleteIsotopeDialog = self.CreateDialog("去同位素参数设置", 35, 25)

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
        # 第一行内容，IntensityX
        layout.addWidget(self.GetQLabel("IntensityX(" + str(ConstValues.PsDelIsoIntensityXMin) + "~" + ConstValues.PsDelIsoIntensityXMaxStr + ") :"), 0, 0, 1, 4)
        layout.addWidget(deleteIsotopeEdit1, 0, 4, 1, 2)
        # 第二行内容，13C2RelativeIntensity
        layout.addWidget(self.GetQLabel("13C2RelativeIntensity(" + str(ConstValues.PsDelIso_13C2RelativeIntensityMin) + "~" + str(ConstValues.PsDelIso_13C2RelativeIntensityMax) + "):"), 1, 0, 1, 4)
        layout.addWidget(deleteIsotopeEdit2, 1, 4, 1, 2)
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
        self.RemoveFPDialog = self.CreateDialog("去假阳性参数设置", 35, 20)

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
        self.PlotMainUIRadioButton1.setChecked(True)
        self.PlotMainUIRadioButton1.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        self.PlotMainUIRadioButton2.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        self.PlotMainUIRadioButton3.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        self.PlotMainUIRadioButton4.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        self.PlotMainUIRadioButton5.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        self.PlotMainUIRadioButton6.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
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
                print("PlotMainUIRadioButtonState self.PlotType : ", self.PlotType)

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
            self.PlotSubUI_1ButtonPrev.setIcon(QIcon(QPixmap('./images/back.png')))
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
        if ConstValues.PsMainWindowStyle != "Qdarkstyle":
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
            self.PlotSubUI_2ButtonPrev.setIcon(QIcon(QPixmap('./images/back.png')))
        elif ConstValues.PsIconType == 2:
            self.PlotSubUI_2ButtonPrev.setIcon(qtawesome.icon(ConstValues.PsqtaIconBack))
        self.PlotSubUI_2LabelPrev = self.GetQLabel("")  # 标签
        # 单选按钮
        self.PlotSubUI_2ListWidget = QListWidget()  # 列表控件
        if ConstValues.PsMainWindowStyle != "Qdarkstyle":
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
                    print(self.PlotClassItem[0])
                break

    # -------------------------------------- 第三个：Carbon number distribution by class and DBE，创建控件
    def PlotSubUI_3CreateWidget(self):
        # 返回上一个界面按钮
        self.PlotSubUI_3ButtonPrev = QPushButton("back")
        self.PlotSubUI_3ButtonPrev.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)
        if ConstValues.PsIconType == 1:
            self.PlotSubUI_3ButtonPrev.setIcon(QIcon(QPixmap('./images/back.png')))
        elif ConstValues.PsIconType == 2:
            self.PlotSubUI_3ButtonPrev.setIcon(qtawesome.icon(ConstValues.PsqtaIconBack))
        self.PlotSubUI_3LabelPrev = self.GetQLabel("")  # 标签
        # 单选按钮
        self.PlotSubUI_3ListWidget1 = QListWidget()  # 列表控件1
        if ConstValues.PsMainWindowStyle != "Qdarkstyle":
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
        if ConstValues.PsMainWindowStyle != "Qdarkstyle":
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
                    print("PlotSubUI_3RadioButtonClass self.PlotDBENum : ", self.PlotDBENum)
                break

    # 一级子界面第三个界面 选择需要绘制的DBE
    def PlotSubUI_3RadioButtonDBE(self, Class):
        for num in self.PlotDictionary[Class]:
            if globals()["radioBox_3_2" + str(Class) + str(num)].isChecked():
                self.PlotClassItem[0] = Class
                self.PlotDBENum = num
                if ConstValues.PsIsDebug:
                    print(self.PlotClassItem[0])
                    print(self.PlotDBENum)
                break

    # -------------------------------------- 第四个：DBE vs carbon number by class，创建控件
    def PlotSubUI_4CreateWidget(self):
        # 返回上一个界面按钮
        self.PlotSubUI_4ButtonPrev = QPushButton("back")
        self.PlotSubUI_4ButtonPrev.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)
        if ConstValues.PsIconType == 1:
            self.PlotSubUI_4ButtonPrev.setIcon(QIcon(QPixmap('./images/back.png')))
        elif ConstValues.PsIconType == 2:
            self.PlotSubUI_4ButtonPrev.setIcon(qtawesome.icon(ConstValues.PsqtaIconBack))
        self.PlotSubUI_4LabelPrev = self.GetQLabel("")  # 标签
        # 单选按钮
        self.PlotSubUI_4ListWidget = QListWidget()  # 列表控件
        if ConstValues.PsMainWindowStyle != "Qdarkstyle":
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
                    print(self.PlotClassItem[0])
                break

    # -------------------------------------- 第五个：Kendrick mass defect （KMD），创建控件
    def PlotSubUI_5CreateWidget(self):
        # 返回上一个界面按钮
        self.PlotSubUI_5ButtonPrev = QPushButton("back")
        self.PlotSubUI_5ButtonPrev.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)
        if ConstValues.PsIconType == 1:
            self.PlotSubUI_5ButtonPrev.setIcon(QIcon(QPixmap('./images/back.png')))
        elif ConstValues.PsIconType == 2:
            self.PlotSubUI_5ButtonPrev.setIcon(qtawesome.icon(ConstValues.PsqtaIconBack))
        self.PlotSubUI_5LabelPrev = self.GetQLabel("")  # 标签
        # 单选按钮
        self.PlotSubUI_5ListWidget = QListWidget()  # 列表控件
        if ConstValues.PsMainWindowStyle != "Qdarkstyle":
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
            self.PlotSubUI_6ButtonPrev.setIcon(QIcon(QPixmap('./images/back.png')))
        elif ConstValues.PsIconType == 2:
            self.PlotSubUI_6ButtonPrev.setIcon(qtawesome.icon(ConstValues.PsqtaIconBack))
        self.PlotSubUI_6LabelPrev = self.GetQLabel("")  # 标签
        # 单选按钮
        self.PlotSubUI_6ListWidget1 = QListWidget()  # 列表控件1
        if ConstValues.PsMainWindowStyle != "Qdarkstyle":
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
        if ConstValues.PsMainWindowStyle != "Qdarkstyle":
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
                    print("PlotSubUI_6RadioButtonClass self.PlotDBENum : ", self.PlotDBENum)
                break

    # 一级子界面第三个界面 选择需要绘制的DBE
    def PlotSubUI_6RadioButtonDBE(self, Class):
            for num in self.PlotDictionary[Class]:
                if globals()["radioBox_6_2" + str(Class) + str(num)].isChecked():
                    self.PlotClassItem[0] = Class
                    self.PlotDBENum = num
                    if ConstValues.PsIsDebug:
                        print(self.PlotClassItem[0])
                        print(self.PlotDBENum)
                    break

    # -------------------------------------- 一级子界面对应的二级子界面，命名功能等
    def PlotSubUINameCreateWidget(self):
        # 返回上一个界面按钮
        self.PlotSubUINamePrev = QPushButton("back")
        self.PlotSubUINamePrev.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)
        if ConstValues.PsIconType == 1:
            self.PlotSubUINamePrev.setIcon(QIcon(QPixmap('./images/back.png')))
        elif ConstValues.PsIconType == 2:
            self.PlotSubUINamePrev.setIcon(qtawesome.icon(ConstValues.PsqtaIconBack))
        self.PlotSubUINameLabelPrev = self.GetQLabel("")

        style = "background-color:white;border-width:1px; border-style:solid; border-color:rgb(211, 211, 211);"
        pa = QPalette()
        # 第一行输入内容
        self.PlotSubUINameLabel1 = self.GetQLabel("标题")
        self.PlotSubUINameEdit1 = self.RegExpQLineEdit(text=self.PlotTitleName)
        if ConstValues.PsMainWindowStyle != "Qdarkstyle":
            self.PlotSubUINameEdit1.setStyleSheet("background-color: white;")
        self.PlotSubUINameLabel1_ = self.GetQLabel(text="标题", style=style, alignment="AlignCenter")
        self.PlotSubUINameLabel1_.setFixedSize(ConstValues.PsSetupFontSize * 4, ConstValues.PsSetupFontSize * 2)
        self.PlotSubUINameButton1 = QPushButton("color")
        pa.setColor(QPalette.WindowText, QColor(*self.PlotTitleColor))
        self.PlotSubUINameLabel1_.setPalette(pa)
        # 第二行输入内容
        self.PlotSubUINameLabel2 = self.GetQLabel("x轴名称")
        self.PlotSubUINameEdit2 = self.RegExpQLineEdit(text=self.PlotXAxisName)
        if ConstValues.PsMainWindowStyle != "Qdarkstyle":
            self.PlotSubUINameEdit2.setStyleSheet("background-color: white;")
        self.PlotSubUINameLabel2_ = self.GetQLabel(text="x轴", style=style, alignment="AlignCenter")
        self.PlotSubUINameLabel2_.setFixedSize(ConstValues.PsSetupFontSize * 4, ConstValues.PsSetupFontSize * 2)
        self.PlotSubUINameButton2 = QPushButton("color")
        pa.setColor(QPalette.WindowText, QColor(*self.PlotXAxisColor))
        self.PlotSubUINameLabel2_.setPalette(pa)
        # 第三行输入内容
        self.PlotSubUINameLabel3 = self.GetQLabel("y轴名称")
        self.PlotSubUINameEdit3 = self.RegExpQLineEdit(text=self.PlotYAxisName)
        if ConstValues.PsMainWindowStyle != "Qdarkstyle":
            self.PlotSubUINameEdit3.setStyleSheet("background-color: white;")
        self.PlotSubUINameLabel3_ = self.GetQLabel(text="y轴", style=style, alignment="AlignCenter")
        self.PlotSubUINameLabel3_.setFixedSize(ConstValues.PsSetupFontSize * 4, ConstValues.PsSetupFontSize * 2)
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
            print(color.getRgb())
        p = QPalette()
        p.setColor(QPalette.WindowText, color)
        if DType == 1:  # 标题颜色
            self.PlotSubUINameLabel1_.setPalette(p)
            self.PlotTitleColor = color.getRgb()
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
        if ConstValues.PsSetupStyleEnabled and (ConstValues.PsMainWindowStyle != "Qdarkstyle"):
            self.StartModeDialog.setStyleSheet(ConstValues.PsSetupStyle)

        # 创建控件
        StartModeLabel = self.GetQLabel("Select Run Mode", "font:15pt '楷体'; color:blue;")
        # 单选按钮
        StartModeListWidget = QListWidget()  # 列表控件
        if ConstValues.PsMainWindowStyle != "Qdarkstyle":
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
                    print(self.startMode)
                break




