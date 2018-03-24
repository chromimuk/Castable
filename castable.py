#! python3 
# Generate an HTML page containing all the castable videos in a specific folder
# The page will allow us to easily stream stuff

import sys
import os
import http.server
import socketserver
import json
import re
from shutil import copyfile

PORT = 8000


def getFilesFromFolder(folder):
    return [x for x in os.listdir(folder) if x.endswith(".mp4")]

def generateMediaJSON(serverAddress, files):
    media = []
    for i in range(len(files)):
        m = {}
        m['idx'] = i
        m['url'] = os.path.join(serverAddress, files[i])
        m['title'] = files[i]
        m['img'] = ' '
        media.append(m)
    return media

def replaceTemplateInFile(filename, old_string, new_string):
    with open(filename) as f:
        newText=f.read().replace(old_string, new_string)
    with open(filename, "w") as f:
        f.write(newText)

# basic validation for ipv4 address
def validateServerAddress(serverAddress):
    serverAddressRegex = re.compile(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}')
    return serverAddressRegex.search(serverAddress)
    
def startServer(serverAddress):
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer((serverAddress, PORT), Handler) as httpd:
        print("Serving HTTP on ", serverAddress, " port ", PORT)
        httpd.serve_forever()



if (len(sys.argv) < 2):
    print('Usage: python castable.py [localServerAddress]')
    sys.exit()

serverAddress = sys.argv[1]
isValid = validateServerAddress(serverAddress)
if (not isValid):
    print('serverAddress specified not valid')
    sys.exit()

folderName = os.path.abspath(os.path.dirname(__file__))
files = getFilesFromFolder(folderName)
if (len(files) == 0):
    print("No files found")
    sys.exit()

media = generateMediaJSON("http://" + serverAddress + ":8000", files)
copyfile('template.html', 'index.html')
replaceTemplateInFile('index.html', '{tmp}', folderName)
replaceTemplateInFile('index.html', '{media}', str(media))

startServer(serverAddress)