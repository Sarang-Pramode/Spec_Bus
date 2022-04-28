import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime
import boto3

def Upload_to_s3(file_name):
    s3_resource = boto3.resource('s3')
    MY_BUCKET_NAME = 's3-script-tests6544a2ec-2be3-4d25-ab1e-1e3494d732c7'
    s3_resource.Bucket(MY_BUCKET_NAME).upload_file(
    Filename=file_name, Key=file_name)

    return 0


def lambda_handler(event, context):

    Example_schema = pa.schema([
        ('timestamp', pa.timestamp('ms')),
        ('id', pa.int32()),
        ('email', pa.string())
    ])

    timestamps = pa.array([
    datetime(2019, 9, 3, 9, 0, 0),
    datetime(2019, 9, 3, 10, 0, 0),
    datetime(2019, 9, 3, 11, 0, 0)
    ], type = pa.timestamp('ms'))

    ids = pa.array([1, 2, 3], type = pa.int32())

    emails = pa.array(
        ['first@example.com', 'second@example.com', 'third@example.com'],
        type = pa.string()
    )

    batch = pa.RecordBatch.from_arrays(
        [timestamps, ids, emails],
        names = Example_schema
    )

    dataframe = pd.DataFrame([
    [datetime(2019, 9, 3, 9, 0, 0), 1, 'first@example.com'],
    [datetime(2019, 9, 3, 10, 0, 0), 1, 'second@example.com'],
    [datetime(2019, 9, 3, 11, 0, 0), 1, 'third@example.com'],
    ], columns = ['timestamp', 'id', 'email'])

    table = pa.Table.from_batches([batch])
    table_from_pandas = pa.Table.from_pandas(dataframe)
    pq.write_table(table_from_pandas, f'/tmp/Examples_pandas.parquet')

    Upload_to_s3(f'/tmp/Examples_pandas.parquet')

    return{
        "statusCode": 200,
    }
