#!/usr/bin/env python
# encoding:utf-8
"""
Date : 2021/10/29
Time: 22:23
File: P_average.py

Compute the average P value of each project.

"""


def average_P(directory):
    AVs_dir = directory + "affectedVersions\\"
    coldStartP_dir = directory + "affectedVersions\\coldStartP\\"
    average_dir = directory + "affectedVersions\\averageP\\"

    # display all columns and rows, and set the item of row of dataframe
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 5000)

    with open(AVs_dir + "List_76.txt") as l_all:
        lines_all = l_all.readlines()

    average_P_file = pd.DataFrame(columns=["project", "averageP", "countP", 'stdP', 'maxP', 'medianP',
                                           'minP', 'firstP', 'firstPcount', 'secondP', 'secondPcount', 'thirdP',
                                           'thirdPcount'])

    for line in lines_all:
        file = line.replace("\n", "")
        print(file)
        df_coldStartP = pd.read_csv(coldStartP_dir + file + "_coldStartP.csv", index_col=False)
        print(df_coldStartP.head())
        print(df_coldStartP.columns.values)
        print(df_coldStartP['P'].mean())
        print(df_coldStartP['P'].count())
        print(df_coldStartP['P'].std())
        print(df_coldStartP['P'].max())
        print(df_coldStartP['P'].min())
        print(df_coldStartP['P'].median())
        print(df_coldStartP['P'].value_counts())
        print(len(df_coldStartP['P'].value_counts()))
        key_1, key_2, key_3, value_1, value_2, value_3 = 0, 0, 0, 0, 0, 0
        if len(df_coldStartP['P'].value_counts()) > 2:
            k = 0
            for key, value in df_coldStartP['P'].value_counts().items():
                print(key, value)
                k += 1
                if k == 1:
                    key_1 = key
                    value_1 = value
                elif k == 2:
                    key_2 = key
                    value_2 = value
                elif k == 3:
                    key_3 = key
                    value_3 = value
                else:
                    break

        average_P_file = average_P_file.append({'project': file, 'averageP': df_coldStartP['P'].mean(),
                                                'countP': df_coldStartP['P'].count(), 'stdP': df_coldStartP['P'].std(),
                                                'maxP': df_coldStartP['P'].max(),
                                                'medianP': df_coldStartP['P'].median(),
                                                'minP': df_coldStartP['P'].min(), 'firstP': key_1,
                                                'firstPcount': value_1, 'secondP': key_2, 'secondPcount': value_2,
                                                'thirdP': key_3, 'thirdPcount': value_3}, ignore_index=True)
        # break

    average_P_file.to_csv(average_dir + "averageP.csv", index=False)
    # .remove(average_P_file.loc[i, 'averageP'])
    col_name = average_P_file.columns.tolist()
    col_name.insert(1, 'coldStartP')
    average_P_file = average_P_file.reindex(columns=col_name)
    # average_P_file['coldStartP'] = [np.median(list(set(average_P_file['averageP'].tolist())
    #                                 - set(average_P_file['averageP'].tolist()[i]))) for i in range(len(average_P_file))]
    average_P_file['coldStartP'] = [np.median(average_P_file['averageP'].tolist()[0:i] +
                                    average_P_file['averageP'].tolist()[i+1:]) for i in range(len(average_P_file))]
    average_P_file.to_csv(average_dir + "averageP_coldStartP.csv", index=False)


if __name__ == '__main__':

    import os
    import sys
    import time
    import random
    import shutil
    from datetime import datetime
    import pandas as pd
    import numpy as np

    s_time = time.time()

    Directory = "F:\\defectData\\"
    os.chdir(Directory)

    average_P(Directory)

    e_time = time.time()
    execution_time = e_time - s_time

    print("The __name__ is ", __name__, ".\nFrom ", time.asctime(time.localtime(s_time)), " to ",
          time.asctime(time.localtime(e_time)), ",\nthis", os.path.basename(sys.argv[0]), "ended within",
          execution_time,
          "(s), or ", (execution_time / 60), " (m).")
