import requests
import json
 
  
url = "https://www.googleapis.com/drive/v2/files"
Apikey = 'API key goes here'


payload = {'key': Apikey, 'q': '\'0B1xc-Yrf99jZblNrMlRKY2NJZlk\' in parents and mimeType contains \'csv\''}
list_files = requests.get(url, params=payload)
answer = list_files.json()
inners = answer[u'items']

jsonData = []

for inner in inners:
    jsonData.append({"{#OCT.FILE.NAME}": inner[u'title'], "{#OCT.MODIFIED.DATE}": inner[u'modifiedDate'][0:10], "{#OCT.FILE.SIZE.BYTES}": inner[u'fileSize']})


print(json.dumps({"data": jsonData}, indent=4))

