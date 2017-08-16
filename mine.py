import os


def count():
    fileList = {}
    for fileName in os.listdir(filePath):
        lineCount = 0
        lineRead = ""
        print(fileName)
        with open(filePath + fileName) as f:
            while f.readline() != "":
                lineCount += 1
            fileList[fileName] = lineCount
    return fileList


def getFiles(filePath):
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
                if x in matched:
                    pass
                else:
                    matched.append(x)
                    print("{}.{}\n{}.{}\n\n".format(x[0], x[1], y[0], y[1]))
                break
    return matched


def searchCategory(splitList, path):
    categories = ["pressure"]
    for item in splitList:
        if item[1] == "LBL":
            with open(path + item[0] + "." + item[1]) as f:
                line = f.readline()
                while line != "":
                    if line == "= \" PRESSURE \"":
                        print("Pressure is found in {}".format(
                            path + item[0] + item[1]))
                    # print(line)
                    line = f.readline()

if __name__ == '__main__':
    filePath = "./Data/"
    files = getFiles(filePath)
    splits = splitName(files)
    matched = match(splits)
    # searchCategory(matched, filePath)
    # print(splits)
    # print(splitName(files))
