# coding=utf-8
# 此文件负责定义：负责画图
import matplotlib.pyplot as plt
from Utils import *
from ConstValues import ConstValues


class ClassPlot:
    def __init__(self, parameterList, outputFilesPath):
        assert len(parameterList) == 11, "ClassPlot参数个数不对!"
        self.RemoveFPId = parameterList[0]  # 判断选择了哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
        self.RemoveFPResult = parameterList[1]  # 所有类别去假阳性的结果，二维列表，有表头
        self.PlotHasEnter = parameterList[2]  # 记录是否进入过PlotSetup()函数
        self.PlotType = parameterList[3]  # 绘图类型
        self.PlotClassList = parameterList[4]  # 列表，需要绘制的类型，例子：["CH", "N1"]
        self.PlotTitleName = parameterList[5]  # 标题名称
        self.PlotTitleColor = parameterList[6]  # 标题颜色，(R, G, B, Alpha)，针对plt，值为0~255，需要转为0~1
        self.PlotXAxisName = parameterList[7]  # x轴名称
        self.PlotXAxisColor = parameterList[8]  # x轴颜色，(R, G, B, Alpha)，针对plt，值为0~255，需要转为0~1
        self.PlotYAxisName = parameterList[9]  # y轴名称
        self.PlotYAxisColor = parameterList[10]  # y轴颜色，(R, G, B, Alpha)，针对plt，值为0~255，需要转为0~1

        # 用户选择的文件的生成位置
        self.outputFilesPath = outputFilesPath

    # 主逻辑，画图
    def Plot(self):
        # 添加标题
        plt.title(self.PlotTitleName, fontproperties='SimHei', fontsize=12, color=[num / 255 for num in self.PlotTitleColor])
        # 添加坐标名称，标题
        plt.xlabel(self.PlotXAxisName, fontproperties='SimHei', fontsize=12, color=[num / 255 for num in self.PlotXAxisColor])
        plt.ylabel(self.PlotYAxisName, fontproperties='SimHei', fontsize=12, color=[num / 255 for num in self.PlotYAxisColor])

        # 创建对应文件夹
        newDirectory = CreateDirectory(self.outputFilesPath, "./intermediateFiles", "/_7_plot")

        # 根据图的类型不同，绘制图形
        if self.PlotType == 1:  # Class distribution
            if len(self.PlotClassList) == 0:  # 不存在要绘制的类别，绘制失败
                plt.close()
                return None, []
            # 3.搜同位素 去假阳性后的数据
            # ["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
            ClassIndex = 2
            sumIndex = 1  # 需要加和的为SampleIntensity
            if self.RemoveFPId == 2:  # 4.峰识别 去假阳性后的数据，需要加和的为area
                # ["SampleMass", "Area", "startRT", "startRTValue", "endRT", "endRTValue", "TICMassMedian",
                # "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
                ClassIndex = 7

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

            # 可以绘制图形，横坐标：self.PlotClassList，纵坐标：sumList
            plt.bar(self.PlotClassList, sumList)
            imagePath = newDirectory + "/" + self.PlotTitleName
            plt.savefig(fname=imagePath, dpi=150)
            # 关闭绘图
            plt.close()
            # 返回图片路径
            return imagePath + ".png", [self.PlotClassList, [num/100 for num in sumList]]

        elif self.PlotType == 2:  # DBE distribution by class
            pass
        elif self.PlotType == 3:  # Carbon number distribution by class and DBE
            pass
        elif self.PlotType == 4:  # van Krevelen by class
            pass
        elif self.PlotType == 5:  # DBE vs. carbon number by class
            pass
        elif self.PlotType == 6:  # Kendrick mass defect vs. m/z
            pass




