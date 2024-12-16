FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

COPY requirements.txt .

RUN apt-get update && apt-get install -y git && apt-get install -y nano && apt-get install -y procps && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

ADD bot.py .

CMD python3 ./bot.py