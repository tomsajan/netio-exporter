# netio-exporter
Prometheus exporter for NETIO PDUs

This program is designed to obtain metering information from various [Netio](https://www.netio-products.com/en/products/all-products) products and expose them in format scrapable by [Prometheus](https://prometheus.io/)


All NETIO products equipped with the ability to expose data via JSON are supported. Currently those are:
- [Netio 4ALL](https://www.netio-products.com/en/device/netio-4all) 
- [Netio 4](https://www.netio-products.com/en/device/netio-4) 
- [PowerPDU 4C](https://www.netio-products.com/en/device/powerpdu-4c) 
- [Powercable REST](https://www.netio-products.com/en/device/powercable-rest-101x) 

## Configuration
The `netio-exporter` can be configured both via `environment variables` and `commandline arguments`.
The CMDline arguments have the highest priority. The following options are available:

| ENV                       | CMDline                           | Default |Description |
|---------------------------|-----------------------------------|---------|-------------|
| NETIO_URL=<url>           | `-u URL`, `--netio-url URL`       | --------| netio.json endpoint of the monitored Netio PDU. For example `http://192.168.0.1/netio.json` |
| NETIO_PORT=<port>         | `-p PORT`, `--port PORT`          | `9595`  | The port the exporter will listen at. The default port is registered on [Prometheus](https://github.com/prometheus/prometheus/wiki/Default-port-allocations#exporters-starting-at-9100) to avoid clashes with other exportera |
| NETIO_USERNAME=<username> | `--username USERNAME`             | `netio` | Username used for authentication into the JSON API |
| NETIO_PASSWORD=<pass>     | `--password PASSWORD`             | `netio` | Password used for authentication into the JSON API |
| NETIO_DEBUG=true          | `-d`, `--debug`                   | `False` | Turn on debug logging |
| NETIO_TIMEOUT=<timeout>   | `-t TIMEOUT`, `--timeout TIMEOUT` | `5`     | Request timeout. In seconds |


Note: if no authentication (username, password) is required (turned off in NETIO), the default can be used as the credentials are not checked on the NETIO side.

## How to run?
### Native
`Python 3.6` or later is required due to the usage of [f-strings](https://realpython.com/python-f-strings/) and [type-hinting](https://docs.python.org/3/library/typing.html)

Install required python packages:
```
pip install -r requirements.txt
```

Start the exporter:
```
python netio-exporter.py [-h] [-p PORT] -u URL [--username USERNAME]
                         [--password PASSWORD] [-d] [-t TIMEOUT] [-v]
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

| Metric | Description | Unit |
|--------|-------------|------|
| netio_agent_info | Various info about the PDU, key-value information as labels | --- |
| netio_global_current_amperes | Global current | A |
| netio_global_energy_watthours_total | Total energy consumed | Wh |
| netio_global_frequency_hertz | Inlet frequency | Hz |
| netio_global_load_watts | Total PDU load | W |
| netio_global_power_factor_ratio | Global Power factor | --- |
| netio_global_voltage_volts | Inlet voltage | V |
| netio_port_current_amperes | Per port current | A |
| netio_port_energy_watthours_total | Per port consumed energy | Wh |
| netio_port_load_watts | Per port load | W |
| netio_port_power_factor_ratio | Per port power factor | --- |
| netio_port_state | Whether port is ON/OFF | --- |


An example output from a `PowerPDU 4C`
```
netio_agent_info{json_version="2.1",model="PowerPDU 4C",name="myNetio",outputs="4",sn="24:A4:2C:39:31:2E",target="http://192.168.0.121/netio.json",version="3.3.1"} 1.0
netio_global_current_amperes 0.23
netio_global_energy_watthours_total 543.0
netio_global_frequency_hertz 50.0
netio_global_load_watts 45.0
netio_global_power_factor_ratio 0.85
netio_global_voltage_volts 237.1
netio_port_current_amperes{id="1",name="output_1"} 0.194
netio_port_current_amperes{id="2",name="output_2"} 0.0
netio_port_current_amperes{id="3",name="output_3"} 0.0
netio_port_current_amperes{id="4",name="output_4"} 0.036000000000000004
netio_port_energy_watthours_total{id="1",name="output_1"} 204.0
netio_port_energy_watthours_total{id="2",name="output_2"} 0.0
netio_port_energy_watthours_total{id="3",name="output_3"} 0.0
netio_port_energy_watthours_total{id="4",name="output_4"} 338.0
netio_port_load_watts{id="1",name="output_1"} 45.0
netio_port_load_watts{id="2",name="output_2"} 0.0
netio_port_load_watts{id="3",name="output_3"} 0.0
netio_port_load_watts{id="4",name="output_4"} 0.0
netio_port_power_factor_ratio{id="1",name="output_1"} 0.99
netio_port_power_factor_ratio{id="2",name="output_2"} 0.0
netio_port_power_factor_ratio{id="3",name="output_3"} 0.0
netio_port_power_factor_ratio{id="4",name="output_4"} 0.1
netio_port_state{id="1",name="output_1"} 1.0
netio_port_state{id="2",name="output_2"} 0.0
netio_port_state{id="3",name="output_3"} 0.0
netio_port_state{id="4",name="output_4"} 1.0
```

## Grafana dashboard
The grafana dashboard for metrics from this exporter can be found [here](https://grafana.com/grafana/dashboards/12022)

**Happy hacking!**