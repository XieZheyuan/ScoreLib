import numpy as np

items = ["标准差", "方差", "平均数", "中位数", "众数", "极差"]


def n(a):
    return round(float(a), 5)


def count_std(a: list):
    # 标准差
    np_a = np.std(a, ddof=1)
    return n(np_a)


def count_var(a: list):
    # 方差
    np_a = np.var(a)
    return n(np_a)


def count_average(a: list):
    # 平均数
    return n(np.average(a))


def count_median(a: list):
    # 中位数
    return n(np.median(a))


def count_mode(a: list):
    # 众数(https://blog.csdn.net/qiubingcsdn/article/details/82631411)
    return n(sorted(a)[len(a) // 2])


def count_range(a: list):
    # 极差
    return n(max(a) - min(a))


item_dict = {
    "标准差": count_std,
    "方差": count_var,
    "平均数": count_average,
    "中位数": count_median,
    "众数": count_mode,
    "极差": count_range
}