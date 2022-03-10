# import urllib library
import urllib
  
# import json
import json

#MTA BUS_TIME API KEY
api_key = '3e1c22fb-8377-4657-8334-260c3e1f11d6'
SIRI_url = 'https://api.prod.obanyc.com/api/siri/vehicle-monitoring.json?key='+api_key+''
GTFS_url = 'http://gtfsrt.prod.obanyc.com/tripUpdates?key='+api_key+'' # GTFS RT , response does not work with urllib
  
# store the response of URL
response = urllib.urlopen(SIRI_url)
  

data = response.read().decode("utf-8")
#Converting the File to JSON Format
data = json.loads(data)
  
# print the json response
#print(data)

with open('data.json', 'w') as f:
    json.dump(data, f)