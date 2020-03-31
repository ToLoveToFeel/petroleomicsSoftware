# coding=utf-8
# 此文件负责定义：扣空白
import sys
import numpy as np
from Utils import *
from ConstValues import ConstValues


class ClassDeleteBlank:
    def __init__(self, parameterList, outputFilesPath):
        """
        :param parameterList: 程序运行所需要的参数列表
        """
        assert len(parameterList) == 5, "ClassDeleteBlank参数不对"
        # 样本文件路径
        self.samplePath = parameterList[0]
        # 空白文件路径
        self.blankPath = parameterList[1]
        # 1~9999（整数）
        self.deleteBlankIntensity = parameterList[2]
        # 0.01~99.99（浮点数）
        self.deleteBlankPPM = parameterList[3]
        # 1~100（整数）
        self.deleteBlankPercentage = parameterList[4]
        # 数据预处理
        self.sampleData = pd.read_excel(io=self.samplePath, header=ConstValues.PsHeaderLine)
        self.sampleData.columns = ["Mass", "Intensity"]  # 强制改变列名，方便后面使用
        self.blankData = pd.read_excel(io=self.blankPath, header=ConstValues.PsHeaderLine)
        self.blankData.columns = ["Mass", "Intensity"]  # 强制改变列名，方便后面使用
        # 用户选择的文件的生成位置
        self.outputFilesPath = outputFilesPath

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
            # 180-onescan-external.xlsx处理后：5888
            # blank-3.xlsx处理后：3778
            print(
                "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                sys._getframe().f_code.co_name, "\" method***：",
                "self.sampleData.shape[0]:", self.sampleData.shape[0], "self.blankData.shape[0]:", self.blankData.shape[0]
            )

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
        header = [["Mass", "Intensity"]]
        m1 = self.sampleData["Mass"].values            # 样本中的mass，类型为numpy中的ndarray
        in1 = self.sampleData["Intensity"].values     # 样本中的intensity
        m2 = self.blankData["Mass"].values             # 空白中的mass
        in2 = self.blankData["Intensity"].values      # 空白中的intensity
        result = np.hstack([m1.reshape(-1, 1), in1.reshape(-1, 1)])  # 两个一维数组拼接为二维数组
        if ConstValues.PsIsDebug:
            print(
                "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                sys._getframe().f_code.co_name, "\" method***：",
                "type(result):", type(result), "result[:6, :]:", result[:6, :]
            )

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
                    if abs((in1[j] - in2[i]) * 100.0 / in1[j]) < self.deleteBlankPercentage:
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

        result = np.delete(result, deleteList, axis=0)  # 删除索引在deleteList中的向量
        result = result.tolist()
        result = header + result

        if ConstValues.PsIsDebug:
            print(
                "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                sys._getframe().f_code.co_name, "\" method***：",
                "len(deleteList):", len(deleteList), "len(result):", len(result), "result[:6]:", result[:6]
            )

        # 数据写入excel文件中
        newDirectory = CreateDirectory(self.outputFilesPath, "./intermediateFiles", "/_1_deleteBlank")
        WriteDataToExcel(result, newDirectory + "/" + ConstValues.PsNameDeleteBlank)

        return result, True

