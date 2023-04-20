import time
from random import random

import numpy as np


class concept:
    def __init__(self, x, a, b, c):
        self.X = x
        self.A = a
        self.B = b
        self.C = c

    def get_mx(self, m):
        V = []
        for i in range(m):
            V.append(chr(i + 97))
        # alpha = intersection( union(self.A, self.B), self.C )
        beta = subtract(subtract(V, self.A), self.B)
        gamma = subtract(union(self.A, self.B), self.C)
        return (len(beta) + 0.5 * len(gamma)) / len(V)


#  并集
def union(a, b):
    len_1 = len(a)
    len_2 = len(b)
    res = []
    i = 0
    j = 0
    while i < len_1 and j < len_2:
        if a[i] < b[j]:
            res.append(a[i])
            i += 1
        elif a[i] > b[j]:
            res.append(b[j])
            j += 1
        else:
            res.append(a[i])
            i += 1
            j += 1
    while i < len_1:
        res.append(a[i])
        i += 1
    while j < len_2:
        res.append(b[j])
        j += 1
    return res


#  交集
def intersection(a, b):
    len_1 = len(a)
    len_2 = len(b)
    res: list = []
    i = 0
    j = 0
    while i < len_1 and j < len_2:
        if a[i] == b[j]:
            res.append(a[i])
            i += 1
            j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    return res


#  减法
def subtract(a, b):
    len_1 = len(a)
    len_2 = len(b)
    res: list = []
    i = 0
    j = 0
    while i < len_1 and j < len_2:
        if a[i] < b[j]:
            res.append(a[i])
            i += 1
        elif a[i] > b[j]:
            j += 1
        else:
            i += 1
            j += 1
    if j == len_2:
        while i < len_1:
            res.append(a[i])
            i += 1
    return res


#  判断序列是否存在交集
def judge_intersection(a, b):
    len_1 = len(a)
    len_2 = len(b)
    i = 0
    j = 0
    while i < len_1 and j < len_2:
        if a[i] == b[j]:
            return True
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    return False


#  更新概念的对象
def update_concept(cpt: concept, b: list) -> concept:
    cpt.X = b
    return cpt


#  合并概念
def combine_concept(a: concept, b: concept) -> concept:
    return concept(union(a.X, b.X), intersection(a.A, b.A), intersection(a.B, b.B), intersection(a.C, b.C))


#  判断当前结果中是否缺少顶部概念   缺少 ： true， 不缺少 ： false
def is_top_concept(all_cpt, n, e):
    size = len(all_cpt)
    s = []
    for i in range(n):
        s.append(i + 1 + e)
    for i in range(size):
        if all_cpt[i].X == s:
            return False
    return True


#  输出一个概念
def out_one_concept(cpt: concept):
    x_size = len(cpt.X)
    a_size = len(cpt.A)
    b_size = len(cpt.B)
    c_size = len(cpt.C)
    print("( ", end="")
    #  X
    if x_size == 0:
        print("'φ'", end=" ")
    else:
        for j in range(x_size):
            print(cpt.X[j], end=" ")
    print(",  ( ", end="")
    #  A
    if a_size == 0:
        print("'φ'", end=" ")
    else:
        for j in range(a_size):
            print(cpt.A[j], end=" ")
    print(", ", end="")
    #  B
    if b_size == 0:
        print("'φ'", end=" ")
    else:
        for j in range(b_size):
            print(cpt.B[j], end=" ")
    print(", ", end="")
    #  C
    if c_size == 0:
        print("'φ'", end=" ")
    else:
        for j in range(c_size):
            print(cpt.C[j], end=" ")
    print(") )")


#  输出一个序列中的所有概念
def out_concept_in_list(cpt: list):
    list_size = len(cpt)
    for i in range(list_size):
        out_one_concept(cpt[i])
    print()


#  创建二维数组
def get_two_dimensional_array(n, m):
    a = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            rand = random()
            if 0 < rand < 0.8:
                a[i][j] += 1
            elif 0.9 <= rand < 1:
                a[i][j] -= 1
    return a


#  以显眼的方式输出二维数组
def out_two_dimensional_array(a):
    n = len(a)
    m = len(a[0])
    for i in range(n):
        print(" |-->     ", end="")
        for j in range(m):
            print(a[i][j], end="  ")
        print()
    print()


#  获取基础概念
def get_base_concept(a, n: int, m: int, e):
    base_cpt = []
    for i in range(n):
        cpt = concept([], [], [], [])
        cpt.X.append(i + 1 + e)
        for j in range(m):
            temp = a[i][j]
            if temp == 1 or temp == 0:
                cpt.A.append(chr(j + 97))
            if temp == -1 or temp == 0:
                cpt.B.append(chr(j + 97))
            if temp == 1 or temp == -1:
                cpt.C.append(chr(j + 97))
        base_cpt.append(cpt)
    return base_cpt


