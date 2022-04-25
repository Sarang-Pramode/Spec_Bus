import requests
import json
from google.transit import gtfs_realtime_pb2
import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd
import boto3

## _______________________________________

# Personal Note:

# Importing pandas module results in 12 sec execution time for lambda function
#  - Error : 
#  Function 'vPositionsFunction' timed out after 3 seconds
#  No response from invoke container for vPositionsFunction

# Solved by adding Timeout in Properties in Template file (currently set to 20 sec)

## _______________________________________
# import boto3

def lambda_handler(event, context):

    key_file_path = "MTA_API_KEY.json"
    
    with open(key_file_path, 'r') as f:
        data = json.load(f)

    api_key = data['API_KEY']

    GTFS_RT_Endpoints = {
        'tUpdates' : 'http://gtfsrt.prod.obanyc.com/tripUpdates?key='+api_key+'',
        'vPositions' : 'http://gtfsrt.prod.obanyc.com/vehiclePositions?key='+api_key+'',
        'alerts' : 'http://gtfsrt.prod.obanyc.com/alerts?key='+api_key+''
    }

    #create enpoint
    GTFS_RT_feed = 'alerts'
    Req_endpoint = GTFS_RT_Endpoints[GTFS_RT_feed]

    feed = gtfs_realtime_pb2.FeedMessage() #create feedmessage buffer
    response = requests.get(Req_endpoint) #GET request and save the response

    # TODO 
    # Write handler for failed responses
    feed.ParseFromString(response.content) #parse the response(protobuf) and store in feed  

    return 0