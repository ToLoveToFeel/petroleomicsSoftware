# coding=utf-8
# 此文件负责定义：生成数据库
from Utils import *
from PromptBox import PromptBox


class ClassGenerateDataBase():
    def __init__(self, parameterList, outputFilesPath):
        assert len(parameterList) == 11, "ClassGenerateDataBase参数不对"
        self.GDBClass = parameterList[0]  # 数据库生成(参数)：Class类型
        # 1~100（整数）
        self.GDBCarbonRangeLow = parameterList[1]  # 数据库生成(参数)：carbon rage(碳数范围)最小值(包含)
        self.GDBCarbonRangeHigh = parameterList[2]  # 数据库生成(参数)：carbon rage(碳数范围)最大值(包含)
        # 1~30（整数）
        self.GDBDBERageLow = parameterList[3]  # 数据库生成(参数)：DBE rage(不饱和度范围)最小值(包含)
        self.GDBDBERageHigh = parameterList[4]  # 数据库生成(参数)：DBE rage(不饱和度范围)最大值(包含)
        # 50~1500(整数)
        self.GDBM_ZRageLow = parameterList[5]  # 数据库生成(参数)：m/z rage(质荷比范围)最小值(包含)
        self.GDBM_ZRageHigh = parameterList[6]  # 数据库生成(参数)：m/z rage(质荷比范围)最大值(包含)
        # 离子类型
        self.GDB_MHPostive = parameterList[7]  # 数据库生成(参数)：正离子，是否选择[M+H]+，True为选中
        self.GDB_MPostive = parameterList[8]  # 数据库生成(参数)：正离子，是否选择M+，True为选中
        self.GDB_MHNegative = parameterList[9]  # 数据库生成(参数)：负离子，是否选择[M-H]-，True为选中
        self.GDB_MNegative = parameterList[10]  # 数据库生成(参数)：负离子，是否选择M-，True为选中
        # 用户选择的文件的生成位置
        self.outputFilesPath = outputFilesPath

    # 负责生成数据库
    def GenerateData(self):
        # excel表头
        header = ["Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]

        # 判断最后一列（ion）应该填入什么
        isPositive = self.GDB_MHPostive or self.GDB_MPostive  # 是否为正离子
        # isChoiceTwo = 0  # 是否勾选了两项
        if isPositive:
            isChoiceTwo = self.GDB_MHPostive + self.GDB_MPostive
        else:
            isChoiceTwo = self.GDB_MHNegative + self.GDB_MNegative

        # 生成数据主逻辑
        if isPositive:
            if isChoiceTwo == 2:  # 说明选择的是两个正离子
                data = self._GenerateData([1, 2])
            elif self.GDB_MHPostive:  # 说明选择的是一个正离子[M＋H]+
                data = self._GenerateData([1])
            else:  # 说明选择的是一个正离子M+
                data = self._GenerateData([2])
        else:
            if isChoiceTwo == 2:  # 说明选择的是两个负离子
                data = self._GenerateData([3, 4])
            elif self.GDB_MHNegative == True:  # 说明选择的是一个负离子[M-H]-
                data = self._GenerateData([3])
            else:  # 说明选择的是一个负离子M-
                data = self._GenerateData([4])

        result = [header]  # 根据m/z筛选符合条件的item
        # result.append(header)
        for item in data:
            if self.GDBM_ZRageLow <= item[3] <= self.GDBM_ZRageHigh:
                result.append(item)

        # 数据写入excel文件中
        newDirectory = CreateDirectory(self.outputFilesPath, "./intermediateFiles", "/_2_generateDataBase")
        WriteDataToExcel(result, newDirectory + "/" + ConstValues.PsNameGDB)

        return result, True

    # 根据类型生成数据
    def _GenerateData(self, typeList):
        data = []
        for Class in self.GDBClass:  # 对每个Class会生成多条NeutralDBE
            # 计算N的数目，为后面排除不符合要求数据使用
            NNumber = 0
            for i in range(len(Class)):
                if Class[i] == "N":
                    NNumber = int(Class[i + 1])
                    break
            for NeutralDBE in range(self.GDBDBERageLow, self.GDBDBERageHigh + 1):  # 对每个NeutralDBE会根据C数不同生成不同的分子式
                for CNumber in range(self.GDBCarbonRangeLow, self.GDBCarbonRangeHigh + 1):  # 每个C数生成一个分子式（可能对应两项数据）
                    if CNumber >= NeutralDBE / 0.9 - NNumber:  # 排除一些不法分子式
                        for i in typeList:
                            item = self.GenerateItem(Class, NeutralDBE, CNumber, i)
                            if item is not None:
                                data.append(item)
        return data

    # 负责生成excel某一行（项）
    def GenerateItem(self, Class, NeutralDBE, CNumber, IonType):
        """
        :param Class: 物质类型，字符串类型，（N1，N1O1，N1S1，O1S1，N2，N1O2，O1，O2，S1，CH），必须保证1个原子也要写上1，除了CH
        :param NeutralDBE: DBE(不饱和度)，整数类型1~30
        :param CNumber: carbon number(碳数目)，整数类型1~100
        :param IonType: (离子类型选项)：包括[M＋H]+和M+和[M-H]-和M-(可选择一个也可以选择两个，只能选相同电荷的)
                        1：代表[M＋H]+
                        2：代表M+
                        3：代表[M-H]-
                        4：代表M-
        :return:
        """
        # 计算各元素的数目
        # O的数目，N的数目，S的数目
        ONumber = 0
        NNumber = 0
        SNumber = 0
        for i in range(len(Class)):
            if Class[i] == "O":
                ONumber = int(Class[i + 1])
            elif Class[i] == "N":
                NNumber = int(Class[i + 1])
            elif Class[i] == "S":
                SNumber = int(Class[i + 1])
        # H的数目，class为Nz（这里z表示氮的个数）DBE为x，碳数为y,则formula为Cy H 2y+z-2x+2 Nz
        HNumber = 2 * CNumber + NNumber - 2 * NeutralDBE + 2

        # H数少于0，可以直接排除
        if HNumber <= 0:
            return None

        # 生成分子式
        formula = "C" + str(CNumber)
        formula = formula + "H" + str(HNumber)
        if Class != "CH":
            formula += Class

        # 根据用户选择计算cal m/z，ion
        calMZ = 0.0
        ion = None
        if IonType == 1:  # 代表[M＋H]+
            calMZ = CNumber * 12.0 + HNumber * 1.007825 \
                    + ONumber * 15.994915 + NNumber * 14.003074 + SNumber * 31.972071 + 1.007277
            ion = "H"
        elif IonType == 2:  # 代表M+
            calMZ = CNumber * 12.0 + HNumber * 1.007825 + \
                    ONumber * 15.994915 + NNumber * 14.003074 + SNumber * 31.972071 + 0.000549
        elif IonType == 3:  # 代表[M-H]-
            calMZ = CNumber * 12.0 + HNumber * 1.007825 + \
                    ONumber * 15.994915 + NNumber * 14.003074 + SNumber * 31.972071 - 1.007276
            ion = "H"
        elif IonType == 4:  # 代表M-
            calMZ = CNumber * 12.0 + HNumber * 1.007825 + \
                    ONumber * 15.994915 + NNumber * 14.003074 + SNumber * 31.972071 - 0.000548
        item = []
        item.append(Class)  # 字符串
        item.append(NeutralDBE)  # 整数
        item.append(formula)  # 字符串
        item.append(calMZ)  # 浮点数
        item.append(CNumber)  # 整数
        if ion != None:
            item.append(ion)  # 字符串

        return item
