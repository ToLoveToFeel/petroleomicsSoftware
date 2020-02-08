# coding=utf-8
# 此文件负责定义：扣空白
import numpy as np
import pandas as pd
from ConstValues import ConstValues


class ClassDeleteBlank():
    def __init__(self, samplePath, blankPath):
        """
        :param samplePath: 样本文件路径
        :param blankPath: 空白文件路径
        """
        self.reslut = None  # 最终处理后得到的数据
        self.sampleData = pd.read_excel(io=samplePath, header=ConstValues.PsHeaderLine)
        self.sampleData.columns = ["Mass", "Intensity"]  # 强制改变列名，方便后面使用
        self.blankData = pd.read_excel(io=blankPath, header=ConstValues.PsHeaderLine)
        self.blankData.columns = ["Mass", "Intensity"]  # 强制改变列名，方便后面使用

    # 删除Intensity小于dintensity的行
    def DeleteSmallIntensity(self, intensity):
        # 只保留大于intensity的行
        self.sampleData = self.sampleData[self.sampleData.Intensity > intensity]
        self.blankData = self.blankData[self.blankData.Intensity > intensity]
        if ConstValues.PsIsDebug == True:
            print(self.sampleData.shape[0])  # 180-onescan-external.xlsx处理后：5888
            print(self.blankData.shape[0])  # blank-3.xlsx处理后：3778

    # 删去样本和空白中相同的mass且intensity相近的mass，必须调过DeleteSmallIntensity函数调用此函数才有意义
    def DeleteSimilarToBlank(self, ppm, percentage):
        """
                    m1:样本中的mass
                    m2:空白中的mass
                    in1:样本中的intensity
                    in2:空白中的intensity
        :param ppm: abs((m1 - m2) * 1000000.0 / m1) < ppm，则认为mass相同，这个ppm需要可以设置，条件1
        :param percentage: 0 < abs((in1 - in2)  * 100.0 / in1) < percentage%，则认为intensity相近，这个percentage也需要可以设置，条件2
        :return: 处理后的数据(格式：numpy二维数组)
        """
        m1 = self.sampleData["Mass"].values            # 样本中的mass，类型为numpy中的ndarray
        in1 = self.sampleData["Intensity"].values     # 样本中的intensity
        m2 = self.blankData["Mass"].values             # 空白中的mass
        in2 = self.blankData["Intensity"].values      # 空白中的intensity
        self.reslut = np.hstack([m1.reshape(-1, 1), in1.reshape(-1, 1)])  # 两个一维数组拼接为二维数组
        if ConstValues.PsIsDebug == True:
            print(type(self.reslut))
            print(self.reslut[:6, :])

        # 核心处理逻辑
        deleteList = []  # 记录需要删除的索引
        breakFlag = False
        # 要求m1和m2为升序
        i = 0
        j = 0
        while i < m2.size:
            breakFlag = False
            j = 0
            while j < m1.size:
                if abs((m1[j] - m2[i]) * 1000000.0 / m1[j]) < ppm:
                    if abs((in1[j] - in2[i]) * 100.0 / in1[j]) * 100 < percentage:
                        deleteList.append(j)
                        breakFlag = True
                elif breakFlag == True or m1[j] > m2[i]:
                    break
                j += 1
            i += 1

        # # 不要求要求m1和m2为有序
        # for i in range(m2.size):
        #     for j in range(m1.size):
        #         if abs((m1[j] - m2[i]) * 1000000.0 / m1[j]) < ppm:
        #             if abs((in1[j] - in2[i]) * 100.0 / in1[j]) * 100 < percentage:
        #                 deleteList.append(j)

        self.reslut = np.delete(self.reslut, deleteList, axis=0)  # 删除索引在deleteList中的向量

        if ConstValues.PsIsDebug == True:
            print(len(deleteList))
            print(self.reslut.shape)
            print(self.reslut[:6, :])

        # # 将self.reslut写入excel文件，需要头文件openpyxl
        # writer = pd.ExcelWriter("afterDeleteBlank.xlsx")
        # data = pd.DataFrame(self.reslut)
        # data.columns = ["Mass", "Intensity"]
        # data.to_excel(writer)
        # writer.save()
        # writer.close()

        # # 将self.reslut写入txt文件
        # np.savetxt("afterDeleteBlank.txt", self.reslut, fmt='%.6f')

        deleteBlankIsFinished = True  # 该过程已经完成

        return self.reslut, deleteBlankIsFinished



