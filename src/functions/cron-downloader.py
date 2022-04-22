import boto3
import io
import datetime
import logging
import pandas as pd
import requests
from lib.ticker_converter import ticker_converter as tc

# https://towardsdatascience.com/introduction-to-amazon-lambda-layers-and-boto3-using-python3-39bd390add17

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

bucket_name = 'riga-cron-data'
query="modules=assetProfile%2CsummaryDetail%2CesgScores%2Cprice%2CincomeStatementHistory%2CincomeStatementHistoryQuarterly%2CbalanceSheetHistory%2CbalanceSheetHistoryQuarterly%2CcashflowStatementHistory%2CcashflowStatementHistoryQuarterly%2CdefaultKeyStatistics%2CfinancialData%2CcalendarEvents%2CsecFilings%2CrecommendationTrend%2CupgradeDowngradeHistory%2CinstitutionOwnership%2CfundOwnership%2CmajorDirectHolders%2CmajorHoldersBreakdown%2CinsiderTransactions%2CinsiderHolders%2CnetSharePurchaseActivity%2Cearnings%2CearningsHistory%2CearningsTrend%2CindustryTrend%2CindexTrend%2CsectorTrend"
url_extra_query ='&lang=en-US&region=US&crumb=t5QZMhgytYZ&corsDomain=finance.yahoo.com'
headers = {'User-Agent': ''}

start_date= datetime.now()
start_date_string = datetime.now().strftime("%Y-%m-%d-%H:%M")

def get_tickers(s3_client):
    movements_object= s3_client.get_object(Bucket=bucket_name, Key='0000-excel-ark-movements.xlsx')
    movements_data = movements_object['Body'].read()
    movements = pd.read_excel(io.BytesIO(movements_data), header=0)
    tickers = movements['Ticker'].unique()

    return tickers

def run(event, context):
    s3_client = boto3.client('s3')

    tickers = get_tickers(s3_client)

    for counter, ticker in enumerate(tickers):
        logger.info(f'ticker ({counter}): {ticker}')
        ticker = tc.ticker_converter.convert_yahoo_name(ticker)
        if (ticker is None):
            logger.info('  > skipping ticker')
            continue

        quote_summary = f'https://query2.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?{query}{url_extra_query}'
        response = requests.get(quote_summary, headers=headers)
        if (response.ok):
            s3_client.upload_fileobj(response.content, bucket_name, f'{start_date_string.replace(":", "")}-{ticker}.json')
        else:
            logger.info(f'Failed to retrieve: {ticker} response {response.status_code}')

if __name__ == "__main__":
    run()
