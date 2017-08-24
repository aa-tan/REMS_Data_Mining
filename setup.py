import os
import json
import re


def loadParams(dataSet):  # reads parameters file
    params = {}
    with open("./parameters.json") as f:
        params = json.load(f)
    if dataSet == "temp":
        params = params["temperature"]
        params = getTempFiles(params)
        print("loading temp")
        return params
    elif dataSet == "wind":
        params = params["wind"]
        params = getWindFiles(params)
        print("loading wind")
        return params


def getTempFiles(params):  # populates params dictionary with filepaths as defined in parameters.json
    for path, suDirs, files in os.walk(params["data_path"]):
        for name in files:
            match = re.search("(.+RMC_.+(...))", name)
            if match != None:
                if match.group(2) == "LBL":
                    params["file_names"]["lbls"].append(os.path.join(path, name))
                elif match.group(2) == "TAB":
                    params["file_names"]["tabs"].append(os.path.join(path, name))
    return params


def getWindFiles(params):
    for path, suDirs, files in os.walk(params["data_path"]):
        for name in files:
            match = re.search("(TELLTALE.+\.(...))", name)
            if match != None:
                if match.group(2) == "LBL":
                    params["file_names"]["lbls"].append(os.path.join(path, name))
                elif match.group(2) == "TAB":
                    params["file_names"]["tabs"].append(os.path.join(path, name))
    return params
