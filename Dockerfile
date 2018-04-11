FROM python:alpine3.7

RUN mkdir -p /app/ConDeBot
WORKDIR /app/ConDeBot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY ./docker/config ./config
COPY ./data /data/ConDeBot
RUN rm -r ./data ./docker

ENTRYPOINT ["python", "./ConDeBot.py" ]
