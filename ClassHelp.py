# coding=utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ConstValues import ConstValues
import qtawesome


class ClassHelp:

    def __init__(self, function, theme=""):
        self.__function = function
        self.MainWindowsStyle = theme

    # 设置QLabel
    def GetQLabel(self, text, style="", alignment=""):
        label = QLabel()
        label.setText(text)
        label.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
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
            dialog.setWindowIcon(
                qtawesome.icon(ConstValues.PsqtaWindowIcon, color=ConstValues.PsqtaWindowIconColor))
        return dialog

    def Help(self):
        if self.__function == "UIHelp":
            dialog = self.CreateDialog("界面介绍", 60, 40)
            dialog.setWindowOpacity(0.94)  # 设置透明度

            label = QLabel()
            imagePath = "./__system/images/help/uiExplain1.png"
            if self.MainWindowsStyle == "Qdarkstyle":
                imagePath = "./__system/images/help/uiExplainDark1.png"
            pixmap = QPixmap(imagePath)
            pixmap = pixmap.scaled(ConstValues.PsSetupFontSize * 55, 4000, Qt.KeepAspectRatio, Qt.SmoothTransformation) # 限制一个即可
            label.setPixmap(pixmap)  # 设置图片
            label.setAlignment(Qt.AlignCenter)  # 居中对齐

            layout = QVBoxLayout(dialog)  # 创建栅格布局
            # 栅格布局添加控件
            layout.addWidget(label)

            dialog.exec()  # 运行
        elif self.__function == "FileHelp":
            dialog = self.CreateDialog("文件帮助", 60, 40)
            dialog.setWindowOpacity(0.94)  # 设置透明度

            label = self.GetQLabel("菜单栏 “文件” 下各项功能解释：", "color:red; font-size:15pt")
            textEdit = QTextEdit()
            textEdit.setFocusPolicy(Qt.NoFocus)  # 禁止编辑
            textEdit.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
            # 显示内容编辑
            sampleExplain = "样本：该文件应该为excel文件，前" + str(ConstValues.PsHeaderLine) + "行为仪器输出信息概况，" \
                            "第" + str(ConstValues.PsHeaderLine+1) + "行为表头:(Mass, Intensity)，之后为两列数据。这个" \
                            "文件生成过程：添加石油的样本经过仪器处理后生成总离子图文件(TIC)，对于每个扫描点的所有Mass" \
                             "和Intensity求平均后得到的结果。"
            blankExplain = "空白：格式同“样本”。这个文件的生成过程：未添加石油的样本经过仪器处理后生成总离子图文件(" \
                           "TIC)，对于每个扫描点的所有Mass和Intensity求平均后得到的结果。"
            TICExplain = "样本TIC：该文件应该为txt文件，第一行是表头(labels, masses, intensity)，之后为数据。这个文件" \
                         "的生成过程：从仪器生成的.raw或者.mzXML文件经处理得到的结果。"
            importExplain = "导入：导入上次运行生成的文件夹中的文件，从而方便绘制图形。如果“输出”未选择的话，应该选择" \
                            "默认生成的intermediateFiles导入，否则应该选择你所选择“输出”文件夹。"
            outputExplain = "输出：选择软件运行过程中文件输出到的文件夹，如果不选择的话，中间文件会生成在intermediateFiles" \
                            "文件夹中。"
            ExitExplain = "退出：退出整个程序。"
            taskbarExplain = "工具栏和菜单栏对应功能一致。"
            showStr = sampleExplain + "\n\n" + blankExplain + "\n\n" + TICExplain + "\n\n" + importExplain + "\n\n" + outputExplain + "\n\n" + ExitExplain + "\n\n\n" + taskbarExplain
            textEdit.setPlainText(showStr)

            layout = QGridLayout(dialog)  # 创建栅格布局
            # 栅格布局添加控件
            layout.addWidget(label, 0, 0, 1, 1)
            layout.addWidget(textEdit, 1, 0, 1, 1)
            dialog.exec()  # 运行
        elif self.__function == "EditHelpDeleteBlank":
            explain = "这是一个参数设置界面，如果没有导入“空白”，虽然能设置数据，但不能运行这一步。" \
                      "这一步的目的：去除样品中无关物质以及仪器产生的影响，使得分析结果更加准确。"
            self.EditShow("去空白", explain)
        elif self.__function == "EditHelpGDB":
            explain = "这是一个参数设置界面，这一步不需要任何输入文件即可运行，根据用户输出参数自动生成信息，" \
                      "信息格式为：（Class, Neutral, Formula, Calc m/z, C, ion），即（类别，不饱和度，分子式，质荷比，" \
                      "碳的数目，仪器离子模式），生成的数据最终存储在excel中。这一步的目的：为后续分子式匹配做准备。"
            self.EditShow("数据库生成", explain)
        elif self.__function == "EditHelpDeleteIso":
            explain = "这是一个参数设置界面，这一步需要“（去空白后的）样本文件”（记为file_A）和生成的数据库文件，我们根据file_A里的内" \
                      "容根据Mass去匹配数据库，如果未匹配到，当前Mass结束，不记录任何信息，继续file_A中下一条记录的匹配；如果匹配到，则计算匹" \
                      "配到的分子式分子量为12的C元素替换为分子量为13的C元素，分别替换一个和两个，根据替换后分子量在file_A中搜" \
                      "索是否有对应的记录，并记录下来；信息格式为（SampleMass，SampleIntensity，Class, Neutral, Formula," \
                      " Calc m/z, C, ion），即（file_A中的Mass，file_A中的Intensity，类别，不饱和度，分子式，质荷比，碳的数目，仪器" \
                      "离子模式）；如果搜到同位素，则记下来，格式为（Mass，Intensity，iostope）。这个步骤最终生成一个excel文件，excel中" \
                      "的内容都是匹配到分子的记录。"
            self.EditShow("搜同位素", explain)
        elif self.__function == "EditHelpPeakDis":
            explain = "这是一个参数设置界面，这一步需要“搜同位素后的结果”（记为file_B）和总离子流图文件（TIC），我们根据file_B中的" \
                      "SampleMass去TIC中搜索是否有基本连续的Mass，并记录TIC中连续的Mass，信息格式为：（SampleMass，Area，startRT，" \
                      "startRTValue，endRT，endRTValue，TICMassMedian，Class，Neutral DBE，Formula，Calc m/z，C，ion），即（file_B" \
                      "中的Mass，TIC中区间[startRT,endRT]对应的Intensity之和，TIC中连续Mass开始的索引（从0开始，到扫描点个数-1结束），" \
                      "开始索引对应的保留时间（RT）的值，TIC中连续Mass结束的索引，结束索引对应的保留时间（RT）的值，TIC中区间[startRT," \
                      "endRT]对应的Mass大于该区间中最大Mass的60%的数据集合的中位数，类别，不饱和度，分子式，质荷比，碳的数目，仪器离子" \
                      "模式）。这个步骤最终生成一个excel文件。"
            self.EditShow("峰匹配", explain)
        elif self.__function == "EditHelpRFP":
            explain = "这是一个参数设置界面，这一步需要“搜同位素后的结果”（记为file_B）或者“峰匹配后的结果”（记为file_C），根据不饱" \
                      "和度（Neutral DBE）以及碳数（C）的连续性，判断是否需要去除，不满足连续条件的会被删除。这个步骤最终生成一个excel文" \
                      "件，格式和file_B或者file_C的格式一致。"
            self.EditShow("去假阳性", explain)
        elif self.__function == "EditHelpPeakDiv":
            explain = "这是一个参数设置界面，这一步需要“去假阳性后的结果（并且去假阳性需要选择的是“峰匹配后的结果”）”（记为file_D），" \
                      "我们已经进行了峰匹配，根据峰匹配的功能解释，我们相当于总离子流图（TIC）提取出一个个提取离子流图（EIC），这一步的" \
                      "目的就是：提取出每一个m/z的色峰谱，并计算峰面积。"
            self.EditShow("峰识别", explain)
        elif self.__function == "PlotHelp":
            dialog = self.CreateDialog("绘图帮助", 60, 40)
            dialog.setWindowOpacity(0.94)  # 设置透明度

            label = self.GetQLabel("菜单栏 “绘图->添加” 下解释：", "color:red; font-size:15pt")
            textEdit = QTextEdit()
            textEdit.setFocusPolicy(Qt.NoFocus)  # 禁止编辑
            textEdit.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
            # 显示内容编辑
            showStr = "需要去假阳性后生成的文件，去假阳性选择了哪个文件，就选择该文件去假阳性之后" \
                      "的文件进行可视化。"
            plot1Explain = "Class distribution：比较不同种类杂原子化合物（class）的相对含量差异。"
            plot2Explain = "DBE distribution by class：比较具有相同class的化合物，DBE的分布情况。"
            plot3Explain = "Carbon number distribution by class and DBEn：比较相同相同class且相" \
                           "同DBE的化合物碳数分布情况（根据这个情况，可以推测一定化合物结构信息）。"
            plot4Explain = "DBE vs carbon number by class：比较相同class化合物的DBE和碳数分布情况。"
            plot5Explain = "Kendrick mass defect （KMD）：KMD图（辅助判断排除假阳性的充分性）。"
            plot6Explain = "Retention time vs carbon number：同系物之间保留时间和碳数的关系（" \
                           "体现液相色谱方法的优越性）。"
            taskbarExplain = "工具栏和菜单栏对应功能一致。"
            showStr = showStr + "\n\n" + plot1Explain + "\n\n" + plot2Explain + "\n\n" + plot3Explain + \
                      "\n\n" + plot4Explain + "\n\n" + plot5Explain + "\n\n" + plot6Explain + "\n\n" + taskbarExplain
            textEdit.setPlainText(showStr)

            layout = QGridLayout(dialog)  # 创建栅格布局
            # 栅格布局添加控件
            layout.addWidget(label, 0, 0, 1, 1)
            layout.addWidget(textEdit, 1, 0, 1, 1)
            dialog.exec()  # 运行
        elif self.__function == "ModeHelp":
            dialog = self.CreateDialog("模式选择帮助", 60, 40)
            dialog.setWindowOpacity(0.94)  # 设置透明度

            label = self.GetQLabel("工具栏 “模式选择” 解释：", "color:red; font-size:15pt")
            textEdit = QTextEdit()
            textEdit.setFocusPolicy(Qt.NoFocus)  # 禁止编辑
            textEdit.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
            # 显示内容编辑
            showStr = "模式选择：此软件一共有6个主要的步骤（除了绘图之外），有些功能可以不必运行，但某些" \
                      "功能运行前必须运行某些功能，用户可以根据需要选择需要运行哪些内容。"
            textEdit.setPlainText(showStr)

            layout = QGridLayout(dialog)  # 创建栅格布局
            # 栅格布局添加控件
            layout.addWidget(label, 0, 0, 1, 1)
            layout.addWidget(textEdit, 1, 0, 1, 1)
            dialog.exec()  # 运行
        elif self.__function == "OtherHelp":
            dialog = self.CreateDialog("其他帮助", 60, 40)
            dialog.setWindowOpacity(0.94)  # 设置透明度

            label = self.GetQLabel("其他帮助：", "color:red; font-size:15pt")
            textEdit = QTextEdit()
            textEdit.setFocusPolicy(Qt.NoFocus)  # 禁止编辑
            textEdit.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
            # 显示内容编辑
            showStr = "用户点击重置软件后，所有参数会重置为默认参数，并且需要重新读入各个文件才能运行"
            textEdit.setPlainText(showStr)

            layout = QGridLayout(dialog)  # 创建栅格布局
            # 栅格布局添加控件
            layout.addWidget(label, 0, 0, 1, 1)
            layout.addWidget(textEdit, 1, 0, 1, 1)
            dialog.exec()  # 运行
        elif self.__function == "About":
            dialog = self.CreateDialog("关于", 20, 10)
            label = self.GetQLabel("石油组学软件：" + ConstValues.PsSoftwareEdition, alignment="AlignCenter")  # 创建label
            layout = QVBoxLayout(dialog)  # 创建垂直布局
            layout.addWidget(label)
            dialog.exec()

    def EditShow(self, name, explain):
        dialog = self.CreateDialog("编辑->" + name, 60, 40)
        dialog.setWindowOpacity(0.94)  # 设置透明度

        label = self.GetQLabel("菜单栏 “编辑->" + name + "” 下功能解释：", "color:red; font-size:15pt")
        textEdit = QTextEdit()
        textEdit.setFocusPolicy(Qt.NoFocus)  # 禁止编辑
        textEdit.setFont(QFont(ConstValues.PsSetupFontType, ConstValues.PsSetupFontSize))
        # 显示内容编辑
        explain = name + ":" + explain
        taskbarExplain = "工具栏对应的“" + name + "”是运行按钮，菜单栏对应的“" + name + "”是参数设置。"
        showStr = explain + "\n\n\n" + taskbarExplain
        textEdit.setPlainText(showStr)

        layout = QGridLayout(dialog)  # 创建栅格布局
        # 栅格布局添加控件
        layout.addWidget(label, 0, 0, 1, 1)
        layout.addWidget(textEdit, 1, 0, 1, 1)
        dialog.exec()  # 运行
