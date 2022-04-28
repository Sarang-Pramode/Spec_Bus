import requests
import json
from google.transit import gtfs_realtime_pb2
import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd
import boto3

# GET all routes with issues
def getRouteWithAlerts(feed):
    problem_routes = []
    for entity in feed.entity:
        for informed_entity in entity.alert.informed_entity:
            route_value = informed_entity.trip.route_id
            if(route_value == ''):
                route_value = informed_entity.route_id
            problem_routes.append(route_value)
    return problem_routes

def Upload_to_s3(file_name):
    s3_resource = boto3.resource('s3')
    MY_BUCKET_NAME = 'nyc-mta-gtfs-rt-alerts'
    s3_resource.Bucket(MY_BUCKET_NAME).upload_file(
    Filename=file_name, Key=file_name)

    return 0


def lambda_handler(event, context):
    with open('MTA_API_KEY.json', 'r') as f:
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
    problem_routes = getRouteWithAlerts(feed)
    
    print(problem_routes)

    #temp test
    #problem_routes = ['BX16', 'BX34', '', '', '', '', '', '', '', '', '', '', 'S53', 'S93', 'M9', 'M14A+', 'M21', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'M15', 'M15+', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 'Q17', 'Q27', '', '', '', '', '', '', '', '', 'SIM33', 'SIM4C', 'SIM3C', 'SIM1C', 'SIM7', 'SIM9', 'X27', 'X28', '', '', '', '', '', '', '', '', 'M5', 'M7', '', '', '', '', '', '', '', '', '', '', '', '', 'B103', 'BM4', 'BM3', 'BM2', 'BM1', 'Q09', 'Q07', 'Q40', 'Q112', '', '', '', '', 'BXM4', 'BX34', '', '', 'BXM7', 'BXM8', 'BXM9']
    p_data = pd.DataFrame({'data':problem_routes})
    #table = pa.Table.from_pandas(p_data)

    #write to parqueet
    #pq.write_table(table,'example.parquet')
    p_data.to_parquet(f"/tmp/{'routes_with_issues.parquet'}")

    source_path=f"/tmp/{'routes_with_issues.parquet'}" 
    print(Upload_to_s3(source_path))

    return {
        'success' : True
    }

    