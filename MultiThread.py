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
import sys


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
                cdb = ClassDeleteBlank(self.__parameters, self.outputFilesPath)
                deleteBlankResult, deleteBlankIsFinished = cdb.DeleteBlank()
                self.signal.emit(["ClassDeleteBlank", deleteBlankResult, deleteBlankIsFinished])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_CDB_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_CDB_MultiThread"])
        elif self.__function == "ClassGenerateDataBase":
            try:
                cgdb = ClassGenerateDataBase(self.__parameters, self.outputFilesPath)
                GDBResult, GDBIsFinished = cgdb.GenerateData()
                self.signal.emit(["ClassGenerateDataBase", GDBResult, GDBIsFinished])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_CGDB_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_CGDB_MultiThread"])
        elif self.__function == "ClassDeleteIsotope":
            try:
                cdi = ClassDeleteIsotope(self.__parameters, self.outputFilesPath)
                DelIsoResult, DelIsoIsFinished = cdi.DeleteIsotope()
                self.signal.emit(["ClassDeleteIsotope", DelIsoResult, DelIsoIsFinished])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_CDI_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_CDI_MultiThread"])
        elif self.__function == "ClassPeakDistinguish":
            try:
                cpd = ClassPeakDistinguish(self.__parameters, self.outputFilesPath)
                PeakDisResult, PeakDisIsFinished = cpd.PeakDistinguish()
                self.signal.emit(["ClassPeakDistinguish", PeakDisResult, PeakDisIsFinished])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_CPD1_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_CPD1_MultiThread"])
        elif self.__function == "ClassRemoveFalsePositive":
            try:
                crfp = ClassRemoveFalsePositive(self.__parameters, self.outputFilesPath)
                RemoveFPResult, RemoveFPIsFinished = crfp.RemoveFalsePositive()
                self.signal.emit(["ClassRemoveFalsePositive", RemoveFPResult, RemoveFPIsFinished])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_CRFP_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_CRFP_MultiThread"])
        elif self.__function == "ClassPeakDivision":
            try:
                cpd = ClassPeakDivision(self.__parameters, self.outputFilesPath)
                PeakDivResult, PeakDivIsFinished = cpd.PeakDivision()
                self.signal.emit(["ClassPeakDivision", PeakDivResult, PeakDivIsFinished])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_CPD2_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_CPD2_MultiThread"])
        elif self.__function == "ClassPlot":
            try:
                cp = ClassPlot(self.__parameters, self.outputFilesPath)
                PlotImagePath, PlotRawData = cp.Plot()
                self.signal.emit(["ClassPlot", PlotImagePath, PlotRawData])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_CPlot_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_CPlot_MultiThread"])
        elif self.__function == "ImportSampleFile":  # 读入数据显示，后台处理
            try:
                sampleFilePath = self.__parameters[0]  # 提取参数
                sampleData = np.array(pd.read_excel(sampleFilePath, header=None)).tolist()  # 弹出提示框
                self.signal.emit(["ImportSampleFile", sampleData])  # 返回结果
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_ImSample_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_ImSample_MultiThread"])
        elif self.__function == "ImportBlankFile":  # 读入数据显示，后台处理
            try:
                blankFilePath = self.__parameters[0]  # 提取参数
                blankData = np.array(pd.read_excel(blankFilePath, header=None)).tolist()  # 弹出提示框
                self.signal.emit(["ImportBlankFile", blankData])  # 返回结果
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_ImBlank_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_ImBlank_MultiThread"])
        elif self.__function == "ImportTICFile":  # 读入数据显示，后台处理
            try:
                TICFilePath = self.__parameters[0]  # 提取参数
                TICData, TICDataDictionary = self.ReadTIC(TICFilePath)  # 弹出提示框
                self.signal.emit(["ImportTICFile", TICData, TICDataDictionary])  # 返回结果
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_ImTIC_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_ImTIC_MultiThread"])
        elif self.__function == "StartMode1":
            try:
                # 提取参数
                DeleteBlankParameterList = self.__parameters[0]  # 去空白
                GDBParameterList = self.__parameters[1]  # 数据库生成
                DelIsoParameterList = self.__parameters[2]  # 搜同位素
                RemoveFPParameterList = self.__parameters[3]  # 去假阳性
                # 去空白
                cdb = ClassDeleteBlank(DeleteBlankParameterList, self.outputFilesPath)
                deleteBlankResult, deleteBlankIsFinished = cdb.DeleteBlank()
                functionStr = "去空白处理完毕！正在处理：数据库生成..."
                self.signal.emit(["deleteBlankFinished", deleteBlankResult, deleteBlankIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("扣空白完成！")
                # 数据库生成
                cgdb = ClassGenerateDataBase(GDBParameterList, self.outputFilesPath)
                GDBResult, GDBIsFinished = cgdb.GenerateData()
                functionStr = "数据库生成完毕！正在处理：搜同位素..."
                self.signal.emit(["GDBFinished", GDBResult, GDBIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("数据库生成完成！")
                # 搜同位素
                DelIsoParameterList[0] = deleteBlankResult  # 更新数据，此处注意
                DelIsoParameterList[1] = GDBResult
                cdi = ClassDeleteIsotope(DelIsoParameterList, self.outputFilesPath)
                DelIsoResult, DelIsoIsFinished = cdi.DeleteIsotope()
                functionStr = "搜同位素处理完毕！正在处理：去假阳性..."
                self.signal.emit(["DelIsoFinished", DelIsoResult, DelIsoIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("搜同位素完成！")
                # 去假阳性
                RemoveFPParameterList[0] = DelIsoResult  # 更新数据，此处注意
                # RemoveFPParameterList[1] = PeakDisResult
                crfp = ClassRemoveFalsePositive(RemoveFPParameterList, self.outputFilesPath)
                RemoveFPResult, RemoveFPIsFinished = crfp.RemoveFalsePositive()
                functionStr = "全部处理完毕！"
                self.signal.emit(["RemoveFPFinished", RemoveFPResult, RemoveFPIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("去假阳性完成！")
                # 返回结果
                self.signal.emit(["StartMode"])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_StartMode1_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_StartMode_MultiThread"])
        elif self.__function == "StartMode2":
            try:
                # 提取参数
                DeleteBlankParameterList = self.__parameters[0]  # 去空白
                GDBParameterList = self.__parameters[1]  # 数据库生成
                DelIsoParameterList = self.__parameters[2]  # 搜同位素
                PeakDisParameterList = self.__parameters[3]  # 峰提取
                RemoveFPParameterList = self.__parameters[4]  # 去假阳性
                # 去空白
                cdb = ClassDeleteBlank(DeleteBlankParameterList, self.outputFilesPath)
                deleteBlankResult, deleteBlankIsFinished = cdb.DeleteBlank()
                functionStr = "去空白处理完毕！正在处理：数据库生成..."
                self.signal.emit(["deleteBlankFinished", deleteBlankResult, deleteBlankIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("扣空白完成！")
                # 数据库生成
                cgdb = ClassGenerateDataBase(GDBParameterList, self.outputFilesPath)
                GDBResult, GDBIsFinished = cgdb.GenerateData()
                functionStr = "数据库生成完毕！正在处理：搜同位素..."
                self.signal.emit(["GDBFinished", GDBResult, GDBIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("数据库生成完成！")
                # 搜同位素
                DelIsoParameterList[0] = deleteBlankResult  # 更新数据，此处注意
                DelIsoParameterList[1] = GDBResult
                cdi = ClassDeleteIsotope(DelIsoParameterList, self.outputFilesPath)
                DelIsoResult, DelIsoIsFinished = cdi.DeleteIsotope()
                functionStr = "搜同位素处理完毕！正在处理：峰提取..."
                self.signal.emit(["DelIsoFinished", DelIsoResult, DelIsoIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("搜同位素完成！")
                # 峰提取
                PeakDisParameterList[1] = DelIsoResult  # 更新数据，此处注意
                cpd = ClassPeakDistinguish(PeakDisParameterList, self.outputFilesPath)
                PeakDisResult, PeakDisIsFinished = cpd.PeakDistinguish()
                functionStr = "峰提取处理完毕！正在处理：去假阳性..."
                self.signal.emit(["PeakDisFinished", PeakDisResult, PeakDisIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("峰提取完成！")
                # 去假阳性
                RemoveFPParameterList[0] = DelIsoResult  # 更新数据，此处注意
                RemoveFPParameterList[1] = PeakDisResult
                crfp = ClassRemoveFalsePositive(RemoveFPParameterList, self.outputFilesPath)
                RemoveFPResult, RemoveFPIsFinished = crfp.RemoveFalsePositive()
                functionStr = "全部处理完毕！"
                self.signal.emit(["RemoveFPFinished", RemoveFPResult, RemoveFPIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("去假阳性完成！")
                # 返回结果
                self.signal.emit(["StartMode"])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_StartMode2_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_StartMode_MultiThread"])
        elif self.__function == "StartMode3":
            try:
                # 提取参数
                DeleteBlankParameterList = self.__parameters[0]  # 去空白
                GDBParameterList = self.__parameters[1]  # 数据库生成
                DelIsoParameterList = self.__parameters[2]  # 搜同位素
                PeakDisParameterList = self.__parameters[3]  # 峰提取
                RemoveFPParameterList = self.__parameters[4]  # 去假阳性
                PeakDivParameterList = self.__parameters[5]  # 峰检测
                # 去空白
                cdb = ClassDeleteBlank(DeleteBlankParameterList, self.outputFilesPath)
                deleteBlankResult, deleteBlankIsFinished = cdb.DeleteBlank()
                functionStr = "去空白处理完毕！正在处理：数据库生成..."
                self.signal.emit(["deleteBlankFinished", deleteBlankResult, deleteBlankIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("扣空白完成！")
                # 数据库生成
                cgdb = ClassGenerateDataBase(GDBParameterList, self.outputFilesPath)
                GDBResult, GDBIsFinished = cgdb.GenerateData()
                functionStr = "数据库生成完毕！正在处理：搜同位素..."
                self.signal.emit(["GDBFinished", GDBResult, GDBIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("数据库生成完成！")
                # 搜同位素
                DelIsoParameterList[0] = deleteBlankResult  # 更新数据，此处注意
                DelIsoParameterList[1] = GDBResult
                cdi = ClassDeleteIsotope(DelIsoParameterList, self.outputFilesPath)
                DelIsoResult, DelIsoIsFinished = cdi.DeleteIsotope()
                functionStr = "搜同位素处理完毕！正在处理：峰提取..."
                self.signal.emit(["DelIsoFinished", DelIsoResult, DelIsoIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("搜同位素完成！")
                # 峰提取
                PeakDisParameterList[1] = DelIsoResult  # 更新数据，此处注意
                cpd = ClassPeakDistinguish(PeakDisParameterList, self.outputFilesPath)
                PeakDisResult, PeakDisIsFinished = cpd.PeakDistinguish()
                functionStr = "峰提取处理完毕！正在处理：去假阳性..."
                self.signal.emit(["PeakDisFinished", PeakDisResult, PeakDisIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("峰提取完成！")
                # 去假阳性
                RemoveFPParameterList[0] = DelIsoResult  # 更新数据，此处注意
                RemoveFPParameterList[1] = PeakDisResult
                crfp = ClassRemoveFalsePositive(RemoveFPParameterList, self.outputFilesPath)
                RemoveFPResult, RemoveFPIsFinished = crfp.RemoveFalsePositive()
                functionStr = "去假阳性处理完毕！正在处理：峰检测..."
                self.signal.emit(["RemoveFPFinished", RemoveFPResult, RemoveFPIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("去假阳性完成！")
                # 峰检测
                # PeakDisClassIsNeed = PeakDisParameterList[5]
                # if PeakDisClassIsNeed:  # 需要判断是否需要运行，此时设置的参数不起作用
                PeakDivParameterList[1] = RemoveFPResult[1]  # 更新数据，此处注意
                PeakDivParameterList[2] = PeakDisResult[2]
                cpd = ClassPeakDivision(PeakDivParameterList, self.outputFilesPath)
                PeakDivResult, PeakDivIsFinished = cpd.PeakDivision()
                functionStr = "全部处理完毕！"
                self.signal.emit(["PeakDivFinished", PeakDivResult, PeakDivIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("峰检测完成！")
                # 返回结果
                self.signal.emit(["StartMode"])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_StartMode3_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_StartMode_MultiThread"])
        elif self.__function == "StartMode4":
            try:
                # 提取参数
                GDBParameterList = self.__parameters[0]  # 数据库生成
                DelIsoParameterList = self.__parameters[1]  # 搜同位素
                RemoveFPParameterList = self.__parameters[2]  # 去假阳性
                # 数据库生成
                cgdb = ClassGenerateDataBase(GDBParameterList, self.outputFilesPath)
                GDBResult, GDBIsFinished = cgdb.GenerateData()
                functionStr = "数据库生成完毕！正在处理：搜同位素..."
                self.signal.emit(["GDBFinished", GDBResult, GDBIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("数据库生成完成！")
                # 搜同位素
                # DelIsoParameterList[0] = deleteBlankResult  # 更新数据，此处注意
                DelIsoParameterList[1] = GDBResult  # 更新数据，此处注意
                cdi = ClassDeleteIsotope(DelIsoParameterList, self.outputFilesPath)
                DelIsoResult, DelIsoIsFinished = cdi.DeleteIsotope()
                functionStr = "搜同位素处理完毕！正在处理：去假阳性..."
                self.signal.emit(["DelIsoFinished", DelIsoResult, DelIsoIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("搜同位素完成！")
                # 去假阳性
                RemoveFPParameterList[0] = DelIsoResult  # 更新数据，此处注意
                # RemoveFPParameterList[1] = PeakDisResult
                crfp = ClassRemoveFalsePositive(RemoveFPParameterList, self.outputFilesPath)
                RemoveFPResult, RemoveFPIsFinished = crfp.RemoveFalsePositive()
                functionStr = "全部处理完毕！"
                self.signal.emit(["RemoveFPFinished", RemoveFPResult, RemoveFPIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("去假阳性完成！")
                # 返回结果
                self.signal.emit(["StartMode"])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_StartMode4_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_StartMode_MultiThread"])
        elif self.__function == "StartMode5":
            try:
                # 提取参数
                GDBParameterList = self.__parameters[0]  # 数据库生成
                DelIsoParameterList = self.__parameters[1]  # 搜同位素
                PeakDisParameterList = self.__parameters[2]  # 峰提取
                RemoveFPParameterList = self.__parameters[3]  # 去假阳性
                # 数据库生成
                cgdb = ClassGenerateDataBase(GDBParameterList, self.outputFilesPath)
                GDBResult, GDBIsFinished = cgdb.GenerateData()
                functionStr = "数据库生成完毕！正在处理：搜同位素..."
                self.signal.emit(["GDBFinished", GDBResult, GDBIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("数据库生成完成！")
                # 搜同位素
                DelIsoParameterList[1] = GDBResult  # 更新数据，此处注意
                cdi = ClassDeleteIsotope(DelIsoParameterList, self.outputFilesPath)
                DelIsoResult, DelIsoIsFinished = cdi.DeleteIsotope()
                functionStr = "搜同位素处理完毕！正在处理：峰提取..."
                self.signal.emit(["DelIsoFinished", DelIsoResult, DelIsoIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("搜同位素完成！")
                # 峰提取
                PeakDisParameterList[1] = DelIsoResult  # 更新数据，此处注意
                cpd = ClassPeakDistinguish(PeakDisParameterList, self.outputFilesPath)
                PeakDisResult, PeakDisIsFinished = cpd.PeakDistinguish()
                functionStr = "峰提取处理完毕！正在处理：去假阳性..."
                self.signal.emit(["PeakDisFinished", PeakDisResult, PeakDisIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("峰提取完成！")
                # 去假阳性
                RemoveFPParameterList[0] = DelIsoResult  # 更新数据，此处注意
                RemoveFPParameterList[1] = PeakDisResult
                crfp = ClassRemoveFalsePositive(RemoveFPParameterList, self.outputFilesPath)
                RemoveFPResult, RemoveFPIsFinished = crfp.RemoveFalsePositive()
                functionStr = "全部处理完毕！"
                self.signal.emit(["RemoveFPFinished", RemoveFPResult, RemoveFPIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("去假阳性完成！")
                # 返回结果
                self.signal.emit(["StartMode"])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_StartMode5_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_StartMode_MultiThread"])
        elif self.__function == "StartMode6":
            try:
                # 提取参数
                GDBParameterList = self.__parameters[0]  # 数据库生成
                DelIsoParameterList = self.__parameters[1]  # 搜同位素
                PeakDisParameterList = self.__parameters[2]  # 峰提取
                RemoveFPParameterList = self.__parameters[3]  # 去假阳性
                PeakDivParameterList = self.__parameters[4]  # 峰检测
                # 数据库生成
                cgdb = ClassGenerateDataBase(GDBParameterList, self.outputFilesPath)
                GDBResult, GDBIsFinished = cgdb.GenerateData()
                functionStr = "数据库生成完毕！正在处理：搜同位素..."
                self.signal.emit(["GDBFinished", GDBResult, GDBIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("数据库生成完成！")
                # 搜同位素
                DelIsoParameterList[1] = GDBResult  # 更新数据，此处注意
                cdi = ClassDeleteIsotope(DelIsoParameterList, self.outputFilesPath)
                DelIsoResult, DelIsoIsFinished = cdi.DeleteIsotope()
                functionStr = "搜同位素处理完毕！正在处理：峰提取..."
                self.signal.emit(["DelIsoFinished", DelIsoResult, DelIsoIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("搜同位素完成！")
                # 峰提取
                PeakDisParameterList[1] = DelIsoResult  # 更新数据，此处注意
                cpd = ClassPeakDistinguish(PeakDisParameterList, self.outputFilesPath)
                PeakDisResult, PeakDisIsFinished = cpd.PeakDistinguish()
                functionStr = "峰提取处理完毕！正在处理：去假阳性..."
                self.signal.emit(["PeakDisFinished", PeakDisResult, PeakDisIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("峰提取完成！")
                # 去假阳性
                RemoveFPParameterList[0] = DelIsoResult  # 更新数据，此处注意
                RemoveFPParameterList[1] = PeakDisResult
                crfp = ClassRemoveFalsePositive(RemoveFPParameterList, self.outputFilesPath)
                RemoveFPResult, RemoveFPIsFinished = crfp.RemoveFalsePositive()
                functionStr = "去假阳性处理完毕！正在处理：峰检测..."
                self.signal.emit(["RemoveFPFinished", RemoveFPResult, RemoveFPIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("去假阳性完成！")
                # 峰检测
                # PeakDisClassIsNeed = PeakDisParameterList[5]
                # if PeakDisClassIsNeed:  # 需要判断是否需要运行，此时设置的参数不起作用
                PeakDivParameterList[1] = RemoveFPResult[1]  # 更新数据，此处注意
                PeakDivParameterList[2] = PeakDisResult[2]
                cpd = ClassPeakDivision(PeakDivParameterList, self.outputFilesPath)
                PeakDivResult, PeakDivIsFinished = cpd.PeakDivision()
                functionStr = "全部处理完毕！"
                self.signal.emit(["PeakDivFinished", PeakDivResult, PeakDivIsFinished, functionStr])
                if ConstValues.PsIsDebug:
                    print("峰检测完成！")
                # 返回结果
                self.signal.emit(["StartMode"])
            except Exception as e:
                if ConstValues.PsIsDebug:
                    print("Error_StartMode6_MultiThread : ", e)
                    traceback.print_exc()
                self.signal.emit(["Error_StartMode_MultiThread"])
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
            print(
                "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                sys._getframe().f_code.co_name, "\" method***：",
                "扫描点的个数 len(resDictionary):", len(resDictionary)
            )
        endTime = time.time()
        if ConstValues.PsIsDebug:
            print(
                "***Debug In \"", self.__class__.__name__, "\" class，In \"",
                sys._getframe().f_code.co_name, "\" method***：",
                "读入和处理文件费时: ", endTime - startTime, " s"
            )
        return resList, resDictionary


