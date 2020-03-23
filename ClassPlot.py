# coding=utf-8
# 此文件负责定义：负责画图
import matplotlib.pyplot as plt
from Utils import *
from ConstValues import ConstValues


class ClassPlot:
    def __init__(self, parameterList, outputFilesPath):
        assert len(parameterList) == 14, "ClassPlot参数个数不对!"
        self.RemoveFPId = parameterList[0]  # 判断选择了哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
        self.RemoveFPResult = parameterList[1]  # 所有类别去假阳性的结果，二维列表，有表头
        self.PlotTitleName = parameterList[2]  # 标题名称
        self.PlotTitleColor = parameterList[3]  # 标题颜色，(R, G, B, Alpha)，针对plt，值为0~255，需要转为0~1
        self.PlotXAxisName = parameterList[4]  # x轴名称
        self.PlotXAxisColor = parameterList[5]  # x轴颜色，(R, G, B, Alpha)，针对plt，值为0~255，需要转为0~1
        self.PlotYAxisName = parameterList[6]  # y轴名称
        self.PlotYAxisColor = parameterList[7]  # y轴颜色，(R, G, B, Alpha)，针对plt，值为0~255，需要转为0~1
        self.PlotHasEnter = parameterList[8]  # 记录是否进入过PlotSetup()函数
        self.PlotType = parameterList[9]  # 绘图类型
        self.PlotClassList = parameterList[10]  # 列表，需要绘制的类型，例子：["CH", "N1"]
        self.PlotClassItem = parameterList[11]  # 列表，需要绘制的类型，例子：["CH"]，对应单选钮，长度必须为1
        self.PlotDBENum = parameterList[12]  # 整数，记录用户选择的DBE数目
        self.PlotConfirm = parameterList[13]  # 是否需要绘图

        # 用户选择的文件的生成位置
        self.outputFilesPath = outputFilesPath

        # 去掉表头
        self.RemoveFPResult = self.RemoveFPResult[1:]

    # 主逻辑，画图
    def Plot(self):
        # 添加坐标名称，标题
        plt.xlabel(self.PlotXAxisName, fontproperties='SimHei', fontsize=12, color=[num / 255 for num in self.PlotXAxisColor])
        plt.ylabel(self.PlotYAxisName, fontproperties='SimHei', fontsize=12, color=[num / 255 for num in self.PlotYAxisColor])

        # 创建对应文件夹
        newDirectory = CreateDirectory(self.outputFilesPath, "./intermediateFiles", "/_7_plot")

        # 3.搜同位素 去假阳性后的数据
        # ["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
        ClassIndex = 2  # 类别对应的Index
        DBEIndex = 3  # 不饱和度对应的Index
        CIndex = 6  # C数对应的Index
        if self.RemoveFPId == 2:  # 4.峰识别 去假阳性后的数据，需要加和的为area
            # ["SampleMass", "Area", "startRT", "startRTValue", "endRT", "endRTValue", "TICMassMedian",
            # "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
            ClassIndex = 7
            DBEIndex = 8
            CIndex = 11
        sumIndex = 1  # 需要加和的为SampleIntensity，或者Area

        # 根据图的类型不同，绘制图形
        if self.PlotType == 1:  # Class distribution
            if len(self.PlotClassList) == 0:  # 不存在要绘制的类别，绘制失败
                plt.close()
                return None, []

            # 计算所需要的数据
            sumList = [0.0 for _ in range(len(self.PlotClassList))]
            # 转为字典，方便后面查找指定类型对应索引
            PlotClassDictionary = dict(zip(self.PlotClassList, [i for i in range(len(self.PlotClassList))]))
            for item in self.RemoveFPResult:
                if len(item) != 0:
                    itemClass = item[ClassIndex]
                    if itemClass in self.PlotClassList:
                        itemIndex = PlotClassDictionary[itemClass]  # 查询对应类别的下标
                        sumList[itemIndex] += item[sumIndex]
            sum = 0  # 计算总和
            for num in sumList:
                sum += num
            # 计算比例
            sumList = [num*100/sum for num in sumList]

            # 添加标题
            plt.title(self.PlotTitleName, fontproperties='SimHei', fontsize=12, color=[num / 255 for num in self.PlotTitleColor])
            # 可以绘制图形，横坐标：self.PlotClassList，纵坐标：sumList
            plt.bar(self.PlotClassList, sumList)
            imagePath = newDirectory + "/" + self.PlotTitleName
            plt.savefig(fname=imagePath, dpi=150)
            # 关闭绘图
            plt.close()
            # 返回图片路径
            return imagePath + ".png", [[self.PlotXAxisName]+self.PlotClassList, [self.PlotYAxisName]+[num/100 for num in sumList]]
        elif self.PlotType == 2:  # DBE distribution by class
            if len(self.PlotClassItem) == 0:  # 不存在要绘制的类别，绘制失败
                plt.close()
                return None, []

            # 计算所需要的数据
            DBEDictionary = {}  # key : DBE ,   value : 总量

            for item in self.RemoveFPResult:
                if len(item) != 0:
                    itemClass = item[ClassIndex]  # 获取类别
                    itemDBE = item[DBEIndex]  # DBE数目
                    if itemClass in self.PlotClassItem:
                        if itemDBE not in DBEDictionary:
                            DBEDictionary[itemDBE] = item[sumIndex]
                        else:
                            DBEDictionary[itemDBE] += item[sumIndex]

            # 提取出横纵坐标
            xList = []
            yList = []
            for key in sorted(DBEDictionary):
                value = DBEDictionary[key]
                xList.append(key)
                yList.append(value)

            sum = 0  # 计算总和
            for num in yList:
                sum += num
            yList = [num * 100 / sum for num in yList]  # 计算比例

            # 添加标题
            title = self.PlotTitleName + "_(" + str(self.PlotClassItem[0]) + ")"
            plt.title(title, fontproperties='SimHei', fontsize=12, color=[num / 255 for num in self.PlotTitleColor])
            # 可以绘制图形，横坐标：xList，纵坐标：yList
            plt.bar(xList, yList)
            imagePath = newDirectory + "/" + title
            plt.savefig(fname=imagePath, dpi=150)
            # 关闭绘图
            plt.close()
            # 返回图片路径
            return imagePath + ".png", [[self.PlotXAxisName]+xList, [self.PlotYAxisName]+[num / 100 for num in yList]]
        elif self.PlotType == 3:  # Carbon number distribution by class and DBE
            if (len(self.PlotClassItem) == 0) or (self.PlotDBENum == ConstValues.PsPlotDBENum):  # 不存在要绘制的类别，绘制失败
                plt.close()
                return None, []

            # 计算所需要的数据
            CDictionary = {}  # key : C ,   value : 总量

            for item in self.RemoveFPResult:
                if len(item) != 0:
                    itemClass = item[ClassIndex]  # 获取类别
                    itemDBE = item[DBEIndex]  # DBE数目
                    itemCNum = item[CIndex]
                    if (itemClass in self.PlotClassItem) and (self.PlotDBENum == itemDBE):
                        if itemDBE not in CDictionary:
                            CDictionary[itemCNum] = item[sumIndex]
                        else:
                            CDictionary[itemCNum] += item[sumIndex]

            # 提取出横纵坐标
            xList = []
            yList = []
            for key in sorted(CDictionary):
                value = CDictionary[key]
                xList.append(key)
                yList.append(value)

            sum = 0  # 计算总和
            for num in yList:
                sum += num
            yList = [num * 100 / sum for num in yList]  # 计算比例

            # 添加标题
            title = self.PlotTitleName + "_(" + str(self.PlotClassItem[0]) + "_DBE_" + str(self.PlotDBENum) + ")"
            plt.title(title, fontproperties='SimHei', fontsize=12, color=[num / 255 for num in self.PlotTitleColor])
            # 可以绘制图形，横坐标：xList，纵坐标：yList
            plt.bar(xList, yList)
            imagePath = newDirectory + "/" + title
            plt.savefig(fname=imagePath, dpi=150)
            # 关闭绘图
            plt.close()
            # 返回图片路径
            return imagePath + ".png", [[self.PlotXAxisName]+xList, [self.PlotYAxisName]+[num / 100 for num in yList]]
        elif self.PlotType == 4:  # DBE vs carbon number by class
            if len(self.PlotClassItem) == 0:  # 不存在要绘制的类别，绘制失败
                plt.close()
                return None, []

            # 计算所需要的数据
            DBECDictionary = {}  # key : (DBE, CNum),   value : 总量

            for item in self.RemoveFPResult:
                if len(item) != 0:
                    itemClass = item[ClassIndex]  # 获取类别
                    itemDBE = item[DBEIndex]  # DBE数目
                    itemCNum = item[CIndex]
                    if itemClass in self.PlotClassItem:  # 是需要绘制的类别
                        if (itemDBE, itemCNum) not in DBECDictionary:
                            DBECDictionary[(itemDBE, itemCNum)] = item[sumIndex]
                        else:
                            DBECDictionary[(itemDBE, itemCNum)] += item[sumIndex]

            # 提取出横纵坐标，气泡图的大小
            xList = []
            yList = []
            sizeList = []
            for key in sorted(DBECDictionary):
                value = DBECDictionary[key]
                xList.append(key[1])  # CNum
                yList.append(key[0])  # DBE
                sizeList.append(value)

            sum = 0  # 计算总和
            for num in sizeList:
                sum += num
            scaledSizeList = [num * 10000 / sum for num in sizeList]  # 计算比例

            # 添加标题
            title = self.PlotTitleName + "_(" + str(self.PlotClassItem[0]) + ")"
            plt.title(title, fontproperties='SimHei', fontsize=12, color=[num / 255 for num in self.PlotTitleColor])
            # 可以绘制图形，横坐标：xList，纵坐标：yList
            plt.scatter(xList, yList, s=scaledSizeList, c="red", alpha=0.6)
            imagePath = newDirectory + "/" + title
            plt.savefig(fname=imagePath, dpi=150)
            # 关闭绘图
            plt.close()
            # 返回图片路径
            return imagePath + ".png", [[self.PlotXAxisName]+xList, [self.PlotYAxisName]+yList, ["Size"]+sizeList]
        elif self.PlotType == 5:  # Kendrick mass defect （KMD）
            def round_up(num):
                # 默认num大于0，用round函数会造成数据错误，如：round(2.5) --> 2
                integer = int(num)
                decimalNum = num - integer
                if decimalNum >= 0.5:
                    return integer + 1
                else:
                    return integer

            sampleMassIndex = 0
            sampleMassSet = set()  # 记录不同的 sampleMass
            xList = []  # KM
            yList = []  # KMD
            for item in self.RemoveFPResult:
                if len(item) != 0:
                    # 获取sampleMass
                    sampleMass = item[sampleMassIndex]
                    # 记录数据
                    if sampleMass not in sampleMassSet:
                        KM = (sampleMass * 14.0) / 14.01565
                        NKM = round_up(KM)
                        KMD = NKM - KM
                        xList.append(NKM)
                        yList.append(KMD)
                    # 集合中添加元素
                    sampleMassSet.add(sampleMass)

            # 添加标题
            plt.title(self.PlotTitleName, fontproperties='SimHei', fontsize=12, color=[num / 255 for num in self.PlotTitleColor])
            # 可以绘制图形，横坐标：xList，纵坐标：yList
            plt.scatter(xList, yList, s=20, c="blue", alpha=0.8)
            imagePath = newDirectory + "/" + self.PlotTitleName
            plt.savefig(fname=imagePath, dpi=150)
            # 关闭绘图
            plt.close()
            # 返回图片路径
            return imagePath + ".png", [[self.PlotXAxisName] + xList, [self.PlotYAxisName] + yList]
        elif self.PlotType == 6:  # Retention time vs carbon number
            if (len(self.PlotClassItem) == 0) or (self.PlotDBENum == ConstValues.PsPlotDBENum):  # 不存在要绘制的类别，绘制失败
                plt.close()
                return None, []

            # startRTValue 位置
            startRTValueIndex = 3
            # 计算所需要的数据
            xList = []  # CNum
            yList = []  # startRTValue

            for item in self.RemoveFPResult:
                if len(item) != 0:
                    itemClass = item[ClassIndex]  # 获取类别
                    itemDBE = item[DBEIndex]  # DBE数目
                    itemCNum = item[CIndex]  # C的数目
                    itemStartRTValue = item[startRTValueIndex]
                    if (itemClass in self.PlotClassItem) and (self.PlotDBENum == itemDBE):
                        xList.append(itemCNum)
                        yList.append(itemStartRTValue)

            # 添加标题
            title = self.PlotTitleName + "_(" + str(self.PlotClassItem[0]) + "_DBE_" + str(self.PlotDBENum) + ")"
            plt.title(title, fontproperties='SimHei', fontsize=12, color=[num / 255 for num in self.PlotTitleColor])
            # 可以绘制图形，横坐标：xList，纵坐标：yList
            plt.scatter(xList, yList, s=20, c="blue", alpha=0.8)
            imagePath = newDirectory + "/" + title
            plt.savefig(fname=imagePath, dpi=150)
            # 关闭绘图
            plt.close()
            # 返回图片路径
            return imagePath + ".png", [[self.PlotXAxisName]+xList, [self.PlotYAxisName]+[num / 100 for num in yList]]



