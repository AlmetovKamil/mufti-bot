FROM python:3.12

USER bot
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

ADD bot.py .

CMD python3 ./bot.py