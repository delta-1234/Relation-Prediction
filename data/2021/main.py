import pandas as pd

csv_path = './data2021.csv'

context = pd.read_csv(csv_path)
re = context['relation']
head = context['head']
tail = context['tail']
entity = []
relation = []
triple = []
# print(head)
for i in range(0, len(re)):
    if [head[i], re[i], tail[i]] not in triple:
        triple.append([head[i], re[i], tail[i]])
    if head[i] not in entity:
        entity.append(head[i])
    if tail[i] not in entity:
        entity.append(tail[i])
    if re[i] not in relation:
        relation.append(re[i])

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
