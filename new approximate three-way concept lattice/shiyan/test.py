from random import random


#  创建二维数组
def get_two_dimensional_array(n, m):
    a = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            rand = random()
            if 0 < rand < 0.33:
                a[i][j] += 1
            elif 0.66 <= rand < 1:
                a[i][j] -= 1
    return a


def main():
    N = 20
    M = 10

    a = get_two_dimensional_array(N, M)
    print(a)


if __name__ == '__main__':
    main()
