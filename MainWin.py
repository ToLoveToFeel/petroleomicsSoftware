# coding=utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PromptBox import PromptBox
from Utils import *
from SetupInterface import SetupInterface
from MultiThread import MultiThread
import qtawesome
import math
import traceback
import time


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
        if ConstValues.PsIconType == 1:
            self.setWindowIcon(QIcon(ConstValues.PsWindowIcon))
        elif ConstValues.PsIconType == 2:
            self.setWindowIcon(qtawesome.icon(ConstValues.PsqtaWindowIcon, color=ConstValues.PsqtaWindowIconColor))
        # 设置背景颜色
        self.setObjectName("MainWindow")
        self.setStyleSheet(ConstValues.PsMainBackgroundStyle)
        # 设置透明度
        self.setWindowOpacity(0.98)
        # 设置窗口显示内容
        self.initShow()
        # 显示主窗口
        self.show()

    # -------------------------------------- 设置窗口显示内容
    def initShow(self):
        # 主界面左侧栏目标号，从0开始，每添加一个内容，加1
        self.tabWidgetId = 0
        # 主界面读取文件名称列表，读入相同名称的文件时，需要确认是否覆盖
        self.mainDataNameSet = set()  # 当前显示表格名称集合，里面全是字符串，可增可减
        self.mainDataNameSetAll = set()  # 所有可能需要显示的表格名称集合，里面全是字符串，只增不减
        self.mainNeedCover = False
        # 创建文件夹
        newDirectory = CreateDirectory("", "./intermediateFiles", "/_7_plot")

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.Layout = QGridLayout(self.centralwidget)
        # 创建左右两边Widget框
        self.mainTreeWidget = QTreeWidget()  # 树控件，左边
        self.mainTreeWidget.setColumnCount(1)
        self.mainTreeWidget.setHeaderLabel("Project")
        self.mainTreeWidget.header().setMinimumSectionSize(500)  # 杜文文件名太长，设置这一句有水平滚动条
        self.mainTreeWidget.setFont(QFont(ConstValues.PsTreeFontType, ConstValues.PsTreeFontSize))  # 设置字体和大小
        self.plotStack = QStackedWidget()  # 堆栈窗口控件，右边
        # 主窗口放置左右两大控件
        self.Layout.addWidget(self.mainTreeWidget, 0, 0, 1, 2)
        self.Layout.addWidget(self.plotStack, 0, 2, 1, 8)

        # 树控件设置根节点
        self.mainTreeRoot = QTreeWidgetItem(self.mainTreeWidget)
        self.mainTreeRoot.setText(0, "石油组学数据")
        self.mainTreeRoot.setIcon(0, qtawesome.icon(ConstValues.PsqtaWindowIcon, color=ConstValues.PsqtaWindowIconColor))
        # 树控件创建子节点
        self.mainTreeChild1 = QTreeWidgetItem(self.mainTreeRoot)
        self.mainTreeChild1.setText(0, ConstValues.PsTreeInputFiles)
        self.mainTreeChild1.setIcon(0, qtawesome.icon(ConstValues.PsqtaIconTreeFolder, color=ConstValues.PsqtaIconFolderColor))
        self.mainTreeChild2 = QTreeWidgetItem(self.mainTreeRoot)
        self.mainTreeChild2.setText(0, ConstValues.PsTreeDeleteBlank)
        self.mainTreeChild2.setIcon(0, qtawesome.icon(ConstValues.PsqtaIconTreeFolder, color=ConstValues.PsqtaIconFolderColor))
        self.mainTreeChild3 = QTreeWidgetItem(self.mainTreeRoot)
        self.mainTreeChild3.setText(0, ConstValues.PsTreeGDB)
        self.mainTreeChild3.setIcon(0, qtawesome.icon(ConstValues.PsqtaIconTreeFolder, color=ConstValues.PsqtaIconFolderColor))
        self.mainTreeChild4 = QTreeWidgetItem(self.mainTreeRoot)
        self.mainTreeChild4.setText(0, ConstValues.PsTreeDelIso)
        self.mainTreeChild4.setIcon(0, qtawesome.icon(ConstValues.PsqtaIconTreeFolder, color=ConstValues.PsqtaIconFolderColor))
        self.mainTreeChild5 = QTreeWidgetItem(self.mainTreeRoot)
        self.mainTreeChild5.setText(0, ConstValues.PsTreePeakDis)
        self.mainTreeChild5.setIcon(0, qtawesome.icon(ConstValues.PsqtaIconTreeFolder, color=ConstValues.PsqtaIconFolderColor))
        self.mainTreeChild6 = QTreeWidgetItem(self.mainTreeRoot)
        self.mainTreeChild6.setText(0, ConstValues.PsTreeRemoveFP)
        self.mainTreeChild6.setIcon(0, qtawesome.icon(ConstValues.PsqtaIconTreeFolder, color=ConstValues.PsqtaIconFolderColor))
        self.mainTreeChild7 = QTreeWidgetItem(self.mainTreeRoot)
        self.mainTreeChild7.setText(0, ConstValues.PsTreePeakDiv)
        self.mainTreeChild7.setIcon(0, qtawesome.icon(ConstValues.PsqtaIconTreeFolder, color=ConstValues.PsqtaIconFolderColor))
        self.mainTreeChild8 = QTreeWidgetItem(self.mainTreeRoot)
        self.mainTreeChild8.setText(0, ConstValues.PsTreePlot)
        self.mainTreeChild8.setIcon(0, qtawesome.icon(ConstValues.PsqtaIconTreeFolder, color=ConstValues.PsqtaIconFolderColor))

        # 展开所有树控件
        self.mainTreeWidget.expandAll()
        # 树控件关联槽函数，显示内容包括excel
        self.mainTreeWidget.clicked.connect(self.onTreeClicked)

        # 创建一个QTabWidget，专门用于存放用于显示的数据(包括excel,txt以及中间生成的数据)
        self.tabWidgetShowData = QTabWidget()
        self.tabWidgetShowData.setFont(QFont(ConstValues.PsMainFontType, ConstValues.PsMainFontSize))
        self.tabWidgetShowData.setFixedWidth(ConstValues.PsMainWindowWidth*8/10)
        style = "QTabBar::tab{background-color: #DCDCDC;}" + \
              "QTabBar::tab:selected{background-color:rbg(255, 255, 255, 0);} "
        self.tabWidgetShowData.setStyleSheet(style)
        self.tabWidgetShowData.setTabsClosable(True)  # 可以关闭
        self.tabWidgetShowData.tabCloseRequested.connect(self.TabWidgetCloseTab)  # 点击叉号后关闭
        self.plotStack.addWidget(self.tabWidgetShowData)  # 添加 QTabWidget，1

        titleList = ["people.png", "dandelion.png"]
        imagePathList = ["./images/people.png", "./images/dandelion.png"]
        self.tabWidget1 = self.CreateQTabWidgetImages(titleList, imagePathList)  # 创建 QTabWidget
        self.plotStack.addWidget(self.tabWidget1)  # 添加 QTabWidget，2
        self.mainTreeChild8_1 = QTreeWidgetItem(self.mainTreeChild8)
        self.mainTreeChild8_1.setText(0, "initShow")
        self.mainTreeChild8_1.setIcon(0, qtawesome.icon(ConstValues.PsqtaIconTreeImage, color=ConstValues.PsqtaIconFolderColor))
        self.mainTreeChild8_1.setSelected(True)
        self.plotStack.setCurrentWidget(self.tabWidget1)

        # TODO:右侧添加内容，测试
        self.tabWidget2, self.tabWidgetLabel2 = self.CreateQTabWidget("./images/feather.png")  # 创建 QTabWidget
        self.plotStack.addWidget(self.tabWidget2)  # 添加 QTabWidget，3
        self.mainTreeChild8_2 = QTreeWidgetItem(self.mainTreeChild8)
        self.mainTreeChild8_2.setText(0, "TODO")
        self.mainTreeChild8_2.setIcon(0, qtawesome.icon(ConstValues.PsqtaIconTreeImage, color=ConstValues.PsqtaIconFolderColor))

        # 右键处理
        self.tabWidgetLabel2.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabWidgetLabel2.customContextMenuRequested.connect(self.rightMenuShow)  # 开放右键策略

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
                print("i am root")
            return
        treeWidgetName = item.parent().text(0)
        indexRow = index.row()

        if treeWidgetName == ConstValues.PsTreeInputFiles \
                or treeWidgetName == ConstValues.PsTreeDeleteBlank \
                or treeWidgetName == ConstValues.PsTreeGDB \
                or treeWidgetName == ConstValues.PsTreeDelIso \
                or treeWidgetName == ConstValues.PsTreePeakDis \
                or treeWidgetName == ConstValues.PsTreeRemoveFP \
                or treeWidgetName == ConstValues.PsTreePeakDiv:
            myName = item.text(0)
            if myName not in self.mainDataNameSet:  # 如果当前tab没显示在主界面上，添加到主界面
                self.tabWidgetShowData.addTab(globals()["tableWidget_" + myName], myName)
            self.tabWidgetShowData.setCurrentWidget(globals()["tableWidget_" + myName])  # 切换到当前tab
            self.plotStack.setCurrentIndex(0)
        elif treeWidgetName == ConstValues.PsTreePlot:  # 画图结果
            self.plotStack.setCurrentIndex(indexRow + 1)

        if ConstValues.PsIsDebug:
            print(indexRow)
            print('key=%s' % treeWidgetName)

    # 创建选项卡控件
    def CreateQTabWidgetImages(self, titleList, imagePathList):
        if len(titleList) != len(imagePathList):
            if ConstValues.PsIsDebug:
                print("CreateQTabWidgetImages 列表长度不一致!")
                return
        tabWidget = QTabWidget()
        tabWidget.setFont(QFont(ConstValues.PsMainFontType, ConstValues.PsMainFontSize))
        style = "QTabBar::tab{background-color: #DCDCDC;}" + \
                "QTabBar::tab:selected{background-color:rbg(255, 255, 255, 0);} "
        tabWidget.setStyleSheet(style)
        # 固定 QTabWidget 大小
        tabWidget.setFixedWidth(ConstValues.PsMainWindowWidth * 8 / 10)

        for i in range(len(titleList)):
            imagePath = imagePathList[i]
            title = titleList[i]

            tb = QScrollArea()
            tb.setAlignment(Qt.AlignCenter)
            tb.setStyleSheet("background-color: #FFFFFF;")
            label = QLabel()  # 创建Label
            label.setPixmap(QPixmap(imagePath))
            tb.setWidget(label)

            tabWidget.addTab(tb, title)

        return tabWidget

    # 创建选项卡控件
    def CreateQTabWidget(self,imagePath):
        tabWidget = QTabWidget()
        tabWidget.setFont(QFont(ConstValues.PsMainFontType, ConstValues.PsMainFontSize))
        style = "QTabBar::tab{background-color: #DCDCDC;}" + \
                "QTabBar::tab:selected{background-color:rbg(255, 255, 255, 0);} "
        tabWidget.setStyleSheet(style)
        # 固定 QTabWidget 大小
        tabWidget.setFixedWidth(ConstValues.PsMainWindowWidth*8/10)

        # tb1相关内容
        tb1 = QScrollArea()
        tb1.setAlignment(Qt.AlignCenter)
        tb1.setStyleSheet("background-color: #FFFFFF;")
        label = QLabel()  # 创建Label
        label.setPixmap(QPixmap(imagePath))
        tb1.setWidget(label)

        # tb2相关内容
        tb2 = QWidget()

        tabWidget.addTab(tb1, "图形")
        tabWidget.addTab(tb2, "原始数据")

        return tabWidget, label

    # 关闭 self.tabWidgetShowData 中的一个tab
    def TabWidgetCloseTab(self, index):
        sender = self.sender()
        name = self.tabWidgetShowData.tabText(index)  # 当前tab的名称
        if ConstValues.PsIsDebug:
            print("TabWidgetCloseTab()中sender：", sender)
            print("TabWidgetCloseTab()中name：", name)
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
        # 调整列和行
        tableWidget.resizeColumnsToContents()
        tableWidget.resizeRowsToContents()

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
        # 禁止编辑
        tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        return tableWidget

    # 读入文件后树控件添加一项，并切换到当前数据显示，在 HandleData 调用
    def AddTreeItemShowData(self, parent, name, data, promptBox, icon, functionStr=""):
        # 判断是否需要覆盖原本文件，并进行相应的操作
        if self.mainNeedCover:
            self.tabWidgetShowData.removeTab(self.tabWidgetShowData.indexOf(globals()["tableWidget_" + name]))
        # 记录导入文件的信息
        self.mainDataNameSet.add(name)
        self.mainDataNameSetAll.add(name)
        # 树控件创建对应项
        if not self.mainNeedCover:
            mainTreeChild1_ = QTreeWidgetItem(parent)
            mainTreeChild1_.setText(0, name)
            mainTreeChild1_.setIcon(0, qtawesome.icon(icon, color=ConstValues.PsqtaIconFolderColor))
            # 遍历所有节点，如果选择，则取消选择，因为只可能有一个选择了，所以碰到第一个选择的之后就可以退出
            item = QTreeWidgetItemIterator(self.mainTreeWidget)
            while item.value():
                treeWidgetItem = item.value()
                if ConstValues.PsIsDebug:
                    print(treeWidgetItem)
                    print(treeWidgetItem.text(0))
                if treeWidgetItem.isSelected():
                    treeWidgetItem.setSelected(False)
                treeWidgetItem.setFont(0, QFont(ConstValues.PsTreeFontType, ConstValues.PsTreeFontSize))  # 树控件设置字体大小
                # 到下一个节点
                item += 1
            # 光标选择到当前导入的文件
            mainTreeChild1_.setSelected(True)
        # 创建 QTableWidget
        globals()["tableWidget_" + name] = self.CreateQTableWidget(data)
        # self.tabWidgetShowData 添加该项内容
        if globals()["tableWidget_" + name] is not None:  # # 添加 QTableWidget
            self.tabWidgetShowData.addTab(globals()["tableWidget_" + name], name)
            self.tabWidgetShowData.setCurrentWidget(globals()["tableWidget_" + name])  # 切换到当前tab
        self.plotStack.setCurrentIndex(0)  # 显示导入的数据
        self.mainNeedCover = False  # 下次导入文件默认不需要覆盖，经过检查确定是否需要覆盖
        # 更新状态栏消息
        self.statusSetup(ConstValues.PsMainWindowStatusMessage, functionStr)
        if promptBox is not None:
            promptBox.closeGif()
        # 如果行数过多，不全部显示，提醒用户
        if len(data) > ConstValues.PsMainMaxRowNum:
            message = "文件" + name + "行数多于" + str(ConstValues.PsMainMaxRowNum) + "行, 未完全显示."
            PromptBox().warningMessage(message)

    # 右击选项菜单（Plot / Raw Plot Data）
    def rightMenuShow(self):
        menu = QMenu()
        menu.addAction(QAction("导出到", menu))
        menu.triggered.connect(self.MenuSlot)
        menu.exec_(QCursor.pos())

    # 右击后处理函数
    def MenuSlot(self, act):
        print(act.text())

    # -------------------------------------- 全局数据初始化
    def dataInit(self):
        # StartAll函数运行所需要的参数，全部参数
        self.AllData = None
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
        self.deleteBlankIntensity = ConstValues.PsDeleteBlankIntensity      # 去空白(参数)：删除Intensity小于deleteBlankIntensity的行
        # 0.00~100.00（浮点数）
        self.deleteBlankPPM = ConstValues.PsDeleteBlankPPM                  # 去空白(参数)：删去样本和空白中相同的mass且intensity相近的mass中的指标
        # 0~100（整数）
        self.deleteBlankPercentage = ConstValues.PsDeleteBlankPercentage    # 去空白(参数)：删去样本和空白中相同的mass且intensity相近的mass中的指标
        self.deleteBlankList = [
                                    self.sampleFilePath,  # 格式：字符串
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
        self.DelIsoResult = None  # 去同位素：最终返回的结果（格式：list二维数组，有表头）
        self.DelIsoIsFinished = False   # 去同位素：记录去同位素过程是否完成

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

        # 绘图全过程所需要的数据  记录是否进入过PlotSetup()函数
        self.PlotHasEnter = ConstValues.PsPlotHasEnter
        # 1~6(整数)
        self.PlotType = ConstValues.PsPlotType  # 绘图类型
        self.PlotClassList = ConstValues.PsPlotClassList  # 列表，需要绘制的类型，例子：["CH", "N1"]
        self.PlotTitleName = ConstValues.PsPlotTitleName  # 标题名称
        self.PlotTitleColor = ConstValues.PsPlotTitleColor  # 标题颜色
        self.PlotXAxisName = ConstValues.PsPlotXAxisName  # x轴名称
        self.PlotXAxisColor = ConstValues.PsPlotXAxisColor  # x轴颜色
        self.PlotYAxisName = ConstValues.PsPlotYAxisName  # y轴名称
        self.PlotYAxisColor = ConstValues.PsPlotYAxisColor  # y轴颜色

        self.PlotList = [
                            self.RemoveFPId,  # 判断选择了哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
                            self.RemoveFPResult[0],  # 所有类别去假阳性的结果，二维列表，有表头
                            self.PlotHasEnter,  # 记录是否进入过PlotSetup()函数
                            self.PlotType,  # 绘图类型
                            self.PlotClassList,  # 列表，需要绘制的类型，例子：["CH", "N1"]
                            self.PlotTitleName,
                            self.PlotTitleColor,
                            self.PlotXAxisName,
                            self.PlotXAxisColor,
                            self.PlotYAxisName,
                            self.PlotYAxisColor
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

        TICFile = QAction("离子图", self)  # 添加二级菜单
        file.addAction(TICFile)
        TICFile.triggered.connect(self.ImportTICFile)

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

        peakDistinguish = QAction("峰识别", self)  # 添加二级菜单
        set.addAction(peakDistinguish)
        peakDistinguish.triggered.connect(self.PeakDistinguishSetup)

        RemoveFP = QAction("去假阳性", self)  # 添加二级菜单
        set.addAction(RemoveFP)
        RemoveFP.triggered.connect(self.RemoveFalsePositiveSetup)

        peakDivision = QAction("峰检测", self)  # 添加二级菜单
        set.addAction(peakDivision)
        peakDivision.triggered.connect(self.PeakDivisionSetup)

        # 创建第三个主菜单
        plot = bar.addMenu("画图")
        addPlot = QAction("添加", self)  # 添加二级菜单
        plot.addAction(addPlot)
        addPlot.triggered.connect(self.SetupAndPlot)

        # 设置字体大小
        bar.setFont(QFont(ConstValues.PsMenuFontType, ConstValues.PsMenuFontSize))
        importSampleFile.setFont(QFont(ConstValues.PsMenuFontType, ConstValues.PsMenuFontSize))
        importBlankFile.setFont(QFont(ConstValues.PsMenuFontType, ConstValues.PsMenuFontSize))
        TICFile.setFont(QFont(ConstValues.PsMenuFontType, ConstValues.PsMenuFontSize))
        OutFilesPath.setFont(QFont(ConstValues.PsMenuFontType, ConstValues.PsMenuFontSize))
        exitProgram.setFont(QFont(ConstValues.PsMenuFontType, ConstValues.PsMenuFontSize))
        deleteBlank.setFont(QFont(ConstValues.PsMenuFontType, ConstValues.PsMenuFontSize))
        DBSearch.setFont(QFont(ConstValues.PsMenuFontType, ConstValues.PsMenuFontSize))
        deleteIsotope.setFont(QFont(ConstValues.PsMenuFontType, ConstValues.PsMenuFontSize))
        peakDistinguish.setFont(QFont(ConstValues.PsMenuFontType, ConstValues.PsMenuFontSize))
        RemoveFP.setFont(QFont(ConstValues.PsMenuFontType, ConstValues.PsMenuFontSize))
        peakDivision.setFont(QFont(ConstValues.PsMenuFontType, ConstValues.PsMenuFontSize))
        plot.setFont(QFont(ConstValues.PsMenuFontType, ConstValues.PsMenuFontSize))

        # 设置图标
        if ConstValues.PsIconType == 1:  # 从图片读取
            importSampleFile.setIcon(QIcon(ConstValues.PsIconOpenFile))
            importBlankFile.setIcon(QIcon(ConstValues.PsIconOpenFile))
            TICFile.setIcon(QIcon(ConstValues.PsIconOpenFile))
            OutFilesPath.setIcon(QIcon(ConstValues.PsIconOpenFile))
            exitProgram.setIcon(QIcon(ConstValues.PsIconExit))
            deleteBlank.setIcon(QIcon(ConstValues.PsIconDeleteBlank))
            DBSearch.setIcon(QIcon(ConstValues.PsIconGDB))
            deleteIsotope.setIcon(QIcon(ConstValues.PsIcondelIso))
            peakDistinguish.setIcon(QIcon(ConstValues.PsIconpeakDis))
            RemoveFP.setIcon(QIcon(ConstValues.PsIconRemoveFP))
            peakDivision.setIcon(QIcon(ConstValues.PsIconpeakDiv))
            addPlot.setIcon(QIcon(ConstValues.PsIconPlot))
        elif ConstValues.PsIconType == 2:  # 来自 qtawesome
            importSampleFile.setIcon(qtawesome.icon(ConstValues.PsqtaIconOpenFileExcel, color=ConstValues.PsqtaColor))
            importBlankFile.setIcon(qtawesome.icon(ConstValues.PsqtaIconOpenFileExcel, color=ConstValues.PsqtaColor))
            TICFile.setIcon(qtawesome.icon(ConstValues.PsqtaIconOpenFileTxt, color=ConstValues.PsqtaColor))
            OutFilesPath.setIcon(qtawesome.icon(ConstValues.PsqtaIconOpenFileOut, color=ConstValues.PsqtaColor))
            exitProgram.setIcon(qtawesome.icon(ConstValues.PsqtaIconExit, color=ConstValues.PsqtaColor))
            deleteBlank.setIcon(qtawesome.icon(ConstValues.PsqtaIconDeleteBlank, color=ConstValues.PsqtaColor))
            DBSearch.setIcon(qtawesome.icon(ConstValues.PsqtaIconGDB, color=ConstValues.PsqtaColor))
            deleteIsotope.setIcon(qtawesome.icon(ConstValues.PsqtaIcondelIso, color=ConstValues.PsqtaColor))
            peakDistinguish.setIcon(qtawesome.icon(ConstValues.PsqtaIconpeakDis, color=ConstValues.PsqtaColor))
            RemoveFP.setIcon(qtawesome.icon(ConstValues.PsqtaIconRemoveFP, color=ConstValues.PsqtaColor))
            peakDivision.setIcon(qtawesome.icon(ConstValues.PsqtaIconpeakDiv, color=ConstValues.PsqtaColor))
            addPlot.setIcon(qtawesome.icon(ConstValues.PsqtaIconPlot, color=ConstValues.PsqtaColor))

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

        TICFile = QAction("离子图", self)
        TICFile.setToolTip("选择需要导入的总离子图文件")
        tb1.addAction(TICFile)
        TICFile.triggered.connect(self.ImportTICFile)

        OutFilesPath = QAction("输出", self)
        OutFilesPath.setToolTip("选择生成文件位置")
        tb1.addAction(OutFilesPath)
        OutFilesPath.triggered.connect(self.GetOutputFilesPath)

        exitProgram = QAction("退出", self)
        exitProgram.setToolTip("退出程序")
        tb1.addAction(exitProgram)
        exitProgram.triggered.connect(self.QuitApplication)

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

        peakDistinguish = QAction("峰识别", self)
        tb2.addAction(peakDistinguish)
        peakDistinguish.triggered.connect(self.PeakDistinguish)

        RemoveFP = QAction("去假阳性", self)
        tb2.addAction(RemoveFP)
        RemoveFP.triggered.connect(self.RemoveFalsePositive)

        self.TBpeakDivision = QAction("峰检测", self)  # 因为需要控制是否使能，所以为全局变量
        tb2.addAction(self.TBpeakDivision)
        self.TBpeakDivision.triggered.connect(self.PeakDivision)
        self.TBpeakDivision.setEnabled(self.PeakDisClassIsNeed)

        plot = QAction("画图", self)
        tb2.addAction(plot)
        plot.triggered.connect(self.SetupAndPlot)

        # 添加第三个工具栏
        tb4 = self.addToolBar("全部开始按钮")
        tb4.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # 设置图标下显示功能
        # 为第三个工具栏添加按钮
        allStart = QAction("全部开始", self)
        tb4.addAction(allStart)
        allStart.triggered.connect(self.StartAll)

        allReset = QAction("重置软件", self)
        allReset.setToolTip("重置所有参数为默认参数")
        tb4.addAction(allReset)
        allReset.triggered.connect(self.ResetProgram)

        # 设置字体大小
        importSampleFile.setFont(QFont(ConstValues.PsToolbarFontType, ConstValues.PsToolbarFontSize))
        importBlankFile.setFont(QFont(ConstValues.PsToolbarFontType, ConstValues.PsToolbarFontSize))
        TICFile.setFont(QFont(ConstValues.PsToolbarFontType, ConstValues.PsToolbarFontSize))
        OutFilesPath.setFont(QFont(ConstValues.PsToolbarFontType, ConstValues.PsToolbarFontSize))
        exitProgram.setFont(QFont(ConstValues.PsToolbarFontType, ConstValues.PsToolbarFontSize))
        deleteBlank.setFont(QFont(ConstValues.PsToolbarFontType, ConstValues.PsToolbarFontSize))
        DBSearch.setFont(QFont(ConstValues.PsToolbarFontType, ConstValues.PsToolbarFontSize))
        deleteIsotope.setFont(QFont(ConstValues.PsToolbarFontType, ConstValues.PsToolbarFontSize))
        peakDistinguish.setFont(QFont(ConstValues.PsToolbarFontType, ConstValues.PsToolbarFontSize))
        RemoveFP.setFont(QFont(ConstValues.PsToolbarFontType, ConstValues.PsToolbarFontSize))
        self.TBpeakDivision.setFont(QFont(ConstValues.PsToolbarFontType, ConstValues.PsToolbarFontSize))
        allStart.setFont(QFont(ConstValues.PsToolbarFontType, ConstValues.PsToolbarFontSize))
        allReset.setFont(QFont(ConstValues.PsToolbarFontType, ConstValues.PsToolbarFontSize))

        # 设置图标
        if ConstValues.PsIconType == 1:  # 从图片读取
            importSampleFile.setIcon(QIcon(ConstValues.PsIconOpenFile))
            importBlankFile.setIcon(QIcon(ConstValues.PsIconOpenFile))
            TICFile.setIcon(QIcon(ConstValues.PsIconOpenFile))
            OutFilesPath.setIcon(QIcon(ConstValues.PsIconOpenFile))
            exitProgram.setIcon(QIcon(ConstValues.PsIconExit))
            deleteBlank.setIcon(QIcon(ConstValues.PsIconDeleteBlank))
            DBSearch.setIcon(QIcon(ConstValues.PsIconGDB))
            deleteIsotope.setIcon(QIcon(ConstValues.PsIcondelIso))
            peakDistinguish.setIcon(QIcon(ConstValues.PsIconpeakDis))
            RemoveFP.setIcon(QIcon(ConstValues.PsIconRemoveFP))
            self.TBpeakDivision.setIcon(QIcon(ConstValues.PsIconpeakDiv))
            plot.setIcon(QIcon(ConstValues.PsIconPlot))
            allStart.setIcon(QIcon(ConstValues.PsIconAllStart))
            allReset.setIcon(QIcon(ConstValues.PsIconAllReset))
        elif ConstValues.PsIconType == 2:  # 来自 qtawesome
            importSampleFile.setIcon(qtawesome.icon(ConstValues.PsqtaIconOpenFileExcel, color=ConstValues.PsqtaColor))
            importBlankFile.setIcon(qtawesome.icon(ConstValues.PsqtaIconOpenFileExcel, color=ConstValues.PsqtaColor))
            TICFile.setIcon(qtawesome.icon(ConstValues.PsqtaIconOpenFileTxt, color=ConstValues.PsqtaColor))
            OutFilesPath.setIcon(qtawesome.icon(ConstValues.PsqtaIconOpenFileOut, color=ConstValues.PsqtaColor))
            exitProgram.setIcon(qtawesome.icon(ConstValues.PsqtaIconExit, color=ConstValues.PsqtaColor))
            deleteBlank.setIcon(qtawesome.icon(ConstValues.PsqtaIconDeleteBlank, color=ConstValues.PsqtaColor))
            DBSearch.setIcon(qtawesome.icon(ConstValues.PsqtaIconGDB, color=ConstValues.PsqtaColor))
            deleteIsotope.setIcon(qtawesome.icon(ConstValues.PsqtaIcondelIso, color=ConstValues.PsqtaColor))
            peakDistinguish.setIcon(qtawesome.icon(ConstValues.PsqtaIconpeakDis, color=ConstValues.PsqtaColor))
            RemoveFP.setIcon(qtawesome.icon(ConstValues.PsqtaIconRemoveFP, color=ConstValues.PsqtaColor))
            self.TBpeakDivision.setIcon(qtawesome.icon(ConstValues.PsqtaIconpeakDiv, color=ConstValues.PsqtaColor))
            plot.setIcon(qtawesome.icon(ConstValues.PsqtaIconPlot, color=ConstValues.PsqtaColor))
            allStart.setIcon(qtawesome.icon(ConstValues.PsqtaIconAllStart, color=ConstValues.PsqtaColor))
            allReset.setIcon(qtawesome.icon(ConstValues.PsqtaIconAllReset, color=ConstValues.PsqtaColor))

    # 设置主窗口底部状态栏
    def status(self):
        self.statusBar = self.statusBar()
        # 设置状态栏背景颜色
        self.statusBar.setStyleSheet(ConstValues.PsStatusStyle)
        # 设置字体显示样式
        style = "color:rgb(0,0,0,250); font-size:15px; font-family: Microsoft YaHei;"
        # 第一条显示的信息
        nowDate = str(QDate.currentDate().toString("yyyy.MM.dd"))
        self.statusContext1 = QLabel(ConstValues.PsMainWindowStatusMessage + "|   日期：" + nowDate)
        self.statusContext1.setStyleSheet(style)
        # 第二条显示的信息
        self.statusContext2 = QLabel("当前处于空闲状态.")
        self.statusContext2.setStyleSheet(style)
        # 状态栏添加显示的信息
        self.statusBar.addPermanentWidget(self.statusContext1, stretch=3)
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

    # 选择输入的文件存放的文件夹
    def GetOutputFilesPath(self):
        # 导入文件，并得到文件名称
        self.outputFilesPath = QFileDialog.getExistingDirectory(self, '选择文件生成到的文件夹', './')
        if ConstValues.PsIsDebug:
            print(self.outputFilesPath)

    # -------------------------------------- 重置软件，参数重置
    def ResetProgram(self):
        if PromptBox().informationMessage("是否重置?"):
            self.dataInit()
            self.ResetAssembly()
            PromptBox().informationMessage("已重置.")

    # 复位主窗口中的一些组件（如：标签）
    def ResetAssembly(self):
        pass

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
        newParameters = SetupInterface().GenerateDataBaseSetup(self.GDBList)
        self.UpdateData("GenerateDataBaseSetup", newParameters)

    # 去同位素参数设置
    def DeleteIsotopeSetup(self):
        newParameters = SetupInterface().DeleteIsotopeSetup(self.DelIsoList[3:])
        self.UpdateData("DeleteIsotopeSetup", newParameters)

    # 峰识别参数设置
    def PeakDistinguishSetup(self):
        newParameters = SetupInterface().PeakDistinguishSetup(self.PeakDisList[2:])
        self.UpdateData("PeakDistinguishSetup", newParameters)

    # 去假阳性参数设置
    def RemoveFalsePositiveSetup(self):
        newParameters = SetupInterface().RemoveFalsePositiveSetup(self.RemoveFPList[2:])
        self.UpdateData("RemoveFalsePositiveSetup", newParameters)

    # 峰检测参数设置
    def PeakDivisionSetup(self):
        newParameters = SetupInterface().PeakDivisionSetup(self.PeakDivList[3:])
        self.UpdateData("PeakDivisionSetup", newParameters)

    def PlotSetup(self):
        if ConstValues.PsIsSingleRun:  # 读取文件需要花费一些时间，所以界面会延迟一下
            self.RemoveFPIsFinished = True
            filePath = "./intermediateFiles/_5_removeFalsePositive/" + ConstValues.PsNameRemoveFPFrom_PeakDisResult
            self.RemoveFPResult[0] = ReadExcelToList(filepath=filePath, hasNan=True)
        # 画图前前需要先读入数据
        if not self.RemoveFPIsFinished:
            PromptBox().warningMessage(ConstValues.PsPlotErrorMessage)  # 弹出错误提示
            return
        # 更新数据
        self.PlotList = [
            self.RemoveFPId,  # 判断选择了哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
            self.RemoveFPResult[0],  # 所有类别去假阳性的结果，二维列表，有表头
            self.PlotHasEnter,  # 记录是否进入过PlotSetup()函数
            self.PlotType,  # 绘图类型
            self.PlotClassList,  # 列表，需要绘制的类型，例子：["CH", "N1"]
            self.PlotTitleName,
            self.PlotTitleColor,
            self.PlotXAxisName,
            self.PlotXAxisColor,
            self.PlotYAxisName,
            self.PlotYAxisColor
        ]
        newParameters = SetupInterface().PlotSetup(self.PlotList)
        self.UpdateData("PlotSetup", newParameters)

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

    # 去同位素
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
        pass

    # 全部开始
    def StartAll(self):
        if not self.BeforeRunning("StartAll"):
            return
        self.StartRunning("StartAll")
        self.AfterRunning("StartAll")

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
                promptBox = self.deleteBlankPromptBox
                icon = ConstValues.PsqtaIconOpenFileExcel
                functionStr = "去空白处理完毕！"
                self.AddTreeItemShowData(parent, name, data, promptBox, icon, functionStr)
            elif retList[0] == "ClassGenerateDataBase":
                self.GDBResult = retList[1]
                self.GDBIsFinished = retList[2]
                # 数据显示到界面
                parent = self.mainTreeChild3
                name = ConstValues.PsNameGDB
                data = self.GDBResult
                promptBox = self.GDBPromptBox
                icon = ConstValues.PsqtaIconOpenFileExcel
                functionStr = "数据库生成处理完毕！"
                self.AddTreeItemShowData(parent, name, data, promptBox, icon, functionStr)
            elif retList[0] == "ClassDeleteIsotope":
                self.DelIsoResult = retList[1]
                self.DelIsoIsFinished = retList[2]
                # 数据显示到界面
                parent = self.mainTreeChild4
                name = ConstValues.PsNameDeleteIsotope
                data = self.DelIsoResult
                promptBox = self.DelIsoPromptBox
                icon = ConstValues.PsqtaIconOpenFileExcel
                functionStr = "找同位素处理完毕！"
                self.AddTreeItemShowData(parent, name, data, promptBox, icon, functionStr)
            elif retList[0] == "ClassPeakDistinguish":
                self.PeakDisResult = retList[1]  # 列表，有三个数据
                self.PeakDisIsFinished = retList[2]
                # 数据显示到界面
                parent = self.mainTreeChild5
                name = ConstValues.PsNamePeakDistinguish
                data = self.PeakDisResult[0]
                promptBox = self.DelIsoPromptBox
                icon = ConstValues.PsqtaIconOpenFileExcel
                functionStr = "峰识别处理完毕！"
                self.AddTreeItemShowData(parent, name, data, promptBox, icon, functionStr)
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
                promptBox = self.RemoveFPPromptBox
                icon = ConstValues.PsqtaIconOpenFileExcel
                functionStr = "去假阳性处理完毕！"
                self.AddTreeItemShowData(parent, name, data, promptBox, icon, functionStr)
            elif retList[0] == "ClassPeakDivision":
                self.PeakDivResult = retList[1]
                self.PeakDivIsFinished = retList[2]
                # 数据显示到界面
                parent = self.mainTreeChild7
                name = ConstValues.PsNamePeakDivision
                data = self.PeakDivResult
                promptBox = self.PeakDivPromptBox
                icon = ConstValues.PsqtaIconOpenFileExcel
                functionStr = "峰检测处理完毕！"
                self.AddTreeItemShowData(parent, name, data, promptBox, icon, functionStr)
            elif retList[0] == "StartAll":
                # 更新状态
                self.StartAllPromptBox.closeGif()
            elif retList[0] == "deleteBlankFinished":
                self.deleteBlankResult = retList[1]
                self.deleteBlankIsFinished = retList[2]
                # 数据显示到界面
                parent = self.mainTreeChild2
                name = ConstValues.PsNameDeleteBlank
                data = self.deleteBlankResult
                icon = ConstValues.PsqtaIconOpenFileExcel
                functionStr = "去空白处理完毕！"
                self.AddTreeItemShowData(parent, name, data, None, icon, functionStr)
            elif retList[0] == "GDBFinished":
                self.GDBResult = retList[1]
                self.GDBIsFinished = retList[2]
                # 数据显示到界面
                parent = self.mainTreeChild3
                name = ConstValues.PsNameGDB
                data = self.GDBResult
                icon = ConstValues.PsqtaIconOpenFileExcel
                functionStr = "数据库生成处理完毕！"
                self.AddTreeItemShowData(parent, name, data, None, icon, functionStr)
            elif retList[0] == "DelIsoFinished":
                self.DelIsoResult = retList[1]
                self.DelIsoIsFinished = retList[2]
                # 数据显示到界面
                parent = self.mainTreeChild4
                name = ConstValues.PsNameDeleteIsotope
                data = self.DelIsoResult
                icon = ConstValues.PsqtaIconOpenFileExcel
                functionStr = "找同位素处理完毕！"
                self.AddTreeItemShowData(parent, name, data, None, icon, functionStr)
            elif retList[0] == "PeakDisFinished":
                self.PeakDisResult = retList[1]  # 列表，有三个数据
                self.PeakDisIsFinished = retList[2]
                # 数据显示到界面
                parent = self.mainTreeChild5
                name = ConstValues.PsNamePeakDistinguish
                data = self.PeakDisResult[0]
                icon = ConstValues.PsqtaIconOpenFileExcel
                functionStr = "峰识别处理完毕！"
                self.AddTreeItemShowData(parent, name, data, None, icon, functionStr)
            elif retList[0] == "RemoveFPFinished":
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
                self.AddTreeItemShowData(parent, name, data, None, icon, functionStr)
            elif retList[0] == "PeakDivFinished":
                self.PeakDivResult = retList[1]
                self.PeakDivIsFinished = retList[2]
                # 数据显示到界面
                parent = self.mainTreeChild7
                name = ConstValues.PsNamePeakDivision
                data = self.PeakDivResult
                icon = ConstValues.PsqtaIconOpenFileExcel
                functionStr = "峰检测处理完毕！"
                self.AddTreeItemShowData(parent, name, data, None, icon, functionStr)
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
            elif retList[0] == "ImportSampleFile":
                # 读入数据，并显示到主界面
                self.sampleData = retList[1]
                if ConstValues.PsIsDebug:
                    print(self.sampleData)
                # 处理过程
                parent = self.mainTreeChild1
                name = self.sampleFilePath.split("/")[-1]
                data = self.sampleData
                promptBox = self.ImportSampleFilePromptBox
                icon = ConstValues.PsqtaIconOpenFileExcel
                functionStr = "样本导入完成!"
                self.AddTreeItemShowData(parent, name, data, promptBox, icon, functionStr)
            elif retList[0] == "ImportBlankFile":
                # 读入数据，并显示到主界面
                self.blankData = retList[1]
                if ConstValues.PsIsDebug:
                    print(self.blankData)
                # 处理过程
                parent = self.mainTreeChild1
                name = self.blankFilePath.split("/")[-1]
                data = self.blankData
                promptBox = self.ImportBlankFilePromptBox
                icon = ConstValues.PsqtaIconOpenFileExcel
                functionStr = "空白导入完成!"
                self.AddTreeItemShowData(parent, name, data, promptBox, icon, functionStr)
            elif retList[0] == "ImportTICFile":
                # 读入数据，并显示到主界面
                self.TICData = retList[1]
                self.TICDataDictionary = retList[2]
                # if ConstValues.PsIsDebug:
                #     print(self.TICData)
                # 处理过程
                parent = self.mainTreeChild1
                name = self.TICFilePath.split("/")[-1]
                data = self.TICData
                promptBox = self.ImportTICFilePromptBox
                icon = ConstValues.PsqtaIconOpenFileTxt
                functionStr = "总离子流图导入完成!"
                self.AddTreeItemShowData(parent, name, data, promptBox, icon, functionStr)
        except Exception as e:
            if ConstValues.PsIsDebug:
                print("HandleData Error : ", e)
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
            self.PlotHasEnter = newParameters[0]  # 记录是否进入过PlotSetup()函数
            self.PlotType =newParameters[1]  # 绘图类型
            self.PlotClassList = newParameters[2]  # 列表，需要绘制的类型，例子：["CH", "N1"]
            self.PlotTitleName = newParameters[3]  # 标题名称
            self.PlotTitleColor = newParameters[4]  # 标题颜色
            self.PlotXAxisName = newParameters[5]  # x轴名称
            self.PlotXAxisColor = newParameters[6]  # x轴颜色
            self.PlotYAxisName = newParameters[7]  # y轴名称
            self.PlotYAxisColor = newParameters[8]  # y轴颜色
            self.PlotList = [
                self.RemoveFPId,  # 判断选择了哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
                self.RemoveFPResult[0],  # 所有类别去假阳性的结果，二维列表，有表头
                self.PlotHasEnter,  # 记录是否进入过PlotSetup()函数
                self.PlotType,  # 绘图类型
                self.PlotClassList,  # 列表，需要绘制的类型，例子：["CH", "N1"]
                self.PlotTitleName,
                self.PlotTitleColor,
                self.PlotXAxisName,
                self.PlotXAxisColor,
                self.PlotYAxisName,
                self.PlotYAxisColor
            ]

            if ConstValues.PsIsDebug:
                print(self.PlotList[2:])

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
                    self.TICDataDictionary,
                    self.DelIsoResult,
                    self.PeakDisContinuityNum,
                    self.PeakDisMassDeviation,
                    self.PeakDisDiscontinuityPointNum,
                    self.PeakDisClassIsNeed,  # 第二部分
                    self.PeakDisClass,
                ],
                [
                    # 去假阳性
                    self.DelIsoResult,
                    self.PeakDisResult,
                    self.RemoveFPId,  # 决定选择哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
                    self.RemoveFPContinue_CNum,
                    self.RemoveFPContinue_DBENum
                 ],
                [
                    # 峰检测
                    self.RemoveFPId,  # 判断选择了哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
                    self.RemoveFPResult[1],  # 去假阳性后的需要峰识别（第二部分）结果，二维列表，无表头
                    self.PeakDisResult[2],  # 第三个是txt文件中RT值(从小到大排序)
                    self.PeakDivNoiseThreshold,
                    self.PeakDivRelIntensity,
                    self.PeakDivNeedMerge,  # 该参数决定是否需要将溶剂效应的第一个峰融合到第二个峰
                    self.PeakDivNeedGenImage  # 该参数决定是否生成图片信息
                 ]
            ]
            if ConstValues.PsNameDeleteBlank in self.mainDataNameSetAll:
                self.mainNeedCover = PromptBox().warningMessage("是否确定覆盖当前文件?")
                return self.mainNeedCover
        elif Type == "ImportSampleFile":
            # 导入文件，并得到文件名称
            openfile_name = QFileDialog.getOpenFileName(self, '选择样本文件', ConstValues.PsReadFileDefaultDirectoy, 'Excel files(*.xlsx , *.xls)')
            self.sampleFilePath = openfile_name[0]
            if ConstValues.PsIsDebug:
                print(self.sampleFilePath)
            if self.sampleFilePath == "":
                return False
            # # 读入文件合法性检查（是否重名）
            name = self.sampleFilePath.split("/")[-1]
            if name in self.mainDataNameSetAll:
                self.mainNeedCover = PromptBox().warningMessage("是否确定覆盖当前文件?")
                return self.mainNeedCover
        elif Type == "ImportBlankFile":
            # 导入文件，并得到文件名称
            openfile_name = QFileDialog.getOpenFileName(self, '选择空白文件', ConstValues.PsReadFileDefaultDirectoy, 'Excel files(*.xlsx , *.xls)')
            self.blankFilePath = openfile_name[0]
            if ConstValues.PsIsDebug:
                print(self.blankFilePath)
            if self.blankFilePath == "":
                return False
            # # 读入文件合法性检查（是否重名）
            name = self.blankFilePath.split("/")[-1]
            if name in self.mainDataNameSetAll:
                self.mainNeedCover = PromptBox().warningMessage("是否确定覆盖当前文件?")
                return self.mainNeedCover
        elif Type == "ImportTICFile":
            # 导入文件，并得到文件名称
            openfile_name = QFileDialog.getOpenFileName(self, '选择总离子流图文件', ConstValues.PsReadFileDefaultDirectoy, 'Txt files(*.txt)')
            self.TICFilePath = openfile_name[0]
            if ConstValues.PsIsDebug:
                print(self.TICFilePath)
            if self.TICFilePath == "":
                return False
            # # 读入文件合法性检查（是否重名）
            name = self.TICFilePath.split("/")[-1]
            if name in self.mainDataNameSetAll:
                self.mainNeedCover = PromptBox().warningMessage("是否确定覆盖当前文件?")
                return self.mainNeedCover

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
        if Type == "DeleteBlank":
            # 更新状态栏消息
            self.statusSetup(ConstValues.PsMainWindowStatusMessage, "正在处理扣空白，请稍后...")
            # 弹出提示框
            # PromptBox().informationMessageAutoClose("即将运行......", ConstValues.PsBeforeRunningPromptBoxTime)
            self.deleteBlankPromptBox = PromptBox()
            self.deleteBlankPromptBox.showGif("正在处理扣空白，请稍后...", ConstValues.PsIconLoading)
        elif Type == "GenerateDataBase":
            # 更新状态栏消息
            self.statusSetup(ConstValues.PsMainWindowStatusMessage, "正在生成数据库，请稍后...")
            # 弹出提示框
            self.GDBPromptBox = PromptBox()
            self.GDBPromptBox.showGif("正在生成数据库，请稍后...", ConstValues.PsIconLoading)
        elif Type == "DeleteIsotope":
            # 更新状态栏消息
            self.statusSetup(ConstValues.PsMainWindowStatusMessage, "正在处理去同位素，请稍后...")
            # 弹出提示框
            self.DelIsoPromptBox = PromptBox()
            self.DelIsoPromptBox.showGif("正在处理去同位素，请稍后...", ConstValues.PsIconLoading)
        elif Type == "PeakDistinguish":
            # 更新状态栏消息
            self.statusSetup(ConstValues.PsMainWindowStatusMessage, "正在处理去峰识别，请稍后...")
            # 弹出提示框
            self.PeakDisPromptBox = PromptBox()
            self.PeakDisPromptBox.showGif("正在处理峰识别，请稍后...", ConstValues.PsIconLoading)
        elif Type == "RemoveFalsePositive":
            # 更新状态栏消息
            self.statusSetup(ConstValues.PsMainWindowStatusMessage, "正在处理去假阳性，请稍后...")
            # 弹出提示框
            self.RemoveFPPromptBox = PromptBox()
            self.RemoveFPPromptBox.showGif("正在处理去假阳性，请稍后...", ConstValues.PsIconLoading)
        elif Type == "PeakDivision":
            # 更新状态栏消息
            self.statusSetup(ConstValues.PsMainWindowStatusMessage, "正在处理峰检测，请稍后...")
            # 弹出提示框
            self.PeakDivPromptBox = PromptBox()
            self.PeakDivPromptBox.showGif("正在处理峰检测，请稍后...", ConstValues.PsIconLoading)
        elif Type == "StartAll":
            # 更新状态栏消息
            self.statusSetup(ConstValues.PsMainWindowStatusMessage, "正在处理中，请稍后...")
            # 弹出提示框
            self.StartAllPromptBox = PromptBox()
            self.StartAllPromptBox.showGif("正在处理中，请稍后...", ConstValues.PsIconLoading)
        elif Type == "ImportSampleFile":
            # 更新状态栏消息
            self.statusSetup(ConstValues.PsMainWindowStatusMessage, "正在导入样本文件，请稍后...")
            # 弹出提示框
            self.ImportSampleFilePromptBox = PromptBox()
            self.ImportSampleFilePromptBox.showGif("正在导入样本文件，请稍后...", ConstValues.PsIconLoading)
        elif Type == "ImportBlankFile":
            # 更新状态栏消息
            self.statusSetup(ConstValues.PsMainWindowStatusMessage, "正在导入空白文件，请稍后...")
            # 弹出提示框
            self.ImportBlankFilePromptBox = PromptBox()
            self.ImportBlankFilePromptBox.showGif("正在导入空白文件，请稍后...", ConstValues.PsIconLoading)
        elif Type == "ImportTICFile":
            # 更新状态栏消息
            self.statusSetup(ConstValues.PsMainWindowStatusMessage, "正在导入总离子图文件，请稍后...")
            # 弹出提示框
            self.ImportTICFilePromptBox = PromptBox()
            self.ImportTICFilePromptBox.showGif("正在导入总离子图文件，请稍后...", ConstValues.PsIconLoading)

    # 画图
    def SetupAndPlot(self):
        self.PlotSetup()
        self.Plot()
