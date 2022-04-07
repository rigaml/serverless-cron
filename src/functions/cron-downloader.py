import datetime
import logging
import boto3
import pandas as pd
import requests

# https://towardsdatascience.com/introduction-to-amazon-lambda-layers-and-boto3-using-python3-39bd390add17

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def run(event, context):
    s3_client = boto3.client('s3')

    print(s3_client.list_buckets())

    # TODO: Move file to s3 when using locally
    movements_file= s3_client.get_object('riga-cron-data', '0000-excel-ark-movements.xlsx')
    movements = pd.read_excel(movements_file)

    current_time = datetime.datetime.now().time()
    function_name = context.function_name
    logger.info("Cron function " + function_name + " ran at " + str(current_time))
    logger.info("Head " + movements.head())

if __name__ == "__main__":
    run()
