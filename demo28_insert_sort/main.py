#!/usr/bin/python3

# 插入排序
#
# 输入: n个数的一个序列
# 输出: 输出一个有序序列

def insertSort(A):
    i = 0
    end = len(A)
    while i < end:
        print(f"{A[i]}", end=' ')
        i += 1
    if len(A) > 0:
        print('')


A = [1, 2, 3, 4, 5]

insertSort(A)
