import time
from random import random


class concept:
    def __init__(self, x, a, b, c, d):
        self.X = x
        self.A = a
        self.B = b
        self.C = c
        self.D = d

    def get_mx(self, m):
        V = []
        for i in range(m):
            V.append(chr(i + 97))
        # alpha = intersection( union(self.A, self.B), self.C )
        beta = subtract(self.B, self.D)
        gamma = union(subtract(self.B, self.A), subtract(self.D, self.C))
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
    return concept(union(a.X, b.X), intersection(a.A, b.A), intersection(a.B, b.B),
                   intersection(a.C, b.C), intersection(a.D, b.D))


#  判断当前结果中是否缺少顶部概念   缺少 ： true， 不缺少 ： false
def is_top_concept(all_cpt, n, size):
    s = []
    for i in range(n):
        s.append(i + 1)
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
    d_size = len(cpt.D)
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
    #  D
    if d_size == 0:
        print("'φ'", end=" ")
    else:
        for j in range(b_size):
            print(cpt.B[j], end=" ")
    print(", ", end="")
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
            if 0 < rand < 0.7:
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
def get_base_concept(a, n: int, m: int):
    base_cpt = []
    for i in range(n):
        cpt = concept([], [], [], [], [])
        cpt.X.append(i + 1)
        for j in range(m):
            temp = a[i][j]
            if temp == 1:
                cpt.A.append(chr(j + 97))
            if temp == 1 or temp == 0:
                cpt.B.append(chr(j + 97))
            if temp == -1:
                cpt.C.append(chr(j + 97))
            if temp == -1 or temp == 0:
                cpt.D.append(chr(j + 97))
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
    bottom_cpt = concept([], [], [], [], [])
    for i in range(num_of_basecpt):
        bottom_cpt.A = union(bottom_cpt.A, base_cpt[i].A)
        bottom_cpt.B = union(bottom_cpt.B, base_cpt[i].B)
        bottom_cpt.C = union(bottom_cpt.C, base_cpt[i].C)
        bottom_cpt.D = union(bottom_cpt.D, base_cpt[i].D)
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
                    or judge_intersection(insert_cpt.C, cpt.C) or judge_intersection(insert_cpt.D, cpt.D):
                #  存在交集，将两者合并得到新概念
                new_cpt = combine_concept(cpt, insert_cpt)
                #  遍历已生成的所有概念，判断是否存在一个概念，其内涵等于Ncpt的内涵    有 ：True  没有 ： False
                flg: bool = False
                sizeof_L = len(all_cpt[L])
                for k in range(sizeof_L):
                    if new_cpt.A == all_cpt[L][k].A and new_cpt.B == all_cpt[L][k].B \
                            and new_cpt.C == all_cpt[L][k].C and new_cpt.D == all_cpt[L][k].D:
                        #  若有，更新这个概念
                        if all_cpt[L][k].X != new_cpt.X:
                            all_cpt[L][k] = update_concept(all_cpt[L][k], union(all_cpt[L][k].X, new_cpt.X))
                        #  保存当前访问的概念
                        if all_cpt[L][k].A != cpt.A or all_cpt[L][k].B != cpt.B \
                                or all_cpt[L][k].C != cpt.C or all_cpt[L][k].D != cpt.D:
                            all_cpt[L].append(cpt)
                        flg = True
                        break
                # end for
                #  若没有，插入合并后的概念
                if not flg:
                    all_cpt[L].append(new_cpt)
                    #  保存当前访问的概念
                    if new_cpt.A != cpt.A or new_cpt.B != cpt.B \
                            or new_cpt.C != cpt.C or new_cpt.D != cpt.D:
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
def get_top_concept(n):
    cpt = concept([], [], [], [], [])
    for i in range(n):
        cpt.X.append(i + 1)
    return cpt


#  a: list of concept    b: object
def contain_object(a: list, b: list) -> concept:
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
    ans = concept([], [], [], [], [])
    while flg:
        for i in range(size_res):
            if len(res[i].X) == size_b + flg:
                return res[i]
        flg += 1


def random_object(n, count) -> list:
    res = []
    while len(res) < 10:
        a = []
        for j in range(n):
            if random() < 0.4:
                a.append(j + 1)
        if 1 < len(a) < 6:
            res.append(a)
    return res


def find_object(a: list, all_cpt, m) -> float:
    size_of_all = len(all_cpt)
    res = concept([], [], [], [], [])
    flg = False
    for i in range(size_of_all):
        #  寻找直接相等的
        if a == all_cpt[i].X:
            res = all_cpt[i]
            flg = True
    if not flg:
        #  寻找包含的最小的概念
        res = contain_object(all_cpt, a)
    return res.get_mx(m)


def main():
    N = 20
    M = 10

    #  获取二维数组
    # a = get_two_dimensional_array(N, M)
    a = [[1, 1, -1, 1, 1, 1, 1, 0, 1, 1], [1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
         [1, 0, 0, -1, 1, 1, 0, 0, 1, 1], [1, 0, 0, 0, 1, 1, 1, 0, 0, 0],
         [0, -1, 1, 1, 0, -1, 1, 1, 1, 1], [-1, 1, 1, 0, 1, 1, 1, 1, -1, 0],
         [1, 1, 1, 1, 1, 1, 1, -1, 1, 1], [0, 0, 1, -1, 0, -1, 1, 0, 0, 0],
         [1, 1, 1, 1, 1, 0, 1, 1, 1, -1], [0, -1, 1, 1, 1, 1, 0, 1, 1, 0],

         [1, 1, -1, 1, -1, 1, 1, 0, 1, 0], [1, 1, 1, -1, 0, 1, 1, 1, 1, 1],
         [1, 1, 0, 1, -1, 0, 1, -1, 1, 0], [0, 0, 1, -1, 0, -1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 0, 1], [1, 1, 1, 1, 1, 1, -1, 0, 0, 1],
         [0, 1, 1, 1, 1, 1, 0, 1, 1, -1], [-1, 1, 1, 1, -1, -1, 1, -1, 0, 0],
         [0, 1, 0, 1, 1, 1, 0, 1, -1, 0], [1, 1, 0, -1, 1, 1, 1, 1, 1, 1]]

    # out_two_dimensional_array(a)

    #  获取基础概念
    base_cpt = get_base_concept(a, N, M)
    # out_concept_in_list(base_cpt)

    #  获取所有概念
    all_cpt = get_all_concept(base_cpt)
    size_of_all_cpt = len(all_cpt)
    if is_top_concept(all_cpt, N, size_of_all_cpt):
        all_cpt.append(get_top_concept(N))
        size_of_all_cpt += 1

    # out_concept_in_list(all_cpt)
    # print("所有的概念的总数是： ", end="")
    # print(size_of_all_cpt)

    ans = []
    for t in range(10):

        #  随机生成一些对象集
        count = 700
        b = random_object(N, count)

        #  开始计时
        start = time.perf_counter()

        #  在所有概念中查找对象集，并返回冲突结果
        b_size = len(b)
        c = []
        for i in range(b_size):
            c.append(find_object(b[i], all_cpt, M))

        #  结束计时
        end = time.perf_counter()
        ans.append(end - start)

        print("已运行", end="")
        print(t, end="")
        print("次")
        # print("运行时间为： ", end - start, '  seconds')

    sum1 = 0
    for i in range(10):
        sum1 = sum1 + ans[i]
    print(sum1 / 10)


if __name__ == '__main__':
    main()
