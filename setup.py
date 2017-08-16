import os
import json


def getAllFiles(filePath):
    fileList = []
    for fileName in os.listdir(filePath):
        fileList.append(fileName)
    return fileList


def splitName(fileList):
    splitList = []
    for fileName in fileList:
        splitList.append(fileName.split("."))
    return splitList


def match(splitList):
    matched = []
    for x in splitList:
        for y in splitList:
            if x[0] in y and x[1] not in y:
                matched.append(x)
                break
    return matched


def genFileList(matchList):
    outList = []
    for item in matchList:
        tempList = [item[0] + ".LBL", item[0] + ".TAB"]
        if tempList in outList:
            pass
        else:
            outList.append(tempList)
    with open("./FileList/list.json", "w") as outFile:
        json.dump(outList, outFile)


def getDataTypes():
    dataTypes = []
    with open(dataTypePath) as f:
        dataTypes = json.load(f)
        print dataTypes
    return dataTypes


def searchCategory():  # todo read from gen
    categories = ["PRESSURE"]
    fileList = []
    mineLocation = {}
    with open("./FileList/list.json") as f:
        fileList = json.load(f)
    for item in fileList:
        with open(dataPath + item[0]) as labelFile:
            for line in labelFile:
                for category in categories:
                    if "= \"{}\"".format(category) in line:
                        print("{} is found in {}".format(category,
                                                         dataPath + item[0]))
                        mineLocation[category] = item[0]


if __name__ == '__main__':
    dataPath = "./SampleData/"
    dataTypePath = "./datatypes.json"
    fileList = getAllFiles(dataPath)
    split = splitName(fileList)
    matched = match(split)
    genFileList(matched)
    getDataTypes()
    # searchCategory()
