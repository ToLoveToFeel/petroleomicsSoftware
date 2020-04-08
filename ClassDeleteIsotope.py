# coding=utf-8
# 此文件负责定义：去同位素
from Utils import *
from ConstValues import ConstValues
import sys


class ClassDeleteIsotope:
    def __init__(self, parameterList, outputFilesPath):
        assert len(parameterList) == 8, "ClassDeleteIsotope参数个数不对"
        self.deleteBlankResult = parameterList[0]  # 删空白的结果（格式：list二维数组，有表头）
        self.GDBResult = parameterList[1]  # 数据库生成的结果（格式：list二维数组，有表头）
        self.deleteBlankIntensity = parameterList[2]  # 格式：整数
        self.DelIsoIntensityX = parameterList[3]  # 格式：整数
        self.DelIso_13C2RelativeIntensity = parameterList[4]  # 格式：整数
        self.DelIsoMassDeviation = parameterList[5]  # 格式：浮点数
        self.DelIsoIsotopeMassDeviation = parameterList[6]  # 格式：浮点数
        self.DelIsoIsotopeIntensityDeviation = parameterList[7]  # 格式：整数
        # 去掉表头
        self.deleteBlankResult = self.deleteBlankResult[1:]
        self.GDBResult = self.GDBResult[1:]
        # 用户选择的文件的生成位置
        self.outputFilesPath = outputFilesPath

    # 负责去同位素
    def DeleteIsotope(self):
        result = []
        header = ["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
        result.append(header)

        for sampleItem in self.deleteBlankResult:
            # sampleItem均为列表，列表：[Mass, Intensity]，都是浮点数
            ret = self.DelIsoHandleItem(sampleItem)
            for item in ret:
                result.append(item)

        # 去同位素按照Formula（主键），C（次主键）从小到大顺序排序
        result = self.DelIsoSort(result)

        # 数据写入excel文件中
        newDirectory = CreateDirectory(self.outputFilesPath, "./intermediateFiles", "/_3_deleteIsotope")
        WriteDataToExcel(result, newDirectory + "/" + ConstValues.PsNameDeleteIsotope)

        return result, True

    # 负责判断某个删空白样本是否能匹配成功 数据库
    def DelIsoHandleItem(self, sampleItem):
        """
        :param sampleItem: 样本(self.deleteBlankResult)中某个样本，是列表：[Mass, Intensity]，都是浮点数
        :return: list二维列表，长度可能为2或3或4，最后一个元素均为[]，目的显示写入文件后容易区分
        """
        sampleItemMass = sampleItem[0]
        sampleItemIntensity = sampleItem[1]
        # 返回结果：list二维数组，数组的长度可能为1或2或3
        ret = []
        for DBItem in self.GDBResult:
            # DatabaseItem均为列表，列表：["Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
            # [str, int, str, float, int, str]
            # DBItemClass = DBItem[0]  # 类型
            # DBItemNDBE = DBItem[1]  # 不饱和度
            # DBItemFormula = DBItem[2]  # 分子式
            DBItemM_Z = DBItem[3]  # 质荷比
            DBItemCNumber = DBItem[4]  # 碳数目

            # 1.sampleItem中Mass与database一个class中的cal m/z是否相同
            if abs((sampleItemMass - DBItemM_Z) * 1000000.0 / DBItemM_Z) > self.DelIsoMassDeviation:
                continue

            # 2.根据cal m/z 对应的碳数，计算“13C1”及其intensity1，计算“13C2”及其intensity2
            DBItem_13C1 = DBItemM_Z + 1.00335
            DBItem_13C1Intensity = 1.081572829 * DBItemCNumber
            DBItem_13C2 = DBItemM_Z + 1.00335 * 2
            DBItem_13C2Intensity = (1.081572829 * DBItemCNumber) ** 2 / 200

            if sampleItemIntensity * DBItem_13C1Intensity / 100.0 < self.deleteBlankIntensity:
                ret.append(sampleItem + DBItem)
                break
            else:
                # 3.sampleItemIntensity>self.DelIsoIntensityX 且 DBItem_13C2Intensity>self.DelIso_13C2RelativeIntensity
                # if (sampleItemIntensity > self.DelIsoIntensityX) and (DBItem_13C2Intensity > self.DelIso_13C2RelativeIntensity):
                # 3.sampleItemIntensity * DBItem_13C2Intensity > self.deleteBlankIntensity
                if sampleItemIntensity * DBItem_13C2Intensity > self.deleteBlankIntensity:
                    # 4.样本(self.deleteBlankResult)中所有mass是否有对应的“13C1”和“13C2”及intensity相近
                    parameterList = [DBItem_13C1, DBItem_13C1Intensity, DBItem_13C2, DBItem_13C2Intensity, sampleItemIntensity]
                    retValue = self.DelIsoHasCorrespondInSample(parameterList)
                    if retValue[0]:
                        ret.append(sampleItem + DBItem)
                        ret.append(retValue[1] + ["iostope"])
                        if len(ret) == 3:
                            ret.append(retValue[2] + ["iostope"])
                        break
                else:
                    # 5.样本中是否有对应的“13C1”及intensity1相近
                    parameterList = [DBItem_13C1, DBItem_13C1Intensity, sampleItemIntensity]
                    retValue = self.DelIsoHasCorrespondInSample(parameterList)
                    if retValue[0]:
                        ret.append(sampleItem + DBItem)
                        ret.append(retValue[1] + ["iostope"])
                        break

        if len(ret) == 0:
            ret.append(sampleItem)
        ret.append([])

        return ret

    # 4.样本(self.deleteBlankResult)中所有mass是否有对应的“13C1”和“13C2”及intensity相近。5.样本中是否有对应的“13C1”及intensity1相近
    def DelIsoHasCorrespondInSample(self, parameterList):
        if len(parameterList) == 5:  # 4.样本(self.deleteBlankResult)中所有mass是否有对应的“13C1”和“13C2”及intensity相近
            # 返回值可能为：[False]，[True, []]，[True, [], []]
            DBItem_13C1 = parameterList[0]
            DBItem_13C1Intensity = parameterList[1]
            DBItem_13C2 = parameterList[2]
            DBItem_13C2Intensity = parameterList[3]
            sampleItemIntensity = parameterList[4]
            ret = []
            for item in self.deleteBlankResult:
                Mass = item[0]
                Intensity = item[1]
                # if (abs((Mass - DBItem_13C1) * 1000000.0 / DBItem_13C1)) <= self.DelIsoIsotopeMassDeviation and \
                #         (abs((Intensity * 100.0 / sampleItemIntensity - DBItem_13C1Intensity) * 100.0 / DBItem_13C1Intensity) < self.DelIsoIsotopeIntensityDeviation):
                if (abs((Mass - DBItem_13C1) * 1000000.0 / DBItem_13C1)) <= self.DelIsoIsotopeMassDeviation and \
                        (abs((Intensity * 100.0 / sampleItemIntensity - DBItem_13C1Intensity)) < self.DelIsoIsotopeIntensityDeviation):
                    ret.append(True)
                    ret.append(item)
                    break
            for item in self.deleteBlankResult:
                Mass = item[0]
                Intensity = item[1]
                # if (abs((Mass - DBItem_13C2) * 1000000.0 / DBItem_13C2)) <= self.DelIsoIsotopeMassDeviation and \
                #         (abs((Intensity * 100.0 / sampleItemIntensity - DBItem_13C2Intensity) * 100.0 / DBItem_13C2Intensity) < self.DelIsoIsotopeIntensityDeviation):
                if (abs((Mass - DBItem_13C2) * 1000000.0 / DBItem_13C2)) <= self.DelIsoIsotopeMassDeviation and \
                        (abs((Intensity * 100.0 / sampleItemIntensity - DBItem_13C2Intensity)) < self.DelIsoIsotopeIntensityDeviation):
                    if len(ret) == 0:
                        ret.append(True)
                    ret.append(item)
                    break
            if len(ret) == 0:
                ret.append(False)
            return ret
        elif len(parameterList) == 3:  # 5.样本中是否有对应的“13C1”及intensity1相近
            # 返回值可能为：[False]，[True, []]
            DBItem_13C1 = parameterList[0]
            DBItem_13C1Intensity = parameterList[1]
            sampleItemIntensity = parameterList[2]
            ret = []
            for item in self.deleteBlankResult:
                Mass = item[0]
                Intensity = item[1]
                # if (abs((Mass - DBItem_13C1) * 1000000.0 / DBItem_13C1)) <= self.DelIsoIsotopeMassDeviation and \
                #         (abs((Intensity * 100.0 / sampleItemIntensity - DBItem_13C1Intensity) * 100.0 / DBItem_13C1Intensity) < self.DelIsoIsotopeIntensityDeviation):
                if (abs((Mass - DBItem_13C1) * 1000000.0 / DBItem_13C1)) <= self.DelIsoIsotopeMassDeviation and \
                        (abs((Intensity * 100.0 / sampleItemIntensity - DBItem_13C1Intensity)) < self.DelIsoIsotopeIntensityDeviation):
                    ret.append(True)
                    ret.append(item)
                    break
            if len(ret) == 0:
                ret.append(False)
            return ret

        # 传入的参数个数错误
        if ConstValues.PsIsDebug:
            print(
                "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                sys._getframe().f_code.co_name, "\" method***：",
                "parameterList参数错误！"
            )

        return False

    # 峰识别按照Formula（主键），C（次主键）从小到大顺序排序
    def DelIsoSort(self, result):
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
        length = len(result)
        while i < length:
            firstItem = result[i]
            if len(firstItem) != 8:
                i += 1
                continue
            # 此时找到第一个符合条件的记录，查找其紧随的下面是否有 类型三
            item = [firstItem]  # 是一个二维列表，对应一种物质
            i += 1
            nextItem = result[i]
            while len(nextItem) != 0:
                item.append(nextItem)
                i += 1
                nextItem = result[i]

            key = firstItem[2]  # "Class"作为键
            if key in dataDirectory.keys():
                dataDirectory[key].append(item)
                dataOneDirectory[key].append([firstItem[3]] + [firstItem[6]] + [len(dataOneDirectory[key])])
            else:
                dataDirectory[key] = [item]
                dataOneDirectory[key] = [[firstItem[3]] + [firstItem[6]] + [0]]
            # 查看下一条数据
            i += 1

        # 对dataOneDirectory中的各项进行排序
        for key in dataOneDirectory.keys():
            dataOneDirectory[key] = sorted(dataOneDirectory[key], key=(lambda x: [x[0], x[1]]), reverse=False)

        # 重新整理结果
        ret = [["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]]
        for key in dataOneDirectory.keys():
            data = dataOneDirectory[key]
            for item1 in data:
                for item2 in dataDirectory[key][item1[2]]:
                    ret.append(item2)
                ret.append([])

        return ret


