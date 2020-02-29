# coding=utf-8
# 此文件负责定义：峰识别第二阶段，峰检测分割
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import numpy as np
from Utils import *
from ConstValues import ConstValues
import traceback


class ClassPeakDivision:
    def __init__(self, parameterList, outputFilesPath):
        assert len(parameterList) == 7, "ClassPeakDivision参数个数不对!"
        self.RemoveFPId = parameterList[0]  # 判断选择了哪一个文件：self.DelIsoResult 或者 self.PeakDisResult
        self.RemoveFPPlotResult = parameterList[1]  # 去假阳性后的需要峰识别（第二部分）结果，二维列表，无表头
        self.sortedRTValue = parameterList[2]  # 第三个是txt文件中RT值(从小到大排序)

        self.PeakDivNoiseThreshold = parameterList[3]
        self.PeakDivRelIntensity = parameterList[4]
        self.PeakDivNeedMerge = parameterList[5]  # 该参数决定是否需要将溶剂效应的第一个峰融合到第二个峰
        self.PeakDivNeedGenImage = parameterList[6]  # 该参数决定是否生成图片信息
        # 用户选择的文件的生成位置
        self.outputFilesPath = outputFilesPath
        if ConstValues.PsIsSingleRun:
            self.RemoveFPPlotResult = \
                ReadExcelToList(filepath="./intermediateFiles/_5_removeFalsePositive/PeakDisPart1DetailPlotAfterRFP.xlsx", hasNan=False)
            self.sortedRTValue = ReadExcelToList(filepath="./intermediateFiles/_4_peakDistinguish/sortedRTValue.xlsx", hasNan=False)[0]

    # 第二部分，峰检测分割  ######################################################################
    def PeakDivision(self):
        try:
            resultPart2 = []  # 第二部分，峰检测与分割，即将多个峰分开输出
            headerPart2 = ["SampleMass", "Area", "PeakRT", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion", "orderOfMagnitude"]
            resultPart2.append(headerPart2)
            # 峰检测预处理
            ret1DetailPreprocessing = self.PeakDivPreprocessing()
            # 统计连续区间的个数
            ret1DetailContinueList = self.PeakDivSeekContinue(ret1DetailPreprocessing)
            # 为生成图片准备数据
            parametersList = self.PeakDivPrepareParams(ret1DetailPreprocessing, ret1DetailContinueList)
            # 生成图片，同时生成结果
            for parameters in parametersList:
                ret = self.PlotAfterRemoveFP(parameters)  # 返回结果为二维列表
                for item in ret:
                    resultPart2.append(item)
            # 数据写入文件
            newDirectory = CreateDirectory(self.outputFilesPath, "./intermediateFiles", "/_6_peakDivision")
            WriteDataToExcel(ret1DetailPreprocessing, newDirectory + "/ret1DetailPreprocessing.xlsx")
            WriteDataToExcel(resultPart2, newDirectory + "/PeakDivision.xlsx")

            return resultPart2, True
        except Exception as e:
            if ConstValues.PsIsDebug:
                print("plt Error : ", e)
                traceback.print_exc()

    # 峰检测预处理
    def PeakDivPreprocessing(self):
        # 返回结果：二维列表，和self.RemoveFPPlotResult格式完全一致

        # 预处理，删除一些干扰值，具体包括：
        # 1.设置噪音阈值: 500000，小于这个强度的都删除，这样应该删除一部分强度低，峰形不好的图像
        # 2.设置一个相对强度阈值：0.1%，这个和你之前的想法一样，就是删去每张图中，相对强度小于最高峰的0.1%的那些信号
        # TODO: 3.设置一个最小峰宽? 至少现在没有这一步

        # 二维列表，物质相关信息，后续拼接使用
        rawInformation = [[num for num in self.RemoveFPPlotResult[i][:9]] for i in range(len(self.RemoveFPPlotResult))]
        # 二维列表，峰识别第一阶段生成的需要进行第二阶段的数据，无表头，非数据项全部移除
        rawData = np.array([[num for num in self.RemoveFPPlotResult[i][9:]] for i in range(len(self.RemoveFPPlotResult))])
        rawData[rawData < self.PeakDivNoiseThreshold] = 0  # 第1步
        for i in range(len(rawData)):
            RelativeThreshold = np.max(rawData[i]) * self.PeakDivRelIntensity / 100.0  # 第2步
            rawData[i][rawData[i] < RelativeThreshold] = 0

        rawData = rawData.tolist()
        # 二维列表，最终结果
        ret1DetailPreprocessing = [rawInformation[i] + rawData[i] for i in range(len(rawInformation))]

        return ret1DetailPreprocessing

    # dataProcessing中所有行查到符合条件的记录集合
    def PeakDivSeekContinue(self, dataProcessing):
        """
        :param dataProcessing: 格式二维列表，
                    每一行["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion",....]
        :return: 三维列表，[[[...], ..., [..]], ..., [[...], ..., [..]]]
                    [[...], ..., [..]]代表dataProcessing每一行处理的结果
        """
        ret = []
        for item in dataProcessing:
            ret.append(self.PeakDivSeekContinueItem(item))
        return ret

    # dataProcessing中某一行查到符合连续条件（这里的连续是中间没有超过5个为0的点）的记录集合
    def PeakDivSeekContinueItem(self, item):
        # 返回内容格式：
        # 三维列表，[[[...], ..., [..]], ..., [[...], ..., [..]]]
        # [[...], ..., [..]]代表dataProcessing每一行处理的结果
        # 获取需要处理的数据
        itemData = item[9:]
        # 获取扫描点数目
        scanNum = len(itemData)
        # TODO:参数
        PeakDisDiscontinuityPointNum = 5

        ret = [item[:9]]  # ContinueList
        k = 0
        while k < scanNum:
            firstRT = 0
            continuityIntensities = []  # 存储连续的符合要求的记录，为列表[Intensity, ..., Intensity]
            while k < scanNum and firstRT == 0:
                firstRT = itemData[k]
                k += 1
            if k >= scanNum:
                break
            # 此时保证在itemData找到第一个不为0记录
            startRT = k - 1
            continuityIntensities.append(firstRT)  # 不严格连续

            # 寻找连续的符合要求的记录
            DiscontinuityPointNum = 0
            nextRT = itemData[k]
            if nextRT == 0:
                DiscontinuityPointNum += 1
            while k < scanNum and ((nextRT != 0) or DiscontinuityPointNum < PeakDisDiscontinuityPointNum):
                continuityIntensities.append(nextRT)
                if nextRT == 0:
                    DiscontinuityPointNum += 1
                else:
                    DiscontinuityPointNum = 0
                k += 1
                if k >= scanNum:
                    break
            # 到这里连续的记录已经结束
            continuityIntensities = np.array(continuityIntensities)
            Area = np.sum(continuityIntensities)  # 求面积
            endRT = startRT + len(continuityIntensities) - 1  # 结束的扫描点在TIC中属于第几个扫描点
            ret.append([startRT, endRT, Area])  # ContinueList

            # 本次连续的考察完毕，进行之后没有考虑的扫描点考察
            k += 1
        return ret

    # 为绘制峰准备数据
    def PeakDivPrepareParams(self, dataProcessing, ContinueList):
        """
        :param dataProcessing: 峰检测预处理后的数据
                每一行["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion",....]
        :param ContinueList: 数据的连续信息，[[[...], ..., [..]], ..., [[...], ..., [..]]]
                [[...], ..., [..]]代表dataProcessing每一行处理的结果
        :return: 返回一个二维列表[[..], ... , [...]]，[..]对应每个图片的参数信息
        """
        assert len(dataProcessing) == len(ContinueList), "Error1 in PeakDivPrepareParams!"
        assert len(dataProcessing[0][9:]) == len(self.sortedRTValue), "Error2 in PeakDivPrepareParams!"
        rawData = np.array([[num for num in dataProcessing[i][9:]] for i in range(len(self.RemoveFPPlotResult))])
        # 存储每行的最大值
        maxValueList = [np.max(item) for item in rawData]
        # 存储每个数据的数量级（数字），例如：10000
        orderValueList = [10 ** int(math.log10(maxValue+1)) for maxValue in maxValueList]  # +1是为了防止maxValue=0
        # 存储每个数据的数量级（字符串），例如：1e4
        orderStrList = ["1e" + str(int(math.log10(maxValue+1))) for maxValue in maxValueList]
        # 获取数据个数
        length = len(rawData[0])
        # 将数据进行平滑处理，分为两段平滑：[0...shortEdge]，[longEdge...length-1]
        shortWinLength = 101          # 平滑数据窗口大小
        longWinLength = 201
        shortEdge = int(length / 6)  # 3
        bufferLength = int(length / 20)  # 15
        longEdge = shortEdge - 2*bufferLength
        smoothData = []  # 平滑后的数据，每一项均为numpy类型数据
        for item in dataProcessing:
            data = item[9:]
            y1 = savgol_filter(data[:shortEdge], window_length=shortWinLength, polyorder=2)
            y2 = savgol_filter(data[longEdge:], window_length=longWinLength, polyorder=2)
            # 合并平滑后的数据：[0...shortEdge-bufferLength]，[bufferLength...length-1]
            y = np.hstack([y1[: shortEdge-bufferLength], y2[bufferLength:]])
            smoothData.append(y)
        # 主逻辑
        ret = []
        for i in range(len(ContinueList)):
            ContinueItem = ContinueList[i]  # 是个二维列表，最前面一项是个列表，表示该物质信息
            ret.append([dataProcessing[i], smoothData[i]])
            redList = []  # 一维列表
            areas = []  # 一维列表
            peakInfo = []  # 记录峰顶信息：二维列表，因为可能有多个峰[[index, RT, Intensity], ..., [...]]
            if len(ContinueItem) == 1:  # 说明该图为空图
                areas.append(0)
            elif (len(ContinueItem) == 2) and \
                    ((ContinueItem[1][1]-ContinueItem[1][0]) <= int(length/10)):  # 说明只有一项连续的数据，并且很窄
                redList = ContinueItem[1][:2]
                areas = [format(ContinueItem[1][2]/orderValueList[i], '.2f')]
                # 计算峰顶信息，smoothData[a:b]最大值对应的索引对应的实际值
                peakMaxIndex = np.argmax(smoothData[i][ContinueItem[1][0]:ContinueItem[1][1]]) + ContinueItem[1][0]
                peakMaxIntensity = format(rawData[i][peakMaxIndex]/orderValueList[i], '.3f')
                peakInfo.append([peakMaxIndex, self.sortedRTValue[peakMaxIndex], peakMaxIntensity])
            else:  # 说明有一项既以上的连续数据，此时需要峰分割，只有一项连续的数据，不窄，重点逻辑
                redList, areas, peakInfo = self.PeakDivSplit(rawData[i], smoothData[i], orderValueList[i])
            parameters = [redList, areas, peakInfo, orderStrList[i], maxValueList[i]]
            ret[i].append(parameters)

        return ret

    # 重点逻辑，峰分割
    def PeakDivSplit(self, rawdata, smoothdata, ordervalue):
        """
        :param rawdata: 原始数据，一维numpy格式
        :param smoothdata: 平滑处理后的数据，一维numpy格式
        :param ordervalue: rawdata中最大值
        :return:
        """
        # 返回内容
        ret = []
        areas = []
        # 定义峰谷，峰顶左右比较数据的偏移量
        # 若：smoothdata[i] < smoothdata[i-deviation]，smoothdata[i] < smoothdata[i+deviation]，smoothdata[i]是峰底
        # 若：smoothdata[i] > smoothdata[i-deviation]，smoothdata[i] > smoothdata[i+deviation]，smoothdata[i]是峰顶
        deviation = int(len(rawdata) / 75)
        # 平滑后的数据的最大值
        smoothMax = np.max(smoothdata)
        i = deviation
        while i < len(smoothdata) - deviation:
            # 寻找峰谷
            while (i < len(smoothdata) - deviation) and \
                    not ((smoothdata[i] < smoothdata[i-deviation]) and (smoothdata[i] < smoothdata[i+deviation])):
                i += 1
            left = i
            # 寻找峰顶
            while (i < len(smoothdata) - deviation) and \
                    not ((smoothdata[i] > smoothdata[i-deviation]) and (smoothdata[i] > smoothdata[i+deviation])):
                i += 1
            top = i
            # 寻找峰谷
            while (i < len(smoothdata) - deviation) and \
                    not ((smoothdata[i] < smoothdata[i - deviation]) and (smoothdata[i] < smoothdata[i + deviation])):
                i += 1
            right = i
            # 判断峰是否足够高
            while (i < len(smoothdata) - deviation) and (smoothdata[top] - smoothdata[right] < smoothMax / 100):
                # 寻找峰顶
                while (i < len(smoothdata) - deviation) and \
                        not ((smoothdata[i] > smoothdata[i - deviation]) and (smoothdata[i] > smoothdata[i + deviation])):
                    i += 1
                top = i
                # 寻找峰谷
                while (i < len(smoothdata) - deviation) and \
                        not ((smoothdata[i] < smoothdata[i - deviation]) and (smoothdata[i] < smoothdata[i + deviation])):
                    i += 1
                right = i
            if i < len(smoothdata) - deviation:
                ret.append(left)
                ret.append(right)
                # 计算面积
                areas.append(format(np.sum(rawdata[left:right])/ordervalue, '.2f'))
        # 面积小于0.05的峰，删除
        areaThreshold = 0.05
        redList = []
        areasList = []
        k = 0
        while k < len(areas):
            if float(areas[k]) >= areaThreshold:
                redList.append(ret[2*k])
                redList.append(ret[2*k+1])
                areasList.append(areas[k])
            k += 1
        # 计算峰顶相关信息，smoothData[a:b]最大值对应的索引对应的实际值
        peakInfo = []
        for i in range(len(areasList)):
            peakLeft = redList[2*i]
            peakRight = redList[2*i+1]
            peakMaxIndex = np.argmax(smoothdata[peakLeft:peakRight]) + peakLeft
            peakMaxIntensity = rawdata[peakMaxIndex] / ordervalue  # 可能为0，因为存在不连续的点

            tempIndex = peakMaxIndex
            tempIntensity = peakMaxIntensity
            while tempIntensity == 0.0:  # 寻找邻近的不为0的点
                tempIndex += 1  # peakMaxIndex此时不一定是最大值对应的索引
                if tempIndex >= len(rawdata):
                    break
                tempIntensity = rawdata[tempIndex] / ordervalue
            if tempIndex >= len(rawdata):
                peakMaxIntensity = format(peakMaxIntensity, '.3f')  # str格式
            else:
                peakMaxIndex = tempIndex
                peakMaxIntensity = format(tempIntensity, '.3f')  # str格式

            peakInfo.append([peakMaxIndex, self.sortedRTValue[peakMaxIndex], peakMaxIntensity])  # 和areasList长度一致

        if self.PeakDivNeedMerge:  # 根据参数决定最前面的尖峰是否合并到后面
            lengthThreshold = int(len(smoothdata) / 15)  # 200左右
            leftThreshold = int(len(smoothdata) / 6)  # 500左右
            if len(areas) >= 3:  # 只有峰数大于等于三个才可能合并
                if redList[1] <= leftThreshold \
                        and (redList[1] - redList[0]) <= lengthThreshold \
                        and redList[1] == redList[2]:
                    sumArea = format(float(areasList[0]) + float(areasList[1]), '.2f')
                    del redList[2]
                    del redList[1]
                    del areasList[1]
                    del areasList[0]
                    del peakInfo[0]
                    areasList.insert(0, sumArea)

        return redList, areasList, peakInfo

    # 根据某个峰的数据，画出相应的图形
    def PlotAfterRemoveFP(self, parameters):
        """
        :param parameters: 生成该图片需要的所有数据
            item: 格式：["SampleMass", "SampleIntensity", "Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion",....]
            smoothItem: 该组数据平滑后的结果，只有item中的数据平滑后的结果
            parameters:
                redList: 列表，对应的位置红线,位置从小到大,不包含0 和 len(data)-1
                        [50, 100, 100, 425, 500, 700]代表[50...100]，[100...425]，[500...700]三个峰
                areas: 列表，各个峰的面积
                        [2.104, 3.105, 5.211]代表[50...100]，[100...425]，[500...700]三个峰的面积分别为2.104, 3.105, 5.211
                orderOfMagnitude: 面积的数量级，字符串格式，比如：1e8
                max: 该组数据的最大值（item的最大值），数字格式
        :return:
        """
        # 运行该函数一次生成一张图片
        item = parameters[0]
        smoothItem = parameters[1]
        parameter = parameters[2]
        # 二级参数
        redList = parameter[0]  # 列表
        areas = parameter[1]  # 列表，里面的数据是str
        peakInfo = parameter[2]  # 记录峰顶信息：二维列表，因为可能有多个峰[[index, RT, Intensity], ..., [...]]
        orderOfMagnitude = parameter[3]  # 字符串
        max = parameter[4]  # 浮点数

        # 将item分切为两部分，信息 和 数据
        information = item[:9]
        data = item[9:]
        # 横坐标
        x = [i for i in range(len(data))]
        # 文件输出需要的信息
        SampleMass = information[0]
        Class = information[2]  # 化合物类型
        DBENum = information[3]  # 不饱和度数目
        formula = information[4]
        CNum = information[6]
        # 返回值
        ret = []
        for i in range(len(areas)):
            ret.append([SampleMass, float(areas[i]), peakInfo[i][0]] + information[2:] + [orderOfMagnitude])
        if len(ret) != 0:
            ret.append([])
        if self.PeakDivNeedGenImage:  # 根据参数决定是否生成图片
            # 创建对应的文件夹
            newDirectory = CreateDirectory(self.outputFilesPath, "./intermediateFiles", "/_6_peakDivision/peakImages/" + Class + "_DBE" + str(DBENum))
            try:
                # 画图
                step = 0.05
                # 改变y坐标的范围
                bottomNum = 2 if len(peakInfo) <= 2 else len(peakInfo)
                plt.ylim(-(step * (bottomNum + 1) * max), (1+step*6) * max)
                # 添加坐标提示，标题
                plt.xlabel('RT', fontproperties='SimHei', fontsize=15, color='k')
                plt.ylabel('Intensity', fontproperties='SimHei', fontsize=15, color='k')
                title = "Mass:" + str(SampleMass) + "  DBE:" + str(DBENum) + "  formula:" + formula
                plt.title(title, fontproperties='SimHei', fontsize=12, color='red')
                # 画出线图，原始数据
                plt.vlines(x=x, ymin=0, ymax=data, colors="b", linewidth=1)
                # 画出峰之间以及两侧的分割线，+15为了修正画出来的偏移
                for splitIndex in redList:
                    plt.vlines(x=splitIndex+15, ymin=-int((step*2) * max), ymax=int((1+step*4) * max), colors="g", linewidth=0.5)
                # 添加峰面积信息
                for k in range(len(areas)):
                    start = redList[k*2]
                    end = redList[k*2+1]
                    middle = int((start + end) / 2 - 50)
                    plt.text(middle, int((1+step*(k % 2+1))*(max+1)), areas[k], fontproperties='SimHei', fontsize=5, color="k")
                # 添加数量级标识
                plt.text(int(4 * len(data) / 5), int((1+step*4.4) * (max + 1)), "数量级:" + orderOfMagnitude, fontproperties='SimHei', fontsize=8, color="k")
                # 添加三元组含义提示
                plt.text(int(len(data) / 50), int((1+step*4.6) * (max + 1)), "三元组含义:(Index, RT, Intensity)", fontproperties='SimHei', fontsize=6, color="k")
                # 画出平滑后的曲线
                plt.plot(x, smoothItem, color="r", linewidth=0.6)
                # 添加峰顶标记信息
                for i in range(len(peakInfo)):
                    peak = peakInfo[i]
                    index = peak[0]  # int
                    RT = peak[1]  # float
                    Intensity = peak[2]  # str
                    plt.vlines(x=x[index], ymin=-int(step * max), ymax=int((1+step*2) * max), colors="r", linewidth=0.5, linestyle="--")
                    text = "(" + str(index) + ", " + str(RT) + ", " + Intensity + ")"
                    plt.text(index-200, -int(step * (i % 4 + 1) * (max + 1)), text, fontproperties='SimHei', fontsize=5, color="k")
                # 保存图像
                plt.savefig(fname=newDirectory + "/" + Class + "_DBE" + str(DBENum) + "_C" + str(CNum), dpi=200)
                # 关闭当前图像
                plt.close()
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("plt Error : ", e)
                    traceback.print_exc()

        return ret
