# Yahoo Finance Stock Data Downloader using AWS Lambda

A serverless AWS Lambda function that periodically downloads stock data from Yahoo Finance and stores it in an S3 bucket.

## Description

This project provides an AWS Lambda function that retrieves data from Yahoo Finance at scheduled intervals, based on a cron job. The retrieved data for each stock ticker is saved to a specific folder in an S3 bucket, with the tickers and schedule configurable.

The Lambda function reads input from `config.DOWNLOADER_TICKERS_FILE`, which contains a list of stock tickers, and uses `config.DOWNLOADER_INDEX_FILE` to track the last processed ticker, ensuring no data is missed.

## Features
- Scheduled Lambda function triggered multiple times daily.
- Data stored in a structured format in AWS S3.
- Uses Serverless Framework and Localstack for local development and testing.
  
## Environment Setup

The project includes a development environment with a Docker container (`Dockerfile.dev`) that installs all necessary dependencies inside the container. This ensures isolation from the host machine, allowing smooth development.

To get started with development:
- If using Visual Studio Code, rebuild and reopen the container by pressing `F1` (or `Ctrl+Shift+P`), then select `Dev Containers: Rebuild and Reopen Container`.
- Make sure Docker Desktop is running.

Serverless Framework, in combination with Localstack, simulates the AWS environment locally, enabling local execution and debugging.

## Application Setup

Before running the application, configure the following:
1. **S3 Bucket**: Create an S3 bucket with the name specified in `config.BUCKET_NAME`.
2. **S3 Folder**: Create a folder inside the bucket as defined in `config.BUCKET_FOLDER`.
3. **Tickers File**: Create a tickers file (`config.TICKERS_DOWNLOAD_FILE`) inside the bucket containing a list of Yahoo Finance stock ticker symbols, each on a new line, sorted alphabetically.

## Requirements

Ensure all dependencies are installed when opening the project in the Docker container (using Visual Studio Code with Dev Containers). The required libraries and dependencies will be set up automatically.

## Deploying to AWS

To deploy the Lambda function to AWS, follow these steps:

1. **Configure AWS Credentials**  
   Run the following command to configure your AWS CLI:
   ```bash
   aws configure
   ```

2. **Deploy with Serverless Framework**  
   You will need to register/login at the [Serverless Framework](https://app.serverless.com/) to deploy the application. Once registered/login, deploy using:
   ```bash
   serverless deploy --stage prd
   ```

## Running Locally

1. **Install Dependencies**  
   After building the development container, the Serverless/Node dependencies will be installed automatically through the `postCreateCommand` command specified in `devcontainer.json`.

2. **Start the Serverless Framework**  
   Start the local Serverless environment by running:
   ```bash
   yarn dev
   ```

3. **Run Localstack**  
   If using Localstack for local testing, run the following command on your host machine (not from the Dev container) to start the services:
   ```bash
   docker-compose -f docker-compose.yml up
   ```

4. **Invoke Lambda Locally**  
   Call the Lambda function locally by specifying the function name from `serverless.yml`:
   ```bash
   serverless invoke local --function cronDownloader
   ```

## Common local commands

- **Create a local S3 bucket**  
   ```bash
   aws s3api create-bucket --bucket your-unique-bucket-name --region us-east-1 --endpoint-url=http://localhost:4566
   ```

- **List S3 buckets**  
   ```bash
   aws s3api list-buckets --endpoint-url=http://localhost:4566
   ```

- **List objects in S3 bucket**  
   ```bash
   aws s3api list-objects --bucket your-unique-bucket-name --query 'Contents[].{Key: Key, Size: Size}' --endpoint-url=http://localhost:4566
   ```

- **List Lambda functions**  
   ```bash
   aws lambda list-functions --max-items 10 --endpoint-url=http://localhost:4566
   ```

## Future Enhancements
- Implement S3 bucket creation and management using Terraform for infrastructure as code.

## References
- [Serverless Framework: Getting Started](https://www.serverless.com/framework/docs/getting-started)
- [Serverless CLI Reference](https://www.serverless.com/framework/docs/providers/aws/cli-reference)