import pandas as pd
import re


def readcsv(path):
    csvData = pd.read_csv(path)
    dfData = pd.DataFrame(csvData)
    print("Original data length is " + str(len(dfData) - 1))
    print("Column name is " + str([column for column in dfData]))
    print('Read complete')
    return dfData


def detectcsv(dfdata):
    n = len(dfdata)
    list = []
    for i in range(0, n):
        if dfdata.iloc[i, 0] == "id":
            list.append(i)
    print('Detect complete')
    return list


def modify(list, dfdata):
    data_after_unusual = dfdata.drop(labels=list, axis=0)
    data_after_duplicated = data_after_unusual.drop_duplicates(subset=["id"], keep='first', inplace=False)
    n = len(data_after_duplicated)
    date_formula = re.compile(
        '(([1-3][0-9]{3})[-]{0,1}(((0[13578]|1[02])[-]{0,1}(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)[-]{0,1}'
        '(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8])))\s\d{1,2}:\d{1,2}:\d{1,2})|(([1-3][0-9]{3})[-]'
        '{0,1}(((0[13578]|1[02])[-]{0,1}(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)-(0[1-9]|[12][0-9]|30))|(02-'
        '(0[1-9]|[1][0-9]|2[0-8])))\s\d{1,2}:\d{1,2})|(([1-3][0-9]{3})[-]{0,1}(((0[13578]|1[02])[-]{0,1}'
        '(0[1-9]|[12][0-9]|3[01]))|((0[469]|11)[-]{0,1}(0[1-9]|[12][0-9]|30))|(02-(0[1-9]|[1][0-9]|2[0-8]))))')
    tempDf = pd.DataFrame(data_after_duplicated)
    for i in range(0, n):
        if if_contain_symbol(data_after_duplicated.iloc[i, 2]):
            tempDf.iloc[i, 2] = (date_formula.search(data_after_duplicated.iloc[i, 2]).group(0) + " 中国标准时间")
            print(tempDf.iloc[i, 2])
    print('Modify complete')
    return tempDf


def savetoPath(path, dfdata):
    dfdata.to_csv(path, index=None)
    print('Save complete')


def if_contain_symbol(keyword):
    if re.search(r"\W", keyword):
        return True
    else:
        return False


if __name__ == '__main__':
    readPath = 'E:\WorkSpace\Python\Twint\data\italy\event1\original-event1.csv'
    writePath = 'E:\WorkSpace\Python\Twint\data\italy\event1\event1.csv'
    dfData = readcsv(readPath)
    duplicateList = detectcsv(dfData)
    dfData = modify(duplicateList, dfData)
    savetoPath(writePath, dfData)
