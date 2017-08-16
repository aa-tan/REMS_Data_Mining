import setup


if __name__ == '__main__':
    dataPath = "./SampleData/"
    fileList = setup.getAllFiles(dataPath)
    for item in fileList:
        print(item)
