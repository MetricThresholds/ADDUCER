# !/usr/bin python3
# encoding: utf-8
# @file: metric.py
# @time: 2020/9/21 5:49
"""

inputs: 1. a list file : one of projects' source versions;
        2. bug files :
        3. source codes :
        The name in three inputs need to be same.
outputs: metric files of one systems.

"""

import os
import csv
import numpy as np
import pandas as pd

working_dir = "/home/mei/PycharmProjects/OOM/metrics/"
source_codes_dir = "/home/mei/PycharmProjects/OOM/metrics/source_codes/"
bug_files_dir = "/home/mei/PycharmProjects/OOM/metrics/bug_files/"
result_dir = "/home/mei/PycharmProjects/OOM/metrics/und_result/"
List = "List.txt"

print(os.getcwd())
os.chdir(result_dir)
print(os.getcwd())

with open(result_dir + List) as L:
    lines = L.readlines()

for line in lines:
    file = line.replace("\n", "")
    print("the file is ", file)
    print("the file is ", file[:-4])

    # create .udb file
    udb_file = file[:-4] + ".udb"
    print(udb_file)
    if os.path.exists(source_codes_dir + udb_file):
        print("the udb file is created in last execution, so it will not be created this time.")
    else:
        com_1 = working_dir + "scitools/bin/linux64/und create -db " + source_codes_dir + udb_file + " -languages java"
        com_2 = working_dir + "scitools/bin/linux64/und -db " + source_codes_dir + udb_file + " add " + \
                source_codes_dir + file[:-4] + "/"
        com_3 = working_dir + "scitools/bin/linux64/und analyze -db " + source_codes_dir + udb_file

        print(repr(com_1))
        print(repr(com_2))
        print(repr(com_3))

        print(os.popen(com_1).read())
        print(os.popen(com_2).read())
        print(os.popen(com_3).read())

    # execute the und script
    csv_file = file[:-4] + ".csv"
    txt_output = file[:-4] + ".txt"
    print(csv_file)
    print(txt_output)

    if os.path.exists(result_dir + csv_file):
        print("the csv file is created in last execution, so will not be created this time.")
    else:
        # com_4 = working_dir + "scitools/bin/linux64/und purge " + udb_file
        # com_5 = working_dir + "scitools/bin/linux64/und analyze " + udb_file
        com_7 = working_dir + "scitools/bin/linux64/und settings -metricmetricsAdd all " + source_codes_dir + udb_file
        com_8 = working_dir + "scitools/bin/linux64/und settings -MetricFileNameDisplayMode RelativePath " + \
                source_codes_dir + udb_file
        com_9 = working_dir + "scitools/bin/linux64/und settings -MetricDeclaredInFileDisplayMode RelativePath " + \
                source_codes_dir + udb_file
        com_10 = working_dir + "scitools/bin/linux64/und settings -MetricShowDeclaredInFile on " + \
                 source_codes_dir + udb_file
        com_11 = working_dir + "scitools/bin/linux64/und settings -MetricShowFunctionParameterTypes on " + \
                 source_codes_dir + udb_file
        com_12 = working_dir + "scitools/bin/linux64/und metrics " + source_codes_dir + udb_file
                 # + " >> " + result_dir + txt_output
        #       + result_dir + csv_file + " > " + result_dir + txt_output
        # print(repr(com_4))
        # print(repr(com_5))
        print(repr(com_7))
        print(repr(com_8))
        print(repr(com_9))
        print(repr(com_10))
        print(repr(com_11))
        print(repr(com_12))
        print(os.popen(com_7).read())
        print(os.popen(com_8).read())
        print(os.popen(com_9).read())
        print(os.popen(com_10).read())
        print(os.popen(com_11).read())
        print(os.popen(com_12).read())
