"""
Playground example to access a file in AWS S3
https://towardsdatascience.com/introduction-to-amazon-lambda-layers-and-boto3-using-python3-39bd390add17
"""
from datetime import datetime
import logging
import pandas as pd
import boto3
import io
import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def run(event, context):
    s3_client = boto3.client('s3')

    print(s3_client.list_objects(Bucket=config.BUCKET_NAME))

    movements_object= s3_client.get_object(Bucket=config.BUCKET_NAME, Key='0000-excel-ark-movements.xlsx')
    movements_data = movements_object['Body'].read()
    movements = pd.read_excel(io.BytesIO(movements_data))

    current_time = datetime.now().time()
    function_name = context.function_name
    logger.info("Cron function " + function_name + " ran at " + str(current_time))

    print(movements.head())

if __name__ == "__main__":
    # Dummy event and context for local testing
    dummy_event = {}
    dummy_context = type('obj', (object,), {'function_name': 'dummy_function'})
    run(dummy_event, dummy_context)
