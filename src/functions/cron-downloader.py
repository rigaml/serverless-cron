"""
Download stock tickers information from Yahoo Finance API
"""

from datetime import datetime, date
import logging
import requests
import boto3

import config
from src.modules.ticker_converter import TickerConverter as tc

headers = {'User-Agent': ''}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def load_file(s3_client, file_name):
    file_object = s3_client.get_object(Bucket=config.BUCKET_NAME, Key=file_name)
    file_data = file_object['Body'].read()
    return file_data.decode("utf-8")


def save_file(s3_client, file_name, content):
    s3_client.put_object(Body=content, Bucket=config.BUCKET_NAME, Key=file_name)


def get_tickers_names(s3_client):
    tickers_names = load_file(s3_client, config.DOWNLOADER_TICKERS_FILE)
    # separate lines and then remove empty lines
    return [y for y in (x.strip() for x in tickers_names.splitlines()) if y]


def get_downloader_index(s3_client):
    downloader_index = load_file(s3_client, config.DOWNLOADER_INDEX_FILE)
    values = downloader_index.split(',')
    if len(values) == 2:
        last_day = values[0]
        last_name = values[1]
    else:
        last_day = '2000-01-01'
        last_name = config.DOWNLOADER_INDEX_MARK

    return (datetime.strptime(last_day, '%Y-%m-%d').date(), last_name)


def get_tickers_set(s3_client):
    tickers = get_tickers_names(s3_client)

    (last_day, last_name) = get_downloader_index(s3_client)

    today = date.today()
    if (last_day < today):
        return (tickers[0:config.TICKERS_PER_REQUEST], False)

    if last_name == config.DOWNLOADER_INDEX_MARK:
        return ([], False)

    if last_name in tickers:
        last_name_index = tickers.index(last_name)
        if (last_name_index >= len(tickers)):
            return ([], True)

        return (tickers[last_name_index+1:last_name_index+1+config.TICKERS_PER_REQUEST], False)

    logger.error(f'Last name "{last_name}" not found in tickets: {tickers}')
    return (tickers[0:config.TICKERS_PER_REQUEST], False)


def run(event, context):
    start_time_string = datetime.now().strftime("%Y-%m-%d-%H%M")
    today_date_string = date.today().strftime("%Y-%m-%d")

    s3_client = boto3.client('s3')

    (tickers, save_eof) = get_tickers_set(s3_client)

    if len(tickers) == 0 and save_eof:
        save_file(s3_client, config.DOWNLOADER_INDEX_FILE, f'{today_date_string},{config.DOWNLOADER_INDEX_MARK}')

    for counter, ticker in enumerate(tickers):
        logger.info(f'ticker ({counter}): {ticker}')
        request_ticker = tc.convert_yahoo_name(ticker)
        if (request_ticker is None):
            logger.info('  > skipping ticker')
            continue

        quote_summary_url = f'{config.DOWNLOAD_URL}{request_ticker}?{config.DOWNLOAD_URL_QUERY}{config.DOWNLOAD_URL_EXTRA_QUERY}'
        response = requests.get(quote_summary_url, headers=headers)
        if (response.ok):
            s3_client.put_object(Body=response.content, Bucket=config.BUCKET_NAME,
                                 Key=f'{config.BUCKET_FOLDER}{today_date_string}/{start_time_string}-{request_ticker}.json')
        else:
            logger.error(f'Failed to retrieve: {request_ticker} response {response.status_code}')

        save_file(s3_client, config.DOWNLOADER_INDEX_FILE, f'{today_date_string},{ticker}')


if __name__ == "__main__":
    # Dummy event and context for local testing
    dummy_event = {}
    dummy_context = type('obj', (object,), {'function_name': 'dummy_function'})
    run(dummy_event, dummy_context)