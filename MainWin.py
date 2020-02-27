# coding=utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PromptBox import PromptBox
from Utils import *
from SetupInterface import SetupInterface
from MultiThread import MultiThread


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
        QApplication.setStyle(ConstValues.PsMainWindowStyle)
        # 设置窗口样式
        self.setWindowFlags(Qt.WindowMinimizeButtonHint  # 最小化
                            | Qt.WindowCloseButtonHint  # 关闭
                            )
        # 创建主窗口应用的图标
        self.setWindowIcon(QIcon(ConstValues.PsMainWindowIcon))
        # 设置背景颜色
        self.setObjectName("MainWindow")
        self.setStyleSheet("#MainWindow{background-color:white}")
        # 设置窗口显示内容
        self.initShow()
        # 显示主窗口
        self.show()
        # # 设置初始主窗口显示内容, dll导入错误
        # self.browser = QWebEngineView()
        # self.browser.load(QUrl("https://github.com/"))
        # self.setCentralWidget(self.browser)

    # 设置窗口显示内容
    def initShow(self):
        space = 100
        textList = ["扣空白状态：", "数据库生成状态：", "去同位素状态：", "峰识别状态：", "去假阳性状态：", "峰检测状态："]
        for i in range(len(textList)):
            self.TextLabel(textList[i], 20, (i + 1) * space)

        # 扣空白message
        self.messageLabel1 = QLabel(self)
        self.messageLabel1.setText("未运行")
        self.messageLabel1.resize(180, 50)
        self.messageLabel1.setFont(QFont("Arial", 15))
        self.messageLabel1.move(180, space * 1)
        # 数据库生成message
        self.messageLabel2 = QLabel(self)
        self.messageLabel2.setText("未运行")
        self.messageLabel2.resize(180, 50)
        self.messageLabel2.setFont(QFont("Arial", 15))
        self.messageLabel2.move(180, space * 2)
        # 去同位素message
        self.messageLabel3 = QLabel(self)
        self.messageLabel3.setText("未运行")
        self.messageLabel3.resize(180, 50)
        self.messageLabel3.setFont(QFont("Arial", 15))
        self.messageLabel3.move(180, space * 3)
        # 峰识别message
        self.messageLabel4 = QLabel(self)
        self.messageLabel4.setText("未运行")
        self.messageLabel4.resize(180, 50)
        self.messageLabel4.setFont(QFont("Arial", 15))
        self.messageLabel4.move(180, space * 4)
        # 去假阳性message
        self.messageLabel5 = QLabel(self)
        self.messageLabel5.setText("未运行")
        self.messageLabel5.resize(180, 50)
        self.messageLabel5.setFont(QFont("Arial", 15))
        self.messageLabel5.move(180, space * 5)
        # 峰检测message
        self.messageLabel6 = QLabel(self)
        self.messageLabel6.setText("未运行")
        self.messageLabel6.resize(180, 50)
        self.messageLabel6.setFont(QFont("Arial", 15))
        self.messageLabel6.move(180, space * 6)

    # 主界面文本显示
    def TextLabel(self, text, x, y):
        textLabel = QLabel(self)
        textLabel.resize(180, 50)
        textLabel.setText(text)
        textLabel.setFont(QFont("Arial", 15))
        textLabel.move(x, y)

    # 分区绘制
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)

        size = self.size()

        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(400, 74, 400, size.height())

        painter.end()

    # 全局数据初始化
    def dataInit(self):
        # StartAll函数运行所需要的参数，全部参数
        self.AllData = None
        # 文件路径

        self.sampleFilePath = ""  # 样本文件路径
        self.blankFilePath = ""  # 空白文件路径
        self.outputFilesPath = ""  # 输出文件路径
        if ConstValues.PsIsDebug:
            self.sampleFilePath = "./inputData/350/60%ACN-phenyl-kbd350-3.xlsx"
            self.blankFilePath = "./inputData/test/blank-54.xlsx"

        # 扣空白全过程需要的数据  0~10000（整数）
        self.deleteBlankIntensity = ConstValues.PsDeleteBlankIntensity      # 去空白(参数)：删除Intensity小于deleteBlankIntensity的行
        # 0.00~100.00（浮点数）
        self.deleteBlankPPM = ConstValues.PsDeleteBlankPPM                  # 去空白(参数)：删去样本和空白中相同的mass且intensity相近的mass中的指标
        # 0~100（整数）
        self.deleteBlankPercentage = ConstValues.PsDeleteBlankPercentage    # 去空白(参数)：删去样本和空白中相同的mass且intensity相近的mass中的指标
        self.deleteBlankList = [self.sampleFilePath,  # 格式：字符串
                                self.blankFilePath,  # 格式：字符串
                                self.deleteBlankIntensity,  # 格式：整数
                                self.deleteBlankPPM,  # 格式：浮点数
                                self.deleteBlankPercentage  # 格式：整数
                                ]
        self.deleteBlankResult = None  # 去空白：最终返回的结果（格式：list二维数组，有表头）
        self.deleteBlankIsFinished = False   # 去空白：记录扣空白过程是否完成

        # 数据库生成全过程需要的数据
        self.GDBClass = ConstValues.PsGDBClass        # 数据库生成(参数)：Class类型
        # 1~100（整数）
        self.GDBCarbonRangeLow = ConstValues.PsGDBCarbonRangeLow    # 数据库生成(参数)：carbon rage(碳数范围)最小值(包含)
        self.GDBCarbonRangeHigh = ConstValues.PsGDBCarbonRangeHigh  # 数据库生成(参数)：carbon rage(碳数范围)最大值(包含)
        # 1~30（整数）
        self.GDBDBERageLow = ConstValues.PsGDBDBERageLow            # 数据库生成(参数)：DBE rage(不饱和度范围)最小值(包含)
        self.GDBDBERageHigh = ConstValues.PsGDBDBERageHigh          # 数据库生成(参数)：DBE rage(不饱和度范围)最大值(包含)
        # 50~1500(整数)
        self.GDBM_ZRageLow = ConstValues.PsGDBM_ZRageLow            # 数据库生成(参数)：m/z rage(质荷比范围)最小值(包含)
        self.GDBM_ZRageHigh = ConstValues.PsGDBM_ZRageHigh          # 数据库生成(参数)：m/z rage(质荷比范围)最小值(包含)
        # 离子类型
        self.GDB_MHPostive = ConstValues.PsGDB_MHPostive            # 数据库生成(参数)：正离子，是否选择[M+H]+，True为选中
        self.GDB_MPostive = ConstValues.PsGDB_MPostive              # 数据库生成(参数)：正离子，是否选择M+，True为选中
        self.GDB_MHNegative = ConstValues.PsGDB_MHNegative          # 数据库生成(参数)：负离子，是否选择[M-H]-，True为选中
        self.GDB_MNegative = ConstValues.PsGDB_MNegative            # 数据库生成(参数)：负离子，是否选择M-，True为选中
        self.GDBList = [self.GDBClass,  # 格式：列表，列表中均为字符串
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
        self.DelIsoList = [self.deleteBlankResult,  # 删空白的结果（格式：list二维数组，有表头）
                           self.GDBResult,  # 数据库生成的结果（格式：list二维数组，有表头）
                           self.deleteBlankIntensity,
                           self.DelIsoIntensityX,  # 格式：整数
                           self.DelIso_13C2RelativeIntensity,  # 格式：整数
                           self.DelIsoMassDeviation,  # 格式：浮点数
                           self.DelIsoIsotopeMassDeviation,  # 格式：浮点数
                           self.DelIsoIsotopeIntensityDeviation  # 格式：整数
                           ]
        self.DelIsoResult = None  # 去同位素：最终返回的结果（格式：list二维数组，有表头）
        self.DelIsoIsFinished = False   # 去同位素：记录去同位素过程是否完成

        # 峰识别全过程所需要的数据
        self.TICFilePath = ""  # 总离子流图路径，第一部分
        if ConstValues.PsIsDebug:
            self.TICFilePath = "./inputData/350/60%ACN-phenyl-kbd350-3.txt"
        # 0~10000（整数）
        self.PeakDisContinuityNum = ConstValues.PsPeakDisContinuityNum
        # 0.00~100.00（浮点数）
        self.PeakDisMassDeviation = ConstValues.PsPeakDisMassDeviation
        # 0~30(整数)
        self.PeakDisDiscontinuityPointNum = ConstValues.PsPeakDisDiscontinuityPointNum
        self.PeakDisClassIsNeed = ConstValues.PsPeakDisClassIsNeed  # 第二部分，峰检测
        self.PeakDisClass = ConstValues.PsPeakDisClass
        # 3~10（整数）
        self.PeakDisScanPoints = ConstValues.PsPeakDisScanPoints
        self.PeakDisList = [self.TICFilePath,
                            self.DelIsoResult,
                            self.PeakDisContinuityNum,
                            self.PeakDisMassDeviation,
                            self.PeakDisDiscontinuityPointNum,
                            self.PeakDisClassIsNeed,  # 第二部分
                            self.PeakDisClass,
                            self.PeakDisScanPoints
                            ]
        self.PeakDisResult = None  # 峰识别：最终返回的结果（格式：list二维数组，有表头）
        self.PeakDisIsFinished = False  # 峰识别：记录峰识别过程是否完成

        # 去假阳性全过程所需要的数据
        self.RemoveFPId = ConstValues.PsRemoveFPId  # 1：去同位素之后的内容，2：峰识别之后的内容
        # 0~100（整数）
        self.RemoveFPContinue_CNum = ConstValues.PsRemoveFPContinue_CNum  # 连续碳数
        # 0~100（整数）
        self.RemoveFPContinue_DBENum = ConstValues.PsRemoveFPContinue_DBENum  # 连续DBE数
        self.RemoveFPList = [self.DelIsoResult,
                             self.PeakDisResult,
                             self.RemoveFPId,  # 决定选择哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
                             self.RemoveFPContinue_CNum,
                             self.RemoveFPContinue_DBENum
                             ]
        # 结果是一个三维列表，有两个元素，第一个所有类别去假阳性的结果，第二个是去假阳性后需要峰检测的数据
        self.RemoveFPResult = [[], []]
        self.RemoveFPIsFinished = False

        # 峰检测全过程所需要的数据  0~1000000(整数)
        self.PeakDivNoiseThreshold = ConstValues.PsPeakDivNoiseThreshold  # 噪音阈值
        # 0.0~100.0(浮点数)
        self.PeakDivRelIntensity = ConstValues.PsPeakDivRelIntensity  # # 相对强度阈值
        # TODO:未定参数
        self.PeakDivMinimalPeakWidth = ConstValues.PsPeakDivMinimalPeakWidth
        self.PeakDivList = [self.RemoveFPId,  # 判断选择了哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
                            self.RemoveFPResult[1],  # 去假阳性后的需要峰识别结果
                            self.PeakDivNoiseThreshold,
                            self.PeakDivRelIntensity,
                            self.PeakDivMinimalPeakWidth
                            ]
        self.PeakDivResult = None
        self.PeakDivIsFinished = False

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
        importSampleFile = QAction("导入样本文件", self)  # 添加二级菜单
        file.addAction(importSampleFile)
        importSampleFile.triggered.connect(self.ImportSampleFile)

        importBlankFile = QAction("导入空白文件", self)  # 添加二级菜单
        file.addAction(importBlankFile)
        importBlankFile.triggered.connect(self.ImportBlankFile)

        TICFile = QAction("导入总离子图文件", self)  # 添加二级菜单
        file.addAction(TICFile)
        TICFile.triggered.connect(self.ImportTICFile)

        OutFilesPath = QAction("选择生成文件位置", self)  # 添加二级菜单
        file.addAction(OutFilesPath)
        OutFilesPath.triggered.connect(self.GetOutputFilesPath)

        exitProgram = QAction("退出程序", self)  # 添加二级菜单
        file.addAction(exitProgram)
        exitProgram.triggered.connect(self.QuitApplication)


        # 创建第二个主菜单
        set = bar.addMenu("参数设置")
        deleteBlank = QAction("去空白", self)  # 添加二级菜单
        set.addAction(deleteBlank)
        deleteBlank.triggered.connect(self.DeleteBlankSetup)

        DBSearch = QAction("数据库生成", self)  # 添加二级菜单
        set.addAction(DBSearch)
        DBSearch.triggered.connect(self.GenerateDataBaseSetup)

        deleteIsotope = QAction("去同位素", self)  # 添加二级菜单
        set.addAction(deleteIsotope)
        deleteIsotope.triggered.connect(self.DeleteIsotopeSetup)

        peakDistinguish = QAction("峰识别", self)  # 添加二级菜单
        set.addAction(peakDistinguish)
        peakDistinguish.triggered.connect(self.PeakDistinguishSetup)

        disturbRemove = QAction("去假阳性", self)  # 添加二级菜单
        set.addAction(disturbRemove)
        disturbRemove.triggered.connect(self.RemoveFalsePositiveSetup)

        peakDivision = QAction("峰检测", self)  # 添加二级菜单
        set.addAction(peakDivision)
        peakDivision.triggered.connect(self.PeakDivisionSetup)

    # 设置工具栏
    def toolbar(self):
        # 添加第一个工具栏
        tb1 = self.addToolBar("文件")
        tb1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # 设置图标下显示功能
        # 为第一个工具栏添加按钮
        importSampleFile = QAction(QIcon('./images/open.png'), "sample", self)
        tb1.addAction(importSampleFile)
        importSampleFile.triggered.connect(self.ImportSampleFile)

        importBlankFile = QAction(QIcon('./images/open.png'), "blank", self)
        tb1.addAction(importBlankFile)
        importBlankFile.triggered.connect(self.ImportBlankFile)

        TICFile = QAction(QIcon('./images/open.png'), "TIC", self)
        tb1.addAction(TICFile)
        TICFile.triggered.connect(self.ImportTICFile)

        OutFilesPath = QAction(QIcon('./images/open.png'), "OUT", self)
        tb1.addAction(OutFilesPath)
        OutFilesPath.triggered.connect(self.GetOutputFilesPath)

        exitProgram = QAction(QIcon('./images/close.ico'), "exit", self)
        tb1.addAction(exitProgram)
        exitProgram.triggered.connect(self.QuitApplication)


        # 添加第二个工具栏
        tb2 = self.addToolBar("单项处理开始按钮")
        # tb2.setToolButtonStyle(Qt.ToolButtonTextOnly)  # 设置只显示文本
        tb2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # 设置图标下显示功能
        # 为第二个工具栏添加按钮
        deleteBlank = QAction(QIcon('./images/work/j1.png'), "去空白", self)
        tb2.addAction(deleteBlank)
        deleteBlank.triggered.connect(self.DeleteBlank)

        DBSearch = QAction(QIcon('./images/work/j2.png'), "数据库生成", self)
        tb2.addAction(DBSearch)
        DBSearch.triggered.connect(self.GenerateDataBase)

        deleteIsotope = QAction(QIcon('./images/work/j3.png'), "去同位素", self)
        tb2.addAction(deleteIsotope)
        deleteIsotope.triggered.connect(self.DeleteIsotope)

        peakDistinguish = QAction(QIcon('./images/work/j4.png'), "峰识别", self)
        tb2.addAction(peakDistinguish)
        peakDistinguish.triggered.connect(self.PeakDistinguish)

        disturbRemove = QAction(QIcon('./images/work/j5.png'), "去假阳性", self)
        tb2.addAction(disturbRemove)
        disturbRemove.triggered.connect(self.RemoveFalsePositive)

        peakDivision = QAction(QIcon('./images/work/j6.png'), "峰检测", self)
        tb2.addAction(peakDivision)
        peakDivision.triggered.connect(self.PeakDivision)


        # 添加第三个工具栏
        tb3 = self.addToolBar("全部开始按钮")
        tb3.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # 设置图标下显示功能
        # 为第三个工具栏添加按钮
        allStart = QAction(QIcon('./images/work/j21.png'), "全部开始", self)
        tb3.addAction(allStart)
        allStart.triggered.connect(self.StartAll)

        allReset = QAction(QIcon('./images/work/j12.png'), "重置软件", self)
        tb3.addAction(allReset)
        allReset.triggered.connect(self.ResetProgram)

    # 设置主窗口底部状态栏
    def status(self):
        self.statusBar = self.statusBar()
        nowDate = str(QDate.currentDate().toString("yyyy.MM.dd"))
        self.statusBar.showMessage(ConstValues.PsMainWindowStatusMessage +
                                   "|   日期：" + nowDate, 0)  # 0代表永久显示

    # 导入样本文件，文件路径存在sampleFileName中
    def ImportSampleFile(self):
        # 导入文件，并得到文件名称
        openfile_name = QFileDialog.getOpenFileName(self, '选择样本文件', '', 'Excel files(*.xlsx , *.xls)')
        self.sampleFilePath = openfile_name[0]
        if ConstValues.PsIsDebug:
            print(self.sampleFilePath)

    # 导入空白文件，文件路径存在blankFileName中
    def ImportBlankFile(self):
        # 导入文件，并得到文件名称
        openfile_name = QFileDialog.getOpenFileName(self, '选择空白文件', '', 'Excel files(*.xlsx , *.xls)')
        self.blankFilePath = openfile_name[0]
        if ConstValues.PsIsDebug:
            print(self.blankFilePath)

    # 导入总离子流图文件，文件路径存在TICFilePath中
    def ImportTICFile(self):
        # 导入文件，并得到文件名称
        openfile_name = QFileDialog.getOpenFileName(self, '选择总离子流图文件', '', 'Txt files(*.txt)')
        self.TICFilePath = openfile_name[0]
        # # 文件合法性检查
        # f = open(self.TICFilePath, "r")
        # content = f.read().strip().replace("\n", "\t").replace(" ", "").split("\t")
        # # 去除表头
        # content = content[3:]
        # if len(content) / 3 != int(len(content) / 3):
        #     PromptBox().warningMessage("总离子流图文件(txt)存在问题，请重新选择！")
        #     self.TICFilePath = ""
        if ConstValues.PsIsDebug:
            print(self.TICFilePath)

    # 选择输入的文件存放的文件夹
    def GetOutputFilesPath(self):
        # 导入文件，并得到文件名称
        self.outputFilesPath = QFileDialog.getExistingDirectory(self, '打开文件夹', './')
        if ConstValues.PsIsDebug:
            print(self.outputFilesPath)

    # 重置软件，参数重置
    def ResetProgram(self):
        if PromptBox().informationMessage("是否重置?"):
            self.dataInit()
            self.ResetAssembly()
            PromptBox().informationMessage("已重置.")

    # 复位主窗口中的一些组件（如：标签）
    def ResetAssembly(self):
        self.messageLabel1.setText("未运行")  # 去空白
        self.messageLabel2.setText("未运行")  # 数据库生成
        self.messageLabel3.setText("未运行")  # 去同位素
        self.messageLabel4.setText("未运行")  # 峰识别
        self.messageLabel5.setText("未运行")  # 去同位素
        self.messageLabel6.setText("未运行")  # 峰检测

    # 退出程序
    @staticmethod
    def QuitApplication(self):
        app = QApplication.instance()
        # 退出应用程序
        app.quit()

    # 扣空白参数设置  #######################################
    def DeleteBlankSetup(self):
        # 重新设置参数
        newParameters = SetupInterface().DeleteBlankSetup(self.deleteBlankList[2:])
        # 更新数据
        self.UpdateData("DeleteBlankSetup", newParameters)

    # 数据库生成参数设置
    def GenerateDataBaseSetup(self):
        # 重新设置参数
        newParameters = SetupInterface().GenerateDataBaseSetup(self.GDBList)
        # 更新数据
        self.UpdateData("GenerateDataBaseSetup", newParameters)

    # 去同位素参数设置
    def DeleteIsotopeSetup(self):
        # 重新设置参数
        newParameters = SetupInterface().DeleteIsotopeSetup(self.DelIsoList[3:])
        # 更新数据
        self.UpdateData("DeleteIsotopeSetup", newParameters)

    # 峰识别参数设置
    def PeakDistinguishSetup(self):
        # 重新设置参数
        newParameters = SetupInterface().PeakDistinguishSetup(self.PeakDisList[2:])
        # 更新数据
        self.UpdateData("PeakDistinguishSetup", newParameters)

    # 去假阳性参数设置
    def RemoveFalsePositiveSetup(self):
        # 重新设置参数
        newParameters = SetupInterface().RemoveFalsePositiveSetup(self.RemoveFPList[2:])
        # 更新数据
        self.UpdateData("RemoveFalsePositiveSetup", newParameters)

    # 峰检测参数设置
    def PeakDivisionSetup(self):
        pass

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
        # 生成数据库
        self.StartRunning("GenerateDataBase")
        # 程序开始运行后收尾工作
        self.AfterRunning("GenerateDataBase")

    # 去同位素
    def DeleteIsotope(self):
        # 程序运行前准备工作
        if not self.BeforeRunning("DeleteIsotope"):
            return
        # 去同位素
        self.StartRunning("DeleteIsotope")
        # 程序开始运行后收尾工作
        self.AfterRunning("DeleteIsotope")

    # 峰识别
    def PeakDistinguish(self):
        # 程序运行前准备工作
        if not self.BeforeRunning("PeakDistinguish"):
            return
        # 峰识别
        self.StartRunning("PeakDistinguish")
        # 程序开始运行后收尾工作
        self.AfterRunning("PeakDistinguish")

    # 去假阳性
    def RemoveFalsePositive(self):
        # 程序运行前准备工作
        if not self.BeforeRunning("RemoveFalsePositive"):
            return
        # 去假阳性
        self.StartRunning("RemoveFalsePositive")
        # 程序开始运行后收尾工作
        self.AfterRunning("RemoveFalsePositive")

    # 峰检测
    def PeakDivision(self):
        # 程序运行前准备工作
        if not self.BeforeRunning("PeakDivision"):
            return
        # 去假阳性
        self.StartRunning("PeakDivision")
        # 程序开始运行后收尾工作
        self.AfterRunning("PeakDivision")

    # 辅助函数 #######################################
    def StartAll(self):  # 全部开始
        # 程序运行前准备工作
        if not self.BeforeRunning("StartAll"):
            return
        # 运行全过程
        self.StartRunning("StartAll")
        # 程序开始运行后收尾工作
        self.AfterRunning("StartAll")

    # 多进程数据返回接收
    def HandleData(self, retList):
        if retList[0] == "ClassDeleteBlank":
            self.deleteBlankResult = retList[1]
            self.deleteBlankIsFinished = retList[2]
            # 显示完成提示
            self.messageLabel1.setText("处理完毕!")
            # PromptBox().informationMessageAutoClose("处理完毕！", ConstValues.PsAfterRunningPromptBoxTime)
            self.deleteBlankPromptBox.closeGif()
        elif retList[0] == "ClassGenerateDataBase":
            self.GDBResult = retList[1]
            self.GDBIsFinished = retList[2]
            # 显示完成提示
            self.messageLabel2.setText("处理完毕!")
            self.GDBPromptBox.closeGif()
        elif retList[0] == "ClassDeleteIsotope":
            self.DelIsoResult = retList[1]
            self.DelIsoIsFinished = retList[2]
            # 显示完成提示
            self.messageLabel3.setText("处理完毕!")
            self.DelIsoPromptBox.closeGif()
        elif retList[0] == "ClassPeakDistinguish":
            self.PeakDisResult = retList[1]
            self.PeakDisIsFinished = retList[2]
            # 显示完成提示
            self.messageLabel4.setText("处理完毕!")
            self.PeakDisPromptBox.closeGif()
        elif retList[0] == "ClassRemoveFalsePositive":
            self.RemoveFPResult = retList[1]
            self.RemoveFPIsFinished = retList[2]
            # 显示完成提示
            self.messageLabel5.setText("处理完毕!")
            self.RemoveFPPromptBox.closeGif()
        elif retList[0] == "ClassPeakDivision":
            self.PeakDivResult = retList[1]
            self.PeakDivIsFinished = retList[2]
            # 显示完成提示
            self.messageLabel6.setText("处理完毕!")
            self.PeakDivPromptBox.closeGif()
        elif retList[0] == "StartAll":
            # 更新结果
            self.deleteBlankResult = retList[1]
            self.deleteBlankIsFinished = retList[2]
            self.GDBResult = retList[3]
            self.GDBIsFinished = retList[4]
            self.DelIsoResult = retList[5]
            self.DelIsoIsFinished = retList[6]
            self.PeakDisResult = retList[7]
            self.PeakDisIsFinished = retList[8]
            self.RemoveFPResult = retList[9]
            self.RemoveFPIsFinished = retList[10]
            # 关闭弹出的程序运行指示对话框
            self.StartAllPromptBox.closeGif()
        elif retList[0] == "deleteBlankFinished":
            # 显示完成提示
            self.messageLabel1.setText("处理完毕!")
        elif retList[0] == "GDBFinished":
            # 显示完成提示
            self.messageLabel2.setText("处理完毕!")
        elif retList[0] == "DelIsoFinished":
            # 显示完成提示
            self.messageLabel3.setText("处理完毕!")
        elif retList[0] == "PeakDisFinished":
            # 显示完成提示
            self.messageLabel4.setText("处理完毕!")
        elif retList[0] == "RemoveFPFinished":
            # 显示完成提示
            self.messageLabel5.setText("处理完毕!")
        elif retList[0] == "ClassDeleteBlank Error":
            self.deleteBlankPromptBox.closeGif()
            PromptBox().errorMessage("去空白出现错误!")
        elif retList[0] == "ClassGenerateDataBase Error":
            self.GDBPromptBox.closeGif()
            PromptBox().errorMessage("数据库生成出现错误!")
        elif retList[0] == "ClassDeleteIsotope Error":
            self.DelIsoPromptBox.closeGif()
            PromptBox().errorMessage("去同位素出现错误!")
        elif retList[0] == "ClassPeakDistinguish Error":
            self.PeakDisPromptBox.closeGif()
            PromptBox().errorMessage("峰识别出现错误!")
        elif retList[0] == "ClassRemoveFalsePositive Error":
            self.RemoveFPPromptBox.closeGif()
            PromptBox().errorMessage("去假阳性出现错误!")
        elif retList[0] == "ClassPeakDivision Error":
            self.PeakDivPromptBox.closeGif()
            PromptBox().errorMessage("峰检测出现错误!")
        elif retList[0] == "StartAll Error":
            # 关闭弹出的程序运行指示对话框
            self.StartAllPromptBox.closeGif()
            PromptBox().errorMessage("程序运行出现错误!")

    # 设置：数据更新
    def UpdateData(self, Type, newParameters):
        if Type == "DeleteBlankSetup":
            self.deleteBlankIntensity = newParameters[0]
            self.deleteBlankPPM = newParameters[1]
            self.deleteBlankPercentage = newParameters[2]
            self.deleteBlankList = [self.sampleFilePath,  # 格式：字符串
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
            self.GDBList = [self.GDBClass,  # 格式：列表，列表中均为字符串
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
            self.DelIsoList = [self.deleteBlankResult,  # 删空白的结果（格式：list二维数组，有表头）
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
            self.PeakDisScanPoints = newParameters[5]
            self.PeakDisList = [self.TICFilePath,
                                self.DelIsoResult,
                                self.PeakDisContinuityNum,
                                self.PeakDisMassDeviation,
                                self.PeakDisDiscontinuityPointNum,
                                self.PeakDisClassIsNeed,  # 第二部分
                                self.PeakDisClass,
                                self.PeakDisScanPoints
                                ]

            if ConstValues.PsIsDebug:
                print(self.PeakDisList[2:])
        elif Type == "RemoveFalsePositiveSetup":
            self.RemoveFPId = newParameters[0]
            self.RemoveFPContinue_CNum = newParameters[1]
            self.RemoveFPContinue_DBENum = newParameters[2]
            self.RemoveFPList = [self.DelIsoResult,
                                 self.PeakDisResult,
                                 self.RemoveFPId,  # 决定选择哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
                                 self.RemoveFPContinue_CNum,
                                 self.RemoveFPContinue_DBENum
                                 ]

            if ConstValues.PsIsDebug:
                print(self.RemoveFPList[2:])

    # 程序运行前准备工作
    def BeforeRunning(self, Type):
        if Type == "DeleteBlank":
            # 扣空白前需要先读入数据
            if self.sampleFilePath == "" or self.blankFilePath == "":
                PromptBox().warningMessage(ConstValues.PsDeleteBlankErrorMessage)  # 弹出错误提示
                return False

            # 因为有self.sampleFilePath，self.blankFilePath，所以需要更新self.sampleFilePath,self.blankFilePath（最开始前两项为空字符串）
            self.deleteBlankList = [self.sampleFilePath,  # 格式：字符串
                                    self.blankFilePath,  # 格式：字符串
                                    self.deleteBlankIntensity,  # 格式：整数
                                    self.deleteBlankPPM,  # 格式：浮点数
                                    self.deleteBlankPercentage  # 格式：整数
                                    ]
        elif Type == "GenerateDataBase":
            # 无
            pass
        elif Type == "DeleteIsotope":
            # 单独运行，调试使用
            if ConstValues.PsIsSingleRun:
                self.deleteBlankIsFinished = True
                self.deleteBlankResult = ReadExcelToList(filepath="./intermediateFiles/_1_deleteBlank/DeleteBlank.xlsx",
                                                         hasNan=False)
                self.GDBIsFinished = True
                self.GDBResult = ReadExcelToList(filepath="./intermediateFiles/_2_generateDataBase/GDB.xlsx",
                                                 hasNan=False)

            # 去同位素前需要扣空白，数据库生成
            if (not self.deleteBlankIsFinished) or (not self.GDBIsFinished):
                PromptBox().warningMessage(ConstValues.PsDeleteIsotopeErrorMessage)
                return False

            # 因为有self.deleteBlankResult和self.GDBResult，所以需要更新self.DelIsoList（最开始前两项为空）
            self.DelIsoList = [self.deleteBlankResult,  # 删空白的结果（格式：list二维数组，有表头）
                               self.GDBResult,  # 数据库生成的结果（格式：list二维数组，有表头）
                               self.deleteBlankIntensity,
                               self.DelIsoIntensityX,  # 格式：整数
                               self.DelIso_13C2RelativeIntensity,  # 格式：整数
                               self.DelIsoMassDeviation,  # 格式：浮点数
                               self.DelIsoIsotopeMassDeviation,  # 格式：浮点数
                               self.DelIsoIsotopeIntensityDeviation  # 格式：整数
                               ]
        elif Type == "PeakDistinguish":
            # 扣空白前需要先读入数据
            if self.TICFilePath == "":
                PromptBox().warningMessage(ConstValues.PsPeakDistinguishErrorMessage1)  # 弹出错误提示
                return False
            # 单独运行，调试使用
            if ConstValues.PsIsSingleRun:
                self.DelIsoIsFinished = True
                self.DelIsoResult = ReadExcelToList(filepath="./intermediateFiles/_3_deleteIsotope/DeleteIsotope.xlsx",
                                                    hasNan=True)
            # 峰识别前需要去同位素
            if not self.DelIsoIsFinished:
                PromptBox().warningMessage(ConstValues.PsPeakDistinguishErrorMessage2)
                return False
            # 因为有self.TICFilePath，self.DelIsoResult，所以需要更新self.TICFilePath，self.PeakDisList（最开始第一项为空字符串，第二项为空）
            self.PeakDisList = [self.TICFilePath,
                                self.DelIsoResult,
                                self.PeakDisContinuityNum,
                                self.PeakDisMassDeviation,
                                self.PeakDisDiscontinuityPointNum,
                                self.PeakDisClassIsNeed,  # 第二部分
                                self.PeakDisClass,
                                self.PeakDisScanPoints
                                ]
        elif Type == "RemoveFalsePositive":
            # 单独运行，调试使用
            if ConstValues.PsIsSingleRun:
                if self.RemoveFPId == 1:
                    self.DelIsoIsFinished = True
                    self.DelIsoResult = ReadExcelToList(
                        filepath="./intermediateFiles/_3_deleteIsotope/DeleteIsotope.xlsx", hasNan=True)
                elif self.RemoveFPId == 2:
                    self.PeakDisIsFinished = True
                    self.PeakDisResult = ReadExcelToList(
                        filepath="./intermediateFiles/_4_peakDistinguish/PeakDisPart1.xlsx", hasNan=True)
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
            self.RemoveFPList = [self.DelIsoResult,
                                 self.PeakDisResult,
                                 self.RemoveFPId,  # 决定选择哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
                                 self.RemoveFPContinue_CNum,
                                 self.RemoveFPContinue_DBENum
                                 ]
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
            self.PeakDivList = [self.RemoveFPId,  # 判断选择了哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
                                self.RemoveFPResult[1],  # 去假阳性后的需要峰识别结果
                                self.PeakDivNoiseThreshold,
                                self.PeakDivRelIntensity,
                                self.PeakDivMinimalPeakWidth
                                ]
        elif Type == "StartAll":
            if self.sampleFilePath == "" or self.blankFilePath == "" or self.TICFilePath == "":
                PromptBox().warningMessage(ConstValues.PsDeleteBlankErrorMessage)  # 弹出错误提示
                return False
            self.AllData = [
                [
                    # 去空白
                    self.sampleFilePath,  # 格式：字符串
                    self.blankFilePath,  # 格式：字符串
                    self.deleteBlankIntensity,  # 格式：整数
                    self.deleteBlankPPM,  # 格式：浮点数
                    self.deleteBlankPercentage  # 格式：整数
                ],
                [
                    # 数据库生成
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
                ],
                [
                    # 去同位素
                    self.deleteBlankResult,  # 删空白的结果（格式：list二维数组，有表头）
                    self.GDBResult,  # 数据库生成的结果（格式：list二维数组，有表头）
                    self.deleteBlankIntensity,
                    self.DelIsoIntensityX,  # 格式：整数
                    self.DelIso_13C2RelativeIntensity,  # 格式：整数
                    self.DelIsoMassDeviation,  # 格式：浮点数
                    self.DelIsoIsotopeMassDeviation,  # 格式：浮点数
                    self.DelIsoIsotopeIntensityDeviation  # 格式：整数
                ],
                [
                    # 峰识别
                    self.TICFilePath,
                    self.DelIsoResult,
                    self.PeakDisContinuityNum,
                    self.PeakDisMassDeviation,
                    self.PeakDisDiscontinuityPointNum,
                    self.PeakDisClassIsNeed,  # 第二部分
                    self.PeakDisClass,
                    self.PeakDisScanPoints
                ],
                [
                    self.DelIsoResult,
                    self.PeakDisResult,
                    self.RemoveFPId,  # 决定选择哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
                    self.RemoveFPContinue_CNum,
                    self.RemoveFPContinue_DBENum
                 ],
            ]

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
        elif Type == "StartAll":
            self.StartAllMt = MultiThread("StartAll", self.AllData, self.outputFilesPath)
            self.StartAllMt.signal.connect(self.HandleData)
            self.StartAllMt.start()

    # 程序开始运行后收尾工作
    def AfterRunning(self, Type):
        if Type == "DeleteBlank":
            # 界面显示的提示信息
            # gifQMovie = QMovie("./images/ajax-loading.gif")  # 方式1
            # self.messageLabel1.setMovie(gifQMovie)
            # gifQMovie.start()
            self.messageLabel1.setText("正在处理，请稍后...")  # 方式2
            # 弹出提示框
            # PromptBox().informationMessageAutoClose("即将运行......", ConstValues.PsBeforeRunningPromptBoxTime)
            self.deleteBlankPromptBox = PromptBox()
            self.deleteBlankPromptBox.showGif("正在处理扣空白，请稍后...", "./images/ajax-loading.gif")
        elif Type == "GenerateDataBase":
            # 界面显示的提示信息
            self.messageLabel2.setText("正在处理，请稍后...")  # 文字可以正常显示
            # 弹出提示框
            # PromptBox().informationMessageAutoClose("即将运行......", ConstValues.PsBeforeRunningPromptBoxTime)
            self.GDBPromptBox = PromptBox()
            self.GDBPromptBox.showGif("正在生成数据库，请稍后...", "./images/ajax-loading.gif")
        elif Type == "DeleteIsotope":
            # 界面显示的提示信息
            self.messageLabel3.setText("正在处理，请稍后...")
            # 弹出提示框
            self.DelIsoPromptBox = PromptBox()
            self.DelIsoPromptBox.showGif("正在处理去同位素，请稍后...", "./images/ajax-loading.gif")
        elif Type == "PeakDistinguish":
            # 界面显示的提示信息
            self.messageLabel4.setText("正在处理，请稍后...")
            # 弹出提示框
            self.PeakDisPromptBox = PromptBox()
            self.PeakDisPromptBox.showGif("正在处理峰识别，请稍后...", "./images/ajax-loading.gif")
        elif Type == "RemoveFalsePositive":
            # 界面显示的提示信息
            self.messageLabel5.setText("正在处理，请稍后...")
            # 弹出提示框
            self.RemoveFPPromptBox = PromptBox()
            self.RemoveFPPromptBox.showGif("正在处理去假阳性，请稍后...", "./images/ajax-loading.gif")
        elif Type == "PeakDivision":
            # 界面显示的提示信息
            self.messageLabel6.setText("正在处理，请稍后...")
            # 弹出提示框
            self.PeakDivPromptBox = PromptBox()
            self.PeakDivPromptBox.showGif("正在处理峰检测，请稍后...", "./images/ajax-loading.gif")
        elif Type == "StartAll":
            # 界面显示的提示信息
            self.messageLabel1.setText("正在处理，请稍后...")
            self.messageLabel2.setText("正在处理，请稍后...")
            self.messageLabel3.setText("正在处理，请稍后...")
            self.messageLabel4.setText("正在处理，请稍后...")
            self.messageLabel5.setText("正在处理，请稍后...")
            self.messageLabel6.setText("正在处理，请稍后...")
            # 弹出提示框
            self.StartAllPromptBox = PromptBox()
            self.StartAllPromptBox.showGif("正在处理中，请稍后...", "./images/ajax-loading.gif")



