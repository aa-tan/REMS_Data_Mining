import re
import dateutil.parser as dp
import datetime as dt
import setup
import json


def getStartTime(dataPath, filePath):  # gets start time of data
    openFile = "{}{}.LBL".format(dataPath, getFileName(filePath))
    with open(openFile) as f:
        for line in f:
            startTime = re.search("START_TIME += (.+)", line)
            if startTime != None:
                return startTime.group(1)


def toUnix(iso):  # converts ISO8106 to UNIX Epoch time
    parsed = dp.parse(iso)
    return parsed.strftime("%s")


def toIso(unix):  # converts UNIX Epoch to ISO8106 time
    return dt.datetime.utcfromtimestamp(float(unix)).isoformat()


def writeHeader(writeLoc, filePath):  # creates empty csv file and writes header info
    if "Temperature" in writeLoc:
        header = "t_utc,timestamp,pressure,temp_250,temp_500,temp_1000,temp_absolute\n"
    elif "Wind" in writeLoc:
        header = "t_utc,timestamp,wind_speed,wind_speed_err_pos,wind_speed_err_neg,wind_dir,wind_dir_err"
    outFileName = "{}CSV/{}.csv".format(writeLoc, getFileName(filePath))
    with open(outFileName, "w") as f:
        f.write(header)


def getFileName(filePath):  # returns only filename, used for appending extension
    fileName = re.search('.+\/(.+)\....', filePath)
    return fileName.group(1)


def writeData(params, filePath):  # main function for writing CSV files
    writeHeader(params["write_location"], filePath)
    outString = ""
    tempString = ""
    timeStart = getStartTime(params["data_path"], filePath)
    unix = toUnix(timeStart)
    outFileName = "{}CSV/{}.csv".format(
        params["write_location"], getFileName(filePath))
    with open(filePath) as f:
        for line in f:
            tempString = line.split(",")
            tempUnix = float(unix) + float(tempString[0])
            tempString.pop(0)
            tempIso = toIso(tempUnix)
            tempString.insert(0, str(tempIso))
            tempString.insert(0, str(tempUnix))
            outString += ",".join(tempString)
    with open(outFileName, "a") as f:
        f.write(outString)
    writeJSON(params, filePath)


def writeJSON(params, filePath):
    out = {"action": "insert", "database": "sam.rems_temp", "records": {"type": "csv"}}
    out["records"]["$object_id"] = "{}CSV/{}.csv".format(
        params["write_location"], getFileName(filePath))
    with open("{}{}.json".format(params["write_location"], getFileName(filePath)), "w") as f:
        json.dump(out, f)

if __name__ == '__main__':
    # executing will create csv files for file defined in parameters.json
    # creates only for temperature and pressure
    params = setup.loadParams("temp")
    for count in range(len(params["file_names"]["tabs"])):
        writeData(params, params["file_names"]["tabs"][count])