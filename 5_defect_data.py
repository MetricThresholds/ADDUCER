#!/usr/bin/env python
# encoding:utf-8
"""
Date : 2021/9/26
Time: 19:46
File: defect_data.py

Divide the bug files into each version of a project.

"""


def defects_version(working_Dir, result_Dir):

    from datetime import datetime
    workingDirectory = working_Dir
    resultDirectory = result_Dir

    with open(resultDirectory + "BugList.txt") as l:
        lines = l.readlines()

    print("the len lines is ", len(lines))

    for line in lines:
        file = line.replace("\n", "")
        print("the file is ", file)
        project = file.split("_")[0]
        print("the project is ", project)
        release_file = project.lower() + "_release_date.csv"
        print("the release_file is ", release_file)

        if not os.path.exists(resultDirectory + project):
            os.mkdir(resultDirectory + project)

        # display all columns and rows, and set the item of row of dataframe
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.width', 5000)

        # read a file to get the time interval of a certain bug
        bug_df = pd.read_csv(workingDirectory + "BugFiles_results\\" + file, error_bad_lines=False, header=0,
                             index_col=False)
        print(bug_df.columns.values)

        # read a release time to compare the
        release_df = pd.read_csv(workingDirectory + "ReleaseFiles\\" + release_file, error_bad_lines=False,
                                 header=0, index_col=False)

        for i in range(len(bug_df)):
            # print(i, bug_df.loc[i, "CreatedDate"][0:19], bug_df.loc[i, "ResolutionDate"][0:19],
            #       bug_df.loc[i, "AffectsVersions"], type(bug_df.loc[i, "CreatedDate"]),
            #       type(bug_df.loc[i, "ResolutionDate"]), type(bug_df.loc[i, "AffectsVersions"]))
            CreatedDate = datetime.strptime(bug_df.loc[i, "CreatedDate"][0:19].replace("T", " "), "%Y-%m-%d %H:%M:%S")
            ResolutionDate = datetime.strptime(bug_df.loc[i, "ResolutionDate"][0:19].replace("T", " "),
                                               "%Y-%m-%d %H:%M:%S")
            # print(i, CreatedDate, ResolutionDate)

            for j in range(len(release_df)):

                release_date = datetime.strptime(release_df.loc[j, "release_date"][0:19].replace("T", " "),
                                                 "%Y-%m-%d %H:%M:%S")
                version_file = release_df.loc[j, "release_name"]
                # print(j, release_df.loc[j, "release_name"], release_df.loc[j, "release_date"], release_date)
                # if (release_date > CreatedDate) and (release_date < ResolutionDate):
                #     print("This bug file is on the current version!")
                #     print(i, j, release_df.loc[j, "release_name"], CreatedDate, release_date, ResolutionDate,
                #           bug_df.loc[i, "AffectsVersions"], bug_df.loc[i, "FixedVersions"])
                #
                #     # release_date = release_df.loc[j, "release_date"]
                #
                #     with open(resultDirectory + project + "\\" + version_file + ".csv", 'a+', encoding="utf-8",
                #               newline='') as f:
                #         writer = csv.writer(f)
                #         if os.path.getsize(resultDirectory + project + "\\" + version_file + ".csv") == 0:
                #             writer.writerow(np.append(bug_df.columns.values, "release_date"))
                #         writer.writerow(np.append(bug_df.loc[i, :].values, release_date))
                # else:
                AffectsVersions = bug_df.loc[i, "AffectsVersions"]
                print("the type of AffectsVersions is ", AffectsVersions)
                # print("the type of AffectsVersions is ", type(AffectsVersions))
                # print("the type of AffectsVersions is ", type(str(AffectsVersions)))
                if "nan" in str(AffectsVersions):
                    print("the nan is in AffectsVersions!", AffectsVersions)
                    continue

                AffectsVersions = str(AffectsVersions).split("|")
                # print("the AffectsVersions AffectsVersions is ", AffectsVersions)
                # print("the current version is ", release_df.loc[j, "release_name"])
                # print("the current version is ", "-".join(release_df.loc[j, "release_name"].split("-")[1:]))
                current_version = "-".join(release_df.loc[j, "release_name"].split("-")[1:])
                if current_version in AffectsVersions:
                    print("the AffectsVersions AffectsVersions is ", AffectsVersions)
                    print("the ", current_version, " is in ", AffectsVersions)
                    with open(resultDirectory + project + "\\" + version_file + ".csv", 'a+', encoding="utf-8",
                              newline='') as f:
                        writer = csv.writer(f)
                        if os.path.getsize(resultDirectory + project + "\\" + version_file + ".csv") == 0:
                            writer.writerow(np.append(bug_df.columns.values, "release_date"))
                        writer.writerow(np.append(bug_df.loc[i, :].values, release_date))


            # break


if __name__ == '__main__':

    import os
    import csv
    import sys
    import time
    import pandas as pd
    import numpy as np
    # from datetime import datetime
    import random
    import datetime

    s_time = time.time()
    workingDir = "E:\\PycharmProjects\\Jira\\"
    resultDir = "E:\\PycharmProjects\\Jira\\DefectData\\"
    os.chdir(workingDir)
    defects_version(workingDir, resultDir)
    e_time = time.time()
    execution_time = e_time - s_time

    print("The __name__ is ", __name__, ". From ", time.asctime(time.localtime(s_time)), " to ",
          time.asctime(time.localtime(e_time)), ", this", os.path.basename(sys.argv[0]), "ended within", execution_time,
          "(s), or ", (execution_time / 60), " (m).")
