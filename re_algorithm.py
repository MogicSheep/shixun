from math import *
import csv
import pandas as pd
# movies = pd.read_csv("./movies.csv")
# ratings = pd.read_csv("./ratings.csv")##这里注意如果路径的中文件名开头是r，要转义。
# data = pd.merge(movies,ratings,on = 'movieId')#通过两数据框之间的movieId连接
# data[['userId','rating','movieId','title']].sort_values('userId').to_csv('./data.csv',index=False)
# !/usr/bin/env python
# encoding: utf-8



# print(data)


"""计算任何两位用户之间的相似度，由于每位用户评论的珠宝不完全一样，所以兽先要找到两位用户共同评论过的珠宝
       然后计算两者之间的欧式距离，最后算出两者之间的相似度
"""


def Euclidean(user1, user2, data):
    # 取出两位用户评论过的珠宝和评分
    user1_data = data[user1]
    user2_data = data[user2]
    distance = 0
    # 找到两位用户都评论过的珠宝，并计算欧式距离
    for key in user1_data.keys():
        if key in user2_data.keys():
            # 注意，distance越大表示两者越相似
            distance += pow(float(user1_data[key]) - float(user2_data[key]), 2)

    return 1 / (1 + sqrt(distance))  # 这里返回值越小，相似度越大


# 计算某个用户与其他用户的相似度
def top10_simliar(userID, data):
    res = []
    for userid in data.keys():
        # 排除与自己计算相似度
        if not userid == userID:
            simliar = Euclidean(userID, userid, data)
            res.append((userid, simliar))
    res.sort(key=lambda val: val[1])
    return res[:4]


# RES = top10_simliar('1')
# print(RES)


########################################################################
# 根据用户推荐珠宝给其他人
def recommend(user, data):
    # 相似度最高的用户
    top_sim_user = top10_simliar(user, data)[0][0]
    # 相似度最高的用户的观影记录
    items = data[top_sim_user]
    recommendations = []
    # 筛选出该用户未观看的珠宝并添加到列表中
    for item in items.keys():
        if item not in data[user].keys():
            recommendations.append((item, items[item]))
    recommendations.sort(key=lambda val: val[1], reverse=True)  # 按照评分排序
    # 返回评分最高的10部珠宝
    return recommendations[:10]

def get_re_list():
    file = open("./data/data.csv", 'r')  # 记得读取文件时加‘r’， encoding='UTF-8'
    # 读取data.csv中每行中除了名字的数据
    data = {}  # 存放每位用户评论的珠宝和评分
    for line in file.readlines():
        # 注意这里不是readline()
        line = line.strip().split(',')
        # 如果字典中没有某位用户，则使用用户ID来创建这位用户
        if not line[0] in data.keys():
            data[line[0]] = {line[3]: line[1]}
        # 否则直接添加以该用户ID为key字典中
        else:
            data[line[0]][line[3]] = line[1]
    return recommend("3", data)

'''
if __name__ == '__main__':
    Recommendations = get_re_list('3')
    recommend_id = []
    for item in Recommendations:
        recommend_id.append(item[0])
    print(recommend_id)
    print(Recommendations)
    #add_list(['1', '4', '3221', 'dsad'])
'''