#!/usr/bin/env python
# encoding:utf-8
"""
Date : 2021/10/26
Time: 20:13
File: git_commit.py

Retrieve the repository of each project to get the data time and the changed files of each commit
 corresponding to each BUG ID.
"""


def commit_file_date(directory):

    commitDate_dir = directory + "commitDate\\"
    commitFile_dir = directory + "commitFile\\"
    Repository_dir = directory + "Repository\\"

    # display all columns and rows, and set the item of row of dataframe
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 5000)

    df = pd.read_csv(directory + "TopProjects_new.csv", header=None)
    # print(df)
    print(len(df))

    with open(commitDate_dir + "List_76.txt") as l_all:
        lines_all = l_all.readlines()

    for line in lines_all:
        file = line.replace("\n", "")
        print(file)
        print(df[df[0] == file].loc[:, 1].tolist()[0].split("/")[-1][:-4])
        file_dir = df[df[0] == file].loc[:, 1].tolist()[0].split("/")[-1][:-4]
        os.chdir(Repository_dir + file_dir + "\\")
        print(os.getcwd())
        com_Date = "git log --pretty=format:\"%H,%cd,%s\" --grep=\"" + file + "\" > " + commitDate_dir + file + ".csv"
        print(com_Date)
        os.system(com_Date)
        com_file = "git log --pretty=format:\"%H\" --name-only > " + commitFile_dir + "originalFile\\" + file + ".txt"
        print(com_file)
        os.system(com_file)
        with open(commitFile_dir + "originalFile\\" + file + ".txt") as commit_file:
            lines_commit_file = commit_file.readlines()
        # print(lines_commit_file)

        df_commit_file = pd.DataFrame(columns=["commitID", "files"])
        a_commit = []
        for line in lines_commit_file:
            print(line)
            if line != '\n':
                a_commit.append(line.replace("\n", ""))
                # print(a_commit)
            else:
                commitID = a_commit[0]
                print(df_commit_file.shape[0])
                for i in range(len(a_commit) - 1):
                    print(commitID, a_commit[i + 1])
                    df_commit_file.loc[df_commit_file.shape[0] + 1] = {'commitID': commitID, 'files': a_commit[i + 1]}
                    # df_commit_file.append([[commitID, a_commit[i + 1]]], ignore_index=True)
                a_commit = []
                # print(df_commit_file)
                # break
        print(df_commit_file)
        df_commit_file.to_csv(commitFile_dir + file + ".csv", index=False)
        break


if __name__ == '__main__':

    import os
    import sys
    import time
    import random
    import shutil
    import datetime
    import pandas as pd

    s_time = time.time()

    Directory = "F:\\defectData\\"
    os.chdir(Directory)
    commit_file_date(Directory)

    e_time = time.time()
    execution_time = e_time - s_time

    print("The __name__ is ", __name__, ".\nFrom ", time.asctime(time.localtime(s_time)), " to ",
          time.asctime(time.localtime(e_time)), ",\nthis", os.path.basename(sys.argv[0]), "ended within", execution_time,
          "(s), or ", (execution_time / 60), " (m).")