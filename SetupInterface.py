# coding=utf-8
# 此文件负责定义：各个设置参数界面
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ConstValues import ConstValues
from PromptBox import PromptBox
import qtawesome


class SetupInterface():
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
        self.RemoveFPId = None  # 1：去同位素之后的内容，2：峰识别之后的内容
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
        self.PlotType = None  # 绘图类型

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
    def RegExpQLineEdit(self, reg, text):
        # 设置校验器
        regExpValidator = QRegExpValidator()
        regExpValidator.setRegExp(QRegExp(reg))
        # 创建QLineEdit
        lineEdit = QLineEdit()
        lineEdit.setValidator(regExpValidator)  # 设置校验器
        lineEdit.setPlaceholderText(text)  # 默认显示内容
        lineEdit.setAlignment(Qt.AlignLeft)  # 对齐方式
        lineEdit.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))  # 设置字体
        return lineEdit

    # 设置QLabel
    def GetQLabel(self, text, style=""):
        label = QLabel()
        label.setText(text)
        label.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        label.setStyleSheet(style)
        return label

    #############################################################
    def DeleteBlankSetup(self, parameters):
        # 扣空白设置对话框
        # 设置默认参数
        self.DeleteBlankSetDefaultParameters(parameters)

        # 创建QDialog
        self.deleteBlankDialog = QDialog()
        self.deleteBlankDialog.setWindowTitle("扣空白参数设置")
        self.deleteBlankDialog.setFixedSize(ConstValues.PsSetupFontSize * 25, ConstValues.PsSetupFontSize * 16)  # 固定窗口大小
        self.deleteBlankDialog.setWindowIcon(QIcon(ConstValues.PsMainWindowIcon))
        # self.deleteBlankDialog.setStyleSheet(ConstValues.PsSetupStyle)

        # Intensity对话框
        deleteBlankEdit1 = self.IntQLineEdit(ConstValues.PsDeleteBlankIntensityMin, ConstValues.PsDeleteBlankIntensityMax, str(self.deleteBlankIntensity))
        deleteBlankEdit1.textChanged.connect(lambda : self.HandleTextChangedDeleteBlank("Intensity", deleteBlankEdit1))
        # PPM对话框
        deleteBlankEdit2 = self.DoubleQLineEdit(int(ConstValues.PsDeleteBlankPPMMin), int(ConstValues.PsDeleteBlankPPMMax), 2, str(self.deleteBlankPPM))
        deleteBlankEdit2.textChanged.connect(lambda : self.HandleTextChangedDeleteBlank("PPM", deleteBlankEdit2))
        # Percentage对话框
        deleteBlankEdit3 = self.IntQLineEdit(ConstValues.PsDeleteBlankPercentageMin, ConstValues.PsDeleteBlankPercentageMax, str(self.deleteBlankPercentage))
        deleteBlankEdit3.textChanged.connect(lambda : self.HandleTextChangedDeleteBlank("Percentage", deleteBlankEdit3))
        # 创建按钮
        deleteBlankButton1 = QPushButton("确定")
        deleteBlankButton1.setFixedSize(ConstValues.PsSetupFontSize * 5, ConstValues.PsSetupFontSize * 3)
        deleteBlankButton1.clicked.connect(lambda : self.HBCDeleteBlank(parameters, True))
        deleteBlankButton2 = QPushButton("退出")
        deleteBlankButton2.setFixedSize(ConstValues.PsSetupFontSize * 5, ConstValues.PsSetupFontSize * 3)
        deleteBlankButton2.clicked.connect(lambda : self.HBCDeleteBlank(parameters, False))

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

    #############################################################
    def GenerateDataBaseSetup(self, parameters):
        # 数据库生成设置对话框
        # 设置参数（上一次更改后的参数）
        self.GDBSetDefaultParameters(parameters)

        # 创建QDialog
        self.GDBDialog = QDialog()
        self.GDBDialog.setWindowTitle("数据库生成参数设置")
        self.GDBDialog.setFixedSize(ConstValues.PsSetupFontSize * 52, ConstValues.PsSetupFontSize * 35)  # 固定窗口大小
        self.GDBDialog.setWindowIcon(QIcon(ConstValues.PsMainWindowIcon))
        # self.GDBDialog.setStyleSheet(ConstValues.PsSetupStyle)


        # Class
        GDBEdit1 = self.RegExpQLineEdit("([A-Z0-9]|,)+$", ",".join(self.GDBClass))  # 注意：list需要转为str
        GDBEdit1.textChanged.connect(lambda : self.HandleTextChangedGDB("Class", GDBEdit1))
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

    #############################################################
    def DeleteIsotopeSetup(self, parameters):
        # 去同位素设置对话框
        # 设置默认参数
        self.DeleteIsotopeSetDefaultParameters(parameters)

        # 创建QDialog
        self.deleteIsotopeDialog = QDialog()
        self.deleteIsotopeDialog.setWindowTitle("去同位素参数设置")
        self.deleteIsotopeDialog.setFixedSize(ConstValues.PsSetupFontSize * 35, ConstValues.PsSetupFontSize * 25)  # 固定窗口大小
        self.deleteIsotopeDialog.setWindowIcon(QIcon(ConstValues.PsMainWindowIcon))
        # self.deleteIsotopeDialog.setStyleSheet(ConstValues.PsSetupStyle)

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

    #############################################################
    def PeakDistinguishSetup(self, parameters):
        # 峰识别设置对话框
        # 设置默认参数
        self.PeakDistinguishDefaultParameters(parameters)

        # 创建QDialog
        self.peakDistinguishDialog = QDialog()
        self.peakDistinguishDialog.setWindowTitle("峰识别参数设置")
        self.peakDistinguishDialog.setFixedSize(ConstValues.PsSetupFontSize * 40, ConstValues.PsSetupFontSize * 25)  # 固定窗口大小
        self.peakDistinguishDialog.setWindowIcon(QIcon(ConstValues.PsMainWindowIcon))
        # self.peakDistinguishDialog.setStyleSheet(ConstValues.PsSetupStyle)

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

    #############################################################
    def RemoveFalsePositiveSetup(self, parameters):
        # 去假阳性设置对话框
        # 设置默认参数
        self.RemoveFalsePositiveDefaultParameters(parameters)

        # 创建QDialog
        self.RemoveFPDialog = QDialog()
        self.RemoveFPDialog.setWindowTitle("去假阳性参数设置")
        self.RemoveFPDialog.setFixedSize(ConstValues.PsSetupFontSize * 35, ConstValues.PsSetupFontSize * 20)  # 固定窗口大小
        self.RemoveFPDialog.setWindowIcon(QIcon(ConstValues.PsMainWindowIcon))
        # self.RemoveFPDialog.setStyleSheet(ConstValues.PsSetupStyle)

        # PsRemoveFPId二选一按钮
        RemoveFPQRadioButton1 = QRadioButton("去同位素后的文件")
        RemoveFPQRadioButton1.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        RemoveFPQRadioButton1.toggled.connect(lambda: self.RemoveFalsePositiveQRadioButton(RemoveFPQRadioButton1))
        RemoveFPQRadioButton2 = QRadioButton("峰识别后的文件")
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

    #############################################################
    def PeakDivisionSetup(self, parameters):
        # 峰检测设置对话框，设置默认参数
        self.PeakDivisionDefaultParameters(parameters)

        # 创建QDialog
        self.PeakDivDialog = QDialog()
        self.PeakDivDialog.setWindowTitle("峰检测参数设置")
        self.PeakDivDialog.setFixedSize(ConstValues.PsSetupFontSize * 35, ConstValues.PsSetupFontSize * 20)  # 固定窗口大小
        self.PeakDivDialog.setWindowIcon(QIcon(ConstValues.PsMainWindowIcon))
        # self.PeakDivDialog.setStyleSheet(ConstValues.PsSetupStyle)

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

    #############################################################
    def PlotSetup(self, parameters):
        # 图形生成参数设置对话框，设置默认参数，这是第一个主窗口
        self.PlotDefaultParameters(parameters)

        # 创建QDialog
        self.PlotDialog = QDialog()
        self.PlotDialog.setWindowTitle("图形生成参数设置")
        self.PlotDialog.setFixedSize(ConstValues.PsSetupFontSize * 67, ConstValues.PsSetupFontSize * 40)  # 固定窗口大小
        self.PlotDialog.setWindowIcon(QIcon(ConstValues.PsMainWindowIcon))
        # self.PlotDialog.setStyleSheet(ConstValues.PsSetupStyle)

        # 创建栅格布局
        self.PlotLayout = QGridLayout(self.PlotDialog)

        # 主界面内容设置
        self.PlotMainUIList = self.PlotMainUI(parameters)

        # 运行
        self.PlotDialog.exec()

    # 设置参数为用户上次输入的值
    def PlotDefaultParameters(self, parameters):
        self.PlotType = parameters[0]

    # 用户输入文本后，会进入这个函数处理
    def HandleTextChangedPlot(self, DBType, edit):
        pass

    # 当单选按钮状态改变会进入该函数
    def PlotMainUIRadioButtonState(self, radioButton, Id):  # 用一个整数代表选中了哪个单选按钮
        if radioButton.isChecked():
            if ConstValues.PsIsDebug:
                print(Id)
            self.PlotType = Id

    # HBC：HandleButtonClicked 用户点击 Finished/Cancel后，会进入这个函数处理
    def HBCPlot(self, parameters, isOK):
        if not isOK:  # 点击取消按钮
            self.PlotDefaultParameters(parameters)
            self.PlotDialog.close()
        else:  # 点击确认按钮
            inputState = self.PlotIsParameterValidate()

    # 参数合法性检查
    def PlotIsParameterValidate(self):
        return 0

    # 主设置界面
    def PlotMainUI(self, parameters):
        self.PlotMainUICreateWidget(parameters)
        return self.PlotMainUIAddWidget()

    # 创建主界面控件
    def PlotMainUICreateWidget(self, parameters):
        # 单选按钮
        self.PlotMainUIRadioButton1 = QRadioButton("Class distribution")
        self.PlotMainUIRadioButton2 = QRadioButton("DBE distribution by class")
        self.PlotMainUIRadioButton3 = QRadioButton("Carbon number distribution by class and DBE")
        self.PlotMainUIRadioButton4 = QRadioButton("van Krevelen by class")
        self.PlotMainUIRadioButton5 = QRadioButton("DBE vs. carbon number by class")
        self.PlotMainUIRadioButton6 = QRadioButton("Kendrick mass defect vs. m/z")
        self.PlotMainUIRadioButton1.setChecked(True)
        self.PlotMainUIRadioButton1.toggled.connect(lambda: self.PlotMainUIRadioButtonState(self.PlotMainUIRadioButton1, 1))
        self.PlotMainUIRadioButton2.toggled.connect(lambda: self.PlotMainUIRadioButtonState(self.PlotMainUIRadioButton2, 2))
        self.PlotMainUIRadioButton3.toggled.connect(lambda: self.PlotMainUIRadioButtonState(self.PlotMainUIRadioButton3, 3))
        self.PlotMainUIRadioButton4.toggled.connect(lambda: self.PlotMainUIRadioButtonState(self.PlotMainUIRadioButton4, 4))
        self.PlotMainUIRadioButton5.toggled.connect(lambda: self.PlotMainUIRadioButtonState(self.PlotMainUIRadioButton5, 5))
        self.PlotMainUIRadioButton6.toggled.connect(lambda: self.PlotMainUIRadioButtonState(self.PlotMainUIRadioButton6, 6))
        self.PlotMainUIRadioButton1.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        self.PlotMainUIRadioButton2.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        self.PlotMainUIRadioButton3.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        self.PlotMainUIRadioButton4.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        self.PlotMainUIRadioButton5.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        self.PlotMainUIRadioButton6.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        # Next/Cancel
        self.PlotMainUIButton1 = QPushButton("Next")
        self.PlotMainUIButton1.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)
        self.PlotMainUIButton1.clicked.connect(lambda: self.PlotSubUI_1(parameters))
        self.PlotMainUIButton2 = QPushButton("Cancel")
        self.PlotMainUIButton2.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)
        self.PlotMainUIButton2.clicked.connect(lambda: self.HBCPlot(parameters, False))

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

    # 添加主界面控件
    def PlotMainUIAddWidget(self):
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
        
    # 删除控件
    def PlotRemoveWidget(self, destoryList):
        for item in destoryList:
            # self.PlotLayout.removeWidget(item)  # 不行
            item.setParent(None)

    # 添加控件
    def PlotAddWidget(self, IdStr):
        if IdStr == "MainUI":
            self.PlotMainUIAddWidget()

    # 删除控件后再添加控件
    def PlotRemoveAddWidget(self, destoryList, IdStr):
        self.PlotRemoveWidget(destoryList)
        self.PlotAddWidget(IdStr)

    # 一级子界面
    def PlotSubUI_1(self, parameters):
        # 删除界面中所有控件
        self.PlotRemoveWidget(self.PlotMainUIList)
        # 根据选择绘制一级子界面
        if self.PlotType == 1:  # Class distribution
            self.PlotSubUI_1_1List = self.PlotSubUI_1_1(parameters)
        elif self.PlotType == 2:  # DBE distribution by class
            pass
        elif self.PlotType == 3:  # Carbon number distribution by class and DBE
            pass
        elif self.PlotType == 4:  # van Krevelen by class
            pass
        elif self.PlotType == 5:  # DBE vs. carbon number by class
            pass
        elif self.PlotType == 6:  # Kendrick mass defect vs. m/z
            pass

    # 一级界面下右六个不同的设置界面，第一个：Class distribution
    def PlotSubUI_1_1(self, parameters):
        # 返回上一个界面按钮
        self.PlotSubUI_1_1ButtonPrev = QPushButton("back")
        self.PlotSubUI_1_1ButtonPrev.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)
        self.PlotSubUI_1_1ButtonPrev.clicked.connect(lambda: self.PlotRemoveAddWidget(self.PlotSubUI_1_1List, "MainUI"))
        if ConstValues.PsIconType == 1:
            self.PlotSubUI_1_1ButtonPrev.setIcon(QIcon(QPixmap('./images/back.png')))
        elif ConstValues.PsIconType == 2:
            self.PlotSubUI_1_1ButtonPrev.setIcon(qtawesome.icon(ConstValues.PsqtaIconBack))
        # 复选按钮
        self.PlotSubUI_1_1CheckBox1 = QCheckBox("All")
        self.PlotSubUI_1_1CheckBox1.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        self.PlotSubUI_1_1CheckBox2 = QCheckBox("None")
        self.PlotSubUI_1_1CheckBox2.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))

        # 复选按钮
        self.PlotSubUI_1_1CheckBox3 = QCheckBox("1")
        self.PlotSubUI_1_1Item1 = QListWidgetItem()

        self.PlotSubUI_1_1List = QListWidget()  # 列表控件
        self.PlotSubUI_1_1List.addItem(self.PlotSubUI_1_1Item1)
        self.PlotSubUI_1_1List.setItemWidget(self.PlotSubUI_1_1Item1, self.PlotSubUI_1_1CheckBox3)

        # Next/Cancel
        self.PlotSubUI_1_1Button1 = QPushButton("Next")
        self.PlotSubUI_1_1Button1.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)
        self.PlotSubUI_1_1Button2 = QPushButton("Cancel")
        self.PlotSubUI_1_1Button2.setFixedSize(ConstValues.PsSetupFontSize * 6, ConstValues.PsSetupFontSize * 2)
        self.PlotSubUI_1_1Button2.clicked.connect(lambda: self.HBCPlot(parameters, False))

        # 向 self.PlotDialog 添加控件， 第一个文本
        self.PlotLayout.addWidget(self.PlotSubUI_1_1ButtonPrev, 0, 0, 1, 1)
        self.PlotSubUI_1_1Label1 = self.GetQLabel("")
        self.PlotLayout.addWidget(self.PlotSubUI_1_1Label1, 0, 1, 1, 4)
        # 第二行
        self.PlotLayout.addWidget(self.PlotSubUI_1_1CheckBox1, 1, 0, 1, 1)
        self.PlotLayout.addWidget(self.PlotSubUI_1_1CheckBox2, 1, 1, 1, 1)
        # 第三行
        self.PlotLayout.addWidget(self.PlotSubUI_1_1List, 2, 0, 1, 2)
        # 最后一行
        self.PlotLayout.addWidget(self.PlotSubUI_1_1Button1, 8, 3, 1, 1)
        self.PlotLayout.addWidget(self.PlotSubUI_1_1Button2, 8, 4, 1, 1)

        return [
            self.PlotSubUI_1_1Button1
        ]



