# coding=utf-8
# 此文件负责定义：各个设置参数界面
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *


class SetupInterface():
    def __init__(self):
        # 全局变量初始化
        self.dataInit()

    def dataInit(self):
        # 扣空白所需要返回的数据，数据初值无所谓
        self.deleteBlankIntensity = None
        self.deleteBlankPPM = None
        self.deleteBlankPercentage = None

    #######################################
    # 扣空白设置对话框
    def DeleteBlankSetup(self, defaultIntensity=1000, defalutPPM=1.00, defaultPercentage=50):
        """
        :param defaultIntensity: 默认强度
        :param defalutPPM: 默认PPM
        :param defaultPercentage: 默认百分比
        :return: 返回设置后的强度，PPM，百分比
        """
        self.deleteBlankIntensity = defaultIntensity
        self.deleteBlankPPM = defalutPPM
        self.deleteBlankPercentage = defaultPercentage

        # Intensity对话框
        self.deleteBlankdialog = QDialog()
        self.deleteBlankdialog.setWindowTitle("扣空白参数设置")
        self.deleteBlankdialog.setFixedSize(200, 120)  # 固定窗口大小
        # 创建QLineEdit
        self.deleteBlankEdit1 = QLineEdit()
        self.deleteBlankEdit1.setValidator(QIntValidator())  # 设置int校验器
        self.deleteBlankEdit1.setMaxLength(4)  # 不超过9999
        self.deleteBlankEdit1.setAlignment(Qt.AlignRight)  # 设置右对齐
        self.deleteBlankEdit1.setPlaceholderText(str(defaultIntensity))  # 设置默认显示数值
        self.deleteBlankEdit1.textChanged.connect(self.HandleTextChangedIntensity)
        #edit1.setFont(QFont("Arial", 10))  # 设置字体

        # PPM对话框
        self.deleteBlankEdit2 = QLineEdit()  # ppm 范围[0.01,99.99]浮点数
        doubleValidator = QDoubleValidator()
        doubleValidator.setRange(0, 100)  # 设置校验器范围
        doubleValidator.setNotation(QDoubleValidator.StandardNotation)  # 必须有这一句校验器设置的范围才有效
        doubleValidator.setDecimals(2)  # 设置校验器小数点位数
        self.deleteBlankEdit2.setValidator(doubleValidator)  # 设置浮点数校验器
        self.deleteBlankEdit2.setAlignment(Qt.AlignRight)
        self.deleteBlankEdit2.setPlaceholderText(str(defalutPPM))  # 设置默认显示数值
        self.deleteBlankEdit2.textChanged.connect(self.HandleTextChangedPPM)

        # Percentage对话框
        self.deleteBlankEdit3 = QLineEdit()  # percentage 范围[0,99]整数
        self.deleteBlankEdit3.setValidator(QIntValidator())  # 设置int校验器
        self.deleteBlankEdit3.setMaxLength(2)  # 不超过99
        self.deleteBlankEdit3.setAlignment(Qt.AlignRight)  # 设置右对齐
        self.deleteBlankEdit3.setPlaceholderText(str(defaultPercentage))  # 设置默认显示数值
        self.deleteBlankEdit3.textChanged.connect(self.HandleTextChangedPercentage)

        # 创建按钮
        self.deleteBlankButton1 = QPushButton("确定")
        # self.deleteBlankButton1.resize(30, 10)
        self.deleteBlankButton1.clicked.connect(self.HandleButton1Clicked)

        formLayout = QFormLayout(self.deleteBlankdialog)
        formLayout.addRow(QLabel("intensity"), self.deleteBlankEdit1)
        formLayout.addRow(QLabel("ppm"), self.deleteBlankEdit2)
        formLayout.addRow(QLabel("percentage%"), self.deleteBlankEdit3)
        formLayout.addRow(self.deleteBlankButton1)

        self.deleteBlankdialog.exec()
        return self.deleteBlankIntensity, self.deleteBlankPPM, self.deleteBlankPercentage

    def HandleTextChangedIntensity(self, text):
        if text != "":
            self.deleteBlankIntensity = int(text)

    def HandleTextChangedPPM(self, text):
        if text != "":
            self.deleteBlankPPM = float(text)

    def HandleTextChangedPercentage(self, text):
        if text != "":
            self.deleteBlankPercentage = int(text)

    def HandleButton1Clicked(self):
        self.deleteBlankdialog.close()
    #######################################

