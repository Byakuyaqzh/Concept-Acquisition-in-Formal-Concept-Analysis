import time


class concept:
    def __init__(self, x: list, b: list):
        self.X = x
        self.B = b

    #  更新概念的外延
    def update_concept(self, x: list):
        return concept(union(self.X, x), self.B)


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
    res = []
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


#  合并两个概念，外延不变，内涵取差集，
#  差集：指 a - b，而不是b - a
def subtract(a, b):
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
            j += 1
        else:
            i += 1
            j += 1
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


#  输出一个概念
def out_one_concept(cpt, e=-1):
    x_size = len(cpt.X)
    y_size = len(cpt.B)
    if -1 < e < 9:
        print(e + 1, end="  ")
    elif e > 8:
        print(e + 1, end=" ")
    print("-> [ ", end="")
    #  输出
    for i in range(x_size):
        print(cpt.X[i], end=" ")
    print("],  [ ", end="")
    for i in range(y_size):
        print(cpt.B[i], end=" ")
    print("]")


#  输出一个序列中的所有概念
def out_concept_in_list(cpt: list):
    list_size = len(cpt)
    for i in range(list_size):
        out_one_concept(cpt[i], i)
    print()


#  获取所有概念
def get_all_concept(a, n, m) -> list:
    #  获取基础概念
    base_cpt = []
    for i in range(n):
        cpt = concept([], [])
        cpt.X.append(i + 1)
        for j in range(m):
            if a[i][j] == 1:
                # cpt.B.append(chr(j + 97))
                cpt.B.append(j + 1)
        base_cpt.append(cpt)

    out_concept_in_list(base_cpt)
    print()

    #  使用两个数组交替存放结果
    all_cpt = [[], []]

    #  首先，插入前两个概念
    #  1 (φ, x1*)
    #  2 (x1, allObj)
    first_cpt_B = []
    second_cpt_B = []
    for i in range(m):
        if a[0][i] == 0:
            # first_cpt_B.append(chr(i + 97))
            first_cpt_B.append(i + 1)
        # second_cpt_B.append(chr(i + 97))
        second_cpt_B.append(i + 1)
    all_cpt[0].append(concept([], first_cpt_B))
    all_cpt[0].append(concept([1], second_cpt_B))

    #  使用两个数组交替存放结果, 每次循环后 交换两个数组的作用
    #  使用L、R 表示两个数组，每次循环后交换位置
    #  *首次循环时，所有概念存放在0中，循环结束后结果存放在1中
    #  *在程序循环中，始终操作/计算R中的概念，将结果存放在L中
    #  本次循环中，R 储存的是上一次循环的结果
    turn: bool = True
    for i in range(1, n):
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
            if judge_intersection(insert_cpt.B, cpt.B):
                #  存在交集，将两者合并得到新概念，外延不变，内涵取差集，
                new_cpt = concept(cpt.X, subtract(cpt.B, insert_cpt.B))
                #  遍历已生成的所有概念，判断是否存在一个概念，其内涵等于Ncpt的内涵    有 ：True  没有 ： False
                flg: bool = False
                size_of_L = len(all_cpt[L])
                for k in range(size_of_L):
                    if new_cpt.B == all_cpt[L][k].B:
                        # #  若有，更新这个概念
                        # if all_cpt[L][k].X != new_cpt.X:
                        #     all_cpt[L][k] = update_concept(all_cpt[L][k], union(all_cpt[L][k].X, new_cpt.X))
                        # #  保存当前访问的概念
                        # if all_cpt[L][k].A != cpt.A:
                        #     all_cpt[L].append(cpt)
                        flg = True
                        break
                #  end for
                #  若没有，则插入合并后的概念
                if not flg:
                    all_cpt[L].append(new_cpt)
                #  保存当前访问的概念

                all_cpt[L].append(cpt.update_concept(insert_cpt.X))

            # end if
            #  不存在交集
            else:
                all_cpt[L].append(cpt)
        #  end for

        # print("这是第", end="")
        # print(i, end="")
        # print("次循环")
        # out_one_concept(insert_cpt)
        # print()
        # out_concept_in_list(all_cpt[R])

        #  本次循环结束，清空R，用于下次存放结果
        all_cpt[R].clear()
    #  end for

    #  总循环结束，检查结果
    if all_cpt[0]:
        return all_cpt[0]
    else:
        return all_cpt[1]


def main():
    a = [
        [1, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 1, 1, 0],
        [0, 1, 1, 0, 1, 0, 0],
        [0, 0, 0, 1, 0, 0, 1],
        [0, 1, 1, 0, 1, 1, 0],
        [0, 1, 0, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 1],

        # [0, 0, 1, 1, 0, 1, 0],
        # [1, 1, 0, 0, 0, 1, 0],
        # [0, 1, 0, 1, 1, 1, 1],
        # [0, 0, 0, 1, 1, 1, 1],
        # [1, 1, 1, 0, 1, 0, 0],
        # [1, 1, 1, 1, 0, 1, 0],
    ]

    N = len(a)
    M = len(a[0])

    out_two_dimensional_array(a)

    #  开始计时
    start = time.perf_counter()

    #  获取所有概念
    all_cpt = get_all_concept(a, N, M)

    #  结束计时
    end = time.perf_counter()

    out_concept_in_list(all_cpt)
    print("上面是所有的概念，总数是： ", end="")
    print(len(all_cpt))
    print("运行时间为： ", round(end - start), '  seconds')


if __name__ == '__main__':
    main()
