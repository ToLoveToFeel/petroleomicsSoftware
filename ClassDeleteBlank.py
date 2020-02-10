# coding=utf-8
# 此文件负责定义：扣空白
import numpy as np
import pandas as pd
import xlsxwriter
from ConstValues import ConstValues


class ClassDeleteBlank():
    def __init__(self, samplePath, blankPath, parameterList):
        """
        :param samplePath: 样本文件路径
        :param blankPath: 空白文件路径
        :param parameterList: 程序运行所需要的参数列表
        """
        self.sampleData = pd.read_excel(io=samplePath, header=ConstValues.PsHeaderLine)
        self.sampleData.columns = ["Mass", "Intensity"]  # 强制改变列名，方便后面使用
        self.blankData = pd.read_excel(io=blankPath, header=ConstValues.PsHeaderLine)
        self.blankData.columns = ["Mass", "Intensity"]  # 强制改变列名，方便后面使用
        # 可调参数
        assert len(parameterList) == 3, "ClassDeleteBlank参数不对"
        # 1~9999（整数）
        self.deleteBlankIntensity = parameterList[0]
        # 0.01~99.99（浮点数）
        self.deleteBlankPPM = parameterList[1]
        # 1~100（整数）
        self.deleteBlankPercentage = parameterList[2]

    # 负责扣空白
    def DeleteBlank(self):
        self.DeleteSmallIntensity()
        return self.DeleteSimilarToBlank()

    # 删除Intensity小于self.deleteBlankIntensity的行
    def DeleteSmallIntensity(self):
        # 只保留大于intensity的行
        self.sampleData = self.sampleData[self.sampleData.Intensity > self.deleteBlankIntensity]
        self.blankData = self.blankData[self.blankData.Intensity > self.deleteBlankIntensity]
        if ConstValues.PsIsDebug:
            print(self.sampleData.shape[0])  # 180-onescan-external.xlsx处理后：5888
            print(self.blankData.shape[0])  # blank-3.xlsx处理后：3778

    # 删去样本和空白中相同的mass且intensity相近的mass，必须调过DeleteSmallIntensity函数调用此函数才有意义
    def DeleteSimilarToBlank(self):
        """
                    m1:样本中的mass
                    m2:空白中的mass
                    in1:样本中的intensity
                    in2:空白中的intensity
        :param ppm: abs((m1 - m2) * 1000000.0 / m1) < ppm，则认为mass相同，这个ppm需要可以设置，条件1
        :param percentage: 0 < abs((in1 - in2)  * 100.0 / in1) < percentage%，则认为intensity相近，这个percentage也需要可以设置，条件2
        :return: 处理后的数据(格式：list二维数组)
        """
        header = ["Mass", "Intensity"]
        m1 = self.sampleData["Mass"].values            # 样本中的mass，类型为numpy中的ndarray
        in1 = self.sampleData["Intensity"].values     # 样本中的intensity
        m2 = self.blankData["Mass"].values             # 空白中的mass
        in2 = self.blankData["Intensity"].values      # 空白中的intensity
        reslut = np.hstack([m1.reshape(-1, 1), in1.reshape(-1, 1)])  # 两个一维数组拼接为二维数组
        if ConstValues.PsIsDebug:
            print(type(reslut))
            print(reslut[:6, :])

        # 核心处理逻辑
        deleteList = []  # 记录需要删除的索引
        # 要求m1和m2为升序
        i = 0
        j = 0
        while i < m2.size:
            breakFlag = False
            j = 0
            while j < m1.size:
                if abs((m1[j] - m2[i]) * 1000000.0 / m1[j]) < self.deleteBlankPPM:
                    if abs((in1[j] - in2[i]) * 100.0 / in1[j]) * 100 < self.deleteBlankPercentage:
                        deleteList.append(j)
                        breakFlag = True
                elif breakFlag or m1[j] > m2[i]:
                    break
                j += 1
            i += 1

        # # 不要求要求m1和m2为有序
        # for i in range(m2.size):
        #     for j in range(m1.size):
        #         if abs((m1[j] - m2[i]) * 1000000.0 / m1[j]) < ppm:
        #             if abs((in1[j] - in2[i]) * 100.0 / in1[j]) * 100 < percentage:
        #                 deleteList.append(j)

        reslut = np.delete(reslut, deleteList, axis=0)  # 删除索引在deleteList中的向量
        reslut = reslut.tolist()
        reslut.insert(0, header)

        if ConstValues.PsIsDebug:
            print(len(deleteList))
            print(len(reslut))
            print(type(reslut))
            print(reslut[:6])

        # 数据写入excel文件中
        self.WriteDataToExcel(reslut, "./intermediateFiles/_1_deleteBlank/DeleteBlank.xlsx")

        deleteBlankIsFinished = True  # 该过程已经完成

        return reslut, deleteBlankIsFinished

    # 负责将数据写入xlsx文件
    def WriteDataToExcel(self, data, filename):
        """
        :param data: 每一行是一组数据，第一行是表头
        :return:
        """
        # 新建excel表
        workbook = xlsxwriter.Workbook(filename)
        # 创建sheet，默认名称sheet1
        worksheet = workbook.add_worksheet()
        # 数据写入excel
        for i in range(len(data)):
            worksheet.write_row("A{}".format(i + 1), data[i])
        # 将excel文件保存关闭，如果没有这一行运行代码会报错
        workbook.close()