#  获取所有概念
def get_all_concept(base_cpt):
    num_of_basecpt = len(base_cpt)
    if num_of_basecpt == 1:
        return base_cpt

    #  使用两个数组交替存放结果
    all_cpt: list = [[] for _ in range(2)]
    while True:
        temp_1: list = []
        temp_2: list = []
        all_cpt.append(temp_1)
        all_cpt.append(temp_2)
        break

    # 首先插入底部的（phi，（all, all, all））元素和第一个元素
    bottom_cpt = concept([], [], [], [])
    for i in range(num_of_basecpt):
        bottom_cpt.A = union(bottom_cpt.A, base_cpt[i].A)
        bottom_cpt.B = union(bottom_cpt.B, base_cpt[i].B)
        bottom_cpt.C = union(bottom_cpt.C, base_cpt[i].C)
    all_cpt[0].append(bottom_cpt)
    all_cpt[0].append(base_cpt[0])

    #  使用两个vector数组交替存放结果, 每次循环后 交换两个数组的作用
    #  使用L、R 表示两个数组，每次循环后交换位置
    #  *首次循环时，所有概念存放在0中，循环结束后结果存放在1中
    #  *在程序循环中，始终操作/计算R中的概念，将结果存放在L中
    turn: bool = True
    for i in range(1, num_of_basecpt):
        R: int
        L: int

        if turn:
            R = 0
            L = 1
            turn = False
        else:
            R = 1
            L = 0
            turn = True

        #  当前需要插入的概念
        insert_cpt = base_cpt[i]

        #  遍历所有概念 （R）
        size_of_R = len(all_cpt[R])
        for j in range(size_of_R):
            #  当前正在访问的概念
            cpt = all_cpt[R][j]
            #  判断属性是否存在交集
            if judge_intersection(insert_cpt.A, cpt.A) or judge_intersection(insert_cpt.B, cpt.B) \
                    or judge_intersection(insert_cpt.C, cpt.C):
                #  存在交集，将两者合并得到新概念
                new_cpt = combine_concept(cpt, insert_cpt)
                #  遍历已生成的所有概念，判断是否存在一个概念，其内涵等于Ncpt的内涵    有 ：True  没有 ： False
                flg: bool = False
                sizeof_L = len(all_cpt[L])
                for k in range(sizeof_L):
                    if new_cpt.A == all_cpt[L][k].A and new_cpt.B == all_cpt[L][k].B \
                            and new_cpt.C == all_cpt[L][k].C:
                        #  若有，更新这个概念
                        if all_cpt[L][k].X != new_cpt.X:
                            all_cpt[L][k] = update_concept(all_cpt[L][k], union(all_cpt[L][k].X, new_cpt.X))
                        #  保存当前访问的概念
                        if all_cpt[L][k].A != cpt.A or all_cpt[L][k].B != cpt.B or all_cpt[L][k].C != cpt.C:
                            all_cpt[L].append(cpt)
                        flg = True
                        break
                # end for
                #  若没有，插入合并后的概念
                if not flg:
                    all_cpt[L].append(new_cpt)
                    #  保存当前访问的概念
                    if new_cpt.A != cpt.A or new_cpt.B != cpt.B or new_cpt.C != cpt.C:
                        all_cpt[L].append(cpt)
            else:
                #  不存在交集
                all_cpt[L].append(cpt)
        #  本次循环结束，清空R，用于下次存放结果
        all_cpt[R].clear()
    # end for

    #  总循环结束，检查结果
    if not all_cpt[0]:
        return all_cpt[1]
    else:
        return all_cpt[0]


#  获取顶部概念
def get_top_concept(n, e):
    cpt = concept([], [], [], [])
    for i in range(n):
        cpt.X.append(i + 1 + e)
    return cpt


#  a: list of concept    b: object
def contain_object(a: list, b: list, m) -> concept:
    size_a = len(a)
    res = []
    for i in range(size_a):
        # a[i] -> concept    b -> object
        len_1 = len(a[i].X)
        len_2 = len(b)
        if len_1 < len_2:
            continue
        j = 0
        k = 0
        while j < len_1 and k < len_2:
            if a[i].X[j] == b[k]:
                j += 1
                k += 1
            elif a[i].X[j] < b[k]:
                j += 1
            else:
                break
        if k == len_2:
            res.append(a[i])
    size_b = len(b)
    size_res = len(res)
    flg = 1

    while flg < m:
        for i in range(size_res):
            if len(res[i].X) == size_b + flg:
                return res[i]
        flg += 1
    return concept([], [], [], [])


