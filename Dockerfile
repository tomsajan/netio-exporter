FROM python:3-alpine

WORKDIR /netio

COPY netio-exporter.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "netio-exporter.py" ]
