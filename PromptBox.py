# coding=utf-8
# 此文件负责定义：弹出对话框
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class PromptBox():
    def __init__(self):
        pass
        # # 显示图像对话框
        # self.imageDialog = None
        # # 显示图像对话框
        # self.gifDialog = None

    # 警告对话框
    def warningMessage(self, message):
        # 创建对话框
        dialog = QDialog()
        reply = QMessageBox.warning(dialog, '警告', message, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        # reply = QMessageBox.warning(dialog, '警告', message, QMessageBox.Yes)
        return reply == QMessageBox.Yes

    # 消息对话框
    def informationMessage(self, message):
        # 创建对话框
        dialog = QDialog()
        reply = QMessageBox.information(dialog, '消息', message, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        return reply == QMessageBox.Yes

    # 一定时间后自动关闭消息对话框
    def informationMessageAutoClose(self, message, milliSecond):
        infoBox = QMessageBox()  # Message Box that doesn't run
        infoBox.setIcon(QMessageBox.Information)
        infoBox.setText(message)
        infoBox.setWindowTitle("Information")
        infoBox.setStandardButtons(QMessageBox.Ok)
        infoBox.button(QMessageBox.Ok).animateClick(milliSecond)  # 3秒自动关闭
        infoBox.exec_()

    # 显示图片
    def showImage(self, title, filename):
        """
        :param title: 窗口名称
        :param filename: 图片路径
        :return:
        """
        # 创建对话框
        self.imageDialog = QDialog()
        # 设置对话框名称
        self.imageDialog.setWindowTitle(title)
        # 设置对话框弹出后后面的界面不可用
        self.imageDialog.setWindowModality(Qt.ApplicationModal)
        # 创建image标签
        imageLabel = QLabel()
        imageLabel.setPixmap(QPixmap(filename))
        # 将image标签放到layout中
        layout = QVBoxLayout()
        layout.addWidget(imageLabel)
        # 将layout标签放到dialog中
        self.imageDialog.setLayout(layout)
        # 保证提示框一直出现
        self.imageDialog.exec()

    # 显示gif
    def showGif(self, title, filename):
        """
        :param title: 窗口名称
        :param filename: gif路径
        :return:
        """
        # 创建对话框
        self.gifDialog = QDialog()
        # 设置窗口状态
        # self.gifDialog.setWindowFlags(Qt.WindowCloseButtonHint)  # 只显示叉号
        self.gifDialog.setWindowFlags(Qt.WindowMaximizeButtonHint| Qt.MSWindowsFixedSizeDialogHint)  # 禁止使用叉号
        # 设置对话框名称
        self.gifDialog.setWindowTitle(title)
        # 设置对话框弹出后后面的界面不可用
        self.gifDialog.setWindowModality(Qt.ApplicationModal)
        # gif标签
        gifLabel = QLabel()
        self.gifQMovie = QMovie(filename)
        gifLabel.setMovie(self.gifQMovie)
        self.gifQMovie.start()
        # 将gif标签放到layout中
        layout = QVBoxLayout()
        layout.addWidget(gifLabel)
        # 将layout标签放到dialog中
        self.gifDialog.setLayout(layout)
        # 保证提示框一直出现
        self.gifDialog.exec()