def random_object(n, count) -> list:
    res = []
    while len(res) < count:
        a = []
        for j in range(n):
            if random() < 0.4:
                a.append(j + 1)
        if len(a) == 5:
            res.append(a)
    return res


def main():
    N = 14
    M = 11

    #  获取二维数组
    # a = get_two_dimensional_array(N, M)

    #   8  1  1
    # a = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [1, 1, 1, 1, 1, 0, 1, 1, -1, 1], [1, 0, -1, 1, 0, 1, 1, 1, 1, 0],
    #      [1, 1, 1, 1, 0, 1, 1, 0, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, -1, 1], [1, 1, 1, 0, 1, 0, 1, 1, -1, 1],
    #      [1, -1, 1, 1, 1, 1, -1, 1, 1, 1], [-1, 1, 1, 0, -1, 1, -1, 1, 1, 1], [1, 1, 1, -1, 1, 1, 1, 1, 1, 1],
    #      [1, 0, 1, 1, 1, -1, 0, -1, 1, 1], [1, -1, 1, 1, 1, 1, 1, 0, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #      [1, 1, 1, 1, 1, 1, 1, -1, 1, -1], [-1, 1, 1, 1, 1, -1, 1, 1, 0, 1], [1, -1, 1, 1, 1, 1, 1, 1, 1, 0],
    #      [1, 1, 1, 0, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 0, -1, 1, 1, 0, 1], [1, 1, 1, 1, 1, -1, 1, 1, 1, 1],
    #      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 0, 1, 1, 0, -1, 1, 1, 1]]

    #   3  1  1
    # a = [[-1, 1, 0, 1, 1, 1, 1, -1, 1, 0], [-1, -1, 0, 1, 1, 0, 1, 1, -1, 1], [-1, 1, 0, 0, 1, 0, 0, 1, 1, 1],
    #      [1, -1, -1, -1, 1, 1, 1, 0, -1, -1], [1, 1, 0, 1, -1, 1, 1, 0, 1, 0], [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #      [1, 1, 1, -1, 1, 1, 1, 0, 0, 1], [1, 1, 1, 1, 1, -1, 0, 1, -1, -1], [1, 1, 1, 1, -1, 1, 0, -1, 1, -1],
    #      [-1, 0, -1, 1, 1, 0, 1, 1, 1, 1], [0, 1, 0, 1, 1, -1, 0, 0, 1, -1], [1, 1, 1, 1, 0, 1, 1, 1, 0, -1],
    #      [1, 1, 1, 0, 1, 1, 1, 1, -1, 1], [1, -1, 1, 1, 1, -1, 1, 0, 1, 1], [1, 1, 1, 1, 0, -1, 0, 1, -1, 1],
    #      [1, 1, 1, 0, 1, -1, -1, 1, -1, 0], [-1, 0, 1, 0, 1, 1, 1, -1, 1, 0], [0, 1, 0, -1, 1, 1, 1, 1, 1, 1],
    #      [1, 1, 0, 1, 1, -1, 1, 1, -1, 0], [0, 1, 0, 0, 0, 1, 0, -1, 1, 1]]

    #   1  1  1
    # a = [[0, -1, 0, 1, -1, 1, -1, -1, 0, 0], [0, -1, 0, 1, -1, 0, -1, -1, 1, -1], [0, 1, 0, 0, 0, 0, -1, 0, -1, 1],
    #      [0, 1, 0, 1, -1, -1, 1, 1, 0, -1], [1, 0, 0, 1, -1, -1, 0, -1, -1, 0], [1, -1, 0, 1, 0, 0, 1, -1, 1, -1],
    #      [0, -1, -1, -1, -1, -1, 0, -1, 1, 0], [0, 1, -1, -1, -1, -1, 0, 1, 1, 0], [0, 0, -1, 0, 0, 0, 1, -1, 1, 0],
    #      [-1, 0, -1, -1, 1, -1, 0, -1, -1, 1], [1, 0, -1, 1, -1, 0, 0, -1, -1, 1], [0, 1, 1, -1, -1, 1, 1, 1, -1, 0],
    #      [-1, -1, 1, 1, -1, 1, -1, 0, 0, -1], [1, 1, -1, 0, 1, 0, 1, 1, 1, 0], [1, 1, -1, 1, -1, 1, 1, -1, 1, 1],
    #      [1, -1, 1, -1, 1, 0, -1, 1, 0, 0], [-1, 0, 1, 1, 0, 1, -1, 1, -1, -1], [0, 0, 1, 0, -1, 1, 1, -1, -1, 1],
    #      [-1, -1, -1, 1, 1, -1, 1, 0, 0, 0], [-1, -1, 0, -1, 1, -1, 1, -1, -1, 0]]

    #  sun
    # a = [
    #     [1, -1, 0, -1, 1, -1, 0, -1, 1, -1, 1],
    #     [0, 1, -1, 0, 0, 1, -1, 0, 0, 1, -1],
    #     [-1, 0, -1, -1, -1, 1, 1, -1, -1, 0, 0],
    #     [0, 0, -1, 1, 1, -1, -1, 1, 0, -1, -1],
    #     [-1, 1, -1, 0, -1, 1, 0, 0, -1, 1, 1],
    #
    #     [0, 1, 0, -1, -1, -1, -1, -1, 0, 1, -1],
    #     [1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0],
    #     [-1, 0, -1, 1, -1, 0, 1, 1, -1, 0, 1],
    #     [1, 1, 0, -1, 1, 1, -1, -1, 1, 1, -1],
    #     [-1, -1, -1, 0, 1, -1, 1, 0, -1, -1, 1],
    #
    #     [-1, 0, -1, -1, -1, -1, -1, -1, -1, 0, -1],
    #     [0, 1, 0, -1, 1, 1, 1, -1, 0, 1, 0],
    #     [-1, 0, -1, 1, 0, 0, 0, 1, -1, 0, 1],
    #     [-1, -1, -1, 0, -1, -1, -1, 0, -1, -1, -1],
    # ]

    #  8  1  1    30
    # a = [[0, 0, -1, 1, 1, 1, 1, 1, 0, 1], [0, 1, 1, 1, 0, 1, 1, 1, 1, 1], [1, 0, 1, 1, 0, 1, 1, 1, 1, 1],
    #      [0, 1, 1, 0, 1, 1, 1, 1, 1, 1], [0, 0, -1, -1, 1, 1, 1, 1, 0, 1], [0, 1, 1, 1, -1, 1, 0, 1, 1, 0],
    #      [1, 0, -1, 0, 0, 1, 1, 0, 0, 0], [1, -1, 1, 1, 1, -1, 1, 1, 1, 1], [1, 1, 0, 1, 1, 1, 1, 1, 1, 0],
    #      [1, 1, 1, 0, 0, 0, 1, 0, 1, 0], [-1, 1, 1, 1, 1, 1, 1, 1, 1, 0], [-1, 1, 0, 1, 1, 0, 0, 1, 1, 1],
    #      [-1, 1, 1, -1, 1, 1, 0, -1, 0, 1], [1, 0, 0, 1, 0, 1, 0, -1, 1, -1], [1, 1, 1, 0, 1, 1, 1, 1, -1, 1],
    #      [1, 1, -1, 1, 1, 1, 1, 0, 0, 0], [1, 1, 0, 0, 0, 1, -1, 0, 1, 1], [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #      [1, 1, -1, 1, 1, 1, -1, -1, 0, 1], [-1, 1, 1, 1, 1, -1, -1, 1, -1, 1], [0, 0, 1, 1, 1, 0, 1, 1, -1, -1],
    #      [-1, 1, -1, 1, 1, 0, 1, 1, 0, 1], [1, 1, 1, 1, 1, 1, -1, 1, -1, -1], [1, 0, -1, 0, 0, 1, 1, 1, 1, 1],
    #      [1, 0, 1, -1, 1, 1, 1, 0, 1, 0], [0, 1, -1, 0, 1, 1, 1, 1, 0, 0], [1, 0, 1, 1, -1, 1, 1, 1, 0, 1],
    #      [1, 1, 1, 1, 0, 0, 1, -1, 1, 1], [-1, 0, 1, 1, -1, 0, 1, 1, 1, 1], [1, 1, -1, 1, 1, 1, 1, -1, 1, 1]]

    #  3  1  1    30
    # a = [[1, -1, 1, 1, 0, 1, -1, 1, 0, 1], [1, 0, 0, 1, -1, 1, 1, 0, -1, 1], [0, 1, 1, 0, 1, 1, -1, 1, 1, 1],
    #      [1, 1, -1, 1, 1, 1, -1, -1, -1, 1], [1, 1, 0, -1, 0, 1, 1, 1, 1, 1], [1, 1, 1, 1, 0, 1, -1, -1, 1, 1],
    #      [1, 0, -1, -1, 1, 1, -1, 1, 0, 1], [1, 0, 1, 1, 0, 1, 0, -1, 1, 0], [1, -1, 0, 1, 1, 1, 0, 1, 1, 1],
    #      [1, 1, 1, 1, -1, -1, 1, 1, 1, 1], [1, 1, -1, 1, 1, 1, -1, -1, 1, 0], [1, -1, 1, 1, 0, 1, 1, 0, 1, 1],
    #      [1, 1, 1, 1, -1, -1, 1, 1, -1, 1], [-1, 0, 1, -1, 1, 0, -1, 0, 1, 1], [0, 1, -1, 0, 0, -1, 0, -1, 1, -1],
    #      [1, 1, 1, 1, 0, 1, 1, -1, 1, -1], [1, 0, 0, 1, 1, 1, 1, -1, 1, -1], [-1, 1, 0, 1, -1, 1, -1, 1, 1, 1],
    #      [-1, 0, 1, 0, 1, 1, -1, 1, 0, 1], [1, -1, 1, 1, -1, 0, 1, 1, 0, 1], [-1, 0, 0, 1, 0, 1, 1, -1, 1, 1],
    #      [1, 0, 1, 1, -1, -1, -1, 1, 1, 1], [1, 1, 1, 1, 0, 1, 1, 1, -1, 0], [1, 0, -1, 1, -1, -1, -1, 1, 0, 1],
    #      [1, 1, 1, -1, 0, 1, 1, -1, -1, 1], [1, -1, 1, 1, 1, 0, 1, 0, 0, 1], [1, 1, 1, -1, 1, 1, -1, 1, 0, 0],
    #      [-1, -1, 1, 0, 0, 1, 1, 1, -1, 1], [0, 1, 1, 1, 1, -1, 1, -1, 0, 1], [0, 0, 1, -1, 1, 1, 1, 1, 0, -1]]

    #  1  1  1    30
    # a = [[1, -1, 0, 1, 0, 1, 1, -1, -1, 1], [-1, -1, -1, 1, 0, 0, 0, 0, 0, 0], [0, -1, 1, 0, 0, -1, -1, -1, 1, 0],
    #      [0, 1, 0, 1, 1, 0, -1, -1, 1, 0], [0, 1, 0, -1, -1, -1, 1, -1, 1, 1], [-1, 1, 1, 1, 0, -1, 1, 0, -1, 0],
    #      [-1, -1, -1, -1, 0, 0, 0, 1, 1, -1], [0, 0, 1, -1, 1, -1, 0, -1, 1, -1], [0, 0, -1, 0, 0, 0, 1, 0, -1, 1],
    #      [-1, 0, -1, 1, -1, 0, 1, -1, -1, 0], [-1, 0, -1, 1, 1, 1, 0, -1, -1, 1], [0, -1, 1, 0, 1, 1, 0, 1, -1, 1],
    #      [0, -1, 1, 0, 1, 1, 1, -1, 0, 1], [-1, 0, 1, 1, -1, 1, 0, 1, -1, -1], [1, 0, 1, 1, 1, 1, 0, 0, 1, -1],
    #      [1, 0, 1, 1, -1, -1, -1, 1, 1, -1], [1, 1, 0, 1, 0, -1, 0, -1, 0, -1], [1, 1, 0, 0, 1, 0, 0, -1, 0, 1],
    #      [0, 0, 1, 0, 1, 0, 0, 0, 0, -1], [0, 1, -1, -1, -1, 1, 0, -1, 1, -1], [-1, 1, 1, -1, 0, 0, 1, 0, 1, 0],
    #      [0, -1, 1, 1, 1, 0, 0, -1, 1, 0], [-1, -1, -1, 0, -1, 0, 0, -1, 0, 1], [-1, 0, 0, -1, 1, 1, -1, 1, -1, 1],
    #      [1, 1, 0, 0, 0, -1, 0, 1, -1, 1], [0, -1, 0, -1, -1, 0, -1, -1, 1, -1], [-1, 1, -1, -1, 1, 1, -1, -1, 0, 1],
    #      [-1, 1, 0, -1, 0, 1, 0, 1, -1, -1], [1, 0, 0, 1, 0, -1, 1, 0, 0, 0], [-1, 0, 0, -1, -1, -1, 0, 0, -1, -1]]

    #  8  1  1    25
    # a = [[-1, 1, -1, 0, 0, 0, 1, 0, 1, 1], [0, 1, -1, 1, -1, 1, 1, 1, -1, 1], [1, 0, 1, -1, 0, 1, 1, 1, 1, 1],
    #      [1, 1, 1, -1, 1, 1, 1, 1, 1, 1], [0, 0, 1, 1, 1, 1, 1, -1, 1, 0], [1, 1, 1, 0, 1, 1, 1, 1, 1, -1],
    #      [0, 0, 1, 0, 0, 1, 1, 1, 1, 0], [-1, 0, 1, 1, 0, 0, 0, 1, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #      [1, 0, 1, 1, 1, 0, 1, 1, 1, 1], [-1, 1, 1, 1, 1, 1, 0, -1, 1, 0], [-1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
    #      [1, 1, 0, 1, 1, 1, 1, -1, 1, 1], [1, -1, 0, -1, 1, 1, 1, 0, 1, 1], [-1, -1, 1, 1, 1, 1, 1, 1, 1, 0],
    #      [1, 1, 1, 1, 0, 0, 0, 1, 1, 0], [1, -1, 1, 1, 1, 0, -1, 1, 0, 1], [0, -1, 1, 1, -1, 1, 1, -1, 1, 0],
    #      [1, 1, -1, 1, 0, 0, -1, 1, 1, 0], [1, 1, 1, 0, 1, 1, 0, 1, 1, 1], [1, -1, 1, -1, 1, 1, 1, -1, 1, -1],
    #      [1, 1, 1, 1, -1, 1, -1, 0, -1, 1], [0, 1, 0, 1, 1, -1, 0, 0, 0, 0], [1, 1, 1, -1, 1, 1, -1, 1, -1, 0],
    #      [-1, 0, 1, 1, -1, 1, 0, 0, 1, -1]]

    #  3  1  1    25
    # a = [[-1, 1, 1, 0, 1, -1, 1, -1, 1, -1], [1, 1, 1, -1, 1, 1, 1, -1, 0, 0], [1, 1, 0, -1, 1, -1, 0, 1, -1, 1],
    #      [0, 1, 1, 1, 1, 1, 1, 0, 1, 1], [1, -1, -1, 0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0, 0, 1, -1, 1, 0, -1],
    #      [0, 1, 1, 1, 0, 1, 1, 1, 1, 1], [1, -1, 1, 1, 0, 1, 0, -1, 0, 0], [1, 1, -1, 1, 0, -1, 1, 1, 1, 1],
    #      [1, 0, -1, 1, 1, 1, 0, 1, 1, -1], [1, 0, 1, 0, 1, -1, -1, 0, 1, -1], [0, -1, 1, 1, 1, 0, 0, 0, 1, 1],
    #      [1, 1, 1, 0, -1, 1, 0, 1, 1, -1], [1, 0, -1, 1, 1, 1, 1, 1, -1, 1], [1, 0, 1, -1, 0, 1, -1, 1, 1, 1],
    #      [1, 1, 1, 1, -1, -1, 1, 1, 1, 0], [0, 1, 1, 1, 0, 0, 0, 1, -1, 1], [1, -1, 1, 1, 0, 1, 1, 1, 1, -1],
    #      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [-1, 1, 0, 0, 0, 0, -1, 1, 1, 0], [-1, 1, 0, 1, 1, 0, 1, -1, 1, 1],
    #      [1, 0, 1, 1, 0, 0, 1, 0, 0, 1], [-1, -1, -1, 0, 1, 1, -1, 1, 1, 0], [1, -1, 1, 1, -1, -1, 1, 1, -1, 1],
    #      [1, 0, 0, 1, -1, 1, 1, 1, 1, 0]]

    #  1  1  1    25
    a = [[0, -1, 1, -1, 0, -1, 1, -1, -1, -1], [0, -1, -1, 1, 0, -1, 0, -1, -1, 0], [-1, 1, 0, 0, -1, -1, -1, 1, 1, 0],
         [0, 0, -1, 0, -1, -1, -1, 1, 0, 0], [0, 1, -1, 1, 1, 1, -1, -1, 1, 1], [1, 0, 0, 1, 1, 1, 0, 1, 0, -1],
         [0, 0, 1, 1, 0, -1, 1, -1, 0, 0], [-1, -1, 1, -1, 0, -1, 1, -1, 1, 0], [0, -1, 0, 0, 1, -1, -1, 0, 1, 0],
         [1, -1, 1, 0, -1, 1, 0, -1, 0, 1], [1, 0, -1, 0, -1, 0, -1, 0, -1, 0], [0, -1, -1, -1, 0, -1, 1, 1, 0, -1],
         [0, 1, 1, -1, -1, -1, 1, 1, 0, 0], [1, 1, -1, 0, 1, -1, 1, 1, 1, -1], [1, 0, -1, 0, 1, 1, 1, -1, 1, 0],
         [0, 0, 0, 1, -1, 1, 0, 1, 1, 0], [0, 0, -1, 0, 0, -1, 1, 0, 1, -1], [0, -1, -1, 1, 0, -1, 1, 0, 0, 0],
         [-1, 1, 0, 1, 0, 0, 0, 0, -1, 0], [1, 0, 0, 1, -1, 0, -1, -1, 1, 0], [1, 1, 1, 1, 0, -1, 0, -1, -1, -1],
         [0, -1, 0, 0, -1, 1, 1, 1, -1, 1], [1, 0, 0, -1, 0, -1, 0, 1, 0, 1], [0, -1, 1, -1, -1, 0, 1, 0, 1, 0],
         [0, -1, 0, 1, 0, 1, 0, -1, 1, 0]]

    N = len(a)
    M = len(a[0])



    # out_two_dimensional_array(a)
    ######################################################
    newa = np.array_split(a, 7)
    a_1 = newa[0]
    a_2 = newa[1]
    a_3 = newa[2]
    a_4 = newa[3]
    a_5 = newa[4]
    a_6 = newa[5]
    a_7 = newa[6]
    n_1 = len(a_1)
    n_2 = len(a_2)
    n_3 = len(a_3)
    n_4 = len(a_4)
    n_5 = len(a_5)
    n_6 = len(a_6)
    n_7 = len(a_7)

    #  获取基础概念
    base_cpt_1 = get_base_concept(a_1, n_1, M, 0)
    base_cpt_2 = get_base_concept(a_2, n_2, M, n_1)
    base_cpt_3 = get_base_concept(a_3, n_3, M, n_1 + n_2)
    base_cpt_4 = get_base_concept(a_4, n_4, M, n_1 + n_2 + n_3)
    base_cpt_5 = get_base_concept(a_5, n_5, M, n_1 + n_2 + n_3 + n_4)
    base_cpt_6 = get_base_concept(a_6, n_6, M, n_1 + n_2 + n_3 + n_4 + n_5)
    base_cpt_7 = get_base_concept(a_7, n_7, M, n_1 + n_2 + n_3 + n_4 + n_5 + n_6)

    #  获取所有概念
    all_cpt_1 = get_all_concept(base_cpt_1)
    size_of_all_cpt_1 = len(all_cpt_1)
    if is_top_concept(all_cpt_1, n_1, 0):
        all_cpt_1.append(get_top_concept(n_1, 0))
        size_of_all_cpt_1 += 1

    all_cpt_2 = get_all_concept(base_cpt_2)
    size_of_all_cpt_2 = len(all_cpt_2)
    if is_top_concept(all_cpt_2, n_2, n_1):
        all_cpt_2.append(get_top_concept(n_2, n_1))
        size_of_all_cpt_2 += 1

    all_cpt_3 = get_all_concept(base_cpt_3)
    size_of_all_cpt_3 = len(all_cpt_3)
    if is_top_concept(all_cpt_3, n_3, n_1 + n_2):
        all_cpt_3.append(get_top_concept(n_3, n_1 + n_2))
        size_of_all_cpt_3 += 1

    all_cpt_4 = get_all_concept(base_cpt_4)
    size_of_all_cpt_4 = len(all_cpt_4)
    if is_top_concept(all_cpt_4, n_4, n_1 + n_2 + n_3):
        all_cpt_4.append(get_top_concept(n_4, n_1 + n_2 + n_3))
        size_of_all_cpt_4 += 1

    all_cpt_5 = get_all_concept(base_cpt_5)
    size_of_all_cpt_5 = len(all_cpt_5)
    if is_top_concept(all_cpt_5, n_5, n_1 + n_2 + n_3 + n_4):
        all_cpt_5.append(get_top_concept(n_5, n_1 + n_2 + n_3 + n_4))
        size_of_all_cpt_5 += 1

    all_cpt_6 = get_all_concept(base_cpt_6)
    size_of_all_cpt_6 = len(all_cpt_6)
    if is_top_concept(all_cpt_6, n_6, n_1 + n_2 + n_3 + n_4 + n_5):
        all_cpt_6.append(get_top_concept(n_6, n_1 + n_2 + n_3 + n_4 + n_5))
        size_of_all_cpt_6 += 1

    all_cpt_7 = get_all_concept(base_cpt_7)
    size_of_all_cpt_7 = len(all_cpt_7)
    if is_top_concept(all_cpt_7, n_7, n_1 + n_2 + n_3 + n_4 + n_5 + n_6):
        all_cpt_7.append(get_top_concept(n_7, n_1 + n_2 + n_3 + n_4 + n_5 + n_6))
        size_of_all_cpt_7 += 1

    # out_concept_in_list(all_cpt_1)
    # out_concept_in_list(all_cpt_2)
    # out_concept_in_list(all_cpt_3)
    # out_concept_in_list(all_cpt_4)
    # out_concept_in_list(all_cpt_5)
    # out_concept_in_list(all_cpt_6)
    # out_concept_in_list(all_cpt_7)

    #  在所有概念中查找对象集，并返回冲突结果
    u_1 = []
    u_2 = []
    u_3 = []
    u_4 = []
    u_5 = []
    u_6 = []
    u_7 = []
    for i in range(n_1):
        u_1.append(i + 1)
    for i in range(n_1, n_1 + n_2):
        u_2.append(i + 1)
    for i in range(n_1 + n_2, n_1 + n_2 + n_3):
        u_3.append(i + 1)
    for i in range(n_1 + n_2 + n_3, n_1 + n_2 + n_3 + n_4):
        u_4.append(i + 1)
    for i in range(n_1 + n_2 + n_3 + n_4, n_1 + n_2 + n_3 + n_4 + n_5):
        u_5.append(i + 1)
    for i in range(n_1 + n_2 + n_3 + n_4 + n_5, n_1 + n_2 + n_3 + n_4 + n_5 + n_6):
        u_6.append(i + 1)
    for i in range(n_1 + n_2 + n_3 + n_4 + n_5 + n_6, N):
        u_7.append(i + 1)


    t = 0
    ans = []
    for i in range(30):

        #  随机生成一些对象集
        count = 1000
        b = random_object(N, count)

        #  开始计时
        start = time.perf_counter()
        #  b是随机生成的集合
        #  拆分，分别找到对应的概念，合并，计算mx
        b_size = len(b)
        b_1 = []
        b_2 = []
        b_3 = []
        b_4 = []
        b_5 = []
        b_6 = []
        b_7 = []
        for j in range(b_size):
            b_1.append(intersection(b[j], u_1))
            b_2.append(intersection(b[j], u_2))
            b_3.append(intersection(b[j], u_3))
            b_4.append(intersection(b[j], u_4))
            b_5.append(intersection(b[j], u_5))
            b_6.append(intersection(b[j], u_6))
            b_7.append(intersection(b[j], u_7))

        for j in range(b_size):
            res_1 = concept([], [], [], [])
            res_2 = concept([], [], [], [])
            res_3 = concept([], [], [], [])
            res_4 = concept([], [], [], [])
            res_5 = concept([], [], [], [])
            res_6 = concept([], [], [], [])
            res_7 = concept([], [], [], [])

            #  第一个
            if len(b_1) != 0:
                flg = False
                for k in range(size_of_all_cpt_1):
                    #  寻找直接相等的
                    if b_1[j] == all_cpt_1[k].X:
                        res_1 = all_cpt_1[k]
                        flg = True
                if not flg:
                    #  寻找包含的最小的概念
                    res_1 = contain_object(all_cpt_1, b_1[j], M)

            # 第二个
            if len(b_2) != 0:
                flg = False
                for k in range(size_of_all_cpt_2):
                    #  寻找直接相等的
                    if b_2[j] == all_cpt_2[k].X:
                        res_2 = all_cpt_2[k]
                        flg = True
                if not flg:
                    #  寻找包含的最小的概念
                    res_2 = contain_object(all_cpt_2, b_2[j], M)

            # 第三个
            if len(b_3) != 0:
                flg = False
                for k in range(size_of_all_cpt_3):
                    #  寻找直接相等的
                    if b_3[j] == all_cpt_3[k].X:
                        res_3 = all_cpt_3[k]
                        flg = True
                if not flg:
                    #  寻找包含的最小的概念
                    res_3 = contain_object(all_cpt_3, b_3[j], M)

            # 第四个
            if len(b_4) != 0:
                flg = False
                for k in range(size_of_all_cpt_4):
                    #  寻找直接相等的
                    if b_4[j] == all_cpt_4[k].X:
                        res_4 = all_cpt_4[k]
                        flg = True
                if not flg:
                    #  寻找包含的最小的概念
                    res_4 = contain_object(all_cpt_4, b_4[j], M)

            # 第五个
            if len(b_5) != 0:
                flg = False
                for k in range(size_of_all_cpt_5):
                    #  寻找直接相等的
                    if b_5[j] == all_cpt_5[k].X:
                        res_5 = all_cpt_5[k]
                        flg = True
                if not flg:
                    #  寻找包含的最小的概念
                    res_5 = contain_object(all_cpt_5, b_5[j], M)

            # 第六个
            if len(b_6) != 0:
                flg = False
                for k in range(size_of_all_cpt_6):
                    #  寻找直接相等的
                    if b_6[j] == all_cpt_6[k].X:
                        res_6 = all_cpt_6[k]
                        flg = True
                if not flg:
                    #  寻找包含的最小的概念
                    res_6 = contain_object(all_cpt_6, b_6[j], M)

            # 第六个
            if len(b_7) != 0:
                flg = False
                for k in range(size_of_all_cpt_7):
                    #  寻找直接相等的
                    if b_7[j] == all_cpt_7[k].X:
                        res_7 = all_cpt_7[k]
                        flg = True
                if not flg:
                    #  寻找包含的最小的概念
                    res_7 = contain_object(all_cpt_7, b_7[j], M)

            #  前并后交
            res = combine_concept(combine_concept(combine_concept(res_1, res_2), combine_concept(res_3, res_4)),
                                  combine_concept(combine_concept(res_5, res_6), res_7))

            # out_one_concept(res)

            ans.append(res.get_mx(M))

        #  结束计时
        end = time.perf_counter()
        t = t + end - start

    print(t / 30 * 1000)


if __name__ == '__main__':
    main()
