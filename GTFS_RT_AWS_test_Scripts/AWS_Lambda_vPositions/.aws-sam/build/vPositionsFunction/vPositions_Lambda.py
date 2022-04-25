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
    
    #print first feed
    #print(feed.entity[0])

    p_data = pd.DataFrame({'data':feed.entity[0]})
    table = pa.Table.from_pandas(p_data)

    #write to parqueet
    pq.write_table(table,'AWS_Lambda_vPositions/example.parquet')
    file_name = 'AWS_Lambda_vPositions/example.parquet'


    #write to s3
    s3_resource = boto3.resource('s3')
    MY_BUCKET_NAME = 's3-script-tests6544a2ec-2be3-4d25-ab1e-1e3494d732c7'
    s3_resource.Bucket(MY_BUCKET_NAME).upload_file(
    Filename=file_name, Key=file_name)

    return 0