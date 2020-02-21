# coding=utf-8
# 此文件负责定义：去假阳性


class ClassRemoveFalsePositive:
    def __init__(self, parameterList, outputFilesPath):
        assert len(parameterList) == 5, "ClassRemoveFalsePositive参数个数不对!"
        self.RemoveFPId = parameterList[0]    # 1：去同位素之后的内容self.DelIsoResult 2：峰识别之后的内容self.DelIsoResult
        self.DelIsoResult = parameterList[1]  # 扣同位素后生成的文件，两项记录之间通过空列表分割（格式：list二维数组，有表头）
        self.PeakDisResult = parameterList[2]  # 峰识别第一阶段后生成的文件，两项记录之间通过空列表分割（格式：list二维数组，有表头）
        self.RemoveFPContinue_CNum = parameterList[3]
        self.RemoveFPContinue_DBENum = parameterList[4]

    def RemoveFalsePositive(self):
        result = []
        if self.RemoveFPId == 1:
            result = self.RemoveFPFromDelIso()
        elif self.RemoveFPId == 2:
            result = self.RemoveFPFromPeakDis()

        RemoveFPIsFinished = True
        return result, RemoveFPIsFinished

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
        dataOneDirectory = {}  # 某个分子式对应多条记录，只记录第一条，长度为9，最后一个数据记录其位置
        dataDeleteDirectory = {}  # 记录各个类别需要删除的索引

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
            nextItem = self.DelIsoResult[i]
            while len(nextItem) != 0:
                item.append(nextItem)
                i += 1
                nextItem = self.DelIsoResult[i]

            key = firstItem[2]  # "Class"作为键
            if key in dataDirectory:
                dataDirectory[key].append(item)
                dataOneDirectory[key].append(firstItem + [len(dataOneDirectory[key])])
            else:
                dataDirectory[key] = [item]
                dataOneDirectory[key] = [firstItem + [0]]

    # 从峰识别第一阶段后的文件里去假阳性
    def RemoveFPFromPeakDis(self):
        pass




