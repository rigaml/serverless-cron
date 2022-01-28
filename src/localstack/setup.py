import pandas as pd
import boto3

bucket_name= 'riga-cron-data'

if __name__ == "__main__":
    session = boto3.Session(
        region_name='us-east-1', 
        aws_access_key_id='dummy_key_id', 
        aws_secret_access_key='dummy_access_key')

    s3 = session.resource('s3', endpoint_url='http://host.docker.internal:4566')
    bucket = s3.create_bucket(Bucket=bucket_name)
    bucket.upload_file(
        './data/0000-excel-ark-movements.xlsx', 
        '0000-excel-ark-movements.xlsx')
