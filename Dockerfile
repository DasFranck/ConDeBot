FROM python:3.9-alpine

RUN mkdir -p /app/ConDeBot /data/ConDeBot
WORKDIR /app/ConDeBot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apk -U add haveged && rc-service haveged start && rc-update add haveged

COPY . .
COPY ./docker/config ./config
RUN rm -r ./docker

ENTRYPOINT ["python", "./ConDeBot.py" ]
