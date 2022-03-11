# https://github.com/docker-library/python/blob/0f753da42f7ca178a073836c4532dc1433d6cac0/3.9/slim-buster/Dockerfile
FROM python:3.9-slim-buster


#### Serverless
## Installing NodeJS and npm

# Use root user to have permissions to install
USER root

# Installing NodeJS
RUN apt-get update -yq \
    && apt-get -yq install curl \
    && curl -L https://deb.nodesource.com/setup_16.x | bash \
    && apt-get update -yq \
    && apt-get install -yq \
        nodejs

RUN npm install -g serverless
RUN npm install -g serverless-offline
RUN npm install -g yarn

WORKDIR /usr/src

COPY package*.json ./

RUN yarn

EXPOSE 3000

#### Python requirements for the container

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .

#Create a virtual environment
RUN python3 -m venv /app
#Install the requirements
RUN python3 -m pip install -r requirements.txt

WORKDIR /usr/src/app
COPY ./src ./

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /usr/src
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "localstack/setup.py"]
