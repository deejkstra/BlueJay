# BlueJay EDR Activity Simulator

## Overview

This program simulates some basic system telemetry ex. File CRUD, executing processes, and network connections. You can use it to test your Endpoint Detection and Response (EDR) agents.

## API

### Start Process

* Pass an executable filepath plus args to the program to run the file.
* `--start-process --command="/path/to/executable/file --and --some --args"`

### Create File

* Create a file with some random payload.
* `--create-file --filename=/path/to/file.txt`

### Edit File 

* Update a file with some random payload.
* `--edit-file --filename=/path/to/file.txt`

### Delete File

* Remove the file from the system.
* `--delete-file --filename=/path/to/file.txt`

### Start Network

* This generates a simple TCP socket client and socket server which exchange a random string payload on a specified port.
* `--start-network --port=12345`

## Logging

The logger creates a dateime based filename using the following format:

```
redcanary_%Y-%m-%d.json
```

Each line of the logfile is a json blob, the following is a sample output:

```
{
    "timestamp": "2021-01-19 23:06:14.911330",
    "username": "someuser",
    "process_id": 27728,
    "process_name": "redcanary",
    "process_command": "./redcanary.py --create-file --filename=test.txt",
    "filepath": "test.txt",
    "operation": "create"
}
```

## Support

This program was tested on macOS Big Sur v11.1 and linux CentOS 7.
