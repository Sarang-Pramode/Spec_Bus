import requests
import json
from google.transit import gtfs_realtime_pb2
import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd

# GET all routes with issues
def getRouteWithAlerts(feed):
    problem_routes = []
    for entity in feed.entity:
        for informed_entity in entity.alert.informed_entity:
            problem_routes.append(informed_entity.route_id)
    return problem_routes


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

    p_data = pd.DataFrame({'data':problem_routes})
    table = pa.Table.from_pandas(p_data)

    #write to parqueet
    pq.write_table(table,'example.parquet')