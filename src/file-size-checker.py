import os
import platform
import re
import requests
import time
import sys
from pathvalidate import ValidationError, validate_filename, validate_filepath, sanitize_filepath
    
def isAbsolutePath(path):
    if platform.system() == "Linux":
        if (path[0] == "/"):
            return True
        else:
            return False
    elif platform.system() == "Windows":
        x = re.search("^[a-zA-z]{1}:\\\\", path)
        if x:
            return True
        else:
            return False
def sendMetrics(filename, filesize):
    url = ' http://localhost:14499/metrics/ingest'
    payload = "custom.file.size,file_name="+filename+" "+str(filesize)
    print(payload)
    request_result = requests.post(url, data = payload)
    print(request_result)

def checkFileSizes(config_file):
    f = open(config_file, "r")
    for file_definition in f:
        file_definition = file_definition.strip()
        print("Checking ", file_definition, " size.")
        file_size = os.path.getsize(sanitize_filepath(file_definition, platform = platform.system()).replace("\\\\","\\"))
        print(file_definition, " size is :", file_size, "bytes")
        sendMetrics(filename=file_definition, filesize=file_size)
        
def isConfigurationValid(config_file):
    f = open(config_file, "r")
    status = True
    for file_definition in f:
        file_definition = file_definition.strip()
        try:
            #validate_filename(file_definition)
            validate_filepath(file_path = file_definition, platform = platform.system())
            os.stat(file_definition)
            print(file_definition," is valid.")
            status = status*True
        except ValidationError as e:
            print(f"{e}\n", file=sys.stderr)
            print("File "+file_definition+" is invalid for this OS.")
            status = status*False
        except FileNotFoundError as e:
            print(f"{e}\n", file=sys.stderr)
            print("File "+file_definition+" does not exist. Please check if the path is correct and if the file exists and has the right permissions.")
            status = status*False
    
    if status == True:
        print("All file definitions are valid, continuing...")
    return status

if (platform.system() != "Linux" and platform.system() != "Windows"):
    print("The platform you are running is not supported, please run this script on either a 'Windows' or 'Linux' system.")
    exit(1)


config_file = "file-size-checker.conf"
#creating an array that will hold all the files that need to be checked

if isConfigurationValid(config_file) == True:
    checkFileSizes(config_file)
    #print("Do something...")

    #while(True):
    #    for file_definition in f:
    #        print(file_definition)
    #        try:
    #            validate_filename(file_definition)
    #            validate_filepath(file_definition)
    #        except ValidationError as e:
    #            print(f"{e}\n", file=sys.stderr)

            
                
            

            
            
            #print("File Size is :", file_size, "bytes")
            

            #print(x.text)
    #    time.sleep(1)
else:
    print("Invalid configuration found, exiting....")
    exit(1)