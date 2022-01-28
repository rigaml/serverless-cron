import pandas as pd
import boto3

if __name__ == "__main__":
    s3_client = boto3.client('s3',
    aws_access_key_id='dummy_key_id',
    aws_secret_access_key='dummy_access_key',
    endpoint_url='http://localhost:8000')

    movements = pd.read_excel('./data/0000-excel-ark-movements.xlsx', parse_dates=['Date'])

    s3_object = s3_client.Object('riga-cron-data', '0000-excel-ark-movements.xlsx')
    s3_movements= s3_object.put(Body=movements)

