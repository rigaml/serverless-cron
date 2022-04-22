import boto3
import io
import datetime
import logging
import pandas as pd
import requests

# https://towardsdatascience.com/introduction-to-amazon-lambda-layers-and-boto3-using-python3-39bd390add17

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def run(event, context):
    s3_client = boto3.client('s3')

    print(s3_client.list_objects(Bucket='riga-cron-data'))

    movements_object= s3_client.get_object(Bucket='riga-cron-data', Key='0000-excel-ark-movements.xlsx')
    movements_data = movements_object['Body'].read()
    movements = pd.read_excel(io.BytesIO(movements_data))

    current_time = datetime.datetime.now().time()
    function_name = context.function_name
    logger.info("Cron function " + function_name + " ran at " + str(current_time))

    print(movements.head())

if __name__ == "__main__":
    run()
