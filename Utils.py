# coding=utf-8
import math
import pandas as pd
import xlsxwriter


# 将excel文件读入到list中
def ReadExcelToList(filepath="", hasNan=True):
    if not hasNan:
        result = []
        result += pd.read_excel(io=filepath, header=None).values.tolist()
    else:  # 每一行的数据长度不一致，且nan在正常数据最后
        dataFrame = pd.read_excel(io=filepath, header=None)
        result = [dataFrame.values[0].tolist()]
        data = dataFrame.values[1:]
        for item in data:
            # 全部是nan
            if math.isnan(item[0]):
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


