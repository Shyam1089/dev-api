FROM python:alpine3.7

RUN apk add --update --no-cache g++=6.4.0-r5 \
 gcc=6.4.0-r5 \
 libxslt-dev=1.1.31-r1 \
 build-base=0.5-r0 \
 linux-headers=4.4.6-r2

RUN apk add --no-cache --update \
    python3-dev \
    build-base=0.5-r0 \
    gcc=6.4.0-r5 \
    musl-dev=1.1.18-r3 && \
    apk add --no-cache --update postgresql-dev=10.8-r0 && \
    pip install psycopg2==2.7.5

RUN mkdir -p /app

WORKDIR /app

COPY requirements.pip /app/requirements.pip
RUN pip install -r /app/requirements.pip

COPY config/uwsgi.ini /etc/uwsgi.ini

COPY data_service/ /app/data_service/
COPY entrypoint.sh /app/

EXPOSE 8080

CMD ["sh", "/app/entrypoint.sh"]