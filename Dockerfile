FROM python:alpine3.7

RUN mkdir -p /app/ConDeBot /data/ConDeBot
WORKDIR /app/ConDeBot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY ./docker/config ./config
RUN rm -r ./docker

ENTRYPOINT ["python", "./ConDeBot.py" ]
