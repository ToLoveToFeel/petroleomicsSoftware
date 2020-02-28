# coding=utf-8
import time
from PyQt5.QtCore import *
from ClassDeleteBlank import ClassDeleteBlank
from ClassGenerateDataBase import ClassGenerateDataBase
from ClassDeleteIsotope import ClassDeleteIsotope
from ClassPeakDistinguish import ClassPeakDistinguish
from ClassRemoveFalsePositive import ClassRemoveFalsePositive
from ClassPeakDivision import ClassPeakDivision
from ConstValues import ConstValues


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
                    print("ClassDeleteBlank Error : ", e)
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
                    print("ClassGenerateDataBase Error : ", e)
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
                    print("ClassDeleteIsotope Error : ", e)
                self.signal.emit(["ClassDeleteIsotope Error"])
        elif self.__function == "ClassPeakDistinguish":
            try:
                retList = ["ClassPeakDistinguish"]
                cpd = ClassPeakDistinguish(self.__parameters, self.outputFilesPath)
                # cpd.PeakDisPlotPeak()
                PeakDisIsFinished, PeakDisResult = cpd.PeakDistinguish()
                retList.append(PeakDisResult)
                retList.append(PeakDisIsFinished)
                self.signal.emit(retList)
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("ClassPeakDistinguish Error : ", e)
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
                    print("ClassRemoveFalsePositive Error : ", e)
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
                    print("ClassPeakDivision Error : ", e)
                self.signal.emit(["ClassPeakDivision Error"])
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
                PeakDisResult, PeakDisIsFinished = cpd.PeakDistinguish()
                retList.append(PeakDisResult)
                retList.append(PeakDisIsFinished)
                self.signal.emit(["PeakDisFinished"])
                if ConstValues.PsIsDebug:
                    print("峰识别完成！")
                # 去假阳性
                RemoveFPParameterList[0] = DelIsoResult  # 更新数据，此处注意
                RemoveFPParameterList[1] = PeakDisResult
                crfp = ClassRemoveFalsePositive(RemoveFPParameterList, self.outputFilesPath)
                RemoveFPIsFinished, RemoveFPResult = crfp.RemoveFalsePositive()
                retList.append(RemoveFPResult)
                retList.append(RemoveFPIsFinished)
                self.signal.emit(["RemoveFPFinished"])
                if ConstValues.PsIsDebug:
                    print("去假阳性完成！")
                # 峰检测
                PeakDisClassIsNeed = PeakDisParameterList[5]
                if PeakDisClassIsNeed:  # 需要判断是否需要运行
                    PeakDivParameterList[1] = RemoveFPResult[1]  # 更新数据，此处注意
                    cpd = ClassPeakDivision(self.__parameters, self.outputFilesPath)
                    PeakDivResult, PeakDivIsFinished = cpd.PeakDivision()
                    retList.append(PeakDivResult)
                    retList.append(PeakDivIsFinished)
                    self.signal.emit(["PeakDivFinished"])
                    if ConstValues.PsIsDebug:
                        print("峰检测完成！")
                # 返回结果
                self.signal.emit(retList)
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("StartAll Error : ", e)
                self.signal.emit(["StartAll Error"])

        endTime = time.time()
        if ConstValues.PsIsDebug:
            if endTime - startTime > 60:
                print("程序运行总用时：", (endTime - startTime) / 60, " min.")
            else:
                print("程序运行总用时：", endTime - startTime, " s.")



