import boto3
# import datetime and date class from datetime module
from datetime import datetime, date
import logging
import requests
from src.modules.ticker_converter import ticker_converter as tc

# https://towardsdatascience.com/introduction-to-amazon-lambda-layers-and-boto3-using-python3-39bd390add17

bucket_name = 'riga-cron-data'
folder = 'summaries/'
tickers_per_request = 5
downloader_index_mark= '[EOF]'

query="modules=assetProfile%2CsummaryDetail%2CesgScores%2Cprice%2CincomeStatementHistory%2CincomeStatementHistoryQuarterly%2CbalanceSheetHistory%2CbalanceSheetHistoryQuarterly%2CcashflowStatementHistory%2CcashflowStatementHistoryQuarterly%2CdefaultKeyStatistics%2CfinancialData%2CcalendarEvents%2CsecFilings%2CrecommendationTrend%2CupgradeDowngradeHistory%2CinstitutionOwnership%2CfundOwnership%2CmajorDirectHolders%2CmajorHoldersBreakdown%2CinsiderTransactions%2CinsiderHolders%2CnetSharePurchaseActivity%2Cearnings%2CearningsHistory%2CearningsTrend%2CindustryTrend%2CindexTrend%2CsectorTrend"
url_extra_query ='&lang=en-US&region=US&crumb=t5QZMhgytYZ&corsDomain=finance.yahoo.com'
headers = {'User-Agent': ''}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def load_file(s3_client, file_name):
    file_object= s3_client.get_object(Bucket=bucket_name, Key=file_name)
    file_data = file_object['Body'].read()
    return file_data.decode("utf-8")

def save_file(s3_client, file_name, content):
    s3_client.put_object(Body=content, Bucket=bucket_name, Key=file_name)

def get_tickers_names(s3_client):
    tickers_names = load_file(s3_client, '0000-excel-ark-movements-unique-sorted.csv')
    # separate lines and then remove empty lines
    return [y for y in (x.strip() for x in tickers_names.splitlines()) if y]

def get_downloader_index(s3_client):
    downloader_index = load_file(s3_client, '0000-cron-downloader-index.csv')
    values = downloader_index.split(',')
    if len(values) == 2:
        last_day = values[0]
        last_name = values[1]
    else:
        last_day = '2000-01-01'
        last_name = downloader_index_mark

    return (datetime.strptime(last_day, '%Y-%m-%d').date(), last_name)

def get_tickers_set(s3_client):
    tickers = get_tickers_names(s3_client)
    # print(f'tickers: {tickers}')

    (last_day, last_name)= get_downloader_index(s3_client)

    today= date.today()
    if (last_day < today):
        return (tickers[0:tickers_per_request], False)

    if last_name == downloader_index_mark:
        return ([], False)

    if last_name in tickers:
        last_name_index = tickers.index(last_name)
        if (last_name_index >= len(tickers)):
            return ([], True)
            
        return (tickers[last_name_index+1:last_name_index+1+tickers_per_request], False)

    logger.error(f'Last name "{last_name}" not found in tickets: {tickers}')
    return (tickers[0:tickers_per_request], False)

def run(event, context):
    start_time_string = datetime.now().strftime("%Y-%m-%d-%H%M")
    today_date_string= date.today().strftime("%Y-%m-%d")

    s3_client = boto3.client('s3')

    (tickers, save_eof) = get_tickers_set(s3_client)

    if len(tickers) == 0 and save_eof:
        save_file(s3_client, '0000-cron-downloader-index.csv', f'{today_date_string},[EOF]')

    for counter, ticker in enumerate(tickers):
        logger.info(f'ticker ({counter}): {ticker}')
        request_ticker = tc.convert_yahoo_name(ticker)
        if (request_ticker is None):
            logger.info('  > skipping ticker')
            continue

        quote_summary_url = f'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{request_ticker}?{query}{url_extra_query}'
        response = requests.get(quote_summary_url, headers=headers)
        if (response.ok):
            s3_client.put_object(Body=response.content, Bucket=bucket_name, Key=f'{folder}{today_date_string}/{start_time_string}-{request_ticker}.json')
        else:
            logger.error(f'Failed to retrieve: {request_ticker} response {response.status_code}')

        save_file(s3_client, '0000-cron-downloader-index.csv', f'{today_date_string},{ticker}')


if __name__ == "__main__":
    run()
