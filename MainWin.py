# coding=utf-8
import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ConstValues import ConstValues
from PromptBox import PromptBox
from ClassDeleteBlank import ClassDeleteBlank
from SetupInterface import SetupInterface


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
        self.setWindowIcon(QIcon('./images/Dragon.ico'))
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
        textList = ["扣空白状态：", "扣空白状态：", "扣空白状态：", "扣空白状态：", "扣空白状态："]
        for i in range(len(textList)):
            self.TextLabel(textList[i], 20, (i + 1) * 120)

        # 扣空白message
        self.messageLabel1 = QLabel(self)
        self.messageLabel1.setText("未运行")
        self.messageLabel1.resize(150, 50)
        self.messageLabel1.setFont(QFont("Arial", 15))
        self.messageLabel1.move(150, 120)
        # 扣空白message
        self.messageLabel2 = QLabel(self)
        self.messageLabel2.setText("未运行")
        self.messageLabel2.resize(150, 50)
        self.messageLabel2.setFont(QFont("Arial", 15))
        self.messageLabel2.move(150, 240)
        # 扣空白message
        self.messageLabel3 = QLabel(self)
        self.messageLabel3.setText("未运行")
        self.messageLabel3.resize(150, 50)
        self.messageLabel3.setFont(QFont("Arial", 15))
        self.messageLabel3.move(150, 360)
        # 扣空白message
        self.messageLabel4 = QLabel(self)
        self.messageLabel4.setText("未运行")
        self.messageLabel4.resize(150, 50)
        self.messageLabel4.setFont(QFont("Arial", 15))
        self.messageLabel4.move(150, 480)
        # 扣空白message
        self.messageLabel5 = QLabel(self)
        self.messageLabel5.setText("未运行")
        self.messageLabel5.resize(150, 50)
        self.messageLabel5.setFont(QFont("Arial", 15))
        self.messageLabel5.move(150, 600)

    # 主界面文本显示
    def TextLabel(self, text, x, y):
        textLabel = QLabel(self)
        textLabel.resize(150, 50)
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
        # 文件路径
        self.sampleFilePath = ""  # 样本文件路径
        self.blankFilePath = ""  # 空白文件路径
        # self.sampleFilePath = "D:/Code/Libratory/大连化物所/石油组学软件/inputData/180-onescan-external.xlsx"
        # self.blankFilePath = "D:/Code/Libratory/大连化物所/石油组学软件/inputData/blank-3.xlsx"
        # 删空白全过程需要的数据
        self.deleteBlankIntensity = 1000     # 删空白：删除Intensity小于deleteBlankIntensity的行
        self.deleteBlankPPM = 1.00           # 删空白：删去样本和空白中相同的mass且intensity相近的mass中的指标
        self.deleteBlankPercentage = 50      # 删空白：删去样本和空白中相同的mass且intensity相近的mass中的指标
        self.deleteBlankIsFinished = False   # 删空白：记录删空白过程是否完成
        self.deleteBlankResult = None        # 删空白：最终返回的结果（格式：numpy二维数组）

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

        exitProgram = QAction("退出程序", self)  # 添加二级菜单
        file.addAction(exitProgram)
        exitProgram.triggered.connect(self.QuitApplication)


        # 创建第二个主菜单
        set = bar.addMenu("参数设置")
        deleteBlank = QAction("扣空白", self)  # 添加二级菜单
        set.addAction(deleteBlank)
        deleteBlank.triggered.connect(self.DeleteBlankSetup)

        deleteIsotope = QAction("扣同位素", self)  # 添加二级菜单
        set.addAction(deleteIsotope)
        deleteIsotope.triggered.connect(self.DeleteIsotopeSetup)

        peakDistinguish = QAction("峰识别", self)  # 添加二级菜单
        set.addAction(peakDistinguish)
        peakDistinguish.triggered.connect(self.PeakDistinguishSetup)

        DBSearch = QAction("数据库搜索", self)  # 添加二级菜单
        set.addAction(DBSearch)
        DBSearch.triggered.connect(self.DataBaseSearchSetup)

        disturbRemove = QAction("干扰排除", self)  # 添加二级菜单
        set.addAction(disturbRemove)
        disturbRemove.triggered.connect(self.DisturbRemoveSetup)

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

        exitProgram = QAction(QIcon('./images/close.ico'), "exit", self)
        tb1.addAction(exitProgram)
        exitProgram.triggered.connect(self.QuitApplication)


        # 添加第二个工具栏
        tb2 = self.addToolBar("单项处理开始按钮")
        # tb2.setToolButtonStyle(Qt.ToolButtonTextOnly)  # 设置只显示文本
        tb2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # 设置图标下显示功能
        # 为第二个工具栏添加按钮
        deleteBlank = QAction(QIcon('./images/work/j1.png'), "扣空白", self)
        tb2.addAction(deleteBlank)
        deleteBlank.triggered.connect(self.DeleteBlank)

        deleteIsotope = QAction(QIcon('./images/work/j2.png'), "扣同位素", self)
        tb2.addAction(deleteIsotope)
        deleteIsotope.triggered.connect(self.DeleteIsotope)

        peakDistinguish = QAction(QIcon('./images/work/j3.png'), "峰识别", self)
        tb2.addAction(peakDistinguish)
        peakDistinguish.triggered.connect(self.PeakDistinguish)

        DBSearch = QAction(QIcon('./images/work/j4.png'), "数据库搜索", self)
        tb2.addAction(DBSearch)
        DBSearch.triggered.connect(self.DataBaseSearch)

        disturbRemove = QAction(QIcon('./images/work/j5.png'), "干扰排除", self)
        tb2.addAction(disturbRemove)
        disturbRemove.triggered.connect(self.DisturbRemove)


        # 添加第三个工具栏
        tb3 = self.addToolBar("全部开始按钮")
        tb3.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)  # 设置图标下显示功能
        # 为第三个工具栏添加按钮
        allStart = QAction(QIcon('./images/work/j21.png'), "全部开始", self)
        tb3.addAction(allStart)

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
        if ConstValues.PsIsDebug == True:
            print(self.sampleFilePath)

    # 导入空白文件，文件路径存在BlankFileName中
    def ImportBlankFile(self):
        # 导入文件，并得到文件名称
        openfile_name = QFileDialog.getOpenFileName(self, '选择空白文件', '', 'Excel files(*.xlsx , *.xls)')
        self.blankFilePath = openfile_name[0]
        if ConstValues.PsIsDebug == True:
            print(self.blankFilePath)

    # 重置软件，参数重置
    def ResetProgram(self):
        reply = PromptBox().informationMessage("是否重置?")
        if reply == True:
            self.dataInit()
            self.ResetAssembly()
            PromptBox().informationMessage("已重置.")

    # 复位主窗口中的一些组件（如：标签）
    def ResetAssembly(self):
        self.messageLabel1.setText("未运行")

    # 退出程序
    def QuitApplication(self):
        app = QApplication.instance()
        # 退出应用程序
        app.quit()

    # 扣空白 #######################################
    def DeleteBlank(self):
        # 扣空白前需要先读入数据
        if self.sampleFilePath == "" or self.blankFilePath == "":
            PromptBox().warningMessage(ConstValues.PsDeleteBlankErrorMessage)  # 弹出错误提示
            return
        # 弹出提示框
        # gifQMovie = QMovie("./images/ajax-loading")  # gif会卡死
        # self.messageLabel1.setMovie(gifQMovie)
        # gifQMovie.start()
        # self.messageLabel1.setPixmap(QPixmap("./images/load.png"))  # 图像可以正常显示
        self.messageLabel1.setText("Running!")  # 文字可以正常显示
        PromptBox().informationMessageAutoClose("即将运行......", 2000)

        # 处理删空白
        cdb = ClassDeleteBlank(self.sampleFilePath, self.blankFilePath)
        # 第一步：过滤掉强度较小的数据
        cdb.DeleteSmallIntensity(self.deleteBlankIntensity)
        # 第二步：删去样本和空白中相同的mass且intensity相近的mass
        self.deleteBlankResult, self.deleteBlankIsFinished = cdb.DeleteSimilarToBlank(self.deleteBlankPPM, self.deleteBlankPercentage)
        # 显示完成提示
        self.messageLabel1.setText("Finished!")
        PromptBox().informationMessageAutoClose("处理完毕！", 2000)


    # 扣同位素
    def DeleteIsotope(self):
        if self.deleteBlankIsFinished == False:
            PromptBox().warningMessage(ConstValues.PsDeleteIsotopeErrorMessage)
            return

    # 峰识别
    def PeakDistinguish(self):
        self.messageLabel1.setPixmap(QPixmap("./images/load.png"))
        for i in range(10000):
            print("hello")

    # 数据库搜索
    def DataBaseSearch(self):
        pass

    # 干扰排除
    def DisturbRemove(self):
        pass

    #######################################
    # 扣空白参数设置
    def DeleteBlankSetup(self):
        self.deleteBlankIntensity, self.deleteBlankPPM, self.deleteBlankPercentage \
            = SetupInterface().DeleteBlankSetup(self.deleteBlankIntensity, self.deleteBlankPPM, self.deleteBlankPercentage)
        if ConstValues.PsIsDebug == True:
            print(self.deleteBlankIntensity, self.deleteBlankPPM, self.deleteBlankPercentage)

    # 扣同位素参数设置
    def DeleteIsotopeSetup(self):
        pass

    # 峰识别参数设置
    def PeakDistinguishSetup(self):
        pass

    # 数据库搜索参数设置
    def DataBaseSearchSetup(self):
        pass

    # 干扰排除参数设置
    def DisturbRemoveSetup(self):
        pass


if __name__ == '__main__':
    # 创建QApplication类的实例
    app = QApplication(sys.argv)
    # 创建一个窗口
    main = MainWin()
    # 进入程序的主循环、并通过exit_()函数确保主循环安全结束
    sys.exit(app.exec_())

