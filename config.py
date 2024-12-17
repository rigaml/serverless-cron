# URL from where download the data
DOWNLOAD_URL = 'https://query1.finance.yahoo.com/v8/finance/chart/'

# Define fields to download
DOWNLOAD_URL_QUERY = "range=1d&interval=1m"

# Configuration setting for the download
DOWNLOAD_URL_EXTRA_QUERY = ''

# Name of the AWS S3 bbucket where the data will be stored
BUCKET_NAME = 'riga-cron-data'

# Subfolder of the AWS S3 bucket where the data will be stored
BUCKET_FOLDER = 'summaries/'

# Name of the S3 object that contains the list of tickers to download
DOWNLOADER_TICKERS_FILE = '0000-cron-downloader-tickers-unique-sorted.csv'

# Contains the last downloaded ticker or 'DOWNLOADER_INDEX_MARK' if all tickers have been downloaded
DOWNLOADER_INDEX_FILE = '0000-cron-downloader-index.csv'

# How many tickers will be downloaded on each lamba function call
TICKERS_PER_REQUEST = 5

# Value in the DOWNLOADER_INDEX_FILE that indicates that all tickers have been downloaded for the day
DOWNLOADER_EOF_MARK = '[EOF]'
