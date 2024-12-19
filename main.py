import argparse
import pandas as pd
import numpy as np
import time

"""
This method should read the contents of the preferences.xlsx file.
"""
def read_file(path):
    data = pd.read_excel(path);
    a = np.zeros([data.shape[0], data.shape[0]])

    likes = data[["L1", "L2", "L3", "L4", "L5"]]
    dislikes = data[["D1", "D2", "D3", "D4", "D5"]]
    for p in range(data.shape[0]):
        for like in likes.values[p]:
            id = 0
            for name in data["Name"]:
                if like == name:
                    a[p][id] = 1
                id += 1 
        for dislike in dislikes.values[p]:
            id = 0
            for name in data["Name"]:
                if dislike == name:
                    a[p][id] = -1
                id += 1
    
    return data["Name"], a

"""
This method should build the groups based on the preferences and the group sizes.
Each person should only be in one group.
Each group should have the size specified in the group_sizes list.
"""
def build_groups(persons, preferences, group_sizes):
    groups = np.zeros([len(group_sizes), preferences.shape[0]])
    group_index = 0
    for i in range(len(persons)):
        group = groups[group_index]
        if sum(group) < group_sizes[group_index]:
            group[i] = 1
        else:
            group_index += 1
            group = groups[group_index]
            group[i] = 1



    return groups

def calculate_score(groups, preferences):
    score = 0
    for i in range(len(groups)):
        group_score = 0
        for j in range(len(groups[i])):
            if groups[i][j] == 1:
                group_score += np.matmul(preferences[j], groups[i]).sum()
        score += group_score
    return score

"""
Randomly swap students between groups, but be aware of the group sizes. Swap only 1 and 1.
"""
def mutate_groups(groups):
    group1 = 0
    group2 = 0

    while group1 == group2:
        group1 = np.random.randint(0, len(groups))
        group2 = np.random.randint(0, len(groups))

    person1 = 0
    person1_id = 0
    person2 = 0
    person2_id = 0
    while person1 == 0 or person2 == 0:
        person1_id = np.random.randint(0, len(groups[group1]))
        person1 = groups[group1][person1_id]
        person2_id = np.random.randint(0, len(groups[group2]))
        person2 = groups[group2][person2_id]

    groups[group1][person1_id] = 0
    groups[group2][person2_id] = 0
    groups[group1][person2_id] = 1
    groups[group2][person1_id] = 1

    return groups


def output(persons, preferences, groups, score):
    print("Score: ", score)
    for i in range(len(groups)):
        print("Group", i)
        group_score = 0
        for j in range(len(groups[i])):
            if groups[i][j] == 1:
                score = np.matmul(preferences[j], groups[i]).sum()
                group_score += score
                print(persons[j] + " " + str(score))
        print("Score: " + str(group_score))
        print("")

parser = argparse.ArgumentParser("Group Preference Splitter")
parser.add_argument("path", metavar="P", type=str)
parser.add_argument("-g", "--group", type=int, nargs="+")
parser.add_argument("-t", "--time", type=int, default=60)

args = parser.parse_args()
persons, preferences = read_file(args.path)
groups = build_groups(persons, preferences, args.group)
start_time = time.time()

best_groups = None
best_score = -1
while time.time() - start_time < args.time:
    groups = mutate_groups(groups.copy())
    score = calculate_score(groups, preferences)
    if score > best_score:
        best_groups = groups
        best_score = score
        print("New best score: " + str(best_score))
output(persons, preferences, best_groups, best_score)

