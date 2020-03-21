# coding=utf-8
import time
from PyQt5.QtCore import *
from ClassDeleteBlank import ClassDeleteBlank
from ClassGenerateDataBase import ClassGenerateDataBase
from ClassDeleteIsotope import ClassDeleteIsotope
from ClassPeakDistinguish import ClassPeakDistinguish
from ClassRemoveFalsePositive import ClassRemoveFalsePositive
from ClassPeakDivision import ClassPeakDivision
from ClassPlot import ClassPlot
from ConstValues import ConstValues
from PromptBox import PromptBox
import numpy as np
import pandas as pd
import traceback


class MultiThread(QThread):
    signal = pyqtSignal(list)

    def __init__(self, function=None, parameters=None, outputFilesPath=""):
        super(MultiThread, self).__init__()
        self.__function = function  # 指定运行的功能
        self.__parameters = parameters  # 运行需要的参数
        self.outputFilesPath = outputFilesPath  # 文件输出的路径

    def run(self):
        startTime = time.time()

        if self.__function == "ClassDeleteBlank":
            try:
                retList = ["ClassDeleteBlank"]
                cdb = ClassDeleteBlank(self.__parameters, self.outputFilesPath)
                deleteBlankResult, deleteBlankIsFinished = cdb.DeleteBlank()
                retList.append(deleteBlankResult)
                retList.append(deleteBlankIsFinished)
                self.signal.emit(retList)
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("MultiThread ClassDeleteBlank Error : ", e)
                self.signal.emit(["ClassDeleteBlank Error"])
        elif self.__function == "ClassGenerateDataBase":
            try:
                retList = ["ClassGenerateDataBase"]
                cgdb = ClassGenerateDataBase(self.__parameters, self.outputFilesPath)
                GDBResult, GDBIsFinished = cgdb.GenerateData()
                retList.append(GDBResult)
                retList.append(GDBIsFinished)
                self.signal.emit(retList)
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("MultiThread ClassGenerateDataBase Error : ", e)
                self.signal.emit(["ClassGenerateDataBase Error"])
        elif self.__function == "ClassDeleteIsotope":
            try:
                retList = ["ClassDeleteIsotope"]
                cdi = ClassDeleteIsotope(self.__parameters, self.outputFilesPath)
                DelIsoResult, DelIsoIsFinished = cdi.DeleteIsotope()
                retList.append(DelIsoResult)
                retList.append(DelIsoIsFinished)
                self.signal.emit(retList)
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("MultiThread ClassDeleteIsotope Error : ", e)
                self.signal.emit(["ClassDeleteIsotope Error"])
        elif self.__function == "ClassPeakDistinguish":
            try:
                retList = ["ClassPeakDistinguish"]
                cpd = ClassPeakDistinguish(self.__parameters, self.outputFilesPath)
                # cpd.PeakDisPlotPeak()
                PeakDisResult, PeakDisIsFinished = cpd.PeakDistinguish()
                time.sleep(5)  # 认为睡眠20s
                retList.append(PeakDisResult)
                retList.append(PeakDisIsFinished)
                self.signal.emit(retList)
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("MultiThread ClassPeakDistinguish Error : ", e)
                self.signal.emit(["ClassPeakDistinguish Error"])
        elif self.__function == "ClassRemoveFalsePositive":
            try:
                retList = ["ClassRemoveFalsePositive"]
                crfp = ClassRemoveFalsePositive(self.__parameters, self.outputFilesPath)
                RemoveFPResult, RemoveFPIsFinished = crfp.RemoveFalsePositive()
                retList.append(RemoveFPResult)
                retList.append(RemoveFPIsFinished)
                self.signal.emit(retList)
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("MultiThread ClassRemoveFalsePositive Error : ", e)
                self.signal.emit(["ClassRemoveFalsePositive Error"])
        elif self.__function == "ClassPeakDivision":
            try:
                retList = ["ClassPeakDivision"]
                cpd = ClassPeakDivision(self.__parameters, self.outputFilesPath)
                PeakDivResult, PeakDivIsFinished = cpd.PeakDivision()
                retList.append(PeakDivResult)
                retList.append(PeakDivIsFinished)
                self.signal.emit(retList)
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("MultiThread ClassPeakDivision Error : ", e)
                self.signal.emit(["ClassPeakDivision Error"])
        elif self.__function == "ClassPlot":
            try:
                retList = ["ClassPlot"]
                cp = ClassPlot(self.__parameters, self.outputFilesPath)
                PlotImagePath, PlotRawData = cp.Plot()
                retList.append(PlotImagePath)
                retList.append(PlotRawData)
                self.signal.emit(retList)
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("MultiThread ClassPlot Error : ", e)
                    traceback.print_exc()
                # self.signal.emit(["Plot Error"])
        elif self.__function == "StartAll":
            try:
                retList = ["StartAll"]
                # 提取参数
                DeleteBlankParameterList = self.__parameters[0]  # 去空白
                GDBParameterList = self.__parameters[1]  # 数据库生成
                DelIsoParameterList = self.__parameters[2]  # 扣同位素
                PeakDisParameterList = self.__parameters[3]  # 峰识别
                RemoveFPParameterList = self.__parameters[4]  # 去假阳性
                PeakDivParameterList = self.__parameters[5]  # 峰检测
                # 去空白
                cdb = ClassDeleteBlank(DeleteBlankParameterList, self.outputFilesPath)
                deleteBlankResult, deleteBlankIsFinished = cdb.DeleteBlank()
                self.signal.emit(["deleteBlankFinished", deleteBlankResult, deleteBlankIsFinished])
                if ConstValues.PsIsDebug:
                    print("扣空白完成！")
                # 数据库生成
                cgdb = ClassGenerateDataBase(GDBParameterList, self.outputFilesPath)
                GDBResult, GDBIsFinished = cgdb.GenerateData()
                self.signal.emit(["GDBFinished", GDBResult, GDBIsFinished])
                if ConstValues.PsIsDebug:
                    print("数据库生成完成！")
                # 扣同位素
                DelIsoParameterList[0] = deleteBlankResult  # 更新数据，此处注意
                DelIsoParameterList[1] = GDBResult
                cdi = ClassDeleteIsotope(DelIsoParameterList, self.outputFilesPath)
                DelIsoResult, DelIsoIsFinished = cdi.DeleteIsotope()
                self.signal.emit(["DelIsoFinished", DelIsoResult, DelIsoIsFinished])
                if ConstValues.PsIsDebug:
                    print("扣同位素完成！")
                # 峰识别
                PeakDisParameterList[1] = DelIsoResult  # 更新数据，此处注意
                cpd = ClassPeakDistinguish(PeakDisParameterList, self.outputFilesPath)
                PeakDisResult, PeakDisIsFinished = cpd.PeakDistinguish()
                self.signal.emit(["PeakDisFinished", PeakDisResult, PeakDisIsFinished])
                if ConstValues.PsIsDebug:
                    print("峰识别完成！")
                # 去假阳性
                RemoveFPParameterList[0] = DelIsoResult  # 更新数据，此处注意
                RemoveFPParameterList[1] = PeakDisResult
                crfp = ClassRemoveFalsePositive(RemoveFPParameterList, self.outputFilesPath)
                RemoveFPResult, RemoveFPIsFinished = crfp.RemoveFalsePositive()
                retList.append(RemoveFPResult)
                retList.append(RemoveFPIsFinished)
                self.signal.emit(["RemoveFPFinished", RemoveFPResult, RemoveFPIsFinished])
                if ConstValues.PsIsDebug:
                    print("去假阳性完成！")
                # 峰检测
                PeakDisClassIsNeed = PeakDisParameterList[5]
                if PeakDisClassIsNeed:  # 需要判断是否需要运行
                    PeakDivParameterList[1] = RemoveFPResult[1]  # 更新数据，此处注意
                    PeakDivParameterList[2] = PeakDisResult[2]
                    cpd = ClassPeakDivision(PeakDivParameterList, self.outputFilesPath)
                    PeakDivResult, PeakDivIsFinished = cpd.PeakDivision()
                    self.signal.emit(["PeakDivFinished", PeakDivResult, PeakDivIsFinished])
                    if ConstValues.PsIsDebug:
                        print("峰检测完成！")
                # 返回结果
                self.signal.emit(retList)
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("MultiThread StartAll Error : ", e)
                self.signal.emit(["StartAll Error"])
        elif self.__function == "ImportSampleFile":  # 读入数据显示，后台处理
            try:
                retList = ["ImportSampleFile"]
                # 提取参数
                sampleFilePath = self.__parameters[0]
                # 弹出提示框
                sampleData = np.array(pd.read_excel(sampleFilePath, header=None)).tolist()
                # 返回结果
                retList.append(sampleData)
                self.signal.emit(retList)
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("MultiThread ImportSampleFile : ", e)
                # self.signal.emit(["ImportSampleFile"])
        elif self.__function == "ImportBlankFile":  # 读入数据显示，后台处理
            try:
                retList = ["ImportBlankFile"]
                # 提取参数
                blankFilePath = self.__parameters[0]
                # 弹出提示框
                blankData = np.array(pd.read_excel(blankFilePath, header=None)).tolist()
                # 返回结果
                retList.append(blankData)
                self.signal.emit(retList)
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("MultiThread ImportBlankFile : ", e)
                # self.signal.emit(["ImportBlankFile"])
        elif self.__function == "ImportTICFile":  # 读入数据显示，后台处理
            try:
                retList = ["ImportTICFile"]
                # 提取参数
                TICFilePath = self.__parameters[0]
                # 弹出提示框
                TICData, TICDataDictionary = self.ReadTIC(TICFilePath)
                # 返回结果
                retList.append(TICData)
                retList.append(TICDataDictionary)
                self.signal.emit(retList)
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("MultiThread ImportTICFile : ", e)
        endTime = time.time()
        if ConstValues.PsIsDebug:
            if endTime - startTime > 60:
                print("程序运行总用时：", (endTime - startTime) / 60, " min.")
            else:
                print("程序运行总用时：", endTime - startTime, " s.")

    # 负责读取总离子流图文件(txt)
    def ReadTIC(self, TICFilePath):
        """
        文件格式必须为：每行三个数据，一个表头，数据之间用制表符(\t)分割，无其他无关字符
        :return:返回结果为字典：{key:value,...,key:value}，value为二维列表[[Mass, Intensity],...,[Mass, Intensity]]
        """
        startTime = time.time()
        # 读取数据，数据分割
        f = open(TICFilePath, "r")
        content = f.read().strip().replace("\n", "\t").replace(" ", "").split("\t")
        # 去除表头
        header = content[:3]
        content = content[3:]
        if len(content) / 3 != int(len(content) / 3):
            # raise Exception("Error in ClassPeakDistinguish ReadTIC.")
            PromptBox().warningMessage("总离子流图文件(txt)存在问题，请重新选择！")
            return None, None
        # str全部转为float
        content = [float(item) for item in content]
        # 返回结果，二维字典
        resList = [header]
        # 返回结果为字典：{key:value}，value为二维列表[[Mass, Intensity],...,[Mass, Intensity]]
        resDictionary = {}

        key = content[0]
        value = []
        for i in range(int(len(content) / 3)):
            resList.append(content[(i * 3): (i * 3 + 3)])
            if content[i * 3] != key:
                resDictionary[key] = value  # 字典中添加元素（二维列表）
                key = content[i * 3]
                value = []
            value.append([content[i * 3 + 1], content[i * 3 + 2]])

        if ConstValues.PsIsDebug:
            print("扫描点的个数： ", len(resDictionary))
        endTime = time.time()
        if ConstValues.PsIsDebug:
            print("读入和处理文件费时： ", endTime - startTime, " s")
        return resList, resDictionary


