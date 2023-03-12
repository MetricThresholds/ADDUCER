#!/usr/bin/env python
# encoding:utf-8
"""
Date : 2021/10/26
Time: 18:24
File: P_MovingWindow.py

Label Affected versions and corresponding classes of a project with bug information (bug ID in issue tracker, Jira).

Reference:
     Vandehei, B., et al. (2021). "Leveraging the Defects Life Cycle to Label Affected Versions and Defective Classes."
            ACM Trans. Softw. Eng. Methodol. 30(2): Article 24.
"""


def cold_start(directory):
    commitDate_dir = directory + "commitDate\\"
    commitFile_dir = directory + "commitFile\\"
    versionDate_dir = directory + "versionDate\\"
    bug_report_dir = directory + "Jira\\"
    AVs_dir = directory + "affectedVersions\\"
    coldStartP_dir = directory + "affectedVersions\\coldStartP\\"
    bugCommitFile_dir = directory + "affectedVersions\\bugCommitFile\\"

    # display all columns and rows, and set the item of row of dataframe
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 5000)

    with open(AVs_dir + "List_76.txt") as l_all:
        lines_all = l_all.readlines()

    for line in lines_all:
        file = line.replace("\n", "")
        # if file != 'STDCXX':
        #     continue
        print(file)
        # 如果文件不规则，行尾有分隔符，则可以设定index_col = False 来是的pandas不适用第一列作为行索引。
        df_bug = pd.read_csv(bug_report_dir + file + ".csv", index_col=False)
        df_commitFile = pd.read_csv(commitFile_dir + file + ".csv", index_col=False)
        print(df_commitFile.head())
        print(df_commitFile.columns.values)
        df_versionDate = pd.read_csv(versionDate_dir + file + "_versionDate.csv", index_col=False)
        df_commitDate_tmp = pd.read_csv(commitDate_dir + file + ".csv", header=None, sep='\n')
        # df_commitDate = df_commitDate[0].str.split(',', expand=True)
        df_commitDate = pd.DataFrame(columns=['commit', 'date', 'title'])
        for item in range(len(df_commitDate_tmp)):
            df_commitDate.loc[item, 'commit'] = df_commitDate_tmp.loc[item, 0].split(',')[0]
            df_commitDate.loc[item, 'date'] = df_commitDate_tmp.loc[item, 0].split(',')[1]
            df_commitDate.loc[item, 'title'] = df_commitDate_tmp.loc[item, 0].split(',')[2:]
        # print(df_commitDate)
        # print(len(df_commitDate))
        print(df_commitDate.columns.values)
        # print(df_versionDate)
        # print(df_bug.index)
        print(df_bug.columns.values)
        print(df_versionDate.columns.values)
        # print(df_bug._stat_axis.values)
        # print(df_bug.shape[0])
        # print(df_bug.shape[1])
        print(len(df_bug))
        coldStartP_file = pd.DataFrame(columns=["Project", "BugID", "IV", "OV", "FV", "P", "IVid", "OVid", "FVid"])
        bugCommitFile_file = pd.DataFrame(columns=["BugID", "commitID", "files"])
        for i in range(len(df_bug)):
            # print(df_bug.loc[i, 'AffectsVersions'])
            # print(df_bug.loc[i, 'AffectsVersions'] is np.nan)

            if df_bug.loc[i, 'AffectsVersions'] is np.nan:
                # print(df_bug.loc[i, 'AffectsVersions'])
                continue

            Project = df_bug.loc[i, 'ProjectKey']
            BugID = df_bug.loc[i, 'Key']
            IVid = df_bug.loc[i, 'AffectsVersions'].split("|")[0]
            # print(df_bug.loc[i, 'CreatedDate'])
            CreatedDate_bug = datetime.strptime(df_bug.loc[i, 'CreatedDate'],
                                                "%Y-%m-%dT%H:%M:%S.000+0000").strftime("%Y-%m-%dT%H:%M:%S")
            ResolutionDate_bug = datetime.strptime(df_bug.loc[i, 'ResolutionDate'],
                                                   "%Y-%m-%dT%H:%M:%S.000+0000").strftime("%Y-%m-%dT%H:%M:%S")
            # print(CreatedDate_bug)
            versions_in_Date = df_versionDate['name'].values.tolist()
            # print(versions_in_Date)

            # commits should be in BUG id time between CreatedDate_bug and ResolutionDate_bug
            commitDate_list = []
            commit_list = []
            for item_commit in range(len(df_commitDate)):
                title_list = df_commitDate.loc[item_commit, 'title']
                title_date = datetime.strptime(df_commitDate.loc[item_commit, 'date'][:-6],
                                               "%a %b %d %H:%M:%S %Y").strftime("%Y-%m-%dT%H:%M:%S")
                if title_date < CreatedDate_bug or title_date > ResolutionDate_bug:
                    continue
                for title in title_list:
                    if BugID in title:
                        # print(df_commitDate.loc[item_commit, 'date'][:-6])
                        commitDate_list.append(title_date)
                        commit_list.append(df_commitDate.loc[item_commit, 'commit'])
                        break
            # print(BugID, IVid)
            # bug id time interval ([Created,ResolutionDate]) does not including any commit which includes the BUG id.
            if len(commitDate_list) == 0:
                continue
            else:
                last_commitDate = max(commitDate_list)
            # print(commitDate_list)
            # print(max(commitDate_list))
            # print(commit_list)
            for item_commitFile in range(len(df_commitFile)):
                commitID = df_commitFile.loc[item_commitFile, 'commitID']
                commitFile = df_commitFile.loc[item_commitFile, 'files']
                if commitID in commit_list:
                    bugCommitFile_file = bugCommitFile_file.append({'BugID': BugID, 'commitID': commitID,
                                                                    'files': commitFile}, ignore_index=True)
            P = 0
            FV = 0
            if IVid in versions_in_Date:
                # print(df_versionDate.loc[:, :])
                # print(df_versionDate[df_versionDate['name'] == IVid].loc[:, 'index'])
                # print(type(df_versionDate[df_versionDate['name'] == IVid].loc[:, 'index'].values.tolist()[0]))
                IV = df_versionDate[df_versionDate['name'] == IVid].loc[:, 'index'].values.tolist()[0]
                # print(IV, IVid)
                OV = 0
                for j in range(len(versions_in_Date)):
                    versionDate = df_versionDate.loc[j, 'Date']
                    versionDate = datetime.strptime(versionDate, "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%dT%H:%M:%S")
                    # print(CreatedDate_bug, last_commitDate, versionDate, ResolutionDate_bug)
                    # print(CreatedDate_bug > versionDate)
                    # OV
                    if CreatedDate_bug > versionDate:
                        continue
                    else:
                        if OV == 0:
                            OV = df_versionDate.loc[j, 'index']
                            OVid = df_versionDate.loc[j, 'name']
                            # print(IV, IVid, OV, OVid)
                    # judge its consistent, if IV <= OV, namely exclude the non post-release
                    if IV > OV:
                        with open(coldStartP_dir + file + "_coldStartP_IV_lost.txt", 'a', encoding='utf-8') as fw:
                            fw.write(Project + "," + BugID + "," + str(IV) + ",(" + IVid + "), is larger than OV\n")
                        break

                    # if ResolutionDate_bug > versionDate:
                    if last_commitDate > versionDate:
                        continue
                    else:
                        FV = df_versionDate.loc[j, 'index']
                        FVid = df_versionDate.loc[j, 'name']
                        # print(IV, IVid, OV, OVid, FV, FVid)
                    # P = (FV - IV) / (FV - OV)
                    if FV != OV:
                        P = (FV - IV) / (FV - OV)
                    else:
                        P = FV - IV
                    break

            else:
                with open(coldStartP_dir + file + "_coldStartP_IV_lost.txt", 'a', encoding='utf-8') as fw:
                    fw.write(Project + "," + BugID + "," + IVid + "," + CreatedDate_bug + ", is not in versions\n")
                continue

            if P != 0 and IV <= OV:
                print(Project, BugID, IV, OV, FV, P)
                coldStartP_file = coldStartP_file.append({'Project': Project, 'BugID': BugID, 'IV': IV, 'OV': OV,
                                                          'FV': FV, 'P': P, 'IVid': IVid, 'OVid': OVid, 'FVid': FVid},
                                                           ignore_index=True)
            # break

        # print(coldStartP_file)
        coldStartP_file.to_csv(coldStartP_dir + file + "_coldStartP.csv", index=False)
        bugCommitFile_file.to_csv(bugCommitFile_dir + file + "_bugCommitFile.csv", index=False)
        # break


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
    # 1. clone 76 repositories, done!
    # clone_repository(Directory)
    # 2. number the versions of projects beginning with the oldest version as version 1.
    # number_version(Directory)
    # 3. git log the commit date and files of each BUG ID, done！
    # commit_file_date(Directory)
    # 4. using moving window method to label AVs of BUG ID which the bug report does not supply.
    cold_start(Directory)

    e_time = time.time()
    execution_time = e_time - s_time

    print("The __name__ is ", __name__, ".\nFrom ", time.asctime(time.localtime(s_time)), " to ",
          time.asctime(time.localtime(e_time)), ",\nthis", os.path.basename(sys.argv[0]), "ended within",
          execution_time,
          "(s), or ", (execution_time / 60), " (m).")
