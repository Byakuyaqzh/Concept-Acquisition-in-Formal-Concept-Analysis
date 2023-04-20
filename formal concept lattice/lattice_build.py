from random import random
import time


class concept:
    def __init__(self, x, a):
        self.X = x
        self.A = a


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
    return concept(union(a.X, b.X), intersection(a.A, b.A))


#  判断当前结果中是否缺少顶部概念   缺少 ： true， 不缺少 ： false
def top_concept(all_cpt, n, size):
    s = []
    for i in range(n):
        s.append(i+1)
    for i in range(size):
        if all_cpt[i].X == s:
            return False
    return True


#  输出一个概念
def out_one_concept(cpt: concept):
    x_size = len(cpt.X)
    a_size = len(cpt.A)
    print("( ", end="")
    if x_size == 0:
        print("'φ'", end=" ")
    else:
        for j in range(x_size):
            print(cpt.X[j], end=" ")
    print(",  ", end="")
    if a_size == 0:
        print("'φ'", end=" ")
    else:
        for j in range(a_size):
            print(cpt.A[j], end=" ")
    print(")")


#  输出一个序列中的所有概念
def out_concept_in_list(cpt: list):
    list_size = len(cpt)
    for i in range(list_size):
        out_one_concept(cpt[i])


#  创建二维数组
def get_two_dimensional_array(n, m):
    a = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if random() > 0.5:
                a[i][j] += 1
    return a


#  以显眼的方式输出二维数组
def out_two_dimensional_array(a):
    n = len(a)
    m = len(a[0])
    for i in range(n):
        print(" |-->    ", end="")
        for j in range(m):
            print(a[i][j], end="  ")
        print()
    print()


#  获取基础概念
def get_base_concept(a, n, m) -> list:
    base_cpt: list = []
    for i in range(n):
        cpt = concept([], [])
        cpt.X.append(i + 1)
        for j in range(m):
            if a[i][j] == 1:
                cpt.A.append(chr(j + 97))
        base_cpt.append(cpt)
    return base_cpt


#  获取所有概念
def get_all_concept(base_cpt: list) -> list:
    num_of_basecpt = len(base_cpt)
    if num_of_basecpt == 1:
        return base_cpt

    #  使用两个数组交替存放结果
    all_cpt = [[], []]

    # 首先插入底部的（phi，all）元素和第一个元素
    bottom_cpt = concept([], [])
    for i in range(num_of_basecpt):
        bottom_cpt.A = union(bottom_cpt.A, base_cpt[i].A)
    all_cpt[0].append(bottom_cpt)
    all_cpt[0].append(base_cpt[0])

    #  使用两个数组交替存放结果, 每次循环后 交换两个数组的作用
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
            if judge_intersection(insert_cpt.A, cpt.A):
                #  存在交集，将两者合并得到新概念
                new_cpt = combine_concept(cpt, insert_cpt)
                #  遍历已生成的所有概念，判断是否存在一个概念，其内涵等于Ncpt的内涵    有 ：True  没有 ： False
                flg: bool = False
                size_of_L = len(all_cpt[L])
                for k in range(size_of_L):
                    if new_cpt.A == all_cpt[L][k].A:
                        #  若有，更新这个概念
                        if all_cpt[L][k].X != new_cpt.X:
                            all_cpt[L][k] = update_concept(all_cpt[L][k], union(all_cpt[L][k].X, new_cpt.X))
                        #  保存当前访问的概念
                        if all_cpt[L][k].A != cpt.A:
                            all_cpt[L].append(cpt)
                        flg = True
                        break
                #  end for
                #  若没有，则插入合并后的概念
                if not flg:
                    all_cpt[L].append(new_cpt)
                    #  保存当前访问的概念
                    if new_cpt.A != cpt.A:
                        all_cpt[L].append(cpt)
            # end if
            #  不存在交集
            else:
                all_cpt[L].append(cpt)
        #  end for
        #  本次循环结束，清空R，用于下次存放结果
        all_cpt[R].clear()
    #  end for

    #  总循环结束，检查结果
    if not all_cpt[0]:
        return all_cpt[1]
    else:
        return all_cpt[0]


#  获取顶部概念
def get_top_concept(n):
    cpt = concept([], [])
    for i in range(n):
        cpt.X.append(i + 1)
    return cpt


def main():
    # N = 4
    # M = 4

    #  获取二位数组
    # a = get_two_dimensional_array(N, M)
    #  手动输入二位数组
    # a = [[0, 1, 0, 1, 0, 0, 0],
    #      [0, 1, 1, 0, 0, 0, 0],
    #      [0, 1, 1, 1, 1, 0, 1],
    #      [1, 1, 0, 1, 1, 0, 0],
    #      [1, 1, 1, 0, 1, 1, 0],
    #      [1, 0, 1, 0, 0, 0, 1],
    #      [0, 0, 1, 0, 0, 0, 0]]
    a = [
        [1, 0, 0],
        [0, 1, 1],
        [1, 0, 1],
    ]

    N = len(a)
    M = len(a[0])
    out_two_dimensional_array(a)

    #  开始计时
    start = time.perf_counter()

    #  获取基础概念
    base_cpt = get_base_concept(a, N, M)
    # out_concept_in_list(base_cpt)

    #  获取所有概念
    all_cpt = get_all_concept(base_cpt)
    size_of_all_cpt = len(all_cpt)
    if top_concept(all_cpt, N, size_of_all_cpt):
        all_cpt.append(get_top_concept(N))
        size_of_all_cpt += 1

    #  结束计时
    end = time.perf_counter()

    out_concept_in_list(all_cpt)
    print("上面是所有的概念，总数是： ", end="")
    print(size_of_all_cpt)
    print("运行时间为： ", round(end - start), '  seconds')


if __name__ == '__main__':
    main()
