
#Repo used for help - https://github.com/bennett39/mta-real-time-data/blob/master/gtfs.py

#Desc : get a JSON response from the MTA GTFS API - (Single call)

import requests
from google.transit import gtfs_realtime_pb2


feed = gtfs_realtime_pb2.FeedMessage()

api_key = '3e1c22fb-8377-4657-8334-260c3e1f11d6'
GTFS_url1 = 'http://gtfsrt.prod.obanyc.com/tripUpdates?key='+api_key+''
GTFS_url2 = 'http://gtfsrt.prod.obanyc.com/vehiclePositions?key='+api_key+''
GTFS_url3 = 'http://gtfsrt.prod.obanyc.com/alerts?key='+api_key+'' 

print(GTFS_url3)
response = requests.get(GTFS_url3, allow_redirects=True)

feed.ParseFromString(response.content)

with open('output'+str(4)+'.txt', mode='w') as f:
        for entity in feed.entity:
            f.write(str(entity))
            #if entity.HasField('vehiclePositions'):
                #f.write(str(entity.vehiclePositions))
