#!/usr/bin/env python
import re
import datetime as dt
import json
import os
import sys
# Author: Aaron Tan


def load_properties():
    # reads properties file
    print("Loading Properties")
    properties = {}
    with open("./properties.json") as f:
        properties = json.load(f)
        properties = get_files(properties)
        return properties


def get_files(properties):
    # populates properties dictionary with filepaths as defined in properties.json
    for path, suDirs, files in os.walk(properties["data_path"]):
        for name in files:
            match = re.search("RME_.+RMD.+(...)", name)
            if match != None:
                if match.group(1) == "LBL":
                    properties["file_names"]["lbls"].append(
                        os.path.join(path, name))
                elif match.group(1) == "TAB":
                    properties["file_names"]["tabs"].append(
                        os.path.join(path, name))
    return properties


def to_unix(timestamp):
    # converts J2000 epoch to Unix by adding missing seconds
    return str(int(timestamp) + 946728000)


def to_iso(unix):
    # converts UNIX Epoch to ISO8106 time
    return dt.datetime.utcfromtimestamp(float(unix)).isoformat()


def get_file_name(filePath):
    # returns only filename, used for appending extension
    fileName = re.search('.+\/(.+)\....', filePath)
    return fileName.group(1)


def filter_data(arr):
    # remove unneeded indices
    toKeep = [0, 3, 4, 5, 15, 30, 37]
    return [arr[i] for i in toKeep]


def prepare_line(filePath):
    # removes unwated data, converts timestamp, inserts to string of each line
    print("Reading File: {}".format(filePath))
    try:
        ret = ""
        with open(filePath) as f:
            for line in f:
                tempString = filter_data(line.split(","))
                tempString[0] = to_unix(tempString[0])
                tempString.insert(0, str(to_iso(tempString[0])))
                ret += ",".join(tempString)
                ret += "\n"
            return ret
    except:
        print("Failed to Read File: {}".format(filePath))


def write_header(filePath):
    # creates empty csv file and writes header info
    header = "t_utc,timestamp,h_wind_speed,v_wind_speed,wind_dir,ambient_temp,humidity,pressure\n"
    outFileName = "{}CSV/{}.csv".format(
        properties["write_location"], get_file_name(filePath))
    print("Writing header of file: {}".format(outFileName))
    try:
        with open(outFileName, "w") as f:
            f.write(header)
    except:
        print("Failed to write header")


def write_data(filePath):
    # function for writing CSV files
    outString = prepare_line(filePath)
    outFileName = "{}CSV/{}.csv".format(
        properties["write_location"], get_file_name(filePath))
    print("Writing CSV File")
    try:
        with open(outFileName, "a") as f:
            f.write(outString)
    except:
        print("Failed to write CSV File")


def write_JSON(filePath):
    # writes JSON files defining DB action
    print("Writing JSON File")
    try:
        out = {"action": "insert", "database": "sam.rems_temp",
               "records": {"type": "csv"}}
        out["records"]["$object_id"] = "{}CSV/{}.csv".format(
            properties["write_location"], get_file_name(filePath))
        with open("{}{}.json".format(properties["write_location"], get_file_name(filePath)), "w") as f:
            json.dump(out, f)
        print("Success\n")
    except:
        print("Failed to write JSON File")


def update_path(read_path, write_path):
    # Sets read/write path to that defined in cmd line arguments
    properties["data_path"] = read_path
    properties["write_location"] = write_path


def execute():
    # main function handling mining process
    # iterates through list of file names
    #
    # for each file
    # write the row denoting data type (UTC time, timestamp, etc)
    # read file data line by line
    # format line and writes to out file
    # writes json file for DB insertion
    print("\nStarting Mining Process\n----")
    try:
        filePath = properties["file_names"]["tabs"]
        for count in range(len(properties["file_names"]["tabs"])):
            write_header(filePath[count])
            write_data(filePath[count])
            write_JSON(filePath[count])

    except:
        print("\n\n----\nAN ERROR HAS OCCURRED\n----\\nn")


# load properties for global use
properties = load_properties()
if __name__ == '__main__':
    # executing will create csv files for files defined in properties.json
    if len(sys.argv) == 3:
        print("Updating path to match arguments")
        update_path(sys.argv[1], sys.argv[2])
        execute()
    elif len(sys.argv) == 1:
        print("Running using properties.json paths")
        execute()