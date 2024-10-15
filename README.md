# Download Yahoo Finance stocks data using serverless.
Creates AWS lambda function that is triggered by a cron serverless `schedule` event.

## Description

A simple Python script that downloads Yahoo Finance finantial summary data and stores it in S3.
A lambda function is triggered multiple times during the day on a specified schedule. 
For each company on each day the donwloaded the data is stored in folder inside S3 bucket.

Lambda input is read from file `config.DOWNLOADER_TICKERS_FILE` and a index file `config.DOWNLOADER_INDEX_FILE` keeps track of the last ticker data downloaded.

## Environment Setup
The project defines a development container, `Dockerfile.dev`, that installs all the application requirements inside the container. This allows to work on the application in isolation from the host machine.

If using Visual Studio Code and Docker Desktop is running, press `F1` (or Ctrl+Shift+P) and select `Dev Containers: Rebuild and Reopen Container` to create the container.

Using [Serverless Framework](https://www.serverless.com/) with [Localstack](https://github.com/localstack/localstack) allows to create the AWS resources necessary so can execute and debug the application locally.

## Application Setup

Create a bucket in AWS S3 with name `config.BUCKET_NAME`
Create a folder inside this bucket with name `config.BUCKET_FOLDER` 
Create a file `config.TICKERS_DOWNLOAD_FILE` with the list of stock tickers want to download from Yahoo. One ticker Id for each line of the file.
Ticker names in the file should unique and ordered alphabetically.

## Requirements
All requeriments should be installed when opening VS Code usign the Docker.

## Deploy to AWS

- Set AWS credentials
```bash
  aws configure
```

- Perform deployment:
Register with [Serverless Framework](https://app.serverless.com/) to be able to deploy applications.

```bash
  serverless deploy --stage prd
```

## Working locally

- Local dependencies should have been installed with the `yarn` specified in `devcontainer.json` -> `postCreateCommand`.  

- Start serverless framework
```bash
yarn dev
```

- Call a lambda function specifying the name of the function in `serverless.yml`
```bash
serverless invoke local --function cronDownloader
```

- List the content of S3
Assuming files are stored in bucket `riga-cron-data`

```bash
aws s3api list-buckets --endpoint-url=http://localhost:4566
aws s3api list-objects --bucket riga-cron-data --query 'Contents[].{Key: Key, Size: Size}' --endpoint-url=http://localhost:4566
```

-Check lambdas defined

```bash
aws lambda list-functions --max-items 10 --endpoint-url=http://localhost:4566
```
## Next Steps
- Create S3 buckets with Terraform.

## References
- Serverless Getting started
  https://www.serverless.com/framework/docs/getting-started

- Serverless CLI reference
  https://www.serverless.com/framework/docs/providers/aws/cli-reference