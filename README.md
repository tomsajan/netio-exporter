# netio-exporter
Prometheus exporter for NETIO PDUs

This program is designed to obtain metering information from various [Netio](https://www.netio-products.com/en/products/all-products) products and expose them in format scrapable by [Prometheus](https://prometheus.io/)


All NETIO products equipped with the ability to expose data via JSON are supported. Currently those are:
- [Netio 4ALL](https://www.netio-products.com/en/device/netio-4all) 
- [Netio 4](https://www.netio-products.com/en/device/netio-4) 
- [PowerPDU 4C](https://www.netio-products.com/en/device/powerpdu-4c) 
- [Powercable REST](https://www.netio-products.com/en/device/powercable-rest-101x) 

## Configuration
The `netio-exporter` can be configured both via `environment variables` and `commandline arguments`. The following options are available:

| ENV   |      CMDline      |  Description |
|----------|:-------------:|------:|
| NETIO_URL=<url> | `-u URL`, `--netio-url URL` | netio.json endpoint of the monitored Netio PDU. For example `http://192.168.0.1/netio.json` |
| NETIO_PORT=<port> | `-p PORT`, `--port PORT` | The port the exporter will listen at. The default is `9595`. This port is registered on [Prometheus](https://github.com/prometheus/prometheus/wiki/Default-port-allocations#exporters-starting-at-9100) to avoid clashes with other exporter |
| NETIO_USERNAME=<username> | `--username USERNAME` | Username used for authentication into the JSON API |
| NETIO_PASSWORD=<pass> | `--password PASSWORD` | Password used for authentication into the JSON API |
| NETIO_DEBUG=true | `d`, `--debug` | Turn on debug logging |
| NETIO_TIMEOUT=<timeout> | `t TIMEOUT`, `--timeout TIMEOUT` | Request timeout. In seconds |


## How to run?
### Native
`Python 3.6` or later is required due to the usage of [f-strings](https://realpython.com/python-f-strings/) and [type-hinting](https://docs.python.org/3/library/typing.html)
Install required python packages:
```
pip install -r requirements.txt
```

Start the exporter:
```
python netio_exporter.py [-h] [-p PORT] [-u URL] [--username USERNAME]
                         [--password PASSWORD] [-d] [-t TIMEOUT]
```

### Docker
Running the exporter in docker is also supported. There is also a pre-built image: [tomsajan/netio-exporter](https://hub.docker.com/r/tomsajan/netio-exporter/tags)
```
docker run -tid --name netio-exporter -p <port:port> -e <ENV_NAME>=<ENV_VAL> <image_name>:<image_tag>

``` 

For example
```
docker run -tid -p 9595:9595 -e NETIO_DEBUG=true -e NETIO_URL=http://192.168.0.242/netio.json -e NETIO_USERNAME=netio -e NETIO_PASSWORD=netio --name netio-exporter tomsajan/netio-exporter:latest 
```

The exporter will be available on the specified port for Prometheus scraping.

## Prometheus metrics
The exporter provides the following prometheus metrics:
