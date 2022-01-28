import datetime
import logging
import boto3
import pandas as pd
import requests


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def run(event, context):
    s3_client = boto3.client('s3',
    aws_access_key_id='dummy_key_id',
    aws_secret_access_key='dummy_access_key',
    endpoint_url='http://localhost:8000')

    print(s3_client.list_buckets())

    # TODO: Move file to s3 when using locally
    movements_file= s3_client.get_object('riga-cron-data', '0000-excel-ark-movements.xlsx')
    movements = pd.read_excel(movements_file)

    current_time = datetime.datetime.now().time()
    function_name = context.function_name
    logger.info("Cron function " + function_name + " ran at " + str(current_time))
    logger.info("Head " + movements.head())
