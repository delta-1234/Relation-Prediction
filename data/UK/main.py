import pandas as pd
import numpy as np

csv_path = './UK Road Safety Data - accidents 2021.csv'

context = pd.read_csv(csv_path, low_memory=False)
accident = context['accident_index'][:10000].tolist()
date = context['date'][:10000].tolist()
time = context['time'][:10000].tolist()
road_type = context['road_type'][:10000].tolist()
light = context['light_conditions'][:10000].tolist()
weather = context['weather_conditions'][:10000].tolist()

for i in range(len(accident)):
    accident[i] = str(accident[i])
    road_type[i] = "road_type" + str(road_type[i])
    light[i] = "light" + str(light[i])
    weather[i] = "weather" + str(weather[i])

re = []
head = accident * 5 + date
re_name = ["发生的日期", "发生的时间", "路面状况", "光照", "天气", "日期对应时间"]
for i in range(0, 6):
    for j in range(len(accident)):
        re.append(re_name[i])
tail = date + time + road_type + light + weather + time

entity = []
relation = []
triple = []

print(len(head))
print(len(tail))
print(len(re))
# for i in range(0, len(re)):
#     if not any(np.array_equal([head[i], re[i], tail[i]], e) for e in triple):
#         triple.append([head[i], re[i], tail[i]])
#     if not any(np.array_equal(head[i], e) for e in entity):
#         entity.append(head[i])
#     if not any(np.array_equal(tail[i], e) for e in entity):
#         entity.append(tail[i])
#     if not any(np.array_equal(re[i], e) for e in entity):
#         relation.append(re[i])
#     print(i)
# print(triple)
for i in range(0, len(re)):
    triple.append([head[i], re[i], tail[i]])
    if head[i] not in entity:
        entity.append(head[i])
    if tail[i] not in entity:
        entity.append(tail[i])
    if re[i] not in relation:
        relation.append(re[i])
    print(i)
print(triple)

with open('entity2id.txt', 'w') as f1:
    f1.write(str(len(entity)) + "\n")
    for i in range(len(entity)):
        f1.write(str(entity[i]) + " " + str(i) + "\n")

with open('relation2id.txt', 'w') as f1:
    f1.write(str(len(relation)) + "\n")
    for i in range(len(relation)):
        f1.write(str(relation[i]) + " " + str(i) + "\n")

tr_num = 0
v_num = 0
ts_num = 0
with open('train.txt', 'w') as tr:
    with open('valid.txt', 'w') as v:
        with open('test.txt', 'w') as ts:
            for i in range(len(triple)):
                temp = str(triple[i][0]) + " " + str(triple[i][1]) + " " + str(triple[i][2])
                if i % 10 == 0:
                    v.write(temp + "\n")
                    v_num += 1
                elif i % 10 == 9:
                    ts.write(temp + "\n")
                    ts_num += 1
                else:
                    tr.write(temp + "\n")
                    tr_num += 1

with open('train2id.txt', 'w') as tr:
    tr.write(str(tr_num) + "\n")
    with open('valid2id.txt', 'w') as v:
        v.write(str(v_num) + "\n")
        with open('test2id.txt', 'w') as ts:
            ts.write(str(ts_num) + "\n")
            for i in range(len(triple)):
                temp = str(entity.index(triple[i][0])) + " " + str(entity.index(triple[i][2])) + " " + \
                       str(relation.index(triple[i][1]))
                if i % 10 == 0:
                    v.write(temp + "\n")
                elif i % 10 == 9:
                    ts.write(temp + "\n")
                else:
                    tr.write(temp + "\n")

h = []
t = []
with open('type_constrain.txt', 'w') as tc:
    tc.write(str(len(relation)) + "\n")
    for i in relation:
        for j in triple:
            if j[1] == i:
                if j[0] not in h:
                    h.append(j[0])
                if j[2] not in t:
                    t.append(j[2])
        tc.write(str(relation.index(i)) + " ")
        for j in h:
            tc.write(str(entity.index(j)) + " ")
        tc.write("\n")
        tc.write(str(relation.index(i)) + " ")
        for j in t:
            tc.write(str(entity.index(j)) + " ")
        tc.write("\n")
