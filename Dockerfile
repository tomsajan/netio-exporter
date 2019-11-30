FROM python:3.8.0-alpine3.10

WORKDIR /netio

COPY netio_exporter.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

ENV NETIO_PORT 9595
EXPOSE 9595

ENTRYPOINT [ "python", "netio_exporter.py" ]