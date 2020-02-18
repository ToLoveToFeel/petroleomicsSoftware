# coding=utf-8
# 此文件负责定义：扣同位素
import xlsxwriter
import time
import numpy as np
from Utils import *
from ConstValues import ConstValues
from PromptBox import PromptBox


class ClassPeakDistinguish:
    def __init__(self, parameterList):
        assert len(parameterList) == 7, "ClassPeakDistinguish参数个数不对!"
        self.TICFilePath = parameterList[0]  # 总离子流图路径，第一部分
        self.DelIsoResult = parameterList[1]  # 扣同位素后生成的文件，两项记录之间通过空列表分割（格式：list二维数组，有表头）
        self.PeakDisContinuityNum = parameterList[2]  # 连续出现的扫描点个数，格式：整数
        self.PeakDisMassDeviation = parameterList[3]  # 质量偏差，格式：浮点数
        self.PeakDisClassIsNeed = parameterList[4]
        self.PeakDisClass = parameterList[5]  # 第二部分，峰检测
        self.PeakDisScanPoints = parameterList[6]  # 判断峰值的扫描点个数
        # 读取总离子流图
        self.TICData = self.ReadTIC()
        # 去掉表头
        self.DelIsoResult = self.DelIsoResult[1:]

    # 负责峰识别
    def PeakDistinguish(self):
        # 说明读取的文件存在问题
        if self.TICData is None:
            return [], False
        resultPart1 = []  # 第一部分，识别连续的扫描点
        headerPart1 = ["SampleMass", "Area", "startRT", "startRTValue", "endRT", "endRTValue", "TICMassMedian", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
        resultPart1.append(headerPart1)

        resultPart2 = []  # 第二部分，峰检测与分割，即将多个峰分开输出
        headerPart2 = ["SampleMass", "Area", "startRT", "startRTValue", "endRT", "endRTValue", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
        resultPart2.append(headerPart2)

        try:
            for sampleItem in self.DelIsoResult:
                # sampleItem均为列表，有多重类型：
                # 类型一：["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
                # 类型二：["SampleMass", "SampleIntensity"]
                # 类型三：[DBItem_13C1, DBItem_13C1Intensity, "iostope"]或者[DBItem_13C2, DBItem_13C2Intensity, "iostope"]
                # 类型四：[]
                if len(sampleItem) == 8:
                    ret = self.PeakDisHandleItem(sampleItem)
                    for item in ret:
                        resultPart1.append(item)
        except Exception as e:
            print("Error : ", e)

        # 将结果写入excel文件
        WriteDataToExcel(resultPart1, "./intermediateFiles/_4_peakDistinguish/PeakDistinguishPart1.xlsx")

        PeakDisIsFinished = True

        return resultPart1, PeakDisIsFinished

    # 负责判断某个扣同位素后的样本是否能成功在总离子流图文件(txt)查到符合条件的记录集合
    def PeakDisHandleItem(self, sampleItem):
        # 获取样本中的Mass（Mass0）
        sampleMass = sampleItem[0]
        # # 获取样本的类型，判断是否需要进行第二部分
        # needDetectPeak = False
        # if (sampleItem[2] in self.PeakDisClass) and self.PeakDisClassIsNeed:
        #     needDetectPeak = True
        # 获取字典的长度
        scanNum = len(self.TICData)
        # 将字典的键转化为列表
        keysList = list(self.TICData)
        ret = []

        k = 0
        while k < scanNum:
            firstRT = None
            continuityItems = []  # 存储连续的符合要求的记录，为二维列表[[Mass, Intensity],...,[Mass, Intensity]]
            while k < scanNum and firstRT is None:
                firstRT = self.PeakDisHasCorrespondInTIC(keysList, sampleMass, k)
                k += 1
            if k >= scanNum:
                break
            # 此时保证在self.TICData找到第一个符合要求的记录
            startRT = k - 1
            continuityItems.append(firstRT)
            # 寻找连续的符合要求的记录
            nextRT = self.PeakDisHasCorrespondInTIC(keysList, sampleMass, k)
            while k <scanNum and nextRT is not None:
                continuityItems.append(nextRT)
                k += 1
                if k >= scanNum:
                    break
                nextRT = self.PeakDisHasCorrespondInTIC(keysList, sampleMass, k)
            # 到这里连续的记录已经结束
            if len(continuityItems) >= self.PeakDisContinuityNum:  # 说明连续的扫描点数目符合要求
                continuityItems = np.array(continuityItems)
                continuityMasses = continuityItems[:, 0]
                continuityIntensities = continuityItems[:, 1]

                Area = np.sum(continuityIntensities)  # 求面积
                startRTValue = keysList[startRT]  # 开始的扫描点的值
                endRT = startRT + len(continuityItems) - 1  # 结束的扫描点在TIC中属于第几个扫描点
                endRTValue = keysList[endRT]  # 结束的扫描点的值
                MassMedian = np.median(continuityMasses)  # TIC中所有符合条件的连续的记录的

                ret.append([sampleMass, Area, startRT, startRTValue, endRT, endRTValue, MassMedian] + sampleItem[2:])
            # 本次连续的考察完毕，进行之后没有考虑的扫描点考察
            k += 1
        if len(ret) != 0:
            ret.append([])
        return ret

    # 搜索RTk中是否存在和sampleMass相近的记录
    def PeakDisHasCorrespondInTIC(self, keysList, sampleMass, k):
        value = self.TICData[keysList[k]]  # value为二维列表[[Mass, Intensity],...,[Mass, Intensity]]
        for item in value:
            TICMass = item[0]
            # TICIntensity = item[1]
            if abs((TICMass - sampleMass) * 1000000.0 / sampleMass) < self.PeakDisMassDeviation:
                return item
        return None

    # 负责读取总离子流图文件(txt)
    def ReadTIC(self):
        """
        文件格式必须为：每行三个数据，一个表头，数据之间用制表符(\t)分割，无其他无关字符
        :return:返回结果为字典：{key:value,...,key:value}，value为二维列表[[Mass, Intensity],...,[Mass, Intensity]]
        """
        startTime = time.time()
        # 读取数据，数据分割
        f = open(self.TICFilePath, "r")
        content = f.read().strip().replace("\n", "\t").replace(" ", "").split("\t")
        # 去除表头
        content = content[3:]
        if len(content) / 3 != int(len(content) / 3):
            # raise Exception("Error in ClassPeakDistinguish ReadTIC.")
            PromptBox().warningMessage("总离子流图文件(txt)存在问题，请重新选择！")
            return None
        # str全部转为float
        content = [float(item) for item in content]
        # 返回结果为字典：{key:value}，value为二维列表[[Mass, Intensity],...,[Mass, Intensity]]
        res = {}

        key = content[0]
        value = []
        for i in range(int(len(content) / 3)):
            if content[i * 3] != key:
                res[key] = value  # 字典中添加元素（二维列表）
                key = content[i * 3]
                value = []
            value.append([content[i * 3 + 1], content[i * 3 + 2]])

        if ConstValues.PsIsDebug:
            print("扫描点的个数： ", len(res))
        endTime = time.time()
        if ConstValues.PsIsDebug:
            print("读入和处理文件费时： ",endTime - startTime, " s")
        return res

