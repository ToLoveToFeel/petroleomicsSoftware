# coding=utf-8
# 此文件负责定义：去假阳性
import os
import matplotlib.pyplot as plt
from Utils import *
from ConstValues import ConstValues
import numpy as np


class ClassRemoveFalsePositive:
    def __init__(self, parameterList, outputFilesPath):
        assert len(parameterList) == 7, "ClassRemoveFalsePositive参数个数不对!"
        self.DelIsoResult = parameterList[0]  # 扣同位素后生成的文件，两项记录之间通过空列表分割（格式：list二维数组，有表头）

        peakDisResult = parameterList[1]
        # 结果是一个列表，有三个元素，
        # 第一个是峰识别的结果（格式：list二维数组，有表头）
        # 第二个是需要需要峰检测（第二部分）的详细数据，二维列表，无表头
        # 第三个是txt文件中RT值(从小到大排序)
        self.PeakDisResult = peakDisResult[0]  # 峰识别第一阶段后生成的文件，两项记录之间通过空列表分割（格式：list二维数组，有表头）
        self.PeakDisResultDetail = peakDisResult[1]

        self.RemoveFPId = parameterList[2]  # 1：去同位素之后的内容self.DelIsoResult 2：峰识别之后的内容self.DelIsoResult
        self.RemoveFPContinue_CNum = parameterList[3]
        self.RemoveFPContinue_DBENum = parameterList[4]
        self.RemoveFPFromPlot6Need = parameterList[5]  # 是否需要根据Retention time vs carbon number去假阳性
        self.RemoveFPFromPlotMoveDistance = parameterList[6]  # 直线的截距
        # 用户选择的文件的生成位置
        self.outputFilesPath = outputFilesPath

        if ConstValues.PsIsSingleRun:
            filePath = "./intermediateFiles/_4_peakDistinguish/" + ConstValues.PsNamePeakDistinguish
            self.PeakDisResult = ReadExcelToList(filepath=filePath, hasNan=True)
            filePath = "./intermediateFiles/_4_peakDistinguish/PeakDisPart1DetailPlot.xlsx"
            self.PeakDisResultDetail = ReadExcelToList(filepath=filePath, hasNan=False)

    def RemoveFalsePositive(self):
        result = []
        # 创建文件夹
        newDirectory = CreateDirectory(self.outputFilesPath, "./intermediateFiles", "/_5_removeFalsePositive")
        # 运行主逻辑
        if self.RemoveFPId == 1:
            result = self.RemoveFPFromDelIso()
            WriteDataToExcel(result, newDirectory + "/" + ConstValues.PsNameRemoveFPFrom_DelIsoResult)
        elif self.RemoveFPId == 2:
            result = self.RemoveFPFromPeakDis()
            if self.RemoveFPFromPlot6Need:
                result = self.RemoveFPFromPlot(result)
            WriteDataToExcel(result, newDirectory + "/" + ConstValues.PsNameRemoveFPFrom_PeakDisResult)

        # 去假阳性后峰识别的峰
        newData = []
        if self.RemoveFPId == 2:
            newData = self.RemoveFPFromPeakDisPlot(result)  # 从读取PeakDisPart1DetailPlot.xlsx去假阳性后生成newData
            WriteDataToExcel(newData, newDirectory + "/PeakDisPart1DetailPlotAfterRFP.xlsx")
            # self.PlotAfterRemoveFP(newData)

        return [result, newData], True

    # 从去同位素后的文件里去假阳性
    def RemoveFPFromDelIso(self):
        # self.DelIsoResult种每个元素均为列表，有多种类型：
        # 类型一：["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
        # 类型二：["SampleMass", "SampleIntensity"]
        # 类型三：[DBItem_13C1, DBItem_13C1Intensity, "iostope"] 或者 [DBItem_13C2, DBItem_13C2Intensity, "iostope"]
        # 类型四：[]

        # {key:[ [[...], ..., [...]] , ..., [...]], ..., key:[...]}，[[...], ..., [...]]对应某个分子式，长度为1,2或3
        dataDirectory = {}  # 记录所有符合要求的数据
        # {key:[ [...] , ..., [...] ], ..., key:[ [...] , ..., [...] ]}，[...]对应某个分子式，长度为8
        dataOneDirectory = {}  # 某个分子式对应多条记录，只记录第一条，长度为3，最后一个数据记录其位置

        # 以类别为键，将数据整理为字典
        i = 1  # 跳过表头
        length = len(self.DelIsoResult)
        while i < length:
            firstItem = self.DelIsoResult[i]
            if len(firstItem) != 8:
                i += 1
                continue
            # 此时找到第一个符合条件的记录，查找其紧随的下面是否有 类型三
            item = [firstItem]  # 是一个二维列表，对应一种物质
            i += 1
            if i < length:
                nextItem = self.DelIsoResult[i]
                while len(nextItem) != 0:
                    item.append(nextItem)
                    i += 1
                    if i >= length:
                        break
                    nextItem = self.DelIsoResult[i]

            key = firstItem[2]  # "Class"作为键
            if key in dataDirectory.keys():
                dataDirectory[key].append(item)
                dataOneDirectory[key].append([firstItem[3]] + [firstItem[6]] + [len(dataOneDirectory[key])])
            else:
                dataDirectory[key] = [item]
                dataOneDirectory[key] = [[firstItem[3]] + [firstItem[6]] + [0]]
            # 查看下一条数据
            i += 1

        # # 对dataOneDirectory中的各项进行排序，因为修改去同位素的生成文件的顺序，所以这里不需要再次排序
        # for key in dataOneDirectory.keys():
        #     dataOneDirectory[key] = sorted(dataOneDirectory[key], key=(lambda x: [x[0], x[1]]), reverse=False)

        # 删除不符合的数据
        afterDel_DBEDirectory = self.RemoveFPHandleContinue(dataOneDirectory)

        # 重新整理结果
        ret = [["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]]
        for key in afterDel_DBEDirectory.keys():
            data = afterDel_DBEDirectory[key]
            for item1 in data:
                for item2 in dataDirectory[key][item1[2]]:
                    ret.append(item2)
                ret.append([])

        return ret

    # 从峰识别第一阶段后的文件里去假阳性
    def RemoveFPFromPeakDis(self):
        # self.PeakDisResult
        # ["SampleMass", "Area", "startRT", "startRTValue", "endRT", "endRTValue", "TICMassMedian", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
        # {key:[ [...], ..., [...]] , ..., [[...], ..., [...]]], ..., key:[...]}，[[...], ..., [...]]对应某个分子式，[...]长度为13
        dataDirectory = {}  # 记录所有符合要求的数据
        # {key:[ [...] , ..., [...] ], ..., key:[ [...] , ..., [...] ]}，[...]对应某个分子式，长度为8
        dataOneDirectory = {}  # 某个分子式对应多条记录，只记录第一条，长度为3，最后一个数据记录其位置

        # 以类别为键，将数据整理为字典
        i = 1  # 跳过表头
        length = len(self.PeakDisResult)
        while i < length:
            firstItem = self.PeakDisResult[i]
            item = [firstItem]  # 是一个二维列表，对应一种物质
            i += 1
            if i < length:
                nextItem = self.PeakDisResult[i]
                while len(nextItem) != 0:
                    item.append(nextItem)
                    i += 1
                    if i >= length:
                        break
                    nextItem = self.PeakDisResult[i]

            key = firstItem[7]  # "Class"作为键
            if key in dataDirectory.keys():
                dataDirectory[key].append(item)
                dataOneDirectory[key].append([firstItem[8]] + [firstItem[11]] + [len(dataOneDirectory[key])])
            else:
                dataDirectory[key] = [item]
                dataOneDirectory[key] = [[firstItem[8]] + [firstItem[11]] + [0]]
            # 查看下一条数据
            i += 1

        # 对dataOneDirectory中的各项进行排序
        for key in dataOneDirectory.keys():
            dataOneDirectory[key] = sorted(dataOneDirectory[key], key=(lambda x: [x[0], x[1]]), reverse=False)

        # 删除不符合的数据
        afterDel_DBEDirectory = self.RemoveFPHandleContinue(dataOneDirectory)

        # 重新整理结果
        ret = [["SampleMass", "Area", "startRT", "startRTValue", "endRT", "endRTValue", "TICMassMedian", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]]
        for key in afterDel_DBEDirectory.keys():
            data = afterDel_DBEDirectory[key]
            for item1 in data:
                for item2 in dataDirectory[key][item1[2]]:
                    ret.append(item2)
                ret.append([])

        return ret

    # 过滤不符合条件的条目的主逻辑
    def RemoveFPHandleContinue(self, dataOneDirectory):
        """
        :param dataOneDirectory: 是一个字典，类型是键，值是二维列表[[...], ... , [...]]，[...]只有三个数据：DBE,C,在dataDirectory中的index
        :return: 过滤掉不符合条件后的dataOneDirectory，格式一样
        """
        # 记录需要删除的数据，首先删除C数不符合要求的
        afterDel_CDirectory = {}  # 记录C数目>=self.RemoveFPContinue_CNum的数据
        for key in dataOneDirectory.keys():  # 针对每一个类别进行下面的过程
            data = dataOneDirectory[key]  # 获取二维有序列表,data[0]是Neutral DBE，data[1]是C数
            i = 0
            dataLength = len(data)
            while i < dataLength - 1:
                firstDBE = data[i]
                everyDBEList = [firstDBE]  # 每个类别有多个不同的DBE，记录某一个DBE所对应的记录
                i += 1
                while data[i][0] == firstDBE[0]:  # Neutral DBE相同
                    everyDBEList.append(data[i])
                    i += 1
                    if i >= dataLength:
                        break
                # 获取到某一个DBE所对应的记录
                everyDBEListLength = len(everyDBEList)
                if everyDBEListLength < self.RemoveFPContinue_CNum:  # 长度不足，直接舍去
                    continue
                # 此时长度符合要求，考察是否连续
                j = 0
                while j < everyDBEListLength - 1:  # 考虑一个DBE
                    nowDBE = everyDBEList[j]
                    continueDBEList = [nowDBE]  # 二维列表
                    nextDBE = everyDBEList[j + 1]
                    j += 1
                    while nowDBE[1] + 1 == nextDBE[1]:  # 考虑连续的DBE，一个DBE可能有多个连续的
                        continueDBEList.append(nextDBE)
                        nowDBE = nextDBE  # 更新当前DBE
                        j += 1
                        if j >= len(everyDBEList):
                            break
                        nextDBE = everyDBEList[j]  # 获取下一个DBE
                    if len(continueDBEList) >= self.RemoveFPContinue_CNum:  # 找到符合要求的数据
                        if key in afterDel_CDirectory.keys():
                            for k in range(len(continueDBEList)):
                                afterDel_CDirectory[key].append(continueDBEList[k])
                        else:
                            afterDel_CDirectory[key] = continueDBEList

        # 记录需要删除的数据，之后删除DBE数不符合要求的
        afterDel_DBEDirectory = {}  # 记录DBE数目>=self.RemoveFPContinue_DBENum的数据
        for key in afterDel_CDirectory.keys():  # 针对每一个类别进行下面的过程
            data = afterDel_CDirectory[key]  # 获取二维有序列表,data[0]是Neutral DBE，data[1]是C数
            i = 0
            dataLength = len(data)
            while i < dataLength - 1:
                first = data[i]
                continueList = [first]
                continueNum = 1
                next = data[i + 1]
                i += 1
                # 寻找相等的条目
                while first[0] == next[0]:
                    continueList.append(next)
                    i += 1
                    if i >= dataLength:
                        break
                    first = next
                    next = data[i]
                # 寻找连续的条目
                if i < dataLength:
                    while (first[0] + 1 == next[0]) or (first[0] == next[0]):
                        continueList.append(next)
                        i += 1
                        if i >= dataLength:
                            break
                        if first[0] + 1 == next[0]:
                            continueNum += 1
                        first = next
                        next = data[i]
                if continueNum >= self.RemoveFPContinue_DBENum:
                    if key in afterDel_DBEDirectory.keys():
                        for k in range(len(continueList)):
                            afterDel_DBEDirectory[key].append(continueList[k])
                    else:
                        afterDel_DBEDirectory[key] = continueList

        return afterDel_DBEDirectory

    # 读取PeakDisPart1DetailPlot.xlsx文件的内容，并进行去假阳性
    def RemoveFPFromPeakDisPlot(self, result):
        # ["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
        if ConstValues.PsIsSingleRun:
            self.PeakDisResultDetail = ReadExcelToList(filepath="./intermediateFiles/_4_peakDistinguish/PeakDisPart1DetailPlot.xlsx", hasNan=False)
        massSet = set()
        newData = []  # 存储需要画出图形的经过去假阳性后的数据
        for item in result:
            if len(item) != 0:
                massSet.add(item[0])
        for item in self.PeakDisResultDetail:
            if item[0] in massSet:
                newData.append(item)
        return newData

    # 过滤峰识别第一阶段生成的PeakDistinguishPart1Detail.xlsx文件，并绘制图形
    def PlotAfterRemoveFP(self, data):
        lengthList = [i for i in range(len(data[0][9:]))]
        # 创建对应的文件夹
        CreateDirectory(self.outputFilesPath, "./intermediateFiles", "/_5_removeFalsePositive/peakImagesAfterRemoveFP")
        for i in range(len(data)):
            item = data[i]
            Class = item[2]  # 化合物类型
            DBE = item[3]  # 不饱和度数目
            plt.xlabel('RT', fontproperties='SimHei', fontsize=15, color='blue')
            plt.ylabel('Intensity', fontproperties='SimHei', fontsize=15, color='blue')
            plt.title("Mass:" + str(item[0]) + "  DBE:" + str(DBE) + "  formula:" + item[4], fontproperties='SimHei', fontsize=12, color='red')
            plt.vlines(x=lengthList, ymin=0, ymax=item[9:])
            newDirectory = CreateDirectory(self.outputFilesPath,
                                           "./intermediateFiles",
                                           "/_5_removeFalsePositive/peakImagesAfterRemoveFP/"+Class+"_DBE"+str(DBE)
                                           )
            plt.savefig(fname=newDirectory+"/"+Class+"_DBE"+str(DBE)+"_C"+str(item[6]), dpi=300)
            plt.close()

    # 根据绘图中的 Retention time vs carbon number 去除假阳性
    def RemoveFPFromPlot(self, data):
        # {(Class, Neutral DBE):[[...], [...]], ...}    二维列表存储的分别是C和startRTValue
        dictionary = {}
        # "SampleMass", "Area", "startRT", "startRTValue", "endRT", "endRTValue", "TICMassMedian", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"
        newData = [data[0]]  # 存储表头
        i = 1  # 从1开始跳过表头
        while i < len(data):
            firstItem = data[i]
            if len(firstItem) == 0:
                i += 1
                continue
            firstClass = firstItem[7]
            firstDBE = firstItem[8]
            firstCNum = firstItem[11]
            firstStartRTValue = firstItem[3]
            dictionary[(firstClass, firstDBE)] = [[firstCNum], [firstStartRTValue]]  # 此时字典中一定不存在这个
            j = i + 1
            while j < len(data):
                item = data[j]
                if len(item) == 0:
                    j += 1
                    continue
                Class = item[7]
                DBE = item[8]
                if not (Class == firstClass and DBE == firstDBE):
                    break
                CNum = item[11]
                startRTValue = item[3]
                dictionary[(Class, DBE)][0].append(CNum)  # 此时字典中一定存在这个
                dictionary[(Class, DBE)][1].append(startRTValue)
                j += 1
            i = j
        # 去除假阳性
        for key in dictionary.keys():
            newXList, newYList = self.RemoveFPFromOnePlot(dictionary[key][0], dictionary[key][1])
            dictionary[key][0] = newXList
            dictionary[key][1] = newYList
        # 生成去假阳性后的数据
        flag = False  # 判断何时加上空行
        for item in data[1:]:
            if len(item) == 0:
                if flag:
                    newData.append([])
                    flag = False
                continue
            Class = item[7]
            DBE = item[8]
            CNum = item[11]
            startRTValue = item[3]
            if (CNum in dictionary[(Class, DBE)][0]) and (startRTValue in dictionary[(Class, DBE)][1]):
                flag = True
                newData.append(item)
        return newData

    # 根据绘图中的一幅 Retention time vs carbon number图 去除假阳性
    def RemoveFPFromOnePlot(self, xList, yList):
        if len(xList) <= 15:  # 长度过短，直接返回
            return xList, yList

        splitXList = []  # 二维数组，[[x, ...], [...]]，分开是因为可能不连续
        splitYList = []
        coordinateList = []  # 二维数组，[[x1, x2], [y1, y2], ...]

        # 不连续的数据分割
        j = 0
        notContinueNum = 5
        while j < len(xList) - 1:
            if not (xList[j] == xList[j + 1] or
                    (xList[j + 1] <= xList[j] + notContinueNum)):
                break
            j += 1
        if j == len(xList) - 1:  # 说明全部连续
            splitXList.append(xList)
            splitYList.append(yList)
            # 求坐标
            xMin = np.min(xList)
            xMax = np.max(xList)
            yMin = np.min(yList)
            yMax = np.max(yList)
            coordinateList.append([xMin, xMax])
            coordinateList.append([yMin, yMax])
        else:  # 说明不是全部连续，需要分为两部分处理：[0...j]  [j+1...end]
            # 第一段
            splitXList.append(xList[:j + 1])
            splitYList.append(yList[:j + 1])
            xMin = np.min(xList[:j + 1])  # 求坐标
            xMax = np.max(xList[:j + 1])
            yMin = np.min(yList[:j + 1])
            yMax = np.max(yList[:j + 1])
            coordinateList.append([xMin, xMax])
            coordinateList.append([yMin, yMax])
            # 第二段
            splitXList.append(xList[j + 1:])
            splitYList.append(yList[j + 1:])
            xMin = np.min(xList[j + 1:])  # 求坐标
            xMax = np.max(xList[j + 1:])
            yMin = np.min(yList[j + 1:])
            yMax = np.max(yList[j + 1:])
            coordinateList.append([xMin, xMax])
            coordinateList.append([yMin, yMax])

        # 假阳性去除
        oneXList = []
        oneYList = []
        for j in range(len(splitXList)):  # 一幅图可能分为多个部分
            deltaX = coordinateList[j * 2][1] - coordinateList[j * 2][0]
            deltaY = coordinateList[j * 2 + 1][1] - coordinateList[j * 2 + 1][0]
            if (deltaX == 0) or (deltaY == 0):  # 说明分割线水平或者垂直，直接保留全部数据
                oneXList += splitXList[j]
                oneYList += splitYList[j]
                continue
            xMin = coordinateList[j * 2][0]
            yMin = coordinateList[j * 2 + 1][0]
            for k in range(len(splitXList[j])):  # 依次考察各个点
                x = splitXList[j][k]
                y = splitYList[j][k]
                # x * (yMax - yMin) - (y - moveDistance) * (xMax - xMin) - xMin * (yMax - yMin) + yMin * (xMax - xMin) > 0
                if (x * deltaY - (y - self.RemoveFPFromPlotMoveDistance) * deltaX - xMin * deltaY + yMin * deltaX) >= 0:
                    oneXList.append(x)
                    oneYList.append(y)
        return oneXList, oneYList
