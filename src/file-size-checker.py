import os
import platform
import re
import requests

def processFileDefinition(path):
    separator = ""
    #if platform.system() == "Windows":
    #    path = path.replace("\\","\\\\")
    
    print("Path: "+path)
    if isWildCardOnFileName(path):
        basename = os.path.basename(path)
        dirname = os.path.dirname(path)
        #print(basename)
        print("Dirname "+dirname)
        os.listdir(dirname)
        #print("")
        
        # do something
    #else:
        #do somrething else


def isWildCardOnFileName(path):
    separator = ""
    if platform.system() == "Linux":
        separator = "/"
    else:
        separator = "\\"
    
    split_path = path.split(separator)
    file_name = split_path[len(split_path)-1]
    
    regex = "(^.*[*].*$)"
    regex_result = re.search(regex, file_name)
    
    if regex_result:
        return True
    else:
        return False

def isPathGood(path):
    status = False
    if isWildCardOnDirectories(path) != True:
  #      print("Wild card is good.")
        status = True
    if isAbsolutePath(path) == True:
 #       print("Absolute path is good")
        status = True
    return status

def isWildCardOnDirectories(path):
    regex = ""
    if platform.system() == "Linux":
        regex = "(^.*[*]{1,}.*/.*$)"
    else:
        regex = "(^.*[*]{1,}.*\\\\.*$)"

#    print("Regex: "+ regex)
    regex_result = re.search(regex, path)
    if regex_result:
        return True
    else:
        return False
    
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

if (platform.system() != "Linux" and platform.system() != "Windows"):
    print("The platform you are running is not supported, please run this script on either a 'Windows' or 'Linux' system.")
    exit(1)

f = open("file-size-checker.conf", "r")
file_path = "file-size-checker.conf"
file_size = os.path.getsize(file_path)
#creating an array that will hold all the files that need to be checked
files_to_check = []

for file_definition in f:
    #print("File " + file_definition + " is valid?")
    #print(str(isPathGood(file_definition)))
    #processFileDefinition(file_definition)
    print("File Size is :", file_size, "bytes")
    url = ' http://localhost:14499/metrics/ingest'
    payload = "custom.file.size,file_name="+os.path.basename(file_definition)+" "+str(file_size)

    request_result = requests.post(url, data = payload)

    #print(x.text)



#def isValidLine():

