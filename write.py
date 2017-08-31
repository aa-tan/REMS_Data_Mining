import re
import dateutil.parser as dp
import datetime as dt
# import setup
import json
import os


def load_params():
    # reads parameters file
    print("Loading Parameters")
    params = {}
    with open("./parameters.json") as f:
        params = json.load(f)
        params = get_files(params)
        return params


def get_files(params):
    # populates params dictionary with filepaths as defined in parameters.json
    for path, suDirs, files in os.walk(params["data_path"]):
        for name in files:
            match = re.search("RME_.+RMD.+(...)", name)
            if match != None:
                if match.group(1) == "LBL":
                    params["file_names"]["lbls"].append(os.path.join(path, name))
                elif match.group(1) == "TAB":
                    params["file_names"]["tabs"].append(os.path.join(path, name))
    return params


# def getStartTime(dataPath, filePath):
#     # gets start time of data
#     openFile = "{}{}.LBL".format(dataPath, get_file_name(filePath))
#     with open(openFile) as f:
#         for line in f:
#             startTime = re.search("START_TIME += (.+)", line)
#             if startTime != None:
#                 return startTime.group(1)


# def to_unix(iso):
#     # converts ISO8106 to UNIX Epoch time
#     parsed = dp.parse(iso)
#     return parsed.strftime("%s")


def to_iso(unix):
    # converts UNIX Epoch to ISO8106 time
    return dt.datetime.utcfromtimestamp(float(unix)).isoformat()


def write_header(writeLoc, filePath):
    # creates empty csv file and writes header info
    header = "t_utc,timestamp,h_wind_speed,v_wind_speed,wind_dir,ambient_temp,humidity,pressure\n"
    outFileName = "{}CSV/{}.csv".format(writeLoc, get_file_name(filePath))
    print("Writing header of file: {}".format(outFileName))
    try:
        with open(outFileName, "w") as f:
            f.write(header)
    except:
        print("Failed to write header")


def get_file_name(filePath):
    # returns only filename, used for appending extension
    fileName = re.search('.+\/(.+)\....', filePath)
    return fileName.group(1)


def filter_data(arr):
    # remove unneeded indices
    toKeep = [0, 3, 4, 5, 15, 30, 37]
    return [arr[i] for i in toKeep]


def prepare_line(filePath):
    # removes extra indices, converts timestamp, inserts to string, of each line
    print("Reading File: {}".format(filePath))
    try:
        ret = ""
        with open(filePath) as f:
            for line in f:
                tempString = filter_data(line.split(","))
                tempString.insert(0, str(to_iso(tempString[0])))
                ret += ",".join(tempString)
                ret += "\n"
            return ret
    except:
        print("Failed to Read File: {}".format(filePath))


def write_data(params, filePath):
    # main function for writing CSV files
    outString = prepare_line(filePath)
    outFileName = "{}CSV/{}.csv".format(
        params["write_location"], get_file_name(filePath))
    print("Writing CSV File")
    try:
        with open(outFileName, "a") as f:
            f.write(outString)
    except:
        print("Failed to write CSV File")


def write_JSON(params, filePath):
    # writes JSON files defining DB action
    print("Writing JSON File")
    try:
        out = {"action": "insert", "database": "sam.rems_temp",
               "records": {"type": "csv"}}
        out["records"]["$object_id"] = "{}CSV/{}.csv".format(
            params["write_location"], get_file_name(filePath))
        with open("{}{}.json".format(params["write_location"], get_file_name(filePath)), "w") as f:
            json.dump(out, f)
        print("Success\n")
    except:
        print("Failed to write JSON File")


def execute():
    print("\nStarting Mining Process\n----")
    try:
        params = load_params()
        filePath = params["file_names"]["tabs"]
        for count in range(len(params["file_names"]["tabs"])):
            write_header(params["write_location"], filePath[count])
            write_data(params, filePath[count])
            write_JSON(params, filePath[count])

    except:
        print("\n\n----\nAN ERROR OCCURRED\n----\\nn")


if __name__ == '__main__':
    # executing will create csv files for file defined in parameters.json
    # creates only for temperature and pressure
    execute()
