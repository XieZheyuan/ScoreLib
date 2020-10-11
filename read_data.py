import pprint
import pandas
import xlrd


def get_data_from_excel(excel_path: str):
    return pandas.read_excel(excel_path).values.tolist()


def get_data_from_excel_2(excel_path: str):
    """
    https://www.cnblogs.com/tynam/p/11204895.html
    """
    data = xlrd.open_workbook(excel_path)
    table = data.sheet_by_index(0)
    l = []
    for rowNum in range(table.nrows):
        li = []
        rowVale = table.row_values(rowNum)
        for colNum in range(table.ncols):
            if rowNum > 0 and colNum == 0:

                li.append(str(rowVale[0]))
            else:

                li.append(str(rowVale[colNum]))

        l.append(li)
    return l


if __name__ == '__main__':
    pprint.pprint(get_data_from_excel("1.xlsx"))
    print(get_data_from_excel_2("1.xlsx"))


