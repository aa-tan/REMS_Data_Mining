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


def searchCategory(splitList, path):  # todo read from gen
    categories = ["pressure"]
    for item in splitList:
        if item[1] == "LBL":
            with open(path + item[0] + "." + item[1]) as f:
                for line in f:
                    if "= \"PRESSURE\"" in line:
                        print("Pressure is found in {}".format(
                            path + item[0] + item[1]))


if __name__ == '__main__':
    dataPath = "./SampleData/"
    fileList = getAllFiles(dataPath)
    split = splitName(fileList)
    matched = match(split)
    genFileList(matched)
