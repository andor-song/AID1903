##AID1903 git 学习

> 学习内容包括git 和 github

> 加油
# 1. randrange() 方法返回指定递增基数集合中的一个随机数，基数缺省值为1

# import random
# random.randrange ([start,] stop [,step])
# start -- 指定范围内的开始值，包含在范围内。
# stop -- 指定范围内的结束值，不包含在范围内。
# step -- 指定递增基数。

import random
# 输出 100 <= number < 1000 间的偶数
print("randrange(100, 1000, 2) : ", random.randrange(100, 1000, 2))
# 输出 100 <= number < 1000 间的以3为步长数
print("randrange(100, 1000, 3) : ", random.randrange(100, 1000, 3))
# 在结果上与 random.choice(range(100, 1000, 3) 等效
print("randrange(100, 1000, 3) : ", random.choice(range(100, 1000, 3)))

#2.在列表内找出一个数组最小与次小&最大与次大的2个数
if __name__ == '__main__':
    # 加入一个变量m2，每次比较后m1会变小，那我们每次比较后给m1赋值前把前一个m1给赋值给m2是不是可以呢？
    L = [6, 4, 7, 3, 7, 2, 9, 3, 5, 3]
    m1 = m2 = L[0]
    for x in range(0, len(L)):
        if m1 > L[x]:
            m2 = m1
            m1 = L[x]
    print(m1, m2)  #换组数据，会出现bug

    L = [9,8,7,5,4,2,3]
    m1 = m2 = L[0]
    for x in range(0, len(L)):
        if m1 > L[x]:
            m2 = m1
            m1 = L[x]
    print(m1, m2)#当第二小数值在最小值之后,存在bug,结果：2,4
    # m2值的改变是依赖于后面有比m1小的数，如果是图上这种2在1后面的情况，m1跳过了和1的比较，所以我们还需要给m2加一个比较过程。


    L = [9, 8, 7, 5, 4, 2, 3]
    m1 = m2 = L[0]
    for x in range(0, len(L)):
        if m1 > L[x]:
            m2 = m1
            m1 = L[x]
        elif m2 > L[x]:
            m2 = L[x]
    print(m1, m2) #换组数据，存在bug

    L = [ 2, 3, 4, 5, 6, 7]
    m1 = m2 = L[0]
    for x in range(0, len(L)):
        if m1 > L[x]:
            m2 = m1
            m1 = L[x]
        elif m2 > L[x]:
            m2 = L[x]
    print(m1, m2) #当最小值在第一位时，m1=m2=L[0]，进行后续if判断将不再变动


    # 最终结果：最小2个
    # 把m1和m2的初始值变成一个极大的数
     L = [1, 2, 3, 4, 5, 6, 7]
     m1 = m2 = float('inf')
     for x in range(0, len(L)):
         if m1 > L[x]:
             m2 = m1
             m1 = L[x]
         elif m2 > L[x]:
             m2 = L[x]
     print(m1, m2)
    #
    # # 最终结果：最大2个
    # # 把m1和m2的初始值变成一个极小的数
     L = [8, 2, 3, 4, 5, 6, 7]
     m1 = m2 = float('-inf')
     for x in range(0, len(L)):
         if m1 < L[x]:
             m2 = m1
             m1 = L[x]
         elif m2 < L[x]:
             m2 = L[x]
     print(m1, m2)
    #
    # # 备注：
    # # Python中可以用如下方式表示正负无穷：
     print(float("inf"))
     print(float("-inf"))
    #
    # # 利用inf做简单加、乘算术运算仍会得到inf
     print(1 + float('inf'))
     print(2 * float('inf'))
    #
    # # 但是利用inf乘以0会得到not -a - number(NaN)：
     print(0 * float("inf"))
    #
    # # 除了inf外的其他数除以inf，会得到0
     print(889 / float('inf'))
     print(float('inf') / float('inf'))
    #
    # # 不等式： 当涉及 > 和 < 运算时， 所有数都比 - inf大 所有数都比 + inf小
    # # 等式： +inf和 + inf相等 - inf和 - inf相等