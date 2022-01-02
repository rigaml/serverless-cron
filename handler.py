import datetime
import logging
import boto3

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def run(event, context):
    s3_client = boto3.resource('s3')

    s3_client.

    current_time = datetime.datetime.now().time()
    name = context.function_name
    logger.info("Cron function " + name + " ran at " + str(current_time))
