# coding=utf-8
import math
import pandas as pd
import xlsxwriter
import os
from ConstValues import ConstValues


# 将excel文件读入到list中
def ReadExcelToList(filepath="", hasNan=True):
    if not hasNan:
        result = []
        result += pd.read_excel(io=filepath, header=None).values.tolist()
    else:  # 每一行的数据长度不一致，且nan在正常数据最后
        dataFrame = pd.read_excel(io=filepath, header=None)
        result = [dataFrame.values[0].tolist()]  # 处理表头
        data = dataFrame.values[1:]
        for item in data:
            # 全部是nan
            if isinstance(item[0], float) and math.isnan(item[0]):
                result.append([])
                continue
            # 后面一部分是nan
            flag = False
            for i in range(len(item)):
                if isinstance(item[i], str):
                    continue
                if math.isnan(item[i]):
                    result.append(item[:i].tolist())
                    flag = True
                    break
            # 全部不是nan
            if not flag:
                result.append(item.tolist())

    return result


# 负责将数据写入xlsx文件
def WriteDataToExcel(data, filename):
    """
    :param data: 每一行是一组数据，第一行是表头
    :return:
    """
    # 新建excel表
    workbook = xlsxwriter.Workbook(filename)
    # 创建sheet，默认名称sheet1
    worksheet = workbook.add_worksheet()
    # 数据写入excel
    for i in range(len(data)):
        worksheet.write_row("A{}".format(i + 1), data[i])
    # 将excel文件保存关闭，如果没有这一行运行代码会报错
    workbook.close()


# 负责创建文件夹，要求此文件必须和其他的py文件目录同级
def CreateDirectory(outputFilesPath="", directoryPath = "", subDirectory=""):
    if outputFilesPath == "" and directoryPath == "":
        return

    # 默认的文件输出路径
    if outputFilesPath == "":
        if not os.path.exists(directoryPath + subDirectory):
            os.makedirs(directoryPath + subDirectory)
            if ConstValues.PsIsDebug:
                print("文件夹 " + directoryPath + subDirectory + " 不存在，创建成功......")
        return directoryPath + subDirectory
    else:  # 用户选择的文件输出路径
        if not os.path.exists(outputFilesPath + subDirectory):
            os.makedirs(outputFilesPath + subDirectory)
            if ConstValues.PsIsDebug:
                print("文件夹 " + outputFilesPath + subDirectory + "不存在，创建成功......")
        return outputFilesPath + subDirectory



