# MIO

## TODO / NEXT TECHDAY

-Create a development container
https://code.visualstudio.com/docs/remote/create-dev-container
-Docker from Docker Compose
https://github.com/microsoft/vscode-dev-containers/tree/main/containers/docker-from-docker-compose

-Using Docker as a Dev Environment with VS Code
https://spin.atomicobject.com/2021/06/15/developing-docker-vs-code/
https://spin.atomicobject.com/2021/06/16/docker-development-container/

-MIO: How to assign IAM role to lambda so it doesn't need credentials to access AWS resources (s3...)
-MIO: How to deploy lambdas locally
+When list the lambdas in localstack displays []

-MIO: How to deploy lambdas to localstack locally
Article: Localstack with Terraform and Docker for running AWS locally
https://dev.to/mrwormhole/localstack-with-terraform-and-docker-for-running-aws-locally-3a6d

-MIO: How to trigger the lambdas locally

-MIO: How to deploy to AWS with Terraform

-MIO: How to deploy SQLite with permissions to write in AWS S3 file

## Instructions

-Regenerate image after a change
Ctrl+Shift+P -> Remote-Container: Rebuild and Reopen Container

- Serverless Getting started
  https://www.serverless.com/framework/docs/getting-started

-Installing prune

```
   sls plugin install -n serverless-prune-plugin
```

- Check if AWS CLI installed

```bash
  aws --version
```

- Setup credetials with IAM user name: pluralsight + (Ke passa)

```bash
  aws configure
```

-S3 commands

```bash
aws s3api list-buckets --endpoint-url=http://localhost:4566
aws s3api list-objects --bucket riga-cron-data --query 'Contents[].{Key: Key, Size: Size}' --endpoint-url=http://localhost:4566
```

-Check lambdas defined

```bash
aws lambda list-functions --max-items 10 --endpoint-url=http://localhost:4566
```

python3 ./functions/handler.py

aws lambda invoke --function-name testFunction --cli-binary-format raw-in-base64-out --payload file://event.json response.json

To test functions locally
serverless invoke local --function <serverless-function>
ex. serverless invoke local --function cronDownloader

To be able to include 3rd party dependencies in the `requirements.txt`
serverless plugin install -n serverless-python-requirements

The above adds `serverless-python-requirements` to `plugins` section in your `serverless.yml` file and adds it as a `devDependency` to `package.json` file. Now you will be able to add your dependencies to `requirements.txt` file and they will be automatically injected to Lambda package during build process.

-Deploy to AWS: https://serverless-stack.com/chapters/stages-in-serverless-framework.html
serverless deploy --stage prd

-AWS Cost
https://docs.google.com/spreadsheets/d/e/2PACX-1vR0gBoKn8BmtP1zVXvjZb1w6KmLE8YNd7W-6nXkQ_3EzKmPu9PMT6U8XuJ72Gr-ZW-UlLRl0yLFRI4_/pubhtml

====== INSTRUCTIONS IN THE REPO

# Serverless Framework Python Scheduled Cron on AWS

This template demonstrates how to develop and deploy a simple cron-like service running on AWS Lambda using the traditional Serverless Framework.

## Schedule event type

This examples defines two functions, `rateHandler` and `cronHandler`, both of which are triggered by an event of `schedule` type, which is used for configuring functions to be executed at specific time or in specific intervals. For detailed information about `schedule` event, please refer to corresponding section of Serverless [docs](https://serverless.com/framework/docs/providers/aws/events/schedule/).

When defining `schedule` events, we need to use `rate` or `cron` expression syntax.

### Rate expressions syntax

```pseudo
rate(value unit)
```

`value` - A positive number

`unit` - The unit of time. ( minute | minutes | hour | hours | day | days )

In below example, we use `rate` syntax to define `schedule` event that will trigger our `rateHandler` function every minute

```yml
functions:
  rateHandler:
    handler: handler.run
    events:
      - schedule: rate(1 minute)
```

Detailed information about rate expressions is available in official [AWS docs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html#RateExpressions).

### Cron expressions syntax

```pseudo
cron(Minutes Hours Day-of-month Month Day-of-week Year)
```

All fields are required and time zone is UTC only.

| Field        |     Values      |   Wildcards    |
| ------------ | :-------------: | :------------: |
| Minutes      |      0-59       |    , - \* /    |
| Hours        |      0-23       |    , - \* /    |
| Day-of-month |      1-31       | , - \* ? / L W |
| Month        | 1-12 or JAN-DEC |    , - \* /    |
| Day-of-week  | 1-7 or SUN-SAT  | , - \* ? / L # |
| Year         |     192199      |    , - \* /    |

In below example, we use `cron` syntax to define `schedule` event that will trigger our `cronHandler` function every second minute every Monday through Friday

```yml
functions:
  cronHandler:
    handler: handler.run
    events:
      - schedule: cron(0/2 * ? * MON-FRI *)
```

Detailed information about cron expressions in available in official [AWS docs](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html#CronExpressions).

## Usage

### Deployment

This example is made to work with the Serverless Framework dashboard, which includes advanced features such as CI/CD, monitoring, metrics, etc.

In order to deploy with dashboard, you need to first login with:

```
serverless login
```

and then perform deployment with:

```
serverless deploy
```

After running deploy, you should see output similar to:

```bash
Serverless: Packaging service...
Serverless: Excluding development dependencies...
Serverless: Uploading CloudFormation file to S3...
Serverless: Uploading artifacts...
Serverless: Uploading service aws-python-scheduled-cron.zip file to S3 (84.82 KB)...
Serverless: Validating template...
Serverless: Updating Stack...
Serverless: Checking Stack update progress...
........................
Serverless: Stack update finished...
Service Information
service: aws-python-scheduled-cron
stage: dev
region: us-east-1
stack: aws-python-scheduled-cron-dev
resources: 16
api keys:
  None
endpoints:
  None
functions:
  rateHandler: aws-python-scheduled-cron-dev-rateHandler
  cronHandler: aws-python-scheduled-cron-dev-cronHandler
layers:
  None
Serverless: Publishing service to the Serverless Dashboard...
Serverless: Successfully published your service to the Serverless Dashboard: https://app.serverless.com/xxxx/apps/xxxx/aws-python-scheduled-cron/dev/us-east-1
```

There is no additional step required. Your defined schedules becomes active right away after deployment.

### Local invocation

In order to test out your functions locally, you can invoke them with the following command:

```
serverless invoke local --function rateHandler
```

After invocation, you should see output similar to:

```bash
INFO:handler:Your cron function aws-python-scheduled-cron-dev-rateHandler ran at 15:02:43.203145
```

### Bundling dependencies

In case you would like to include 3rd party dependencies, you will need to use a plugin called `serverless-python-requirements`. You can set it up by running the following command:

```bash
serverless plugin install -n serverless-python-requirements
```

Running the above will automatically add `serverless-python-requirements` to `plugins` section in your `serverless.yml` file and add it as a `devDependency` to `package.json` file. The `package.json` file will be automatically created if it doesn't exist beforehand. Now you will be able to add your dependencies to `requirements.txt` file (`Pipfile` and `pyproject.toml` is also supported but requires additional configuration) and they will be automatically injected to Lambda package during build process. For more details about the plugin's configuration, please refer to [official documentation](https://github.com/UnitedIncome/serverless-python-requirements).

-Boto3: AWS SDK
https://towardsdatascience.com/introduction-to-pythons-boto3-c5ac2a86bb63
