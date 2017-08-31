import os
import json
import re


def loadParams():  # reads parameters file
    params = {}
    with open("./parameters.json") as f:
        params = json.load(f)
        params = getFiles(params)
        return params


def getFiles(params):  # populates params dictionary with filepaths as defined in parameters.json
    for path, suDirs, files in os.walk(params["data_path"]):
        for name in files:
            match = re.search("RME_.+RMD.+(...)", name)
            if match != None:
                if match.group(1) == "LBL":
                    params["file_names"]["lbls"].append(os.path.join(path, name))
                elif match.group(1) == "TAB":
                    params["file_names"]["tabs"].append(os.path.join(path, name))
    return params
