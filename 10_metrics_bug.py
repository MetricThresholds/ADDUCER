#!/usr/bin/env python
# encoding:utf-8
"""
Date : 2021/10/7
Time: 10:16
File: metrics_bug.py

Merge the data of each metric and its bug's number.

Steps: 1. read the metrics dataframe and increase an field of "bug".
       2. read the corresponding file of bug dataframe.
       3. merge the two dataframe into one dataframe with the same File field.

       Mapping of two metrics file's fields
          metrics_dataframe            bug_metrics
          relName (File)———————————————file

Notes: the directory in relName(File) is \, while in file is /. So, it needs to convert into the same format.
e.g.   the file in relName field is
           components\camel-mllp\src\main\java\org\apache\camel\component\mllp\MllpAcknowledgementException.java
       the file in file filed is
           components/camel-mllp/src/main/java/org/apache/camel/component/mllp/MllpAcknowledgementException.java
       In fact, they are the same file in two dataframe.
"""


def metrics_bug_merge(metric_Dir, bug_Dir, result_Dir):

    metric_dir = metric_Dir
    bug_dir = bug_Dir
    results_dir = result_Dir

    import os
    import pandas as pd

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 10000)

    # results_dir = "/home/mei/PycharmProjects/OOM/merged_metrics/merged_metrics/"

    with open(results_dir + "List.txt") as List:
        lines = List.readlines()

    for line in lines:
        file = line.replace("\n", "")
        project = file.split("-")[0]
        print("the file is ", file)
        print("the project is ", project)

        # if file != "camel-2.11.0.csv":
        #     continue

        if not os.path.exists(results_dir + project):
            os.mkdir(results_dir + project)

        metric_df = pd.read_csv(metric_dir + project + '\\uperl_und_' + file, sep=",", header=0, index_col=False)
        # print("the len of metric_df is ", len(metric_df))
        # metric_df = metric_df.relName.drop_duplicates()
        # print("the len of metric_df is ", len(metric_df))
        # uperl_df = uperl_df.drop_duplicates()
        bug_df = pd.read_csv(bug_dir + project + '\\' + file, sep=",", header=0, index_col=False)
        merged_df = pd.DataFrame(columns=list(metric_df.columns) + ["bug"])
        duplicated_metric_df = pd.DataFrame(columns=list(metric_df.columns))
        print(" the columns of merged_df is ", merged_df.columns)
        print(" the len of bug_df is ", len(bug_df))
        print(" the count of file field bug_df is ", len(bug_df.file.values))
        print(" the count file field bug_df is ", len(set(bug_df.file.values)))
        print(" the count of relName field is ", len(metric_df.relName.values))
        print(" the count of relName field set is ", len(set(metric_df.relName.values)))
        print(" the count of relName field is ", len(bug_df.file.values))
        print(" the count of relName field set is ", len(set(bug_df.file.values)))

        print(os.getcwd())
        os.chdir(results_dir)
        print(os.getcwd())

        for i in range(len(metric_df)):
            file_name = metric_df.loc[i, "relName"]
            class_name = metric_df.loc[i, "className"]
            bug_value = 0

            # if the file name is not identical to the class name,  remove the row to duplicated_metric_df.
            if file_name.split("\\")[-1].split(".")[0] != class_name.split(".")[-1]:
                print("the file_name is ", file_name.split("\\")[-1].split(".")[0], class_name.split(".")[-1])
                duplicated_metric_df = duplicated_metric_df.append(metric_df[i:i+1], ignore_index=True)
                # merged_df.loc[i, "bug"] = bug_value
                # continue

            for j in range(len(bug_df)):
                bug_file_name = bug_df.loc[j, "file"].replace("/", "\\")

                if file_name == bug_file_name:
                    print(file_name, bug_file_name)
                    print(file_name == bug_file_name)
                    bug_value += 1
            print(i, " The file_name is ", file_name, " the bug_value is ", bug_value)
            for metric_column in metric_df.columns.values:
                merged_df.loc[i, metric_column] = metric_df.loc[i, metric_column]
            merged_df.loc[i, "bug"] = bug_value

        if not os.path.exists(results_dir + project):
            os.mkdir(results_dir + project)

        duplicated_metric_df.to_csv(results_dir + project + '\\' + "duplicated_" + file, sep=',', header=True,
                                    index=False)
        merged_df.to_csv(results_dir + project + '\\' + "merged_" + file, sep=',', header=True, index=False)


if __name__ == '__main__':
    import os
    import sys
    import time
    import pandas as pd

    s_time = time.time()
    bugDir = "E:\\PycharmProjects\\Jira\\DefectData\\"
    metricDir = "E:\\PycharmProjects\\Jira\\Metrics\\merged\\"
    resultDir = "E:\\PycharmProjects\\Jira\\Metrics\\metricsBugs\\"
    os.chdir(resultDir)

    metrics_bug_merge(metricDir, bugDir, resultDir)

    e_time = time.time()
    execution_time = e_time - s_time

    print("The __name__ is ", __name__, ". From ", time.asctime(time.localtime(s_time)), " to ",
          time.asctime(time.localtime(e_time)), ", this", os.path.basename(sys.argv[0]), "ended within", execution_time,
          "(s), or ", (execution_time / 60), " (m).")
