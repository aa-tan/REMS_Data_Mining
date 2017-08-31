write_headerimport re
import dateutil.parser as dp
import datetime as dt
import setup
import json


def getStartTime(dataPath, filePath):
    # gets start time of data
    openFile = "{}{}.LBL".format(dataPath, get_file_name(filePath))
    with open(openFile) as f:
        for line in f:
            startTime = re.search("START_TIME += (.+)", line)
            if startTime != None:
                return startTime.group(1)


def to_unix(iso):
    # converts ISO8106 to UNIX Epoch time
    parsed = dp.parse(iso)
    return parsed.strftime("%s")


def to_iso(unix):
    # converts UNIX Epoch to ISO8106 time
    return dt.datetime.utcfromtimestamp(float(unix)).isoformat()


def write_header(writeLoc, filePath):
    # creates empty csv file and writes header info
    header = "t_utc,timestamp,h_wind_speed,v_wind_speed,wind_dir,ambient_temp,humidity,pressure\n"
    outFileName = "{}CSV/{}.csv".format(writeLoc, get_file_name(filePath))
    with open(outFileName, "w") as f:
        f.write(header)


def get_file_name(filePath):
    # returns only filename, used for appending extension
    fileName = re.search('.+\/(.+)\....', filePath)
    return fileName.group(1)


def filter_data(arr):
    # remove unneeded indices
    toKeep = [0, 3, 4, 5, 15, 30, 37]
    return [arr[i] for i in toKeep]


def prepare_line():
    # removes extra indices, converts timestamp, inserts to string, of each line
    ret = ""
    with open(filePath) as f:
        for line in f:
            tempString = filter_data(line.split(","))
            tempString.insert(0, str(to_iso(tempString[0])))
            ret += ",".join(tempString)
            ret += "\n"
        return ret


def write_data(params, filePath):
    # main function for writing CSV files
    write_header(params["write_location"], filePath)
    outString = prepare_line(filePath)
    outFileName = "{}CSV/{}.csv".format(
        params["write_location"], get_file_name(filePath))

    with open(outFileName, "a") as f:
        f.write(outString)
    write_JSON(params, filePath)


def write_JSON(params, filePath):
    # writes JSON files defining DB action
    out = {"action": "insert", "database": "sam.rems_temp", "records": {"type": "csv"}}
    out["records"]["$object_id"] = "{}CSV/{}.csv".format(
        params["write_location"], get_file_name(filePath))
    with open("{}{}.json".format(params["write_location"], get_file_name(filePath)), "w") as f:
        json.dump(out, f)


if __name__ == '__main__':
    # executing will create csv files for file defined in parameters.json
    # creates only for temperature and pressure
    params = setup.loadParams()
    for count in range(len(params["file_names"]["tabs"])):
        write_data(params, params["file_names"]["tabs"][count])
