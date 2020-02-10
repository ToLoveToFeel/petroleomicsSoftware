# coding=utf-8
# 此文件负责定义：扣同位素
import numpy as np
import pandas as pd
import xlsxwriter
from ConstValues import ConstValues


class ClassDeleteIsotope():
    def __init__(self, parameterList):
        assert len(parameterList) == 7, "ClassDeleteIsotope参数不对"
        self.deleteBlankResult = parameterList[0]  # 删空白的结果（格式：list二维数组，有表头）
        self.GDBResult = parameterList[1]  # 数据库生成的结果（格式：list二维数组，有表头）
        self.DelIsoIntensityX = parameterList[2]  # 格式：整数
        self.DelIso_13C2RelativeIntensity = parameterList[3]  # 格式：整数
        self.DelIsoMassDeviation = parameterList[4]  # 格式：浮点数
        self.DelIsoIsotopeMassDeviation = parameterList[5]  # 格式：浮点数
        self.DelIsoIsotopeIntensityDeviation = parameterList[6]  # 格式：整数

    # 负责扣同位素
    def DeleteIsotope(self):
        result = []
        header = ["SampleMass", "SampleIntensity", "DBMass", "DBIntensity"]
        result.append(header)
        for sampleItem in self.deleteBlankResult[1:]:
            # 跳过表头，其余sampleItem均为列表，列表：[Mass, Intensity]，都是浮点数
            self.HandleItem(sampleItem)

    # 负责判断某个样本是否能匹配成功 数据库
    def HandleItem(self, sampleItem):
        sampleItemMass = sampleItem[0]
        sampleItemIntensity = sampleItem[1]
        for DBItem in self.GDBResult[1:]:
            # 跳过表头，其余DatabaseItem均为列表，列表：["Class", "Neutral DBE", "Formula", "Calc m/z", "C", "ion"]
            # [str, int, str, float, int, str]
            DBItemClass = DBItem[0]  # 类型
            DBItemNDBE = DBItem[1]  # 不饱和度
            DBItemFormula = DBItem[2]  # 分子式
            DBItemM_Z = DBItem[3]  # 质荷比
            DBItemCNumber = DBItem[4]  # 碳数目


    # 负责将数据写入xlsx文件
    def WriteDataToExcel(self, data, filename):
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

