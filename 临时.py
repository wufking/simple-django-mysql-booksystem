# n = 9
# pastjob = {1:0,2:0,3:0,4:1,5:3,6:1,7:4,8:6}
# v = {1:5,2:1,3:7,4:5,5:3,6:8,7:2,8:4}
# maxVMemo = {0:0,1:5}
#
# for i in range(2,n):
#     choose = v[i] + maxVMemo[pastjob[i]]
#     not_choose = maxVMemo[i-1]
#     maxVMemo[i] = max(choose,not_choose)
#
# print(maxVMemo[n-1]) # 17
#
# #声明状态空间S=[0.1...151
# S=[s for s in range(16)]
# #声明行动空间
# A=['e','s','n']
# #初始化状态值函数
# Vs = [0 for _ in range(16)]
# #折现因子
# gamma = 1.0
# #用字典存储各个状态的下一时刻状态空间
# nextStates= {0: [0], 15: [15]}
# for i in range(1, 15):
#     nextStates[i]=[]
#     if i in [0,15]:
#         nextStates[i].append(i)
#     for a in A:
#         actValue={'e': 1, 's': 4, 'w':-1,'n':-4}
#         if ((i+1)%4==0 and a=='e') or (i>11 and a=='s')\
#         or (i%4==0 and a=='w') or (i<4 and a=='n'):
#             nextStates[i].append(i)
#         else:
#             nextStates[i]. append(i + actValue[a])
# print (nextStates)
#
# #选代函数
# def iterationFunc():
#     global Vs
#     for i in range(16):
#         print('{:>5.2f}'.format(Vs[i]), end='')
#         if(i+1)%4 ==0:
#             print('')
#     newVs =[0 for _ in range(16)]
#     for s in S:
#         newVs[s] = newVsFunc(s)
#     Vs = newVs
#
# def newVsFunc(s):
# #奖成函数
#     reward =-1
#     if s in [0, 15]:
#         reward =0
#     #根据公式4.5求解
#     newValue = 0.00
#     for next_s in nextStates[s]:
#         newValue += 1.00/4 * (reward + gamma * Vs[next_s])
#     return newValue
#
# def main():
#     maxIter = 160
#     i=0
#     while i<= maxIter:
#         print(f'Iteration {i}:')
#         iterationFunc()
#         i += 1
# if __name__ == '__main__':
#     main()
#
# a = [1, 2, 3]
# b = a
# b.pop()
# print(a)

# from django import http
# print(http.__all__)