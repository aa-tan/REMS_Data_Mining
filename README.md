# MSL Datamining Script
This script performs the action of converting MODRDR data from the MSL dataset into a csv format for insertion into XINA.

## Setup
The directory contains two files:
 - properties.json
 - rems_data_mine.<i></i>py
 - parsed_files.json

#### rems_data_mine.<i></i>py

Executing this script without arguments will read the properties.json file and begin the mining process.
The alternative is to provide read and write paths as arguments.

It will proceed to traverse the directory defined in `data_path` and record the paths to each file containing `RMD` in the file name and `TAB` as the extension. These files hold the MODRDR data, which is the data post-processing and adjustment.

The script will then access each file according to the recorded path and create a CSV file. It will write the first row that contains the column names.

Next, each file is read line by line and each line is formatted to remove un-wanted data. The time stamps are converted to the appropriate format and added to the line before it is added to the file.

Lastly, the script creates a JSON file using the filepath to the CSV as it's object id.

The script will also record the names of files that have been processed (parsed_files.json) in order to prevent re-processing the file.

#### properties.json
The properties defines the write location of the CSV/JSON files and also defines the read location of the MSL dataset.
Stores name of database to be written in JSON files.

Edit the `write_location: ""` and `data_path: ""` values with the desired path.

Example:
`write_location: "./log/data_entries"`
`data_path: "./raw_data/sol-1_50"`

Edit the `database: ""` value to define the name of the database

#### parsed_files.json
Stores the file names of files that have been processed and should not be re-processed.

For first use, make sure the JSON file contains an empty list `[]`


## Usage

Executing using file paths defined in properties.json
`$ python rems_data_mine.py`

or

```
$ chmod +x rems_data_mine.py
$ ./rems_data_mine.py
```

Executing by defining file paths defined as arguments
`$ python rems_data_mine.py <read_location> <write_location>`

or

```
$ chmod +x rems_data_mine.py
$ ./rems_data_mine.py <read_location> <write_location>
```

Example:

`python rems_data_mine.py ./raw_data/sol-1_50 ./log/data_entries/`

`CTRL-C` to quit process
