import urllib.request
import json

with urllib.request.urlopen('http://rbi.ddns.net/getBreadCrumbData') as response:
    with open('b.json', 'wb') as file:
        file.write(response.read())

reader = open('b.json')

y=json.load(reader)
#y = json.loads(b.json)
print(y)

