# coding=utf-8
import sys
from MainWin import MainWin
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    # 创建QApplication类的实例
    app = QApplication(sys.argv)
    # 创建一个窗口
    main = MainWin()
    # 进入程序的主循环、并通过exit_()函数确保主循环安全结束
    sys.exit(app.exec_())



