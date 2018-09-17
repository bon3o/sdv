import requests
import json
import urllib.request
import csv
import os


url = "https://www.googleapis.com/drive/v2/files"
Apikey = 'API key goes here' #form https://console.developers.google.com/apis/credentials?project=custom-library-192209&authuser=1&organizationId=0&pli=1
path = '/Users/p.botov/Downloads/OCT/'


payload = {'key': Apikey, 'q': '\'0B1xc-Yrf99jZblNrMlRKY2NJZlk\' in parents and mimeType contains \'csv\''} #parent folder name and type of files


list_files = requests.get(url, params=payload)


answer = list_files.json()
inners = answer[u'items']


jsonData = []


for inner in inners:


    url = inner[u'webContentLink']
    response = urllib.request.urlretrieve(url, path + inner[u'title'])
        with open(path + inner[u'title'], "r") as f:
            reader = csv.reader(f, delimiter=",")
            data = list(reader)
            row_count = len(data)
        os.remove(path + inner[u'title'])
        jsonData.append({"{#OCT.FILE.NAME}": inner[u'title'], "{#OCT.MODIFIED.DATE}": inner[u'modifiedDate'][0:10],
                                                                             "{#OCT.FILE.SIZE.BYTES}": inner[u'fileSize'], "{#OCT.ROW.COUNT}": row_count})

print(json.dumps({"data": jsonData}, indent=4))
