import time
import random

class concept:
    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __eq__(self, other):
        if isinstance(other, concept):
            return self.X == other.X and self.Y == other.Y
        return False

    def __str__(self):
        return f"concept([{', '.join(map(str, self.X))}], [{', '.join(map(str, self.Y))}])"

    def get_conflict_level(self):
        return round(1 - sum(self.Y) / len(self.Y), 5)


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
    print("]", end="        ")
    print(cpt.get_conflict_level())


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


#  5 -> 3
def five_to_three_concept(all_cpt_5):
    #  定义结果集
    res = []

    for cpt in all_cpt_5:
        if all(x in {0, 0.5, 1} for x in cpt.X):
            res.append(cpt)

    return res


#  检查合并结果，是否与直接获取的结果相同
def check_combine_result(comb_res, all_res):
    if len(comb_res) != len(all_res):
        return "长度不相等！"

    n = len(comb_res)
    for i in range(n):
        if comb_res[i] != all_res[i]:
            return "元素不相等！当前序号为" + str(i) + \
                   '[' + ', '.join(str(x) for x in comb_res[i].X) + ', || ' \
                   + ', '.join(str(x) for x in comb_res[i].Y) + ']' + \
                   ', [' + ', '.join(str(x) for x in all_res[i].X) + ', || ' \
                   + ', '.join(str(x) for x in all_res[i].Y) + ']'

    return "True"


def main():

    n = 7
    m = 8

    k = 5

    choices = [0, 0.5, 1]
    a = [[random.choice(choices) for _ in range(k)] for _ in range(n)]
    b = [[random.choice(choices) for _ in range(k)] for _ in range(m)]

    c = a + b


    # n = len(a)
    # m = len(b)

    #  t 代表模糊值的种类    3 ->  [0, 0.5, 1]  ,  5 -> [0, 0.25, 0.5, 0.75, 1]
    t3 = 3
    t5 = 5
    #  表
    table3 = get_table(t3)
    table5 = get_table(t5)


    #  获取前置概念
    front_cpt_start_time = time.perf_counter()
    #  x 所有可能的排列   第一个3  第二个5
    x_list_n = get_all_sort_x(n, t3)
    x_list_m = get_all_sort_x(m, t5)

    #  通过 表、模糊形式背景、x所有可能的排列，计算所有概念
    all_cpt_1 = get_all_cpt(table3, a, x_list_n)
    all_cpt_2 = get_all_cpt(table5, b, x_list_m)
    front_cpt_end_time = time.perf_counter()


    #  直接获取所有概念
    all_cpt_start_time = time.perf_counter()

    #  总结果 5
    x_list_nm = get_all_sort_x(n+m, t3)

    all_cpt_3 = get_all_cpt(table3, c, x_list_nm)

    all_cpt_end_time = time.perf_counter()

    #  上面完成了两组冲突分析结果的制作，第一组是3等级分析，第二组是5等级分析

    #  3 -> 5
    #  降低分析等级花费时间
    up_level_start_time = time.perf_counter()

    all_cpt_2_53 = five_to_three_concept(all_cpt_2)
    # output_concept_list(all_cpt_2_53)

    up_level_end_time = time.perf_counter()

    #  测试  3 -> 5 与 5是否一致   输出 -> true
    # x_list_m_test = get_all_sort_x(m, t3)
    # all_cpt_2_test = get_all_cpt(table3, b, x_list_m_test)
    # print(check_combine_result(all_cpt_2_53, all_cpt_2_test))


    #  获取所有的模糊对象集
    num = len(x_list_nm)
    combine_result = []

    #  合并
    #  合并概念花费时间
    combine_start_time = time.perf_counter()
    for cpt_1 in all_cpt_1:
        for cpt_2 in all_cpt_2_53:
            cpt = concept([], [])
            cpt.X = cpt_1.X + cpt_2.X
            cpt.Y = [min(num1, num2) for num1, num2 in zip(cpt_1.Y, cpt_2.Y)]
            combine_result.append(cpt)

    combine_end_time = time.perf_counter()
    # print('''''''''''''''''''''''''''''''''''''')
    # output_concept_list(combine_result)
    # output_concept_list(all_cpt_3)

    #  检查合并结果是否正确
    # print(check_combine_result(combine_result, all_cpt_3))



    print("获取前置概念花费时间")
    print("{:.6f}".format(front_cpt_end_time - front_cpt_start_time))

    print("降低分析等级花费时间")
    print("{:.6f}".format(up_level_end_time - up_level_start_time))

    print("合并概念花费时间")
    print("{:.6f}".format(combine_end_time - combine_start_time))

    print("所有概念花费时间：")
    print("{:.6f}".format(all_cpt_end_time - all_cpt_start_time))



#  合并成功
if __name__ == "__main__":
    main()
