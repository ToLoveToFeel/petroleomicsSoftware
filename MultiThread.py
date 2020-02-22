# coding=utf-8
import time
from PyQt5.QtCore import *
from ClassDeleteBlank import ClassDeleteBlank
from ClassGenerateDataBase import ClassGenerateDataBase
from ClassDeleteIsotope import ClassDeleteIsotope
from ClassPeakDistinguish import ClassPeakDistinguish
from ClassRemoveFalsePositive import ClassRemoveFalsePositive
from ConstValues import ConstValues


class MultiThread(QThread):
    signal = pyqtSignal(list)

    def __init__(self, function=None, parameters=None, outputFilesPath=""):
        super(MultiThread, self).__init__()
        self.__function = function
        self.__parameters = parameters
        self.outputFilesPath = outputFilesPath

    def run(self):
        startTime = time.time()

        if self.__function == "ClassDeleteBlank":
            retList = ["ClassDeleteBlank"]
            cdb = ClassDeleteBlank(self.__parameters, self.outputFilesPath)
            deleteBlankResult, deleteBlankIsFinished = cdb.DeleteBlank()
            retList.append(deleteBlankResult)
            retList.append(deleteBlankIsFinished)
            self.signal.emit(retList)
        elif self.__function == "ClassGenerateDataBase":
            retList = ["ClassGenerateDataBase"]
            cgdb = ClassGenerateDataBase(self.__parameters, self.outputFilesPath)
            GDBResult, GDBIsFinished = cgdb.GenerateData()
            retList.append(GDBResult)
            retList.append(GDBIsFinished)
            self.signal.emit(retList)
        elif self.__function == "ClassDeleteIsotope":
            retList = ["ClassDeleteIsotope"]
            cdi = ClassDeleteIsotope(self.__parameters, self.outputFilesPath)
            DelIsoResult, DelIsoIsFinished = cdi.DeleteIsotope()
            retList.append(DelIsoResult)
            retList.append(DelIsoIsFinished)
            self.signal.emit(retList)
        elif self.__function == "ClassPeakDistinguish":
            retList = ["ClassPeakDistinguish"]
            cpd = ClassPeakDistinguish(self.__parameters, self.outputFilesPath)
            # cpd.PeakDisPlotPeak()
            PeakDisIsFinished, PeakDisResult = cpd.PeakDistinguish()
            retList.append(PeakDisResult)
            retList.append(PeakDisIsFinished)
            self.signal.emit(retList)
        elif self.__function == "ClassRemoveFalsePositive":
            retList = ["ClassRemoveFalsePositive"]
            crfp = ClassRemoveFalsePositive(self.__parameters, self.outputFilesPath)
            # cpd.PeakDisPlotPeak()
            RemoveFPIsFinished, RemoveFPResult = crfp.RemoveFalsePositive()
            retList.append(RemoveFPResult)
            retList.append(RemoveFPIsFinished)
            self.signal.emit(retList)
        elif self.__function == "StartAll":
            retList = ["StartAll"]
            # 提取参数
            DeleteBlankParameterList = self.__parameters[0]  # 去空白
            GDBParameterList = self.__parameters[1]  # 数据库生成
            DelIsoParameterList = self.__parameters[2]  # 扣同位素
            PeakDisParameterList = self.__parameters[3]  # 峰识别
            # 去空白
            cdb = ClassDeleteBlank(DeleteBlankParameterList, self.outputFilesPath)
            deleteBlankResult, deleteBlankIsFinished = cdb.DeleteBlank()
            retList.append(deleteBlankResult)
            retList.append(deleteBlankIsFinished)
            self.signal.emit(["deleteBlankFinished"])
            if ConstValues.PsIsDebug:
                print("扣空白完成！")
            # 数据库生成
            cgdb = ClassGenerateDataBase(GDBParameterList, self.outputFilesPath)
            GDBResult, GDBIsFinished = cgdb.GenerateData()
            retList.append(GDBResult)
            retList.append(GDBIsFinished)
            self.signal.emit(["GDBFinished"])
            if ConstValues.PsIsDebug:
                print("数据库生成完成！")
            # 扣同位素
            DelIsoParameterList[0] = deleteBlankResult  # 更新数据，此处注意
            DelIsoParameterList[1] = GDBResult
            cdi = ClassDeleteIsotope(DelIsoParameterList, self.outputFilesPath)
            DelIsoResult, DelIsoIsFinished = cdi.DeleteIsotope()
            retList.append(DelIsoResult)
            retList.append(DelIsoIsFinished)
            self.signal.emit(["DelIsoFinished"])
            if ConstValues.PsIsDebug:
                print("扣同位素完成！")
            # 峰识别
            PeakDisParameterList[1] = DelIsoResult  # 更新数据，此处注意
            cpd = ClassPeakDistinguish(PeakDisParameterList, self.outputFilesPath)
            PeakDisIsFinished, PeakDisResult = cpd.PeakDistinguish()
            retList.append(PeakDisResult)
            retList.append(PeakDisIsFinished)
            self.signal.emit(["PeakDisFinished"])
            if ConstValues.PsIsDebug:
                print("峰识别完成！")
            # 返回结果
            self.signal.emit(retList)

        endTime = time.time()
        if ConstValues.PsIsDebug:
            if endTime - startTime > 60:
                print("程序运行总用时：", (endTime - startTime) / 60, " min.")
            else:
                print("程序运行总用时：", endTime - startTime, " s.")
