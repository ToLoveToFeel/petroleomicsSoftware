# coding=utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ConstValues import ConstValues
import qtawesome


class ClassHelp:

    def __init__(self, function):
        self.__function = function

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
            imagePath = "./images/help/uiExplain1.png"
            if ConstValues.PsMainWindowStyle == "Qdarkstyle":
                imagePath = "./images/help/uiExplainDark1.png"
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
            explain = "这是一个参数设置界面，我们根据（去空白后的）样本文件里的内容根据Mass去匹配数据库，如果" \
                      "未匹配到，当前Mass结束，继续（去空白后的）样本文件下一条记录的匹配；如果匹配到，则计算匹配到的分" \
                      "子式分子量为12的C元素替换为分子量为13的C元素，分别替换一个和两个，根据替换后分子量在（去空白后的）" \
                      "样本文件中搜索是否有对应的记录，并记录下来。这个步骤最终生成一个excel文件。"
            self.EditShow("搜同位素", explain)
        elif self.__function == "EditHelpPeakDis":
            explain = "这是一个参数设置界面，"
            self.EditShow("峰匹配", explain)
        elif self.__function == "EditHelpRFP":
            explain = "这是一个参数设置界面，"
            self.EditShow("去假阳性", explain)
        elif self.__function == "EditHelpPeakDiv":
            explain = "这是一个参数设置界面，"
            self.EditShow("峰识别", explain)
        elif self.__function == "PlotHelp":
            pass
        elif self.__function == "ModeHelp":
            pass
        elif self.__function == "OtherHelp":
            pass
        elif self.__function == "About":
            dialog = self.CreateDialog("关于", 20, 10)
            label = self.GetQLabel("石油组学软件：v1.0", alignment="AlignCenter")  # 创建label
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
