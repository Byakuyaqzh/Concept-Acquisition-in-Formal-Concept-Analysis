import time
import random

class concept:
    def __init__(self, x, y):
        self.X = x
        self.Y = y


#  输出一个序列中的所有概念
def output_concept_list(all_cpt):
    n = len(all_cpt)
    for i in range(n):
        output_concept(all_cpt[i], i)
    print()


#  输出一个概念
def output_concept(cpt, e=-1):
    x_size = len(cpt.X)
    y_size = len(cpt.Y)
    if -1 < e < 9:
        print(e + 1, end="  ")
    elif e > 8:
        print(e + 1, end=" ")
    print("-> [  ", end="")
    #  输出
    for i in range(x_size):
        print(cpt.X[i], end="  ")
    print("],  [  ", end="")
    for i in range(y_size):
        print(cpt.Y[i], end="  ")
    print("]")


#  第一个值是对象个数， 第二个值： 3 ->  [0, 0.5, 1],  5 -> [0, 0.25, 0.5, 0.75, 1]
def get_table(t):
    ans = [[0 for _ in range(t)] for _ in range(t)]
    val = []
    if t == 3:
        val = [0, 0.5, 1]
    if t == 5:
        val = [0, 0.25, 0.5, 0.75, 1]

    for i in range(t):
        for j in range(t):
            if 1 - val[i] + val[j] >= 1:
                ans[i][j] = 1
            else:
                ans[i][j] = 1 - val[i] + val[j]
    return ans


#  获取x所有可能的排列
def get_all_sort_x(n, t):
    val = []
    if t == 3:
        val = [0, 0.5, 1]
    if t == 5:
        val = [0, 0.25, 0.5, 0.75, 1]
    ans = []

    #  d: 深度   j: 3/5个值   tmp: 当前结果
    def dfs(d, tmp):
        if d == n:
            res = [0 for _ in range(n)]
            for k in range(n):
                res[k] = tmp[k]
            ans.append(res)
            return
        for j in range(t):
            tmp[d] = val[j]
            dfs(d + 1, tmp)

    for i in range(t):
        first = [0 for _ in range(n)]
        first[0] = val[i]
        dfs(1, first)
    return ans


#  查表
def judge_xy(table, x, y):
    if len(table) == 3:
        return table[int(x * 2)][int(y * 2)]
    if len(table) == 5:
        return table[int(x * 4)][int(y * 4)]


#  获取所有概念
def get_all_cpt(table, a, x_list):
    #  all_cpt 存放最后的结果
    all_cpt = []
    n = len(a)
    m = len(a[0])
    num = len(x_list)

    #  遍历所有x的组合
    for i in range(num):
        #  生成的新概念
        cpt = concept([], [])
        cpt.X = x_list[i]
        for j in range(m):
            tmp = []
            for k in range(n):
                tmp.append(judge_xy(table, x_list[i][k], a[k][j]))
            cpt.Y.append(min(tmp))

        all_cpt.append(cpt)

        # #  插入总集
        # sizeof_all = len(all_cpt)
        # #  插入第一个
        # if sizeof_all == 0:
        #     all_cpt.append(cpt)
        # #  遍历，检查是否重复   flg :  True -> 不重复   False -> 重复
        # else:
        #     flg = True
        #     for k in range(sizeof_all):
        #         #  重复
        #         if cpt.Y == all_cpt[k].Y:
        #             for g in range(n):
        #                 all_cpt[k].X[g] = max(all_cpt[k].X[g], cpt.X[g])
        #             flg = False
        #     #  无重复
        #     if flg:
        #         all_cpt.append(cpt)

    return all_cpt


def get_random_list_3(n, num):
    res = []
    choices = [0, 0.5, 1]
    for i in range(num):
        tmp = [random.choice(choices) for _ in range(n)]
        res.append(tmp)
    return res


def get_random_list_5(n, num):
    res = []
    choices = [0, 0.25, 0.5, 0.75, 1]
    for i in range(num):
        tmp = [random.choice(choices) for _ in range(n)]
        res.append(tmp)
    return res


#  合并属性，取最小值
def combine_attribute(a, b):
    return [min(x) for x in zip(a, b)]


#  检查合并结果，是否与直接获取的结果相同
def check_combine_result(comb_res, all_res):
    flg = True
    for i, cpt in enumerate(comb_res):
        for c in all_res:
            if cpt.X == c.X:
                if cpt.Y != c.Y:
                    flg = False
                    break
        if not flg:
            break
    return flg


def main():
    a = [
        #  纵向 1
        # [1, 0.5, 0.5, 1, 1],
        [1, 1, 1, 1, 0.5],
        [0, 0, 0.5, 0.5, 1],

        #  纵向
        #  1
        # [1, 0.5, 0.5, 1, 1],
        # [1, 1, 1, 1, 0.5],
        # [0, 0, 0.5, 0.5, 1],


    ]
    b = [
        #  纵向 1
        [0.5, 0, 0.5, 1, 0.5],
        [1, 0.5, 1, 0, 0],

        #  纵向 2
        # [0.5, 0, 0.5, 1, 0.5],
        # [1, 0.5, 1, 0, 0],
        # [0.5, 0, 0, 0, 1],
    ]
    c = [
        # [1, 0.5, 0.5, 1, 1],
        [1, 1, 1, 1, 0.5],
        [0, 0, 0.5, 0.5, 1],
        [0.5, 0, 0.5, 1, 0.5],
        [1, 0.5, 1, 0, 0],
    ]
    t = 3
    #  t 代表模糊值的种类    3 ->  [0, 0.5, 1]  ,  5 -> [0, 0.25, 0.5, 0.75, 1]

    n = len(a)
    m = len(b)

    #  表
    table = get_table(t)
    #  x 所有可能的排列
    x_list_n = get_all_sort_x(n, t)
    x_list_m = get_all_sort_x(m, t)
    x_list_nm = get_all_sort_x(n+m, t)

    #  通过 表、模糊形式背景、x所有可能的排列，计算所有概念
    all_cpt_1 = get_all_cpt(table, a, x_list_n)
    all_cpt_2 = get_all_cpt(table, b, x_list_m)
    all_cpt_3 = get_all_cpt(table, c, x_list_nm)
    all_cpt_1_size = len(all_cpt_1)
    all_cpt_2_size = len(all_cpt_2)
    all_cpt_3_size = len(all_cpt_3)

    #  输出所有概念
    # output_concept_list(all_cpt_1)
    # print()
    # output_concept_list(all_cpt_2)
    # print()

    #  获取随机的模糊对象集
    num = 10
    random_list = get_random_list_3(n+m, num)
    # random_list = get_random_list_5(n+m, num)

    #  获取所有的模糊对象集
    num = len(x_list_nm)

    combine_result = []

    for i in range(num):

        random_list_n = random_list[i][:n]
        random_list_m = random_list[i][-m:]

        cpt_1_y = []
        cpt_2_y = []

        for j in range(all_cpt_1_size):
            if all_cpt_1[j].X == random_list_n:
                cpt_1_y = all_cpt_1[j].Y
                break
        for j in range(all_cpt_2_size):
            if all_cpt_2[j].X == random_list_m:
                cpt_2_y = all_cpt_2[j].Y
                break

        combine_result.append(concept(random_list[i], combine_attribute(cpt_1_y, cpt_2_y)))
    output_concept_list(combine_result)

    #  检查合并结果是否正确
    print(check_combine_result(combine_result, all_cpt_3))


#  代码已完成
if __name__ == "__main__":
    main()
